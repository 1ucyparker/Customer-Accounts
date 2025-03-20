from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# API Key and Google Sheet ID
API_KEY = "AIzaSyDOs-Wl2bTLvL5jyipmsh1yZgnLTJUlXdE"
SHEET_ID = "1Bx6CjndHFmR-i6Z7cuoA83BjqX4wTG1r_cGTblddzdc"
SHEET_NAME = "Sheet1"

def fetch_google_sheets_data():
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{SHEET_NAME}?key={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        values = data.get("values", [])
        if not values or len(values) < 2:
            raise HTTPException(status_code=500, detail="No data found in sheet")

        headers = values[0]  # First row as headers
        items = [dict(zip(headers, row)) for row in values[1:]]  # Convert rows to JSON

        return items

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/accounts")
def get_accounts():
    accounts = fetch_google_sheets_data()

    # Transform data into desired format
    formatted_accounts = [
        {
            "account_name": item.get("ACCOUNT NAME", ""),  # Adjust based on actual column name
            "customer_rid": int(item.get("CUSTOMER ID", "0"))  # Convert to int
        }
        for item in accounts
    ]

    return {"data": formatted_accounts}

# Run the API using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
