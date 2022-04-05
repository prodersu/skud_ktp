import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime

import db_connection as db
from home_window import Ui_HomeWindow
from duty_window import Ui_DutyWindow
from park_window import Ui_ParkWindow
from list_cars import Ui_ListCars

import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
default_text = "---Новых машин нет.---"


class HomeWindow(QtWidgets.QMainWindow, Ui_HomeWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.timer = QtCore.QTimer(self)
        self.timer.start(500)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(getData)

        self.open_duty_btn.clicked.connect(lambda: duty.show())
        self.open_park_btn.clicked.connect(lambda: park.show())
        self.open_cars_btn.clicked.connect(lambda: listCars.show())


class DutyWindow(QtWidgets.QMainWindow, Ui_DutyWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.allow_btn.clicked.connect(lambda: allowAction())
        self.forbid_btn.clicked.connect(lambda: forbidAction())
        self.clean_btn.clicked.connect(lambda: db.delete_records())

    def new_car_text(self, res):
        self.new_car.setText(res)


class ParkWindow(QtWidgets.QMainWindow, Ui_ParkWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.arrive_btn.clicked.connect(lambda: self.arrive())
        self.depart_btn.clicked.connect(lambda: self.depart())
        self.dep_count.setText("1")
        self.arrive_btn.setEnabled(False)
        self.depart_btn.setEnabled(False)

    def depart(self):
        dep_count = 1
        if self.dep_count.toPlainText() is not None:
            dep_count = int(self.dep_count.toPlainText())
        text = self.new_car.text().split(' ')
        car_id = int(text[0][:-1])
        num_model = text[1] + " " + text[2]
        db.depart_car(car_id, dep_count, text[3], num_model)
        self.new_car.setText(default_text)
        self.new_car.setFont(QtGui.QFont("Verdana", 12))
        self.new_car.setStyleSheet("color: black")
        self.depart_btn.setEnabled(False)
        self.arrive_btn.setEnabled(False)

    def arrive(self):
        text = self.new_car.text().split(' ')
        car_id = int(text[0][:-1])
        num_model = text[1] + " " + text[2]
        db.arrive_car(car_id, num_model, text[3])
        self.new_car.setText(default_text)
        self.new_car.setFont(QtGui.QFont("Verdana", 12))
        self.new_car.setStyleSheet("color: black")
        self.arrive_btn.setEnabled(False)
        self.depart_btn.setEnabled(False)

    def new_car_text(self, res):
        self.new_car.setText(res)


class ListCarsWindow(QtWidgets.QMainWindow, Ui_ListCars):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.add_btn.clicked.connect(lambda: self.add_car())
        self.delete_btn.clicked.connect(lambda: self.delete())

    def add_car(self):
        num = self.num_input.toPlainText()
        model = self.model_input.toPlainText()
        if len(num) != 0 and len(model) != 0:
            num = re.sub(' ', '_', num)
            model = re.sub(' ', '_', model)
            db.insert_car(num, model)
            self.num_input.setText("")
            self.model_input.setText("")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Заполните все формы")
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def delete(self):
        selectedRow = str(self.all_cars.currentItem().text())
        if selectedRow is not None:
            car_id = selectedRow.split(':')[0]
            db.delete_car(car_id)


# def openDutyWindow():
#     duty = DutyWindow()
#     duty.show()
#     resValue = duty.exec_()
#
#
# def openParkWindow():
#     park = ParkWindow()
#     park.show()
#     resValue = park.exec_()
#
#
# def openListCarsWindow():
#     listWindow = ListCarsWindow()
#     listWindow.show()
#     resValue = listWindow.exec_()

duty = DutyWindow
park = ParkWindow
listCars = ListCarsWindow


def allowAction():
    park.new_car.setText(park.new_car.text() + " --Добро-- ")
    park.new_car.setStyleSheet("color: green")
    duty.new_car.setText(default_text)
    park.depart_btn.setEnabled(True)
    park.arrive_btn.setEnabled(True)


def forbidAction():
    park.new_car.setText(park.new_car.text() + " --Запрет-- ")
    park.new_car.setStyleSheet("color: red")
    duty.new_car.setText(default_text)
    park.depart_btn.setEnabled(False)
    park.arrive_btn.setEnabled(False)


def getData():
    # get all cars
    duty.all_cars.clear()
    park.all_cars.clear()
    listCars.all_cars.clear()
    cars = db.get_cars()
    for car in cars:
        car_text = str(car[0]) + ": " + car[1] + " " + car[2]
        car_text = re.sub('_', ' ', car_text)
        duty.all_cars.addItem(car_text)
        park.all_cars.addItem(car_text)
        listCars.all_cars.addItem(str(car_text))
    duty.cars_amount.setText(str(len(duty.all_cars)))
    park.cars_amount.setText(str(len(park.all_cars)))
    listCars.cars_amount.setText(str(len(listCars.all_cars)))
    # get arrived cars
    duty.arrived_cars.clear()
    park.arrived_cars.clear()
    cars = db.get_arrived_cars()
    if cars is not None:
        for car in cars:
            car_text = str(car[3]) + ": " + car[1] + " " + car[2]
            car_text = re.sub('_', ' ', car_text)
            duty.arrived_cars.addItem(car_text)
            park.arrived_cars.addItem(car_text)
    duty.arrive_amount.setText(str(len(duty.arrived_cars)))
    park.arrive_amount.setText(str(len(park.arrived_cars)))
    # get departed cars
    duty.departed_cars.clear()
    park.departed_cars.clear()
    cars = db.get_departed_cars()
    if cars is not None:
        for car in cars:
            car_text = str(car[1]) + ": " + car[4] + " " + str(car[3]) + " человек " + car[2]
            car_text = re.sub('_', ' ', car_text)
            duty.departed_cars.addItem(car_text)
            park.departed_cars.addItem(car_text)
    duty.depart_amount.setText(str(len(duty.departed_cars)))
    park.depart_amount.setText(str(len(park.departed_cars)))


def sort_results(text):
    nums = False
    car_num = "abc"
    for i in range(len(text) - 2):
        if text[i:i + 3].isnumeric():
            car_num = text[i:i + 3]
            nums = True

    if len(text) < 5 and not nums:
        pass
    else:
        if car_num.isnumeric():
            print(car_num)
            res = db.find_car(car_num)
            if res is not None and duty.new_car.text().split('.')[0] is not car_num:
                now = datetime.now()
                current_time = now.strftime("%d/%m/%Y-%H:%M")
                result_text = str(res[0]) + ". " + str(res[1]) + " " + str(res[2]) + " " + current_time
                duty.new_car_text(result_text)
                park.new_car_text(result_text)
                # w.new_car_text(result)
                cv2.waitKey(15 * 1000)


def camera_work():
    cap = cv2.VideoCapture(0)
    cap.set(3, 500)
    cap.set(4, 500)

    while True:
        success, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cars = cv2.CascadeClassifier('cascades/car.xml')
        cars1 = cv2.CascadeClassifier('cascades/car1.xml')
        cars2 = cv2.CascadeClassifier('cascades/car2.xml')

        var1 = cars.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(25, 25))
        var2 = cars1.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(25, 25))
        var3 = cars2.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(25, 25))

        variants = [var1, var2, var3]
        results = None
        for res in variants:
            if res is None:
                pass
            else:
                results = res

        if results is None:
            cv2.imshow('Camera', img)
        else:
            result = None
            for (x, y, w, h) in results:
                result = img[y:y + h, x:x + w]
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 0, 255), 2)
            if result is None:
                cv2.imshow('Camera', img)
            else:
                cv2.imshow('Camera', img)
                res_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
                res_blur = cv2.bilateralFilter(res_gray, 5, 90, 90)
                unknown_text = pytesseract.image_to_string(res_blur, lang="eng")
                sort_results(unknown_text)

        if cv2.waitKey(10) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    duty = DutyWindow()
    park = ParkWindow()
    listCars = ListCarsWindow()
    home = HomeWindow()
    home.show()
    camera_work()
    sys.exit(app.exec_())
