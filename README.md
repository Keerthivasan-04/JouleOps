# JouleOps @ NorthWind Manufacturing

> **Agentic AI Enterprise Assistant built with SAP BTP, SAP HANA Cloud, FastAPI, and Model Context Protocol (MCP).**

JouleOps is an enterprise AI assistant concept for **NorthWind Manufacturing** that converts routine SAP data operations into natural-language requests.

The solution connects an AI agent/tool layer with enterprise data through two governed paths:

- **REST/FastAPI actions** deployed on SAP BTP Cloud Foundry
- **MCP tools** exposed through a dedicated MCP server

Both paths ultimately access **SAP HANA Cloud**, while business rules, validation, role-based access control, and audit logging remain in the backend.

---

## 📌 Project Overview

Manufacturing employees often need to navigate multiple enterprise screens just to answer simple operational questions or perform routine actions.

JouleOps addresses this by providing a conversational architecture in which a request can follow this flow:

```text
User Request
     │
     ▼
SAP Joule / Agent Layer
     │
     ├───────────────┐
     ▼               ▼
Joule Skill       MCP Tool
     │               │
     ▼               ▼
SAP BTP Destination
     │               │
     ▼               ▼
FastAPI Backend   MCP Server
     │               │
     └───────┬───────┘
             ▼
      SAP HANA Cloud
             │
             ▼
       Structured JSON
             │
             ▼
      Grounded Response
```

The project demonstrates how enterprise AI can interact with structured business data while keeping database credentials and write operations outside the AI layer.

---

## 🎯 Objectives

- Build an enterprise-oriented Agentic AI backend architecture.
- Connect Python services with **SAP HANA Cloud**.
- Expose business operations through **FastAPI REST endpoints**.
- Implement a custom **Model Context Protocol (MCP) server**.
- Support both REST actions and MCP-based tool access.
- Apply input validation using **Pydantic**.
- Implement role-based authorization for write operations.
- Maintain an audit trail for ticket creation.
- Deploy backend services to **SAP BTP Cloud Foundry**.
- Demonstrate realistic manufacturing, sales, finance, and maintenance scenarios.

---

## 🏭 Business Scenario

NorthWind Manufacturing is modeled as an industrial equipment company operating multiple plants and managing:

- Materials and inventory
- Sales orders
- Customers
- Invoices
- Maintenance tickets

The assistant is designed around three representative personas:

| Persona | Role                   | Example Requirement                                  |
| ------- | ---------------------- | ---------------------------------------------------- |
| Ramesh  | Plant Supervisor       | Check material stock and create a maintenance ticket |
| Priya   | Regional Sales Manager | Retrieve open sales orders for a region              |
| Anil    | Finance Controller     | Review overdue customer invoices                     |

### Example Natural-Language Requests

```text
Is material MAT-1023 below safety stock?

Show me last week's open sales orders for the South region.

Summarise C-501's overdue invoices.

Create a HIGH-priority maintenance ticket for the mechanical team.
```

---

## 🧰 Technology Stack

| Layer               | Technology                       |
| ------------------- | -------------------------------- |
| AI / Agent Layer    | SAP Joule / Joule Studio         |
| Enterprise Platform | SAP Business Technology Platform |
| Database            | SAP HANA Cloud                   |
| Backend API         | Python FastAPI                   |
| MCP Integration     | Model Context Protocol           |
| Database Driver     | SAP HANA `hdbcli`                |
| Validation          | Pydantic v2                      |
| HTTP Client         | HTTPX                            |
| Application Server  | Uvicorn                          |
| Deployment          | SAP BTP Cloud Foundry            |
| Data Generation     | Python / Faker                   |
| API Documentation   | OpenAPI / Swagger UI             |

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
                         │ Natural Language    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ SAP Joule / Agent   │
                         │ Intent + Tool       │
                         │ Selection           │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
          ┌──────────────────┐          ┌──────────────────┐
          │ Joule Skill /    │          │ MCP Tool         │
          │ REST Action      │          │ Server           │
          └────────┬─────────┘          └────────┬─────────┘
                   │                             │
                   └──────────────┬──────────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │ SAP BTP Destination  │
                       └──────────┬───────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
          ┌──────────────────┐        ┌──────────────────┐
          │ FastAPI Service  │        │ MCP Service      │
          │ Cloud Foundry    │        │ Cloud Foundry    │
          └────────┬─────────┘        └────────┬─────────┘
                   │                           │
                   └─────────────┬─────────────┘
                                 │
                                 ▼
                      ┌─────────────────────┐
                      │   SAP HANA Cloud     │
                      │                     │
                      │ CUSTOMERS           │
                      │ MATERIALS           │
                      │ SALES_ORDERS        │
                      │ INVOICES            │
                      │ TICKETS             │
                      │ AUDIT_LOG           │
                      └─────────────────────┘
```

---

## 📂 Project Structure

```text
JouleOps_NorthWind/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── main.py
│   │   ├── models.py
│   │   │
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── customers.py
│   │       ├── invoices.py
│   │       ├── materials.py
│   │       ├── sales_orders.py
│   │       └── tickets.py
│   │
│   ├── manifest.yml
│   ├── Procfile
│   ├── requirements.txt
│   └── runtime.txt
│
├── hana/
│   └── seed_data.py
│
├── mcp_server/
│   ├── manifest.yml
│   ├── Procfile
│   ├── requirements.txt
│   ├── runtime.txt
│   └── server.py
│
└── JouleOps_NorthWind_Documentation.pdf
```

---

## 🗄️ Data Model

The solution works with the following major HANA Cloud tables:

### `MATERIALS`

Stores material and inventory information.

```text
MATERIAL_ID
DESCRIPTION
CATEGORY
STOCK_QUANTITY
UNIT_PRICE
REORDER_LEVEL
SUPPLIER_ID
SAFETY_STOCK
PLANT_CODE
```

### `SALES_ORDERS`

Stores customer sales orders and regional information.

### `CUSTOMERS`

Stores customer profile, credit, and outstanding amount information.

### `INVOICES`

Stores invoice amount, due date, status, and overdue information.

### `TICKETS`

Stores maintenance ticket information.

### `AUDIT_LOG`

Records important write operations for traceability.

---

## 🔌 FastAPI REST API

The FastAPI service is organized into separate routers.

### Materials

```http
GET /materials/{material_id}
```

Returns:

- Material description
- Category
- Stock quantity
- Unit price
- Reorder level
- Safety stock
- Supplier
- Plant

### Sales Orders

```http
GET /sales-orders/open?region={region}&date_from={date}&date_to={date}
```

Returns open sales orders filtered by region and date range.

### Customers

```http
GET /customers/{customer_id}
```

Returns customer information together with overdue invoice summary.

### Tickets

```http
POST /tickets/
GET /tickets/{ticket_id}
```

Creates and retrieves maintenance tickets.

Ticket creation includes authorization and audit logging.

### Invoices

```http
GET /invoices/{customer_id}/overdue-summary
```

Returns:

- Overdue invoice count
- Total overdue amount
- Maximum days overdue

---

## 🔗 MCP Server

The MCP server provides a second integration surface over the same backend data.

Implemented tools include:

```text
health_check
get_material
get_customer
get_sales_orders
create_ticket
get_overdue_invoices
get_ticket
```

The MCP server communicates with the FastAPI service using HTTPX.

This provides a separation between:

```text
AI Tool Interface
       ↓
MCP Server
       ↓
FastAPI Business/API Layer
       ↓
SAP HANA Cloud
```

---

## 🔐 Security & Governance

Security and governance are important parts of the architecture.

### 1. Credential Isolation

SAP HANA credentials are stored as backend environment variables.

The AI/agent layer does not directly receive database credentials.

```text
Agent
  │
  │ Structured request
  ▼
Backend
  │
  │ HANA credentials
  ▼
SAP HANA Cloud
```

### 2. Role-Based Access Control

Ticket creation is restricted to authorized roles.

Current backend authorization includes:

```text
PLANT_SUPERVISOR
MAINTENANCE_MANAGER
ADMIN
```

Unauthorized roles receive:

```http
403 Forbidden
```

### 3. Audit Logging

Ticket creation writes an entry to `AUDIT_LOG` containing information such as:

- User role
- Tool/action name
- Masked parameters
- Outcome
- Timestamp

### 4. Input Validation

Request models use Pydantic validation to enforce required fields and field constraints.

### 5. Parameterized SQL

SQL statements use bound parameters rather than directly concatenating user input.

---

## 🧪 Demo Scenarios

### Scenario 1 — Inventory Check & Action

```text
Is MAT-1023 below safety stock?
If yes, create a HIGH-priority maintenance ticket.
```

The backend checks material inventory and can subsequently create a ticket when the business condition is satisfied.

---

### Scenario 2 — Regional Sales Report

```text
Show me last week's open sales orders for the South region.
```

The API retrieves open orders using the requested region and date range.

---

### Scenario 3 — Customer Credit Exposure

```text
Summarise C-501's overdue invoices.
```

Customer and invoice information can be combined to provide an operational summary.

---

### Scenario 4 — MCP Inventory Path

```text
Give me an inventory snapshot for the Chennai plant.
```

The MCP integration demonstrates an alternative tool path to enterprise data.

---

### Scenario 5 — Safe Action Handling

```text
Create a ticket.
```

If required information is missing, the system should not guess critical values. The intended agent behavior is to request clarification before executing a write operation.

---

## 🚀 Local Setup

### Prerequisites

Install:

- Python 3.x
- SAP HANA Cloud instance
- SAP BTP account
- Cloud Foundry CLI
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/jouleops-northwind.git
cd jouleops-northwind
```

---

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

---

### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

### 4. Configure HANA Credentials

Create a `.env` file inside the `backend` directory:

```env
HANA_HOST=<your-hana-host>
HANA_PORT=443
HANA_USER=<your-hana-user>
HANA_PASSWORD=<your-hana-password>
```

> **Never commit `.env` or database credentials to GitHub.**

Add this to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

### 5. Seed the Database

Configure the HANA connection values required by `hana/seed_data.py`, then run:

```bash
python hana/seed_data.py
```

The seed script generates sample NorthWind data for the project tables and performs verification queries.

---

### 6. Start the FastAPI Backend

From the project root:

```bash
uvicorn backend.app.main:app --reload
```

Or from the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

### 7. Start the MCP Server

Install MCP dependencies:

```bash
cd mcp_server
pip install -r requirements.txt
```

Set the backend URL if necessary:

```env
BACKEND_URL=http://127.0.0.1:8000
```

Run:

```bash
python server.py
```

The MCP server uses streamable HTTP transport and defaults to port `8001`.

---

## ☁️ SAP BTP Cloud Foundry Deployment

The project contains separate Cloud Foundry manifests for the FastAPI and MCP services.

### Deploy FastAPI

```bash
cd backend
cf push
```

### Deploy MCP Server

```bash
cd mcp_server
cf push
```

The manifests configure:

- Python buildpack
- 512 MB memory
- One application instance
- Random application routes

---

## 🔗 SAP BTP Destinations

The architecture uses two destinations:

```text
JouleOps_FastAPI
        ↓
FastAPI Cloud Foundry application

JouleOps_MCP
        ↓
MCP Cloud Foundry application
```

These destinations provide the connectivity layer between SAP BTP and the deployed services.

---

## 📊 API Testing

Swagger UI is automatically generated by FastAPI.

Open:

```text
http://127.0.0.1:8000/docs
```

Example:

```http
GET /materials/MAT-1023
```

Example response structure:

```json
{
  "material_id": "MAT-1023",
  "description": "Steel Coil",
  "category": "Steel",
  "stock_quantity": 12,
  "unit_price": 75000,
  "reorder_level": 50,
  "supplier_id": "SUP-001",
  "safety_stock": 50,
  "plant_code": "PLT-PUN"
}
```

---

## 📈 Key Capabilities Demonstrated

- Natural-language enterprise operation concept
- SAP HANA Cloud integration
- FastAPI microservice architecture
- REST-based business actions
- MCP-based tool integration
- Cloud Foundry deployment
- SAP BTP Destinations
- Role-based authorization
- Audit logging
- Pydantic validation
- Parameterized SQL
- Structured JSON responses
- Multi-step business workflow design

---

## ⚠️ Trial Environment Limitation

This project was developed in an SAP BTP trial / learning environment.

Some SAP Build Joule / Joule Studio capabilities were restricted by the available trial tenant. As a result, the underlying backend, HANA integration, MCP server, Cloud Foundry deployment, API endpoints, and BTP connectivity were implemented and tested independently.

The architecture is designed so that the backend services can be connected to a fully enabled Joule Agent environment.

This distinction is important: the repository demonstrates the **backend and integration implementation**, while live conversational execution through the Joule UI depends on the capabilities available in the target SAP BTP tenant.

---

## 📚 Documentation

The repository includes:

```text
JouleOps_NorthWind_Documentation.pdf
```

The documentation covers:

- Business scenario
- SAP BTP environment setup
- Architecture
- FastAPI implementation
- HANA Cloud integration
- MCP server
- Cloud Foundry deployment
- BTP Destinations
- Demo scenarios
- Security and governance
- Validation results

---

## 📄 License

This project was developed for learning and demonstration purposes.
