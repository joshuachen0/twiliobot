# twiliobot

a bot made with Twilio to handle SMS<->Slack messages.

link to referenced tutorial: https://www.twilio.com/blog/2016/05/build-sms-slack-bot-python.html.



### SETUP:

1. Setup virtulenv and run 'pip install -r requirements.txt' to install required packages in secure environment.

2. Download and unzip ngrok. Run 'mv ngrok /usr/local/bin' to run ngrok directly from command line.

3. Run 'ngrok http 5000' in terminal.

4. Copy https Forwarding URL.

5. Go to 'https://dev4slack.com/services/97863173554'.

6. In URL(s), paste '{https Forwarding URL}/slack'.

7. Go to 'https://www.twilio.com/console/phone-numbers/PN6f50d79181c4197afe56a8f81388e493'.

8. Under Messaging/A MESSAGE COMES IN, paste '{https Forwarding URL}/twilio'.



### RUN: 

1. Run 'python twiliobot.py' in terminal.



### EXIT: 

1. CTRL-C to exit twiliobot Flask app.

2. CTRL-C to exit ngrok.
