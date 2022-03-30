import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime

from gui import UiMainWindow
import db_connection as db

import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class AddDialog(QtWidgets.QDialog, UiMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(
            lambda: self.add_car(self.num_input.toPlainText(), self.model_input.toPlainText()))
        self.buttonBox.rejected.connect(lambda: self.cancel())

    def cancel(self):
        self.close()

    def add_car(self, num, model):
        if len(num) != 0 and len(model) != 0:
            db.insert_car(num, model)
            getCars()
            self.close()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Заполните все формы")
            msg.setWindowTitle("Ошибка")
            msg.exec_()


def openDialog():
    dialog = AddDialog()
    resValue = dialog.exec_()


class MainWindow(QtWidgets.QMainWindow, UiMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.open_dialog.clicked.connect(lambda: openDialog())
        self.arrive_btn.clicked.connect(lambda: self.arrive(self.new_car.text()))
        self.depart_btn.clicked.connect(lambda: self.depart(self.new_car.text()))
        self.clean_btn.clicked.connect(lambda: self.clear())
        self.all_cars.itemSelectionChanged.connect(lambda: self.itemSelect())

    def itemSelect(self):
        self.open_dialog.setVisible(False)

    def new_car_text(self, res):
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y,_%H:%M")
        result = res[0] + ". " + res[1] + " " + res[2] + " " + current_time
        print(result)
        self.new_car.setText(result)

    def arrive(self, text):
        if text != "* Новых машин нет":
            self.arrived_cars.addItem(text)
            self.label_6.setText(str(len(self.arrived_cars)))
            self.new_car.setText("* Новых машин нет")

    def depart(self, text):
        if text != "* Новых машин нет":
            self.depart_cars.addItem(text)
            self.label_5.setText(str(len(self.depart_cars)))
            self.new_car.setText("* Новых машин нет")

    def clear(self):
        self.depart_cars.clear()
        self.arrived_cars.clear()
        self.label_5.setText("0")
        self.label_6.setText("0")


w = MainWindow


def getCars():
    w.all_cars.clear()
    cars = db.get_cars()
    for car in cars:
        w.all_cars.addItem(str(car[0]) + ": " + car[1] + " " + car[2])
    w.label_7.setText(str(len(w.all_cars)))


def sort_results(text):
    nums = False
    car_num = "abc"
    for i in range(len(text)-2):
        if text[i:i+3].isnumeric():
            car_num = text[i:i+3]
            nums = True

    if len(text) < 5 and not nums:
        pass
    else:
        if car_num.isnumeric():
            print(car_num)
            result = db.find_car(car_num)
            if result is not None:
                w.new_car_text(result)
                cv2.waitKey(15*1000)


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
    w = MainWindow()
    getCars()
    w.show()
    camera_work()
    sys.exit(app.exec_())
