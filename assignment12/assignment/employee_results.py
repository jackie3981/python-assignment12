import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../db/lesson.db")

def employee_info(cursor):
    query = """
        SELECT last_name, 
               SUM(price * quantity) AS revenue
        FROM employees e
        JOIN orders o ON e.employee_id = o.employee_id
        JOIN line_items l ON o.order_id = l.order_id
        JOIN products p ON l.product_id = p.product_id
        GROUP BY e.employee_id;
    """
    cursor.execute(query)
    return cursor.fetchall()


    
try:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        conn.execute("PRAGMA foreign_keys = 1")

        results = employee_info(cursor)

        # show result using pandas
        df = pd.DataFrame(results, columns=["last_name", "revenue"])
        print("\nDataFrame:\n", df)

    df.plot(x="last_name", y="revenue", kind="bar", color="skyblue", title="Employee Revenue")
    plt.show()

except sqlite3.Error as e:
    print(f"Database error: {e}")