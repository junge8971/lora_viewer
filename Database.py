#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2


class Database:
    def __init__(self):
        self.db_name = 'Lora'  # имя базы данных
        self.db_user = 'postgres'  # имя пользователя для сервера бд
        self.db_password = '123321'  # пароль для пользователя
        self.db_host = '127.0.0.1'  # адрес бд

    def request_to_bd(self, request_to_db: str, params: list | None = None) -> None | list[dict, ...]:
        """
        Функция делает запрос к базе по предоставленной строке \n
        """
        try:
            connect = psycopg2.connect(dbname=self.db_name,
                                       user=self.db_user,
                                       password=self.db_password,
                                       host=self.db_host)
            cursor = connect.cursor()
            if params is None:
                cursor.execute(request_to_db)
                connect.commit()
                record = cursor.fetchall()
            else:
                full_request = cursor.mogrify(request_to_db, params)
                cursor.execute(full_request)
                connect.commit()
                record = cursor.fetchall()
            return record
        except Exception as error:
            print(f'Ошибка: {error}')
        finally:
            if connect:
                cursor.close()
                connect.close()

    def create_a_table_of_sensor_readings(self) -> None:
        """
        Создаёт таблицу показаний сенсоров (которая №1 на предорставленной схеме)\n
        Содержит поля:\n
        sensor_number - номер сенсора,\n
        date_and_time_UTC - дата и время,\n
        coordinates - координаты,\n
        sensor_readings - показания записаны в символьном формате длинной 20,
        можно втсавить путь и строку
        """
        text = """
                CREATE TABLE IF NOT EXISTS table_of_sensor_readings
                (
                sensor_number CHAR(4) PRIMARY KEY NOT NULL,
                date_and_time_UTC TIMESTAMPTZ NOT NULL,
                coordinates CHAR(20) NOT NULL,
                sensor_readings CHAR(20)
                );
                """
        return self.request_to_bd(text)

    def add_new_sensor_reading(self,
                               sensor_number: str,
                               date_and_time_UTC: str,
                               coordinates: str,
                               sensor_readings: str | None = None
                               ) -> None:
        """
       Добавляет в таблицу показаний сенсоров новую запись (которая №1 на предорставленной схеме)\n
        :param sensor_number: номер сенсора (обязательное значение)
        :param date_and_time_UTC: дата и время в формате: '{year}-{month}-{day} {hour}:{minute}:{sec} Europe/Moscow' (обязательное значение)
        :param coordinates: координаты (обязательное значение)
        :param sensor_readings: показания сенсоров, по дефолту null
        """
        text = """
                INSERT INTO table_of_sensor_readings VALUES (%s, %s, %s, %s)"""
        params = [sensor_number, date_and_time_UTC, coordinates, sensor_readings]
        self.create_a_table_of_sensor_readings()
        return self.request_to_bd(text, params)

    def get_all_sensor_reading(self) -> list[dict, ...]:
        """
        Функция берёт из таблицы показаний сенсоров все значения (которая №1 на предорставленной схеме)\n
        :return: возвращает список словарей, где словари являются содержимым сток.
        """
        text = """ SELECT json_agg(table_of_sensor_readings) FROM table_of_sensor_readings"""
        return self.request_to_bd(text)[0][0]

    def create_a_table_of_sensors(self) -> None:
        """
        Создаёт таблицу сенсоров (которая №2 на предорставленной схеме)\n
        Содержит поля:\n
        sensor_number - номер сенсора,\n
        temperature -температура,\n
        atmosphere_pressure - атмосферное давление,\n
        air_humidity -влажность воздуха,\n
        watering - полив\n
        """
        text = """
                CREATE TABLE IF NOT EXISTS table_of_sensors
                (
                sensor_number CHAR(4) PRIMARY KEY,
                temperature DOUBLE PRECISION,
                atmosphere_pressure DOUBLE PRECISION,
                air_humidity DOUBLE PRECISION,
                watering INT
                );
                """
        return self.request_to_bd(text)

    def add_new_sensor(self,
                       sensor_number: str,
                       temperature: float | None = None,
                       atmosphere_pressure: float | None = None,
                       air_humidity: float | None = None,
                       watering: int | None = None) -> None:
        """
        Добавляет в таблицу сенсоров новую запись (которая №2 на предорставленной схеме)\n
        :param sensor_number: номер сенсора (обязательное значение)
        :param temperature: температура, по дефолту null
        :param atmosphere_pressure: атмосферное давление, по дефолту null
        :param air_humidity: влажность воздуха, по дефолту null
        :param watering: полив, по дефолту null
        """
        text = """
                INSERT INTO table_of_sensors VALUES (%s, %s, %s, %s, %s)"""
        params = [sensor_number, temperature, atmosphere_pressure, air_humidity, watering]
        self.create_a_table_of_sensors()
        return self.request_to_bd(text, params)

    def get_all_sensors(self) -> list[dict, ...]:
        """
        Функция берёт из таблицы сенсоров все записи (которая №2 на предорставленной схеме)\n
        :return: возвращает список словарей, где словари являются содержимым сток.
        """
        text = """ SELECT json_agg(table_of_sensors) FROM table_of_sensors"""
        return self.request_to_bd(text)[0][0]
