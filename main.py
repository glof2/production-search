# Libraries
from PyQt6.QtCore import (Qt)
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QTableWidget, QTableWidgetItem, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QLineEdit)
from PyQt6.QtGui import(QPixmap, QColor)

import json
import sys

##### Functions #####
def loadData():
    with open("data.json", "r") as file:
        return json.load(file)["data"]

def updateTableView(table, search_text, container_type):
    for row_index in range(table.rowCount()):
        name_index = column_names.index("name")
        container_index = column_names.index("type")

        name = table.item( row_index, name_index ).text().lower()
        container = table.item( row_index, container_index ).text().lower()

        query = search_text.lower()

        if query in name and container_type == container:
            table.showRow(row_index)
        else:
            table.hideRow(row_index)
    

##### Main logic #####

# Prepare for program launch ...
# Load product data
data = loadData()

# Global variables
search_query = ""
current_container_index = 0
current_selection_row = 0

column_names = []

# Get column names
for key in data[0]:
    column_names.append(key)


possible_containers = []

for item in data:
    if (item["type"] not in possible_containers):
        possible_containers.append(item["type"])

#### Prepare GUI ####
app = QApplication([])
window = QWidget()
main_layout = QVBoxLayout()
tools_layout = QHBoxLayout()
info_layout = QHBoxLayout()


## Tools ##
search_bar = QLineEdit(window)
search_bar.show()
tools_layout.addWidget(search_bar)

container_combo = QComboBox(window)

container_combo.addItems(possible_containers)

def onIndexChanged(ind):
    global current_container_index
    current_container_index = ind
    updateTableView(table, search_query, possible_containers[current_container_index])

container_combo.currentIndexChanged.connect(onIndexChanged)

tools_layout.addWidget(container_combo)

main_layout.addLayout(tools_layout)

## Info ##

# Load table
table = QTableWidget(window)
table.setRowCount(len(data))
table.setColumnCount(len(data[0]))



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
info_layout.addWidget(label)

def setImage(name:str):
    name = name.replace("/", "-")
    global label
    print("settting to: ", "res/stacking/" + name + ".JPG")
    pixmap = QPixmap("res/stacking/" + name + ".JPG")
    label.setPixmap(pixmap)

main_layout.addLayout(info_layout)
window.setLayout(main_layout)

window.show()


def filter(query):
    global search_query
    search_query = query
    updateTableView(table, search_query, possible_containers[current_container_index])


search_bar.textChanged.connect(filter)

def test():
    global current_selection_row

    sel_row = table.selectedIndexes()[0].row()

    current_selection_row = sel_row

    box_type = table.item(current_selection_row, column_names.index("box_type")).text()
    setImage(box_type)


table.itemSelectionChanged.connect(test)

updateTableView(table, search_query, possible_containers[current_container_index])

app.exec()