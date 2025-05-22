from typing import Optional, List
from uuid import UUID
from datetime import datetime

from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, company_id: UUID) -> Optional[Company]:
        result = await self.session.execute(select(Company).where(Company.id == company_id))
        return result.first()

    async def get_all(self) -> List[Company]:
        result = await self.session.execute(select(Company).order_by(desc(Company.created_at)))
        return result.all()

    async def create(self, company_in: CompanyCreate) -> Company:
        data = company_in.model_dump()
        if data.get("website"):
            data["website"] = str(data["website"])  # Convert HttpUrl to string
        company = Company(**data)
        self.session.add(company)
        await self.session.commit()
        await self.session.refresh(company)
        return company


    async def update(self, company: Company, company_in: CompanyUpdate) -> Company:
        company_data = company_in.model_dump(exclude_unset=True)
        for key, value in company_data.items():
            setattr(company, key, value)
        company.updated_at = datetime.utcnow()
        self.session.add(company)
        await self.session.commit()
        await self.session.refresh(company)
        return company

    async def delete(self, company: Company) -> None:
        await self.session.delete(company)
        await self.session.commit()
