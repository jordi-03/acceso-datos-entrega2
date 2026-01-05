from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db import get_db
from app.schemas import RentalCreate, RentalOut

router = APIRouter(tags=["rentals"])


@router.post("/rentals", status_code=status.HTTP_201_CREATED)
def create_rental(payload: RentalCreate, db: Session = Depends(get_db)):

    q = text("""
        INSERT INTO rental (rental_date, inventory_id, customer_id, return_date, staff_id, last_update)
        VALUES (NOW(), :inventory_id, :customer_id, NULL, :staff_id, NOW())
    """)
    res = db.execute(q, payload.model_dump())
    db.commit()
    return {"rental_id": res.lastrowid}


@router.get("/rentals", response_model=list[RentalOut])
def list_rentals(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    if limit < 1 or limit > 200:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 200")
    if offset < 0:
        raise HTTPException(status_code=422, detail="offset must be >= 0")

    q = text("""
        SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update
        FROM rental
        ORDER BY rental_id DESC
        LIMIT :limit OFFSET :offset
    """)
    rows = db.execute(q, {"limit": limit, "offset": offset}).mappings().all()
    return rows


@router.get("/rentals/{rentalId}", response_model=RentalOut)
def get_rental(rentalId: int, db: Session = Depends(get_db)):
    q = text("""
        SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update
        FROM rental
        WHERE rental_id = :id
    """)
    row = db.execute(q, {"id": rentalId}).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="rental not found")
    return row


@router.put("/rentals/{rentalId}/return")
def return_rental(rentalId: int, db: Session = Depends(get_db)):
  
    q_check = text("SELECT return_date FROM rental WHERE rental_id = :id")
    row = db.execute(q_check, {"id": rentalId}).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="rental not found")
    if row["return_date"] is not None:
        raise HTTPException(status_code=409, detail="rental already returned")

    q = text("""
        UPDATE rental
        SET return_date = NOW(), last_update = NOW()
        WHERE rental_id = :id
    """)
    db.execute(q, {"id": rentalId})
    db.commit()
    return {"status": "returned"}


@router.get("/customers/{customerId}/rentals", response_model=list[RentalOut])
def rentals_by_customer(customerId: int, limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    if limit < 1 or limit > 200:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 200")
    if offset < 0:
        raise HTTPException(status_code=422, detail="offset must be >= 0")

    c = db.execute(text("SELECT customer_id FROM customer WHERE customer_id = :id"), {"id": customerId}).first()
    if not c:
        raise HTTPException(status_code=404, detail="customer not found")

    q = text("""
        SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update
        FROM rental
        WHERE customer_id = :cid
        ORDER BY rental_date DESC
        LIMIT :limit OFFSET :offset
    """)
    rows = db.execute(q, {"cid": customerId, "limit": limit, "offset": offset}).mappings().all()
    return rows
