import os
import sqlite3
import pandas as pd

from flask import Flask, g, render_template, request

app = Flask(__name__)

# Delete the database file if it exists
# if os.path.exists("messages_db.sqlite"):
#     os.remove("messages_db.sqlite")
  

def get_message_db():
    try:
        return g.message_db
    except AttributeError:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cursor = g.message_db.cursor()
        
        # Create the messages table if it doesn't exist
        cmd = 'CREATE TABLE IF NOT EXISTS messages (name TEXT, message TEXT);'
        cursor.execute(cmd)
        g.message_db.commit()
        
        return g.message_db

def insert_message(request):
    message = request.form['message']
    name = request.form["name"]
    db = get_message_db()
    cursor = db.cursor()
    print("here")
    cursor.execute('INSERT INTO messages (name, message) VALUES (?, ?)', (name, message))
    db.commit()
    cursor.close()
    db.close()
    return message, name

def random_messages(n):
    db = get_message_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM messages ORDER BY RANDOM() LIMIT ?", (n,))
    random_messages = cursor.fetchall()

    db.close()

    return random_messages




#Route to render the home page
@app.route('/')
def home():
    return render_template('base.html')

# Route to render the submit page
@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        insert_message(request)
        return render_template('submit.html')
    
@app.route('/view')
def view():
    try:
        messages = random_messages(5)
        return render_template('view.html', messages=messages)
    except:
        return render_template

if __name__ == '__main__':
    app.run(debug=True)