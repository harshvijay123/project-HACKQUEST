from tkinter import *
import Start_activity as sa
import threading
import pyttsx3 as pyt
import time
import Main
import json
import os
import pickle
import sqlite3
import datetime
from tkinter import messagebox
import random
import smtplib
import re


class Interface:
    def __init__(self):
        self.window=Tk()
        self.wn_width,self.wn_height=self.window.maxsize()

        self.window.geometry(str(self.wn_width)+'x'+str(self.wn_height)+"+0+0")
        self.window.attributes('-fullscreen',1)
        self.window.config(bg='#1C1B1A')
        welcome_window=sa.Interface(self)
        self.window.protocol("WM_DELETE_WINDOW",lambda :self.window.destroy())

        

        
        
        self.name=Label(self.window,text='# CodeBeaters',font=('candara',60,'bold'),anchor='center',fg='springgreen',
                        bg='#1C1B1A')
        self.name.place(x=100,y=0)

        self.frame=Frame(self.window,width=self.wn_width,height=self.wn_height-100)
        self.frame.place(x=0,y=100)
        self.canvas_height=self.wn_height
        self.canvas=Canvas(self.frame,bg='#1C1B1A',width=self.wn_width-300,height=self.wn_height-400,scrollregion=(0,0,0,self.canvas_height))
        self.vbar=Scrollbar(self.frame,orient=VERTICAL,bg='#1d3030',troughcolor='#1d3030',activebackground='black')
        self.vbar.pack(side=RIGHT,fill=Y)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(width=self.wn_width-20,height=self.wn_height-100,bd=0,highlightthickness=0)
        self.canvas.config(yscrollcommand=self.vbar.set)
        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)


        self.Entry_work = Frame(self.window,width=self.wn_width//3,height=20)
        self.Entry_work.place(x=self.wn_width//3,y=self.wn_height-80)

        
        self.message=StringVar()
        self.text_entry=Entry(self.Entry_work,bg='#1C1B1A',fg='springgreen',insertbackground='springgreen',textvariable=self.message
                            ,font=('candara',15),width=self.wn_width//30)
        self.text_entry.pack(side='left',expand=YES,fill=BOTH)
        self.text_entry.focus()
        self.send=Button(self.Entry_work,text='>',command=self.f,font=('KiloGram',15,'bold'),fg='#1C1B1A',
                         bg='springgreen',padx=0,pady=0)
        self.send.pack(side='right',expand=YES)
        self.window.bind('<Return>',self.f)

        self.X1=(self.wn_width-36)-550
        self.Y1=40
        self.X2=(self.wn_width-36)
        self.Y2=self.Y1+50


        self.vbar_move_pos=0.1

        self.tts=pyt.init()              
        rate=self.tts.getProperty('rate')
        self.tts.setProperty('rate',rate-50)


        self.emergency_button=Button(self.window,text='Emergency',command=lambda :self.emergency(),font=('KiloGram',15,'bold'),fg='white',
                         bg='red',padx=0,pady=0)
        self.emergency_button.place(x=self.wn_width-120,y=0)




        response=Main.chat('hi')
        response=self.tell_string(response)
        self.place_response(response)
        
        self.window.mainloop()

    def emergency(self):
        self.window.bell()
        self.emergency_window=Toplevel(self.window)
        self.emergency_window.title('Emergency')
        self.emergency_window.config(bg='black')
        self.emergency_window.geometry('600x400+100+100')
        label=Label(self.emergency_window,text='Enter phone number',font=('KiloGram',15,'bold'),fg='springgreen',
                         bg='black',padx=0,pady=0)
        entry=Entry(self.emergency_window,font=('KiloGram',15,'bold'),fg='springgreen',bg='black',insertbackground='springgreen')
        entry.place(x=250,y=10)
        label.place(x=10,y=10)
        import socket
        hostname=socket.gethostname()
        ip=socket.gethostbyname(hostname)
        label=Label(self.emergency_window,text='Your Ip: {}'.format(ip),font=('KiloGram',15,'bold'),fg='springgreen',
                         bg='black',padx=0,pady=0)
        label.place(x=150,y=100)
        button=Button(self.emergency_window,text='Done',font=('KiloGram',15,'bold'),bg='springgreen',
                         fg='black',padx=0,pady=0,command=lambda t=(ip,entry):self.get_emergency_entry(t[0],t[1]))
        button.place(x=250,y=200)
        self.emergency_window.mainloop()


    def get_emergency_entry(self,ip,entry):
        mobile_number=entry.get()
        label=None
        pattern=re.compile(r'[7-9][0-9]{9}')
        isValid=pattern.match(mobile_number)
        if not isValid:
            label=Label(self.emergency_window,text='You did not enter correct mobile number',font=('KiloGram',15,'bold'),fg='red',
                         bg='black',padx=0,pady=0)
            label.place(x=10,y=350)
        else:
            try:
                s=smtplib.SMTP('smtp.gmail.com',587)
                s.starttls()
                s.login('gauravvj1999@gmail.com','aain ayfm lwdb fenf')
                s.sendmail('gauravvj1999@gmail.com','shubhktalks@gmail.com',"Respected sir, I'm alex,chatbot. I captured an emergency help by system IP {} and contact number as +91-{}. Plese take action as soon as possible.".format(ip,mobile_number))
                s.quit()
                response='Your emergency report has placed successfully'
                self.place_response(response)
                self.emergency_window.destroy()
            except Exception as e:
                if label:
                    label['text']='something wrong with network or data-connection'
                else:
                    label=Label(self.emergency_window,text='something wrong with network or data-connection',font=('KiloGram',15,'bold'),fg='red',
                         bg='black',padx=0,pady=0)
                    label.place(x=10,y=350)
                    
                
            

    def speak(self,text):
        self.tts.say(text)
        self.tts.runAndWait()



    def tell_string(self,msg):
        msg=msg.replace('\n',' ')
        if len(msg)>=50 and ' ' in msg:
            msg=msg+'.'
            start=0
            l=[]
            while True:
                s=msg[start:start+50:]
                i=s.rfind(' ')
                l.append(msg[start:i+1])
                msg=msg[i+1::]
                if len(msg[start::])<50 and msg[start::].rfind('.')!=-1:
                    l.append(msg[start:len(msg)-1:])
                    break
            return '\n'.join(l)
        elif len(msg)>=50 and ' ' not in msg:
            l=[]
            for i in range(len(msg)//49):
                l.append(msg[0:50:]+'-')
                msg=msg[50::]

            return '\n'.join(l)

        else:
            return msg

    def place_request(self,msg):
        self.Y2+=msg.count('\n')*25
       
        self.canvas.create_rectangle(self.X1,self.Y1,self.X2,self.Y2,fill='#1d3030',width=3,outline='#1d3030')
        self.canvas.create_text(self.X1+30,self.Y1+10,text=msg,font=('candara',15),anchor='nw',fill='#E3DBD2')

    def place_response(self,response):
        self.x1=10
        self.y1=self.Y2+20
        self.x2=560
        self.y2=self.y1+50+response.count('\n')*25

        if((self.wn_height-200)<self.y2):
            self.canvas['scrollregion']=(0,0,0,self.y2+100)
            self.canvas_height+=100
                
            self.vbar_move_pos+=(self.y2-self.y1)/120+(self.Y2-self.Y1)/120
            self.canvas.yview_moveto(self.vbar_move_pos)
                

        self.canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill='#292921',width=3,outline='#292921')
        self.canvas.create_text(self.x1+30,self.y1+10,text=response,
                                    font=('candara',15),anchor='nw',fill='#E3DBD2')

        self.say=threading.Thread(target=lambda :self.speak(response.replace('\n',' ')))
        self.say.start()
            

        self.Y1=self.y2+20
        self.Y2=self.Y1+50


    def get_content(self):

        msg=self.message.get().lower()
        self.message.set('')
        msg=self.tell_string(msg)
        self.place_request(msg)
        self.details[self.flag]=msg

        if msg=='quit':
            self.place_request(msg)
            response="I'm taking out you from this procedure"
            self.place_response(response)
            self.send['command']=self.f
            self.window.bind('<Return>',self.f)
            return
            
        
        if self.flag==1:
            response='give me a minute to update..!'
            self.place_response(response)
            self.Y1-=20
            self.Y2-=50
            d={"tag": self.details[0]+' crime',
             "patterns": ["what is {}".format(self.details[0]+' crime'), "what is {}".format(self.details[0])],
             "responses": [self.details[1].replace('\n',' ')],
             "context_set": ""
            }
            file=open('intents.json')
            self.data=json.load(file)
            file.close()
            self.data['intents'].append(d)

            file=open('intents1.json','w')
            json.dump(self.data,file)
            file.close()

            os.remove('intents.json')
            os.rename('intents1.json','intents.json')

            with open('reporter.bin','wb') as f:
                pickle.dump(True,f)

            Main.train()

            with open('reporter.bin','wb') as f:
                pickle.dump(False,f)
            response='updated...!'
            self.send['command']=lambda :self.f()
            self.window.bind('<Return>',self.f)
            
        else:
            response=self.question_list[self.flag+1]
        if response:    
            response=self.tell_string(response)
            self.place_response(response)
            self.flag+=1
        
        

    def verify_admin_and_activity(self):
        if self.details[0]=='harsh vijay' and self.details[1]=='harsh vijay':
            self.question_list=['enter crime tag','enter content']
            self.details=[None,None]
            self.flag=0
            response='you are verified...!'

            self.send['command']=lambda :self.get_content()
            self.window.bind('<Return>',lambda event:self.get_content())
            response+=' \n'+self.question_list[0]
            response=self.tell_string(response)
            self.place_response(response)

        else:
            response='you entered wrong details. you need to again send register request. thanks'
            self.send['command']=lambda :self.f()
            self.window.bind('<Return>',self.f)
            response=self.tell_string(response)
            self.place_response(response)
            
            
        
        

    def get_details(self):
        msg=self.message.get().lower()
        self.message.set('')
        msg=self.tell_string(msg)
        
        self.details[self.flag]=msg

        if msg=='quit':
            self.place_request(msg)
            response="I'm taking out you from this procedure"
            self.place_response(response)
            self.send['command']=self.f
            self.window.bind('<Return>',self.f)
            return
        
        if self.flag==1:
            response=None
            self.place_request('*'*len(msg))
            self.verify_admin_and_activity()
            
        else:
            response=self.question_list[self.flag+1]

        if response:
            self.place_request(msg)
            response=self.tell_string(response)
            self.place_response(response)
            self.flag+=1

        

        
        
        
        

    def check_for_admin(self):
        self.flag=0
        self.question_list=['enter your name','enter password']
        self.user_name,self.password=None,None
        self.details=[self.user_name,self.password]
        self.send['command']=lambda :self.get_details()
        self.window.bind('<Return>',lambda event:self.get_details())
        response=self.question_list[0]
        response=self.tell_string(response)
        self.place_response(response)

    def update_crime_to_database(self):

        with open('reports.bin','rb') as file:
            sr=pickle.load(file)
        self.details.insert(0,sr+1)
        self.details.insert(3,str(datetime.datetime.today()).split()[0].replace('-','/'))

        conn=sqlite3.connect('REPORTS.db')
        conn.execute('''insert into REPORTS (SR,Name,Crime_Tag,Date,Address,Contact,Description,Crime_Spot)\
                        values({},'{}','{}','{}','{}','{}','{}','{}');'''.format(*self.details))
        conn.commit()
        with open('reports.bin','wb') as file:
            pickle.dump(sr+1,file)

            
        self.send['command']=lambda :self.f()
        self.window.bind('<Return>',self.f)
        

    def get_crime_details(self):
        msg=self.message.get().lower()
        self.message.set('')
        msg=self.tell_string(msg)

        if msg=='quit':
            self.place_request(msg)
            response="I'm taking out you from this procedure"
            self.place_response(response)
            self.send['command']=self.f
            self.window.bind('<Return>',self.f)
            return

        if self.flag==-3:
            try:
                s=smtplib.SMTP('smtp.gmail.com',587)
                s.starttls()
                s.login('gauravvj1999@gmail.com','aain ayfm lwdb fenf')
                self.otp='{:0>6}'.format(random.randint(0,100000))
                s.sendmail('gauravvj1999@gmail.com',msg,"Hey there....\nI'm Alex. Here is the OTP :- {} for your crime registeration. Don't share it with anyone".format(self.otp))
                s.quit()
                response=self.question_list[self.flag+1]
                
            except Exception as e:
                response='probably you entered an email id that does not exist or your network connection is not working'
                response=self.tell_string(response)
                self.place_request(msg)
                self.place_response(response)
                response=None
                
            
        elif self.flag==-1:
            if msg == self.otp:
                response=self.question_list[self.flag+1]
            else:
                response=self.question_list[self.flag]
                self.place_request(msg)
                self.place_request(msg)
                response=self.tell_string(response)
                self.place_response(response)
                response=None
                
        elif self.flag==5:
            response='roger that. updated'
            self.update_crime_to_database()   
        
        elif self.flag>=0:
            self.details[self.flag]=msg
            response=self.question_list[self.flag+1]
        
        
            
        else:
            response=self.question_list[self.flag+1]



        if response:
            self.place_request(msg)
            response=self.tell_string(response)
            self.place_response(response)
            self.flag+=1

        
        

    def register_crime(self):
        self.flag=-3
        self.question_list=['enter your full name','enter crime tag(like murder,molestation etc)','enter address',
                            'enter contact(like e-mail, phone number etc)','enter full description of crime',
                            'enter crime area',
                            'enter email id',
                            'I have sent you an OTP on the regstered email-id. enter that for further procedure',
                            'you entered wrong otp'
                            ]
        self.details=[i for i in range(len(self.question_list))]
        self.send['command']=lambda :self.get_crime_details()
        self.window.bind('<Return>',lambda event:self.get_crime_details())

        response=self.question_list[self.flag]
        response=self.tell_string(response)
        self.place_response(response)


    def play_news(self,cursor):
        l=list(cursor)[0]
        

        response='''there is a fiery news as...\
{} reported a crime named "{}" on {}. This incident happened in an area of {}. {} reported that\
 "{}"'''.format(l[0],l[1],l[2],l[3],l[0],l[4])

        response=self.tell_string(response)
        self.place_response(response)


    def get_full_detail(self,c):
        c+=1
        conn=conn=sqlite3.connect('REPORTS.db')
        cursor=conn.execute('''select Name,Date,Crime_Tag,Crime_Spot,Contact,Description from REPORTS where SR={};'''.format(c))
        l=list(cursor)[0]
        String='''Reporter Name - {} ,
Date - {} ,
Crime-Tag - {} ,
Crime-Spot - {} ,
Contact - {} ,
Report:
"{}"'''.format(l[0],l[1],l[2],l[3],l[4],self.tell_string(l[5]))

        self.place_response(String)
        conn.close()



    def destroy_listbox(self):
        self.list_box.destroy()
        self.list_get.destroy()
        self.list_close.destroy()
        self.list_label.destroy()
        self.send['state']=ACTIVE

        
        


    def verify_inspector(self):
        if self.details[0]=='harsh vijay' and self.details[1]=='harsh vijay':
            response='You are verified. I poped up a list of reports. You need to select row and click on "Get" button. Thanks'



            conn=sqlite3.connect('REPORTS.db')
            cursor=conn.execute('''select SR,Name,Crime_Tag,Contact,Date from REPORTS;''')
            

            self.list_box=Listbox(self.window,font=('candara',15),width=52,height=16,bg='#292921',bd=0,highlightthickness=0,
                              fg='#E3DBD2')
            self.list_label=Label(self.window,text='SR   Name             Crime-Tag              Contact                     Date'+' '*25,
                        font=('candara',15),bg='#292921',fg='springgreen')
            self.list_label.place(x=self.wn_width-593,y=self.wn_height-630)
            self.send['state']=DISABLED

            self.list_get=Button(self.window,text=' Get ',font=('candara',15),bg='springgreen',
                           command=lambda l=self.list_box:self.get_full_detail(l.curselection()[0]))
            self.list_get.place(x=self.wn_width-75,y=self.wn_height-200)

            self.list_close=Button(self.window,text='Close',font=('candara',15),bg='springgreen',
                                   command=self.destroy_listbox)
            self.list_close.place(x=self.wn_width-593,y=self.wn_height-200)
            
            for i,row in enumerate(cursor,1):   
                self.list_box.insert(i,'{}  {}  {}  {}  {}   '.format(row[0],row[1][:8].ljust(13,' '),
                                    row[2][:21].ljust(20,' '),row[3][:14].ljust(13,' '),row[4]).ljust(10,' '))
            self.list_box.place(x=self.wn_width-593,y=self.wn_height-600)

            conn.close()


            
            




















            
            self.send['command']=lambda :self.f()
            self.window.bind('<Return>',self.f)
            response=self.tell_string(response)
            self.place_response(response)


        else:
            response='you entered wrong details. you need to again send request. thanks'
            self.send['command']=lambda :self.f()
            self.window.bind('<Return>',self.f)
            response=self.tell_string(response)
            self.place_response(response)
        
    def take_inspector_details(self):
        msg=self.message.get().lower()
        self.message.set('')
        msg=self.tell_string(msg)
        
        self.details[self.flag]=msg

        if msg=='quit':
            self.place_request(msg)
            response="I'm taking out you from this procedure"
            self.place_response(response)
            self.send['command']=self.f
            self.window.bind('<Return>',self.f)
            return
        
        if self.flag==1:
            response=None
            self.place_request('*'*len(msg))
            self.verify_inspector()
            
        else:
            response=self.question_list[self.flag+1]

        if response:
            self.place_request(msg)
            response=self.tell_string(response)
            self.place_response(response)
            self.flag+=1
        
        
        

    def f(self,event=None):

        
        msg=self.message.get().lower()
        self.message.set('')
        
        if len(msg)!=0:
            l=msg.split()
            for i in range(len(l)):
                l[i]=l[i].strip()
            msg=' '.join(l)
            
            msg=self.tell_string(msg)
            self.place_request(msg)

            

            
        
            response=Main.chat(msg)
            if response=='register crime':
                self.register_crime()
            elif response=='news':
                with open('reports.bin','rb') as file:
                    r=pickle.load(file)
                sr=random.randint(1,r)

                conn=sqlite3.connect('REPORTS.db')
                cursor=conn.execute('select Name,Crime_Tag,Date,Crime_Spot,Description from REPORTS where SR={};'.format(sr))
                self.play_news(cursor)
                conn.close()
                    
            elif response=='inspection':
                self.details=[None,None]
                self.question_list=['enter your name','enter password']
                self.flag=0
                self.place_response(self.question_list[0])
                
                self.send['command']=lambda :self.take_inspector_details()
                self.window.bind('<Return>',lambda event:self.take_inspector_details())

            elif response=='emergency':
                self.place_response(response+' window ')
                self.emergency()

            elif 'admin' in response:
                self.check_for_admin()

                    
            else:
                response=self.tell_string(response)
                self.place_response(response)



        


if __name__=="__main__":
    Main.train()
    i=Interface()
