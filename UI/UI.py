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
        #CombBox.currentIndexChanged.connect(self.)
        
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
    def __init__(self):
        #--------------------------------------------LANGO_INIT-----------------------------#
        super(MainWindow, self).__init__()
        global event_stop
        event_stop = threading.Event()
        self.setWindowTitle("Ginklo parametrų matuoklis")
        self.setFixedSize(QSize(470,240))
        self.threadpool = QThreadPool()
        
        '''self.videoplayer = QVideoWidget(self)
        self.videoplayer.setGeometry(10,150,400,710)
        self.media_player = QMediaPlayer(None,QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.videoplayer)
        video_path = "SS2.mp4"  # Replace with your video file path
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        
        self.media_player.play()'''
        
        
        
        
        self.GifLabel = QLabel(self)
        self.GifLabel.setGeometry(250,20,180,160)
        self.gif = QMovie('Saudo1.gif')
        self.GifLabel.setMovie(self.gif)
        self.gif.start()
        
        '''self.SSLabel = QLabel(self)
        self.SSLabel.setGeometry(10,220,470,810)
        self.SS = QMovie('SS1.mp4')
        self.SSLabel.setMovie(self.SS)
        self.SS.start()'''
        
        pygame.mixer.init()
        pygame.mixer.music.load('Doom.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)
        
        #self.pixmap = QPixmap("Saudo1.gif")
        '''self.slabel = QLabel(self)
        self.slabel.setPixmap(self.pixmap)
        self.slabel.setGeometry(250,20,self.pixmap.width(),self.pixmap.height())
        self.slabel.resize(self.pixmap.width(),
                          self.pixmap.height())'''
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
        
        
        #--------------------------------------------GRAFIKAS-------------------------------#
        
        """global suviai
        global itampa
        global laikas
        
        suviai = []
        itampa = []
        laikas = []
        
        labelStyle = {'color':'#FFF','font-size':'18pt'}
        global graph_suviai
        graph_suviai=self.graphWidget = pg.PlotWidget(self)
       
        graph_suviai.setLabel('left',text='Šuviai (š/min)', units='',**labelStyle)
        graph_suviai.setLabel('bottom',text='Laikas',units='min',**labelStyle)
        graph_suviai.move(40,40)
        graph_suviai.resize(640,460)
        
        
        
        global graph_itampa
        graph_itampa = self.graphWidget = pg.PlotWidget(self)
        graph_itampa.setLabel('left',text='Įtampa', units='V',**labelStyle)
        graph_itampa.setLabel('bottom',text='Laikas',units='min',**labelStyle)
        graph_itampa.move(700,40)
        graph_itampa.resize(640,460)
        
        self.setGeometry
        self.show()
        data_line1 = graph_suviai.plot(laikas,
                                suviai,
                                pen='g', 
                                symbol = 'o',
                                symbolPen='g',
                                name='green'
                                )
        data_line2 = graph_itampa.plot(laikas, 
                                itampa,
                                prm = 'r',
                                symbol = 'o',
                                symbolPen='r',
                                name='red'
                                ) """ 
        
        #-----------------------------FUNKCIJOS------------------------------------------#
    def surinkti_duomenis(self):
        #mas = []
        check = []
        #com.stm_open()
        com.stm_writeline("A\n") 
        time.sleep(1) 
        data = com.stm_readline()
        print(data)
        data = data.split()
        print(data)
        try:
            if data[0]=='S':
                suviai = int(data[1])
                pertaisymai = int(data[2])
                itampa = float(data[3])
                laikas = float(data[4])/6
                print("surinkta!")
                print(data)
                #com.stm_writeline("E\n")
                time.sleep(1)
                busena_label.setText("Būsena: Surinkta!")
                suviai_label.setText("Šūvių kiekis: %d"%suviai)
                pertaisymai_label.setText("Pertaisymai: %d"%pertaisymai)
                itampa_label.setText("Įtampa: %0.1f V"%itampa)
                laikas_label.setText("Laikas: %0.1f min"%laikas)
        
        except IndexError:
            
            busena_label.setText("Būsena: Klaida. Bandykite vėl.")
            
            #com.stm_reset()
            pass
        '''busena_label.setText("Būsena: Surinkta!")
        suviai_label.setText("Šūvių kiekis: %d"%suviai)
        pertaisymai_label.setText("Pertaisymai: %d"%pertaisymai)
        itampa_label.setText("Įtampa: %0.1f V"%itampa)
        laikas_label.setText("Laikas: %0.1f min"%laikas)'''
    def prisijungti(self):
        global w
        w = AnotherWindow()
        w.show()
            
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()