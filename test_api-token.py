import os
from slackclient import SlackClient

# Create slack client object using api-token from environment variables
slack_client = SlackClient(os.environ.get('SLACK_TOKEN', None))

# Run two built-in tests for the slack client 
message1=slack_client.api_call("api.test")
message2=slack_client.api_call("auth.test")
# Print pass-fail messages
if 'ok' in message1 and message1['ok'] == True:
	print('api.test\tPASS')
else:
	print('api.test\tFAIL')
if 'ok' in message2 and message2['ok'] == True:
	print('auth.test\tPASS')
else:
	print('auth.test\tFAIL')
