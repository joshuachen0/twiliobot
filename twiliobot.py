# ----------------------------------------------------------------------
# twiliobot - a bot made with Twilio to handle SMS<->Slack messages
# 
# SETUP:    Run 'ngrok http 5000' in terminal.
#           Copy https Forwarding URL.
#           Go to 'https://dev4slack.com/services/97863173554'.
#           In URL(s), paste '{https Forwarding URL}/slack'.
#           Go to 'https://www.twilio.com/console/phone-numbers/PN6f50d79181c4197afe56a8f81388e493'.
#           Under Messaging/A MESSAGE COMES IN, paste '{https Forwarding URL}/twilio'.
# RUN:      Run 'python twiliobot.py' in terminal.
# EXIT:     CTRL-C to exit twiliobot Flask app.
#           CTRL-C to exit ngrok.
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
os.environ["SLACK_WEBHOOK_SECRET"] = "MVJcsIsHGDncwxSgzDANXTxZ"
os.environ["TWILIO_NUMBER"] = "+15128722479"
os.environ["USER_NUMBER"] = "+19095364296"
os.environ["SLACK_TOKEN"] = "xoxp-4905231067-97348321795-97400019440-776ebfd86973a3dd78a5fb60cc2b9426"
os.environ["TWILIO_ACCOUNT_SID"] = "AC8c17488c62eefd798304f7ec903c98ec"
os.environ["TWILIO_AUTH_TOKEN"] = "2056f9386c091ef8be39ea0615486961"

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
