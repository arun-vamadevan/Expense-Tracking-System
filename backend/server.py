from fastapi import FastAPI, HTTPException
from datetime import date

import db_helper
from pydantic import BaseModel
from typing import List

class Expense(BaseModel):
    #expense_date: date
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

app = FastAPI()

@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    result = db_helper.fetch_expense_for_date(expense_date)
    if len(result) == 0:
        return "No records found, Try with another date."
    return result

@app.post("/expenses/{expense_date}")
def add_or_update_expenses(expense_date: date, expenses: List[Expense]):
    db_helper.delete_expense_for_date(expense_date)
    for exp in expenses:
        db_helper.insert_expense(expense_date, exp.amount, exp.category, exp.notes)
    return {"message": "Expenses updated successfully"}

@app.post("/analytics/")
def get_analytics_data(date_range: DateRange):
    optimised_data = {}
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from database")

    grand_total = sum(item['total'] for item in data)

    for item in data:
        percentage = (item['total']/grand_total) * 100 if grand_total !=0 else 0
        optimised_data[item['category']] = {
                "total": item['total'], "percentage": percentage
        }

    # "Rent":{"total": 123, "percetage": 45},
    #"Shopping": {"total": 123, "percetage": 45}
    return optimised_data

@app.get("/analytics/month")
def get_analytics_data_by_month():
    data = db_helper.fetch_expense_summary_by_month()
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from database")
    return data
