def convert_time_to_list(time):
    if type(time) == 'None':
        return ['','']
    if time == '':
        return ['','']
    if time[len(time)-2:] != 'pm' or time[len(time)-2:] != 'am':
        if time[len(time)-1] == 'a' or time[len(time)-1] == 'p':
            time = time + 'm'
    if time[len(time)-3] != ' ':
        temp_time = time
        time = temp_time[0:len(temp_time)-2] + ' ' + temp_time[len(temp_time)-2:len(temp_time)]
    timeList = []
    colonSplit = time.split(':')
    timeList.append(int(colonSplit[0]))
    spaceSplit = colonSplit[1].split(' ')
    if spaceSplit[1] == 'AM' or spaceSplit[1] == 'am' and timeList[0] == 12:
        timeList[0] = 0
    timeList.append(int(spaceSplit[0]))
    if (spaceSplit[1] == 'PM' or spaceSplit[1] == 'pm' and timeList[0] != 12):
        timeList[0] = int(timeList[0]) + 12
    return timeList

def convert_time_list_to_string(list):
    temp_string = ''
    for item in list:
        temp_string += str(item)
    return temp_string

def return_list_of_entries_as_lists(database):
    def return_list_of_values_from_entry(entry):
        value_list = []
        value_list.append(entry.start_time)
        value_list.append(entry.switch_time)
        value_list.append(entry.end_time)
        value_list.append(entry.start_link_text)
        value_list.append(entry.switch_link_text)
        return value_list
    
    db_list = []
    returned_list = []
    
    for x in range(7):
        db_list.append(database.query.get(x + 1))
    
    for entry in db_list:
        returned_list.append(return_list_of_values_from_entry(entry))
    
    return returned_list

def return_form_data_as_list_of_dict(form):
    sunday_entry = {
        'day_of_the_week': 'Sunday',
        'start_time': form.sunday_start_time.data,
        'switch_time': form.sunday_switch_time.data,
        'end_time': form.sunday_end_time.data,
        'start_link_text': form.sunday_start_text.data,
        'switch_link_text': form.sunday_switch_text.data
    }

    monday_entry = {
        'day_of_the_week': 'Monday',
        'start_time': form.monday_start_time.data,
        'switch_time': form.monday_switch_time.data,
        'end_time': form.monday_end_time.data,
        'start_link_text': form.monday_start_text.data,
        'switch_link_text': form.monday_switch_text.data
    }

    tuesday_entry = {
        'day_of_the_week': 'Sunday',
        'start_time': form.tuesday_start_time.data,
        'switch_time': form.tuesday_switch_time.data,
        'end_time': form.tuesday_end_time.data,
        'start_link_text': form.tuesday_start_text.data,
        'switch_link_text': form.tuesday_switch_text.data
    }

    wednesday_entry = {
        'day_of_the_week': 'Sunday',
        'start_time': form.wednesday_start_time.data,
        'switch_time': form.wednesday_switch_time.data,
        'end_time': form.wednesday_end_time.data,
        'start_link_text': form.wednesday_start_text.data,
        'switch_link_text': form.wednesday_switch_text.data
    }

    thursday_entry = {
        'day_of_the_week': 'Sunday',
        'start_time': form.thursday_start_time.data,
        'switch_time': form.thursday_switch_time.data,
        'end_time': form.thursday_end_time.data,
        'start_link_text': form.thursday_start_text.data,
        'switch_link_text': form.thursday_switch_text.data
    }

    friday_entry = {
        'day_of_the_week': 'Monday',
        'start_time': form.friday_start_time.data,
        'switch_time': form.friday_switch_time.data,
        'end_time': form.friday_end_time.data,
        'start_link_text': form.friday_start_text.data,
        'switch_link_text': form.friday_switch_text.data
    }

    saturday_entry = {
        'day_of_the_week': 'Monday',
        'start_time': form.saturday_start_time.data,
        'switch_time': form.saturday_switch_time.data,
        'end_time': form.saturday_end_time.data,
        'start_link_text': form.saturday_start_text.data,
        'switch_link_text': form.saturday_switch_text.data
    }


    entry_list = [sunday_entry, monday_entry, tuesday_entry, wednesday_entry, thursday_entry, friday_entry, saturday_entry]
    return entry_list

def update_entry(database, entry, id):
    updated_entry = database.query.get(id) # find entry to be updated
    updated_entry.start_time = convert_time_list_to_string(convert_time_to_list(entry['start_time'])) # update start time after converting to proper format
    updated_entry.switch_time = convert_time_list_to_string(convert_time_to_list(entry['switch_time'])) # update switch time after converting to proper format
    updated_entry.end_time = convert_time_list_to_string(convert_time_to_list(entry['end_time'])) # update end time after converting to proper format
    updated_entry.start_link_text = entry['start_link_text'] # update start link text
    updated_entry.switch_link_text = entry['switch_link_text'] # update switch link text