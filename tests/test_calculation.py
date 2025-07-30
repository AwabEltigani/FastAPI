from calculations.calculation import add, BankAccount
import pytest
from calculations.calculation import InsufficientFunds

#fixture:A function that gets run before any of your specific tests
@pytest.fixture
def zero_bank_account():
    return BankAccount(0)

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1,num2,expected_value",[
    (3,2,5),
    (3,1,4),
    (7,14,21),
    (19,20,39)
])




def test_add(num1,num2,expected_value):
    print("testing add function")
    assert add(num1,num2) == expected_value



def test_bank_set_inital_amount(bank_account):
    back_account = BankAccount(50)
    assert back_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    bank_account = BankAccount()
    assert bank_account.balance == 0
def test_withdraw(zero_bank_account):
    bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_collect_intrest(bank_account):
    bank_account.collectIntrest()
    assert round(bank_account.balance,2) == 55

@pytest.mark.parametrize("deposit,withdraw,expected", [
        (100, 20, 80),
        (1000, 1000, 0),
        (1490, 490, 1000),
    ] )

def test_bank_transaction(zero_bank_account,deposit,withdraw,expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

def test_insufficent_funds(zero_bank_account):
    zero_bank_account.deposit(10)
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(20)




