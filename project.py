import pyfirmata2
from pyfirmata2 import Arduino,util
import tkinter as tk
import sys
import time
import ctypes,os
import math



def firstwin():
    fir=tk.Tk()
    fir.title('WELCOME TO MUSIC WORLD')
    fir.geometry('1920x1080')
    bg = tk.PhotoImage(file='C:/Users/User/PycharmProjects/arduino/2.png')
    l17 = tk.Label(fir, image=bg)
    l17.pack()
    ex=tk.Button(fir,text='Existing user',font=(25),command=exist,bg='black',fg='white')
    ex.place(x=550,y=300)
    new=tk.Button(fir,text='New user',font=(40),command=newuser,bg='black',fg='white')
    new.place(x=550,y=250)
    fir.mainloop()


def exist():
    #fir.destroy()
    exuser=tk.Tk()
    exuser.title('EXISTING USER')
    exuser.geometry('2000x2000')
    ex=tk.Label(exuser,text='LOGIN',font=(30))
    username1=tk.Label(exuser,text='USERNAME',font=(15))
    ex.place(x=510,y=200)
    username1.place(x=450,y=250)
    name=tk.Entry(exuser)
    name.place(x=600,y=255)
    pas=tk.Label(exuser,text='PASSWORD',font=(15))
    pas.place(x=450,y=300)
    password=tk.Entry(exuser)
    password.place(x=600,y=300)
    l=[]
    l.append(name)
    l.append(password)
    file=open(str(l[0]),'r')
    r=file.read()
    file.close()        
    submit=tk.Button(exuser,text='SUBMIT',command=mainwin)
    submit.place(x=650,y=350)
    
    
def newuser():
    #fir.destroy()
    newuser1=tk.Tk()
    newuser1.title('NEW USER')
    newuser1.geometry('2000x2000')
    newuser=tk.Label(newuser1,text='NEW USER SIGN IN',font=(30))
    username1=tk.Label(newuser1,text='USERNAME',font=(15))
    newuser.place(x=510,y=200)
    username1.place(x=450,y=250)
    name=tk.Entry(newuser1)
    name.place(x=600,y=255)
    pas=tk.Label(newuser1,text='PASSWORD',font=(15))
    pas.place(x=450,y=300)
    password=tk.Entry(newuser1)
    password.place(x=600,y=300)
    l=[]
    l.append(name)
    l.append(password)
    file=open(str(l[0]),'w')
    file.write(str(l[1]))
    file.close()
    submit=tk.Button(newuser1,text='SUBMIT',command=exist)
    submit.place(x=650,y=350)
#newuser()

def login():
    x=username_box.get()
    y=password_box.get()
    try:
        u=open(x+'.txt','r')
        ps=u.read()
        if y==ps:
            #start.destroy()
            er='password is correct'
            paswrd=tk.Label(start,text=er)
            paswrd.place(x=700,y=700)
            mainwin()
           
        else:
            er='password is wrong'
            paswrd=tk.Label(start,text=er)
            paswrd.place(x=700,y=700)
    except FileNotFoundError:
        t=('Create an account by  signing up')
        word=tk.Label(start,text=t,font=(30))
        word.place(x=750,y=500)


def mainprogram():
    detect=tk.Tk()
    detect.title('Detect your Music Note')
    detect.geometry('2000x2000')
    def micros():
        tics=ctypes.c_int64()
        freq=ctypes.c_int64()
        ctypes.windll.kernel32.QueryPerformanceCounter(ctypes.byref(tics))
        ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq))
        t_us=tics.value*1e6/freq.value
        return t_us
    SAMPLES=128
    SAMPLING_FREQUENCY=2048
    OFFSETSAMPLES=40
    TUNER=3
    sumoffset=0
    X=[]
    autocorr=[]
    storednotesfreq=[130.1,138.59,146.83,155.56,164.81,174.61,185,196,207.65,220,233.08,246.94]
    offset=[]
    threash=0
    sumofcycles=0
    state_machine=0
    samplesperperiod=0
    signalfrequency = 0
    signalfrequency2 = 0
    signalfrequency3 = 0
    '''
    ****************
    CALIBRATION SECTION
    ****************'''
    print("Calibrating, Please do not play any note during calibration")
    cal=tk.Label(detect,text='Calibrating, Please do not play any note during calibration',font=(20))
    cal.place(x=450,y=200)
    port = "COM3"
    board = Arduino(port)
    pin = board.get_pin('a:0:i')
    it = pyfirmata2.util.Iterator(board)
    time.sleep(0.1)
    it.start()
    for i in range(0,OFFSETSAMPLES):
        a = pin.read()
        time.sleep(0.1)
        a = a * 1023
        offset.append(a)
        time.sleep(0.1)
        sumoffset = sumoffset + offset[i]
    print(offset)
    samplesperperiod = 0
    maxvalue = 0
    '''
    ***************
    PREPARE TO ACCEPT INPUT FROM A0 pin
    ***************'''
    #avgoffset = round(sumoffset/OFFSETSAMPLES)
    print("counting down for input")
    #co=tk.Label(detect,text="counting down for input",font=(20))
    #co.place(x=450,y=250)
    time.sleep(1)
    print(3)
    #c3=tk.Label(detect,text="3",font=(20))
    #c3.place(x=450,y=300)
    time.sleep(1)
    print(2)
    #c2=tk.Label(detect,text="2",font=(20))
    #c2.place(x=450,y=350)
    time.sleep(1)
    print(1)
    #c1=tk.Label(detect,text="1",font=(20))
    #c1.place(x=450,y=400)
    time.sleep(1)
    print("Play your note")
    c0=tk.Label(detect,text="Play your note",font=(20))
    c0.place(x=450,y=450)
    time.sleep(1)
    '''
    ***************
    COLECT SAMPLES FROM A0 WITH SAMPLING PERIOD
    ****************'''
    samplingperiod=1/SAMPLING_FREQUENCY
    for i in range(0,SAMPLES):
        microseconds = micros()
        b = pin.read()
        b=  b* 1023
        X.append(b)
        time.sleep(0.1)
    print(X)
    while(micros() < (microseconds + (samplingperiod * 1000000))):
        print("yes")
        print(micros())
        print(microseconds+(samplingperiod + 1000000))
        pass
    '''
    *****************
    AUTO CORRELATION FUNCTION
    *****************'''
    for i in range(0,SAMPLES):
        sum1 = 0
        for k in range(0,(SAMPLES-i)):
            sum1 =sum1 + ((X[k]-avgoffset)*(X[k+i]-avgoffset))
        autocorr.append(sum1 / SAMPLES)
        if(state_machine==0 and i==0):
            threash = autocorr[i] * 0.5
            state_machine = 1
        elif((state_machine==1 and i>0) and (threash < autocorr[i] and autocorr[i]-autocorr[i-1] > 0)):
            maxvalue=autocorr[i]
        elif((state_machine==1 and i>0) and  (threash < autocorr[i-1] and maxvalue==autocorr[i-1])):
            if(autocorr[i] - autocorr[i-1] <=0):
                periodend = i-1
                state_machine=2
                numofcycles=1
                samplesperperiod = periodend - 0
                period = samplesperperiod
                adjuster = TUNER + ( 50.04 * math.exp(-0.102 * samplesperperiod))
                signalfrequency=(SAMPLING_FREQUENCY/samplesperperiod)-adjuster
        elif((state_machine==2 and i>0 ) and (threash<autocorr[i] and autocorr[i]-autocorr[i-1] > 0 )):
            maxvalue=autocorr[i]
        elif((state_machine==2 and i>0) and (threash<autocorr[i-1] and maxvalue==autocorr[i-1])):
            if(autocorr[i]-autocorr[i-1] <= 0):
                periodend =i-1
                state_machine=3
                numofcycles=2
                samplesperperiod=periodend-0
                signalfrequency2 = ((numofcycles * SAMPLING_FREQUENCY)/(samplesperperiod )- adjuster)
                maxvalue=0
        elif((state_machine==3 and i>0) and ( threash < autocorr[i-1] and maxvalue==autocorr[i-1])):
            if(autocorr[i] - autocorr[i-1] <= 0):
                periodend=i-1
                state_machine=4
                numofcycles=3
                samplesperperiod=periodend-0
                signalfrequency3=(((numofcycles*SAMPLING_FREQUENCY) / (samplesperperiod)) - adjuster)
    '''
    **************
    RESULT ANALYSIS
    **************'''
    total = 0
    print(samplesperperiod)
    if(samplesperperiod == 0):
        #print("Unable to print the result, an error occurred! please try again !")
        out=tk.Label(detect)
    else:
        if(signalfrequency != 0):
            total =1
        if(signalfrequency2 != 0 ):
            total = total + 2
        if(signalfrequency3 != 0):
            total = total + 3
        signalfrequencyguess= ((1/total)*signalfrequency + (2/total)*signalfrequency2) + (3/total)*signalfrequency3
        print("The frequency of the note you played is approximately",signalfrequencyguess,"Hz")
        octaverange=3
        while( (signalfrequencyguess >= storednotefreq[0]-7) and (signalfrequencyguess  <= storednotefreq[11]+7) == False):
           for i in range(0,12):
               storednotesfreq[i] = 2*storednotesfreq[i]
               octaverange = ocatverange + 1
        minvalue=100000000
        notevalue=0
        for i in range(0,12):
            if(minvalue > abs(signalfrequencyguess-storednotefreq[i])):
                minvalue=abs(signalfreqguess - storednotefreq[i])
                notelocation = i
        print("I think you played")
        if(notelocation == 0):
            print("C")
        elif(notelocation == 1):
            print("C#")
        elif(notelocation == 2):
            print("D")
        elif(notelocation == 3):
            print("D#")
        elif(notelocation == 4):
            print("E")
        elif(notelocation == 5):
            print("F")
        elif(notelocation == 6):
            print("F#")
        elif(notelocation == 7):
            print("G")
        elif(notelocation == 8):
            print("G#")
        elif(notelocation == 9):
            print("A")
        elif(notelocation == 10):
            print("A#")
        elif(notelocation == 11):
            print("B")


def mainwin():    
    #try:
        #newuser1.destroy()
    #except NameError:
        #print("hi")
    window=tk.Tk()
    window.title('MUSIC NOTE DETECTOR')
    window.geometry('2000x2000')
    #new=tk.Button()
    music=tk.Button(window,text='Detect the Music Note',font=(20),command=mainprogram)
    music.place(x=300,y=100)
    #freq=tk.button(window,text='Know your Music Frequency',font=(20),command=musicfreq())
    #freq.place(x=300,y=150)
firstwin()
#newuser()
#mainwin()

