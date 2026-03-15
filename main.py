from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# инициализации FastAPI приложения
app = FastAPI()

# словарь для хранения балансов кошельков
# ключ - название кошелька, значение - баланс
BALANCE = {}

class OperationRequest(BaseModel):
    wallet_name: str
    amount: float
    description: str | None = None


@app.get('/balance')
def get_balance(wallet_name: str | None = None):
    # имя кошелька не указано - считаем общий баланс
    if wallet_name is None:
        return {'total_balance': sum(BALANCE.values())}
    # проверяем, существует ли запрашиваемый кошелек
    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )
    # возвращаем баланс конкретного кошелька
    return {'wallet': wallet_name, 'balance': BALANCE[wallet_name]}

@app.post('/wallets/{name}')
def create_wallet(name: str, initial_balance: float = 0):
    # проверяем не существует ли уже такой кошелек
    if name in BALANCE:
        raise HTTPException(
            status_code=400,
            detail=f"Wallet '{name}' already exists"
        )
    # создаем новый кошелек с начальным балансом
    BALANCE[name] = initial_balance
    # возвращаем информацию о созданном кошельке
    return {
        'message': f"Wallet '{name}' created",
        'wallet': name,
        'balance': initial_balance
    }

@app.post('/operations/income')
def add_income(operation: OperationRequest):
    # проверяем существует ли кошелек
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )
    # проверяем положительна ли сумма
    if operation.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail='Amount must be positive'
        )
    # добавляем доход к балансу кошелька
    BALANCE[operation.wallet_name] += operation.amount
    # возвращаем информацию об операции
    return {
        'message': "income added",
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': BALANCE[operation.wallet_name]
    }

@app.post('/operations/expense')
def add_expense(operation: OperationRequest):
    # проверяем существует ли кошелек
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )
    # положительна ли сумма
    if operation.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail='Amount must be positive'
        )
    # хватает ли денег
    if operation.amount > BALANCE[operation.wallet_name]:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient founds. Available: '{BALANCE[operation.wallet_name]}'"
        )
    # вычитаем расход из кошелька
    BALANCE[operation.wallet_name] -= operation.amount
    # возвращаем информацию об операции
    return {
        'message': "Expense added",
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': BALANCE[operation.wallet_name]
    }
