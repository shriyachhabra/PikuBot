from flask import Flask, request, render_template
from pymessenger.bot import Bot
import os
from modules.jokes import *
from modules.wiki import *
from modules.quotes import *
from modules.start_convo import *
import json
from requests_toolbelt import MultipartEncoder

app = Flask(__name__)
ACCESS_TOKEN='EAAJrpa4jEQYBAFPZAndDzVZCKWDOdjZCGzz2pzNdVIbBkWFdbAKuZA2LQwyRNSFQNCpo7IZCGG0wb4G27ZAsoO9ZBf6pZALO7H9jxdgf6OzhT1gHpYHZCIuC27ucDQQor3YqZCoVFGGasHmDv4Wzd7n3QG8g3jVeqWwvsKsT7jV2cTkgZDZD'
# ACCESS_TOKEN1 = 'EAAGGClLVUZAcBAHmHU4mRdSXtSMCZCXTVOrQrbZBqp9LJKRw0wjtr9EFec5NOaougDZBm3XIcb4iwd77sc9KXIDMFYG1e20J1lDFoObxgFafIsZAiLF93mDnaJlFyed3foquAB0UzXCZAQjPA6TznlrBHG3GvUHZBJEVcAZABeYYSVLZBGsrNHmY2'
VERIFY_TOKEN = 'aaruchinu'
bot = Bot(ACCESS_TOKEN)
SRCDIR = os.path.dirname(os.path.abspath(__file__))

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
                if message['message'].get('attachments'):
                    response_sent_nontext = start_conversation()
                    send_message(recipient_id, response_sent_nontext)
                    return "non text response"
                msg=message['message'].get('text')
                txt = msg.split(' ', 1)
                if txt[0]=="/jokes":
                    response_sent_text =get_jokes()
                elif txt[0]=="/wiki":
                    if(len(txt)!=1):
                     response_sent_text=get_wiki(txt[1])
                    else:
                     response_sent_text="Follow the format:\n /wiki search_item"
                elif txt[0]=="/quotes":
                    response_sent_text=get_quotes()
                elif txt[0]=="/memes":
                    print(SRCDIR)
                    path = os.path.join(SRCDIR, 'meme.png')
                    resp = get_memes()
                    if resp == "done":
                        sendImg(recipient_id, path)
                        return "Message Processed"
                elif txt[0] in ["bye","goodbye"]:
                    response_sent_text="Bye :)"
                elif txt[0] in ["thanks","Thanks","wow","Aww","Nice","nice"]:
                    response_sent_text=":D"
                elif txt[0].lower()=="aaru":
                    response_sent_text="I love you my VALENTINE <3"
                elif txt[0].lower()=="meghu":
                    response_sent_text="I love you Bestie!!!! <3 <3"
                else :
                    response_sent_text=start_conversation()
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

def sendImg(recipient_id, image_path):

    params = {
        "access_token": ACCESS_TOKEN
    }
    data = {
        # encode nested json to avoid errors during multipart encoding process
        'recipient': json.dumps({
            'id': recipient_id
        }),
        # encode nested json to avoid errors during multipart encoding process
        'message': json.dumps({
            'attachment': {
                'type': 'image',
                'payload': {}
            }
        }),
        'filedata': (image_path, open('meme.png', 'rb'), 'image/png')
    }
    multipart_data = MultipartEncoder(data)
    multipart_header = {
        'Content-Type': multipart_data.content_type
    }

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params,
                      headers=multipart_header, data=multipart_data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)




if __name__ == '__main__':
    port=int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0',port=port)
    app.run(debug=True)
