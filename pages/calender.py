import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import get_connection

def show():
    st.title("📅 Financial Calendar")
    st.markdown("---")
    
    # Session state for current date
    if "calendar_date" not in st.session_state:
        st.session_state.calendar_date = datetime.now().date()
    if "balloons_shown" not in st.session_state:
        st.session_state.balloons_shown = {}
    
    # Navigation
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if st.button("◀◀ WEEK", use_container_width=True):
            st.session_state.calendar_date -= timedelta(days=7)
            st.rerun()
    
    with col2:
        if st.button("◀ DAY", use_container_width=True):
            st.session_state.calendar_date -= timedelta(days=1)
            st.rerun()
    
    with col3:
        # st.markdown(f"<h3 style='text-align: center;'>{st.session_state.calendar_date.strftime('%B %d, %Y')}</h3>", unsafe_allow_html=True)
        if st.button(" TODAY", use_container_width=True):
            st.session_state.calendar_date = datetime.now().date()
            st.rerun()
    
    with col4:
        if st.button("DAY ▶", use_container_width=True):
            st.session_state.calendar_date += timedelta(days=1)
            st.rerun()
    
    with col5:
        if st.button("WEEK ▶▶", use_container_width=True):
            st.session_state.calendar_date += timedelta(days=7)
            st.rerun()
    
    st.markdown("---")
    
    # Load transactions
    with get_connection() as conn:
        df = pd.read_sql('''
            SELECT t.id, t.date, t.description, c.name as category, c.type, t.amount
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            ORDER BY t.date DESC
        ''', conn)
    
    if not df.empty:
        df['date'] = pd.to_datetime(df['date']).dt.date
    
    # Get 7 days for tabs
    week_dates = [st.session_state.calendar_date + timedelta(days=i - 3) for i in range(7)]
    
    # Create tabs
    tab_labels = []
    for date in week_dates:
        if date == datetime.now().date():
            tab_labels.append(f"📌 {date.strftime('%a, %b %d')}")
        else:
            tab_labels.append(f"{date.strftime('%a, %b %d')}")
    
    tabs = st.tabs(tab_labels)
    
    # Display each day
    for idx, (tab, date) in enumerate(zip(tabs, week_dates)):
        with tab:
            st.subheader(f"Transactions for {date.strftime('%A, %B %d, %Y')}")
            
            # Filter transactions for this date
            if not df.empty:
                day_transactions = df[df['date'] == date].copy()
            else:
                day_transactions = pd.DataFrame()
            
            if not day_transactions.empty:
                # Summary
                total_income = day_transactions[day_transactions['type'] == 'Income']['amount'].sum()
                total_expense = day_transactions[day_transactions['type'] == 'Expense']['amount'].sum()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Income", f"{total_income:,.0f}")
                with col2:
                    st.metric("Expense", f"{total_expense:,.0f}")
                with col3:
                    st.metric("Balance", f"{total_income - total_expense:,.0f}")
                
                # Display transactions
                display_df = day_transactions[['description', 'category', 'amount']].copy()
                display_df['amount'] = display_df['amount'].apply(lambda x: f"{x:,.0f}")
                display_df.columns = ['Description', 'Category', 'Amount']
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # Delete section
                st.divider()
                st.markdown("**Delete Transaction**")
                trans_options = {f"{row['description']} - {row['amount']:,.0f}": row['id'] 
                               for _, row in day_transactions.iterrows()}
                selected = st.selectbox("Select transaction", list(trans_options.keys()), key=f"del_{idx}")
                if st.button("Delete", key=f"del_btn_{idx}"):
                    with get_connection() as conn:
                        conn.execute("DELETE FROM transactions WHERE id = ?", (trans_options[selected],))
                    st.success("Deleted!")
                    st.rerun()
            else:
                st.info("✨ No transactions for this day")
                day_key = date.strftime('%Y-%m-%d')
                if not st.session_state.balloons_shown.get(day_key, False):
                    st.balloons()
                    st.session_state.balloons_shown[day_key] = True
    
    # Add transaction section
    st.markdown("---")
    st.subheader(" Add New Transaction")
    
    with st.form("add_transaction"):
        col1, col2 = st.columns(2)
        
        with col1:
            trans_date = st.date_input("Date", st.session_state.calendar_date)
            
            with get_connection() as conn:
                categories = conn.execute("SELECT id, name, type FROM categories").fetchall()
            cat_options = {f"{cat['name']} ({cat['type']})": cat['id'] for cat in categories}
            selected_cat = st.selectbox("Category", list(cat_options.keys()))
        
        with col2:
            description = st.text_input("Description")
            amount = st.number_input("Amount", min_value=0.0, step=10000.0)
        
        if st.form_submit_button("Save Transaction", type="primary", use_container_width=True):
            if description and amount > 0:
                with get_connection() as conn:
                    conn.execute(
                        "INSERT INTO transactions (date, description, category_id, amount) VALUES (?, ?, ?, ?)",
                        (trans_date.isoformat(), description, cat_options[selected_cat], amount)
                    )
                st.success("Transaction added!")
                st.rerun()
            else:
                st.error("Please fill all fields")