
import os
import time
import logging

import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orders-api")

app = FastAPI(title="DevOps Orders API")

DATABASE_URL = os.environ["DATABASE_URL"]


def get_connection():
    # Retry briefly while PostgreSQL initializes.
    for attempt in range(10):
        try:
            return psycopg2.connect(DATABASE_URL)
        except psycopg2.OperationalError:
            if attempt == 9:
                raise
            time.sleep(2)


class OrderInput(BaseModel):
    customer_name: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)


@app.get("/api/health")
def health():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return {"status": "healthy", "database": "connected"}
    except Exception:
        logger.exception("Health check failed")
        raise HTTPException(status_code=503, detail="Database unavailable")


@app.get("/api/slow")
def slow():
    time.sleep(5)
    return {"status": "completed"}

@app.get("/api/orders")
def list_orders():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, customer_name, amount, status, created_at
                    FROM orders ORDER BY id
                """)
                rows = cur.fetchall()

        return [
            {
                "id": row[0],
                "customer_name": row[1],
                "amount": float(row[2]),
                "status": row[3],
                "created_at": row[4].isoformat(),
            }
            for row in rows
        ]
    except Exception:
        logger.exception("Unable to retrieve orders")
        raise HTTPException(status_code=500, detail="Unable to retrieve orders")


@app.post("/api/orders", status_code=201)
def create_order(order: OrderInput):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO orders (customer_name, amount)
                    VALUES (%s, %s)
                    RETURNING id, customer_name, amount, status, created_at
                    """,
                    (order.customer_name, order.amount),
                )
                row = cur.fetchone()

        logger.info("Created order id=%s", row[0])
        return {
            "id": row[0],
            "customer_name": row[1],
            "amount": float(row[2]),
            "status": row[3],
            "created_at": row[4].isoformat(),
        }
    except Exception:
        logger.exception("Unable to create order")
        raise HTTPException(status_code=500, detail="Unable to create order")

