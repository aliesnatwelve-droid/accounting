import streamlit as st
import pandas as pd
import sqlite3

def get_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect('accounting.db')
    conn.row_factory = sqlite3.Row
    return conn

def reset_categories_to_general():
    """Reset all categories to only have 'General' for each type"""
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    try:
        # Delete all existing categories
        cursor.execute("DELETE FROM categories")
        
        # Insert only 'General' for each category type
        general_categories = [
            ('General Asset', 'Asset'),
            ('General Liability', 'Liability'),
            ('General Equity', 'Equity'),
            ('General Income', 'Income'),
            ('General Expense', 'Expense')
        ]
        
        for name, typ in general_categories:
            cursor.execute("INSERT INTO categories (name, type) VALUES (?, ?)", (name, typ))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error resetting categories: {e}")
        return False
    finally:
        conn.close()

def delete_category_by_id(category_id):
    """Delete category by ID (permanent delete)"""
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    try:
        # Check if trying to delete a General category
        cursor.execute("SELECT name FROM categories WHERE id = ?", (category_id,))
        category = cursor.fetchone()
        
        if category and category[0].startswith('General'):
            return False, "Cannot delete General categories!"
        
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        return True, "Category deleted successfully!"
    except Exception as e:
        print(f"Error deleting category: {e}")
        return False, f"Error: {e}"
    finally:
        conn.close()

def check_category_has_transactions(category_id):
    """Check if category has any transactions"""
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE category_id = ?", (category_id,))
        count = cursor.fetchone()[0]
        return count > 0, count
    except Exception as e:
        print(f"Error checking transactions: {e}")
        return False, 0
    finally:
        conn.close()

def show():
    st.title("📂 Manage Categories")
    st.markdown("---")
    
    # Reset button to restore General categories
    col1, col2 = st.columns([3, 1])
    # with col2:
    #     if st.button("🔄 Reset to General", use_container_width=True, type="secondary"):
    #         if reset_categories_to_general():
    #             st.success("Categories reset to General only!")
    #             st.rerun()
    #         else:
    #             st.error("Error resetting categories!")
    
    # st.markdown("---")
    
    # View categories
    st.subheader("📋 Categories Structure")
    
    conn = sqlite3.connect('accounting.db')
    df = pd.read_sql("SELECT id, name, type FROM categories ORDER BY type, name", conn)
    conn.close()
    
    if not df.empty:
        # Show by type
        for cat_type in ["Asset", "Liability", "Equity", "Income", "Expense"]:
            type_df = df[df['type'] == cat_type]
            if not type_df.empty:
                with st.expander(f"**{cat_type}**", expanded=True):
                    # Display as simple list
                    for _, row in type_df.iterrows():
                        st.write(f"• {row['name']}")
        
        st.markdown("---")
        
        # Add new sub-category section (optional for users)
        st.subheader(" Add New Sub-Category (Optional)")
        st.caption("You can add custom sub-categories under each main category type")
        
        with st.form("add_category"):
            col1, col2 = st.columns(2)
            
            with col1:
                cat_name = st.text_input("Sub-Category Name", placeholder="e.g., Salary, Groceries, Rent...")
            
            with col2:
                cat_type = st.selectbox("Main Category Type", 
                                       ["Asset", "Liability", "Equity", "Income", "Expense"])
            
            submitted = st.form_submit_button("Add Sub-Category", use_container_width=True)
            
            if submitted:
                if cat_name:
                    conn = sqlite3.connect('accounting.db')
                    cursor = conn.cursor()
                    try:
                        cursor.execute("INSERT INTO categories (name, type) VALUES (?, ?)", (cat_name, cat_type))
                        conn.commit()
                        st.success(f"Sub-category '{cat_name}' added under {cat_type}!")
                        st.rerun()
                    except Exception as e:
                        st.error("Category already exists!")
                    finally:
                        conn.close()
                else:
                    st.error("Please enter a category name")
        
        st.markdown("---")
        
        # Delete category section (only for sub-categories)
        # Filter out General categories for deletion
        non_general_df = df[~df['name'].str.startswith('General')]
        
        if not non_general_df.empty:
            st.subheader("🗑️ Delete Sub-Category")
            st.caption("Note: General categories cannot be deleted")
            
            # Create options for selectbox (only sub-categories)
            cat_options = {row['name']: row['id'] for _, row in non_general_df.iterrows()}
            selected_cat = st.selectbox("Select sub-category to delete", list(cat_options.keys()))
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                delete_button = st.button("Delete Sub-Category", type="secondary", use_container_width=True)
            
            if delete_button:
                # Check if category has transactions
                has_trans, trans_count = check_category_has_transactions(cat_options[selected_cat])
                
                if has_trans:
                    st.error(f"Cannot delete '{selected_cat}' because it has {trans_count} transaction(s)!")
                else:
                    # Delete the category
                    success, message = delete_category_by_id(cat_options[selected_cat])
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    else:
        st.info("No categories found. Resetting to General...")
        reset_categories_to_general()
        st.rerun()
    
    st.markdown("---")
    
    # Show categories count
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM categories")
    total_cats = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM categories WHERE name LIKE 'General%'")
    general_cats = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM categories WHERE name NOT LIKE 'General%'")
    sub_cats = cursor.fetchone()[0]
    conn.close()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"📊 Total Categories: {total_cats}")
    with col2:
        st.caption(f"🔹 Main Categories: {general_cats}")
    with col3:
        st.caption(f"📎 Sub-Categories: {sub_cats}")