from fastapi import HTTPException

from app.schemas import OperationRequest
from app.repository import wallets as wallet_repository

def add_income(operation: OperationRequest):
    # проверяем существует ли кошелек
    if not wallet_repository.is_wallet_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    # добавляем доход к балансу кошелька
    new_balance = wallet_repository.add_income(operation.wallet_name, operation.amount)

    # возвращаем информацию об операции
    return {
        'message': "income added",
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': new_balance
    }

def add_expense(operation: OperationRequest):
    # проверяем существует ли кошелек
    if not wallet_repository.is_wallet_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    # хватает ли денег
    balance = wallet_repository.get_wallet_balance_by_name(operation.wallet_name)
    if operation.amount > balance:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient founds. Available: '{balance}'"
        )

    # вычитаем расход из кошелька
    new_balance = wallet_repository.add_expense(operation.wallet_name, operation.amount)

    # возвращаем информацию об операции
    return {
        'message': "Expense added",
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': new_balance
    }