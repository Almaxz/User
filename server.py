from flask import Flask, render_template, request, redirect, session

from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/users")

@app.route("/users/new")
def new_users():
    return render_template("new_user.html")

@app.route("/users/create", methods = ["POST"])
def create_users():
    mysql = connectToMySQL('users')
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s,%(em)s, NOW(), NOW());"
    data = {
        "fn": request.form["f_name"],
        "ln": request.form["l_name"],
        "em": request.form["email"]
    }
    new_user_id = mysql.query_db(query, data)
    return redirect(f"/users/{new_user_id}")

@app.route("/users/<id>")
def user_id(id):
    mysql = connectToMySQL('users')
    query = "SELECT * from users where id = %(id)s"
    data = {
        "id": id
    }
    user = mysql.query_db(query, data)
    return render_template("user_info.html", user = user[0])

@app.route("/users")
def users():
    mysql = connectToMySQL('users')
    users = mysql.query_db('SELECT * FROM users;')
    return render_template("users.html", all_users = users)

@app.route("/users/<id>/edit")
def edit_user(id):
    mysql = connectToMySQL('users')
    query = "SELECT * from users where id = %(id)s"
    data = {
        "id": id
    }
    user = mysql.query_db(query, data)
    return render_template("edit_user.html", user = user[0])

@app.route("/users/<id>/update", methods = ["POST"])
def update_users(id):
    mysql = connectToMySQL('users')
    query = "UPDATE users SET first_name = '%(fn)s', last_name = '%(ln)s', email = '%(em)s', updated_at= NOW() WHERE (id = '%(id)s');"
    data = {
        "id": id,
        "fn": request.form["f_name"],
        "ln": request.form["l_name"],
        "em": request.form["email"]
    }
    updated_user_id = mysql.query_db(query, data)
    return redirect(f"/users/{updated_user_id}")

if __name__ == "__main__":
    app.run(debug=True)
