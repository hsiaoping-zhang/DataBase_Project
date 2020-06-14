from PyQt5 import QtCore, QtGui, QtWidgets

global text_append
text_append = True

# query button is clicked, append text to query block
def query_button_clicked(btn, queryText):
    text = btn.text()
    queryText.textCursor().insertText(text + " ")
    print("query append finish:", text)

# comboBox change: clear text, if method is button, show the column
def comboBox_change(comboBox, text, method):
    text.clear()
    if(comboBox.currentText() == "SQL 指令"):
        method[0] = "SQL"
    elif(comboBox.currentText() == "新增"):
        method[0] = "insert"
    elif(comboBox.currentText() == "刪除"):
        method[0] = "delete"
    elif(comboBox.currentText() == "查詢"):
        method[0] = "select"
    print(method[0])

# append column to queryText
def comboBox_column_change(comboBox, queryText, method):
    
    if(not method[0] == "SQL"):
        return

    text = comboBox.currentText()
    global text_append
    if(text_append == False):
        return
    queryText.textCursor().insertText(text + " ")
    print("column append finish:", text)

# change title, change column list
def change_title(btn, comboBox, title, queryText, method):
    text = btn.text()
    comboBox.clear()
    title.setText(text) 
    global text_append
    text_append = False      # lock to avoid appending default column to query text
    comboBox.addItems(get_query_column(text))
    if(method[0] == "SQL"):
        text_append = True   # unlock

def table_setting(table, column, data):
    clear_table(table)
    table.setColumnCount(len(column))
    table.setHorizontalHeaderLabels(column)

    # add data to table
    for row in data:
        count = table.rowCount()
        table.setRowCount(count + 1)

        for i in range(len(column)):
            table.setItem(count, i, QtWidgets.QTableWidgetItem(str(row[i])))

def get_query_column(table):
    if(table == "SONG"):
        return ["song_id:string", "album_id:string", "Number:int", "Song:string"]

    elif(table == "ALBUM"):
        return ["album_id:string", "Name:string", "English:string", "Date:string", "Made:string", "Release:string", "Title:string"]

    elif(table == "MOVIE"):
        return ["movie_id:string", "Type:string", "Number:int", "Name:string", "song_id:string", "Year:int", "person_id"]

    elif(table == "CONCERT"):
        return ["concert_id:string", "Series:string", "Number:int", "Date:string", "place_id:string", "person_id:string"]

    elif(table == "PLACE"):
        return ["place_id:string", "Place:string", "Country:string", "City:string"]

    elif(table == "PERSON"):
        return ["person_id:string", "Name:string", "Sex:string"]


def get_command(query):
    if("INSERT" in query):
        return "INSERT"
    elif("DELETE" in query):
        return "DELETE"
    elif("UPDATE" in query):
        return "UPDATE"
    elif("EXISTS" in query):
        return "EXISTS"
    else:
        return ""


def clear_table(table):
    while(table.rowCount() > 0):
        table.removeRow(0)