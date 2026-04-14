### it will work within same network if you want to do it in real server use ngrok  
### ib this we are going to do facedetection in live stream video
### you can refer my reppo where we have done that earlier
#  https://github.com/Vivekkoranga1/face-detection-opencv-python

from flask import Flask,render_template,Response #importing flask so we can create our web app with this Response for making 
#custom respone for streaming 
import cv2 #importing cv2 so we can capture video and then convert i to jpeg then then send it in binary format to server then server send it to browser

video = cv2.VideoCapture(0)

face_detection = cv2.CascadeClassifier("faces.xml")


#We are use generator Beacuse we are usign Response class because we are not using text base thing 
#Response accept the iterator and all generator are iterator and we create generator's using yield 
#if we use normal function we will never get input beacuse it wait for all input 
def image_generator():
    while True:
        status,image = video.read()
        
        faces  = face_detection.detectMultiScale(image,1.1,4)  ### use grayscale image for face detection alwyas suggested but color also work
        
        for x,y,w,h in faces:
            face_detected_image = cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255))
        
        st,encoded_image = cv2.imencode(".jpg",face_detected_image)
        bytes_encoded_iamge = encoded_image.tobytes()
       
       #personally whole thing is easy but sending frame part inside yield is consuing for beginners
        yield (b'--frame\r\n' # boundary → tells browser "new frame starts"
                   b'Content-Type: image/jpeg\r\n\r\n' # header → this is an image
                   + bytes_encoded_iamge # actual image data
                   + b'\r\n')  # end of this frame



# "--" http multipart format
# "--bundary and boundary = anything_you want to name just like frame " but then 
# "you need to cahgne in Response boundary = anything you named above"
# \r\n = new line (HTTP standard)


#First \r\n → ends the header line
#Second \r\n → creates empty line

#Why empty line is required?
#“Headers are finished, now actual data (image) starts”

#Two \r\n are used because one ends the header line and the second creates an empty line
#to separate headers from the actual data in HTTP format.

app = Flask(__name__)



@app.route("/")
def home_page():
    return render_template("index.html") #we are using render template to show index.html which is our main streaming page


@app.route("/video_feed")
def video_feed():
    return Response(image_generator(),mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")