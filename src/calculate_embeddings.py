
import time

import face_recognition
import cv2

def generate(image):
    """
    Takes a BGR (OpenCV) image and returns a 128-D face embedding.
    """
    s_time=time.time()
    # Convert BGR → RGB because face_recognition uses RGB
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    # image=cv2.resize(image,(0,0),None,0.50,0.50)
    # Detect face locations
    

 
    # Get encodings (128-D embeddings)
    encodings = face_recognition.face_encodings(image)
    e_time=time.time()
    # print(f"total time in caculate embedings: {e_time-s_time}")
    # Return the first face's embedding (128 values)
    return encodings

def main():
    pass 

if __name__=="__main__":
    main()