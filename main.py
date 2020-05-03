from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data.users import User
from data.requests import Request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    telephone_number = TelField("Номер телефона", validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    street = StringField('Улица', validators=[DataRequired()])
    building = StringField('Дом', validators=[DataRequired()])
    flat = StringField('Квартира')
    about = TextAreaField('Немного о себе')
    submit = SubmitField('Зарегистрироваться')


class RequestForm(FlaskForm):
    name = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField("Содержание")
    is_active = BooleanField("Личное")
    submit = SubmitField('Применить')


# добавляем запрос


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            telephone_number=form.telephone_number.data,
            address={"city": form.city.data, "street": form.street.data, "building": form.building.data,
                     "flat": form.flat.data},
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html")


flag_1 = True


@app.route("/profile")
def profile():
    global flag_1
    if flag_1:
        requests = current_user.outgoing_requests
    else:
        requests = current_user.ingoing_requests
    return render_template("profile.html", requests=requests, flag=flag_1)


@app.route("/profile/switch/ingoing")
def profile_switch_ingoing():
    global flag_1
    flag_1 = False
    return redirect("/profile")


@app.route("/profile/switch/outgoing")
def profile_switch_outgoing():
    global flag_1
    flag_1 = True
    return redirect("/profile")


@app.route('/request', methods=['GET', 'POST'])
@login_required
def add_news():
    form = RequestForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        request = Request()
        request.name = form.name.data
        request.description = form.description.data
        request.is_active = form.is_active.data
        request.sender_id = current_user.id
        current_user.outgoing_requests.append(request)
        session.merge(current_user)
        session.commit()
        return redirect('/profile')
    return render_template('request_edit.html', title='Добавление запроса',
                           form=form)


@app.route('/map')
def map():
    # отображение доступных меток от других людей
    session = db_session.create_session()
    requests = []
    for request in session.query(Request).all():
        user = session.query(User).filter(User.id == request.sender_id).first()
        address = ", ".join(
            [user.address["city"], user.address["street"], user.address["building"]])
        requests.append({"name": request.name,
                         "description": request.description,
                         "user": user.surname + " " + user.name,
                         "telephone": str(user.telephone_number),
                         "address": address
                         })
    print(requests[0]["address"])
    return render_template("map_2.html", requests=requests)


def main():
    db_session.global_init("db/users_requests.sqlite")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
