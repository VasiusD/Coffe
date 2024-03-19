import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.w = None
        self.con = sqlite3.connect("coffee.sqlite")
        self.b.clicked.connect(self.coffe)
        self.b_open.clicked.connect(self.show_new_window)

    def show_new_window(self):
        if self.w is None:
            self.w = AnotherWindow()
        self.w.show()

    def open_coffe(self):
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.b_change.clicked.connect(self.change_coffe)
        self.b_add.clicked.connect(self.add_coffe)
        self.b_return.clicked.connect(self.comeback_coffe)

    def coffe(self):
        query = f"SELECT ID, name, step, molORzer, description, cost, size FROM Coffe_sort"
        cur = self.con.cursor()
        result = cur.execute(query).fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage("К сожалению, ничего не нашлось")
            return
        self.statusBar().showMessage(f"Нашлось {len(result)} записей")
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "название сорта", "степень обжарки", "молотый/в зернах", 'описание вкуса', "цена", "объем упаковки"])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()


class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.b_change.clicked.connect(self.change_coffe)
        self.b_add.clicked.connect(self.add_coffe)
        self.b_return.clicked.connect(self.comeback_coffe)
        query = f"SELECT ID, name, step, molORzer, description, cost, size FROM Coffe_sort"
        cur = self.con.cursor()
        result = cur.execute(query).fetchall()
        self.tableWidget.setRowCount(len(result) + 1)
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "название сорта", "степень обжарки", "молотый/в зернах", 'описание вкуса', "цена", "объем упаковки"])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()

    def change_coffe(self):
        for i in range(self.tableWidget.rowCount()):
            cur = self.con.cursor()
            que = f"""UPDATE Coffe_sort SET name = "{self.tableWidget.item(i, 1).text()}",
            step = "{self.tableWidget.item(i, 2).text()}", 
            molORzer = "{self.tableWidget.item(i, 3).text()}", 
            description = "{self.tableWidget.item(i, 4).text()}", 
            cost = "{self.tableWidget.item(i, 5).text()}", 
            size = "{self.tableWidget.item(i, 6).text()}" WHERE ID = {i + 1}"""
            cur.execute(que)
            self.con.commit()


    def add_coffe(self):
        cur = self.con.cursor()
        data = [self.tableWidget.item(self.tableWidget.rowCount() - 1, x).text()
                for x in range(1, 7)]
        que = f"""INSERT INTO Coffe_sort(name, step, molORzer, description, cost, size)
        VALUES('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', '{data[5]}');"""
        cur.execute(que)
        self.con.commit()

    def comeback_coffe(self):
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
