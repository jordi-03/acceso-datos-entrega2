from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db import get_db
from app.schemas import CustomerCreate, CustomerUpdate, CustomerOut

router = APIRouter(tags=["customers"])


@router.post("/customers", status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    q = text("""
        INSERT INTO customer (store_id, first_name, last_name, email, address_id, active, create_date, last_update)
        VALUES (:store_id, :first_name, :last_name, :email, :address_id, :active, NOW(), NOW())
    """)
    res = db.execute(q, payload.model_dump())
    db.commit()
    new_id = res.lastrowid
    return {"customer_id": new_id}


@router.get("/customers", response_model=list[CustomerOut])
def list_customers(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    if limit < 1 or limit > 200:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 200")
    if offset < 0:
        raise HTTPException(status_code=422, detail="offset must be >= 0")

    q = text("""
        SELECT customer_id, first_name, last_name, email
        FROM customer
        ORDER BY customer_id
        LIMIT :limit OFFSET :offset
    """)
    rows = db.execute(q, {"limit": limit, "offset": offset}).mappings().all()
    return rows


@router.get("/customers/{customerId}", response_model=CustomerOut)
def get_customer(customerId: int, db: Session = Depends(get_db)):
    q = text("""
        SELECT customer_id, first_name, last_name, email
        FROM customer
        WHERE customer_id = :id
    """)
    row = db.execute(q, {"id": customerId}).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="customer not found")
    return row


@router.put("/customers/{customerId}")
def update_customer(customerId: int, payload: CustomerUpdate, db: Session = Depends(get_db)):

    exists_q = text("SELECT customer_id FROM customer WHERE customer_id = :id")
    exists = db.execute(exists_q, {"id": customerId}).first()
    if not exists:
        raise HTTPException(status_code=404, detail="customer not found")

    q = text("""
        UPDATE customer
        SET store_id = :store_id,
            first_name = :first_name,
            last_name = :last_name,
            email = :email,
            address_id = :address_id,
            active = :active,
            last_update = NOW()
        WHERE customer_id = :id
    """)
    params = payload.model_dump()
    params["id"] = customerId
    db.execute(q, params)
    db.commit()
    return {"status": "updated"}


@router.delete("/customers/{customerId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customerId: int, db: Session = Depends(get_db)):

    try:
        q = text("DELETE FROM customer WHERE customer_id = :id")
        res = db.execute(q, {"id": customerId})
        db.commit()
        if res.rowcount == 0:
            raise HTTPException(status_code=404, detail="customer not found")
        return
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="cannot delete customer (maybe has rentals)")
