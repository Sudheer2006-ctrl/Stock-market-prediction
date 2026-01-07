from flask import Flask, render_template, request
from model import analyze_company

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/compare", methods=["POST"])
def compare():
    try:
        company1 = request.form["company1"]
        company2 = request.form["company2"]
        amount = float(request.form["amount"])

        if company1 == company2:
            raise Exception("Please select two different companies")

        if amount < 1000:
            raise Exception("Investment amount must be at least ₹1000")

        c1 = analyze_company(company1)
        c2 = analyze_company(company2)

        # Shares calculation
        shares1 = int(amount // c1["current"])
        shares2 = int(amount // c2["current"])

        # Future value using predicted price
        future1 = round(shares1 * c1["predicted"], 2)
        future2 = round(shares2 * c2["predicted"], 2)

        # 🧠 BEST STOCK DECISION LOGIC (CUSTOMER-CENTRIC)
        if c1["signal"] == "BUY" and c2["signal"] == "SELL":
            better = c1["company"]

        elif c2["signal"] == "BUY" and c1["signal"] == "SELL":
            better = c2["company"]

        elif c1["signal"] == "SELL" and c2["signal"] == "SELL":
            # When both are SELL → choose LOW risk
            risk_rank = {"Low": 1, "Medium": 2, "High": 3}
            better = (
                c1["company"]
                if risk_rank[c1["risk"]] < risk_rank[c2["risk"]]
                else c2["company"]
            )

        else:
            # Both BUY → choose better risk-adjusted score
            better = c1["company"] if c1["score"] > c2["score"] else c2["company"]

        return render_template(
            "result.html",
            c1=c1,
            c2=c2,
            amount=amount,
            shares1=shares1,
            shares2=shares2,
            future1=future1,
            future2=future2,
            better=better
        )

    except Exception as e:
        return f"<h3>Error: {e}</h3>"

if __name__ == "__main__":
    app.run(debug=True)
