from flask import Flask, request, jsonify
import os, uuid
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

            # Do something with the data (e.g., send it to a webhook or store it in a database)
    print("Azure Queue storage - Python quickstart sample")
        # Create a unique name for the queue
    #queue_name = "quickstartqueues-" + str(uuid.uuid4())
    queue_name = "testqueue"

    account_url = "https://saweuprparis.queue.core.windows.net"
    default_credential = DefaultAzureCredential()

    # Create the QueueClient object
    # We'll use this object to create and interact with the queue
    queue_client = QueueClient(account_url, queue_name=queue_name ,credential=default_credential)

    print("\nAdding messages to the queue...")

    # Send several messages to the queue
    queue_client.send_message(u"TEST MESSAGE")

except Exception as ex:
    print('Exception:')
    print(ex)


            # Respond with a success message
            return jsonify({"message": "Data received and processed successfully"})

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
                <input type="text" id="jobid" name="jobid" required><br><br>

                <label for="apikey">APIKey:</label>
                <input type="apikey" id="apikey" name="apikey" required><br><br>

                <label for="dest">Destination Path:</label>
                <textarea id="dest" name="dest" rows="1" required></textarea><br><br>

                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
