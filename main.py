from fastapi import FastAPI, HTTPException

from app.api.v1.wallets import router as wallet_router
from app.api.v1.operations import router as operation_router

# инициализации FastAPI приложения
app = FastAPI()

app.include_router(wallet_router, prefix='/api/v1', tags=['wallet'])
app.include_router(operation_router, prefix='/api/v1', tags=['operations'])

