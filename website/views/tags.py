from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Etag, Itag, Expense, Income, User
import json

tags_bp = Blueprint("tags", __name__)


@tags_bp.route("/etags", methods=["GET", "POST"])
@login_required
def etags():
    if request.method == "POST":
        data = request.form.get("data")
        if len(data) < 1:
            flash("Please enter a tag name!", category="error")
        else:
            unique_tag = True
            for etag in current_user.etags:
                if etag.data == data:
                    flash("Tag name already exists!", category="error")
                    unique_tag = False
        if unique_tag:
            new_etag = Etag(data=data, user_id=current_user.id)
            db.session.add(new_etag)
            db.session.commit()
            flash("A tag has been added!", category="success")
    return render_template("etags.html", user=current_user)


@tags_bp.route("/delete-etag", methods=["POST"])
def delete_etag():
    etag = json.loads(request.data)
    etagId = etag["etagId"]
    etag = Etag.query.get(etagId)
    user = User.query.get(current_user.id)
    if etag:
        if etag.user_id == current_user.id:
            for expense in user.expenses:
                if expense.tag_id == etag.id:
                    db.session.delete(expense)
            db.session.delete(etag)
            db.session.commit()
            flash(
                "The tag and all expenses associated have been removed!",
                category="success",
            )
    return jsonify({})


@tags_bp.route("/itags", methods=["GET", "POST"])
@login_required
def itags():
    if request.method == "POST":
        data = request.form.get("data")
        if len(data) < 1:
            flash("Please enter a tag name!", category="error")
        else:
            unique_tag = True
            for itag in current_user.itags:
                if itag.data == data:
                    flash("Tag name already exists!", category="error")
                    unique_tag = False
        if unique_tag:
            new_itag = Itag(data=data, user_id=current_user.id)
            db.session.add(new_itag)
            db.session.commit()
            flash("A tag has been added!", category="success")
    return render_template("itags.html", user=current_user)


@tags_bp.route("/delete-itag", methods=["POST"])
def delete_itag():
    itag = json.loads(request.data)
    itagId = itag["itagId"]
    itag = Itag.query.get(itagId)
    user = User.query.get(current_user.id)
    if itag:
        if itag.user_id == current_user.id:
            for income in user.incomes:
                if income.tag_id == itag.id:
                    db.session.delete(income)
            db.session.delete(itag)
            db.session.commit()
            flash(
                "The tag and all incomes associated have been removed!",
                category="success",
            )
    return jsonify({})