# main_logic.py
import sys
import json
import time
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate
from datetime import datetime

from ui_pantalla import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Datos Json")

        # creating QAction Instances
        self.pushButtonAll.clicked.connect(self.load_data)
        self.pushButtonRange.clicked.connect(self.load_data_between_dates)
        self.lineEditBuscar

        # Establecer la fecha actual en dateEditInicio y dateEditFin al inicio
        current_date = QDate.currentDate()
        self.dateEditInicio.setDate(current_date)
        self.dateEditFin.setDate(current_date)

        # Conectar la señal returnPressed (tecla Enter) del lineEditBuscar a la función search_on_enter
        self.lineEditBuscar.returnPressed.connect(self.search_on_enter)

    def clear_table(self):
        self.tableWidget.clearContents()  # Eliminar los datos existentes
        self.tableWidget.setRowCount(0)   # Establecer el número de filas en 0

    def load_data(self):
        start_time = time.time()  # Registrar el tiempo de inicio

        #self.tableWidget.clearContents()  # Eliminar los datos existentes
        #self.tableWidget.setRowCount(0)   # Establecer el número de filas en 0
        self.clear_table()

        filename = "data/MOCK_DATA.json"
        with open(filename, "r") as file:
            data = json.load(file)

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))

        headers = list(data[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_value in enumerate(row_data.values()):
                item = QTableWidgetItem(str(cell_value))
                self.tableWidget.setItem(row_idx, col_idx, item)
        
        end_time = time.time()  # Registrar el tiempo de finalización
        elapsed_time = end_time - start_time  # Calcular el tiempo transcurrido
        self.labelTiempo.setText(f"Tiempo de carga: {elapsed_time:.2f} segundos")  # Mostrar el tiempo en el label

        self.labelRegistros.setText(f"Registros: {len(data)}")

        file_size = os.path.getsize(filename)  # Obtener el tamaño del archivo en bytes
        self.labelPeso.setText(f"Peso del archivo: {file_size / 1024:.2f} KB")  # Mostrar el peso en el label

    
    def load_data_between_dates(self):
        start_time = time.time()  # Registrar el tiempo de inicio

        #self.tableWidget.clearContents()  # Eliminar los datos existentes
        #self.tableWidget.setRowCount(0)   # Establecer el número de filas en 0
        self.clear_table()

        filename = "data/MOCK_DATA.json"
        with open(filename, "r") as file:
            data = json.load(file)

        inicio_date = self.dateEditInicio.date().toPyDate()
        fin_date = self.dateEditFin.date().toPyDate()

        filtered_data = [entry for entry in data if inicio_date <= datetime.strptime(entry["fecha"], "%m/%d/%Y").date() <= fin_date]

        self.tableWidget.setRowCount(len(filtered_data))
        self.tableWidget.setColumnCount(len(filtered_data[0]))

        headers = list(filtered_data[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(filtered_data):
            for col_idx, cell_value in enumerate(row_data.values()):
                item = QTableWidgetItem(str(cell_value))
                self.tableWidget.setItem(row_idx, col_idx, item)

        end_time = time.time()  # Registrar el tiempo de finalización
        elapsed_time = end_time - start_time  # Calcular el tiempo transcurrido

        self.labelTiempo.setText(f"Tiempo de carga: {elapsed_time:.2f} segundos")  # Mostrar el tiempo en el label
        
        file_size = os.path.getsize(filename)  # Obtener el tamaño del archivo en bytes
        self.labelPeso.setText(f"Peso del archivo: {file_size / 1024:.2f} KB")  # Mostrar el peso en el label
    

    def search_on_enter(self):
        start_time = time.time()  # Registrar el tiempo de inicio

        self.clear_table()

        search_text = self.lineEditBuscar.text().lower()

        if self.radioButtonId.isChecked():
            key = 'id'
        elif self.radioButtonNombre.isChecked():
            key = 'Nombre'
        elif self.radioButtonApellido.isChecked():
            key = 'Apellido'
        else:
            return

        filename = "data/MOCK_DATA.json"
        with open(filename, "r") as file:
            data = json.load(file)

        if key == 'id':
            # error en lower con datos numericos
            filtered_data = [entry for entry in data if str(entry[key]) == search_text]
        else:
            filtered_data = [entry for entry in data if search_text in entry[key].lower()]

        self.tableWidget.setRowCount(len(filtered_data))
        self.tableWidget.setColumnCount(len(filtered_data[0]))

        headers = list(filtered_data[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(filtered_data):
            for col_idx, cell_value in enumerate(row_data.values()):
                item = QTableWidgetItem(str(cell_value))
                self.tableWidget.setItem(row_idx, col_idx, item)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
