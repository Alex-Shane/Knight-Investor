from flask import Flask, render_template  # Import flask
from daily_report import daily_report as dr
from weekly_report import weekly_report as wr
from monthly_report import monthly_report as mr

app = Flask(__name__)  # Setup the flask app by creating an instance of Flask

@app.route('/')  # When someone goes to / on the server, execute the following function
def home():
    return render_template('index.html')  # Return index.html from the static folder

@app.route('/monthly_report')
def monthly_report():
    return render_template('monthly_report.html')

@app.route('/weekly_report')
def weekly_report():
    return render_template('weekly_report.html')

@app.route('/daily_report')
def daily_report():
    return render_template('daily_report.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':  # If the script that was run is this script (we have not been imported)
    app.debug = True
    app.run()  # Start the server