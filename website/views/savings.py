from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Saving
import json
from datetime import datetime

savings_bp = Blueprint("savings", __name__)


@savings_bp.route("/savings", methods=["GET", "POST"])
@login_required
def savings():
    if request.method == "POST":
        value_string = request.form.get("value")
        try:
            value = float(value_string)
        except:
            flash("Please enter a valid number as value", category="error")
            return render_template("savings.html", user=current_user)
        date = request.form.get("date")
        date = datetime.strptime(date, "%Y-%m-%d")
        if value == 0:
            flash("Please enter a valid number as value", category="error")
        else:
            new_saving = Saving(value=value, date=date, user_id=current_user.id)
            db.session.add(new_saving)
            db.session.commit()
            flash("A saving entry has been added!", category="success")
    return render_template("savings.html", user=current_user)


@savings_bp.route("/delete-saving", methods=["POST"])
def delete_saving():
    saving = json.loads(request.data)
    savingId = saving["savingId"]
    saving = Saving.query.get(savingId)
    if saving:
        if saving.user_id == current_user.id:
            db.session.delete(saving)
            db.session.commit()
            flash("A saving entry has been removed!", category="success")
    return jsonify({})