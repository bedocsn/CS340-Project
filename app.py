# Sample Flask application for a table top game database, snapshot of heros

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


app = Flask(__name__)

# database connection
# Template:
# app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
# app.config["MYSQL_USER"] = "cs340_OSUusername"
# app.config["MYSQL_PASSWORD"] = "XXXX" | last 4 digits of OSU id
# app.config["MYSQL_DB"] = "cs340_OSUusername"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# database connection info
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_OSUusername"
app.config["MYSQL_PASSWORD"] = "XXXX"
app.config["MYSQL_DB"] = "cs340_OSUusername"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes
# have homepage route to /index by default for convenience, generally this will be your home route with its own template
@app.route("/")
def home():
    return redirect("/index")


# route for heros page
@app.route("/heros", methods=["POST", "GET"])
def heros():
    # Separate out the request methods, in this case this is for a POST
    # insert a hero into the heros entity
    if request.method == "POST":
        # fire off if user presses the Add hero button
        if request.form.get("Add_hero"):
            # grab user form inputs
            heroName = request.form["heroName"]
            notebook = request.form["notebook"]

            # account for null notebook
            if notebook == "":
                # mySQL query to insert a new hero into heros with our form inputs
                query = "INSERT INTO heros (heroName) VALUES (%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (heroName))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO heros (heroName, notebook) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (heroName, notebook))
                mysql.connection.commit()

            # redirect back to heros page
            return redirect("/heros")

    # Grab heros data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the heros in heros
        query = "SELECT hero.heroID, heroName, notebook, player.playerID AS PlayerID, LEFT JOIN Player ON PlayerID = player.id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab planet id/name data for our dropdown
        query2 = "SELECT playerID, name FROM Player"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        player_data = cur.fetchall()

        # render edit_hero page passing our query data and player data to the edit_hero template
        return render_template("heros.j2", data=data, player=player_data)


# route for delete functionality, deleting a hero from Hero,
# we want to pass the 'id' value of that hero on button click (see HTML) via the route
@app.route("/delete_hero/<int:id>")
def delete_hero(heroID):
    # mySQL query to delete the hero with our passed id
    query = "DELETE FROM Hero WHERE heroID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (heroID,))
    mysql.connection.commit()

    # redirect back to hero page
    return redirect("/heros")


# route for edit functionality, updating the attributes of a hero in Hero
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_hero/<int:id>", methods=["POST", "GET"])
def edit_hero(heroID):
    if request.method == "GET":
        # mySQL query to grab the info of the hero with our passed id
        query = "SELECT * FROM Hero WHERE heroID = %s" % (heroID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab player id/name data for our dropdown
        query2 = "SELECT playerID, name FROM Player"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        player_data = cur.fetchall()

        # render edit_hero page passing our query data and player data to the edit_hero template
        return render_template("edit_hero.j2", data=data, players=playerlD_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Hero' button
        if request.form.get("Edit_Hero"):
            # grab user form inputs
            heroID = request.form["heroID"]
            heroName = request.form["heroName"]
            notebook = request.form["notebook"]
           

            # account for null notebook
            if (notebook == "" or notebook == "None"):
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE Hero SET Hero.heroName = %s, Hero.notebook = NULL"
                cur = mysql.connection.cursor()
                cur.execute(query, (heroName, heroID))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Hero SET Hero.heroName = %s, notebook = %s, WHERE Hero.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (heroName, notebook, heroId))
                mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/heros")


# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=2018, debug=True)
