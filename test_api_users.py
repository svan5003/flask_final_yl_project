from requests import get, post, put, delete

print('Проверяем GET запрос для  UserResource')
print(get('http://localhost:8080/api/user/1').json())
# обработка несуществующего запроса
print(get('http://localhost:8080/api/user/1000').json())

print('Проверяем GET запрос для  UserListResource')
print(get('http://localhost:8080/api/user').json())

print('Проверяем POST запрос')
# пустой запрос
print(post('http://localhost:8080/api/user').json())
# неполный запрос
print(post('http://localhost:8080/api/user',
           json={'name': 'Имя'}).json())
print(post('http://localhost:8080/api/user',
           json={'name': 'Имя',
                 'surname': 'Фамилия',
                 'about': 'Текст новости',
                 'address': {'city': 'Сочи', 'street': 'Дарвина', 'building': '60', 'flat': '5'},
                 'telephone_number': '79187777777',
                 'email': 'poopybuthole@gmail.com',
                 'password': 'lolkek2014'}).json())

print('Проверяем DELETE запрос')
print(delete('http://localhost:8080/api/user/3').json())
# неверный DELETE запрос
print(delete('http://localhost:8080/api/user/999').json())

print('Проверяем PUT запрос')
print(put('http://localhost:8080/api/user/1',
          json={'about': 'шрек это кек'}).json())
# некорректный запрос
print(put('http://localhost:8080/api/user/999',
          json={'about': 'шрек это кек'}).json())
