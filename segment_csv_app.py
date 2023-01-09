import requests
import pandas as pd
import base64
from flask import Flask, request, render_template, make_response, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_messages', methods=['POST'])
def send_messages():
    # Retrieve the uploaded file and write key from the request object
    csv_file = request.files['csv_file']
    write_key = request.form['write_key']

    # Base64-encode the write key
    write_key_b64 = base64.b64encode(write_key.encode('utf-8')).decode('utf-8')

    # Read in the CSV file using Pandas
    df = pd.read_csv(csv_file)

    # Iterate over the rows of the CSV file and send a message for each row using the Segment API
    for index, row in df.iterrows():
        message = row['message']
        user_id = row['user_id']

        payload = {
            'userId': user_id,
            'traits': {
                'message': message
            }
        }
        requests.post('https://api.segment.io/v1/identify', json=payload, headers={
            'Authorization': 'Basic ' + write_key_b64,
            'Content-Type': 'application/json'
        })

    # Redirect the user's browser to the index page
    return redirect('/')

if __name__ == '__main__':
    app.run()
