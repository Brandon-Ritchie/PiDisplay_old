from crontab import CronTab
import forms
import datetime
import os


def convert_time_to_list(time):
    if time is None:
        return ["", ""]
    elif time == "":
        return ["", ""]
    else:
        time_split = time.split(":")
        time_list = [time_split[0], time_split[1]]
        return time_list


def update_crontab(database):
    some_list = forms.return_list_of_entries_as_lists(database)

    cron = CronTab(user="pi")  # access crontab for user pi
    cron.remove_all()  # remove all previous cron jobs

    # Create command variables
    on_command = "echo 'on 0.0.0.0' | cec-client -s -d 1 && echo \"state = 'on'\" > /home/pi/Scripts/PiDisplay/state.py && DISPLAY=:0 python3 /home/pi/Scripts/PiDisplay/main.py >> /home/pi/Scripts/PiDisplay/pi_display.log 2>&1"
    switch_command_1 = "echo 'standby 0.0.0.0' | cec-client -s -d 1 && echo \"state = 'switch'\" > /home/pi/Scripts/PiDisplay/state.py && DISPLAY=:0 python3 /home/pi/Scripts/PiDisplay/main.py >> /home/pi/Scripts/PiDisplay/pi_display.log 2>&1"
    switch_command_2 = "echo 'on 0.0.0.0' | cec-client -s -d 1"
    off_command = "echo 'standby 0.0.0.0' | cec-client -s -d 1 && pkill chromium"

    # Create Jobs and Times
    def add_cron_job(list):

        # Set day or the week int and insert human readable comment in crontab
        day_of_the_week_int = 0
        if list[5] == 1:
            comment = cron.new(command=" Sunday * * * * *")
            comment.enable(False)
            day_of_the_week_int = 0
        elif list[5] == 2:
            comment = cron.new(command=" Monday * * * * *")
            comment.enable(False)
            day_of_the_week_int = 1
        elif list[5] == 3:
            comment = cron.new(command=" Tuesday * * * * *")
            comment.enable(False)
            day_of_the_week_int = 2
        elif list[5] == 4:
            comment = cron.new(command=" Wednesday * * * * *")
            comment.enable(False)
            day_of_the_week_int = 3
        elif list[5] == 5:
            comment = cron.new(command=" Thursday * * * * *")
            comment.enable(False)
            day_of_the_week_int = 4
        elif list[5] == 6:
            comment = cron.new(command=" Friday * * * * *")
            comment.enable(False)
            day_of_the_week_int = 5
        elif list[5] == 7:
            comment = cron.new(command=" Saturday * * * * *")
            comment.enable(False)
            day_of_the_week_int = 6

        # Outputting 'on' cron job
        if list[0] is not None and list[0] != ["", ""]:
            time_as_list = convert_time_to_list(list[0])
            new_cron_job = cron.new(command=on_command)
            new_cron_job.dow.on(day_of_the_week_int)
            new_cron_job.hour.on(time_as_list[0])
            new_cron_job.minute.on(time_as_list[1])

        # Outputting 'switch' cron job
        if list[1] is not None and list[1] != ["", ""]:
            time_as_list = convert_time_to_list(list[1])
            new_cron_job_1 = cron.new(command=switch_command_1)
            new_cron_job_1.dow.on(day_of_the_week_int)
            new_cron_job_1.hour.on(time_as_list[0])
            new_cron_job_1.minute.on(time_as_list[1])

            new_cron_job_2 = cron.new(command=switch_command_2)
            new_cron_job_2.dow.on(day_of_the_week_int)
            new_cron_job_2.hour.on(time_as_list[0])
            new_cron_job_2.minute.on(int(time_as_list[1]) + 1)

        # Oututting 'off' cron job
        if list[2] is not None and list[2] != ["", ""]:
            time_as_list = convert_time_to_list(list[2])
            new_cron_job = cron.new(command=off_command)
            new_cron_job.dow.on(day_of_the_week_int)
            new_cron_job.hour.on(time_as_list[0])
            new_cron_job.minute.on(time_as_list[1])

    for list in some_list:
        add_cron_job(list)

    # Write cron jobs to file
    cron.write()


def print_with_time(string):
    now = datetime.datetime.now()
    print(now.strftime("[%m-%d-%y: %H:%M:%S] " + string))


def assign_display_text(state, db_list):
    day_of_the_week = datetime.datetime.today().weekday()
    some_list = some_list = forms.return_list_of_entries_as_lists(db_list)

    display_text = ""
    if state == "on":
        if day_of_the_week == 0:
            display_text = some_list[1][3]
        elif day_of_the_week == 1:
            display_text = some_list[2][3]
        elif day_of_the_week == 2:
            display_text = some_list[3][3]
        elif day_of_the_week == 3:
            display_text = some_list[4][3]
        elif day_of_the_week == 4:
            display_text = some_list[5][3]
        elif day_of_the_week == 5:
            display_text = some_list[6][3]
        elif day_of_the_week == 6:
            display_text = some_list[0][3]
    if state == "switch":
        if day_of_the_week == 0:
            display_text = some_list[1][4]
        elif day_of_the_week == 1:
            display_text = some_list[2][4]
        elif day_of_the_week == 2:
            display_text = some_list[3][4]
        elif day_of_the_week == 3:
            display_text = some_list[4][4]
        elif day_of_the_week == 4:
            display_text = some_list[5][4]
        elif day_of_the_week == 5:
            display_text = some_list[6][4]
        elif day_of_the_week == 6:
            display_text = some_list[0][4]

    print_with_time("Display link text is: " + display_text)

    return display_text


def shutdown_pi():
    os.system("sudo shutdown -h now")


def reboot_pi():
    os.system("sudo reboot")


def power_display():
    os.system("echo 'on 0.0.0.0' | cec-client -s -d 1")


def shutdown_display():
    os.system("echo 'standby 0.0.0.0' | cec-client -s -d 1")
