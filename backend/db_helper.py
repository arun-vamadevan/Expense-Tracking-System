import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit = False):
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password ="root",
        database = "expense_manager"
    )

    if connection.is_connected():
        print('Connection Successful!')
    else:
        print('Connection failed')

    cursor = connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()
    print("both closed, Great!!!")

def fetch_all_records():
    connection, cursor = get_db_cursor()
    cursor.execute("SELECT * FROM expenses")
    exp = cursor.fetchall()
    for item in exp:
        print(item)

    cursor.close()
    connection.close()

def fetch_expense_for_date(expense_date):
    logger.info(f"fetch_expense_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        exp = cursor.fetchall()
        return exp

def insert_expense(expense_date, amount, category, notes):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )

def delete_expense_for_date(expense_date):
    logger.info(f"delete_expense_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "DELETE FROM expenses WHERE expense_date= %s",[expense_date]
        )

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start-date: {start_date} and end-date: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT category, sum(amount) as total "
            "FROM expenses WHERE expense_date "
            "BETWEEN %s and %s "
            "GROUP BY category",
            [start_date, end_date]
        )
        data = cursor.fetchall()
        return data

def fetch_expense_summary_by_month():
    logger.info(f"fetch_expense_summary by month called")
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT MONTH(expense_date) AS month, "
            "SUM(amount) AS total_amount "
            "FROM expenses "
            "GROUP BY MONTH(expense_date) "
            "ORDER BY MONTH(expense_date)"
        )
        data = cursor.fetchall()
        return data


if __name__ == "__main__":
    expenses = fetch_expense_for_date("2024-08-01")
    # for item in expenses:
    #     print(item)
    #insert_expense("2025-08-01","300", "Food","bulk shopping")
    #delete_expense_for_date("2025-08-01")
    summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    print(summary)