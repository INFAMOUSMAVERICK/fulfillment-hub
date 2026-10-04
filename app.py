import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title='Fulfillment Hub', page_icon='📦', layout='wide')

# -----------------------------
# Sample data
# -----------------------------
@st.cache_data
def load_data():
    now = datetime(2026, 9, 30, 15, 30)
    orders = pd.DataFrame([
        ['ORD-1001','Amazon','CUST-001','SKU-RED-M','Classic T-Shirt Red / M',1,'Priority','Order Received','2026-09-30 10:05','15:00',''],
        ['ORD-1002','Shopify','CUST-002','SKU-BLU-L','Classic T-Shirt Blue / L',2,'Regular','Picking','2026-09-30 09:20','18:00',''],
        ['ORD-1003','Flipkart','CUST-003','SKU-SHOE-42','Running Shoe / 42',1,'Priority','Inventory Hold','2026-09-30 08:45','14:30','Main warehouse short by 1; transfer required'],
        ['ORD-1004','Amazon','CUST-004','SKU-MUG-WHT','Ceramic Mug / White',4,'Regular','Packing','2026-09-30 11:10','19:00',''],
        ['ORD-1005','Shopify','CUST-005','SKU-BAG-BLK','Laptop Backpack / Black',1,'Priority','Staged','2026-09-30 08:15','16:00','Waiting for courier pickup'],
        ['ORD-1006','Amazon','CUST-006','SKU-HOOD-GRY','Hoodie / Grey / L',1,'Regular','Courier Exception','2026-09-30 07:55','17:00','Courier pickup missed at 14:00'],
        ['ORD-1007','Flipkart','CUST-007','SKU-RED-M','Classic T-Shirt Red / M',3,'Regular','Picking','2026-09-30 12:05','20:00',''],
        ['ORD-1008','Amazon','CUST-008','SKU-SHOE-42','Running Shoe / 42',1,'Priority','Packed','2026-09-30 09:50','17:30',''],
        ['ORD-1009','Shopify','CUST-009','SKU-MUG-WHT','Ceramic Mug / White',2,'Regular','Order Received','2026-09-30 13:15','21:00',''],
        ['ORD-1010','Amazon','CUST-010','SKU-BAG-BLK','Laptop Backpack / Black',2,'Priority','Inventory Hold','2026-09-30 10:40','16:30','Main warehouse short by 2; transfer required'],
    ], columns=['Order ID','Channel','Customer','SKU','Product','Qty','Priority','Status','Order Time','Ship Deadline','Issue'])
    inventory = pd.DataFrame([
        ['SKU-RED-M','Classic T-Shirt Red / M','Main Warehouse',12,15,20],
        ['SKU-BLU-L','Classic T-Shirt Blue / L','Main Warehouse',8,8,12],
        ['SKU-SHOE-42','Running Shoe / 42','Main Warehouse',0,3,8],
        ['SKU-SHOE-42','Running Shoe / 42','Overflow Warehouse',6,0,8],
        ['SKU-MUG-WHT','Ceramic Mug / White','Main Warehouse',20,10,30],
        ['SKU-BAG-BLK','Laptop Backpack / Black','Main Warehouse',0,3,10],
        ['SKU-BAG-BLK','Laptop Backpack / Black','Overflow Warehouse',7,0,10],
        ['SKU-HOOD-GRY','Hoodie / Grey / L','Main Warehouse',5,4,10],
    ], columns=['SKU','Product','Warehouse','On Hand','Reserved','Reorder Point'])
    events = pd.DataFrame([
        ['EX-001','ORD-1003','Inventory','High','Main stock unavailable; transfer 1 unit from Overflow','Open','15:00'],
        ['EX-002','ORD-1005','Staging','Medium','Packed box awaiting courier pickup','Open','16:00'],
        ['EX-003','ORD-1006','Courier','High','Courier missed scheduled pickup','Open','14:00'],
        ['EX-004','ORD-1010','Inventory','High','Main stock unavailable; transfer 2 units from Overflow','Open','16:30'],
    ], columns=['Exception ID','Order ID','Type','Severity','Description','Status','Target Time'])
    return orders, inventory, events

orders, inventory, exceptions = load_data()

# State for simple demo interactions
if 'orders' not in st.session_state:
    st.session_state.orders = orders.copy()
if 'exceptions' not in st.session_state:
    st.session_state.exceptions = exceptions.copy()

orders = st.session_state.orders
exceptions = st.session_state.exceptions

# -----------------------------
# Helpers
# -----------------------------
def kpi_count(condition):
    return int(condition.sum()) if hasattr(condition, 'sum') else int(condition)

st.title('📦 Fulfillment Hub')
st.caption('A simple operations cockpit for XYZ — prioritize, verify, pack, stage and resolve exceptions.')

# Sidebar
with st.sidebar:
    st.header('Filters')
    priority = st.multiselect('Priority', ['Priority','Regular'], default=['Priority','Regular'])
    status_options = sorted(orders['Status'].unique().tolist())
    status = st.multiselect('Status', status_options, default=status_options)
    channel = st.multiselect('Channel', sorted(orders['Channel'].unique()), default=sorted(orders['Channel'].unique()))
    st.divider()
    st.markdown('**Demo workflow**')
    st.markdown('1. Find priority orders\n2. Resolve inventory holds\n3. Pack and stage\n4. Clear courier exceptions')

filtered = orders[
    orders['Priority'].isin(priority) &
    orders['Status'].isin(status) &
    orders['Channel'].isin(channel)
].copy()

# KPIs
c1,c2,c3,c4,c5 = st.columns(5)
with c1: st.metric('Orders today', len(orders))
with c2: st.metric('Priority orders', int((orders.Priority=='Priority').sum()))
with c3: st.metric('Inventory holds', int((orders.Status=='Inventory Hold').sum()))
with c4: st.metric('Open exceptions', int((exceptions.Status=='Open').sum()))
with c5: st.metric('Staged / awaiting pickup', int((orders.Status=='Staged').sum()))

# Alerts
priority_at_risk = orders[(orders.Priority=='Priority') & orders.Status.isin(['Order Received','Inventory Hold','Picking','Packing'])]
if len(priority_at_risk):
    st.warning(f'⚠️ {len(priority_at_risk)} priority order(s) still need action before their shipping deadline.')

# Tabs
ops, inventory_tab, exceptions_tab, order_tab = st.tabs(['🧭 Operations Board','📊 Inventory','🚨 Exceptions','🔎 Order Lookup'])

with ops:
    st.subheader('Today’s fulfillment queue')
    display = filtered.copy()
    display['Deadline'] = pd.to_datetime(display['Ship Deadline']).dt.strftime('%d %b %H:%M')
    display = display[['Order ID','Priority','Channel','Product','Qty','Status','Deadline','Issue']]
    st.dataframe(display, use_container_width=True, hide_index=True)

    st.markdown('### Quick actions')
    col1, col2, col3 = st.columns(3)
    with col1:
        pick_id = st.selectbox('Move order to Picking', orders[orders.Status.isin(['Order Received'])]['Order ID'].tolist() or ['No eligible orders'])
        if st.button('▶ Start picking', disabled=pick_id=='No eligible orders', use_container_width=True):
            st.session_state.orders.loc[st.session_state.orders['Order ID']==pick_id,'Status']='Picking'
            st.rerun()
    with col2:
        pack_id = st.selectbox('Move order to Packed', orders[orders.Status.isin(['Picking'])]['Order ID'].tolist() or ['No eligible orders'])
        if st.button('📦 Mark packed', disabled=pack_id=='No eligible orders', use_container_width=True):
            st.session_state.orders.loc[st.session_state.orders['Order ID']==pack_id,'Status']='Packed'
            st.rerun()
    with col3:
        stage_id = st.selectbox('Move order to Staged', orders[orders.Status.isin(['Packed','Packing'])]['Order ID'].tolist() or ['No eligible orders'])
        if st.button('🚚 Stage for courier', disabled=stage_id=='No eligible orders', use_container_width=True):
            st.session_state.orders.loc[st.session_state.orders['Order ID']==stage_id,'Status']='Staged'
            st.rerun()

    st.info('Design choice: the warehouse team sees only the actions they need. Detailed spreadsheets are replaced by a status-driven queue and exception list.')

with inventory_tab:
    st.subheader('Inventory verification')
    inv = inventory.copy()
    inv['Available'] = inv['On Hand'] - inv['Reserved']
    inv['Health'] = inv.apply(lambda r: '🔴 Hold / transfer needed' if r['Available'] <= 0 else ('🟡 Reorder soon' if r['Available'] <= r['Reorder Point'] else '🟢 Available'), axis=1)
    st.dataframe(inv[['SKU','Product','Warehouse','On Hand','Reserved','Available','Reorder Point','Health']], use_container_width=True, hide_index=True)

    st.subheader('Transfer recommendations')
    held = orders[orders.Status=='Inventory Hold'][['Order ID','SKU','Qty','Product','Issue']]
    if len(held):
        for _, r in held.iterrows():
            overflow = inventory[(inventory.SKU==r.SKU) & (inventory.Warehouse=='Overflow Warehouse')]['On Hand'].sum()
            st.write(f"**{r['Order ID']}** — transfer **{int(r['Qty'])}** × {r['Product']} from Overflow (available: {int(overflow)}).")
    else:
        st.success('No inventory holds.')

with exceptions_tab:
    st.subheader('Exception inbox')
    ex = st.session_state.exceptions.copy()
    st.dataframe(ex, use_container_width=True, hide_index=True)
    open_ex = ex[ex.Status=='Open']
    if len(open_ex):
        resolve_id = st.selectbox('Resolve exception', open_ex['Exception ID'].tolist())
        if st.button('✅ Mark resolved', use_container_width=True):
            st.session_state.exceptions.loc[st.session_state.exceptions['Exception ID']==resolve_id,'Status']='Resolved'
            order_id = st.session_state.exceptions.loc[st.session_state.exceptions['Exception ID']==resolve_id,'Order ID'].iloc[0]
            # For demo purposes, move courier exception forward; inventory exception remains visible until manually processed.
            if st.session_state.orders.loc[st.session_state.orders['Order ID']==order_id,'Status'].iloc[0]=='Courier Exception':
                st.session_state.orders.loc[st.session_state.orders['Order ID']==order_id,'Status']='Staged'
            st.rerun()

with order_tab:
    st.subheader('Single-order lookup')
    oid = st.selectbox('Order ID', orders['Order ID'].tolist())
    row = orders[orders['Order ID']==oid].iloc[0]
    a,b,c = st.columns(3)
    a.metric('Status', row['Status'])
    b.metric('Priority', row['Priority'])
    c.metric('Ship deadline', row['Ship Deadline'])
    st.write(f"**Product:** {row['Product']}  \n**Quantity:** {row['Qty']}  \n**Channel:** {row['Channel']}  \n**Issue:** {row['Issue'] or 'None'}")
    st.markdown('**Suggested next action**')
    next_action = {
        'Order Received':'Start picking',
        'Inventory Hold':'Transfer stock from Overflow, then release to picking',
        'Picking':'Complete pick and verify SKU/variant',
        'Packing':'Pack and verify shipping label',
        'Packed':'Stage box in courier zone',
        'Staged':'Confirm courier pickup',
        'Courier Exception':'Contact courier and record new pickup time',
    }.get(row['Status'],'Review order')
    st.success(next_action)

st.divider()
st.caption('Prototype / sample data only. In production, this could connect to the order channel, inventory system and courier API.')
