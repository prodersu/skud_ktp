import sqlite3 as sl
from datetime import datetime


con = sl.connect('database.sqlite')


def find_car(num):
    with con:
        result = con.execute("select * from cars where number like '%"+num+"%'")
        res = result.fetchone()
        return res


def insert_car(num, model):
    with con:
        car = (num, model)
        con.execute("insert into cars values(null, ?, ?)", car)
        con.commit()


def depart_car(car_id, people_count, current_time, num_model):
    with con:
        data = (car_id, current_time, people_count, num_model)
        con.execute("insert into departed values(null, ?, ?, ?, ?)", data)
        con.commit()


def arrive_car(car_id, num_model, arrived_time):
    with con:
        data = (arrived_time, num_model, car_id)
        con.execute("insert into arrived values(null, ?, ?, ?)", data)
        con.commit()


def delete_car(car_id):
    with con:
        con.execute("delete from cars where id like '%"+car_id+"%'")
        con.commit()


def get_cars():
    with con:
        data = con.execute("select * from cars")
        return data


def get_arrived_cars():
    with con:
        data = con.execute("select * from arrived")
        return data


def get_departed_cars():
    with con:
        data = con.execute("select * from departed")
        return data


def delete_records():
    with con:
        con.execute("delete from departed")
        con.commit()

    with con:
        con.execute("delete from arrived")
        con.commit()
