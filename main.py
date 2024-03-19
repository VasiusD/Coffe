import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.buttons = []
        self.con = sqlite3.connect("coffee.sqlite")
        self.b.clicked.connect(self.coffe)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
