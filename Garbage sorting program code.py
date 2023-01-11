
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.filedialog
from PIL import Image,ImageTk
import oss2
from alibabacloud_imagerecog20190930.client import Client as imagerecog20190930Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_imagerecog20190930 import models as imagerecog_20190930_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
import csv
w = 500
h = 600
def enter():

    app = tkinter.Tk()
    screenwidth = app.winfo_screenwidth()
    screenheight = app.winfo_screenheight()
    size = '%dx%d+%d+%d' % (w, h, (screenwidth - w) / 2, (screenheight - h) / 2)
    app.geometry(size)
    img = Image.open('./home.png')
    app.overrideredirect(True)
    photo = ImageTk.PhotoImage(img.resize((w, h)))
    image_Label = tkinter.Label(app, image=photo)
    image_Label.pack()
    we='Welcome to the garbage classification program'
    t='''
    This program is an auxiliary program for household garbage classification,
    which helps people to classify household garbage. Users need to upload a 
    photo of garbage, and the program can identify and judge what garbage is.
    There are four types of garbage: dry garbage, Household food waste, recyclable
    garbage and hazardous garbage.
    '''
    labelt = tkinter.Label(app,anchor='w',justify='left', text=t)
    labelt.place(x=0, y=450)
    labelw = tkinter.Label(app, anchor='w', justify='center', text=we, font=('Fixdsys', 15, 'bold'))
    labelw.place(x=0, y=440)
    app.after(5000, app.destroy)
    app.mainloop()

enter()

csvFile = open('data.csv', 'r')
reader = csv.reader(csvFile)
data = []
for item in reader:
    data.append(item)
csvFile.close()


class Sample:
    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> imagerecog20190930Client:
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret
        )
        config.endpoint = f'imagerecog.cn-shanghai.aliyuncs.com'
        return imagerecog20190930Client(config)

    @staticmethod
    def main(
        picUrl,
    ) -> None:
        client = Sample.create_client('LTAI5t5ahbc98yBvNVSUbn2W', 'cmorylUDZNaPkWnJMPv30tl2gQqae6')
        classifying_rubbish_request = imagerecog_20190930_models.ClassifyingRubbishRequest(
            image_url=picUrl
        )
        runtime = util_models.RuntimeOptions()
        try:
            #Return classification information
            p=client.classifying_rubbish_with_options(classifying_rubbish_request, runtime)
            return p
        except Exception as error:
            UtilClient.assert_as_string(error.message)

#Select and display pictures
def choosepic():
    path_ = tkinter.filedialog.askopenfilename()
    path.set(path_)
    img_open = Image.open(entry.get())
    img = ImageTk.PhotoImage(img_open.resize((200,200)))
    lableShowImage.config(image=img)
    lableShowImage.image = img
#Identify picture information by category
def classification():
    auth = oss2.Auth('LTAI5t5ahbc98yBvNVSUbn2W', 'cmorylUDZNaPkWnJMPv30tl2gQqae6')
    bucket = oss2.Bucket(auth, 'oss-cn-shanghai.aliyuncs.com', 'cunchuceshi123')
    path=entry.get()
    for i in data:
        if i[0]==path:
            labelCa2["text"] =i[1]
            return
    picName="test.png"
    with open(path, 'rb') as fileobj:
        bucket.put_object(picName, fileobj)
    picUrl='https://cunchuceshi123.oss-cn-shanghai.aliyuncs.com/'+picName
    try:
        js=Sample.main(picUrl)
        if (js.body.data.elements[0].category == ''):
            labelCa2["text"] = 'UnKnown'
        else:
            if js.body.data.elements[0].category=="可回收垃圾":
                labelCa2["text"] ='Recyclable  Garbage'
            if js.body.data.elements[0].category=="干垃圾":
                labelCa2["text"] ='Dry Garbage'
            if js.body.data.elements[0].category=="湿垃圾":
                labelCa2["text"] = 'Household food waste'
            if js.body.data.elements[0].category=="有害垃圾":
                labelCa2["text"] = 'Hazardous Garbage'
            data.append([path,labelCa2["text"]])
            csvFile2 = open('./data.csv', 'w', newline='')
            writer = csv.writer(csvFile2)
            m = len(data)
            for i in range(m):
                writer.writerow(data[i])
            csvFile2.close()
    except:
        labelCa2["text"] = 'Identification failed, please operate again'
app= tk.Tk()
app.title('Garbage Classification')
screenwidth = app.winfo_screenwidth()
screenheight = app.winfo_screenheight()
size = '%dx%d+%d+%d' % (400, 400, (screenwidth - w) / 2, (screenheight - h) / 2)
app.geometry(size)
path = tk.StringVar()
entry = tk.Entry(app, state='readonly', text=path,width = 100)
entry.pack()
#Use Label to display pictures
lableShowImage = tk.Label(app)
lableShowImage.pack()
img_open = Image.open('./add.png')
img = ImageTk.PhotoImage(img_open.resize((200,200)))
lableShowImage.config(image=img)
lableShowImage.image = img
#Button for selecting pictures
buttonSelImage = tk.Button(app, text='Select Picture', command=choosepic)
buttonSelImage.place(x=100,y=250)
buttonSelImage2 = tk.Button(app, text='Classification', command=classification)
buttonSelImage2.place(x=200,y=250)
labelCa = tk.Label(app,text='Category：')
labelCa.place(x=50,y=320)
labelCa2 = tk.Label(app,text='UnKnown')
labelCa2.place(x=120,y=320)
app.mainloop()