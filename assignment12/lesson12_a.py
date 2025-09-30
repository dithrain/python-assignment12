import pandas as pd
import matplotlib.pyplot as plt

# Load a dataset
data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Sales": [100, 150, 200, 250, 300, 350],
    "Expenses": [80, 120, 180, 200, 220, 300]
}
df = pd.DataFrame(data)

#printing to png because i'm using remote desktop that breaks interactive plots
# Line Plot
df.plot(x="Month", y=["Sales", "Expenses"], kind="line", title="Sales vs. Expenses")
plt.savefig("line_plot.png")   # save to file
plt.close()

# Bar Plot
df.plot(x="Month", y="Sales", kind="bar", color="skyblue", title="Monthly Sales")
plt.savefig("bar_plot.png")   # save to file
plt.close()
