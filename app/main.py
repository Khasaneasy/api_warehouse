from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app import crud, schemas

app = FastAPI()


async def get_db():
    async with async_session_maker() as session:
        """Получение сессии базы данных."""
        yield session


@app.post("/products", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, 
                         db: AsyncSession = Depends(get_db)):
    return await crud.create_product(db, product)


@app.get("/products", response_model=list[schemas.Product])
async def get_products(db: AsyncSession = Depends(get_db)):
    return await crud.get_products(db)


@app.get("/products/{product_id}", response_model=schemas.Product)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_product(db, product_id)


@app.put("/products/{product_id}", response_model=schemas.Product)
async def update_product(product_id: int, product: schemas.ProductUpdate,
                         db: AsyncSession = Depends(get_db)):
    return await crud.update_product(db, product_id, product)


@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    await crud.delete_product(db, product_id)
    return {"message": "Продукт успешно удален"}


@app.post("/orders", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate,
                       db: AsyncSession = Depends(get_db)):
    return await crud.create_order(db, order)


@app.get("/orders", response_model=list[schemas.Order])
async def get_orders(db: AsyncSession = Depends(get_db)):
    return await crud.get_orders(db)


@app.get("/orders/{order_id}", response_model=schemas.Order)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_order(db, order_id)


@app.patch("/orders/{order_id}/status", response_model=schemas.Order)
async def update_order_status(order_id: int, status: str,
                              db: AsyncSession = Depends(get_db)):
    return await crud.update_order_status(db, order_id, status)
