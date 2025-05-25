from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate
from app.services.company_service import CompanyService
from app.db.session import get_session

router = APIRouter()

@router.get("/", response_model=List[CompanyRead])
async def read_companies(session: AsyncSession = Depends(get_session)):
    service = CompanyService(session)
    companies = await service.get_all()
    return companies


@router.get("/{company_id}", response_model=CompanyRead)
async def read_company(company_id: UUID, session: AsyncSession = Depends(get_session)):
    service = CompanyService(session)
    company = await service.get(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(company_in: CompanyCreate, session: AsyncSession = Depends(get_session)):
    service = CompanyService(session)
    company = await service.create(company_in)
    return company


@router.put("/{company_id}", response_model=CompanyRead)
async def update_company(company_id: UUID, company_in: CompanyUpdate, session: AsyncSession = Depends(get_session)):
    service = CompanyService(session)
    company = await service.get(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    company = await service.update(company, company_in)
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: UUID, session: AsyncSession = Depends(get_session)):
    service = CompanyService(session)
    company = await service.get(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    await service.delete(company)
    return None
