import flask
from flask import Flask, session, render_template,redirect, url_for
from run import server

@server.route('/')
def index():
    return render_template("tbases/t_index.html", startpage=True)

#@server.route('/dashboard/')
#def dashboard():
#    return render_template("tbases/t_index.html", startpage=True)