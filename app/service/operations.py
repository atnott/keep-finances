from fastapi import HTTPException

from app.database import SessionLocal
from app.schemas import OperationRequest
from app.repository import wallets as wallet_repository

def add_income(operation: OperationRequest):
    # проверяем существует ли кошелек
    db = SessionLocal()
    try:
        if not wallet_repository.is_wallet_exist(db, operation.wallet_name):
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{operation.wallet_name}' not found"
            )

        # добавляем доход к балансу кошелька
        wallet = wallet_repository.add_income(db, operation.wallet_name, operation.amount)

        # возвращаем информацию об операции
        return {
            'message': "income added",
            'wallet': operation.wallet_name,
            'amount': operation.amount,
            'description': operation.description,
            'new_balance': wallet.balance
        }
    finally:
        db.close()

def add_expense(operation: OperationRequest):
    # проверяем существует ли кошелек
    db = SessionLocal()
    try:
        if not wallet_repository.is_wallet_exist(db, operation.wallet_name):
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{operation.wallet_name}' not found"
            )

        # хватает ли денег
        wallet = wallet_repository.get_wallet_balance_by_name(db, operation.wallet_name)
        if operation.amount > wallet.balance:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient founds. Available: '{wallet.balance}'"
            )

        # вычитаем расход из кошелька
        wallet = wallet_repository.add_expense(db, operation.wallet_name, operation.amount)

        # возвращаем информацию об операции
        return {
            'message': "Expense added",
            'wallet': operation.wallet_name,
            'amount': operation.amount,
            'description': operation.description,
            'new_balance': wallet.balance
        }
    finally:
        db.close()