from flask import Flask, render_template, redirect, request
from table_connect import TableConnect
import calendar
import datetime

date_today = calendar.datetime.date.today()

app = Flask(__name__)

tc = TableConnect("localhost", "root", "", "wbr")

# Function to calculate the days from now till the due date of the item
def remaining_days():
    data = tc.viewTasks()
    days = []
    current = datetime.datetime.today().date()
    for each in data:
        due_date = each[3]
        remaining = due_date - current
        days.append(remaining.days)
    return days

# Function to go to the main page
@app.route("/")
def index():
    return render_template("index.html")

# Function to get the list of all items in the table from the database
@app.route("/view")
def viewItem():
    try:
        data = tc.viewTasks()
        days = remaining_days()
        return render_template("index.html", all_tasks=data, days=days, view=True)
    except:
        return render_template("index.html", view=False, no_table=True)

# Function to add an item to the database
@app.route("/add", methods=["GET", "POST"])
def addItem():
    try:
        remaining_days()
        if request.method == "POST":
            task = request.form["task"]
            description = request.form["description"]
            
            due_date = request.form["date"]
            converted = datetime.datetime.strptime(due_date, '%Y-%m-%d').date()
            
            if tc.insertTask(task, description, converted):
                return render_template("index.html", added=True, view=False)
            else:
                return "Error"
        else:
            return render_template("add.html", date_today=date_today)
    except:
        return render_template("error.html", no_table=True) 

# Will delete an item, or go to the page where user can update an item
@app.route("/gettask/<perform>", methods=["POST"])
def getTask(perform):
    perform_task = perform
    task = request.form["task"]
    days = remaining_days()
    if tc.selectTask(task):
        data = tc.selectTask(task)
        if perform_task == "update":
            return render_template("updatetask.html", task_info = data[0])
        elif perform_task == "delete":
            tc.deleteTask(task)
            return render_template("index.html", deleted=True, view=False)
    else:
        data = tc.viewTasks()
        return render_template(perform_task + ".html", all_tasks=data, error=True, days=days)

# Will go to the update page
@app.route("/update")
def update():
    try:
        data = tc.viewTasks()
        days = remaining_days()
        return render_template("update.html", all_tasks = data, days=days)
    except:
        return render_template("error.html", no_table=True)

# Will update the item after user has made the changes
@app.route("/updatetask/<task_id>", methods=["GET", "POST"])
def updateItem(task_id):
    data = tc.viewTasks()
    if request.method == "POST":
        id = int(task_id)
        description = request.form["description"]
        
        due_date = request.form["date"]
        converted = datetime.datetime.strptime(due_date, '%Y-%m-%d').date()

        if tc.updateTask(id, description, converted):
            return render_template("index.html", updated=True, view=False)
        else:
            return "Error"
    else:
        return render_template("update.html", all_tasks = data)

# Function to delete an item
@app.route("/delete", methods=["GET", "POST"])
def deleteItem():
    try:
        data = tc.viewTasks()
        days = remaining_days()
        return render_template("delete.html", all_tasks = data, days=days)
    except:
        return render_template("error.html", no_table=True)


if __name__ == "__main__":
    app.run(debug=True)