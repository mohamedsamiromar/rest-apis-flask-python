from flask import Flask
from flask import jsonify

app = Flask(__name__)

data = {
    "count": 3,
    "next": "null",
    "previous": "null",
    "results": [
        {
            "id": 18,
            "date": "2022/03/16",
            "day": "Wednesday",
            "corporate_name": "Mohamed Samir",
            "city": "Medinah",
            "store": "Headquarter",
            "munjiz": {
                "full_name": "Mohamed Omar Samir",
                "mobile_number": "0501006444",
                "nationality": "Saudi Arabia",
                "bank_name": "null",
                "iban": "null"
            },
            "actual_hours": 10,
            "js_hrs_price": 25,
            "munjiz_commission": 5,
            "total_js_salary": 250,
            "total_munjiz_commission": 50,
            "amount": 300,
            "paid": "True"
        },
        {
            "id": 19,
            "date": "2022/03/16",
            "day": "Wednesday",
            "corporate_name": "Mohamed Samir",
            "city": "Medinah",
            "store": "Headquarter",
            "munjiz": {
                "full_name": "Mohamed Omar Samir",
                "mobile_number": "0501006444",
                "nationality": "Saudi Arabia",
                "bank_name": "null",
                "iban": "null"
            },
            "actual_hours": 10,
            "js_hrs_price": 25,
            "munjiz_commission": 5,
            "total_js_salary": 250,
            "total_munjiz_commission": 50,
            "amount": 300,
            "paid": "True"
        },
        {
            "id": 17,
            "date": "2022/04/30",
            "day": "Saturday",
            "corporate_name": "Mohamed Samir",
            "city": "Medinah",
            "store": "Headquarter",
            "munjiz": {
                "full_name": "Ali Mohamed Ali",
                "mobile_number": "0508741036",
                "nationality": "Egypt",
                "bank_name": "null",
                "iban": "null"
            },
            "actual_hours": 10,
            "js_hrs_price": 25,
            "munjiz_commission": 5,
            "total_js_salary": 250,
            "total_munjiz_commission": 50,
            "amount": 300,
            "paid": "True"
        }
    ]
}

@app.get("/store")
def get_store():
    return {"store": data}

if __name__ == '__main__':
    app.run()
