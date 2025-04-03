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
from src.controller.arb_controller import arb_router
from src.controller.arb_key_controller import key_router
from src.controller import arb_controller 
from src.utils.utils import load_yaml



@inject
def create_app(env: str) -> FastAPI:
    config = load_yaml(f"./config/{env}.yml")
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
    application_container.config.from_yaml(f"config/chunking_config.yml")
    application_container.config.from_yaml(f"config/model_embedding_config.yml")
    application_container.wire(modules)
    app.container = application_container
    app.include_router(arb_router)
    app.include_router(key_router)

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
    application_container.config.from_yaml(f"config/chunking_config.yml")
    application_container.config.from_yaml(f"config/model_embedding_config.yml")
    application_container.wire(modules)


os.environ['APP_MODE'] = sys.argv[-1] if sys.argv[-1] in ['development', 'production'] else 'development'

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
    # os.environ['APP_MODE'] = sys.argv[1] if len(sys.argv) > 1 else 'development'
    # setup_di_modules(os.environ['APP_MODE'])
    # run()



