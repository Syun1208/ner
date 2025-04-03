from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject
from fastapi.encoders import jsonable_encoder
from src.model.api_key_model import Department
 
key_router = APIRouter(tags=["API Key Authentication"])


@key_router.get('/api/v1/{department}/generate_key')
@inject
async def generate_key(
    department: Department
) -> JSONResponse:
    
    print(f'Department: {department.alpha}')
    
    return JSONResponse(
        content=jsonable_encoder({
            "status_code": 200, 
            "error_message": "",
            "data": {
                "api_key": "nfuibay8175105njknia"
            }
        }), 
        status_code=200
    )