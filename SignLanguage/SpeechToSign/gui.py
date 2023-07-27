
from typing import Tuple
import customtkinter
import speech_recognition as sr
from PIL import Image
from translator import ISLConverter
import os
import cv2
class App(customtkinter.CTk):
  def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
    super().__init__(fg_color, **kwargs)
    self.initTextToSign()
  def initTextToSign(self):
    self.title('Sign Language Translator')
    self.converter=ISLConverter()
    self.geometry(f'{600}x{600}')
    self.grid_columnconfigure(1, weight=1)
    self.grid_columnconfigure((2, 3), weight=0)
    self.grid_rowconfigure((0, 1, 2), weight=1)
    self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
    self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
    self.sidebar_frame.grid_rowconfigure(4, weight=1)
    self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.play,text='Play')
    self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=50)
    self.sidebar_button_2=customtkinter.CTkButton(self.sidebar_frame,command=self.initSigntoText,text='Swap')
    self.sidebar_button_2.grid(row=4,column=0,padx=20,pady=50)
    self.sidebar_button_3=customtkinter.CTkButton(self.sidebar_frame,command=self.speech_to_text,text='Speak')
    self.sidebar_button_3.grid(row=3,column=0,padx=20,pady=50)
    self.disp_frame=customtkinter.CTkFrame(self,corner_radius=10)
    self.disp_frame.grid(row=0, column=1,rowspan=3, padx=(20, 10), pady=(20, 10), sticky="nsew")
    self.disp_label=customtkinter.CTkLabel(self.disp_frame,justify=customtkinter.CENTER,text='')
    self.disp_label.pack(padx=10,pady=10,fill='both',expand=True)
    self.entry = customtkinter.CTkEntry(self,placeholder_text='Enter text to be translated')
    self.entry.grid(row=3, column=1, padx=20, pady=20, sticky="nsew")
    self.cv_vid=None
    self.words=[]
    self.delay_between_signs = 1000 // 30
    self.frame_rate = 60
    self.r = sr.Recognizer()
    self.data = os.listdir("data/videos/")
  def initSigntoText(self):
    self.title('Sign Language Translator')
    self.geometry(f'{600}x{600}')
    self.grid_columnconfigure(1, weight=1)
    self.grid_columnconfigure((2, 3), weight=0)
    self.grid_rowconfigure((0, 1, 2), weight=1)
    self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
    self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
    self.sidebar_frame.grid_rowconfigure(4, weight=1)
    
    self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.openCamera,text='Open Camera')
    self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=50)
    self.sidebar_button_3=customtkinter.CTkButton(self.sidebar_frame,command=self.initTextToSign,text='Swap')
    self.sidebar_button_3.grid(row=3,column=0,padx=20,pady=50)
    self.disp_frame=customtkinter.CTkFrame(self,corner_radius=10)
    self.disp_frame.grid(row=0, column=1,rowspan=3, padx=(20, 10), pady=(20, 10), sticky="nsew")
    self.disp_label=customtkinter.CTkLabel(self.disp_frame,justify=customtkinter.CENTER,text='')
    self.disp_label.pack(padx=10,pady=10,fill='both',expand=True)

    self.cv_vid=None
    
  def speech_to_text(self):
    try:
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, duration=1)
            print("Talk now")
            audiot = self.r.listen(source,phrase_time_limit=5,timeout=5)
            myt = self.r.recognize_google(audiot, language="en-IN")
            self.entry.delete(0,customtkinter.END)
            self.entry.insert(0,myt)
    except:
        print("Error")
  def showFrame(self):
    ret,frame=self.cv_vid.read()
    if not ret:
      self.cv_vid.release()
      if self.getNext():
        self.disp_label.after(1000//60,self.showFrame)
      return
        
    img=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photoImg = customtkinter.CTkImage(img,size=(400,300))
    self.disp_label.configure(image=photoImg)
    self.disp_label.after(1000//60,self.showFrame)
  def getNext(self):
    self.words.pop(0)
    if len(self.words)==0:
      return False
    self.cv_vid=cv2.VideoCapture(f'data/videos/{self.words[0].capitalize()}.mp4')
    return True
  
  def play(self):
    words=self.converter.convert_to_isl(self.entry.get()).split()
    for word in words:
      if f'{word.capitalize()}.mp4' in self.data:
        self.words.append(word)
      else:
        self.words.extend(word)
    self.cv_vid=cv2.VideoCapture(f'data/videos/{self.words[0].capitalize()}.mp4')
    self.showFrame()
  def openCamera(self):
    if not self.cv_vid is None and self.cv_vid.isOpened():
      self.closeCamera()
      return
    self.cv_vid=cv2.VideoCapture(0)
    self.showCamera()
    self.sidebar_button_1.configure(text='Close Camera')
    
  def closeCamera(self):
    self.cv_vid.release()
    self.disp_label.configure(image=None)
    self.sidebar_button_1.configure(text='Open Camera')
  def showCamera(self):
    try:
      ret,frame=self.cv_vid.read()
      if not ret:
        return
      img=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
      photoImg = customtkinter.CTkImage(img,size=(400,300))
      self.disp_label.configure(image=photoImg)
      self.disp_label.after(1000//60,self.showCamera)
    except AttributeError:
      pass
  
if __name__=='__main__':      
  app=App()
  app.mainloop()