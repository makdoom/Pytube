

from tkinter import *
from tkinter import ttk
from threading import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import *
from pytube import YouTube

userFormat=''
fileSize=0
def progress(chunk=None, file_handle=None, bytes_remaining=None):
    fileDownloaded = (fileSize - bytes_remaining)
    percentage = (fileDownloaded / fileSize) * 100
    dwnBtn.config(fg='white',text="{:00.0f}% Downloaded".format(percentage))


def strtDownload():
    dwnBtn.config(text='Please Wait')
    global fileSize,userFormat
    URL = userText.get()
    userFormat = avForamt.get()
    path = askdirectory()
    try:
        mytube = YouTube(URL,on_progress_callback= progress)
        if userFormat == 'Video':
            stream = mytube.streams.filter(res='720p').first()
            fileSize = stream.filesize
            dwnBtn.config(text='Downloading..')
            dwnBtn.config(state=DISABLED)
            stream.download(path)
        else:
            stream = mytube.streams.filter(only_audio=True).last()
            fileSize = stream.filesize
            dwnBtn.config(text='Downloading..')
            dwnBtn.config(state=DISABLED)
            stream.download(path)

        showinfo('Downloaded Finished', 'Downloaded Successfully')
        userField.delete(0, END)
        dwnBtn.config(text='Download')
        dwnBtn.config(state=NORMAL)
    except Exception as e:
        error.config(text='Oops !!!! Video Not Found')
        dwnBtn.config(text='Download')

def strtThread():
    thrd = Thread(target=strtDownload)
    thrd.start()

root = Tk()
root.geometry('400x510+300+130')
root.iconbitmap('res/icon.ico')
root.title('Pytube')

#logo
img = PhotoImage(file='res/logo.png')
Label(image=img).pack(pady=10)


Label(text="Enter URL",font='lucida 17').pack(pady=5)

userText = StringVar()
userField = Entry(textvar=userText,justify=CENTER, font='lucida 15 ',borderwidth=0,relief=SUNKEN)
userField.pack(fill=X,padx=10,ipady=6,pady=6)
userField.focus_set()

# Audio/Video Combobox
avForamt = StringVar()
audioVideo = ttk.Combobox(root, textvariable=avForamt,font='lucida 11',state='readonly')
audioVideo['values'] = ('Video', 'Audio')
audioVideo.current(0)
audioVideo.pack(ipady=6,pady=15,ipadx=5)

# Download Button
dwnBtn = Button(root, bg='#f92020',fg='white',text='Download',borderwidth=0,font='lucida 14 bold',relief=RIDGE, command=strtThread)
dwnBtn.pack(pady=40,ipady=10,ipadx=30)

# Error Label
error = Label(text=" ",font='lucida 11 bold')
error.pack()

# Note
note= Label(text="NOTE: Some of the Videos will be downloaded without audio\nbecause some videos dosen't support both audio and video.",font='lucida 10')
note.pack(side=BOTTOM,pady=10)
root.mainloop()