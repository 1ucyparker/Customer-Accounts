from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# API Key and Google Sheet ID (Replace these with your new values)
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

        return items  # Wrap in a single list

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/accounts")
def get_accounts():
    return fetch_google_sheets_data()

# Run the API using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)