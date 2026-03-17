from pydantic import BaseModel, Field, field_validator

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