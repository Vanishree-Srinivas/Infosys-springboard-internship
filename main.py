from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from backend.models import predict_and_plot_trends

app = FastAPI()

# Load the dataset
df = pd.read_csv("data/ecommerce_sales_forecast_dataset.csv")

class MarketFilter(BaseModel):
    start_date: str
    end_date: str
    indicators: list[str]

@app.post("/filter-market-data")
def filter_market_data(filters: MarketFilter):
    filtered_data = df[
        (df["Customer Behavior"].notnull())  # Add any other relevant conditions here
    ][filters.indicators]
    return filtered_data.to_dict(orient="records")

@app.get("/predict-trend-chart")
def get_prediction_chart():
    chart_path = predict_and_plot_trends("data/ecommerce_sales_forecast_dataset.csv")
    return {"chart_path": chart_path}
