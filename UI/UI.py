import Com as com
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import pyqtgraph as pg
import threading
import numpy as np
import sys
import time
import pygame

class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COM Port")
        self.setFixedSize(QSize(260,180))
        
        COMBox_label = QLabel("COM portas",self)
        COMBox_label.setGeometry(20,10,100,30)
        
        global COMBox
        COMBox = QComboBox(self)
        COMBox.setGeometry(20,40,200,30)
        for i in range(20):
            COMBox.addItem("COM%d"%(i+1))
        
        BaudBox_label = QLabel("Baudrate",self)
        BaudBox_label.setGeometry(20,70,100,30)
        
        global BaudBox
        BaudBox = QComboBox(self)
        BaudBox.setGeometry(20,100,200,30)
        BaudBox.addItem("100")
        BaudBox.addItem("500")
        BaudBox.addItem("1000")
        BaudBox.addItem("9600")
        BaudBox.addItem("115200")
        
        global Jungtis_but
        
        Jungtis_but = QPushButton("Jungtis",self)
        Jungtis_but.setGeometry(75,135,100,30)
        Jungtis_but.pressed.connect(self.jungtis)
        
    def jungtis(self):
        try:
            COMPort = COMBox.currentText()
            BaudRate = int(BaudBox.currentText())
            com.stm_init(COMPort,BaudRate)
            w.close()
            busena_label.setText("Būsena: Prijungta!")
        except:
            w.close()
            busena_label.setText("Būsena: Klaida. Neprijungtas STM/blogi pram.")
    



class MainWindow(QMainWindow):
    suviai_int = []
    laikas_int = []
    def __init__(self):
        #--------------------------------------------LANGO_INIT-----------------------------#
        super(MainWindow, self).__init__()
        global event_stop
        event_stop = threading.Event()
        self.setWindowTitle("Ginklo parametrų matuoklis")
        self.setFixedSize(QSize(470,240))
        self.threadpool = QThreadPool()
        
        self.GifLabel = QLabel(self)
        self.GifLabel.setGeometry(250,0,180,160)
        self.gif = QMovie('Saudo1.gif')
        self.GifLabel.setMovie(self.gif)
        self.gif.start()
        
        
        pygame.mixer.init()
        pygame.mixer.music.load('Doom.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)
        
        #--------------------------------------------MYGTUKAI-------------------------------#
        global prisijungti_but
        prisijungti_but = QPushButton("Prisijungti",self)
        prisijungti_but.pressed.connect(self.prisijungti)
        prisijungti_but.setGeometry(105,170,120,40)
        
        global surinkti_duomenis_but
        surinkti_duomenis_but = QPushButton("Surinkti duomenis",self)
        surinkti_duomenis_but.pressed.connect(self.surinkti_duomenis)
        surinkti_duomenis_but.setGeometry(225,170,120,40)
        
        #--------------------------------------------LEIBELIAI-------------------------------#
        global suviai_label
        suviai_label = QLabel("Šūvių kiekis:",self)
        suviai_label.setFont(QFont('Arial',13))
        suviai_label.setGeometry(10,10,250,30)
        
        global pertaisymai_label
        pertaisymai_label = QLabel("Pertaisymų kiekis:",self)
        pertaisymai_label.setFont(QFont('Arial',13))
        pertaisymai_label.setGeometry(10,40,250,30)
        
        global itampa_label
        itampa_label = QLabel("Įtampa: ",self)
        itampa_label.setFont(QFont('Arial',13))
        itampa_label.setGeometry(10,70,200,30)
        
        global laikas_label
        laikas_label = QLabel("Veikimo laikas: ",self)
        laikas_label.setFont(QFont('Arial',13))
        laikas_label.setGeometry(10,100,200,30)
        
        global busena_label
        busena_label = QLabel("Būsena: ",self)
        busena_label.setFont(QFont('Arial',11))
        busena_label.setGeometry(10,130,400,30)
        
        #-----------------------------FUNKCIJOS------------------------------------------#
    def surinkti_duomenis(self):

        com.stm_writeline("A\n") 
        time.sleep(0.8)
        data = com.stm_readline()
        print(data)
        data = data.split()
        print(data)
        try:
            if data[0]=='S':
                suviai = int(data[1])
                pertaisymai = int(data[2])
                itampa = float(data[3])
                laikas = float(data[4])
                i = 0
                while data[6+i]!='E':
                    MainWindow.suviai_int.append(int(data[6+i]))
                    MainWindow.laikas_int.append(10*(i+1))
                    i+=1
                print("surinkta!")
                time.sleep(1)
                busena_label.setText("Būsena: Surinkta!")
                suviai_label.setText("Šūvių kiekis: %d"%suviai)
                pertaisymai_label.setText("Pertaisymai: %d"%pertaisymai)
                itampa_label.setText("Įtampa: %0.1f V"%itampa)
                print(self.suviai_int)
                if laikas < 6:
                    laikas_label.setText("Laikas: %d sec"%(laikas*10))
                if laikas > 6 and laikas < 360:
                    laikas_label.setText("Laikas: %d min %d sec"%((laikas/6),(laikas%6*10)))
                if laikas >= 360:
                    laikas_label.setText("Laikas: %d val %d min %d sec"%((laikas/360),(laikas%360/6),(laikas%6*10)))
                
        except IndexError:
            
            busena_label.setText("Būsena: Klaida. Bandykite vėl.")
            
            pass
        
        global G
        G = GrafikasWindow()
        G.show()
    def prisijungti(self):
        global w
        w = AnotherWindow()
        w.show()
      
class GrafikasWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grafikas")
        self.setFixedSize(QSize(700,550)) 
        
        global graph
        graph=self.graphWidget = pg.PlotWidget(self)
        labelStyle = {'color':'#FFF','font-size':'18pt'}
        graph.setLabel('left',text='Šūviai', units='Š0-Š1',**labelStyle)
        graph.setLabel('bottom',text='Laikas',units='s',**labelStyle)
        graph.resize(700,550)
        global data_line1
        
        suviai_dif = []
        index = 0
        while index<len(MainWindow.suviai_int):
            if index == 0:
                suviai_dif.append(MainWindow.suviai_int[index])
                index+=1
            else:
                suviai_dif.append((MainWindow.suviai_int[index]-MainWindow.suviai_int[(index-1)]))
                index+=1
                    
        
        data_line1 = graph.plot(MainWindow.laikas_int,
                                suviai_dif,
                                pen='g', 
                                symbol = 'o',
                                symbolPen='g',
                                name='green'
                                )
        data_line1.setData(MainWindow.laikas_int,suviai_dif)
        suviai_dif = []
        MainWindow.suviai_int = []
        MainWindow.laikas_int = []
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()