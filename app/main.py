
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.config import PORT
from app.db import get_session, init_db
from app.graphql.schema import schema
from app.logger import logger

app = FastAPI(title="Routes Microservice")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://54.225.75.133:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_context(request: Request):
    session_generator = get_session()
    session = await session_generator.__anext__()
    request.state.session_generator = session_generator
    return {
        "request": request,
        "session": session,
    }


@app.middleware("http")
async def close_db_session(request: Request, call_next):
    response = None
    try:
        response = await call_next(request)
    finally:
        session_gen = getattr(request.state, "session_generator", None)
        if session_gen:
            await session_gen.aclose()
    return response


graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/api/routes")


@app.on_event("startup")
async def startup_event():
    await init_db()
    logger.info("🚀 Microservicio ms-routes iniciado y conectado a PostgreSQL")
