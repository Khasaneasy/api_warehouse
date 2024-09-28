from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from .models import Product, Order, OrderItem
from .schemas import ProductCreate, ProductUpdate, OrderCreate
from fastapi import HTTPException


async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()


async def update_product(
        db: AsyncSession, product_id: int,
        product_update: ProductUpdate):
    product = await get_product(db, product_id)
    for key, value in product_update.dict(exclude_unset=True).items():
        setattr(product, key, value)
    await db.commit()
    await db.refresh(product)
    return product


async def delete_product(db: AsyncSession, product_id: int):
    product = await get_product(db, product_id)
    await db.delete(product)
    await db.commit()


async def create_order(db: AsyncSession, order_data: OrderCreate):
    """Проверка наличия товара и доступного количества."""

    for item in order_data.items:
        product = await get_product(db, item.product_id)
        if product.quantity < 1:
            raise HTTPException(
                status_code=400,
                detail=f"Недостаточно товара на складе {product.name}"
            )

        product.quantity -= 1
        await db.commit()

    db_order = Order(status=order_data.status)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    for item in order_data.items:
        order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id
        )
        db.add(order_item)

    await db.commit()
    return db_order


async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(
        select(Order).options(joinedload(Order.order_items))
        .where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


async def get_orders(db: AsyncSession):
    result = await db.execute(select(Order))
    return result.scalars().all()


async def update_order_status(db: AsyncSession, order_id: int, status: str):
    order = await get_order(db, order_id)
    order.status = status
    await db.commit()
    await db.refresh(order)
    return order
