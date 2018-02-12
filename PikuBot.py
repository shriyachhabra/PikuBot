from flask import Flask, request, render_template
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAAGGClLVUZAcBAHmHU4mRdSXtSMCZCXTVOrQrbZBqp9LJKRw0wjtr9EFec5NOaougDZBm3XIcb4iwd77sc9KXIDMFYG1e20J1lDFoObxgFafIsZAiLF93mDnaJlFyed3foquAB0UzXCZAQjPA6TznlrBHG3GvUHZBJEVcAZABeYYSVLZBGsrNHmY2'
VERIFY_TOKEN = 'aaruchinu'
bot = Bot(ACCESS_TOKEN)

@app.route('/',methods=['POST'])
def post_request_func():
    # if the request was not get, it must be POST and we can just proceed with sending a message # back to user

    # get whatever message a user sent the bot
    output = request.get_json()
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            print (message)
            if message.get('message'):
                # Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text ="hi"
                    send_message(recipient_id, response_sent_text)


    return "Message Processed"

@app.route('/',methods=['GET'])
def receive_mssg():
    """Before allowing people to message your bot, Facebook has implemented a verify token
           that confirms all requests that your bot receives came from Facebook."""
    token_sent = request.args.get("hub.verify_token")
    return verify_fb_token(token_sent)

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == '__main__':
    app.run()
