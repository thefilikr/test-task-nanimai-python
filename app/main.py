import asyncio
import uvicorn
from fastapi import FastAPI
from app.config import settings
from app.balance.api.http import router as balance_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
    )
    app.include_router(balance_router)
    return app

app = create_app()

async def run_http():
    config = uvicorn.Config("app.main:app", host="0.0.0.0", port=settings.HTTP_PORT, reload=True)
    server = uvicorn.Server(config)
    await server.serve()

async def run_grpc():
    import grpc
    from concurrent import futures
    import proto.balance_pb2_grpc as pb2_grpc
    from app.balance.api.grpc import BalanceServiceGRPC

    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_BalanceServiceServicer_to_server(BalanceServiceGRPC(), server)
    server.add_insecure_port(f'[::]:{settings.GRPC_PORT}')
    await server.start()
    print(f"gRPC server started on port {settings.GRPC_PORT}")
    await server.wait_for_termination()

async def main():
    await asyncio.gather(
        run_http(),
        run_grpc()
    )

if __name__ == "__main__":
    asyncio.run(main())