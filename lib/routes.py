from lib.server import app
from datetime import datetime
from flask import request, Request, Flask, flash, redirect, render_template, \
     request, url_for, send_from_directory, session
from lib.VampireSystem import VampireSystem
from lib.UserSystem import UserSystem
from lib.BloodSystem import BloodSystem
from lib.Search import Search
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
import json
import os

#notes: change system to VampireSystem and copy methods from seng2021

@app.route('/')
def welcome():
    loginstatus = False
    loginemployee = False
    if(UserSystem().check_login() == True):
        loginstatus = True
    if (UserSystem().check_employeeLogin() == True):
        loginemployee = True

    bloodTypes = ["A", "B", "AB", "O"]
	for type in bloodTypes:
		requestSent[type] = False
    VampireSystem  = VampireSystem
    #session['url'] = url_for('welcome')
    return render_template("welcome.html",loginstatus=loginstatus,loginemployee=loginemployee)

@app.route('/inventory', methods=['POST', 'GET'])
def inventory():
    # if (System().check_login() == False):
    #     session['url'] = url_for('inventory')
    #     remessy = "You were redirected to login"
    #     return redirect(url_for('login',remess=remessy))
    loginstatus = False
    loginemployee = False
    if(UserSystem().check_login() == True):
        loginstatus = True
    if (UserSystem().check_employeeLogin() == True):
        loginemployee = True

    if request.method == "POST":
        if "view_order" in request.form:
            order = request.form["view_order"]
            if order == "date_added":
                title = "View Inventory by Date Added"
                blood =  BloodSystem().sortBloodbyAddedDate()
            elif order == "expiry_date":
                title = "View Inventory by Expiry Date"
                blood = BloodSystem().sortBloodbyExpiryDate()
            elif order == "quantity":
                title = "View Inventory by Quantity"
                blood = BloodSystem().sortBloodbyQuantity()
            elif order == "blood_type":
                title = "View Inventory by Blood Type"
                blood = BloodSystem().getBloodQuantitybyType()
            return render_template("inventory.html", blood=blood, title=title,loginstatus=loginstatus,loginemployee=loginemployee)

        elif "delete" in request.form:
            index = int(request.form["delete"])
            BloodSystem().deletefromBloodInventory(index)
            expired_blood = BloodSystem().getExpiredBlood()
            return render_template("inventory.html", blood=expired_blood, title="Expired Blood",loginstatus=loginstatus,loginemployee=loginemployee)


    expired_blood = BloodSystem().getExpiredBlood()
    return render_template("inventory.html", blood=expired_blood, title="Expired Blood",loginstatus=loginstatus,loginemployee=loginemployee)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    email = ""
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        message = UserSystem().check_user(email, password)
        if message is "":
            print("LOGGED IN----")
            return redirect(url_for('welcome'))
        print("fail IN----")
        return render_template("login.html", message=message)
    return render_template("login.html", message=message)


@app.route('/delivered', methods=['GET', 'POST'])
def delivered():

    loginstatus = False
    loginemployee = False
    if(UserSystem().check_login() == True):
        loginstatus = True
    if (UserSystem().check_employeeLogin() == True):
        loginemployee = True

    #shows list of blood + respective action button
    deliveredBlood = VampireSystem().getDeliveredBlood()
    if request.method == "POST":
        if "add" in request.form:
            date = datetime.date(datetime.now())
            index = int(request.form['add'])
            #changed updating status to added, instead the input_date is added with the current date
            deliveredBlood[index].setInputDate(date)
            VampireSystem().updateInputDate(deliveredBlood[index])
            #dump to file, retrieve again
            deliveredBlood = VampireSystem().getDeliveredBlood()
        elif "send" in request.form:
            index = request.form['send']
            #coded for now: will change status to tested
            index = int(request.form['send'])
            deliveredBlood[index].setTestStatus("tested")
            VampireSystem().updateBloodStatus(deliveredBlood[index], "added")
    #when add is clicked: add to factory (change status to added) reload page
    #when send is clicked: delete from list OR change status to tested
    return render_template("delivered.html", deliveredBlood = deliveredBlood,loginstatus=loginstatus,loginemployee=loginemployee)

#  requests from medical facilities
@app.route('/requests', methods=['GET', 'POST'])
def requests():
    loginstatus = False
    loginemployee = False
    if(UserSystem().check_login() == True):
        loginstatus = True
    if (UserSystem().check_employeeLogin() == True):
        loginemployee = True
    mf_requests = VampireSystem().getMedicalFacilityRequests()
    #factoryBlood = BloodSystem().getFactoryBlood()
    if request.method == "POST":
        if "send" in request.form:
            index = int(request.form['send'])
            VampireSystem().updateDeliveredStatus(mf_requests[index],"yes")
            mf_requests = VampireSystem().getMedicalFacilityRequests()
        elif "decline" in request.form:
            index = int(request.form['decline'])
            VampireSystem().updateDeliveredStatus(mf_requests[index],"no")
            mf_requests = VampireSystem().getMedicalFacilityRequests()
    return render_template("requests.html",mf_requests = mf_requests,loginstatus=loginstatus,loginemployee=loginemployee)

@app.route('/warning', methods=['GET', 'POST'])
def warning():
    loginstatus = False
    loginemployee = False
    if(UserSystem().check_login() == True):
        loginstatus = True
    if (UserSystem().check_employeeLogin() == True):
        loginemployee = True

    lowBlood = BloodSystem().getLowBlood()
    normalBlood = BloodSystem().getNormalBlood()
    requestSent = Blood
    System().getRequestSent()
    if request.method == "POST":
        type = request.form['request']
        requestSent = BloodSystem().updateRequestSent(type)
    return render_template("warning.html", lowBlood = lowBlood,
    normalBlood = normalBlood, requestSent = requestSent ,loginstatus=loginstatus,loginemployee=loginemployee)


@app.route('/logout')
def logout():
    CurrentUser = UserSystem().get_username()
    message = ""
    message = UserSystem().logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    email = ""
    password = ""
    message = ""
    if request.method == 'POST':
        newemail = request.form["email"]
        newpassword = request.form["password"]
        newusername = request.form["username"]
        newname = request.form["name"]
        role = request.form["role"]

        print(role)
        if newemail is "" or newpassword is "" or newusername is "" or newname is "" :
            return render_template("signup.html", message="Complete all the fields in the form")
        check = UserSystem().check_username_unique(newusername)
        if check == 1:
            return render_template("signup.html",  message="This username is in use")
        check = UserSystem().check_email_unique(newemail)
        if check == 1:
            return render_template("signup.html",  message="This email is in use")
        UserSystem().create_user(newusername,newname,newemail, newpassword, role)

        # if 'url' in session:
        #     return redirect(session['url'])
        return redirect(url_for('welcome'))
    return render_template("signup.html",message="")

@app.route('/search', methods=['GET', 'POST'])
def search():
    factoryBlood = BloodSystem().getFactoryBlood()
    search = Search(factoryBlood)
    loginstatus = False
    loginemployee = False
    if(UserSystem().check_login() == True):
        loginstatus = True
    if (UserSystem().check_employeeLogin() == True):
        loginemployee = True
    if request.method == "POST":
        if 'A' in request.form:
            results = search.searchBloodType('A')
            return render_template("searchResults.html", results = results, searchtype = "blood type A", volume = 0,loginstatus=loginstatus,loginemployee=loginemployee)
        elif 'B' in request.form:
            results = search.searchBloodType('B')
            return render_template("searchResults.html", results = results, searchtype = "blood type B", volume = 0,loginstatus=loginstatus,loginemployee=loginemployee)
        elif 'AB' in request.form:
            results = search.searchBloodType('AB')
            return render_template("searchResults.html", results = results, searchtype = "blood type AB", volume = 0,loginstatus=loginstatus,loginemployee=loginemployee)
        elif 'O' in request.form:
            results = search.searchBloodType('O')
            return render_template("searchResults.html", results = results, searchtype = "blood type O", volume = 0,loginstatus=loginstatus,loginemployee=loginemployee)
        elif 'expirySubmit' in request.form:
            start = request.form['start']
            end = request.form['end']
            results = search.searchBloodExpiry(start, end)
            return render_template("searchResults.html", results = results, searchtype = "expiry dates between " + start + " - " + end, volume = 0,loginstatus=loginstatus,loginemployee=loginemployee)
        elif 'volumeSubmit' in request.form:
            minimum = request.form['minimum']
            maximum = request.form['maximum']
            results = search.searchBloodVolume(minimum, maximum)
            return render_template("searchResults.html", results = results, searchtype = "volumes between " + minimum + " - " + maximum, volume = 1,loginstatus=loginstatus,loginemployee=loginemployee)
    return render_template("searchResults.html",loginstatus=loginstatus,loginemployee=loginemployee)
