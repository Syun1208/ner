import os
import logging
import faiss
import traceback
from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import Provide, inject
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.controller.arb_endpoint_filter import EndpointFilter
from src.module.application_container import ApplicationContainer
from src.service.interface.arb_service.arb_service import ARBService


arb_router = APIRouter()
   
@arb_router.get('/')
async def health_check() -> JSONResponse:
    return JSONResponse(
        content=jsonable_encoder({
            'message': 'OK', 
            'status_code': 200}), 
            status_code=200
        )

    
@arb_router.post('/api/v1/alpha/chat')
@inject
async def chat(
    request: Request,
    arb_service: ARBService = Depends(Provide[ApplicationContainer.arb_service])
) -> JSONResponse:
    try:
        params = await request.json()
        print(params)
        response = arb_service.chat(user_id=params['data']['user_id'], message=params['data']['query'])
        return JSONResponse(
            content=jsonable_encoder({
                'status_code': 200,
                'error_message': "",
                'data':response
            }),
            status_code=200
        )
        
    except Exception as e:
        
        return JSONResponse(
                content=jsonable_encoder({
                    'status_code': 500,
                    'error_message': str(e),
                }),
                status_code=500
            )

