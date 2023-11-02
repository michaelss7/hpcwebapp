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
            
            queue_name = "rescaletransfer"
            account_url = "https://saweuprparis.queue.core.windows.net"
            default_credential = DefaultAzureCredential()
            queue_client = QueueClient(account_url, queue_name=queue_name ,credential=default_credential)
            data = jobid + ";" + apikey + ";" + dest + ";" + ss7email
            queue_client.send_message(data)

            # Respond with a success message
            return jsonify("Data received and sent to queue. You will be notified by email when data copy is complete")

        except Exception as e:
            return jsonify({"error": str(e)}), 500  # Respond with an error if something goes wrong

    # If the request is GET (initial page load)
    return '''
<!doctype html>
<html>

<head>
    <title>HPC Rescale Data Transfer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }

        .container {
            width: 50%;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        }

        h1 {
            color: #007BFF;
        }

        label,
        input {
            display: block;
            margin-bottom: 10px;
            text-align: left;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        input[type="submit"] {
            background-color: #007BFF;
            color: #fff;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 5px;
        }

        .help-text {
            color: #555;
            font-size: 14px;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>HPC Rescale Data Transfer</h1>
        <form method="post">
            <label for="jobid">JobID:</label>
            <input type="text" id="jobid" name="jobid" required placeholder="Rescale jobid">

            <label for="apikey">APIKey:</label>
            <input type="text" id="apikey" name="apikey" required placeholder="Rescale API Key" size="40">

            <label for="ss7email">Subsea7 email:</label>
            <input type="text" id="ss7email" name="ss7email" required placeholder="john.smith@subsea7.com">

            <label for="dest">Destination Path:</label>
            <input type="text" id="dest" name="dest" required placeholder="\\\\subsea7.net\\hpcdata\\pathtodata" size="40">
            <Form.Text id="dest" muted> Destination path is Case-Sensitive.</Form.Text>

            <input type="submit" value="Submit" size="40">
        </form>
    </div>
</body>

</html>

    '''

if __name__ == '__main__':
    app.run(debug=True)
