from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

# инициализации FastAPI приложения
app = FastAPI()

# словарь для хранения балансов кошельков
# ключ - название кошелька, значение - баланс
BALANCE = {}

class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: float
    description: str | None = Field(None, max_length=255)

    # валидатор для проверки, что сумма положительная
    @field_validator('amount')
    def amount_must_be_positive(cls, v: float) -> float:
        # проверяем, что значение > 0
        if v <= 0:
            raise ValueError("Amount must be positive")
        # возвращаем, если все хорошо
        return v

    @field_validator('wallet_name')
    def wallet_name_not_empty(cls, v: str) -> str:
        # убираем пробелы по краям
        v = v.strip()
        # строка не пустая
        if len(v) == 0:
            raise ValueError("Wallet name must not be empty")
        # возвращаем очищенное значение
        return v

class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: float = 0

    @field_validator('initial_balance')
    def balance_not_negative(cls, v: float) -> float:
        # проверяем, что значение > 0
        if v < 0:
            raise ValueError("initial_balance cannot be negative")
        # возвращаем, если все хорошо
        return v

    @field_validator('name')
    def name_not_empty(cls, v: str) -> str:
        # убираем пробелы по краям
        v = v.strip()
        # строка не пустая
        if len(v) == 0:
            raise ValueError("Wallet name must not be empty")
        # возвращаем очищенное значение
        return v

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

@app.post('/wallets')
def create_wallet(wallet: CreateWalletRequest):
    # проверяем не существует ли уже такой кошелек
    if wallet.name in BALANCE:
        raise HTTPException(
            status_code=400,
            detail=f"Wallet '{wallet.name}' already exists"
        )
    # создаем новый кошелек с начальным балансом
    BALANCE[wallet.name] = wallet.initial_balance
    # возвращаем информацию о созданном кошельке
    return {
        'message': f"Wallet '{wallet.name}' created",
        'wallet': wallet.name,
        'balance': BALANCE[wallet.name]
    }

@app.post('/operations/income')
def add_income(operation: OperationRequest):
    # проверяем существует ли кошелек
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
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
