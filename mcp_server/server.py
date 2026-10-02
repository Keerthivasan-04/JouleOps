import os
import httpx
from mcp.server import MCPServer


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)

mcp = MCPServer("JouleOps NorthWind")



@mcp.tool()
def health_check() -> str:
    """Check whether the JouleOps NorthWind MCP server is running."""
    return "JouleOps NorthWind MCP server is healthy"

@mcp.tool()
def get_material(material_id: str) -> dict:
    """
    Get material details including stock quantity, price,
    reorder level, safety stock, supplier, and plant.
    """

    url = f"{BACKEND_URL}/materials/{material_id}"

    try:
        response = httpx.get(url, timeout=10.0)

        if response.status_code == 404:
            return {
                "error": "Material not found",
                "material_id": material_id
            }

        response.raise_for_status()

        return response.json()

    except httpx.RequestError as e:
        return {
            "error": "Unable to connect to FastAPI backend",
            "details": str(e)
        }


@mcp.tool()
def get_customer(customer_id: str) -> dict:
    """
    Get customer details including credit limit,
    outstanding amount, and overdue invoice information.
    """

    url = f"{BACKEND_URL}/customers/{customer_id}"

    try:
        response = httpx.get(url, timeout=10.0)

        if response.status_code == 404:
            return {
                "error": "Customer not found",
                "customer_id": customer_id
            }

        response.raise_for_status()

        return response.json()

    except httpx.RequestError as e:
        return {
            "error": "Unable to connect to FastAPI backend",
            "details": str(e)
        }



@mcp.tool()
def get_sales_orders(
    region: str,
    date_from: str,
    date_to: str
) -> dict:
    """
    Get open sales orders for a region within a date range.
    """

    url = f"{BACKEND_URL}/sales-orders/open"

    params = {
        "region": region,
        "date_from": date_from,
        "date_to": date_to
    }

    try:
        response = httpx.get(
            url,
            params=params,
            timeout=10.0
        )

        if response.status_code == 400:
            return {
                "error": response.json().get(
                    "detail",
                    "Invalid date range"
                )
            }

        response.raise_for_status()

        return response.json()

    except httpx.RequestError as e:
        return {
            "error": "Unable to connect to FastAPI backend",
            "details": str(e)
        }



@mcp.tool()
def create_ticket(
    equipment_id: str,
    material_id: str,
    priority: str,
    assigned_team: str,
    description: str,
    created_by_role: str
) -> dict:
    """
    Create a maintenance ticket through the FastAPI backend.
    The backend enforces role-based authorization.
    """

    url = f"{BACKEND_URL}/tickets/"

    payload = {
        "equipment_id": equipment_id,
        "material_id": material_id,
        "priority": priority,
        "assigned_team": assigned_team,
        "description": description,
        "created_by_role": created_by_role
    }

    try:
        response = httpx.post(
            url,
            json=payload,
            timeout=10.0
        )

        if response.status_code == 403:
            return {
                "error": response.json().get(
                    "detail",
                    "Role is not authorized to create tickets"
                )
            }

        if response.status_code == 422:
            return {
                "error": "Invalid ticket request",
                "details": response.json()
            }

        response.raise_for_status()

        return response.json()

    except httpx.RequestError as e:
        return {
            "error": "Unable to connect to FastAPI backend",
            "details": str(e)
        }



@mcp.tool()
def get_overdue_invoices(customer_id: str) -> dict:
    """
    Get overdue invoice summary for a customer.
    """

    url = f"{BACKEND_URL}/invoices/{customer_id}/overdue-summary"

    try:
        response = httpx.get(
            url,
            timeout=10.0
        )

        if response.status_code == 404:
            return {
                "error": response.json().get(
                    "detail",
                    "Customer not found"
                ),
                "customer_id": customer_id
            }

        if response.status_code == 422:
            return {
                "error": "Invalid customer ID",
                "details": response.json()
            }

        response.raise_for_status()

        return response.json()

    except httpx.RequestError as e:
        return {
            "error": "Unable to connect to FastAPI backend",
            "details": str(e)
        }



@mcp.tool()
def get_ticket(ticket_id: str) -> dict:
    """
    Get details of a maintenance ticket.
    """

    url = f"{BACKEND_URL}/tickets/{ticket_id}"

    try:
        response = httpx.get(
            url,
            timeout=10.0
        )

        if response.status_code == 404:
            return {
                "error": "Ticket not found",
                "ticket_id": ticket_id
            }

        response.raise_for_status()

        return response.json()

    except httpx.RequestError as e:
        return {
            "error": "Unable to connect to FastAPI backend",
            "details": str(e)
        }



if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8001"))
    )



# if __name__ == "__main__":
#     mcp.run(transport="streamable-http", port=8001)