import os
import random
from datetime import datetime, date, timedelta

from dotenv import load_dotenv
from faker import Faker
from hdbcli import dbapi


# ============================================================
# Configuration
# ============================================================

load_dotenv()

HANA_HOST = os.getenv("HANA_HOST")
HANA_PORT = int(os.getenv("HANA_PORT", "443"))
HANA_USER = os.getenv("HANA_USER")
HANA_PASSWORD = os.getenv("HANA_PASSWORD")

SOURCE_SYSTEM = "SEED_SCRIPT"

random.seed(42)
fake = Faker("en_IN")
Faker.seed(42)


# ============================================================
# Database connection
# ============================================================

def get_connection():
    return dbapi.connect(
        address=HANA_HOST,
        port=HANA_PORT,
        user=HANA_USER,
        password=HANA_PASSWORD,
        encrypt=True,
    )


# ============================================================
# Helper functions
# ============================================================

def random_date(start_date, end_date):
    days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, days))


def money(min_value, max_value):
    return round(random.uniform(min_value, max_value), 2)


# ============================================================
# Date ranges
# Current project date: August 11, 2026
#
# Last week:
# Monday August 3, 2026
# Sunday August 9, 2026
# ============================================================

TODAY = date(2026, 8, 11)

LAST_WEEK_MONDAY = date(2026, 8, 3)
LAST_WEEK_SUNDAY = date(2026, 8, 9)

GENERAL_START_DATE = date(2026, 1, 1)


# ============================================================
# Customers
# Exactly 100 customers
#
# C-501 is deliberately included because the capstone
# requires the Anil / C-501 scenario.
# ============================================================

def generate_customers():

    customer_ids = [
        f"C-{i:03d}"
        for i in range(1, 100)
    ]

    # Replace the 100th normal ID with C-501
    customer_ids.append("C-501")

    regions = [
        "South",
        "North",
        "East",
        "West",
        "Central",
    ]

    customers = []

    for customer_id in customer_ids:

        if customer_id == "C-501":
            customer_name = "Apex Industrial Components"
            region = "South"
            credit_limit = 500000.00
        else:
            customer_name = fake.company()
            region = random.choice(regions)
            credit_limit = money(100000, 1000000)

        customers.append({
            "customer_id": customer_id,
            "customer_name": customer_name,
            "email": fake.email(),
            "phone": fake.phone_number()[:30],
            "address": fake.address().replace("\n", ", ")[:250],
            "city": fake.city(),
            "country": "India",
            "region": region,
            "credit_limit": credit_limit,
            "outstanding_amount": 0.00,
            "created_at": datetime.now(),
            "updated_on": datetime.now(),
            "source_system": SOURCE_SYSTEM,
        })

    return customers


# ============================================================
# Materials
# Exactly 500 materials
#
# MAT-1023 is deliberately configured for the Ramesh scenario:
# stock = 12
# safety stock = 50
# plant = PLT-PUN
# ============================================================

def generate_materials():

    plant_codes = [
        "PLT-PUN",
        "PLT-CHN",
        "PLT-HYD",
        "PLT-CBE",
    ]

    categories = [
        "Raw Material",
        "Component",
        "Finished Good",
        "Consumable",
        "Steel",
        "Electrical",
        "Mechanical",
    ]

    materials = []

    for number in range(1001, 1501):

        material_id = f"MAT-{number:04d}"

        category = random.choice(categories)
        plant_code = random.choice(plant_codes)

        materials.append({
            "material_id": material_id,
            "description": fake.catch_phrase()[:150],
            "category": category,
            "stock_quantity": random.randint(20, 500),
            "unit_price": money(100, 100000),
            "reorder_level": random.randint(20, 100),
            "supplier_id": f"SUP-{random.randint(1, 50):03d}",
            "created_at": datetime.now(),
            "safety_stock": random.randint(20, 100),
            "plant_code": plant_code,
            "updated_on": datetime.now(),
            "source_system": SOURCE_SYSTEM,
        })

    # --------------------------------------------------------
    # Required demo material
    # --------------------------------------------------------

    for material in materials:

        if material["material_id"] == "MAT-1023":

            material["description"] = "Steel Coil"
            material["category"] = "Steel"
            material["stock_quantity"] = 12
            material["safety_stock"] = 50
            material["reorder_level"] = 50
            material["plant_code"] = "PLT-PUN"
            material["unit_price"] = 75000.00

    return materials


# ============================================================
# Sales Orders
# Exactly 800 orders
#
# We deliberately create several OPEN South-region orders
# during last week for Priya's reporting scenario.
# ============================================================

def generate_sales_orders(customers, materials):

    customer_ids = [c["customer_id"] for c in customers]

    material_map = {
        m["material_id"]: m
        for m in materials
    }

    orders = []

    for number in range(1, 801):

        order_id = f"SO-{number:05d}"

        customer_id = random.choice(customer_ids)
        material_id = random.choice(list(material_map.keys()))

        quantity = random.randint(1, 25)

        material_price = material_map[material_id]["unit_price"]

        # Slight variation around material price
        unit_price = round(
            material_price * random.uniform(0.90, 1.10),
            2
        )

        order_date = random_date(
            GENERAL_START_DATE,
            TODAY
        )

        status = random.choice([
            "OPEN",
            "OPEN",
            "OPEN",
            "CLOSED",
            "DELIVERED",
            "CANCELLED",
        ])

        customer_region = next(
            c["region"]
            for c in customers
            if c["customer_id"] == customer_id
        )

        orders.append({
            "order_id": order_id,
            "material_id": material_id,
            "quantity": quantity,
            "unit_price": unit_price,
            "order_date": order_date,
            "delivery_date": order_date + timedelta(
                days=random.randint(5, 30)
            ),
            "status": status,
            "customer_id": customer_id,
            "created_at": datetime.now(),
            "region": customer_region,
            "updated_on": datetime.now(),
            "source_system": SOURCE_SYSTEM,
        })

    # --------------------------------------------------------
    # Force 20 orders into last week's South OPEN scenario
    # --------------------------------------------------------

    south_customers = [
        c["customer_id"]
        for c in customers
        if c["region"] == "South"
    ]

    for index in range(20):

        order = orders[index]

        order["customer_id"] = random.choice(south_customers)
        order["material_id"] = random.choice(
            list(material_map.keys())
        )

        order["quantity"] = random.randint(2, 20)

        material = material_map[order["material_id"]]

        order["unit_price"] = round(
            material["unit_price"],
            2
        )

        order["order_date"] = (
            LAST_WEEK_MONDAY
            + timedelta(days=random.randint(0, 6))
        )

        order["delivery_date"] = (
            order["order_date"]
            + timedelta(days=random.randint(5, 20))
        )

        order["status"] = "OPEN"
        order["region"] = "South"

    return orders


# ============================================================
# Invoices
# Exactly 400 invoices
#
# C-501 gets deliberately overdue invoices for Anil's scenario.
# ============================================================

def generate_invoices(customers):

    customer_ids = [c["customer_id"] for c in customers]

    invoices = []

    for number in range(1, 401):

        invoice_id = f"INV-{number:05d}"

        customer_id = random.choice(customer_ids)

        amount = money(10000, 250000)

        status = random.choice([
            "PAID",
            "PAID",
            "OPEN",
            "OVERDUE",
        ])

        if status == "PAID":

            due_date = random_date(
                GENERAL_START_DATE,
                TODAY - timedelta(days=5)
            )

            days_overdue = 0

        elif status == "OPEN":

            due_date = TODAY + timedelta(
                days=random.randint(1, 30)
            )

            days_overdue = 0

        else:

            due_date = TODAY - timedelta(
                days=random.randint(1, 120)
            )

            days_overdue = (
                TODAY - due_date
            ).days

        invoices.append({
            "invoice_id": invoice_id,
            "customer_id": customer_id,
            "amount": amount,
            "due_date": due_date,
            "status": status,
            "days_overdue": days_overdue,
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
            "source_system": SOURCE_SYSTEM,
        })

    # --------------------------------------------------------
    # Force C-501 overdue invoices
    #
    # >60 days  -> HOLD_SHIPMENTS
    # >90 days  -> ESCALATE_TO_LEGAL
    # --------------------------------------------------------

    c501_invoices = [
        {
            "invoice_id": "INV-C501-01",
            "customer_id": "C-501",
            "amount": 125000.00,
            "due_date": TODAY - timedelta(days=30),
            "status": "OVERDUE",
            "days_overdue": 30,
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
            "source_system": SOURCE_SYSTEM,
        },
        {
            "invoice_id": "INV-C501-02",
            "customer_id": "C-501",
            "amount": 180000.00,
            "due_date": TODAY - timedelta(days=75),
            "status": "OVERDUE",
            "days_overdue": 75,
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
            "source_system": SOURCE_SYSTEM,
        },
        {
            "invoice_id": "INV-C501-03",
            "customer_id": "C-501",
            "amount": 220000.00,
            "due_date": TODAY - timedelta(days=105),
            "status": "OVERDUE",
            "days_overdue": 105,
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
            "source_system": SOURCE_SYSTEM,
        },
    ]

    # Remove three randomly selected invoices and replace
    # them with the required C-501 invoices.
    invoices = invoices[:-3]
    invoices.extend(c501_invoices)

    return invoices


# ============================================================
# Delete previous seed data
#
# This makes the script safely re-runnable.
# ============================================================

def clear_previous_seed_data(cursor):

    print("Removing previous SEED_SCRIPT data...")

    # Delete dependent/business data first.
    cursor.execute("""
        DELETE FROM INVOICES
        WHERE SOURCE_SYSTEM = ?
    """, (SOURCE_SYSTEM,))

    cursor.execute("""
        DELETE FROM SALES_ORDERS
        WHERE SOURCE_SYSTEM = ?
    """, (SOURCE_SYSTEM,))

    cursor.execute("""
        DELETE FROM MATERIALS
        WHERE SOURCE_SYSTEM = ?
    """, (SOURCE_SYSTEM,))

    cursor.execute("""
        DELETE FROM CUSTOMERS
        WHERE SOURCE_SYSTEM = ?
    """, (SOURCE_SYSTEM,))


# ============================================================
# Insert Customers
# ============================================================

def insert_customers(cursor, customers):

    sql = """
        INSERT INTO CUSTOMERS (
            CUSTOMER_ID,
            CUSTOMER_NAME,
            EMAIL,
            PHONE,
            ADDRESS,
            CITY,
            COUNTRY,
            CREATED_AT,
            REGION,
            CREDIT_LIMIT,
            OUTSTANDING_AMOUNT,
            UPDATED_ON,
            SOURCE_SYSTEM
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    data = [
        (
            c["customer_id"],
            c["customer_name"],
            c["email"],
            c["phone"],
            c["address"],
            c["city"],
            c["country"],
            c["created_at"],
            c["region"],
            c["credit_limit"],
            c["outstanding_amount"],
            c["updated_on"],
            c["source_system"],
        )
        for c in customers
    ]

    cursor.executemany(sql, data)

    print(f"Inserted {len(data)} customers")


# ============================================================
# Insert Materials
# ============================================================

def insert_materials(cursor, materials):

    sql = """
        INSERT INTO MATERIALS (
            MATERIAL_ID,
            DESCRIPTION,
            CATEGORY,
            STOCK_QUANTITY,
            UNIT_PRICE,
            REORDER_LEVEL,
            SUPPLIER_ID,
            CREATED_AT,
            SAFETY_STOCK,
            PLANT_CODE,
            UPDATED_ON,
            SOURCE_SYSTEM
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    data = [
        (
            m["material_id"],
            m["description"],
            m["category"],
            m["stock_quantity"],
            m["unit_price"],
            m["reorder_level"],
            m["supplier_id"],
            m["created_at"],
            m["safety_stock"],
            m["plant_code"],
            m["updated_on"],
            m["source_system"],
        )
        for m in materials
    ]

    cursor.executemany(sql, data)

    print(f"Inserted {len(data)} materials")


# ============================================================
# Insert Sales Orders
# ============================================================

def insert_sales_orders(cursor, orders):

    sql = """
        INSERT INTO SALES_ORDERS (
            ORDER_ID,
            MATERIAL_ID,
            QUANTITY,
            UNIT_PRICE,
            ORDER_DATE,
            DELIVERY_DATE,
            STATUS,
            CUSTOMER_ID,
            CREATED_AT,
            REGION,
            UPDATED_ON,
            SOURCE_SYSTEM
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    data = [
        (
            o["order_id"],
            o["material_id"],
            o["quantity"],
            o["unit_price"],
            o["order_date"],
            o["delivery_date"],
            o["status"],
            o["customer_id"],
            o["created_at"],
            o["region"],
            o["updated_on"],
            o["source_system"],
        )
        for o in orders
    ]

    cursor.executemany(sql, data)

    print(f"Inserted {len(data)} sales orders")


# ============================================================
# Insert Invoices
# ============================================================

def insert_invoices(cursor, invoices):

    sql = """
        INSERT INTO INVOICES (
            INVOICE_ID,
            CUSTOMER_ID,
            AMOUNT,
            DUE_DATE,
            STATUS,
            DAYS_OVERDUE,
            CREATED_ON,
            UPDATED_ON,
            SOURCE_SYSTEM
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    data = [
        (
            i["invoice_id"],
            i["customer_id"],
            i["amount"],
            i["due_date"],
            i["status"],
            i["days_overdue"],
            i["created_on"],
            i["updated_on"],
            i["source_system"],
        )
        for i in invoices
    ]

    cursor.executemany(sql, data)

    print(f"Inserted {len(data)} invoices")


# ============================================================
# Update customer outstanding amounts
# ============================================================

def update_customer_outstanding(cursor):

    sql = """
        UPDATE CUSTOMERS
        SET OUTSTANDING_AMOUNT = (
            SELECT COALESCE(SUM(I.AMOUNT), 0)
            FROM INVOICES I
            WHERE I.CUSTOMER_ID = CUSTOMERS.CUSTOMER_ID
              AND I.STATUS IN ('OPEN', 'OVERDUE')
        ),
        UPDATED_ON = CURRENT_TIMESTAMP
        WHERE SOURCE_SYSTEM = ?
    """

    cursor.execute(sql, (SOURCE_SYSTEM,))

    print("Updated customer outstanding amounts")


# ============================================================
# Verification
# ============================================================

def verify_data(cursor):

    print("\n========== DATA VERIFICATION ==========")

    tables = [
        "CUSTOMERS",
        "MATERIALS",
        "SALES_ORDERS",
        "INVOICES",
        "TICKETS",
        "AUDIT_LOG",
    ]

    for table in tables:

        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        print(f"{table:<15} {count}")

    # --------------------------------------------------------
    # Verify MAT-1023
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            MATERIAL_ID,
            DESCRIPTION,
            STOCK_QUANTITY,
            SAFETY_STOCK,
            PLANT_CODE
        FROM MATERIALS
        WHERE MATERIAL_ID = 'MAT-1023'
    """)

    material = cursor.fetchone()

    print("\nMAT-1023:")
    print(material)

    # --------------------------------------------------------
    # Verify C-501
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            CUSTOMER_ID,
            CUSTOMER_NAME,
            REGION,
            CREDIT_LIMIT,
            OUTSTANDING_AMOUNT
        FROM CUSTOMERS
        WHERE CUSTOMER_ID = 'C-501'
    """)

    customer = cursor.fetchone()

    print("\nC-501:")
    print(customer)

    # --------------------------------------------------------
    # Verify C-501 overdue invoices
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(AMOUNT), 0),
            MAX(DAYS_OVERDUE)
        FROM INVOICES
        WHERE CUSTOMER_ID = 'C-501'
          AND STATUS = 'OVERDUE'
    """)

    invoice_summary = cursor.fetchone()

    print("\nC-501 overdue invoice summary:")
    print(invoice_summary)

    # --------------------------------------------------------
    # Verify South OPEN orders from last week
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM SALES_ORDERS
        WHERE REGION = 'South'
          AND STATUS = 'OPEN'
          AND ORDER_DATE BETWEEN ? AND ?
    """, (
        LAST_WEEK_MONDAY,
        LAST_WEEK_SUNDAY,
    ))

    south_orders = cursor.fetchone()[0]

    print("\nSouth OPEN orders from last week:")
    print(south_orders)

    # --------------------------------------------------------
    # Verify Chennai materials
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM MATERIALS
        WHERE PLANT_CODE = 'PLT-CHN'
    """)

    chennai_materials = cursor.fetchone()[0]

    print("\nChennai materials:")
    print(chennai_materials)


# ============================================================
# Main
# ============================================================

def main():

    print("========================================")
    print("NorthWind HANA Seed Script")
    print("========================================")

    connection = None
    cursor = None

    try:

        print("\nConnecting to HANA Cloud...")

        connection = get_connection()

        cursor = connection.cursor()

        print("Connected successfully!")

        # ----------------------------------------------------
        # Generate data
        # ----------------------------------------------------

        print("\nGenerating customers...")
        customers = generate_customers()

        print("Generating materials...")
        materials = generate_materials()

        print("Generating sales orders...")
        sales_orders = generate_sales_orders(
            customers,
            materials
        )

        print("Generating invoices...")
        invoices = generate_invoices(customers)

        # ----------------------------------------------------
        # Clear previous seed data
        # ----------------------------------------------------

        clear_previous_seed_data(cursor)

        # ----------------------------------------------------
        # Insert
        # ----------------------------------------------------

        insert_customers(
            cursor,
            customers
        )

        insert_materials(
            cursor,
            materials
        )

        insert_sales_orders(
            cursor,
            sales_orders
        )

        insert_invoices(
            cursor,
            invoices
        )

        # ----------------------------------------------------
        # Calculate customer outstanding amount
        # ----------------------------------------------------

        update_customer_outstanding(cursor)

        # ----------------------------------------------------
        # Commit everything
        # ----------------------------------------------------

        connection.commit()

        print("\nAll data committed successfully!")

        # ----------------------------------------------------
        # Verification
        # ----------------------------------------------------

        verify_data(cursor)

        print("\n========================================")
        print("SEEDING COMPLETED SUCCESSFULLY")
        print("========================================")

    except Exception as e:

        print("\nERROR OCCURRED:")
        print(e)

        if connection:
            connection.rollback()

        print("\nTransaction rolled back.")

        raise

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

        print("\nHANA connection closed.")


if __name__ == "__main__":
    main()