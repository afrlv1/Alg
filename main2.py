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
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
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


class Running(Training):
    """Тренировка: бег."""
    RUN_COEFF_CALORIE: ClassVar[int] = 18
    COEFF_CALORIE_2: ClassVar[int] = 20
    VMIN: ClassVar[int] = 60

    def get_spent_calories(self) -> float:
        spent_calories = ((self.RUN_COEFF_CALORIE * self.get_mean_speed() - self.COEFF_CALORIE_2)
                          * self.weight / self.M_IN_KM * (self.duration * self.VMIN))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_3: ClassVar[float] = 0.035
    COEFF_CALORIE_4: ClassVar[float] = 0.029

    def __init__(self, action: int, duration: float, weight: float, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (self.COEFF_CALORIE_3 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_CALORIE_4 * self.weight) * (self.duration
                                                         * Running.VMIN)


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_calorie_5: ClassVar[float] = 1.1
    coeff_calorie_6: ClassVar[float] = 2.0
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
        spent_calories = (self.get_mean_speed() + self.coeff_calorie_5) * self.coeff_calorie_6 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Union[Running, SportsWalking, Swimming]:
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