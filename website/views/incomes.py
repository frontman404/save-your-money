from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Income, Itag
import json
from datetime import datetime

incomes_bp = Blueprint("incomes", __name__)


@incomes_bp.route("/incomes", methods=["GET", "POST"])
@login_required
def incomes():
    if request.method == "POST":
        value_string = request.form.get("value")
        try:
            value = float(value_string)
        except:
            flash("Please enter a positive valid number as value", category="error")
            return render_template("incomes.html", user=current_user)
        tag = request.form.get("tag")
        for itag in current_user.itags:
            if itag.data == tag:
                tag_id = itag.id
        date = request.form.get("date")
        date = datetime.strptime(date, "%Y-%m-%d")

        if value <= 0:
            flash("Please enter a positive valid number as value", category="error")
        else:
            new_income = Income(
                value=value, tag_id=tag_id, date=date, user_id=current_user.id
            )
            db.session.add(new_income)
            db.session.commit()
            flash("An income entry has been added!", category="success")
    return render_template("incomes.html", user=current_user)


@incomes_bp.route("/delete-income", methods=["POST"])
def delete_income():
    income = json.loads(request.data)
    incomeId = income["incomeId"]
    income = Income.query.get(incomeId)
    if income:
        if income.user_id == current_user.id:
            db.session.delete(income)
            db.session.commit()
            flash("An income entry has been removed!", category="success")
    return jsonify({})