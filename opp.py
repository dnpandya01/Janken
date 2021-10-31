from flask import Flask, render_template, Response
from camera import VideoCamera
from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import time
import keyboard

app = Flask(__name__)

out = ""
number2 = ""
pnconfig = PNConfiguration()
pnconfig.publish_key = 'pub-c-4bab4754-fea9-47a4-ab78-9433e78fbd72'
pnconfig.subscribe_key = 'sub-c-c4d48294-38a6-11ec-b886-526a8555c638'
pnconfig.ssl = True
pubnub = PubNub(pnconfig)


def my_publish_callback(envelope, status):
            # Check whether request successfully completed or not
            if not status.is_error():
                pass
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
    def status(self, pubnub, status):
        pass
    def message(self, pubnub, message):
        global number2
        number2 = message.message
        print("Opponent: " + message.message)
        
        
mylistener = MySubscribeCallback()
mylistener2 = MySubscribeCallback()        
pubnub.add_listener(mylistener)
pubnub.subscribe().channels("chan-1").execute()

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    count = 1
    mesg=""
    while True:
        #print(count)
        p1 = ""
        p2 = ""
        global number2
        global out
        frame, roi = camera.get_frame(mesg)
        
        out = camera.get_res(roi)
        msg = out
        ## publish a message
        p1=msg
        p2=number2
        if(count%50==0):
            pubnub.publish().channel("chan-2").message(str(msg)).pn_async(my_publish_callback)
            keyboard.wait('spacebar')
            time.sleep(5)
            if(p2==""):
                pubnub.add_listener(mylistener2)
                p2=number2
                pubnub.remove_listener(mylistener2)
            if p1==p2:
                mesg='Draw'
                number2 = ""
            elif p1=='Rock' and p2=='Scissor':
                mesg='You Won!'
                number2 = ""
            elif p1=='Rock' and p2=='Paper':
                mesg='Opponent Won!'
                number2 = ""
            elif p1=='Scissor' and p2=='Paper':
                mesg='You Won!'
                number2 = ""
            elif p1=='Scissor' and p2=='Rock':
                mesg='Opponent Won!'
                number2 = ""
            elif p1=='Paper' and p2=='Rock':
                mesg='You Won!'
                number2 = ""
            elif p1=='Paper' and p2=='Scissor':
                mesg='Opponent Won!'
                number2 = ""
            else:
                p1 = ""
                p2 = ""
                number2 = ""
                mesg='Game Aborted!'
            print("Me: "+out)
            print(mesg)
        else:
            pass
        count+=1
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')
        
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=False)