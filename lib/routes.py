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
    loginstatus = False
    loginemployee = False
    if(VampireSystem().check_login() == True):
        loginstatus = True
    if (VampireSystem().check_employeeLogin() == True):
        loginemployee = True
    #session['url'] = url_for('welcome')
    return render_template("welcome.html",loginstatus=loginstatus,loginemployee=loginemployee)

# #inventory
# @app.route('/inventory', methods=['POST', 'GET'])
# def inventory():

#         if (System().check_login() == False):
#             session['url'] = url_for('inventory')
#             remessy = "You were redirected to login"
#             return redirect(url_for('login',remess=remessy))
#     return render_template('inventory.html')

# @app.route('/login/<remess>', methods=['GET', 'POST'])
# def login(remess):
#     message = ""
#     email = ""
#     if request.method == 'POST':
#         email = request.form["email"]
#         password = request.form["password"]
#         message = System().check_user(email, password)
#         if message is "":
#             if 'url' in session:
#                 return redirect(session['url'])
#             return redirect(url_for('inventory', check = check))

#         return render_template("login.html", message=message,remessa="Welcome to the login page")
#     return render_template("login.html", message=message, remessa=remess)

@app.route('/login', methods=['GET', 'POST'])
def login():
    session['url'] = url_for('inventory')
    return render_template("welcome.html")


@app.route('/inventory', methods=['POST', 'GET'])
def inventory():
    # if (System().check_login() == False):
    #     session['url'] = url_for('inventory')
    #     remessy = "You were redirected to login"
    #     return redirect(url_for('login',remess=remessy))
    if request.method == "POST":
        if "view_order" in request.form:
            order = request.form["view_order"]
            if order == "date_added":
                title = "View Inventory by Date Added"
                blood =  VampireSystem().sortBloodbyAddedDate()
            elif order == "expiry_date":
                title = "View Inventory by Expiry Date"
                blood = VampireSystem().sortBloodbyExpiryDate()
            elif order == "quantity":
                title = "View Inventory by Quantity"                
                blood = VampireSystem().sortBloodbyQuantity()
            elif order == "blood_type":    
                title = "View Inventory by Blood Type"
                blood = VampireSystem().sortBloodbyType()
            return render_template("inventory.html", blood=blood, title=title)
        
        elif "delete" in request.form:
            index = int(request.form["delete"])
            VampireSystem().deletefromBloodInventory(index)
            expired_blood = VampireSystem().getExpiredBlood()
            return render_template("inventory.html", blood=expired_blood, title="Expired Blood")
    

    expired_blood = VampireSystem().getExpiredBlood()
    return render_template("inventory.html", blood=expired_blood, title="Expired Blood")

@app.route('/login/<remess>', methods=['GET', 'POST'])
def login(remess):
    message = ""
    email = ""
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        message = VampireSystem().check_user(email, password)
        if message is "":
            print("LOGGED IN----")
            return redirect(url_for('welcome'))
        print("fail IN----")
        return render_template("login.html", message=message)
    return render_template("login.html", message=message)


@app.route('/delivered', methods=['GET', 'POST'])
def delivered():
    #shows list of blood + respective action button
    deliveredBlood = VampireSystem().getDeliveredBlood()
    if request.method == "POST":
        if "add" in request.form:
            index = int(request.form['add'])
            deliveredBlood[index].setStatus("added")
            VampireSystem().updateBloodStatus(deliveredBlood[index], "added")
            #dump to file, retrieve again
            deliveredBlood = VampireSystem().getDeliveredBlood()
        elif "send" in request.form:
            index = request.form['send']
            #coded for now: will change status to tested
            index = int(request.form['send'])
            deliveredBlood[index].setStatus("tested")
            VampireSystem().updateBloodStatus(deliveredBlood[index], "added")
    #when add is clicked: add to factory (change status to added) reload page
    #when send is clicked: delete from list OR change status to tested
    return render_template("delivered.html", deliveredBlood = deliveredBlood)

#  requests from medical facilities
@app.route('/requests')
def requests():
    mf_requests = VampireSystem().getMedicalFacilityRequests()
    return render_template("requests.html",mf_requests = mf_requests)

@app.route('/warning', methods=['GET', 'POST'])
def warning():
    lowBlood = VampireSystem().getLowBlood()
    normalBlood = VampireSystem().getNormalBlood()
    requestSent = VampireSystem().getRequestSent()
    if request.method == "POST":
        type = request.form['request']
        requestSent = VampireSystem().updateRequestSent(type)
    return render_template("warning.html", lowBlood = lowBlood,
    normalBlood = normalBlood, requestSent = requestSent)


@app.route('/logout')
def logout():
    CurrentUser = VampireSystem().get_username()
    message = ""
    message = VampireSystem().logout_user()
    return redirect(url_for('login'))
