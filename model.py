import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Load dataset
data = pd.read_csv("dataset.csv")

# Cache models (performance improvement)
MODEL_CACHE = {}

def calculate_risk(df):
    """
    Risk based on volatility of daily percentage returns
    """
    returns = df["Close"].pct_change().dropna()
    volatility = returns.std() * 100

    if volatility < 1.0:
        return "Low", 1
    elif volatility < 2.5:
        return "Medium", 2
    else:
        return "High", 3

def get_model(company, X, y):
    if company not in MODEL_CACHE:
        model = RandomForestRegressor(
            n_estimators=150,
            random_state=42
        )
        model.fit(X, y)
        MODEL_CACHE[company] = model
    return MODEL_CACHE[company]

def analyze_company(company):
    company = company.upper()
    df = data[data["Company"] == company]

    if df.empty:
        raise Exception("Company not found in dataset")

    X = df[["Open", "High", "Low", "Volume"]]
    y = df["Close"]

    model = get_model(company, X, y)

    latest_features = X.iloc[-1].values.reshape(1, -1)
    predicted_price = model.predict(latest_features)[0]
    current_price = y.iloc[-1]

    change_pct = ((predicted_price - current_price) / current_price) * 100
    signal = "BUY" if change_pct > 1 else "SELL"

    risk_label, risk_score = calculate_risk(df)

    # Risk-adjusted investment score
    investment_score = round(change_pct / risk_score, 2)

    return {
        "company": company,
        "current": round(current_price, 2),
        "predicted": round(predicted_price, 2),
        "change_pct": round(change_pct, 2),
        "signal": signal,
        "risk": risk_label,
        "score": investment_score
    }
