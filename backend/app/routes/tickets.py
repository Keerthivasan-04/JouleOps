from datetime import datetime

from fastapi import APIRouter, HTTPException

from ..db import get_connection
from ..models import CreateTicketRequest


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


# Roles allowed to create maintenance tickets
ALLOWED_ROLES = {
    "PLANT_SUPERVISOR",
    "MAINTENANCE_MANAGER",
    "ADMIN"
}


@router.post("/")
def create_ticket(request: CreateTicketRequest):

    # ------------------------------------------------------
    # RBAC check
    # ------------------------------------------------------

    if request.created_by_role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=403,
            detail="Role is not authorized to create tickets"
        )

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # --------------------------------------------------
        # Generate ticket ID
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM TICKETS
        """)

        ticket_count = cursor.fetchone()[0]

        ticket_id = f"TKT-{ticket_count + 1:05d}"

        # --------------------------------------------------
        # Current timestamp
        # --------------------------------------------------

        now = datetime.now()

        # --------------------------------------------------
        # Insert ticket
        # --------------------------------------------------

        ticket_sql = """
            INSERT INTO TICKETS (
                TICKET_ID,
                EQUIPMENT_ID,
                MATERIAL_ID,
                PRIORITY,
                ASSIGNED_TEAM,
                DESCRIPTION,
                STATUS,
                CREATED_ON,
                CREATED_BY_ROLE,
                UPDATED_ON,
                SOURCE_SYSTEM
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            ticket_sql,
            (
                ticket_id,
                request.equipment_id,
                request.material_id,
                request.priority,
                request.assigned_team,
                request.description,
                "OPEN",
                now,
                request.created_by_role,
                now,
                "FASTAPI"
            )
        )

        # --------------------------------------------------
        # Audit log
        # --------------------------------------------------

        log_id = f"LOG-{ticket_count + 1:05d}"

        audit_sql = """
            INSERT INTO AUDIT_LOG (
                LOG_ID,
                TS,
                USER_ROLE,
                TOOL_NAME,
                PARAMS_MASKED,
                OUTCOME
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """

        params_masked = (
            f"material_id={request.material_id},"
            f"priority={request.priority},"
            f"assigned_team={request.assigned_team}"
        )

        cursor.execute(
            audit_sql,
            (
                log_id,
                now,
                request.created_by_role,
                "create_ticket",
                params_masked,
                "SUCCESS"
            )
        )

        # --------------------------------------------------
        # Commit both operations together
        # --------------------------------------------------

        connection.commit()

        return {
            "ticket_id": ticket_id,
            "equipment_id": request.equipment_id,
            "material_id": request.material_id,
            "priority": request.priority,
            "assigned_team": request.assigned_team,
            "description": request.description,
            "status": "OPEN",
            "created_by_role": request.created_by_role,
            "source_system": "FASTAPI"
        }

    except HTTPException:
        raise

    except Exception as e:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to create ticket: {str(e)}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

@router.get("/{ticket_id}")
def get_ticket(ticket_id: str):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                TICKET_ID,
                EQUIPMENT_ID,
                MATERIAL_ID,
                PRIORITY,
                ASSIGNED_TEAM,
                DESCRIPTION,
                STATUS,
                CREATED_ON,
                CREATED_BY_ROLE,
                UPDATED_ON,
                SOURCE_SYSTEM
            FROM TICKETS
            WHERE TICKET_ID = ?
        """

        cursor.execute(query, (ticket_id,))

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Ticket not found"
            )

        return {
            "ticket_id": row[0],
            "equipment_id": row[1],
            "material_id": row[2],
            "priority": row[3],
            "assigned_team": row[4],
            "description": row[5],
            "status": row[6],
            "created_on": row[7],
            "created_by_role": row[8],
            "updated_on": row[9],
            "source_system": row[10]
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()