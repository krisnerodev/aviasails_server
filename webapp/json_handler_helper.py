import os
import re
from flask import json
from webapp.constants import lastHourSuffix, last3DaysSuffix, yesterdaySuffix


def get_json_path(static_folder, file_name):
    return os.path.join(static_folder, file_name)


def load_json(file_path):
    try:
        with open(file_path) as dashboard:
            return json.load(dashboard)
    except:
        print('file not found')
        return ''


def get_keys_by_suffix(json_data, key_suffix):
    keys = json_data.keys()

    filtered_keys = []
    keys_without_suffix = []

    for key in keys:
        regexp = r'' + key
        if re.search(key_suffix, regexp):
            filtered_keys.append(key)
            keys_without_suffix.append(re.sub(r'' + key_suffix, '', key))

    return {
        'keys_without_suffix': keys_without_suffix,
        'filtered_keys': filtered_keys
    }


def assemble_data_for_client(json_data, keys_list):
    result = {}

    filtered_keys = keys_list['filtered_keys']
    keys_without_suffix = keys_list['keys_without_suffix']

    for index, key in enumerate(filtered_keys):
        result[keys_without_suffix[index]] = json_data[key]

    return result


def find_all_fields_by_suffix(dashboard_dict, key_suffix, timeInterval):
    errors_keys = get_keys_by_suffix(dashboard_dict, key_suffix)
    data_keys = get_keys_by_suffix(dashboard_dict['data'][0], key_suffix)  # better not use [0] but now I keep this

    errors_list = assemble_data_for_client(dashboard_dict, errors_keys)
    data_list = assemble_data_for_client(dashboard_dict['data'][0], data_keys)
    not_reflected_fields = get_not_date_reflect_fields(dashboard_dict)

    return {
        'errors': errors_list['errors'],
        'data': dict(data_list, **not_reflected_fields),
        'timeInterval': timeInterval
    }


def get_not_date_reflect_keys(dashboard_data):
    not_reflected_keys = []
    for key in dashboard_data:
        regexp = r'' + key

        if not re.search(yesterdaySuffix, regexp) \
                and not re.search(lastHourSuffix, regexp) \
                and not re.search(last3DaysSuffix, regexp):
            not_reflected_keys.append(key)

    return not_reflected_keys


def get_not_date_reflect_fields(dashboard_dict):
    dashboard_data = dashboard_dict['data'][0]
    not_date_reflected_keys = get_not_date_reflect_keys(dashboard_data)
    not_date_reflected_fields = {}

    for key in not_date_reflected_keys:
        not_date_reflected_fields[key] = dashboard_data[key]

    return not_date_reflected_fields
