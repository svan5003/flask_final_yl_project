from requests import get, post, put, delete

print('Проверяем GET запрос для  RequestResource')
print(get('http://localhost:8080/api/request/2').json())
# обработка несуществующего запроса
print(get('http://localhost:8080/api/request/1000').json())

print('Проверяем GET запрос для  RequestListResource')
print(get('http://localhost:8080/api/request').json())

print('Проверяем POST запрос')
# пустой запрос
print(post('http://localhost:8080/api/request').json())
# неполный запрос
print(post('http://localhost:8080/api/request',
           json={'name': 'Заголовок'}).json())
print(post('http://localhost:8080/api/request',
           json={'name': 'Заголовок',
                 'description': 'Текст новости',
                 'address': 'Сочи, Апшеронская, 5',
                 'sender_id': 1,
                 'is_active': True}).json())

print('Проверяем DELETE запрос')
print(delete('http://localhost:8080/api/request/9').json())
# неверный DELETE запрос
print(delete('http://localhost:8080/api/request/999').json())

print('Проверяем PUT запрос')
print(put('http://localhost:8080/api/request/9',
          json={'name': 'new новый Заголовок',
                'is_active': 0}).json())
