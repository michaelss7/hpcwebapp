from azure.identity import DefaultAzureCredential

import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage

try:
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
