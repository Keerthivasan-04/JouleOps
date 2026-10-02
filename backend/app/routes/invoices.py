from fastapi import APIRouter, HTTPException

from ..db import get_connection


router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


@router.get("/{customer_id}/overdue-summary")
def get_overdue_invoice_summary(customer_id: str):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # --------------------------------------------------
        # Check whether the customer has invoices
        # --------------------------------------------------

        query = """
            SELECT
                COUNT(*),
                COALESCE(SUM(AMOUNT), 0),
                COALESCE(MAX(DAYS_OVERDUE), 0)
            FROM INVOICES
            WHERE CUSTOMER_ID = ?
              AND STATUS = 'OVERDUE'
        """

        cursor.execute(
            query,
            (customer_id,)
        )

        result = cursor.fetchone()

        overdue_invoice_count = result[0]
        overdue_amount = float(result[1])
        max_days_overdue = result[2]

        # --------------------------------------------------
        # Check customer existence
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM CUSTOMERS
            WHERE CUSTOMER_ID = ?
            """,
            (customer_id,)
        )

        customer_exists = cursor.fetchone()[0]

        if customer_exists == 0:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        # --------------------------------------------------
        # Return summary
        # --------------------------------------------------

        return {
            "customer_id": customer_id,
            "overdue_invoice_count": overdue_invoice_count,
            "overdue_amount": overdue_amount,
            "max_days_overdue": max_days_overdue
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()