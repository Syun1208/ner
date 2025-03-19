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

@arb_router.post('/chat')
@inject
async def indexing_knowledge(
    request: Request,
    arb_service: ARBService = Depends(Provide[ApplicationContainer.arb_service])
) -> JSONResponse:
    try:
        params = await request.json()
        message = arb_service.get_responding(user_id=params['user_id'], session_id=params['session_id'], message=params['message'])
        return JSONResponse(
            content=jsonable_encoder({
                'message': message['text']
            }),
            status_code=200
        )
        
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
