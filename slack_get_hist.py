from slack_sdk import WebClient
from reportlab.pdfgen import canvas
from datetime import datetime

# Create a WebClient instance with your API token
client = WebClient(token='')

# Define a list of channel names
channel_names = ['client-communication', 'payment-communication']

# Retrieve workspace information
response = client.auth_test()
if response["ok"]:
    workspace_name = response["team"]
    print(f"Workspace Name: {workspace_name}")
else:
    print(f"Error: {response['error']}")

# Iterate over each channel name
for channel_name in channel_names:
    # Call the API method to retrieve channel information by name
    response = client.conversations_list(types='public_channel,private_channel')
    if response["ok"]:
        channels = response["channels"]
        channel_id = None

        # Find the channel ID based on the channel name
        for channel in channels:
            if channel["name"] == channel_name:
                channel_id = channel["id"]
                break

        if channel_id:
            # Call the API method to retrieve channel history
            response = client.conversations_history(channel=channel_id)

            # Check if the API call was successful
            if response["ok"]:
                # Retrieve the list of messages
                messages = response["messages"]

                # Create a dictionary to store user names
                user_names = {}

                # Retrieve user names
                for message in messages:
                    user_id = message.get('user')
                    if user_id not in user_names:
                        user_info = client.users_info(user=user_id)
                        user_names[user_id] = user_info["user"]["real_name"]

                output_directory = "C:/Users/Muhammad Bilal/Desktop/"

                pdf_file_name = output_directory + f"{workspace_name}-{channel_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
                pdf = canvas.Canvas(pdf_file_name)

                # Set the initial y-coordinate for the first line
                y = 700

                # Add workspace name at the top of the PDF
                pdf.drawString(50, y, f"Workspace Name: {workspace_name}")
                y -= 20  # Adjust the y-coordinate for the next line

                # Print messages with user names
                for message in messages:
                    # Replace user ID with user name
                    user_id = message.get('user')
                    if user_id:
                        user_name = user_names.get(user_id)
                        if user_name:
                            message['user'] = user_name

                    # Add each message as a line in the PDF document
                    pdf.drawString(50, y, f"{message['user']}: {message['text']}")
                    y -= 15  # Adjust the y-coordinate for the next line

                # Save and close the PDF document
                pdf.save()

                print(f"Exported channel '{channel_name}' to PDF: {pdf_file_name}")
            else:
                # Print the error message if the API call failed
                print(f"Error: {response['error']}")
        else:
            print(f"Channel '{channel_name}' not found.")
    else:
        print(f"Error: {response['error']}")
else:
    print(f"Error: {response['error']}")
