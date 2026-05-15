from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Expense, Etag
import json
from datetime import datetime

expenses_bp = Blueprint("expenses", __name__)


@expenses_bp.route("/expenses", methods=["GET", "POST"])
@login_required
def expenses():
    if request.method == "POST":
        value_string = request.form.get("value")
        try:
            value = float(value_string)
        except:
            flash("Please enter a positive valid number as value!", category="error")
            return render_template("expenses.html", user=current_user)
        tag = request.form.get("tag")
        for etag in current_user.etags:
            if etag.data == tag:
                tag_id = etag.id
        date = request.form.get("date")
        date = datetime.strptime(date, "%Y-%m-%d")

        if value <= 0:
            flash("Please enter a positive valid number as value!", category="error")
        else:
            new_expense = Expense(
                value=value, tag_id=tag_id, date=date, user_id=current_user.id
            )
            db.session.add(new_expense)
            db.session.commit()
            flash("An expense entry has been added!", category="success")
    return render_template("expenses.html", user=current_user)


@expenses_bp.route("/delete-expense", methods=["POST"])
def delete_expense():
    expense = json.loads(request.data)
    expenseId = expense["expenseId"]
    expense = Expense.query.get(expenseId)
    if expense:
        if expense.user_id == current_user.id:
            db.session.delete(expense)
            db.session.commit()
            flash("An expense entry has been removed!", category="success")
    return jsonify({})