import cv2
import mediapipe as mp

import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def fingersCount(lm,tipIds,image,w,h,izquierda):
  fingersUp = [0,0,0,0,0]
  cont=0
  for i in tipIds:
    if i==4:
      y=lm[i].x
      y2=lm[i-1].x
      if izquierda :
        y2=lm[i].x
        y=lm[i-1].x
    else:
      y=lm[i].y
      y2=lm[i-1].y
    if y<y2 :
      fingersUp[cont]=1
    cont+=1
  count=str(sum(fingersUp))
  cv2.putText(image, count, (int(lm[2].x*w-10),int(lm[2].y*h+10)),cv2.FONT_ITALIC,2,(102,102,0), thickness = 3)

# Detecta la señal de shaka o de chill, tipico saludo en el surf, extendiendo el pulgar y el dedo meñique
def surf(lm,tipIds,image,w,h,grosor):
 
def like(lm,tipIds,image,w,h,grosor):
  if lm[tipIds[0]].y<lm[tipIds[1]].y and lm[tipIds[1]].y<lm[tipIds[2]].y and lm[tipIds[2]].y<lm[tipIds[3]].y and lm[tipIds[3]].y<lm[tipIds[4]].y and grosor<0.1:
    cv2.putText(image, "Like", (int(lm[2].x*w-10),int(lm[2].y*h+10)),cv2.FONT_ITALIC,2,(102,102,0), thickness = 3)

def dislike(lm,tipIds,image,w,h,grosor):
  if lm[tipIds[0]].y>lm[tipIds[1]].y and lm[tipIds[1]].y>lm[tipIds[2]].y and lm[tipIds[2]].y>lm[tipIds[3]].y and lm[tipIds[3]].y>lm[tipIds[4]].y and grosor<0.1:
    cv2.putText(image, "Dislike", (int(lm[2].x*w-10),int(lm[2].y*h+10)),cv2.FONT_ITALIC,2,(102,102,0), thickness = 3)

# Detecta si la mano está haciendo el gesto de stop (palma de la mano abierta) pero mirando arriba
def stop(lm,tipIds,image,w,h):
  if lm[tipIds[0]].x>lm[tipIds[1]].x and lm[tipIds[1]].x>lm[tipIds[2]].x and lm[tipIds[2]].x>lm[tipIds[3]].x and lm[tipIds[3]].x>lm[tipIds[4]].x:
    cv2.putText(image, "Stop", (int(lm[2].x*w-10),int(lm[2].y*h+10)),cv2.FONT_ITALIC,2,(102,102,0), thickness = 3)



cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue
    
    # Flip the image horizontally for a selfie-view display.
    image = cv2.flip(image, 1)
    
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

        #----------------
        # Detect fingers
        #----------------
        
        # list of finger tips locators, 4 is thumb, 20 is pinky finger
        tipIds = [4, 8, 12, 16, 20]
        
        lm = hand_landmarks.landmark
        
        # x,y coordinates of pinky tip. Coordinates are normalized to [0.0,1.0] with width and height of the image
        lm[tipIds[4]].x
        lm[tipIds[4]].y

        #height, width and depth (RGB=3) of image
        (h,w,d) = image.shape
        # Funcion
        izquierda= True if(lm[4].x> lm[20].x) else False

        grosor= math.sqrt((lm[19].x-lm[18].x)**2+(lm[19].y-lm[18].y)**2)

        fingersCount(lm,tipIds,image,w,h,izquierda)
        like(lm,tipIds,image,w,h,grosor)
        dislike(lm,tipIds,image,w,h,grosor)
        stop(lm,tipIds,image,w,h)



        # OpenCV function to draw a circle:
        # cv2.circle(image, center_coordinates, radius in pixels, color (Blue 0-255, Green 0-255, Red 0-255), thickness in pixels (-1 solid))
        # Example: draw a red solid circle of 10 pixel radius in the tip of pinky finger:
        # cv2.circle(image, (int(lm[tipIds[4]].x*w),int(lm[tipIds[4]].y*h)), 10, (0,0,255), -1)

        # OpenCV function to draw text on image
        # cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
        # Example: draw a blue "hello" on the upper left corner of the image
        # cv2.putText(image, "hello", (20,60),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0), thickness = 5)
        
        # See other OpenCV functions to draw a line or a rectangle:
        # cv2.line(image, start_point, end_point, color, thickness) 
        # cv2.rectangle(image, start_point (top-left), end_point (bottom-right), color, thickness)

    cv2.imshow('Rebeca\'s Hands', image)    
    
    if cv2.waitKey(5) & 0xFF == 27:
      break
      
cap.release()
