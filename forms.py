from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields import TimeField
from wtforms.validators import DataRequired
from app import db
import datetime


class CrontabForm(FlaskForm):
    # Create all TimeField variables
    sunday_start_time = TimeField("Sunday Start Time", format="%H:%M")
    sunday_switch_time = TimeField("Sunday Switch Time", format="%H:%M")
    sunday_end_time = TimeField("Sunday End Time", format="%H:%M")

    monday_start_time = TimeField("Monday Start Time", format="%H:%M")
    monday_switch_time = TimeField("Monday Switch Time", format="%H:%M")
    monday_end_time = TimeField("Monday End Time", format="%H:%M")

    tuesday_start_time = TimeField("Tuesday Start Time", format="%H:%M")
    tuesday_switch_time = TimeField("Tuesday Switch Time", format="%H:%M")
    tuesday_end_time = TimeField("Tuesday End Time", format="%H:%M")

    wednesday_start_time = TimeField("Wednesday Start Time", format="%H:%M")
    wednesday_switch_time = TimeField("Wednesday Switch Time", format="%H:%M")
    wednesday_end_time = TimeField("Wednesday End Time", format="%H:%M")

    thursday_start_time = TimeField("Thursday Start Time", format="%H:%M")
    thursday_switch_time = TimeField("Thursday Switch Time", format="%H:%M")
    thursday_end_time = TimeField("Thursday End Time", format="%H:%M")

    friday_start_time = TimeField("Friday Start Time", format="%H:%M")
    friday_switch_time = TimeField("Friday Switch Time", format="%H:%M")
    friday_end_time = TimeField("Friday End Time", format="%H:%M")

    saturday_start_time = TimeField("Saturday Start Time", format="%H:%M")
    saturday_switch_time = TimeField("Saturday Switch Time", format="%H:%M")
    saturday_end_time = TimeField("Saturday End Time", format="%H:%M")

    # Create link text fields
    sunday_start_text = StringField("Sunday Start Text")
    sunday_switch_text = StringField("Sunday Switch Text")

    monday_start_text = StringField("Monday Start Text")
    monday_switch_text = StringField("Monday Switch Text")

    tuesday_start_text = StringField("Tuesday Start Text")
    tuesday_switch_text = StringField("Tuesday Switch Text")

    wednesday_start_text = StringField("Wednesday Start Text")
    wednesday_switch_text = StringField("Wednesday Switch Text")

    thursday_start_text = StringField("Thursday Start Text")
    thursday_switch_text = StringField("Thursday Switch Text")

    friday_start_text = StringField("Friday Start Text")
    friday_switch_text = StringField("Friday Switch Text")

    saturday_start_text = StringField("Saturday Start Text")
    saturday_switch_text = StringField("Saturday Switch Text")

    # Create cancel submit field
    cancel = SubmitField("Cancel")

    # Create update submit field
    submit = SubmitField("Update")


def update_crontab_form_defaults(form, list):
    def set_time_default(form, time):
        if type(time) is str:
            form.default = datetime.datetime.strptime(time, "%H:%M").time()
        else:
            form.default = time

    set_time_default(form.sunday_start_time, list[0][0])
    set_time_default(form.sunday_switch_time, list[0][1])
    set_time_default(form.sunday_end_time, list[0][2])
    form.sunday_start_text.default = list[0][3]
    form.sunday_switch_text.default = list[0][4]

    set_time_default(form.monday_start_time, list[1][0])
    set_time_default(form.monday_switch_time, list[1][1])
    set_time_default(form.monday_end_time, list[1][2])
    form.monday_start_text.default = list[1][3]
    form.monday_switch_text.default = list[1][4]

    set_time_default(form.tuesday_start_time, list[2][0])
    set_time_default(form.tuesday_switch_time, list[2][1])
    set_time_default(form.tuesday_end_time, list[2][2])
    form.tuesday_start_text.default = list[2][3]
    form.tuesday_switch_text.default = list[2][4]

    set_time_default(form.wednesday_start_time, list[3][0])
    set_time_default(form.wednesday_switch_time, list[3][1])
    set_time_default(form.wednesday_end_time, list[3][2])
    form.wednesday_start_text.default = list[3][3]
    form.wednesday_switch_text.default = list[3][4]

    set_time_default(form.thursday_start_time, list[4][0])
    set_time_default(form.thursday_switch_time, list[4][1])
    set_time_default(form.thursday_end_time, list[4][2])
    form.thursday_start_text.default = list[4][3]
    form.thursday_switch_text.default = list[4][4]

    set_time_default(form.friday_start_time, list[5][0])
    set_time_default(form.friday_switch_time, list[5][1])
    set_time_default(form.friday_end_time, list[5][2])
    form.friday_start_text.default = list[5][3]
    form.friday_switch_text.default = list[5][4]

    set_time_default(form.saturday_start_time, list[6][0])
    set_time_default(form.saturday_switch_time, list[6][1])
    set_time_default(form.saturday_end_time, list[6][2])
    form.saturday_start_text.default = list[6][3]
    form.saturday_switch_text.default = list[6][4]

    form.process()


def return_list_of_entries_as_lists(db_list):
    def return_list_of_values_from_entry(entry):
        value_list = []  # create empty list to append entry data to
        value_list.append(entry.start_time)
        value_list.append(entry.switch_time)
        value_list.append(entry.end_time)
        value_list.append(entry.start_link_text)
        value_list.append(entry.switch_link_text)
        value_list.append(entry.id)
        return value_list

    returned_list = []

    for (
        entry
    ) in db_list:  # convert database entries into lists for updating default values
        returned_list.append(return_list_of_values_from_entry(entry))

    return returned_list


def return_form_data_as_list_of_dict(form):
    def check_is_not_none(form_entry):
        if form_entry is None:
            return False
        else:
            return True

    def set_entry_time(form_entry, dictionary, key):
        if check_is_not_none(form_entry):
            dictionary[key] = form_entry.strftime("%H:%M")
        else:
            dictionary[key] = form_entry

    sunday_entry = {
        "id": 1,
        "day_of_the_week": "Sunday",
        "start_link_text": form.sunday_start_text.data,
        "switch_link_text": form.sunday_switch_text.data,
    }

    set_entry_time(form.sunday_start_time.data, sunday_entry, "start_time")
    set_entry_time(form.sunday_switch_time.data, sunday_entry, "switch_time")
    set_entry_time(form.sunday_end_time.data, sunday_entry, "end_time")

    monday_entry = {
        "id": 2,
        "day_of_the_week": "Monday",
        "start_link_text": form.monday_start_text.data,
        "switch_link_text": form.monday_switch_text.data,
    }

    set_entry_time(form.monday_start_time.data, monday_entry, "start_time")
    set_entry_time(form.monday_switch_time.data, monday_entry, "switch_time")
    set_entry_time(form.monday_end_time.data, monday_entry, "end_time")

    tuesday_entry = {
        "id": 3,
        "day_of_the_week": "Tuesday",
        "start_link_text": form.tuesday_start_text.data,
        "switch_link_text": form.tuesday_switch_text.data,
    }

    set_entry_time(form.tuesday_start_time.data, tuesday_entry, "start_time")
    set_entry_time(form.tuesday_switch_time.data, tuesday_entry, "switch_time")
    set_entry_time(form.tuesday_end_time.data, tuesday_entry, "end_time")

    wednesday_entry = {
        "id": 4,
        "day_of_the_week": "Wednesday",
        "start_link_text": form.wednesday_start_text.data,
        "switch_link_text": form.wednesday_switch_text.data,
    }

    set_entry_time(form.wednesday_start_time.data, wednesday_entry, "start_time")
    set_entry_time(form.wednesday_switch_time.data, wednesday_entry, "switch_time")
    set_entry_time(form.wednesday_end_time.data, wednesday_entry, "end_time")

    thursday_entry = {
        "id": 5,
        "day_of_the_week": "Thursday",
        "start_link_text": form.thursday_start_text.data,
        "switch_link_text": form.thursday_switch_text.data,
    }

    set_entry_time(form.thursday_start_time.data, thursday_entry, "start_time")
    set_entry_time(form.thursday_switch_time.data, thursday_entry, "switch_time")
    set_entry_time(form.thursday_end_time.data, thursday_entry, "end_time")

    friday_entry = {
        "id": 6,
        "day_of_the_week": "Friday",
        "start_link_text": form.friday_start_text.data,
        "switch_link_text": form.friday_switch_text.data,
    }

    set_entry_time(form.friday_start_time.data, friday_entry, "start_time")
    set_entry_time(form.friday_switch_time.data, friday_entry, "switch_time")
    set_entry_time(form.friday_end_time.data, friday_entry, "end_time")

    saturday_entry = {
        "id": 7,
        "day_of_the_week": "Saturday",
        "start_link_text": form.saturday_start_text.data,
        "switch_link_text": form.saturday_switch_text.data,
    }

    set_entry_time(form.saturday_start_time.data, saturday_entry, "start_time")
    set_entry_time(form.saturday_switch_time.data, saturday_entry, "switch_time")
    set_entry_time(form.saturday_end_time.data, saturday_entry, "end_time")

    entry_list = [
        sunday_entry,
        monday_entry,
        tuesday_entry,
        wednesday_entry,
        thursday_entry,
        friday_entry,
        saturday_entry,
    ]
    return entry_list


def update_display_entry(db_list, entry, id):
    for item in db_list:
        if item.id == id:
            item.start_time = entry["start_time"]  # update start time
            item.switch_time = entry["switch_time"]  # update switch time
            item.end_time = entry["end_time"]  # update end time
            item.start_link_text = entry["start_link_text"]  # update start link text
            item.switch_link_text = entry["switch_link_text"]  # update switch link text


class HardwareControlForm(FlaskForm):
    shutdown_pi_button = SubmitField("Shutdown Pi")
    reboot_pi_button = SubmitField("Reboot Pi")
    power_display_button = SubmitField("Power Display")
    shutdown_display_button = SubmitField("Shutdown Display")


class LoginForm(FlaskForm):
    user = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
