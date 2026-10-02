from fastapi import APIRouter, HTTPException

from ..db import get_connection
from ..models import MaterialResponse


router = APIRouter(
    prefix="/materials",
    tags=["Materials"]
)


@router.get(
    "/{material_id}",
    response_model=MaterialResponse
)
def get_material(material_id: str):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                MATERIAL_ID,
                DESCRIPTION,
                CATEGORY,
                STOCK_QUANTITY,
                UNIT_PRICE,
                REORDER_LEVEL,
                SUPPLIER_ID,
                SAFETY_STOCK,
                PLANT_CODE
            FROM MATERIALS
            WHERE MATERIAL_ID = ?
        """

        cursor.execute(query, (material_id,))

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Material not found"
            )

        return {
            "material_id": row[0],
            "description": row[1],
            "category": row[2],
            "stock_quantity": row[3],
            "unit_price": float(row[4]),
            "reorder_level": row[5],
            "supplier_id": row[6],
            "safety_stock": row[7],
            "plant_code": row[8],
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()