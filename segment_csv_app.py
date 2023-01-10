import requests
import pandas as pd
import base64
from flask import Flask, request, render_template, make_response, redirect, flash

app = Flask(__name__)

# Set the secret key
app.secret_key = 'your-secret-key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_messages', methods=['POST'])
def send_messages():
    try:
        # Retrieve the uploaded file and write key from the request object
        csv_file = request.files['csv_file']
        write_key = request.form['write_key']

        # Base64-encode the write key
        write_key_b64 = base64.b64encode(write_key.encode('utf-8')).decode('utf-8')

        # Read in the CSV file using Pandas
        df = pd.read_csv(csv_file)

        # Get the names of all the columns in the CSV file
        column_names = df.columns.tolist()

        # Iterate over the rows of the CSV file and send a message for each row using the Segment API
        for index, row in df.iterrows():
            # Create an empty dictionary to store the properties
            properties = {}

            # Iterate over the columns and add the values to the properties dictionary
            for column in column_names:
                if column != 'user_id':
                    properties[column] = row[column]

            # Send the message using the Segment API
            requests.post('https://api.segment.io/v1/identify', json={
                'userId': row['user_id'],
                'traits': properties
            }, headers={
                'Authorization': 'Basic ' + write_key_b64,
                'Content-Type': 'application/json'
            })

        # Display a prompt message to the user
        return render_template('index.html', alert='Messages successfully sent to Segment!')

    except Exception as e:
        # If an error occurs, display an alert to the user
        return render_template('index.html', alert='An error occurred while sending messages to Segment: {}'.format(e))