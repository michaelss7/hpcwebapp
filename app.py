import os, uuid
from flask import Flask, request, jsonify
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage

app = Flask(__name__)

# Define a route for the web page
@app.route('/', methods=['GET', 'POST'])
def index():
    # If the request is POST (form submission)
    if request.method == 'POST':
        try:
            # Get data from the incoming request as form data
            jobid = request.form.get('jobid')
            apikey = request.form.get('apikey')
            dest = request.form.get('dest')
            ss7email = request.form.get('ss7email')
            

            # Do something with the data (e.g., send it to a webhook or store it in a database)
            
            queue_name = "testqueue"
            account_url = "https://saweuprparis.queue.core.windows.net"
            default_credential = DefaultAzureCredential()
            queue_client = QueueClient(account_url, queue_name=queue_name ,credential=default_credential)
            data = jobid + ";" + apikey + ";" + dest + ";" + ss7email
            queue_client.send_message(data)

            # Respond with a success message
            return jsonify({"message": "Data received and sent to queue. You will be notified by email when data copy is complete"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500  # Respond with an error if something goes wrong

    # If the request is GET (initial page load)
    return '''
        <!doctype html>
        <html>
        <head>
            <title>HPC Data Transfer</title>
        </head>
        <body>
            <h1>HPC Rescale Data Transfer</h1>
            <form method="post">
                <label for="jobid">JobID:</label>
                <input type="text" id="jobid" name="jobid" required placeholder="Rescale jobid"><br><br>

                <label for="apikey">APIKey:</label>
                <input type="text" id="apikey" name="apikey" required placeholder="Rescale API Key"><br><br>

                <label for="ss7email">Subsea7 email:</label>
                <input type="text" id="ss7email" name="ss7email" required placeholder="john.smith@subsea7.com"><br><br>

                <label for="dest">Destination Path:</label>
                <input type="text" id="dest" name="dest" required size="40" placeholder="\\\\subsea7.net\hpcdata\pathtodata"><br><br>

                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
