import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

def calculate_net_profit_and_update_equity():
    """محاسبه خودکار سود خالص و به‌روزرسانی Equity"""
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    # محاسبه مجموع درآمدها
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE category_id IN (SELECT id FROM categories WHERE type = 'Income')")
    total_income = cursor.fetchone()[0] or 0
    
    # محاسبه مجموع هزینه‌ها
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE category_id IN (SELECT id FROM categories WHERE type = 'Expense')")
    total_expense = cursor.fetchone()[0] or 0
    
    # محاسبه مجموع Equity مستقیم (سرمایه اولیه و ...)
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE category_id IN (SELECT id FROM categories WHERE type = 'Equity')")
    direct_equity = cursor.fetchone()[0] or 0
    
    # محاسبه سود خالص
    net_profit = total_income - total_expense
    
    # Equity نهایی = Equity مستقیم + سود خالص
    total_equity = direct_equity + net_profit
    
    # ذخیره در جدول retained_earnings
    cursor.execute('''
        INSERT INTO retained_earnings (calculation_date, total_income, total_expense, net_profit, accumulated_equity)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), total_income, total_expense, net_profit, total_equity))
    
    conn.commit()
    conn.close()
    
    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_profit': net_profit,
        'direct_equity': direct_equity,
        'total_equity': total_equity
    }

def show():
    st.title("📈 Financial Analysis")
    st.markdown("---")
    
    # دکمه برای محاسبه مجدد
    col1, col2 = st.columns([3, 1])
    
    if st.button("🔄 Recalculate Accounting Equation", use_container_width=True):
        calculate_net_profit_and_update_equity()
        st.success("Accounting equation recalculated!")
        st.rerun()

    st.markdown("---")
    
    with sqlite3.connect('accounting.db') as conn:
        df = pd.read_sql('''
            SELECT t.id, t.date, t.description, c.name as category, c.type, t.amount
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            ORDER BY t.date DESC
        ''', conn)
    
    if df.empty:
        st.info("No data available. Add some transactions first!")
        return
    
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%Y-%m')
    df['year'] = df['date'].dt.year
    df['quarter'] = df['date'].dt.quarter
    df['day_name'] = df['date'].dt.day_name()
    
    # ========== FILTERS SECTION ==========
    st.subheader("🔍 Filters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        
        date_range = st.date_input(
            "Date Range",
            value=[min_date, max_date],
            min_value=min_date,
            max_value=max_date,
            key="date_filter"
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
    
    with col2:
        all_types = ['All'] + sorted(df['type'].unique().tolist())
        selected_type = st.selectbox("Transaction Type", all_types, key="type_filter")
        
        if selected_type != 'All':
            df = df[df['type'] == selected_type]
    
    with col3:
        all_cats = ['All'] + sorted(df['category'].unique().tolist())
        selected_cat = st.selectbox("Category", all_cats, key="cat_filter")
        
        if selected_cat != 'All':
            df = df[df['category'] == selected_cat]
    
    st.caption(f"Showing {len(df)} transactions")
    st.markdown("---")
    
    # ========== KEY METRICS WITH AUTOMATIC EQUITY CALCULATION ==========
    st.subheader("🎯 Key Metrics")
    
    # محاسبه خودکار مقادیر
    total_income = df[df['type'] == 'Income']['amount'].sum()
    total_expense = df[df['type'] == 'Expense']['amount'].sum()
    total_assets = df[df['type'] == 'Asset']['amount'].sum()
    total_liabilities = df[df['type'] == 'Liability']['amount'].sum()
    direct_equity = df[df['type'] == 'Equity']['amount'].sum()
    
    # محاسبه سود خالص و Equity نهایی
    net_profit = total_income - total_expense
    total_equity = direct_equity + net_profit
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("💰 Total Income", f"{total_income:,.0f}")
    with col2:
        st.metric("💸 Total Expense", f"{total_expense:,.0f}")
    with col3:
        delta_color = "normal" if net_profit >= 0 else "inverse"
        st.metric("📈 Net Profit", f"{net_profit:,.0f}", 
                 delta=f"{(net_profit/total_income*100 if total_income > 0 else 0):.1f}%" if total_income > 0 else None)
    with col4:
        st.metric("🏦 Assets", f"{total_assets:,.0f}")
    with col5:
        st.metric("📋 Liabilities", f"{total_liabilities:,.0f}")
    
    st.markdown("---")
    
    # ========== ACCOUNTING EQUATION SECTION ==========
    st.subheader("🧾 Accounting Equation")
    
    # نمایش معادله حسابداری با توضیح
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: #e8f5e9; padding: 1rem; border-radius: 10px; text-align: center;">
            <h3>🏦 ASSETS</h3>
            <h2>{total_assets:,.0f}</h2>
            <p style="font-size: 0.8rem;">دارایی‌ها</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: #fff3e0; padding: 1rem; border-radius: 10px; text-align: center;">
            <h3>📋 LIABILITIES</h3>
            <h2>{total_liabilities:,.0f}</h2>
            <p style="font-size: 0.8rem;">بدهی‌ها</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background-color: #e3f2fd; padding: 1rem; border-radius: 10px; text-align: center;">
            <h3>👥 EQUITY</h3>
            <h2>{total_equity:,.0f}</h2>
            <p style="font-size: 0.8rem;">حقوق صاحبان سهام</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # نمایش نحوه محاسبه Equity
    st.markdown("### 📊 How Equity is Calculated:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Direct Equity:**\n{direct_equity:,.0f} Rials\n(Initial Capital, etc.)")
    
    with col2:
        st.success(f"**Net Profit:**\n{total_income:,.0f} - {total_expense:,.0f} = {net_profit:,.0f} Rials")
    
    with col3:
        st.primary(f"**Total Equity = Direct Equity + Net Profit**\n{total_equity:,.0f} = {direct_equity:,.0f} + {net_profit:,.0f}")
    
    st.markdown("---")
    
    # بررسی تعادل معادله
    st.subheader("⚖️ Equation Balance Check")
    
    left_side = total_assets
    right_side = total_liabilities + total_equity
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Left Side (Assets)", f"{left_side:,.0f}")
    
    with col2:
        st.metric("Right Side (Liabilities + Equity)", f"{right_side:,.0f}")
    
    if abs(left_side - right_side) < 1:
        st.success("✅ **ACCOUNTING EQUATION IS BALANCED!**")
        st.balloons()
    else:
        st.error(f"⚠️ **DIFFERENCE OF {abs(left_side - right_side):,.0f} RIALS**")
        st.warning("Check your category assignments. Make sure:\n- Income/Expense are properly categorized\n- Assets/Liabilities/Equity are correct")
    
    st.markdown("---")
    
    # ادامه کد قبلی برای TAB‌ها...
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "💰 Income Analysis", "💸 Expense Analysis", "📅 Trends", "📋 Reports"])
    
    # ... (بقیه کد TAB‌ها به همان صورت قبلی می‌ماند)