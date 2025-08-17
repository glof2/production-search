# Libraries
from PyQt6.QtCore import (Qt)
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout)
from PyQt6.QtGui import(QPixmap)

import json
import sys

# Functions
def loadData():
    with open("data.json", "r") as file:
        return json.load(file)["data"]

# Main logic

# Prepare for program launch ...
# Load product data
data = loadData()

# Prepare GUI
app = QApplication([])
window = QWidget()
layout = QHBoxLayout()

# Load table
table = QTableWidget(window)
table.setRowCount(len(data))
table.setColumnCount(len(data[0]))

# Get column names
column_names = []
for key in data[0]:
    column_names.append(key)

table.setHorizontalHeaderLabels(column_names)
table.verticalHeader().hide()

# Fill out table
row_index = 0
for row_data in data:

    column_index = 0

    for column_name in column_names:
        e = 1
        item = QTableWidgetItem(str(row_data[column_name]))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table.setItem(row_index, column_index, item)


        column_index += 1

    row_index += 1

layout.addWidget(table)

#table.show()


label = QLabel(window)
pixmap = QPixmap("res/stacking/12-33.JPG")
label.setPixmap(pixmap)
#label.show()
layout.addWidget(label)

# Set the window size based on the image size
#label.resize(pixmap.width(), pixmap.height())

window.setLayout(layout)

window.show()
app.exec()