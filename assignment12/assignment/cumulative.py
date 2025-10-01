import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../db/lesson.db")

def get_order_totals(cursor):
    query = """
        SELECT o.order_id,
               SUM(l.quantity * p.price) AS total_price
        FROM orders o
        JOIN line_items l ON o.order_id = l.order_id
        JOIN products p ON l.product_id = p.product_id
        GROUP BY o.order_id
        ORDER BY o.order_id;
    """
    cursor.execute(query)
    return cursor.fetchall()

try:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        conn.execute("PRAGMA foreign_keys = 1")

        results = get_order_totals(cursor)

        # Convert results to DataFrame
        df = pd.DataFrame(results, columns=["order_id", "total_price"])
        print("\nInitial DataFrame:\n", df)

    def cumulative(row):
        totals_above = df['total_price'][0:row.name+1]
        return totals_above.sum()

    df["cumulative"] = df.apply(cumulative, axis=1)
    # Alternatively, using cumsum for cumulative sum
    # df["cumulative"] = df["total_price"].cumsum()
    print("\nDataFrame with Cumulative Totals:\n", df)

    # Plot cumulative revenue vs. order_id
    df.plot(x="order_id", y="cumulative", kind="line", marker="o", title="Cumulative Revenue")
    plt.xlabel("Order ID")
    plt.ylabel("Cumulative Revenue")
    plt.show()

except sqlite3.Error as e:
    print(f"Database error: {e}")
