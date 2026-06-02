import streamlit as st
import pandas as pd
import sqlite3
from database import get_connection

def show():
    st.title("🏠 Dashboard Home")
    st.markdown("---")
    
    with sqlite3.connect('accounting.db') as conn:
        df = pd.read_sql('''
            SELECT t.id, t.date, t.description, c.name as category, c.type, t.amount
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            ORDER BY t.date DESC
        ''', conn)
    
    if df.empty:
        st.info("✨ No transactions yet! Go to CALENDAR page to add your first transaction.")
        return
    
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    # محاسبه خودکار
    total_income = df[df['type'] == 'Income']['amount'].sum()
    total_expense = df[df['type'] == 'Expense']['amount'].sum()
    net_profit = total_income - total_expense
    direct_equity = df[df['type'] == 'Equity']['amount'].sum()
    total_equity = direct_equity + net_profit
    total_assets = df[df['type'] == 'Asset']['amount'].sum()
    total_liabilities = df[df['type'] == 'Liability']['amount'].sum()
    
    # Summary cards
    st.subheader("📊 Quick Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Income", f"{total_income:,.0f}")
    with col2:
        st.metric("💸 Total Expense", f"{total_expense:,.0f}")
    with col3:
        st.metric("📈 Net Profit", f"{net_profit:,.0f}", 
                 delta=None if net_profit == 0 else "Profit" if net_profit > 0 else "Loss")
    with col4:
        st.metric("📋 Transactions", len(df))
    
    st.markdown("---")
    
    # Accounting Equation Display
    st.subheader("🧾 Accounting Equation (Auto-calculated)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Assets", f"{total_assets:,.0f}")
    with col2:
        st.metric("Liabilities", f"{total_liabilities:,.0f}")
    with col3:
        st.metric("Equity (with Net Profit)", f"{total_equity:,.0f}")
    
    st.caption(f"Equity = Direct Equity ({direct_equity:,.0f}) + Net Profit ({net_profit:,.0f})")
    
    if abs(total_assets - (total_liabilities + total_equity)) < 1:
        st.success("✅ Accounting equation is balanced: Assets = Liabilities + Equity")
    else:
        st.warning("⚠️ Accounting equation is not balanced!")
    
    st.markdown("---")
    
    # Recent transactions
    st.subheader("📋 Recent Transactions")
    recent_df = df.head(10)[['date', 'description', 'category', 'amount']].copy()
    recent_df['amount'] = recent_df['amount'].apply(lambda x: f"{x:,.0f}")
    recent_df.columns = ['Date', 'Description', 'Category', 'Amount']
    st.dataframe(recent_df, use_container_width=True, hide_index=True)