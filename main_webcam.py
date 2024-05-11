import os
import datetime
import time
import tkinter as tk
import cv2
from pyzbar.pyzbar import decode
#import matplotlib.pyplot as plt
import numpy as np

#############this def runs the important function#########

def run_code():
    with open('./whitelist.txt', 'r') as f:
        authorized_users = [l[:-1] for l in f.readlines() if len(l) > 2]
        f.close()

    log_path = './Book1.csv'

    cap = cv2.VideoCapture(0)

    most_recent_access = {}

    time_between_logs_th = 5

    while True:

        ret, frame = cap.read()

        qr_info = decode(frame)

        if len(qr_info) > 0:

            qr = qr_info[0]

            data = qr.data
            rect = qr.rect
            polygon = qr.polygon

            if data.decode() in authorized_users:
                cv2.putText(frame, 'ACCESS GRANTED', (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                if data.decode() not in most_recent_access.keys() \
                        or time.time() - most_recent_access[data.decode()] > time_between_logs_th:
                    most_recent_access[data.decode()] = time.time()
                    with open(log_path, 'a+') as f:
                        f.write('{},{}\n'.format(data.decode(), datetime.datetime.now()))
                        f.close()

            else:
                cv2.putText(frame, 'ACCESS DENIED', (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            frame = cv2.rectangle(frame, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height),
                                (0, 255, 0), 5)

            frame = cv2.polylines(frame, [np.array(polygon)], True, (255, 0, 0), 5)

        cv2.imshow('webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#####this function terminates it#######    
def terminate():
    root.destroy()



####this is the main GUI code########
from tkinter.font import Font
root = tk.Tk()
frame = tk.Frame(root,padx=10,pady=10) #for framing and padding
frame.pack()
my_font = tk.font.Font(size=15) #creates a font object
root.geometry("650x630")  #sets the window size
root.title("QR code Based Attendance System")
root.config(bg='white')
#create a image object
from PIL import ImageTk,Image

image =Image.open("nmamit_logo.png")
width,height=image.size
#image = image.resize((width // 4, height // 4))
photo=ImageTk.PhotoImage(image)
label=tk.Label(root,image=photo,width=width+100)
label.pack()

run_button = tk.Button(frame,text="Start Scanning QR codes", command=run_code,font=my_font,width=50,height=10,bg='green')
run_button.pack()

terminate_button = tk.Button(frame,text="Press  to terminate", command=terminate,font=my_font,width=50,height=10,bg='red')
terminate_button.pack()

root.mainloop()    
