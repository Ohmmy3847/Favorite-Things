
import tkinter as tk

from tkinter.ttk import *
from tkinter import X, Tk, simpledialog, messagebox

import pandas as pd

from io import BytesIO

import requests
import os
from io import BytesIO
from googleapiclient.discovery import build

#https://docs.google.com/spreadsheets/d/186-MSw_hUXVL5b_aPqSmN_uRHrrZZKoaPs0SSiM3wkA/edit?usp=sharing
from google.oauth2 import service_account

from PIL import ImageTk, Image  
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import datetime


global get_topic, barh_t 
def Userdata(newtopic,newfavorite,month,year):
    asking = pd.read_csv('extention/User.csv')
    asking=asking.drop(asking[asking.MONTH !=month].index)
    asking.loc[len(asking.index)] =[newtopic,newfavorite,month,year]   
    asking.to_csv('extention/User.csv',index = False)
def createnew(newtopic,newfavorite,month,year):
    
    
    SERVICE_ACCOUNT_FILE = 'extention/key.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = None
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    SAMPLE_SPREADSHEET_ID = '186-MSw_hUXVL5b_aPqSmN_uRHrrZZKoaPs0SSiM3wkA' 
           
    try:
        service = build('sheets', 'v4', credentials=credentials)
    except:
        DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        service = build('sheets', 'v4', credentials=credentials, discoveryServiceUrl=DISCOVERY_SERVICE_URL)

    sheet = service.spreadsheets()

    newdata = [[newtopic.upper(),newfavorite.upper(),time.month,time.year]]
    sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,range='Favoritedata!A1:D1',valueInputOption='USER_ENTERED',insertDataOption="INSERT_ROWS",body ={'values':newdata}).execute()
def ok():
    global new_topic
    get_topic = Topic_Entry.get().title()
    new_topic =get_topic
    if get_topic == '':
        messagebox.showerror('error','Type something')
    else:
        Topic_Entry.delete(0, 'end')
        #Topic_Entry.insert(0, "")
        if get_topic.upper() not in  Us_data:
            head_letter.config(text='What is your favorite '+get_topic+' ?')
            see_vote_result.config(text='Back',command=connection)
            vote.config(text='vote',command=vote_favorite)
        else:    
            messagebox.showerror('error','You have already voted '+get_topic+'.If you want to vote again.\nYou must wait until next month.')

def vote_favorite():
    
    get_favorite = Topic_Entry.get().title()   
    
    if get_favorite == '':
        messagebox.showerror('error','Type something')
    else:
        
        try:
            
            createnew(new_topic,get_favorite,time.month,time.year)
        except:
            
            connection()
        else:
            Userdata(new_topic.upper(),get_favorite.upper(),time.month,time.year)
            
            connection()
            messagebox.showinfo('Successfully submitted','Your favorite '+str(new_topic)+' is '+str(get_favorite))
       
        
def vote_result():
    global toolbar
    
    world_favorite={}
    
    asking_topic=Topic_Entry.get().upper()
    topic = list(df_f['TOPIC'])
    favorite = list(df_f['FAVORITE'])
 
    print(favorite)
    
    for j in range(len(topic)):
         world_favorite[topic[j]] = list()
    for i in range(len(topic)):
        topic[i] = topic[i].upper()   
        favorite[i] = favorite[i].upper()
   
        if topic[i] in world_favorite:
            
            world_favorite[topic[i]].append(favorite[i].title())
            
        else:    
            world_favorite[topic[i]] = favorite[i].title()
    if asking_topic in world_favorite:
        
        
        try:
            T = pd.read_csv('extention/User.csv')
            T=T[T['TOPIC']==asking_topic]
            print(T["FAVORITE"].values[0])
            your_vote =T["FAVORITE"].values[0]
        except:
            your_vote='none'
        pine = world_favorite[asking_topic]
        du={} 
        for d in pine:   
            du[d] = pine.count(d)
        du = dict(sorted(du.items(), key=lambda item: item[1]))
        
       
        label_before =  list(du.keys())
        label= list(reversed(label_before))[:5]
        label= list(reversed(label))

        v_before = list(du.values())
        v= list(reversed(v_before))[:5]
        v= list(reversed(v))
     
        sv =sum(du.values())

        plot1.clear()
        
        plot1.set_title('Favorite '+asking_topic.title()+' from '+str(sv)+' votes\n Your vote is '+your_vote.title(), fontsize=15, color= 'white', fontweight='bold')
        


        for index, value in enumerate(v):
             plot1.text(value, index,
                str(value), color='white', fontweight='bold')
        plot1.set_facecolor("#121212")
        
        plot1.barh(label,v,color='#F6AC5D')
    

        toolbar = NavigationToolbar2Tk(barh,
                                    root)
        toolbar.config(background='#121212')
        toolbar._message_label.config(background='#121212',fg='White')
        toolbar.winfo_children()[-2].config(background='#121212')
        toolbar.place(relx=0.3,rely=0.9, anchor="center")  
        toolbar.update()
        
       
        barh_t =barh.get_tk_widget()
        barh_t.place(x=350,y=210, anchor="center")
 

        Top1.config(text='')
        Top2.config(text='')
        Top3.config(text='')
        Top4.config(text='')
        Top5.config(text='')
        Top6.config(text='')

        see_vote_result.config(text='Back',command=delete,width=20,)
        see_vote_result.place(relx=0.8,rely=0.9, anchor="center")   
       
    else:
        messagebox.showerror('error',"' "+str(asking_topic.title())+" '"+' isn\'t exists ')

def delete():
    toolbar.destroy()
    connection()
def Out():
    root.destroy()
  
def reconnect():
    
    root.destroy()
    os.startfile("first.py")
def connection():
    global Us_data,time
    
    time = datetime.datetime.now()
    user_data = pd.read_csv('extention/User.csv')
    user_data =user_data[user_data['YEAR']==time.year]
    user_data =user_data[user_data['MONTH']==time.month]
    Us_data = list(user_data['TOPIC'])
    print(Us_data)
    barh_t.place(x=35330,y=23330, anchor="center")
    
  
    

    global df_f
    try:   
        
        r = requests.get('https://docs.google.com/spreadsheet/ccc?key=186-MSw_hUXVL5b_aPqSmN_uRHrrZZKoaPs0SSiM3wkA&output=csv')
    except :
        panel.config(image=img_reconnect,width=550,height=479)
        panel.place(x=350,y=230, anchor="center")
        head_letter.config(text='Connection Lost!!!')
        head_letter.place(x=350,y=40, anchor="center")
        reconnect.place(x=240,y=420, anchor="center")
        Out.place(x=470,y=420, anchor="center")
        Topic_Entry.place(x=470333,y=420333)
       
        head_letter2.place(x=470333,y=420333)
        see_vote_result.place(x=470333,y=420333)
        vote.place(x=470333,y=420333)
    else:
     
        

        asking = pd.read_csv('extention/User.csv')
        asking=asking.drop(asking[asking.MONTH !=time.month].index)
        asking.to_csv('extention/User.csv',index = False)


        data = r.content
        df_f = pd.read_csv(BytesIO(data))
        df_f = df_f[df_f['YEAR']==time.year]
        df_f = df_f[df_f['MONTH']==time.month]
        print(list(df_f['TOPIC']),'dff')
        print(list(user_data['TOPIC']),'----')
        main()
def main():
   
   
    Topic_Entry.delete(0, 'end')
    Topic_Entry.insert(0, "")
    head_letter.config(text='What is your topic?')
    head_letter.place(relx=0.5,rely=0.1, anchor="center")
    #head_letter.pack(side='top', fill=X,expand=1)
    

    Topic_Entry.config(font=('Comic Sans MS',30),width=17)
    Topic_Entry.place(relx=0.5,rely=0.3, anchor="center",relwidth=0.7)

    head_letter2.config(text='Top 6 Topic Voted')
    head_letter2.place(relx=0.5,rely=0.6, anchor="center")

    cm =list(df_f['TOPIC'])

    cm =sorted(cm, key = cm.count,reverse = True)
    cm_save =cm

    see_vote_result.config(text='Vote Result',command=vote_result)
    see_vote_result.place(relx=0.7,rely=0.48, anchor="center",relwidth=0.2,relheight=0.1)

    vote.config(text='Ok',command=ok)
    vote.place(relx=0.3,rely=0.48, anchor="center",relwidth=0.2,relheight=0.1)
    
    cm=list(dict.fromkeys(cm))[:10]
   
    if len(list(set(cm_save))) <1:   
        Top1.config(text='1.???(0 vote)')
        Top2.config(text='2.???(0 vote)')
        Top3.config(text='3.???(0 vote)')
        Top4.config(text='4.???(0 vote)')
        Top5.config(text='5.???(0 vote)')
        Top6.config(text='6.???(0 vote)')
    elif len(list(set(cm_save))) <2:
        most = cm_save.count(cm[0])
        Top1.config(text='1.'+str(cm[0].title())+' ('+str(most)+' votes)')
        Top2.config(text='2.???(0 vote)')
        Top3.config(text='3.???(0 vote)')
        Top4.config(text='4.???(0 vote)')
        Top5.config(text='5.???(0 vote)')
        Top6.config(text='6.???(0 vote)')
    elif len(list(set(cm_save))) <3:
        most = cm_save.count(cm[0])
        Second =cm_save.count(cm[1])
        Top1.config(text='1.'+str(cm[0].title())+' ('+str(most)+' votes)')
        Top2.config(text='2.'+str(cm[1].title())+' ('+str(Second)+' votes)')
        Top3.config(text='3.???(0 vote)')
        Top4.config(text='4.???(0 vote)')
        Top5.config(text='5.???(0 vote)')
        Top6.config(text='6.???(0 vote)')
    elif len(list(set(cm_save))) <4:
        most = cm_save.count(cm[0])
        Second =cm_save.count(cm[1])
        Third = cm_save.count(cm[2])
        Top1.config(text='1.'+str(cm[0].title())+' ('+str(most)+' votes)')
        Top2.config(text='2.'+str(cm[1].title())+' ('+str(Second)+' votes)')
        Top3.config(text='3.'+str(cm[2].title())+' ('+str(Third)+' votes)')
        Top4.config(text='4.???(0 vote)')
        Top5.config(text='5.???(0 vote)')
        Top6.config(text='6.???(0 vote)')
    elif len(list(set(cm_save))) <5:
        most = cm_save.count(cm[0])
        Second =cm_save.count(cm[1])
        Third = cm_save.count(cm[2])
        forth = cm_save.count(cm[3])
        Top1.config(text='1.'+str(cm[0].title())+' ('+str(most)+' votes)')
        Top2.config(text='2.'+str(cm[1].title())+' ('+str(Second)+' votes)')
        Top3.config(text='3.'+str(cm[2].title())+' ('+str(Third)+' votes)')
        Top4.config(text='4.'+str(cm[3].title())+' ('+str(forth)+' votes)')
        Top5.config(text='5.???(0 vote)')
        Top6.config(text='6.???(0 vote)')
    elif len(list(set(cm_save))) <6:
        most = cm_save.count(cm[0])
        Second =cm_save.count(cm[1])
        Third = cm_save.count(cm[2])
        forth = cm_save.count(cm[3])
        fifth = cm_save.count(cm[4])
        Top1.config(text='1.'+str(cm[0].title())+' ('+str(most)+' votes)')
        Top2.config(text='2.'+str(cm[1].title())+' ('+str(Second)+' votes)')
        Top3.config(text='3.'+str(cm[2].title())+' ('+str(Third)+' votes)')
        Top4.config(text='4.'+str(cm[3].title())+' ('+str(forth)+' votes)')
        Top5.config(text='5.'+str(cm[4].title())+' ('+str(fifth)+' votes)')
        Top6.config(text='6.???(0 vote)')   
    else:
        most = cm_save.count(cm[0])
        Second =cm_save.count(cm[1])
        Third = cm_save.count(cm[2])
        forth = cm_save.count(cm[3])
        fifth = cm_save.count(cm[4])
        six = cm_save.count(cm[5])
        Top1.config(text='1.'+str(cm[0].title())+' ('+str(most)+' votes)')
        Top2.config(text='2.'+str(cm[1].title())+' ('+str(Second)+' votes)')
        Top3.config(text='3.'+str(cm[2].title())+' ('+str(Third)+' votes)')
        Top4.config(text='4.'+str(cm[3].title())+' ('+str(forth)+' votes)')
        Top5.config(text='5.'+str(cm[4].title())+' ('+str(fifth)+' votes)')
        Top6.config(text='6.'+str(cm[5].title())+' ('+str(fifth)+' votes)')
        
    Top1.place(relx=0.1,rely=0.7, )
    Top2.place(relx=0.1,rely=0.8, )
    Top3.place(relx=0.1,rely=0.9,)
    Top4.place(relx=0.5,rely=0.7, )
    Top5.place(relx=0.5,rely=0.8, )
    Top6.place(relx=0.5,rely=0.9)

root =tk.Tk()
root.geometry('700x500')
root.iconbitmap('extention/voteicon.ico')
root.resizable(False, False)
root.minsize(700, 500)
root.title('Favorite Things')
root['background']='#121212'
#title_bar = tk.Frame(root, bg='black', relief='raised', bd=2)
#title_bar.pack(expand=1, fill=X)
img= (Image.open("extention/internet_lost.png"))
resized_image= img.resize((350,300), Image.ANTIALIAS)
img_reconnect= ImageTk.PhotoImage(resized_image)


panel = tk.Label(root, image = '',background='#121212')

head_letter =tk.Label(root,text = ' ',font =('Comic Sans MS',35,'bold'),background='#121212',fg='white')


head_letter2 =tk.Label(root,text = ' ',font =('Comic Sans MS',30,'bold'),background='#121212',fg='white')


Topic_Entry =tk.Entry(root, borderwidth=5)


Top1 =tk.Label(root,text = ' ',font =('Comic Sans MS',20,'bold'),background='#121212',fg='white')

Top2 =tk.Label(root,text = ' ',font =('Comic Sans MS',20,'bold'),background='#121212',fg='white')

Top3 =tk.Label(root,text = ' ',font =('Comic Sans MS',20,'bold'),background='#121212',fg='white')

Top4 =tk.Label(root,text = ' ',font =('Comic Sans MS',20,'bold'),background='#121212',fg='white')
Top5 =tk.Label(root,text = ' ',font =('Comic Sans MS',20,'bold'),background='#121212',fg='white')
Top6 =tk.Label(root,text = ' ',font =('Comic Sans MS',20,'bold'),background='#121212',fg='white')

reconnect =tk.Button(root,font=('Comic Sans MS',10,'bold'), borderwidth=5,background='#9AD6F4',
                           text="Reconnect",
                           width=10,
                           height=2,command=reconnect)


Out =tk.Button(root,font=('Comic Sans MS',10,'bold'), borderwidth=5,background='#9AD6F4',
                           text="Exit",
                           width=10,
                           height=2,command=Out)


see_vote_result=tk.Button(root,font=('Comic Sans MS',10,'bold'),
                           text="Vote Result",
                           width=10,
                           height=2,command=vote_result,background='#9AD6F4', borderwidth=5)

vote=tk.Button(root,text="Ok",font=('Comic Sans MS',10,'bold'),
                    width=10,
                    height=2,command=ok,background='#9AF4BB', borderwidth=5,)


vote_bar = Label(root, image = '')

fig = Figure(figsize = (6, 4),
            dpi = 100)
fig.patch.set_facecolor('#121212')

plot1 = fig.add_subplot(111)

plot1.tick_params(axis='y', colors='white')
plot1.tick_params(axis='x', colors='white')

# plotting the graph


# creating the Tkinter canvas
# containing the Matplotlib figure
barh = FigureCanvasTkAgg(fig,
                        master = root,)  
barh.get_tk_widget().configure(bg="#121212")

barh.draw()



barh_t =barh.get_tk_widget()


connection()


root.mainloop()