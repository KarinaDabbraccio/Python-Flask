# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 19:33:45 2021

@author: Karina
"""
from datetime import datetime
import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash
import files


app = Flask(__name__)
app.secret_key = 'Karina'


FORMAT = '%(asctime)-15s :  %(message)s'
logging.basicConfig(filename='record.log', format=FORMAT, datefmt = '%y-%m-%d %H:%M:%S')

logging.disable(logging.WARNING)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    """App route for the login page"""
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        allow_login, msg = files.login(username, password)
        flash(msg)
        if allow_login:
            session['loggedin'] = True
            session['id'] = username
            session['username'] = username
            msg = 'Logged in as ' + username
            app.logger.error(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) +
                               ' : logged in successfully: %s ', username)
            #return redirect(url_for('index'))
            return index()
        else:
            app.logger.error(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) +
                               ' : !!!! failed to log in : %s', username)
            #datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    return render_template('login.html')


@app.route('/logout')
def logout():
    """App route for the logout, to show login page if no user is logged in"""
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/update_pwd', methods =['GET', 'POST'])
def update_pwd():
    """App route for the password update, LAB 8"""

    if not session.get('loggedin'):
        return render_template('login.html')

    msg = ''
    if request.method == 'POST':
        password = request.form['password']
        repeat_pwd = request.form['repeat_pwd']
        if not password == repeat_pwd:
            msg = ' not updated. Repeat the password correctly'
        else:
            msg = files.update(session['username'], password)
        flash(msg)
    return render_template('update_pwd.html',
                           username = session['username'],
                           title = "password update")


@app.route('/register', methods =['GET', 'POST'])
def register():
    """App route for the register page"""
    title = "REGISTER"
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        msg = files.register(username, password)
        flash(msg)

    return render_template('register.html', title = title)

@app.route('/index')
def index():
    """Page1 - main page, doesn't have its route now, rendered after login,
    the function sets the variables values - date, urls - for the page"""

    nav = [
        {'name': 'Christmas menu',
         'url': 'https://theculturetrip.com/europe/ukraine/articles/what-do-ukrainians-eat-for-christmas/'},
        {'name': 'Traditional dishes',
         'url': 'https://theculturetrip.com/europe/ukraine/articles/12-traditional-ukrainian-dishes-you-must-try/'},
        {'name': 'Places on Tripadvisor',
         'url': 'https://www.tripadvisor.com/Restaurants-g294474-Kyiv_Kiev.html'}
    ]

    date = datetime.now()
    dtt = date.strftime("%Y-%m-%d %H:%M:%S")
    if session.get('loggedin'):
        msg = 'Logged in as ' + session['username']
        return render_template('index.html',title = "DAbbr-home", dtt= dtt, msg = msg, nav=nav)
    else:
        return render_template('login.html', msg = 'Login before viewing this page')


@app.route('/casual')
def casual():
    """Page2 -  casual meals."""

    if session.get('loggedin'):
        return render_template('casual.html',title = "DAbbr-casual")
    else:
        return redirect(url_for('login'))
        #render_template('login.html', msg = 'Login before viewing this page')


@app.route('/special')
def special():
    """Page3 - special event meals."""

    # this is ordered list on the page
    oli = ['Appetizers and a little drinking.',
          'Some hot meals, depends on event, and more alcohol can be taken.',
          'Leftovers of appetizers, drinking and mostly talking bacase should be already full.',
          'Might be more hot meals.',
          'Leftovers of appetizers, drinking and mostly talking bacase should be already full.',
          'In fact, not everyone may still be there for the desert.']
    if session.get('loggedin'):
        return render_template('special.html',oli = oli, title = "DAbbr-special")
    else:
        return render_template('login.html', msg = 'Login before viewing this page')


if __name__ == '__main__':
    #app.run()
    # or this to debug:
    app.run(debug = True)
