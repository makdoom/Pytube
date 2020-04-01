
try:
    from pytube import YouTube
    from tkinter import *
    from tkinter import ttk
    from threading import * 
    from tkinter.filedialog import askdirectory
    from tkinter.messagebox import *
except Exception as e:
    print(f'Some modules are missing {e}')

fileSize = 0
def progress(chunk=None, file_handle=None, bytes_remaining=None):
    fileDownloaded = (fileSize - bytes_remaining)
    percentage = (fileDownloaded / fileSize) * 100
    dwnBtn.config(text="{:00.0f}% Downloaded".format(percentage))

def strDownload():
    dwnBtn.config(text='Please Wait')
    global fileSize
    URL = userText.get()
    videoFormat = avformat.get()
    downPath = askdirectory()

    try:
        myTube = YouTube(URL, on_progress_callback = progress)
        if videoFormat == 'Video':
            streams = myTube.streams.filter(res='720p').first()
            fileSize = streams.filesize
            dwnBtn.config(text='Downloading..')
            dwnBtn.config(state=DISABLED)
            streams.download(downPath)
        else:
            streams = myTube.streams.filter(only_audio=True).last()
            fileSize = streams.filesize
            dwnBtn.config(text='Downloading..')
            dwnBtn.config(state=DISABLED)
            streams.download(downPath)

        showinfo('Downloaded Finished','Downloaded Successfully')
        userField.delete(0, END)
        dwnBtn.config(text='Download')
        dwnBtn.config(state=NORMAL)
    except Exception as e:
        error.config(text='Oops.... Video Not Found !!!')
        error.pack()
    
def strDownloadThread():
    thread = Thread(target=strDownload)
    thread.start()

root = Tk()
root.geometry('400x450')
root.title('Pytube')
root.wm_iconbitmap('res/icon.ico')
 
# LOGO
img = PhotoImage(file='res/logo.png')
Label(image=img,bg='#74b9ff').pack(pady=30)

# user filed
Label(text='Enter URL:',font='lucida 16 bold',fg='white',bg='#74b9ff').pack(pady=10)
userText = StringVar()
userField = Entry(textvar=userText,font='lucida 14',justify=CENTER)
userField.focus_set()
userField.pack(fill=X,padx=20,ipady=4,ipadx=5)

#Audio/Video Combobox
avformat = StringVar()
audio_video = ttk.Combobox(root, textvar=avformat,state='readonly')
audio_video['values'] = ('Video','Audio')
audio_video.current(0)
audio_video.pack(padx=10,pady=20,ipady=5)

dwnBtn =Button(text='Download',bg='red',fg='white',relief=RIDGE,font='lucida 15 bold',command=strDownloadThread)
dwnBtn.pack(pady=20,ipadx=20,ipady=5)

error = Label(root, bg='#74b9ff',fg='white',text='',font='lucida 11 bold')
error.pack_forget()

root.config(bg='#74b9ff')
root.mainloop()