from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Note
from .utils import calculate_expenses, calculate_incomes, calculate_savings
import json

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
    tabs = [True, False, False]

    note = request.form.get("note")
    goal_string = request.form.get("goal")

    if request.method == "POST":
        if request.form.get("filter_button") == "1":
            pass
        elif request.form.get("filter_button") == "2":
            tabs = [False, True, False]
        elif request.form.get("filter_button") == "3":
            tabs = [False, False, True]
    if tabs[0] == True:
        start_date_raw = request.form.get("start_date_expenses")
        end_date_raw = request.form.get("end_date_expenses")
    elif tabs[1] == True:
        start_date_raw = request.form.get("start_date_incomes")
        end_date_raw = request.form.get("end_date_incomes")
    elif tabs[2] == True:
        start_date_raw = request.form.get("start_date_incomes")
        end_date_raw = request.form.get("end_date_incomes")

    [incomes_data, incomes_data_total] = calculate_incomes(start_date_raw, end_date_raw)
    [expenses_data, expenses_data_total] = calculate_expenses(
        start_date_raw, end_date_raw
    )
    savings_data = calculate_savings(goal_string)

    if note:
        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash("A note has been added!", category="success")

    return render_template(
        "dashboard.html",
        user=current_user,
        tabs=tabs,
        start_date=start_date_raw,
        end_date=end_date_raw,
        goal=goal_string,
        expenses_data=expenses_data,
        incomes_data=incomes_data,
        expenses_data_total=expenses_data_total,
        incomes_data_total=incomes_data_total,
        savings_data=savings_data,
    )


@dashboard_bp.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("A note has been removed!", category="success")
    return jsonify({})