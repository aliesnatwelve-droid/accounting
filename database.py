import sqlite3

def get_connection():
    conn = sqlite3.connect('accounting.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        # Categories table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('Asset', 'Liability', 'Equity', 'Income', 'Expense'))
            )
        ''')
        
        # Transactions table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT,
                category_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        # Check if categories table is empty
        cursor = conn.execute("SELECT COUNT(*) FROM categories")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insert only General categories
            general_categories = [
                ('General Asset', 'Asset'),
                ('General Liability', 'Liability'),
                ('General Equity', 'Equity'),
                ('General Income', 'Income'),
                ('General Expense', 'Expense')
            ]
            
            for name, typ in general_categories:
                conn.execute("INSERT INTO categories (name, type) VALUES (?, ?)", (name, typ))