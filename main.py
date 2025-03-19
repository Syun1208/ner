import os
import sys
import uvicorn
import warnings
warnings.filterwarnings('ignore')

import logging

import psutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from dependency_injector.wiring import Provide, inject

from src.module.application_container import ApplicationContainer
from src.service.interface.arb_service.arb_service import ARBService
from src.controller.arb_controller import arb_router
from src.controller import arb_controller 
from src.utils.utils import load_yaml



@inject
def create_app(env: str) -> FastAPI:
    config = load_yaml(f"config/{env}.yml")
    app = FastAPI(
        title=f"{config['default']['app_name']} | {config['default']['env']}", 
        description="""<h2>Made by S.A.I team (Key members: Hani, Leon)</h2>"""
    )
    
    application_container = ApplicationContainer()
    application_container.wire(modules=["src.module.application_container"])

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    env = os.environ['APP_MODE']

    modules = [
        sys.modules[__name__]
        , arb_controller
    ]

    application_container.config.from_yaml(f"config/{env}.yml")
    application_container.wire(modules)
    app.container = application_container
    app.include_router(arb_router)

    logging.info("Wire completed")
    logging.basicConfig(level=logging.INFO)

    return app, config

def setup_di_modules(env: str):
    modules = [
        sys.modules[__name__],
        arb_controller
    ]

    application_container = ApplicationContainer()
    application_container.config.from_yaml(f"config/{env}.yml")
    application_container.wire(modules)


@inject
def run(

        arb_service: ARBService = Provide[ApplicationContainer.arb_service]
):
    # indexing thì mở comment dòng dưới
    #arb_service.indexing_knowledge(chunking_approach_id = 2, model_embedding_approach_id = 1)
    ans = arb_service.search(query="Chỉ tiêu tuyển sinh của ngành Công nghệ thông tin (Chương trình Tăng Cường Tiếng Anh) trường đại học Khoa học Tự nhiên năm 2024 là bao nhiêu?")
    print(ans)

os.environ['APP_MODE'] = sys.argv[1] if len(sys.argv) > 1 else 'development'
app, config = create_app(env=os.environ['APP_MODE']) 
if __name__ == "__main__":   
    uvicorn.run(
        app='main:app', 
        host=config['server']['http']['host'], 
        port=int(config['server']['http']['port']), 
        reload=True, 
        workers=psutil.cpu_count(logical=False), 
        timeout_keep_alive=20
    )