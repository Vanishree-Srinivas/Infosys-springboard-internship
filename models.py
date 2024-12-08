from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt

def predict_and_plot_trends(data_path):
    df = pd.read_csv(data_path)
    features = df[["Website Traffic", "Engagement Rate", "Product Availability"]]
    target = df["Sales Forecast"]

    # Train the model
    model = LinearRegression()
    model.fit(features, target)

    # Predict and plot
    df["Predicted Sales"] = model.predict(features)

    # Save the plot
    plt.figure(figsize=(10, 6))
    plt.plot(df["Sales Forecast"], label="Actual Sales Forecast", color="blue")
    plt.plot(df["Predicted Sales"], label="Predicted Sales Forecast", color="red")
    plt.legend()
    plt.title("Sales Forecast Prediction")
    plt.xlabel("Index")
    plt.ylabel("Sales Forecast")
    plt.savefig("data/prediction_plot.png")
    
    return "data/prediction_plot.png"
