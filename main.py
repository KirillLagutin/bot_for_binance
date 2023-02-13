####################################### Задание 1 #########################################
# Напишите код программы на Python, которая будет в реальном времени (с максимально
# возможной скоростью) считывать текущую цену фьючерса XRP/USDT на бирже Binance.
# В случае, если цена упала на 1% от максимальной цены за последний час,
# программа должна вывести сообщение в консоль.
# При этом программа должна продолжать работать дальше, постоянно считывая актуальную цену.
###########################################################################################
from binance.spot import Spot
from binance.error import ClientError

client = Spot()

symbol = "XRPUSDT"


# Максимальная цена за последнее указанное время (например:
# от '1m' до '59m', от '1h' до '23h', от '1d' до '7d'
def high_price_for_a_while(symbol: str, last_time: str):
    result = client.rolling_window_ticker(
        symbol,
        windowSize=last_time,
    ).get('highPrice')

    return float(result)


# Текущая цена - ticker_price()
def current_price(symbol: str):
    result = client.ticker_price(
        symbol,
    ).get('price')

    return float(result)


# Процент от максимальной цены за последний час
def percent_price(symbol: str, percent: float):
    result = high_price_for_a_while(symbol, '1h') / 100 * percent

    return float(result)


# Сообщение о том, что цена упала на ..% от максимальной цены за последний час
def show_message(symbol: str, percent: float):
    print(f"Price of pair[{symbol}] fell by {percent}% from the maximum price in the last hour!")


# Функция запуска с определённой парой
def run(symbol: str, percent: float = 1, last_time: str = '1h'):
    # Если 'цена <= разницы макс цены за последний час и процента от этой цены'
    if current_price(symbol) <= high_price_for_a_while(symbol, last_time) - percent_price(symbol, percent):
        # ...выводим сообщение
        show_message(symbol, percent)

    # Проверка для себя
    print(f"Макс цена[{symbol}] за последний час:                "
          f"{high_price_for_a_while(symbol, '1h')}")
    print(f"Макс цена[{symbol}] за последний час снижена на 1%:  "
          f"{high_price_for_a_while(symbol, '1h') - percent_price(symbol, 1)}")
    print(f"Текущая цена[{symbol}]:                              "
          f"{current_price(symbol)}\n")


# Запуск с определённой парой
while True:
    try:
        run(symbol)
    except ClientError as e:
        print(e.error_code, e.error_message)


####################################### Задание 2 #########################################
# Опишите, как бы вы доработали данную программу, чтобы она обрабатывала все пары,
# а не только XRP/USDT (код писать не нужно, просто текстом)
###########################################################################################

# Решение.
# Через pandas сделал выборку из ticket_price и через get() получил все символы.
# Потом в цикле засовывал каждый символ в одиночный метод run()
# Код написал, для себя, для тренировки


# Код для проверки всех пар
###########################################################################################

import pandas as pd

symbols = pd.DataFrame(client.ticker_price()).get('symbol')


# Функция для проверки всех пар
def multy_bot(symbols: list):
    i = 0

    while i < len(symbols):
        run(symbols[i])
        i += 1


# Чтоб сработал этот while нужно закомментировать while с определённой парой
while True:
    try:
        multy_bot(symbols)
    except ClientError as e:
        print(e.error_code, e.error_message)
