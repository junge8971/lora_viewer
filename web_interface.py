#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from Database import Database

app = Flask(__name__)
app.secret_key = 'asfouhvnsldvszkldvmszdfv'


@app.route('/', methods=['GET', 'POST'])
@app.route('/sensors', methods=['GET', 'POST'])
def sensor():
    if request.method == 'POST':
        list_of_checked_values = list(request.form.values())
        if list_of_checked_values:
            result = {}
            for item in list_of_checked_values:
                sensor_number = item[0:4]
                if result.get(sensor_number) is None:
                    result.update({sensor_number: [item[5:]]})
                else:
                    checked_params_for_sensor = result.get(sensor_number)
                    checked_params_for_sensor += [item[5:]]
                    result.update({sensor_number: checked_params_for_sensor})
            print(result)
        else:
            return 'Ничего не выбранно'


    db = Database()
    all_sensors = db.get_all_sensors()

    # создаём список, в котором не будет записей со всеми пустыми значениями
    all_sensors_without_emptiness = []
    for item in all_sensors:
        all_values_for_dict = list(item.values())
        if all_values_for_dict.count(None) >= 4:
            continue
        else:
            all_sensors_without_emptiness.append(item)

    return render_template('sensor_template.html', sensors=all_sensors_without_emptiness)


@app.route('/sensor_reading')
def sensor_reading():
    db = Database()
    all_sensors = db.get_all_sensors()
    all_sensors_reading = db.get_all_sensor_reading()
    return render_template('sensor_reading_and_sensors.html', sensors=all_sensors, sensors_reading=all_sensors_reading)


def main():
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
