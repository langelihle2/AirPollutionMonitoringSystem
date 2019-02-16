'''
Author : Langelihle Shange  student number : 215021983
Project name : Environment Graphic Pollution System for Air , Water and Soil.
the project monitors the current air, water and soil pollution by using formulas
reviewed to determine the the current pollution value. the collected data is
represented in the form of bar graph, and using different colors to represent pollution
level of a certain quantity.
'''

# ######################################## IMPORT CONFIGURATIONS ###########################################
from tkinter import *
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
from PIL import ImageTk, Image
import requests
import csv
import time
import config
import smtplib

# ######################################### GRAPH CONFIGURATIONS #########################################
plt.style.use('ggplot')
f = Figure(figsize=(12, 5), dpi=100)
# a1 = f.add_axes()
a1 = f.add_subplot(111)
a2 = f.add_subplot(111)
a3 = f.add_subplot(111)
access = 0
denied = 0
json_Aqi = ''
json_location = ''
json_aqi = 0
json_date = ''

# variables for holding the collected data from the sensors
'''CONNECTION TO SERVERS USING AN API KEY TO COLLECT AIR QUALITY DATA FROM THE SENSORS SITUATED IN RICHARDS BAY'''
def collectData():
    global json_aqi
    global json_location
    global json_date
    global json_data
    global json_Aqi

    try:
        # OPEN CSV FILE FOR READING AND APPENDING AT THE END OF THE FILE
        with open('read.csv', 'a+', newline='') as csvFile:
            thewriter = csv.writer(csvFile)
            url = 'https://api.waqi.info/search/?token=17206ac3afa1a1c0df2e7ac61f787364d30f0c95&keyword=cbd'
            if url == '-':
                url = 'https://api.waqi.info/search/?token=17206ac3afa1a1c0df2e7ac61f787364d30f0c95&keyword=eNseleni'

            if url == '-':
                url = 'https://api.waqi.info/search/?token=17206ac3afa1a1c0df2e7ac61f787364d30f0c95&keyword=eSkhaleni'

            if url == '-':
                url = 'https://api.waqi.info/search/?token=17206ac3afa1a1c0df2e7ac61f787364d30f0c95&keyword=shanghai'

            json_data = requests.get(url).json()
            json_date = json_data['data'][0]['time']['stime']
            date = str(time.strftime('%x'))
            json_Aqi = json_data['data'][0]['aqi']
            json_aqi = int(json_data['data'][0]['aqi'])

            # STATUS BAR COLOR CHANGE WITH CHANGING AIR QUALITY VALUE
            pollutionColorStatus()

            json_location = json_data['data'][0]['station']['name']
            thewriter.writerow([json_date, json_aqi, json_location, date])

    except IOError:
        print("Connection error")
    else:
        pass

# ##################################### MAIN CLASS #################################
class Root(Tk):
        def __init__(self):
            Tk.__init__(self)

            collectData()
            self.title("AWS Pollution Scale")
            self.minsize(640, 500)
            self.iconbitmap('window.ico')

            # Setup Frame
            container = Frame(self)
            container.pack(side="top", fill="both", expand=True)
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)

            self.frames = {}

            for F in (Air, Water, Soil):
                frame = F(container, self)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="nsew")

            self.show_frame(Air)

        def show_frame(self, context):
            frame = self.frames[context]
            frame.tkraise()

# -----------------------------Page for AQI -------------------------------


class Air(Frame):
        def __init__(self, parent, controller):
            Frame.__init__(self, parent)

            # Setup Frame
            container1 = Frame(self)
            container1.pack()
            container2 = Frame(self)
            container2.pack(side=BOTTOM)
            heading = Label(container1, text="Air Pollution Visualization", font=("Verdana", 14))
            heading.grid(columnspan=3, row=0, padx=5, pady=5, sticky=EW)

            # BUTTONS FOR AIR SOIL AND WATER AND THE STATUS BAR CODE
            page = Button(container1, text=" Water ", command=lambda: controller.show_frame(Water))
            page.grid(column=2, row=1, sticky=EW)
            page_one = Button(container1, text=" Air ")
            page_one.grid(column=0, row=1, sticky=EW)
            page_two = Button(container1, text=" Soil ", command=lambda: controller.show_frame(Soil))
            page_two.grid(column=1, row=1, sticky=EW)
            aqi = Label(container1, text='AQI' + ' '+json_Aqi + ' ' + json_location, bg=config.statusColorAir,
                        fg='black', font=config.LARGE_FONT_QUALITY)
            aqi.grid(columnspan=3, row=2, sticky=EW)
            UpdatedTime = Label(container1, text='Updated : ' + ' ' + json_date, bg=config.statusColorAir,
                                fg='black', font=config.LARGE_FONT_QUALITY)
            UpdatedTime.grid(columnspan=3, row=3, sticky=EW)

            self.img = ImageTk.PhotoImage(Image.open("Air.png"))
            panel = Label(container2, image=self.img)
            panel.pack(padx=10, pady=10, side=RIGHT)

            self.barGraph(container2)


        def barGraph(self, container):
            a1.clear()

            try:
                data = pd.read_csv('read.csv')
                for eachLine in data.index:
                    try:
                        if data['aqiData'][eachLine] <= 50:

                            if (data['aqiData'][eachLine] > 0) and (data['aqiData'][eachLine] <= 12):
                                a1.bar(data['LogDate'][eachLine],
                                       data['aqiData'][eachLine],
                                       align='center', color='#66FF66', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 12) and (data['aqiData'][eachLine] <= 25):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#00FF00', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 25) and (data['aqiData'][eachLine] <= 38):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#008F00', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 38) and (data['aqiData'][eachLine] <= 50):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#002E00', alpha=1.0)
                        elif (data['aqiData'][eachLine] > 50) and (data['aqiData'][eachLine] <= 100):

                            if (data['aqiData'][eachLine] > 50) and (data['aqiData'][eachLine] <= 63):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#F9FF4D', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 63) and (data['aqiData'][eachLine] <= 76):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#FFFF00', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 76) and (data['aqiData'][eachLine] <= 89):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#919100', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 89) and (data['aqiData'][eachLine] <= 100):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#5E5E13', alpha=1.0)
                        elif (data['aqiData'][eachLine] > 100) and (data['aqiData'][eachLine] <= 150):
                            # sendEmail()
                            if (data['aqiData'][eachLine] > 100) and (data['aqiData'][eachLine] <= 113):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#FFD970', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 113) and (data['aqiData'][eachLine] <= 76):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#FF9D0A', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 76) and (data['aqiData'][eachLine] <= 125):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#994C00', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 89) and (data['aqiData'][eachLine] <= 100):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#663300', alpha=1.0)
                        elif (data['aqiData'][eachLine] > 150) and (data['aqiData'][eachLine] <= 200):
                            # sendEmail()
                            if (data['aqiData'][eachLine] > 150) and (data['aqiData'][eachLine] <= 162):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#FF6666', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 162) and (data['aqiData'][eachLine] <= 175):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#FF0000', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 175) and (data['aqiData'][eachLine] <= 188):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#990000', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 188) and (data['aqiData'][eachLine] <= 200):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#660000', alpha=1.0)
                        elif (data['aqiData'][eachLine] > 200) and (data['aqiData'][eachLine] <= 250):
                            # sendEmail()
                            if (data['aqiData'][eachLine] > 200) and (data['aqiData'][eachLine] <= 213):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#FF99CC', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 213) and (data['aqiData'][eachLine] <= 223):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='FF0080', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 223) and (data['aqiData'][eachLine] <= 239):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#99004D', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 239) and (data['aqiData'][eachLine] <= 250):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#33001A', alpha=1.0)
                        elif (data['aqiData'][eachLine] > 250) and (data['aqiData'][eachLine] <= 300):
                            # sendEmail()
                            if (data['aqiData'][eachLine] > 250) and (data['aqiData'][eachLine] <= 263):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#9999FF', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 263) and (data['aqiData'][eachLine] <= 276):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#3333FF', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 276) and (data['aqiData'][eachLine] <= 289):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#000099', alpha=1.0)
                            elif (data['aqiData'][eachLine] > 289) and (data['aqiData'][eachLine] <= 300):
                                a1.bar(data['LogDate'][eachLine], data['aqiData'][eachLine], align='center',
                                       color='#000033', alpha=1.0)

                    except IOError:
                        print("Connection to servers faild")

            except IOError:
                print("Could not open or read file")
            else:

                title = "AQI pollution graph"
                a1.set_title(title)
                a1.set_xlabel("Date")
                a1.set_ylabel("aqi level")
                rects = a1.patches

                # Make some labels.
                labels = ["%d" % data['aqiData'][i] for i in range(len(rects))]

                for rect, label in zip(rects, labels):
                    height = rect.get_height()
                    a1.text(rect.get_x() + rect.get_width() / 2, height, label,
                            ha='center', va='bottom')
                canvas = FigureCanvasTkAgg(f, container)
                canvas.draw()
                canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

                toolbar = NavigationToolbar2Tk(canvas, container)
                toolbar.update()
                canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)




# -----------------------------Page for WQI -------------------------------
class Water(Frame):
        def __init__(self, parent, controller):
            Frame.__init__(self, parent)
            # Frame Setup
            container1 = Frame(self)
            container1.pack(expand=True)
            container2 = Frame(self)
            container2.pack(side=BOTTOM, expand=True)
            heading = Label(container1, text="Water Pollution Visualization", font=("Verdana", 14))
            heading.grid(columnspan=2, row=0, padx=5, pady=5, sticky=W)
            page = Button(container1, text=" Graph ", command=lambda: self.barGraph(container2))
            page.grid(column=0, row=2, sticky=EW)
            start_page = Button(container1, text="Start Page", command=lambda: controller.show_frame(Air))
            start_page.grid(column=1, row=2, sticky=EW)
            label2 = Label(container1, text='92 Skokomish, Washington', bg='#3333FF', fg='black', font=config.LARGE_FONT)
            label2.grid(columnspan=2, row=3, sticky=EW)
            self.img = ImageTk.PhotoImage(Image.open("water.png"))
            panel = Label(container2, image=self.img)
            panel.pack(padx=10, pady=10, side=RIGHT, expand=True)

        def barGraph(self, contain):
            a2.clear()

            relativeWeigth = []
            subWQI = []
            sum = 0
            global access

            if access == 0:
                try:
                    # open csv file containing water pollutants data
                    datacsv = pd.read_csv('wqiData.csv')
                    for eachLine in datacsv.index:
                        for i in range(7):
                            # list containg relative weigths for each pollutant
                            relativeWeigth.append(config.WQI[i] / config.TOTAL_WQI)
                            # wqi for each pollutant
                            subWQI.append(relativeWeigth[i] * datacsv[config.WQI_DATA[i]][eachLine])
                            # Overall water quality index
                        sum = subWQI[0] + subWQI[1] + subWQI[2] + subWQI[3] + subWQI[4] + subWQI[5] + subWQI[6]

                        if eachLine == 24:
                            break
                        if datacsv['Overall WQI'][eachLine] <= 25:
                            a2.bar(datacsv['Year'][eachLine], datacsv['Overall WQI'][eachLine], align='center',
                                   color='#99FFFF', alpha=1.0)
                        if (datacsv['Overall WQI'][eachLine] > 25) and (datacsv['Overall WQI'][eachLine] <= 50):
                            a2.bar(datacsv['Year'][eachLine], datacsv['Overall WQI'][eachLine], align='center',
                                   color='#66B2FF', alpha=1.0)
                        if (datacsv['Overall WQI'][eachLine] > 50) and (datacsv['Overall WQI'][eachLine] <= 75):
                            a2.bar(datacsv['Year'][eachLine], datacsv['Overall WQI'][eachLine], align='center',
                                   color='#007FFF', alpha=1.0)
                        if (datacsv['Overall WQI'][eachLine] > 75) and (datacsv['Overall WQI'][eachLine] <= 100):
                            a2.bar(datacsv['Year'][eachLine], datacsv['Overall WQI'][eachLine], align='center',
                                   color='#3333FF', alpha=1.0)
                        if (datacsv['Overall WQI'][eachLine] > 100) and (datacsv['Overall WQI'][eachLine] <= 125):
                            a2.bar(datacsv['Year'][eachLine], datacsv['Overall WQI'][eachLine], align='center',
                                   color='#000099', alpha=1.0)
                        if datacsv['Overall WQI'][eachLine] > 125:
                            a2.bar(datacsv['Year'][eachLine], datacsv['Overall WQI'][eachLine], align='center',
                                   color='#000033', alpha=1.0)

                except IOError:
                    print("Could not open or read file")
                else:
                    title = "WQI pollution graph"
                    a2.set_title(title)
                    rects = a2.patches
                    a2.set_xlabel("Date")
                    a2.set_ylabel("WQI Level")

                    # Make some labels.
                    labels = ["%d" % datacsv['Overall WQI'][i] for i in range(len(rects))]

                    for rect, label in zip(rects, labels):
                        height = rect.get_height()
                        a2.text(rect.get_x() + rect.get_width() / 2, height, label,
                                ha='center', va='bottom')

                    canvas = FigureCanvasTkAgg(f, contain)
                    canvas.draw()
                    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

                    toolbar = NavigationToolbar2Tk(canvas, contain)
                    toolbar.update()
                    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
                    access = access + 1

            else:
                pass

# -----------------------------Page for SQI -------------------------------


class Soil(Frame):
        def __init__(self, parent, controller):
            Frame.__init__(self, parent)
            # Frame Setup
            container1 = Frame(self)
            container1.pack(expand=True)
            container2 = Frame(self)
            container2.pack(side=BOTTOM, expand=True)
            heading = Label(container1, text="Soil Pollution Visualization", font=("Verdana", 14))
            heading.grid(columnspan=2, row=0, padx=5, pady=5, sticky=W)
            page = Button(container1, text=" Graph ", command=lambda: self.barGraph(container2))
            page.grid(column=0, row=2, sticky=EW)
            start_page = Button(container1, text="Start Page", command=lambda: controller.show_frame(Air))
            start_page.grid(column=1, row=2, sticky=EW)
            label2 = Label(container1, text='9 White Sulphur Spring, USA', bg='#CC6600', fg='black', font=config.LARGE_FONT)
            label2.grid(columnspan=2, row=3, sticky=EW)
            self.img = ImageTk.PhotoImage(Image.open("soil.png"))
            panel = Label(container2, image=self.img)
            panel.pack(padx=10, pady=10, side=RIGHT, expand=True)

        def barGraph(self, container):
            a3.clear()

            global denied
            sigma = 0
            list = []

            if denied == 0:
                try:
                    # open csv for soil data for data analysis
                    datacsv = pd.read_csv('soildata.csv')
                    for eachLine in datacsv.index:
                        for i in range(13):
                            # assign each value from each field to a list
                            list.append(datacsv[config.SQI_DATA[i]][eachLine])
                        # Add all values in each row
                        Sum = list[0] + list[1] + list[2] + list[3] + list[4] + list[5] + list[6] +\
                              list[7] + list[8] + list[9] + list[10] + list[11] + list[12]
                        # find SQI value
                        sigma = (Sum/10**2)/13

                        if eachLine == 40:
                            break
                        if datacsv['sqi'][eachLine] <= 3:
                            a3.bar(datacsv['Collection_Date'][eachLine], datacsv['sqi'][eachLine], align='center',
                                   color='#331A00', alpha=1.0)
                        if (datacsv['sqi'][eachLine] > 3) and (datacsv['sqi'][eachLine] <= 6):
                            a3.bar(datacsv['Collection_Date'][eachLine], datacsv['sqi'][eachLine], align='center',
                                   color='#663300', alpha=1.0)
                        if (datacsv['sqi'][eachLine] > 6) and (datacsv['sqi'][eachLine] <= 9):
                            a3.bar(datacsv['Collection_Date'][eachLine], datacsv['sqi'][eachLine], align='center',
                                   color='#CC6600', alpha=1.0)
                        if (datacsv['sqi'][eachLine] > 9) and (datacsv['sqi'][eachLine] <= 10):
                            a3.bar(datacsv['Collection_Date'][eachLine], datacsv['sqi'][eachLine], align='center',
                                   color='#FFB366', alpha=1.0)

                except IOError:
                    print('Could not open or read file')

                else:
                    title = "SQI pollution graph"
                    a3.set_title(title)
                    rects = a3.patches
                    a3.set_xlabel("Date")
                    a3.set_ylabel("SQI Level")

                    # Make some labels.
                    labels = ["%d" % datacsv['sqi'][i] for i in range(len(rects))]

                    for rect, label in zip(rects, labels):
                        height = rect.get_height()
                        a3.text(rect.get_x() + rect.get_width() / 2, height, label,
                                ha='center', va='bottom')

                    canvas = FigureCanvasTkAgg(f, container)
                    canvas.draw()
                    canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)

                    toolbar = NavigationToolbar2Tk(canvas, container)
                    toolbar.update()
                    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
                    denied = denied + 1

            else:
                pass


# ################################################ COLOR CODE AND AQI STATUS ##############################
def pollutionColorStatus():

    if json_aqi <= 50:
        if (json_aqi > 0) and (json_aqi <= 12):
            config.statusColorAir = '#66FF66'
        elif (json_aqi > 12) and (json_aqi <= 25):
            config.statusColorAir = '#00FF00'
        elif (json_aqi > 25) and (json_aqi <= 38):
            config.statusColorAir = '#008F00'
        elif (json_aqi > 38) and (json_aqi <= 50):
            config.statusColorAir = '#002E00'
    elif (json_aqi > 50) and (json_aqi <= 100):
        if (json_aqi > 50) and (json_aqi <= 63):
            config.statusColorAir = '#F9FF4D'
        elif (json_aqi > 63) and (json_aqi <= 76):
            config.statusColorAir = '#FFFF00'
        elif (json_aqi > 76) and (json_aqi <= 89):
            config.statusColorAir = '#919100'
        elif (json_aqi > 89) and (json_aqi <= 100):
            config.statusColorAir = '#5E5E13'
    elif (json_aqi > 100) and (json_aqi <= 150):
        if (json_aqi > 100) and (json_aqi <= 113):
            config.statusColorAir = '#FFD970'
        elif (json_aqi > 113) and (json_aqi <= 76):
            config.statusColorAir = '#FF9D0A'
        elif (json_aqi > 76) and (json_aqi <= 125):
            config.statusColorAir = '#994C00'
        elif (json_aqi > 89) and (json_aqi <= 100):
            config.statusColorAir = '#663300'
    elif (json_aqi > 150) and (json_aqi <= 200):
        if (json_aqi > 150) and (json_aqi <= 162):
            config.statusColorAir = '#FF6666'
        elif (json_aqi > 162) and (json_aqi <= 175):
            config.statusColorAir = '#990000'
        elif (json_aqi > 175) and (json_aqi <= 188):
            config.statusColorAir = '#6B6B00'
        elif (json_aqi > 188) and (json_aqi <= 200):
            config.statusColorAir = '#660000'
    elif (json_aqi > 200) and (json_aqi <= 250):
        if (json_aqi > 200) and (json_aqi <= 213):
            config.statusColorAir = '#FF99CC'
        elif (json_aqi > 213) and (json_aqi <= 223):
            config.statusColorAir = '#FF0080'
        elif (json_aqi > 223) and (json_aqi <= 239):
            config.statusColorAir = '#99004D'
        elif (json_aqi > 239) and (json_aqi <= 250):
            config.statusColorAir = '#33001A'
    elif (json_aqi > 250) and (json_aqi <= 300):
        if (json_aqi > 250) and (json_aqi <= 263):
            config.statusColorAir = '#9999FF'
        elif (json_aqi > 263) and (json_aqi <= 276):
            config.statusColorAir = '#3333FF'
        elif (json_aqi > 276) and (json_aqi <= 289):
            config.statusColorAir = '#000099'
        elif (json_aqi > 289) and (json_aqi <= 300):
            config.statusColorAir = '#000033'


# ################# FUNCTION TO SEND EMAIL ##################################
def sendEmail():

    content = "Reporting on the air quality index" \
              "current air quality index at " + json_location + "AQI of " + json_Aqi

    mail = smtplib.SMTP('smtp.gmail.com:587')

    mail.ehlo()

    mail.starttls()

    mail.login(config.EMAIL_ADDRESS, config.PASSWORD)

    mail.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS, content)
    mail.close()


# ################## BLANK WINDOW ###################
window = Root()

window.mainloop()