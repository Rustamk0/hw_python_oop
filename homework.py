from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    MIN_IN_H = 60
    LEN_STEP = 0.65

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER_1 = 18
    CALORIES_MEAN_SPEED_SHIFT_2 = 1.79

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER_1 * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT_2) * self.weight
            / self.M_IN_KM * (self.duration * self.MIN_IN_H)
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_WEIGHT_1 = 0.035
    CALORIES_MEAN_WEIGHT_2 = 0.029
    CALORIES_MEAN_WEIGHT_3 = 2
    SM_IN_M = 100
    M_IN_KM = 1000
    SECOND_IN_M = 60
    MIN_IN_H = 60
    KM_IN_MSEC = round(M_IN_KM / MIN_IN_H / SECOND_IN_M, 3)

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_WEIGHT_1 * self.weight
             + (self.get_mean_speed() * self.KM_IN_MSEC)
             ** self.CALORIES_MEAN_WEIGHT_3 / (self.height / self.SM_IN_M)
             * self.CALORIES_MEAN_WEIGHT_2 * self.weight)
            * (self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MID_SPEED: float = 1.1
    CALORIES_WEIGHT: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIES_MID_SPEED)
                * self.CALORIES_WEIGHT * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    TRAINING_TYPES = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking, }
    if workout_type not in TRAINING_TYPES:
        print('Ошибка данных')
    else:
        return TRAINING_TYPES[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == "__main__":
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
