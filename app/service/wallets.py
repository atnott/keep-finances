from fastapi import HTTPException

from app.schemas import CreateWalletRequest
from app.repository import wallets as wallet_repository

def get_balance(wallet_name: str | None = None):
    # имя кошелька не указано - считаем общий баланс
    if wallet_name is None:
        wallets = wallet_repository.get_all_wallets()
        return {'total_balance': sum(wallets.values())}
    # проверяем, существует ли запрашиваемый кошелек
    if not wallet_repository.is_wallet_exist(wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )
    # возвращаем баланс конкретного кошелька
    balance = wallet_repository.get_wallet_balance_by_name(wallet_name)
    return {'wallet': wallet_name, 'balance': balance}

def create_wallet(wallet: CreateWalletRequest):
    # проверяем не существует ли уже такой кошелек
    if wallet_repository.is_wallet_exist(wallet.name):
        raise HTTPException(
            status_code=400,
            detail=f"Wallet '{wallet.name}' already exists"
        )

    # создаем новый кошелек с начальным балансом
    new_balance = wallet_repository.create_wallet(wallet.name, wallet.initial_balance)

    # возвращаем информацию о созданном кошельке
    return {
        'message': f"Wallet '{wallet.name}' created",
        'wallet': wallet.name,
        'balance': new_balance
    }