from flask_login import current_user
from flask import flash
from .. import db
from ..models import Expense, Income, Itag, Etag, Saving, User
import json
from datetime import datetime
from sqlalchemy import func


def calculate_expenses(start_date_raw, end_date_raw):
    expenses_data = {"Expenses": "Lei"}
    total = 0
    query = db.session.query(
        Etag.data,
        func.sum(Expense.value).label('total_value')
    ).join(Expense).filter(Expense.user_id == current_user.id)

    if start_date_raw and end_date_raw:
        try:
            start_date = datetime.strptime(start_date_raw, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_raw, "%Y-%m-%d")
            query = query.filter(Expense.date >= start_date.date(), Expense.date <= end_date.date())
        except ValueError:
            pass  # Invalid dates, use all

    query = query.group_by(Etag.id).all()

    for tag_data, sum_value in query:
        expenses_data[tag_data] = sum_value
        total += sum_value

    # Sort by value descending
    expenses_data_sorted = sorted(
        [(k, v) for k, v in expenses_data.items() if k != "Expenses"],
        key=lambda x: x[1], reverse=True
    )
    expenses_data = {"Expenses": "Lei"}
    for tag, value in expenses_data_sorted:
        expenses_data[tag] = value

    return [expenses_data, total]


def calculate_incomes(start_date_raw, end_date_raw):
    incomes_data = {"Incomes": "Lei"}
    total = 0
    query = db.session.query(
        Itag.data,
        func.sum(Income.value).label('total_value')
    ).join(Income).filter(Income.user_id == current_user.id)

    if start_date_raw and end_date_raw:
        try:
            start_date = datetime.strptime(start_date_raw, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_raw, "%Y-%m-%d")
            query = query.filter(Income.date >= start_date.date(), Income.date <= end_date.date())
        except ValueError:
            pass

    query = query.group_by(Itag.id).all()

    for tag_data, sum_value in query:
        incomes_data[tag_data] = sum_value
        total += sum_value

    incomes_data_sorted = sorted(
        [(k, v) for k, v in incomes_data.items() if k != "Incomes"],
        key=lambda x: x[1], reverse=True
    )
    incomes_data = {"Incomes": "Lei"}
    for tag, value in incomes_data_sorted:
        incomes_data[tag] = value

    return [incomes_data, total]


def calculate_savings(goal_string):
    savings_data = {"Savings progress": "Lei"}
    total_savings = db.session.query(func.sum(Saving.value)).filter(Saving.user_id == current_user.id).scalar() or 0

    if goal_string:
        try:
            goal = float(goal_string)
            user = User.query.get(current_user.id)
            user.savings_goal = goal
            db.session.commit()
        except ValueError:
            flash("Please enter a valid number as goal!", category="error")
            goal = current_user.savings_goal or 0
    else:
        goal = current_user.savings_goal or 0

    savings_data["Savings"] = total_savings
    if goal > 0:
        savings_data["Still needing"] = max(0, goal - total_savings)
    return savings_data