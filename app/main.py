from fastapi import FastAPI, Query, HTTPException
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker

from app.database import engine, Base
from app.models import Product

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

app = FastAPI(
    title="Product Browser API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Product Browser API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/products")
def get_products(
    page_size: int = Query(50, le=100),
    category: str | None = None,
    cursor: str | None = None
):

    db = SessionLocal()

    try:

        query = db.query(Product)

        if category:
            query = query.filter(
                Product.category == category
            )

        if cursor:
            cursor_dt = datetime.fromisoformat(cursor)

            query = query.filter(
                Product.created_at < cursor_dt
            )

        products = (
            query
            .order_by(desc(Product.created_at))
            .limit(page_size)
            .all()
        )

        result = []

        for p in products:
            result.append({
                "id": str(p.id),
                "name": p.name,
                "category": p.category,
                "price": float(p.price),
                "created_at": p.created_at
            })

        next_cursor = None

        if products:
            next_cursor = str(products[-1].created_at)

        return {
            "count": len(result),
            "next_cursor": next_cursor,
            "products": result
        }

    finally:
        db.close()


@app.get("/products/{product_id}")
def get_product(product_id: str):

    db = SessionLocal()

    try:

        product = db.query(Product).filter(
            Product.id == product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return {
            "id": str(product.id),
            "name": product.name,
            "category": product.category,
            "price": float(product.price),
            "created_at": product.created_at,
            "updated_at": product.updated_at
        }

    finally:
        db.close()