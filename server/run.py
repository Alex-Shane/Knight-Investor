from flask import Flask, render_template, request  # Import flask
import daily_report as dr
import weekly_report as wr
import monthly_report as mr

app = Flask(__name__)  # Setup the flask app by creating an instance of Flask

@app.route('/')  # When someone goes to / on the server, execute the following function
def home():
    return render_template('index.html')  # Return index.html from the static folder

@app.route('/create_report')
def report_page():
    return render_template('report_page.html')

@app.route('/final_report', methods=['POST'])
def report():
    period = request.form['period']
    exchange = request.form['exchange']
    industry = request.form['industry']
    if period == 'month':
        if industry == 'None':
            context = mr.run(exchange)
        else:
            context = mr.run(exchange, industry)
        return render_template('output_monthly.html', **context)
    elif period == 'week':
        if industry == 'None':
            context = wr.run(exchange)
        else:
            context = wr.run(exchange, industry)
        return render_template('output_weekly.html', **context)
    else:
        if industry == 'None':
            context = dr.run(exchange)
        else:
            context = dr.run(exchange, industry)
        return render_template('output_daily.html', **context)
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':  # If the script that was run is this script (we have not been imported)
    app.debug = True
    app.run()  # Start the server