from lib.server import app
from flask import request, Request, Flask, flash, redirect, render_template, \
     request, url_for, send_from_directory, session
from lib.VampireSystem import VampireSystem
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
import json
import os

#notes: change system to VampireSystem and copy methods from seng2021

@app.route('/')
def welcome():
    session['url'] = url_for('inventory')
    return render_template("welcome.html")

#inventory
@app.route('/inventory', methods=['POST', 'GET'])
def inventory():
    if (System().check_login() == False):
        session['url'] = url_for('inventory')
        remessy = "You were redirected to login"
        return redirect(url_for('login',remess=remessy))
    return render_template('inventory.html')

@app.route('/login/<remess>', methods=['GET', 'POST'])
def login(remess):
    message = ""
    email = ""
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        message = VampireSystem().check_user(email, password)
        if message is "":
            if 'url' in session:
                return redirect(session['url'])
            return redirect(url_for('inventory', check = check))

        return render_template("login.html", message=message,remessa="Welcome to the login page")
    return render_template("login.html", message=message, remessa=remess)

@app.route('/delivered')
def delivered():
    #shows list of blood + respective action button
    deliveredBlood = VampireSystem().getDeliveredBlood()
    testedBlood = VampireSystem().getTestedBlood()
    notTestedBlood = VampireSystem().getNotTestedBlood()
    return render_template("delivered.html", deliveredBlood = deliveredBlood)

@app.route('/warning')
def warning():
    return render_template("warning.html")

@app.route('/requests')
def requests():
    return render_template("requests.html")

@app.route('/logout')
def logout():
    CurrentUser = System().get_username()
    message = ""
    message = System().logout_user()
    return redirect(url_for('login',remess="Welcome back to the login page"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("signup.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template("searchResults.html")


@app.route('/otherProfile/<user>', methods = ['POST', 'GET'])
def otherProfile(user):
    if (System().check_login() == False):
        session['url'] = url_for('otherProfile', user = user)
        remessy = "You were redirected to login"
        return redirect(url_for('login',remess=remessy))
    User = System().get_user(user)
    CurrentUser = System().get_username()
    return render_template("otherProfile.html", User = User)

@app.route('/profile', methods = ['POST', 'GET'])
def profile():
    if (System().check_login() == False):
        session['url'] = url_for('profile')
        remessy = "You were redirected to login"
        return redirect(url_for('login',remess=remessy))
    CurrentUser = System().get_username()
    user = System().get_user(CurrentUser)
    return render_template("profile.html", user = user)


#end
