from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder
from datetime import datetime

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data and model
DATA_DIR = ".."
MODEL_PATH = os.path.join(DATA_DIR, "final_rf_model.pkl")

# Global variables for data
df = None
model = None
scaler = StandardScaler()
le = LabelEncoder()

def load_and_preprocess():
    global df, model, scaler, le
    
    # Load model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        print(f"Warning: Model not found at {MODEL_PATH}")

    # Load datasets
    sales_df = pd.read_csv(os.path.join(DATA_DIR, 'sales data-set.csv'))
    features_df = pd.read_csv(os.path.join(DATA_DIR, 'Features data set.csv'))
    stores_df = pd.read_csv(os.path.join(DATA_DIR, 'stores data-set.csv'))

    # Merge
    df = sales_df.merge(features_df, on=['Store', 'Date', 'IsHoliday'], how='left')
    df = df.merge(stores_df, on=['Store'], how='left')

    # Preprocessing (matching build.py)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Week'] = df['Date'].dt.isocalendar().week
    
    markdown_cols = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']
    df[markdown_cols] = df[markdown_cols].fillna(0)
    df['CPI'] = df['CPI'].fillna(df['CPI'].median())
    df['Unemployment'] = df['Unemployment'].fillna(df['Unemployment'].median())
    df['IsHoliday'] = df['IsHoliday'].astype(int)
    
    # Label encode Type
    df['Type'] = le.fit_transform(df['Type'])
    
    # Prepare scaler
    features = ['Store', 'Dept', 'IsHoliday', 'Size', 'Temperature', 'CPI', 'Unemployment', 'Year', 'Month', 'Week', 'Type']
    X = df[features]
    scaler.fit(X)

load_and_preprocess()

class PredictionInput(BaseModel):
    Store: int
    Dept: int
    IsHoliday: bool
    Size: int
    Temperature: float
    CPI: float
    Unemployment: float
    Date: str  # Format: YYYY-MM-DD
    Type: str  # 'A', 'B', or 'C'

@app.get("/api/stats")
async def get_stats():
    if df is None: return {"error": "Data not loaded"}
    
    total_sales = float(df['Weekly_Sales'].sum())
    avg_sales = float(df['Weekly_Sales'].mean())
    total_stores = int(df['Store'].nunique())
    total_depts = int(df['Dept'].nunique())
    
    return {
        "totalSales": total_sales,
        "avgSales": avg_sales,
        "totalStores": total_stores,
        "totalDepts": total_depts
    }

@app.get("/api/trends")
async def get_trends():
    if df is None: return {"error": "Data not loaded"}
    
    # Monthly sales trend
    monthly_sales = df.groupby('Month')['Weekly_Sales'].mean().reset_index()
    trends = monthly_sales.to_dict(orient='records')
    
    # Sales by store type
    type_sales = df.groupby('Type')['Weekly_Sales'].mean().reset_index()
    # Convert numeric type back to original labels
    type_sales['label'] = le.inverse_transform(type_sales['Type'])
    type_data = type_sales[['label', 'Weekly_Sales']].to_dict(orient='records')
    
    return {
        "monthly": trends,
        "byType": type_data
    }

@app.post("/api/predict")
async def predict(data: PredictionInput):
    if model is None: raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        dt = datetime.strptime(data.Date, "%Y-%m-%d")
        year = dt.year
        month = dt.month
        week = dt.isocalendar()[1]
        
        # Map Type back to encoded value
        type_encoded = le.transform([data.Type])[0]
        
        input_data = [
            data.Store, data.Dept, int(data.IsHoliday), data.Size,
            data.Temperature, data.CPI, data.Unemployment,
            year, month, week, type_encoded
        ]
        
        # Scale
        input_scaled = scaler.transform([input_data])
        
        prediction = model.predict(input_scaled)[0]
        return {"prediction": float(prediction)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
