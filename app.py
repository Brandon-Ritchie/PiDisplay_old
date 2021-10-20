"""
Imports
"""

from logging import error
from flask import Flask, flash, render_template, request, redirect
from flask.helpers import url_for
from flask_login import LoginManager, login_required, login_user, current_user
from flask_sqlalchemy import SQLAlchemy  # for database manipulation

app = Flask(__name__)  # application instance
app.config[
    "SECRET_KEY"
] = "Un295VTH7BFLp6U4eVS6ZXGA"  # secret key that I don't think I implimented
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///display.db"  # path to database and database name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # to turn off alerts
db = SQLAlchemy(app)  # database instance
app_login_manager = LoginManager(app)
app_login_manager.init_app(app)

import models
import forms
import utilities  # for updating crotab

"""
Routes
"""


@app_login_manager.user_loader
def load_user(id):
    return db.session.query(models.User).get(int(id))


@app_login_manager.unauthorized_handler
def unauthorized():
    return "Sorry, you must be logged in to view this page."


@app.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    login_form = forms.LoginForm()
    if request.method == "POST":
        user = (
            db.session.query(models.User)
            .filter_by(username=login_form.user.data)
            .first()
        )
        if user:
            if user.check_password(login_form.password.data):
                login_user(user)
                return redirect(url_for("home"))
        else:
            flash(
                "Either the username or password was incorrect.\n Please try again.",
                "error",
            )
    return render_template("index.html", template_form=login_form)


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    crontab_form = forms.CrontabForm()  # crontab form instance

    hardware_form = forms.HardwareControlForm()

    try:
        if hardware_form.shutdown_pi_button.data:
            utilities.shutdown_pi()

        if hardware_form.reboot_pi_button.data:
            utilities.reboot_pi()

        if hardware_form.power_display_button.data:
            utilities.power_display()

        if hardware_form.shutdown_display_button.data:
            utilities.shutdown_display()

        if "sunday_start_time" in request.form:
            if crontab_form.submit.data:
                entry_list = forms.return_form_data_as_list_of_dict(
                    crontab_form
                )  # created as dictionaries of the form data making it easier to deal with
                display_entry_model = (
                    db.session.query(models.DisplayEntry)
                    .order_by(models.DisplayEntry.id)
                    .all()
                )
                try:
                    i = 1
                    for entry in entry_list:
                        forms.update_display_entry(
                            display_entry_model, entry, i
                        )  # update each entry in the DisplayEntry table with the entries from created dictionaries
                        i += 1
                    db.session.commit()
                    utilities.update_crontab(display_entry_model)
                    flash("The display has been updated.")
                except Exception as e:
                    db.session.rollback()
                    flash("There was an error")
                    flash(e)
                    print(e)

            if crontab_form.cancel.data:
                db.session.rollback()

    except Exception as e:
        flash("There was an error: ")
        flash(e)
        print(e)

    display_entry_list = (
        db.session.query(models.DisplayEntry).order_by(models.DisplayEntry.id).all()
    )
    display_entry_list_as_lists = forms.return_list_of_entries_as_lists(
        display_entry_list
    )
    forms.update_crontab_form_defaults(crontab_form, display_entry_list_as_lists)

    return render_template(
        "home.html",
        template_crontab_form=crontab_form,
        template_hardware_form=hardware_form,
    )


"""
Deployment
"""

if __name__ == "__main__":
    app.run(port=80, host="0.0.0.0")
