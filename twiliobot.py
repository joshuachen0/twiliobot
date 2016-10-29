# ----------------------------------------------------------------------
# twiliobot - a bot made with Twilio to handle SMS<->Slack messages
# ----------------------------------------------------------------------

# Used to get environment variables
import os
# Flask to instantiate app; request/Response for HTTP input/responses
from flask import Flask, request, Response
# Used to create slack client object
from slackclient import SlackClient
# Twilio helper library imports to generate TwiML and send texts
from twilio import twiml
from twilio.rest import TwilioRestClient

# Set environment variables
if "TWL_SLK_FLAG" not in os.environ or os.environ["TWL_SLK_FLAG"] != "1":
	os.environ["TWL_SLK_FLAG"] = "1"
	os.environ["SLACK_WEBHOOK_SECRET"] = input("Enter your Slack webhook:\t")
	os.environ["TWILIO_NUMBER"] = input("Enter your Twilio number:\t")
	os.environ["USER_NUMBER"] = input("Enter the user's number:\t")
	os.environ["SLACK_TOKEN"] = input("Enter your Slack account token:\t")
	os.environ["TWILIO_ACCOUNT_SID"] = input("Enter your Twilio account SID:\t")
	os.environ["TWILIO_AUTH_TOKEN"] = input("Enter your Twilio auth token:\t")

# Get environment variables for Twilio and user number
SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET', None)
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', None)
USER_NUMBER = os.environ.get('USER_NUMBER', None)

# Instantiate Flask app
app = Flask(__name__)
# Create slack client object using slack token from environment variable
slack_client = SlackClient(os.environ.get('SLACK_TOKEN', None))
# Create twilio client pulls environment variables automatically
twilio_client = TwilioRestClient()

# Indicates that the app's route and method of request : twilio
@app.route('/twilio', methods=['POST'])
# This function handles incoming HTTP POST request
def twilio_post():
    response = twiml.Response()
    # Test to see if request is from the correct number
    if request.form['From'] == USER_NUMBER:
        message = request.form['Body']
        # Post message to Slack
        slack_client.api_call("chat.postMessage", channel="#publicjg",
                              text=message, username='twiliobotjg',
                              icon_emoji=':robot_face')
    return Response(response.toxml(), mimetype="text/xml"), 200
    
# Indicates that the app's route and method of request : slack
@app.route('/slack', methods=['POST'])
# This function handles incoming HTTP POST request
def slack_post():
    # Test if the token matches the webhook
    if request.form['token'] == SLACK_WEBHOOK_SECRET:
        # Get the channel, username, and text of message
        channel = request.form['channel_name']
        username = request.form['user_name']
        text = request.form['text']
        # Format the message's characteristics
        response_message = ''.join((username, " in ", channel,
                                    " says: ", text));
        # Send message to user number from twilio number
        twilio_client.messages.create(to=USER_NUMBER, 
                                      from_=TWILIO_NUMBER,
                                      body=response_message)
    return Response(), 200

# Default testing for app
@app.route('/', methods=['GET'])
def test():
    return Response('It works!')

# Run app automatically
if __name__ == '__main__':
    app.run(debug=True)
