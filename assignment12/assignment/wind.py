import plotly.express as px
import plotly.data as pldata
import pandas as pd
import re
from pathlib import Path
import webbrowser

# 1. Load wind dataset
df = pldata.wind(return_type="pandas")

# 2. Show first and last 10 rows (before cleaning)
print("\nFirst 10 rows (before cleaning):\n", df.head(10))
print("\nLast 10 rows (before cleaning):\n", df.tail(10))

# 3. Function to convert 'strength'
def convert_strength(val):
    s = str(val).strip()
    # range "a-b" -> average (a+b)/2
    m = re.match(r'^(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)$', s)
    if m:
        return (float(m.group(1)) + float(m.group(2))) / 2.0
    # case "6+" -> 6.5 
    m2 = re.match(r'^(\d+(?:\.\d+)?)\+$', s)
    if m2:
        return float(m2.group(1)) + 0.5
    # if a single number comes
    try:
        return float(s)
    except ValueError:
        return float("nan")

# Apply conversion to 'strength' column
df["strength"] = df["strength"].astype(str).apply(convert_strength)

# Show first 10 rows after cleaning to verify
print("\nFirst 10 rows (after cleaning):\n", df.head(10))
print("\nLast 10 rows (after cleaning):\n", df.tail(10))

# 4. Interactive scatter plot
fig = px.scatter(
    df,
    x="strength",
    y="frequency",
    color="direction",
    title="Wind Strength vs Frequency",
    labels={"strength": "Strength (numeric)", "frequency": "Frequency"}
)

# 5. Save plot as HTML and open in browser
html_path = Path("wind.html").resolve()
fig.write_html(html_path)
print(f"\nPlot saved as: {html_path}")

webbrowser.open(html_path.as_uri())
