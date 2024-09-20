# Кэш для функций факториала и Фибоначчи
factorial_cache = {}
fibonacci_cache = {}

async def app(scope, receive, send):
    assert scope['type'] == 'http'
    path = scope['path']
    query_string = scope['query_string'].decode()

    # Обработка GET-запросов
    if scope['method'] == 'GET':
        # Факториал
        if path.startswith('/factorial'):
            try:
                number = int(query_string.split('=')[1])
                result = factorial(number)
                await send_response(send, 200, str(result).encode())
            except (IndexError, ValueError):
                await send_response(send, 400, b'Error 400: Invalid input. Please provide a valid number.')

        # Число Фибоначчи
        elif path.startswith('/fibonacci'):
            try:
                number = int(query_string.split('=')[1])
                result = fibonacci(number)
                await send_response(send, 200, str(result).encode())
            except (IndexError, ValueError):
                await send_response(send, 400, b'Error 400: Invalid input. Please provide a valid number.')

        # Среднее значение
        elif path.startswith('/mean'):
            try:
                numbers = list(map(float, query_string.split('=')[1].split(',')))
                if not numbers:
                    raise ValueError('Empty list')
                result = mean_value(numbers)
                await send_response(send, 200, str(result).encode())
            except (IndexError, ValueError):
                await send_response(send, 400, b'Error 400: Invalid input. Please provide a valid list of numbers.')

        else:
            await send_response(send, 404, b'Error 404: The requested command was not found.')

    else:
        await send_response(send, 405, b'Error 405: Method Not Allowed.')


async def send_response(send, status_code: int, body: bytes):
    headers = [(b'content-type', b'text/plain')]
    await send({
        'type': 'http.response.start',
        'status': status_code,
        'headers': headers
    })
    await send({
        'type': 'http.response.body',
        'body': body
    })


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