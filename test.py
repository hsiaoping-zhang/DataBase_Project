import sys
import os
import time
import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QListView, QFileDialog
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSlot

from MarkQtUI import Ui_MainWindow
import database
import windows


class Mark(QMainWindow, Ui_MainWindow):
    method = ["SQL"]
    prev_text = ""
    prev_column = ["", ""]

    def __init__(self, parent=None):
        # 繼承Ui_MainWindow 也就是 mark_tool 內的 class
        super(Mark, self).__init__(parent)

        # 建立ui介面
        self.setupUi(self)
        # 這功能主要是點擊了這個按鈕要執行什麼？
        # self.Test_Button 這個 function 在 MarkQtUI.Ui_MainWindow內
        # 因為已經繼承了Ui_MainWindow，因此執行 self.Test_Button
        # 點擊了時候會套用下方的function test_button_clicked，會將值輸出
        # 如果沒有這行，點擊按鈕不會有任何的動作
        # self.view.setScene(myScene);
        # self.view.setForegroundBrush(QtGui.QColor('red'));
        self.comboBox.addItems(["SQL 指令", "查詢", "刪除", "新增"])
        self.table_text.setText("SONG")
        self.comboBox_column.addItems(windows.get_query_column("SONG"))
        self.comboBox_column.currentTextChanged.connect(self.comboBox_change)

        # when combo box is changed, clear the query text
        self.comboBox.currentTextChanged.connect(lambda : windows.comboBox_change(self.comboBox, self.queryText, self.method))
        self.TestButton.clicked.connect(self.test_button_clicked)
        
        # query buttton's text append to the query text
        self.btnSelect.clicked.connect(lambda : windows.query_button_clicked(self.btnSelect, self.queryText))
        self.btnFrom.clicked.connect(lambda : windows.query_button_clicked(self.btnFrom, self.queryText))
        self.btnDistinct.clicked.connect(lambda : windows.query_button_clicked(self.btnDistinct, self.queryText))
        self.btnWhere.clicked.connect(lambda : windows.query_button_clicked(self.btnWhere, self.queryText))
        self.btnDelete.clicked.connect(lambda : windows.query_button_clicked(self.btnDelete, self.queryText))
        self.btnUpdate.clicked.connect(lambda : windows.query_button_clicked(self.btnUpdate, self.queryText))

        # change table title
        self.table_song.clicked.connect(lambda : windows.change_title(self.table_song, self.comboBox_column, self.table_text, self.queryText, self.method))
        self.table_movie.clicked.connect(lambda: windows.change_title(self.table_movie, self.comboBox_column, self.table_text, self.queryText, self.method))
        self.table_concert.clicked.connect(lambda: windows.change_title(self.table_concert, self.comboBox_column, self.table_text, self.queryText, self.method))
        self.table_place.clicked.connect(lambda: windows.change_title(self.table_place, self.comboBox_column, self.table_text, self.queryText, self.method))
        self.table_person.clicked.connect(lambda: windows.change_title(self.table_person, self.comboBox_column, self.table_text, self.queryText, self.method))
        self.table_album.clicked.connect(lambda: windows.change_title(self.table_album, self.comboBox_column, self.table_text, self.queryText, self.method))


    # 不同的功能對 comboBox 改變執行動作不同
    def comboBox_change(self):
        text = self.queryText.toPlainText()
        if(text == ""):
            self.prev_column[0] = self.comboBox_column.currentText()
            return

        if(self.method[0] == "select" or self.method[0] == "delete"):   
            string = self.get_substring("AND ")
            print("text:[%s]" % (string))
            self.prev_text += string

        elif(self.method[0] == "insert"):
            string = self.get_substring(", ")
            print("text:[%s]" % (string))
            self.prev_text += string

        windows.comboBox_column_change(self.comboBox_column, self.queryText, self.method)
        self.queryText.setText("")
        

    def test_button_clicked(self):
        query = self.queryText.toPlainText()
        print("method:", self.method[0])

        if(self.method[0] == "SQL"):
            operand = windows.get_command(query)

        elif(self.method[0] == "select" or self.method[0] == "delete"):
            # get adding string
            method_text = self.method[0].upper()
            string = self.get_substring("")  # final: need not AND
            self.prev_text += string
            table_text = self.table_text.text()

            if(method_text == "DELETE"):
                final_query = "%s FROM %s WHERE %s" % (method_text, table_text, self.prev_text) 
            else:
                final_query = "%s * FROM %s WHERE %s" % (method_text, table_text, self.prev_text) 
            
            query = final_query
            operand = windows.get_command(method_text)

        elif(self.method[0] == "insert"):
            string = self.get_substring("")  # final: need not AND
            self.prev_text += string
            table_text = self.table_text.text()

            final_query = "INSERT INTO %s(%s) VALUES(%s)" % (table_text, self.prev_column[1], self.prev_text)
            query = final_query
            operand = windows.get_command("INSERT")

        # query with result output: SELECT / IN / Aggregate function
        if(operand == ""):
            text, result, column = database.search(query)
            self.exec_result.setText(text)
            self.resultText.setText("")
            windows.table_setting(self.table, column, result)

        elif(operand == "EXISTS"):
            text, result, column = database.search(query)
            if("Error" not in text):
                exist = lambda x : True if x == 1 else False
                self.resultText.setText(str(exist(result[0][0])))  # True / False
                self.exec_result.setText("")
                self.queryText.setText("")
        
        # revise data without output: DELETE / INSERT / UPDATE
        else:
            result = database.insert_delete_update(operand, query)
            print(result)
            self.exec_result.setText(result)
            self.resultText.setText("")

        # clear query
        if("Success" in self.exec_result.text() or "Success" in self.resultText.text()):
            self.queryText.setText("")

        # query text reset
        self.prev_text = ""
        self.prev_column[1] = ""
    
    def get_substring(self, and_str):
        query = self.queryText.toPlainText()
        column_text = self.prev_column[0]

        if(column_text == ""):
            self.prev_column[0] = self.comboBox_column.currentText()
            return ""

        # column: name:type
        column_name, column_type = column_text.split(":")[0], column_text.split(":")[1]
        string = ""
        if(column_type == "string"):
            string = "%s == '%s' %s" % (column_name, query, and_str)
        else:
            string = "%s == %s %s" % (column_name, query, and_str)
        
        # for insert 
        if(self.method[0] == "insert"):
            self.prev_column[1] += (column_name + and_str)
            if(column_type == "string"):
                string = "'%s'%s" % (query, and_str)
            else:
                string = "%s %s" % (query, and_str)

        self.prev_column[0] = self.comboBox_column.currentText()  # update column info

        return string

if __name__ == "__main__":

    app = QApplication(sys.argv)  # 第一行必備，系統呼叫 
    window = Mark()               # 指定 Mark Class 會先執行__init__
    window.show()                 # 將 GUI 介面顯示出來 
    sys.exit(app.exec_())         # 關閉系統