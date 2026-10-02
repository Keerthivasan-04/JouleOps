from pydantic import BaseModel, Field


class MaterialResponse(BaseModel):
    material_id: str
    description: str
    category: str
    stock_quantity: int
    unit_price: float
    reorder_level: int
    supplier_id: str
    safety_stock: int
    plant_code: str


class CreateTicketRequest(BaseModel):
    equipment_id: str | None = Field(
        default=None,
        max_length=20
    )

    material_id: str | None = Field(
        default=None,
        max_length=20
    )

    priority: str = Field(
        min_length=1,
        max_length=20
    )

    assigned_team: str = Field(
        min_length=1,
        max_length=100
    )

    description: str = Field(
        min_length=1,
        max_length=500
    )

    created_by_role: str = Field(
        min_length=1,
        max_length=50
    )