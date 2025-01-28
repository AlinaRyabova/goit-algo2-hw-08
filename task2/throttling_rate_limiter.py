import time
from typing import Dict

class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0):
        """
        Ініціалізація rate limiter з мінімальним інтервалом між повідомленнями.
        :param min_interval: Мінімальний час у секундах між повідомленнями.
        """
        self.min_interval = min_interval
        self.last_message_time: Dict[str, float] = {}

    def can_send_message(self, user_id: str) -> bool:
        """
        Перевіряє, чи може користувач надіслати повідомлення.
        :param user_id: Ідентифікатор користувача.
        :return: True, якщо повідомлення дозволено, інакше False.
        """
        current_time = time.time()
        last_time = self.last_message_time.get(user_id, 0)

        # Дозволити, якщо користувач ще не надсилав повідомлення або інтервал перевищено
        return current_time - last_time >= self.min_interval

    def record_message(self, user_id: str) -> bool:
        """
        Реєструє повідомлення користувача, якщо це дозволено.
        :param user_id: Ідентифікатор користувача.
        :return: True, якщо повідомлення зареєстровано, інакше False.
        """
        if self.can_send_message(user_id):
            self.last_message_time[user_id] = time.time()
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        """
        Обчислює час до наступного дозволеного повідомлення.
        :param user_id: Ідентифікатор користувача.
        :return: Час у секундах до наступного дозволеного повідомлення.
        """
        current_time = time.time()
        last_time = self.last_message_time.get(user_id, 0)
        remaining_time = self.min_interval - (current_time - last_time)
        return max(0.0, remaining_time)
