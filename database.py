import sqlite3

def createTable():

    db = sqlite3.connect('Database.db')
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        filePath TEXT NOT NULL,
        imgPath TEXT NOT NULL
    )

    """)

    db.commit()
    db.close()

def insertProgram(name, path):
    db = sqlite3.connect('Database.db')
    cursor = db.cursor()

    default_img = 'Covers/unknown.png'

    cursor.execute('INSERT INTO data (name, filePath, imgPath) VALUES (?,?,?)',(name,path,default_img))

    db.commit()
    db.close()

def deleteProgram(path):
    db = sqlite3.connect('Database.db')
    cursor = db.cursor()

    cursor.execute('DELETE FROM data WHERE filePath = ?', (path,))

    db.commit()
    db.close()

def getAllPrograms():
    db = sqlite3.connect('Database.db')
    cursor = db.cursor()

    cursor.execute("SELECT * FROM data")
    rows = cursor.fetchall()

    db.close()
    
    return rows

def defImg(exePath, imgPath):
    db = sqlite3.connect('Database.db')
    cursor = db.cursor()

    cursor.execute('UPDATE data SET imgPath = ? WHERE filePath = ?', (imgPath,exePath))

    db.commit()
    db.close()