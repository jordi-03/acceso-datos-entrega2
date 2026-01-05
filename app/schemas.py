from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# -------------------------
# CUSTOMERS
# -------------------------
class CustomerBase(BaseModel):
    store_id: int = Field(..., ge=1, le=2)
    first_name: str = Field(..., min_length=1, max_length=45)
    last_name: str = Field(..., min_length=1, max_length=45)
    email: EmailStr
    address_id: int = Field(..., ge=1)
    active: int = Field(1, ge=0, le=1)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class CustomerOut(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    email: str


# -------------------------
# RENTALS
# -------------------------
class RentalCreate(BaseModel):
    inventory_id: int = Field(..., ge=1)
    customer_id: int = Field(..., ge=1)
    staff_id: int = Field(..., ge=1)


class RentalOut(BaseModel):
    rental_id: int
    rental_date: datetime
    inventory_id: int
    customer_id: int
    return_date: datetime | None
    staff_id: int
    last_update: datetime
