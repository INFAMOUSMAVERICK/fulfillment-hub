# 5-Minute Video Walkthrough Script

## 0:00–0:40 — Problem understanding

“XYZ's main problem is not simply that it uses spreadsheets. The bigger issue is that fulfillment has multiple handoffs, and there is no single place showing what needs attention.

I identified four high-impact failure points: priority orders can miss their deadline, inventory records can differ from physical stock, packed boxes can get stuck before courier pickup, and exceptions are handled informally and can be forgotten.”

## 0:40–1:15 — Product approach

“I designed the application around the actual warehouse flow: Order Received, Picking, Packing, Staged, Shipping, with Inventory Hold and Courier Exception as explicit exception states.

I intentionally kept the interface simple because the warehouse team is experienced but not very comfortable with technology.”

## 1:15–2:15 — Operations Board

“On the Operations Board, the team gets a single fulfillment queue. The KPI cards immediately show today's order volume, priority orders, inventory holds, open exceptions, and staged orders.

The warning highlights priority orders that still need action. I can filter the queue by priority, status, and sales channel.

The Quick Actions section lets a user move eligible orders from received to picking, packed, and staged without editing a spreadsheet.”

## 2:15–3:15 — Inventory

“Next is Inventory. I separate On Hand, Reserved, and Available inventory. This matters because stock being physically present doesn't necessarily mean it is available to fulfill an order.

For orders on Inventory Hold, the application shows the required transfer from the overflow warehouse. This directly addresses the scenario where the spreadsheet says stock exists but the main warehouse cannot pick it.”

## 3:15–4:05 — Exceptions

“The Exceptions tab is designed to stop operational problems from disappearing into chats or informal conversations. Each exception has an ID, order, type, severity, description, status, and target time.

For example, ORD-1006 has a missed courier pickup. The user can resolve the exception, and the demo moves the order back to the staging flow.”

## 4:05–4:40 — Order lookup

“Finally, Order Lookup answers the question a warehouse user is most likely to ask: where is this order and what should I do next?

For an inventory hold, it tells the user to transfer stock before releasing the order to picking. For a staged order, it tells them to confirm courier pickup.”

## 4:40–5:00 — Closing

“This is intentionally a prototype using sample data. In production, I would connect it to the order channels, inventory database, and courier API, add barcode scanning and authentication, and maintain an audit log of every status change.

The core design principle is to make exceptions visible early and reduce the number of manual handoffs.”
