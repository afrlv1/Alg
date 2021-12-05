import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):  # date=''-> date=None
        self.amount = amount
        # Можно так указать dt.datetime.now().date() -> dt.date.today()
        # Перенос строк не очень красивый на мой взгляд. Я бы сделал в одну строку
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:  # Record -> record С большой буквы записывают название класса
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()  # Можно так указать dt.datetime.now().date() -> dt.date.today()
        for record in self.records:
            if (
                (today - record.date).days < 7 and  # Я бы сделал попроще -> 7 > (today - record.date).days >= 0
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')   # Можно и без скобок. Так тоже работает и можно без else Так как всего два варианта
                                        # завершения цикла .


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):  # Константы уже указаны.
                                                                          # Нет необходимости указывать тут повторно
                                                                          # либо название параметра надо писать
                                                                          # в маленьких буквах
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        #  Весь этот блок можно записать в Dict в котором прописываем
        #  обозначения валют и соотносим обозначения с курсом
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00   # Случайно два знака равно
            currency_type = 'руб'
        # для улучшения читаемости, я бы оставил строку. Логически тут уже другой блок
        if cash_remained > 0:
            # Вычислять в f строках - не корректно. Лучше ее отдельно посчитать
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:

            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    # Можно отдельно определять строку типа response = '....'
    # и после цилка if ilse возвращать return response
    # И можно просто if без elif


    # не совсем понятно, для чего мы вызываем еще раз этот параметр.
    def get_week_stats(self):
        super().get_week_stats()
        # PEP 8: W292 Необходим оставлять строчку в конце файла
