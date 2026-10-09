
class BankAccount:

    def __init__(self, owner, account_number):
        """Создание счёта. Начальный баланс всегда равен 0."""
        if not isinstance(owner, str) or owner.strip() == "":
            raise ValueError("Имя владельца должно быть непустой строкой")
        if not isinstance(account_number, str) or account_number.strip() == "":
            raise ValueError("Номер счёта должен быть непустой строкой")

        self.owner = owner                    # имя владельца
        self.account_number = account_number  # номер счёта
        self.balance = 0                      # текущий баланс

    def _check_amount(self, amount):
        """Проверка суммы: >0"""
        # bool - это тоже int в Python, поэтому True/False исключаем отдельно
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise ValueError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля")

    def deposit(self, amount):
        """Пополнение счёта на сумму amount."""
        self._check_amount(amount)
        self.balance += amount

    def withdraw(self, amount):
        """Снятие денег со счёта."""
        self._check_amount(amount)
        if amount > self.balance:
            raise ValueError("Недостаточно средств на счёте")
        self.balance -= amount

    def transfer(self, other, amount):
        """Перевод денег на другой счёт (other)."""
      
        if not isinstance(other, BankAccount):
            raise TypeError("Получатель должен быть банковским счётом")
        if other is self:
            raise ValueError("Нельзя переводить деньги на тот же счёт")
        self._check_amount(amount)
        if amount > self.balance:
            raise ValueError("Недостаточно средств для перевода")

        self.balance -= amount
        other.balance += amount

    def get_balance(self):
        """Возвращает текущий баланс."""
        return self.balance

    def is_empty(self):
        """Счёт пустой, если баланс равен нулю."""
        return self.balance == 0


# Небольшая демонстрация (запускается только при прямом запуске файла)
if __name__ == "__main__":
    acc1 = BankAccount("Айдана", "KG001")
    acc2 = BankAccount("Жайна", "KG002")

    acc1.deposit(1000)
    acc1.withdraw(200)
    acc1.transfer(acc2, 300)

    print("Баланс acc1:", acc1.get_balance())  # 500
    print("Баланс acc2:", acc2.get_balance())  # 300
    print("acc1 пустой?", acc1.is_empty())     # False