from decimal import Decimal

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.idempotency import IdempotencyKey
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["Order Management"])


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    idempotency_key: str | None = Header(default=None),
):
    if not idempotency_key:
        raise HTTPException(
            status_code=400,
            detail="Idempotency-Key header is required",
        )

    # Check whether this request was already processed
    existing_key = (
        db.query(IdempotencyKey)
        .filter(
            IdempotencyKey.idempotency_key == idempotency_key
        )
        .first()
    )

    if existing_key:
        existing_order = (
            db.query(Order)
            .filter(Order.id == existing_key.order_id)
            .first()
        )

        if existing_order:
            return existing_order

    if not order_data.items:
        raise HTTPException(
            status_code=400,
            detail="Order must contain at least one item",
        )

    total_amount = Decimal("0.00")
    order_items = []

    for item in order_data.items:
        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found",
            )

        if item.quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Quantity must be greater than zero",
            )

        subtotal = product.price * item.quantity
        total_amount += subtotal

        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
                subtotal=subtotal,
            )
        )

    order = Order(
        user_id=order_data.user_id,
        status="PENDING",
        total_amount=total_amount,
    )

    db.add(order)
    db.flush()

    for order_item in order_items:
        order_item.order_id = order.id
        db.add(order_item)

    db.flush()

    # Store the idempotency key against this order
    key_record = IdempotencyKey(
        idempotency_key=idempotency_key,
        order_id=order.id,
    )

    db.add(key_record)
    db.commit()
    db.refresh(order)

    return order


@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).order_by(Order.created_at.desc()).all()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return order