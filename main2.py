from dataclasses import dataclass
from typing import ClassVar, Type, Union


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TRAINING_TYPE_MSG: ClassVar[str] = 'Тип тренировки'
    DURATION_MSG: ClassVar[str] = 'Длительность'
    DISTANCE_MSG: ClassVar[str] = 'Дистанция'
    SPEED_MSG: ClassVar[str] = 'Ср. скорость'
    CALORIES_MSG: ClassVar[str] = 'Потрачено ккал'

    def get_message(self) -> str:
        message = (f'{self.TRAINING_TYPE_MSG}: {self.training_type}; '
                   f'{self.DURATION_MSG}: {self.duration:.3f} ч.; '
                   f'{self.DISTANCE_MSG}: {self.distance:.3f} км; '
                   f'{self.SPEED_MSG}: {self.speed:.3f} км/ч; '
                   f'{self.CALORIES_MSG}: {self.calories:.3f}.')
        return message


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[float] = 1000
    action: float
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
        raise NotImplementedError(
            'Определите get_spent_calories в %s.' % type(self).__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(type(self).__name__, self.duration,
                              self.get_distance(), self.get_mean_speed(),
                              self.get_spent_calories())
        return message


@dataclass
class Running(Training):
    """Тренировка: бег."""
    RUN_CALORIE_RATIO_1: ClassVar[float] = 18
    RUN_CALORIE_RATIO_2: ClassVar[float] = 20
    V_MIN: ClassVar[float] = 60

    def get_spent_calories(self) -> float:
        spent_calories = ((self.RUN_CALORIE_RATIO_1 * self.get_mean_speed()
                           - self.RUN_CALORIE_RATIO_2)
                          * self.weight / self.M_IN_KM *
                          (self.duration * self.V_MIN))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_CALORIE_RATIO_1: ClassVar[float] = 0.035
    WALK_CALORIE_RATIO_2: ClassVar[float] = 0.029

    def __init__(self, action: float, duration: float,
                 weight: float, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = (self.WALK_CALORIE_RATIO_1 * self.weight
                          + (self.get_mean_speed() ** 2 // self.height)
                          * self.WALK_CALORIE_RATIO_2 * self.weight) \
                         * (self.duration * Running.V_MIN)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    SWIM_CALORIE_RATIO_1: ClassVar[float] = 1.1
    SWIM_CALORIE_RATIO_2: ClassVar[float] = 2.0
    LEN_STEP: ClassVar[float] = 1.38

    def __init__(self, action: float, duration: float, weight: float,
                 length_pool: float, count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return distance

    def get_mean_speed(self):
        mean_speed = (self.length_pool * self.count_pool / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = (self.get_mean_speed() + self.SWIM_CALORIE_RATIO_1) \
                         * self.SWIM_CALORIE_RATIO_2 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list[int]) \
        -> Union[Type[Swimming],Type[Running], Type[SportsWalking], None]:
    """Прочитать данные полученные от датчиков."""
    read = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    package = read.get(workout_type)
    return package(*data) if package else None


def main(training: Type[Union[Swimming, Running, SportsWalking]]) -> None:
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
        main(training) if training else print('Неизвестный тип тренировки')
