# Домашнее задание по теме "Блокировки и обработка ошибок"
import threading
from random import randint
import time

# Класс Bank для управления балансом и потоками
class Bank:
    def __init__(self):
        self.balance : int = 0 # Инициализация начального баланса
        self.lock = threading.Lock() # Создание объекта Lock для синхронизации доступа к ресурсам

    # Метод для пополнения счета
    def deposit(self):
        for _ in range(100): # Цикл для совершения 100 транзакций пополнения
            the_amount_to_be_replenished = randint(50, 500)  # Генерация случайной суммы пополнения
            self.balance += the_amount_to_be_replenished # Увеличение баланса
            if self.balance >= 500 and self.lock.locked(): # Если баланс достиг 500 и замок закрыт
                self.lock.release()  # Разблокируем замок
            print(f"Пополнение: {the_amount_to_be_replenished}. Баланс: {self.balance}") # Вывод информации о пополнении
            time.sleep(0.001)  # Имитация времени обработки операции

    # Метод для снятия денег
    def take(self):
        for _ in range(100):  # Цикл для совершения 100 транзакций снятия
            the_amount_to_be_withdrawn = randint(50, 500)  # Генерация случайной суммы снятия
            print(f"Запрос на {the_amount_to_be_withdrawn}")
            if the_amount_to_be_withdrawn <= self.balance:  # Проверка наличия достаточного количества средств
                self.balance -= the_amount_to_be_withdrawn  # Уменьшение баланса
                print(f"Снятие: {the_amount_to_be_withdrawn}. Баланс: {self.balance}")  # Вывод информации о снятии
            else:
                print("Запрос отклонён, недостаточно средств")  # Сообщение об отказе в случае недостатка средств
                self.lock.acquire()  # Закрытие замка, чтобы предотвратить дальнейшие действия с балансом
            time.sleep(0.001)  # Имитация времени обработки операции


if __name__ == "__main__":
    # Создаем экземпляр класса Bank
    bk = Bank()
    # Создаем два потока для вызова методов deposit и take
    th1 = threading.Thread(target=Bank.deposit, args=(bk,))
    th2 = threading.Thread(target=Bank.take, args=(bk,))
    # Запускаем оба потока
    th1.start()
    th2.start()
    # Ожидаем завершения обоих потоков
    th1.join()
    th2.join()
    # Выводим итоговый баланс
    print(f'Итоговый баланс: {bk.balance}')