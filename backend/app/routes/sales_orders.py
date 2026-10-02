from datetime import date

from fastapi import APIRouter, HTTPException, Query

from ..db import get_connection


router = APIRouter(
    prefix="/sales-orders",
    tags=["Sales Orders"]
)


@router.get("/open")
def get_open_sales_orders(
    region: str = Query(..., min_length=2),
    date_from: date = Query(...),
    date_to: date = Query(...)
):

    if date_from > date_to:
        raise HTTPException(
            status_code=400,
            detail="date_from cannot be after date_to"
        )

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                ORDER_ID,
                MATERIAL_ID,
                QUANTITY,
                UNIT_PRICE,
                ORDER_DATE,
                DELIVERY_DATE,
                STATUS,
                CUSTOMER_ID,
                REGION
            FROM SALES_ORDERS
            WHERE STATUS = 'OPEN'
              AND REGION = ?
              AND ORDER_DATE BETWEEN ? AND ?
            ORDER BY ORDER_DATE
        """

        cursor.execute(
            query,
            (
                region,
                date_from,
                date_to
            )
        )

        rows = cursor.fetchall()

        return {
            "region": region,
            "date_from": date_from,
            "date_to": date_to,
            "total_orders": len(rows),
            "orders": [
                {
                    "order_id": row[0],
                    "material_id": row[1],
                    "quantity": row[2],
                    "unit_price": float(row[3]),
                    "order_date": row[4],
                    "delivery_date": row[5],
                    "status": row[6],
                    "customer_id": row[7],
                    "region": row[8]
                }
                for row in rows
            ]
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()