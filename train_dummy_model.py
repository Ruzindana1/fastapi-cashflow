import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Example data: month index vs. cashflow
data = pd.DataFrame({
    "month_index": [9, 10, 11],  # September, October, November
    "cashflow": [1200, 1450, 1600]
})

X = data[["month_index"]]
y = data["cashflow"]

# Train a simple linear regression model
model = LinearRegression()
model.fit(X, y)

# Save the model to disk
with open("cashflow_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Dummy model saved as cashflow_model.pkl")
