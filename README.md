# Fulfillment Hub — XYZ Take-Home Project

A lightweight Streamlit prototype for managing e-commerce fulfillment from order receipt through courier pickup.

## What problem this solves

The prototype focuses on four operational risks that can directly cause late shipments, rework, or lost orders:

1. **Priority orders being missed** — a visible priority queue and KPI surface orders that still need action.
2. **Inventory mismatch / stock holds** — available stock is calculated separately from on-hand stock, with overflow-transfer recommendations.
3. **Orders getting stuck between packing and pickup** — staging is an explicit status rather than an informal spreadsheet note.
4. **Exceptions being forgotten** — a central exception inbox gives each issue a status and target time.

It also provides a single-order lookup so a warehouse/office user can quickly answer: “Where is this order and what should I do next?”

## Run locally

Requires Python 3.10+.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL shown by Streamlit, normally `http://localhost:8501`.

## Demo flow for reviewers

1. Open **Operations Board** and filter to **Priority**.
2. Show the KPI cards and priority-at-risk warning.
3. Use **Quick actions** to move an order through Picking → Packed → Staged.
4. Open **Inventory** and show why ORD-1003 / ORD-1010 are on hold and how overflow stock can be transferred.
5. Open **Exceptions** and resolve the missed courier pickup.
6. Use **Order Lookup** to demonstrate the “next action” guidance.

## Product decisions

### Why these features first?

The scenario contains many possible improvements. I deliberately avoided building a complex ERP-style application and prioritized workflow visibility and exception handling because the described problems are operational handoff failures:

**Order queue → Inventory verification → Pick → Pack → Stage → Courier → Exception resolution**

The interface therefore uses a small number of statuses and action buttons instead of requiring warehouse staff to navigate multiple spreadsheets or folders.

### What I would build next

- Barcode scanning for SKU and variant verification.
- Role-specific screens for office vs warehouse users.
- Real inventory reservation and transfer transactions.
- Courier API integration with pickup confirmation.
- Audit log for every status change.
- Authentication and permissions.
- Real-time alerts for approaching priority deadlines.
- Persistent database instead of demo session state.
