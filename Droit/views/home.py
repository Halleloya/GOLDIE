from flask import Blueprint, render_template

home = Blueprint('home', __name__)

@home.route('/')
@home.route('/index')
@home.route('/home')
def index():
    """Render the home page for the project

    Returns:
        response: the flask response object representing the HTML page
    """
    return render_template("home/index.html")

@home.route('/about')
def about():
    """Render the abount page for the project

    Returns:
        response: the flask response object representing the HTML page
    """
    return render_template("home/about.html")

@home.route('/contact')
def contact():
    """Render the contact page for the project

    Returns:
        response: the flask response object representing the HTML page
    """
    return render_template("home/contact.html")
