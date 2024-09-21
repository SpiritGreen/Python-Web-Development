import json

# Кэш для функций факториала и Фибоначчи
factorial_cache = {}
fibonacci_cache = {}

async def app(scope, receive, send) -> None:
    assert scope['type'] == 'http'
    path = scope['path']
    query_string = scope['query_string'].decode()

    # Обработка GET-запросов
    if scope['method'] == 'GET':
        # Факториал
        if path.startswith('/factorial'):
            try:
                # Извлечение параметра n: int из query_string
                params = dict(q.split('=') for q in query_string.split('&'))
                
                # Error 422 - Unprocessable entity (нет параметра)
                if 'n' not in params:
                    return await send_response(send, 422, {'error': "Missing parameter 'n'."})
                
                # Error 400 - Bad request
                n = int(params['n'])
                if n < 0:
                    return await send_response(send, 400, {'error': "Parameter 'n' must be a non-negative integer."})
                
                result = factorial(n)
                await send_response(send, 200, {'result': result})
            
            except (IndexError, ValueError):
                # Error 422 - Unprocessable entity (параметр не целое число)
                await send_response(send, 422, {'error': "Parameter 'n' must be a non-negative integer."})

        # Число Фибоначчи
        elif path.startswith('/fibonacci'):
            try:
                # Извлечение параметра n: int из query_string
                params = dict(q.split('=') for q in query_string.split('&'))

                # Error 422 - Unprocessable entity (нет параметра)
                if 'n' not in params:
                    return await send_response(send, 422, {'error': "Missing parameter 'n'."})
                
                # Error 400 - Bad request
                n = int(params['n'])
                if n < 0:
                    return await send_response(send, 400, {'error': "Parameter 'n' must be a non-negative integer."})
                
                result = fibonacci(n)
                await send_response(send, 200, {'result': result})
            
            except (IndexError, ValueError):
                # Error 422 - Unprocessable entity (параметр не целое число)
                await send_response(send, 422, {'error': "Parameter 'n' must be a non-negative integer."})

        # Среднее значение
        elif path.startswith('/mean'):
            try:
                body_bytes = await receive_body(receive)
                numbers = json.loads(body_bytes)

                # Error 400 - Bad request
                if not isinstance(numbers, list) or not numbers:
                    return await send_response(send, 400, {'error': 'The array cannot be empty'})

                result = mean_value(numbers)
                await send_response(send, 200, {'result': result})

            except (IndexError, ValueError):
                # Error 422 - Unprocessable entity (тело не является массивом float'ов)
                await send_response(send, 422, {'error': "Request body must be a non-empty array of floats."})

        else:
            # Error 404 - Not found
            await send_response(send, 404, {'error': 'Not Found'})

    else:
        # Error 405 - Method Not Allowed
        await send_response(send, 405, {'error': 'Method Not Allowed.'})


async def send_response(send, status_code: int, body: dict) -> None:
    headers = [(b'content-type', b'application/json')]
    body_bytes = json.dumps(body).encode()

    await send({
        'type': 'http.response.start',
        'status': status_code,
        'headers': headers
    })

    await send({
        'type': 'http.response.body',
        'body': body_bytes
    })


async def receive_body(receive) -> bytes:
    message = await receive()
    return message.get('body')


# Вычисляет факториал числа n
def factorial(n: int) -> int:
    if n < 0:
        raise ValueError('Negative number')

    # Проверка, есть ли значение в кэше
    if n in factorial_cache:
        return factorial_cache[n]

    if n == 0:
        return 1

    result = n * factorial(n - 1)
    # Сохраняем результат в кэш
    factorial_cache[n] = result
    return result


# Вычисляет n-е число Фибоначчи
def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError('Negative number')

    # Проверка, есть ли значение в кэше
    if n in fibonacci_cache:
        return fibonacci_cache[n]

    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        result = fibonacci(n - 1) + fibonacci(n - 2)
        # Кэшируем результат
        fibonacci_cache[n] = result
        return result


# Возвращает среднее значение списка чисел
def mean_value(numbers: list) -> float:
    return sum(numbers) / len(numbers)