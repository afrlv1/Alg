from dataclasses import dataclass
from typing import Union, ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'длительность: {self.duration:.3f} ч.; '
                   f'дистанция: {self.distance:.3f} км; '
                   f'ср. скорость: {self.speed:.3f} км/ч; '
                   f'потрачено ккал: {self.calories:.3f}.')
        return message


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(type(self).__name__, self.duration, self.get_distance(),
                              self.get_mean_speed(), self.get_spent_calories())
        return message


@dataclass
class Running(Training):
    """Тренировка: бег."""
    RUN_CALORIE_RATIO_1: ClassVar[int] = 18
    RUN_CALORIE_RATIO_2: ClassVar[int] = 20
    V_MIN: ClassVar[int] = 60

    def get_spent_calories(self) -> float:
        spent_calories = ((self.RUN_CALORIE_RATIO_1 * self.get_mean_speed() - self.RUN_CALORIE_RATIO_2)
                          * self.weight / self.M_IN_KM * (self.duration * self.V_MIN))
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_CALORIE_RATIO_1: ClassVar[float] = 0.035
    WALK_CALORIE_RATIO_2: ClassVar[float] = 0.029

    def __init__(self, action: int, duration: float, weight: float, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = (self.WALK_CALORIE_RATIO_1 * self.weight + (self.get_mean_speed() ** 2 // self.height)
                          * self.WALK_CALORIE_RATIO_2 * self.weight) * (self.duration * Running.V_MIN)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    SWIM_CALORIE_RATIO_1: ClassVar[float] = 1.1
    SWIM_CALORIE_RATIO_2: ClassVar[float] = 2.0
    LEN_STEP: ClassVar[float] = 1.38

    def __init__(self, action: int, duration: float, weight: float, length_pool: float, count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return distance

    def get_mean_speed(self):
        mean_speed = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = (self.get_mean_speed() + self.SWIM_CALORIE_RATIO_1) * self.SWIM_CALORIE_RATIO_2 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list):
    """Прочитать данные полученные от датчиков."""
    read = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    package = read.get(workout_type)(*data)
    return package


def main(training: Union[Running, SportsWalking, Swimming]) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
