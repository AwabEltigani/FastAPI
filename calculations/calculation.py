def add(num1:int,num2:int):
    return num1+num2

class InsufficientFunds(Exception):
    pass


class BankAccount:
    def __init__(self,startingbalance = 0):
        self.balance = startingbalance

    def deposit(self,amount):
        self.balance += amount
    def withdraw(self,amount):
        if(amount > self.balance):
            raise InsufficientFunds ("Insufficient funds in account")
        self.balance -= amount
    def collectIntrest(self):
        self.balance *= 1.1