from dataclasses import asdict, dataclass
from typing import Dict, Type


# Можно лучше: рассказываем студентам про dataclass-ы
@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    # Надо исправить: студенты проходили аннотации в курсе, а значит
    # просим аннотировать все аттрибуты классов. Код должен проходить
    # проверку mypy/pyre/pylance итд.
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    # Можно лучше:
    # Объясняем студентам, что для сопровождения кода выгодно
    # разделять фразы и их примение.
    # Для этого такие фразы выносят в константы класса или модуля
    # а тут наполняют через .format()
    # Тогда, при уточнениях или даже
    # переводах фразы код метода не будет меняться.
    MESSAGE = (
        # Надо исправить:
        # 1) Для вывода тысячных долей
        #    (до третьего знака после запятой) используем .3f
        # 2) Скобки для переноса
        # 3) Приучаем к hanging-indent из код-стайла Django.
        'Тип тренировки: {training_type};'
        ' Длительность: {duration:.3f} ч.;'
        ' Дистанция: {distance:.3f} км;'
        ' Ср. скорость: {speed:.3f} км/ч;'
        ' Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        # Можно лучше (для продвинутых):
        # Рассказываем про, что при помощи asdict из dataclasses
        # можно элегантно передавать данные в format.
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    # Надо исправить: время выводится в часах, чтобы не умножать на 60
    # каждый раз, выводим константу в базовый класс.
    MIN_IN_H: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action: int = action
        # Можно лучше: рекомендуем избавиться от загадочности в значениях,
        # которые храняться в вещественных полях.
        # Для этого имя каждого поля дополнить единицей измерения:
        self.duration_h: float = duration
        self.weight_kg: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        # Можно лучше: рассказываем про вывод имени класса тренировки
        # через  type(self).__name__
        # (так используется меньше магических свойств)
        # или self.__class__.__name__.
        # обычно у студентов тут кастомные значения
        # или вовсе перепись метода в дочерних классах.
        return InfoMessage(
            type(self).__name__,
            self.duration_h,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    # Надо исправить: выносим константы на уровень класса.
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    # Можно лучше: просим дать константам более осмысленное,
    # содержательное имя.
    # Можно лучше: хинты для констант в вещественной формуле
    # лучше делать float, а не int.
    CALORIES_MEAN_SPEED_SHIFT: float = 20

    def get_spent_calories(self) -> float:
        cal_per_minute: float = (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                - self.CALORIES_MEAN_SPEED_SHIFT
            ) * self.weight_kg / self.M_IN_KM
        )
        # Надо исправить: см. выше про переменную MIN_IN_H
        return cal_per_minute * self.duration_h * self.MIN_IN_H


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm: float = height

    def get_spent_calories(self) -> float:
        cal_per_minute = (
            self.CALORIES_WEIGHT_MULTIPLIER * self.weight_kg
            + (self.get_mean_speed() ** 2 // self.height_cm)
            * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
            * self.weight_kg
        )
        # Надо исправить: см. выше про переменную MIN_IN_H
        return cal_per_minute * self.duration_h * self.MIN_IN_H


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: float = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool_m * self.count_pool
            / self.M_IN_KM / self.duration_h
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER * self.weight_kg
        )


def read_package(
    workout_type: str,
    data: list
) -> Training:
    """Прочитать данные полученные от датчиков."""
    # Надо исправить:
    # У 90% студентов на первой итерации тут простыня из ифов.
    # Им стоит намекнуть про словарь и объяснить на примере,
    # почему такая простыня - это плохо.
    # По заданию словарь должен быть в функции.
    # Можно лучше: просим проаннотировать с Type[Training]
    workout_type_classes: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    # Можно лучше: проверка наличие типа тренировки
    # с человекочитаемой ошибкой.
    # Также рассказываем про то,
    # что такое Guard Block, зачем это надо
    # и почему не нужно городить лишние отступы в коде.
    if workout_type not in workout_type_classes:
        allowed = ', '.join(workout_type_classes)
        # На всякий случай - проверка наличия ключа в словаре
        # делается так.
        # Студенты любят if workout_type not in workout_type_classes.keys()
        raise ValueError(
            f'Неизвестный тип тренировки: "{workout_type}".'
            f' Допустимые значения: "{allowed}".'
        )
    # Надо исправить: рассказываем студентам про распаковку значений через *
    # У студентов тут обычно вереница из if-ов и data[0], data[1]...
    return workout_type_classes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)