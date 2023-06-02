'''
This is the main application file. It contains the Flask app and the routes.
'''

from flask import Flask, render_template, make_response, request
import os
import configparser
from app import plotter
from app import data_operations as dOps

app: Flask = Flask(__name__, 
                   template_folder='/root/take_home_project/app/templates', 
                   static_folder='/root/take_home_project/app/static/'
                )

# This is the main route of the web application
@app.route('/')
def hello() -> str:

    # Fetch the start_time and end_time from the URL parameters
    start_time: str = request.args.get('start_time')
    end_time: str = request.args.get('end_time')

    # Fetch the data from the database
    allData = dOps.fetch_data(start_time, end_time)

    # Plot the data
    fig_plot = plotter.plot_data(allData)

    # Convert the plot to HTML
    plot_html: str = fig_plot.to_html(full_html=False)

    # Render the HTML template
    return render_template('index.html', plot=plot_html)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This route is used to download the data as a CSV file
@app.route('/csv')
def download_csv():

    # Fetch the start_time and end_time from the URL parameters
    start_time: str = request.args.get('start_time')
    end_time: str = request.args.get('end_time')
    
    # Fetch the data from the database
    csv_string: str = dOps.fetch_data_DF(start_time, end_time)

    
    # Create a response object with the CSV data and set the headers
    response = make_response(csv_string) 
    response.headers['Content-Disposition'] = 'attachment; filename=Plots.csv'
    response.headers['Content-Type'] = 'text/csv'

    return response

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This function is used to run the webserver at port 8888 
# and listen to all IP addresses
def run_webserver() -> None:
    app.run(debug=True, host='0.0.0.0', port=8888)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This function is used to load the environment variables from the .env file
def init_env() -> None:

    # Read the environment variables from the .env file
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read("../local.env")

    # Set the environment variables
    for section in config.sections():
        for key, value in config.items(section):
            os.environ[key] = value

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This is the main function
def main() -> None:

    # Initialize the environment variables
    init_env()

    # Run the webserver
    run_webserver()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
