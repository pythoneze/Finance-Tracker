import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ['Date', 'Amount', 'Category', 'Description']
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
    
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            'Date': date,
            'Amount': amount,
            'Category': category,
            'Description': description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames= cls.COLUMNS)

            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow(new_entry)
        print("Entry added succesfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['Date'] = pd.to_datetime(df['Date'], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["Date"] >= start_date) & (df['Date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print(
                    f"\nNo transactions found between {start_date.strftime(CSV.FORMAT)} and {end_date.strftime(CSV.FORMAT)}"
                )
        else:
            print(
                    f"\nTransactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
                )
            print(
                filtered_df.to_string(
                    index=False, formatters={"Date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df["Category"] == "Income"]["Amount"].sum()
            total_expense = filtered_df[filtered_df["Category"] == "Expense"]["Amount"].sum()
            print("\nSumary")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${total_income - total_expense:.2f}")

        return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date("\nEnter the date of the transaction (dd-mm-yyyy) or press enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transaction(df):
    df.set_index("Date", inplace=True)

    income_df = (
        df[df["Category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["Category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["Amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["Amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.xlabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\nFinance Tracker Menu")
        print("1. Add a transaction")
        print("2. Get transactions between dates")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("\nEnter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)

            if df is not None and not df.empty:
                if input("Do you want to see a plot? (y/n) ").lower() == "y":
                    plot_transaction(df)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
