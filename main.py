from fastapi import FastAPI, HTTPException

# инициализации FastAPI приложения
app = FastAPI()

# словарь для хранения балансов кошельков
# ключ - название кошелька, значение - баланс
BALANCE = {}

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
def receive_money(name: str, amount: int):
    # если кошелька с таким именем еще нет, создаем его с балансом 0
    if name not in BALANCE:
        BALANCE[name] = 0
    # добавляем сумму к балансу кошелька
    BALANCE[name] += amount
    # возвращаем информацию об операции
    return {
        'message': f'Added {amount} to {name}',
        'wallet': name,
        'new_balance': BALANCE[name]
    }