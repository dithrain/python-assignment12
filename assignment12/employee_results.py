import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

#connect to db
db_path = Path(__file__).resolve().parent.parent / "db" / "lesson.db"
conn = sqlite3.connect(db_path)

#run the provided SQL to build the df
sql = """
SELECT last_name,
       SUM(price * quantity) AS revenue
FROM employees e
JOIN orders o     ON e.employee_id = o.employee_id
JOIN line_items l ON o.order_id   = l.order_id
JOIN products p   ON l.product_id = p.product_id
GROUP BY e.employee_id
ORDER BY revenue DESC;
"""
employee_results = pd.read_sql_query(sql, conn)
conn.close()

print(employee_results.head())  # sanity check in the terminal

#make the bar chart with Pandas' plot()
ax = employee_results.plot(
    x="last_name",
    y="revenue",
    kind="bar",
    legend=False,
    color="#4C78A8",  
    figsize=(8, 5),
    title="Employee Revenue (sum of price × quantity)"
)
ax.set_xlabel("Employee (Last Name)")
ax.set_ylabel("Revenue ($)")
plt.tight_layout()

#save a PNG
out_png = Path(__file__).resolve().parent / "employee_results.png"
plt.savefig(out_png, dpi=150)
print(f"Saved chart to {out_png}")

#try to show the window if environment supports it
try:
    plt.show()
except Exception:
    #headless environment
    pass
