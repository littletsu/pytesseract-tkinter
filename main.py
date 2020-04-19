import numpy as nm 
import pytesseract 
import cv2 
from PIL import ImageGrab,ImageTk 
from tkinter import *
from tkinter import ttk
import pyautogui
import math


pytesseract.pytesseract.tesseract_cmd ='C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'



updateDelay = 200

class Display_Debug():
    def __init__(self):
        self.x1 = 464
        self.y1 = 369
        self.x2 = 515
        self.y2 = 400
        self.points = (self.x1, self.y1, self.x2, self.y2)

        self.tk = Tk()
        self.tk.geometry('1280x40')
        self.tk.resizable(width=False,height=False)
        self.tk.title('Debug')

        self.canvas = Canvas(self.tk, width=1280, height=40)
        self.canvas.pack()

        self.ocr_status = StringVar()

        self.ocr_status.set("Nothing has been detected yet.")

        self.ocr_detected = Label(self.tk, textvariable=self.ocr_status)
        self.ocr_detected.pack(anchor=S, fill=BOTH, expand=YES)

        self.screen_grab = ImageGrab.grab(bbox=self.points)

        self.screen = ImageTk.PhotoImage(self.screen_grab)
       
        self.img_screen = self.canvas.create_image(0, 0, image=self.screen, anchor=NW)

        self.tk.after(updateDelay, self.UpdateScreen)

        self.tk.bind_all('<Key>', self.Keypress)

        self.tk.mainloop()

    def UpdateScreen(self):
        self.screen_grab = ImageGrab.grab(bbox=self.points)
        self.screen = ImageTk.PhotoImage(self.screen_grab)
        self.canvas.itemconfig(self.img_screen, image = self.screen)
        self.tk.geometry('{}x{}'.format(self.screen.width(), self.screen.height()+100))
        self.canvas.config(width=self.screen.width(), height=self.screen.height())
        self.tk.after(50, self.OCR)
        self.tk.after(updateDelay, self.UpdateScreen)

    def OCR(self):
        result = pytesseract.image_to_string( 
                cv2.cvtColor(nm.array(self.screen_grab), cv2.COLOR_BGR2GRAY),  
                lang ='eng')
        print(result)
        self.tk.title(result)
        self.ocr_status.set(result)
        return result

    def Keypress(self, event):
        print(event.keycode)
        if event.keycode == 17:
            print('Set position 1')
            x, y = pyautogui.position()
            
            self.x1 = x
            self.y1 = y
            self.points = (self.x1, self.y1, self.x2, self.y2)
        elif event.keycode == 16:
            print('Set position 2')
            x, y = pyautogui.position()
            self.x2 = x
            self.y2 = y
            self.points = (self.x1, self.y1, self.x2, self.y2)



def main():
    Debug_Window = Display_Debug()
    return 0


if __name__ == '__main__':
    main()