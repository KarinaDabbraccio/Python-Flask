# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 17:25:03 2021

@author: Karina
"""

import os
import csv
import re
from passlib.hash import sha256_crypt

def read_users(nam, pas):
    """Read users from file, helper for login and registration"""
    # user exists and pwd is valid
    exists = False
    valid_pwd = False
    with open('usersc.csv', 'r',   newline='') as users:
        reader = csv.reader(users)
        for record in reader:
            name, hashed_pwd = record
            #if name == nam and passw == pas:
            if name == nam and sha256_crypt.verify(pas, hashed_pwd):
                exists = True
                valid_pwd = True
            #elif name == nam and passw != pas:
            elif name == nam and not sha256_crypt.verify(pas, hashed_pwd):
                exists = True
                valid_pwd = False
    return exists, valid_pwd

def passwd_val(passwd):
    """Helper for registration, validate the password
    for 12 to 20, symbols, upeer-lower-case, numbers"""
    #passwd = 'Aqqsdf1@2'
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{12,20}$"
    # compiling regex
    pat = re.compile(reg)
    # searching regex
    mat = re.search(pat, passwd)
    # validating conditions
    if mat:
        return True
    else:
        return False

def update(name, password):
    """ check complexity from previous labs,
    prohibit new pwd is the same as old, check list of bad pwds"""
    msg = ''

    found = False
    # check complexity lab-7 criteria
    valid_pwd = passwd_val(password)
    #compare with old
    exists, old_pwd = read_users(name, password)
    #compare to list provided
    with open('CommonPasswords.txt', 'r') as cpass:
        for pwrd in cpass:
            if pwrd.strip() == password:
                found = True
                msg += 'Password is in the list of common passwords.  '
                break

    # do msg+= to show all reasons together
    if not valid_pwd:
        msg += 'Password complexity is wrong.'
    if old_pwd:
        msg += 'New pasword should differ from the old one.'
    if not found and not old_pwd and valid_pwd:
        #everything is ok, update in the file
        update_csv(name,password)
        msg += "Updated"
    return msg

def update_csv(username, password):
    """Processing of the update the password in scv file -
    takes username and new password to update the entry"""
    passw= sha256_crypt.hash(password)

    with open('usersc.csv', 'r',   newline='') as accounts:
        reader = csv.reader(accounts)
        for record in reader:
            nam, pas = record
            if not nam == username:
                with open('temp.csv', mode='a',   newline='') as temp:
                    writer = csv.writer(temp)
                    writer.writerow([nam, pas])
            else:
                with open('temp.csv', mode='a',   newline='') as temp:
                    writer = csv.writer(temp)
                    writer.writerow([username, passw])

    os.remove('usersc.csv')
    os.rename('temp.csv',   'usersc.csv')


def register(name, passw):
    """nuser registration, receives name and password, validates them and retuns
    if registration is successful - written to the file the new user,
    or failed, and error message"""
    #name = input('Enter name: ')
    #passw = input('Enter passw: ')
    if not name:
        msg = 'Please enter your Username.'
    elif not passw:
        msg = 'Please enter your Password.'
    # check name
    elif len(name) > 20 or len(name) < 3:
        msg = 'Name length is 3 to 20 letters or numbers'
    elif not re.match(r'[A-Za-z0-9]*$', name):
        msg = 'Name includes numbers and letters only'
    elif not passwd_val(passw):
        msg = 'The password complexity is wrong'
        #print(msg)
    else:
        exists, valid_pwd = read_users(name, passw)
        if exists:
            msg = 'User ' + name + ' alsready exists'
        else:
            #hash pwd before storage
            passw = sha256_crypt.hash(passw)
            #save to file new user
            with open('usersc.csv', mode='a',   newline='') as users:
                writer = csv.writer(users)
                writer.writerow([name, passw])
                msg = 'Registered: ' + name

    return msg


def login(name, passw):
    """Login the user, receives name and password,
    returns bool to allow if valis, and error message"""
    #name = input('Enter name: ')
    #passw = input('Enter passw: ')
    exists = False
    valid_pwd = False
    allow_login = False
    if not name:
        msg = 'Please enter your Username'
        return allow_login, msg
    elif not passw:
        msg = 'Please enter your Password'
        return allow_login, msg
    else:
        #find if user and pwd are in the file
        exists, valid_pwd = read_users(name, passw)


    if exists and valid_pwd:
        allow_login = True
        msg = ''
    elif not exists:
        msg = 'User doesnt exist'
    elif exists and not valid_pwd:
        msg = 'Invalid password'

    return allow_login, msg
