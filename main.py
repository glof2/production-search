# Libraries
from PyQt6.QtCore import (Qt)
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit)
from PyQt6.QtGui import(QPixmap, QColor)

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
main_layout = QVBoxLayout()
info_layout = QHBoxLayout()


search_bar = QLineEdit(window)
search_bar.show()
main_layout.addWidget(search_bar)

# Load table
table = QTableWidget(window)
table.setRowCount(len(data))
table.setColumnCount(len(data[0]))

# Get column names
column_names = []
for key in data[0]:
    column_names.append(key)

table.setHorizontalHeaderLabels(column_names)
table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
table.verticalHeader().hide()

# Fill out table
row_index = 0
for row_data in data:

    column_index = 0

    for column_name in column_names:
        item = QTableWidgetItem(str(row_data[column_name]))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table.setItem(row_index, column_index, item)

        column_index += 1

    row_index += 1

info_layout.addWidget(table)

# Stacking method view
label = QLabel(window)
pixmap = QPixmap("res/stacking/12-33.JPG")
label.setPixmap(pixmap)
info_layout.addWidget(label)

main_layout.addLayout(info_layout)
window.setLayout(main_layout)

window.show()



#search_bar.textChanged.connect()

def filter(query):
    for row_index in range(table.rowCount()):
        column_index = column_names.index("name")
        
        name = table.item( row_index, column_index ).text().lower()
        query = query.lower()

        if query in name:
            table.showRow(row_index)
        else:
            table.hideRow(row_index)


search_bar.textChanged.connect(filter)

current_selection_row = 0
def test():
    global current_selection_row

    sel_row = table.selectedIndexes()[0].row()

    current_selection_row = sel_row

table.itemSelectionChanged.connect(test)


app.exec()