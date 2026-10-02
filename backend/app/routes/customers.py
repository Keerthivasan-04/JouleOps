from fastapi import APIRouter, HTTPException

from ..db import get_connection


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.get("/{customer_id}")
def get_customer(customer_id: str):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # --------------------------------------------------
        # Get customer information
        # --------------------------------------------------

        customer_query = """
            SELECT
                CUSTOMER_ID,
                CUSTOMER_NAME,
                EMAIL,
                PHONE,
                CITY,
                COUNTRY,
                REGION,
                CREDIT_LIMIT,
                OUTSTANDING_AMOUNT
            FROM CUSTOMERS
            WHERE CUSTOMER_ID = ?
        """

        cursor.execute(
            customer_query,
            (customer_id,)
        )

        customer = cursor.fetchone()

        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        # --------------------------------------------------
        # Get overdue invoice information
        # --------------------------------------------------

        invoice_query = """
            SELECT
                COUNT(*),
                COALESCE(SUM(AMOUNT), 0),
                COALESCE(MAX(DAYS_OVERDUE), 0)
            FROM INVOICES
            WHERE CUSTOMER_ID = ?
              AND STATUS = 'OVERDUE'
        """

        cursor.execute(
            invoice_query,
            (customer_id,)
        )

        invoice_summary = cursor.fetchone()

        overdue_invoice_count = invoice_summary[0]
        overdue_amount = float(invoice_summary[1])
        max_days_overdue = invoice_summary[2]

        # --------------------------------------------------
        # Return customer summary
        # --------------------------------------------------

        return {
            "customer_id": customer[0],
            "customer_name": customer[1],
            "email": customer[2],
            "phone": customer[3],
            "city": customer[4],
            "country": customer[5],
            "region": customer[6],
            "credit_limit": float(customer[7]),
            "outstanding_amount": float(customer[8]),
            "overdue_invoice_count": overdue_invoice_count,
            "overdue_amount": overdue_amount,
            "max_days_overdue": max_days_overdue
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()