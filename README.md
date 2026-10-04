# 📦 Fulfillment Hub

### XYZ E-commerce Fulfillment Operations — Take-Home Project

A lightweight Streamlit application designed to help a growing e-commerce business manage order fulfillment from **order receipt → inventory verification → picking → packing → staging → courier pickup**.

The goal is not to replace a full warehouse management system, but to provide a **simple operational cockpit** that makes priority orders, inventory issues, and fulfillment exceptions visible and actionable.

---

## 🎯 Problem

XYZ currently manages fulfillment using spreadsheets, shared folders, printed documents, and informal communication.

As order volume grows, several operational problems appear:

* Priority orders can get mixed with regular orders and miss shipping deadlines.
* Inventory shown in spreadsheets may not match physical stock.
* Orders can become blocked because stock is sitting in the overflow warehouse.
* Wrong products or variants can be picked or shipped.
* Packed orders can be misplaced while waiting for courier pickup.
* Missed courier pickups can go unnoticed.
* Operational issues are often handled informally and can be forgotten.

### Product approach

I focused on the problems with the highest potential operational impact:

> **Visibility → Inventory verification → Workflow progression → Exception management**

Rather than building a complex ERP-style system, I created a small number of clear workflow states and actions that a warehouse team can understand quickly.

---

# 🚀 Key Features

## 1. 🧭 Operations Board

Provides a single view of today's fulfillment queue.

### Includes:

* Priority vs regular orders
* Current fulfillment status
* Sales channel
* Product and quantity
* Shipping deadline
* Current issue
* Priority-at-risk warning
* Quick workflow actions

### Workflow

```text
Order Received
      ↓
   Picking
      ↓
    Packed
      ↓
    Staged
      ↓
Courier Pickup
```

The interface allows warehouse users to move eligible orders through the workflow without editing spreadsheets manually.

---

## 2. 📊 Inventory Verification

Inventory is separated into:

* Main Warehouse
* Overflow Warehouse

The application calculates:

```text
Available Stock = On Hand - Reserved
```

It then highlights inventory that needs attention.

For example:

```text
Running Shoe / 42

Main Warehouse:
Available = 0

Overflow Warehouse:
Available = 6

→ Transfer stock before picking
```

This directly addresses the scenario where inventory exists physically but cannot be picked because it is stored in the secondary warehouse.

---

## 3. 🚨 Exception Inbox

Operational problems are treated as explicit exceptions instead of informal notes.

Example exception types:

* Inventory shortage
* Staging delay
* Courier pickup failure

Each exception contains:

* Exception ID
* Order ID
* Type
* Severity
* Description
* Status
* Target time

Exceptions can be marked as resolved directly from the application.

---

## 4. 🔎 Order Lookup

Users can quickly search an individual order and see:

* Current status
* Priority
* Shipping deadline
* Product
* Quantity
* Sales channel
* Current issue
* Suggested next action

Example:

```text
Status: Inventory Hold

Suggested next action:
Transfer stock from Overflow, then release to picking
```

This answers the operational question:

> **"Where is this order and what should I do next?"**

---

# 🧠 Product Decisions

The scenario contains many possible problems that could be solved.

I deliberately prioritized **workflow visibility and exception handling** because these problems occur at operational handoffs:

```text
Order
  ↓
Inventory
  ↓
Picking
  ↓
Packing
  ↓
Staging
  ↓
Courier
  ↓
Exception resolution
```

A failure at any of these handoffs can cause:

* Late shipments
* Rework
* Customer dissatisfaction
* Lost inventory
* Missed courier pickups

Therefore, the MVP focuses on making these handoffs visible and actionable.

---

# 🛠️ Technology

| Technology    | Purpose                           |
| ------------- | --------------------------------- |
| Python        | Application logic                 |
| Streamlit     | Web application interface         |
| Pandas        | Data manipulation and analysis    |
| Session State | Demonstration of workflow updates |

The project uses **sample data only** and does not connect to real store, inventory, customer, or courier systems.

---

# 📁 Project Structure

```text
fulfillment-hub/
│
├── app.py
├── requirements.txt
├── README.md
├── AI_USAGE_NOTE.md
└── WALKTHROUGH_SCRIPT.md
```

---

# ▶️ Run Locally

### Requirements

* Python 3.10+
* Internet connection for installing dependencies

### 1. Clone the repository

```bash
git clone https://github.com/INFAMOUSMAVERICK/fulfillment-hub.git
cd fulfillment-hub
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the application

```bash
streamlit run app.py
```

Then open the local URL provided by Streamlit, normally:

```text
http://localhost:8501
```

---

# 🎬 Suggested Demo Flow

A reviewer can understand the application through the following short workflow:

### 1. Operations Board

Filter to **Priority** orders and show the priority-at-risk warning.

### 2. Workflow Actions

Move an order through:

```text
Order Received → Picking → Packed → Staged
```

### 3. Inventory

Open the Inventory tab and demonstrate the shortage for:

* `ORD-1003`
* `ORD-1010`

Show how stock in the Overflow Warehouse can be transferred to the Main Warehouse.

### 4. Exceptions

Open the Exception Inbox and resolve the missed courier pickup.

### 5. Order Lookup

Search for an order and demonstrate how the application provides the next recommended action.

---

# 📌 Sample Scenarios

The demo dataset intentionally contains different operational situations.

| Order    | Priority | Status            | Scenario                |
| -------- | -------- | ----------------- | ----------------------- |
| ORD-1001 | Priority | Order Received    | Needs picking           |
| ORD-1002 | Regular  | Picking           | Active warehouse work   |
| ORD-1003 | Priority | Inventory Hold    | Main warehouse shortage |
| ORD-1004 | Regular  | Packing           | Ready for staging       |
| ORD-1005 | Priority | Staged            | Waiting for courier     |
| ORD-1006 | Regular  | Courier Exception | Pickup missed           |
| ORD-1008 | Priority | Packed            | Ready for staging       |
| ORD-1010 | Priority | Inventory Hold    | Main warehouse shortage |

This allows the reviewer to see multiple fulfillment scenarios without requiring any external integrations.

---

# 🔮 What I Would Build Next

If this MVP were taken into production, I would prioritize:

### 1. Barcode scanning

Scan the SKU and variant during picking and packing to reduce wrong-item shipments.

### 2. Real inventory reservations

Replace demo calculations with transactional inventory updates.

### 3. Role-based screens

Provide simpler interfaces for warehouse workers while giving office users more detailed operational controls.

### 4. Courier integration

Connect to courier APIs for pickup booking, tracking, and pickup confirmation.

### 5. Audit log

Record who changed an order, what changed, and when.

### 6. Real-time alerts

Notify the team when a priority order is approaching its shipping deadline.

### 7. Persistent database

Replace Streamlit session state with a production database.

### 8. Authentication and permissions

Ensure warehouse, operations, and management users only see and modify the information relevant to them.

---

# 🤖 AI Usage

AI tools were used during the project to support:

* Brainstorming possible fulfillment workflows
* Structuring the sample dataset
* Generating and refining Streamlit/Pandas implementation ideas
* Reviewing the application flow
* Improving documentation and presentation

Importantly, AI suggestions were treated as a starting point rather than accepted automatically. The final product decisions were based on the requirements of the scenario, usability for a warehouse team with limited technical comfort, and the need to keep the MVP simple.

More details are available in:

**[AI_USAGE_NOTE.md](AI_USAGE_NOTE.md)**

---

# 🎥 Walkthrough

A short walkthrough script is included in:

**[WALKTHROUGH_SCRIPT.md](WALKTHROUGH_SCRIPT.md)**

The intended walkthrough is under the required **5-minute maximum**.

---

# ⚠️ Project Scope

This is a **prototype using fictional sample data** created specifically for the XYZ take-home assignment.

It does not connect to:

* Amazon
* Shopify
* Flipkart
* Real courier APIs
* Real inventory systems
* Real customer data

The architecture is intentionally lightweight so that the core product decisions and workflow can be evaluated easily.

---

## 👤 Author

**Saksham Sharma**

B.Tech Graduate | Data Analytics & Business Analytics

GitHub: https://github.com/INFAMOUSMAVERICK

LinkedIn: https://www.linkedin.com/in/sakshamosharma

---

### ⭐ Project Summary

**Fulfillment Hub turns a spreadsheet-driven fulfillment process into a simple, status-driven operational workflow — making priority orders, inventory blockers, and exceptions visible before they become missed shipments.**
