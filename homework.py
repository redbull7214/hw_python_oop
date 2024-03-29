from dataclasses import dataclass
from typing import List, Union


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {0}; '
                    'Длительность: {1:.3f} ч.; '
                    'Дистанция: {2:.3f} км; '
                    'Ср. скорость: {3:.3f} км/ч; '
                    'Потрачено ккал: {4:.3f}.')

    def get_message(self) -> str:
        returned_message = self.message.format(self.training_type,
                                               self.duration, self.distance,
                                               self.speed, self.calories)
        return returned_message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    mins_in_h: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
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
        info = (InfoMessage(type(self).__name__, self.duration,
                self.get_distance(), self.get_mean_speed(),
                self.get_spent_calories()))
        return info


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        coef_1: int = 18
        coef_2: int = 20
        spent_calories = ((coef_1 * self.get_mean_speed() - coef_2)
                          * self.weight / self.M_IN_KM
                          * self.duration * self.mins_in_h)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coef_1: float = 0.035
        coef_2: float = 0.029
        spent_calories = ((coef_1 * self.weight + (self.get_mean_speed()
                          ** 2 // self.height) * coef_2 * self.weight)
                          * self.duration * self.mins_in_h)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.lenght_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        const_1: float = 1.1
        const_2: int = 2
        spent_calories = ((self.get_mean_speed() + const_1)
                          * const_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: List[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    # Дико извиняюсь, упорно смотрел в определение функции а не переменной
    types: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return types[workout_type](*data)


def main(training: Training) -> None:
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
