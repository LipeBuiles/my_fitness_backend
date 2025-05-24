import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

from fastapi import FastAPI
from app.api.endpoints import router
from app.core.config import settings

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,  # 1.0 captura todas las transacciones, puedes ajustarlo
)

app = FastAPI()
app.include_router(router)
