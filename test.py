# -*- coding: utf-8 -*-
"""
Модульные тесты для класса BankAccount (библиотека unittest).
Запуск: python -m unittest -v test_bank_account
"""

import unittest
from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """Перед каждым тестом создаём два свежих счёта."""
        self.acc1 = BankAccount("Айдана", "KG001")
        self.acc2 = BankAccount("Жайна", "KG002")

    # ---------- Создание счёта ----------
    def test_create_account(self):
        self.assertEqual(self.acc1.owner, "Айдана")
        self.assertEqual(self.acc1.account_number, "KG001")

    def test_initial_balance_is_zero(self):
        self.assertEqual(self.acc1.get_balance(), 0)

    def test_create_with_empty_owner(self):
        with self.assertRaises(ValueError):
            BankAccount("", "KG003")

    def test_create_with_empty_number(self):
        with self.assertRaises(ValueError):
            BankAccount("Айдана", "")

    # ---------- Пополнение ----------
    def test_deposit(self):
        self.acc1.deposit(500)
        self.assertEqual(self.acc1.get_balance(), 500)

    def test_deposit_twice(self):
        self.acc1.deposit(100)
        self.acc1.deposit(250)
        self.assertEqual(self.acc1.get_balance(), 350)

    def test_deposit_negative(self):
        with self.assertRaises(ValueError):
            self.acc1.deposit(-100)
        self.assertEqual(self.acc1.get_balance(), 0)

    def test_deposit_zero(self):
        with self.assertRaises(ValueError):
            self.acc1.deposit(0)

    def test_deposit_not_a_number(self):
        with self.assertRaises(ValueError):
            self.acc1.deposit("сто")

    # ---------- Снятие ----------
    def test_withdraw(self):
        self.acc1.deposit(1000)
        self.acc1.withdraw(400)
        self.assertEqual(self.acc1.get_balance(), 600)

    def test_withdraw_all_money(self):
        self.acc1.deposit(300)
        self.acc1.withdraw(300)
        self.assertEqual(self.acc1.get_balance(), 0)

    def test_withdraw_more_than_balance(self):
        self.acc1.deposit(100)
        with self.assertRaises(ValueError):
            self.acc1.withdraw(150)
        self.assertEqual(self.acc1.get_balance(), 100)  # баланс не изменился

    def test_withdraw_negative(self):
        self.acc1.deposit(100)
        with self.assertRaises(ValueError):
            self.acc1.withdraw(-50)
        self.assertEqual(self.acc1.get_balance(), 100)

    # ---------- Перевод ----------
    def test_transfer_success(self):
        self.acc1.deposit(1000)
        self.acc1.transfer(self.acc2, 300)
        self.assertEqual(self.acc1.get_balance(), 700)
        self.assertEqual(self.acc2.get_balance(), 300)

    def test_transfer_changes_are_equal(self):
        # Баланс отправителя уменьшился на столько же, на сколько вырос баланс получателя
        self.acc1.deposit(1000)
        self.acc2.deposit(200)
        before1 = self.acc1.get_balance()
        before2 = self.acc2.get_balance()

        self.acc1.transfer(self.acc2, 350)

        change1 = before1 - self.acc1.get_balance()
        change2 = self.acc2.get_balance() - before2
        self.assertEqual(change1, change2)

    def test_transfer_not_enough_money(self):
        self.acc1.deposit(100)
        self.acc2.deposit(50)
        with self.assertRaises(ValueError):
            self.acc1.transfer(self.acc2, 500)
        # состояние обоих счетов не изменилось
        self.assertEqual(self.acc1.get_balance(), 100)
        self.assertEqual(self.acc2.get_balance(), 50)

    def test_transfer_negative_amount(self):
        self.acc1.deposit(100)
        with self.assertRaises(ValueError):
            self.acc1.transfer(self.acc2, -10)
        self.assertEqual(self.acc1.get_balance(), 100)
        self.assertEqual(self.acc2.get_balance(), 0)

    def test_transfer_to_same_account(self):
        self.acc1.deposit(100)
        with self.assertRaises(ValueError):
            self.acc1.transfer(self.acc1, 50)
        self.assertEqual(self.acc1.get_balance(), 100)

    def test_transfer_to_not_account(self):
        self.acc1.deposit(100)
        with self.assertRaises(TypeError):
            self.acc1.transfer("KG002", 50)
        self.assertEqual(self.acc1.get_balance(), 100)

    # ---------- Баланс ----------
    def test_get_balance_after_operations(self):
        self.acc1.deposit(1000)
        self.acc1.withdraw(200)
        self.acc1.transfer(self.acc2, 300)
        self.acc1.deposit(50)
        self.assertEqual(self.acc1.get_balance(), 550)

    # ---------- Пустой счёт ----------
    def test_new_account_is_empty(self):
        self.assertTrue(self.acc1.is_empty())

    def test_account_with_money_is_not_empty(self):
        self.acc1.deposit(10)
        self.assertFalse(self.acc1.is_empty())

    def test_account_is_empty_after_withdraw_all(self):
        self.acc1.deposit(100)
        self.acc1.withdraw(100)
        self.assertTrue(self.acc1.is_empty())


if __name__ == "__main__":
    unittest.main()