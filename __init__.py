from flask import Flask, render_template, redirect, url_for, request, session, flash
import json


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'