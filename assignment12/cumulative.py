import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

#locate db, robust
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db", "lesson.db"))
print("Looking for DB at:", db_path)

conn = sqlite3.connect(db_path)

#build per-order totals
#table is line_items, joined to products for price
query = """
SELECT
    o.order_id,
    SUM(p.price * l.quantity) AS total_price
FROM orders o
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_id
"""
df = pd.read_sql_query(query, conn)

#cumulative column, keep both for assignment
#use apply, per instructions
def cumulative(row):
    totals_above = df['total_price'].iloc[:row.name + 1]
    return totals_above.sum()

df['cumulative_apply'] = df.apply(cumulative, axis=1)

#idiomatic: cumsum()
df['cumulative'] = df['total_price'].cumsum()

#plot cumulative revenue vs order_id
ax = df.plot(x="order_id", y="cumulative", kind="line", title="Cumulative Revenue by Order")
ax.set_xlabel("Order ID")
ax.set_ylabel("Cumulative Revenue ($)")
plt.tight_layout()

#show and save
plt.savefig(os.path.join(os.path.dirname(__file__), "..", "cumulative_line.png"))
plt.show()

conn.close()

#print to see first few rows in the terminal
print(df.head())



#task 3

import re
import plotly.express as px
import plotly.data as pldata

#load the Plotly wind dataset as a df
wind_df = pldata.wind(return_type="pandas")

#print first and last 10 lines
print("\n[Task 3] wind_df head (10):")
print(wind_df.head(10))
print("\n[Task 3] wind_df tail (10):")
print(wind_df.tail(10))

#drop rows with missing strength or frequency
def strength_to_float(s):
    if pd.isna(s):
        return None
    s = str(s).strip()
    #handle ranges like 'a-b'
    if "-" in s:
        a, b = s.split("-", 1)
        try:
            return (float(a) + float(b)) / 2.0
        except ValueError:
            pass
    #grab first number if present as a fallback
    m = re.search(r"\d+(\.\d+)?", s)
    if m:
        return float(m.group())
    return None

wind_df["strength_num"] = wind_df["strength"].apply(strength_to_float)

#interactive scatter: strength vs frequency, color by direction
fig = px.scatter(
    wind_df,
    x="strength_num",
    y="frequency",
    color="direction",
    hover_data=["strength", "direction", "frequency"],
    title="Wind: Strength vs Frequency (colored by Direction)"
)

#save to HTML and open in browser
html_out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "wind.html"))
fig.write_html(html_out, auto_open=True)
print(f"[Task 3] Saved interactive plot to {html_out}")
