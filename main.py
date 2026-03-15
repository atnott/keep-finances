from fastapi import FastAPI
from fastapi.responses import Response

# инициализации FastAPI приложения
app = FastAPI()

# делаем health check endpoint
@app.get('/health')
def health_check(): return Response(status_code=200)