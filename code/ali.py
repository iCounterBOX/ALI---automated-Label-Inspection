# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 11:10:35 2024

@author: kristina

NICE

- Reference-Image mit https://www.makesense.ai/  Annotated ( VOC boundingBox Coordinaten)
- Diese coordinates sind die ROI des etikett - diese regionen sollen via OCR gescannt werden
  train - images
          labes
  (dNd images  dNd Annotations   label.txt muss nur im folder der annotations liegen)        
  Bounding-Box  -->  referenceList       
  
  Cam loop .. checking against this List      

08.06.24:
    cam wird nicht destroyed...nur der frame wird eingefroren
    
    NEW images in image_rc : pyrcc5 -o image_rc.py image.qrc
    Exclusiv with WORD-Test-Protocol
10.06.24: 
    wenigstens irgendwo im ocr string MUSS die referenz stehen - sonst FALSE
    gescant wird jetzt der gesamt ocr-string...der ref-string darf nun auch nur als teilstring auftauchen.
    gerade kleine etiketten führn zu 1-string effekten obwohl es eigentlich 2 wörter sein sollten!
    
13.06.24:
    ToDo - self._df_RefStringData noch den genauen workflow definieren wann ein mess-Zyklus beendet ist.
    wann denn DF zurück setzen..auch die buttons neu verriegeln etc
22.07.24:
    failTimer e.g 10 sec.. if exeeded: automatic failure protocoll

"""

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage

import image_rc  #   5_experimental\ai\py39pa>   pyrcc5 -o image_rc.py image.qrc

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import cv2
import sys
import traceback
import logging
#import random
#from matplotlib import pyplot as plt
from pathlib import Path
from configparser import ConfigParser

import paddle  # drin lassen? auto-py-to-exe?
from paddleocr import PaddleOCR

from classALI import c_ocr 
cocr = c_ocr()   # class ocr
config = ConfigParser()
 
try:     
    ocrModel = PaddleOCR( use_angle_cls =True, lang = 'en', use_gpu=True, det_limit_side_len=3456)    
except Exception as e:   
    print(e)     
  
'''
https://stackoverflow.com/questions/7484454/removing-handlers-from-pythons-logging-loggers
Zäh! einmal angelegt wird der name dem Handler übergeben..das auch NUR in einem unserer Module!
Im notfall wenn sich mal der namen des log ändern sollte, dann den Handler rücksetzen:

'''      
logging.getLogger().removeHandler(logging.getLogger().handlers[0])

logFileName = os.getcwd() + "\\" +"ali.log"
logger = logging.getLogger(logFileName)
logging.basicConfig(filename='ali.log', encoding='utf-8', level=logging.INFO)
#logger.debug('This message should go to the log file')
#logger.info('So should this')
#logger.warning('And this, too')
#logger.error('And non-ASCII stuff, too, like Øresund and Malmö')

#logging.basicConfig(filename= os.getcwd() + "\\" +"ali.log",  level=logging.INFO)
logging.info(cocr.dt() + '******** This is Module ocrTemplateUI.py  GO ***************************')

bestellVorlagen_images="assets/train/images/"
bestellVorlagen_labes="assets/train/labels/" 

protocolsPathOk= "protocolsPath/ok/"
Path(protocolsPathOk).mkdir(parents=True, exist_ok=True)

protocolsPathFail= "protocolsPath/fail/"
Path(protocolsPathFail).mkdir(parents=True, exist_ok=True)

ocrTmpFolder = 'images/tmp/'
Path(ocrTmpFolder).mkdir(parents=True, exist_ok=True)

_camScreenPosX = 50
_camScreenPosY = 50

_BaseDir = os.getcwd()
_UI_FILE = os.path.join(_BaseDir,"ali.ui" )
logging.info(cocr.dt() + 'UI file: ' + _UI_FILE)

_myIniFile = os.getcwd() + "\config.ini"
logging.info(cocr.dt() + 'inifile : ' + _myIniFile)




class MainWindow_ALI(QtWidgets.QMainWindow):    
    def __init__(self):
        #super(MainWindow_ALI,self).__init__()
        super().__init__()

        logging.info(cocr.dt() + 'super(window...init..done')
        # load ui file
        try:  
            uic.loadUi( _UI_FILE, self)
        except Exception as e:
            print(e)
            logging.error(traceback.format_exc())        
        
       
        
        # INI File
        
        '''
        Config file:
        https://stackoverflow.com/questions/19078170/python-how-would-you-save-a-simple-settings-config-file
        standard is webcam 0.. on NB the inbuild cam..1 is normally the external USB cam
        [main]
        webcamnr = 1
        key2 = 4 laterUse
        key3 = 4 futureUse
        '''
        self._camNr = self.lineEdit_camNr.text()
        self.failTimer = self.lineEdit_timer.text()
        
        try:    
            if not config.read(_myIniFile):
                with open(_myIniFile,'a'): pass  # if not exist..create
                config.read(_myIniFile)
                config.add_section('main')
                config.set('main', 'webCamNr', '1')
                config.set('main', 'failTimer', '10')
                config.set('main', 'refList', 'put list here') #https://stackoverflow.com/questions/44778/how-would-you-make-a-comma-separated-string-from-a-list-of-strings
                config.set('main', 'key3', '4 futureUse')  
                with open('config.ini', 'w') as f:
                    config.write(f)   
            if config.read(_myIniFile):
                self._camNr = config.getint('main', 'webCamNr')
                self.failTimer = config.getint('main', 'failTimer')
                print("webCamNr : " + str(self._camNr)) 
                print("failTimer : " + str(self.failTimer)) 
                #pre initialize camNr and Timer
                self.lineEdit_camNr.setText(str(self._camNr))       # in JEDEM Fall müssen die beiden Felder für cam u timer einen gültigen wert haben
                self.lineEdit_timer.setText(str(self.failTimer))
                
                   
        except Exception as e:
             print(e)        
             self._camNr = 0
             logging.error(traceback.format_exc())     
             pass
        logging.info(cocr.dt() + 'Camera Nr __ ' + str(self._camNr) + ' __ is selected')
        
        
        
        #mit self in UI muss nach den elementen in der UI nicht mehr gesucht werden :-)           
        
        #self.pushButton_StartStopCam.clicked.connect(self.loadImage)
        # set control_bt callback clicked  function
        '''
        self.pushButton_StartStopCam.clicked.connect(self.controlTimer)
        self.pushButton_StartStopCam.setText('START CAM')  
        self.pushButton_StartStopCam.setEnabled(True)
        '''
        self.pushButton_StartStopCam.hide() # brauchen start cam nicht mehr
        
        self.pushButton_runTest.clicked.connect(self.enableCamForNextDetection) # RUN
        self.pushButton_runTest.setText('First select Test-Label  and click me (RUN)')  
        self.pushButton_runTest.setEnabled(True)
        
        '''
        self.pushButton_save.clicked.connect(self.saveProtocol )
        self.pushButton_save.setStyleSheet('background-color: red;')
        self.pushButton_save.setText('FAIL')         
        self.pushButton_save.setEnabled(False)
        '''
        self.pushButton_save.hide() # wegen failure timer unnötig geworden
        
        self.listWidget_checkOK.doubleClicked.connect(self.openDocumentInWindows_OKs)
        self.listWidget_checkOK.setSortingEnabled(True)
        self.listWidget_checkOK.sortItems(QtCore.Qt.DescendingOrder)
        
        self.listWidget_checkFail.doubleClicked.connect(self.openDocumentInWindows_FAILs)
        self.listWidget_checkFail.setSortingEnabled(True)
        self.listWidget_checkFail.sortItems(QtCore.Qt.DescendingOrder)
                
        self.listWidget_orderTemplates.clicked.connect(self.previewSelectedListObject)
        self.tableWidget_searchStrings.verticalHeader().setVisible(False)
        
        
        self.textBrowser_log.setText(cocr.dt() + 'Welcome in ALI' ) #Append text to the GUI
        self.textBrowser_log.append('1. Please Select Template' ) 
        self.textBrowser_log.append('2. Please start WebCam' ) #Append text to the GUI
        
        
        pixmap = QtGui.QPixmap(':/image/images/yellow.JPG')
        pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        self.label_ampel.setPixmap(pixmap)
        
        pixmap = QtGui.QPixmap(':/image/images/webcamMini.png')
        pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        self.label_miniCamView.setPixmap(pixmap)
         
        
        #template vorladen
        self._objImgWindowWidth = 640
        self._objImgWindowHeight = 480
        
        self.i_sec = 0
        self.fps=0
        self.started = False
        self.frameCnt = 0   
        self.stopCauseApproved = True
        self._imgPaddleOCR = cv2
       
       
        cocr._ocrModel = ocrModel
        cocr.label_ampel =  self.label_ampel  # label zuweisen.. zugriff auf UI via class!
        cocr.label_currentSelectedTemplate = self.label_currentSelectedTemplate
        cocr.lbl_previewOrderTemplateImage = self.lbl_previewOrderTemplateImage
        cocr.tableWidget_searchStrings = self.tableWidget_searchStrings
        cocr._bestellVorlagen_labes = bestellVorlagen_labes      
        cocr.textBrowser_log = self.textBrowser_log
        
        
        # Install an event filter to capture mouse events
        self.centralwidget.installEventFilter(self)
                
        self.listOrderTemplates()     
        self.listPositivReports()
        self.listNegativReports()
        self.previewSelectedListObject()
        
        # create a timer  * TIMER 
        self.timer = QtCore.QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        self.controlTimer()  # cam soll gleich starten .. zeitgleich die labelauswahl  ..los gehts
        
        
        self.timer2 = QTimer()  # failure timer..zeigt im lcd die sekunden an
        self.timer2.setInterval(1000)
        self.timer2.timeout.connect(self.updateLCD)  
        self.timer2.stop() 
    
    # lcd zeigt die secunden an
    def updateLCD(self):
        self.i_sec += 1
        self.lcdNumber_lcd.display(self.i_sec)
        self.lcdNumber_lcd.repaint()
        
    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        self.pushButton_save.setEnabled(True)       
        self.webcam_Found = True          
        if not self.timer.isActive():
            # webCam high resolution ergab nicht bessere results..image war extrem klein..bracht noch
            # gesonderte recherche mit speziellen auflösungen...siehe cartoonCamOnMovie e.g
             
            if cocr.testDevice(int(self.lineEdit_camNr.text())) == False:  # no printout if cam (0) is available
                #toolz.msgBoxInfoOkCancel("Webcam (1) NOT found!","Webcam ISSUE - PLEASE CHECK!")
                cocr.msgBoxInfoOkCancel("NO Webcam available","Webcam I S S U E - PLEASE CHECK!")
                return  
          
            self.cap = cv2.VideoCapture(int(self.lineEdit_camNr.text()) )           
            self.cap.set(5,30)
            
            # start timer
            self.timer.start(30)    #e.g. 10
            # update control_bt text
            ##self.pushButton_runTest.setEnabled(False)
            self.pushButton_save.setEnabled(True)
            self.pushButton_StartStopCam.setText("Stop Cam")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            #self.out.release()
            # update control_bt text
            self.pushButton_StartStopCam.setText("Start Cam" )
            #self.ui.image_label.setText("Camera")

         
       
    # WORD file mit double click öffnen
    def openDocumentInWindows(self, path, lstWidget):
        logging.info(cocr.dt() + 'openDocumentInWindows()') 
        try:
            cur_index = lstWidget.currentRow()
            item = lstWidget.item(cur_index)   
            if item is not None:                   
                    path_of_WordProtocol = os.getcwd() + '/' + path + item.text()
                    os.startfile(path_of_WordProtocol)
        except Exception as e:
            print(e)
            logging.error(traceback.format_exc())    
    def openDocumentInWindows_OKs(self):    
        self.openDocumentInWindows(protocolsPathOk , self.listWidget_checkOK )    
    def openDocumentInWindows_FAILs(self):    
        self.openDocumentInWindows(protocolsPathFail, self.listWidget_checkFail )
            
           
    
    # handle the red cross event
    def closeEvent(self, event): 
        try:
            self.started = False            
            logging.shutdown()
            self.close()            
            #QtWidgets.QApplication.quit()
            #QtWidgets.QCoreApplication.instance().quit()            
            event.accept()
            print('Window closed')
            
            #sys.exit() # die beiden KILL python ALL - restart Kernel :-)
            
        except Exception as e:
            print(e)
            logging.error(traceback.format_exc())        
        

    def listOrderTemplates(self):        
        logging.info(cocr.dt() + 'listOrderTemplates()')  
        included_extensions = ['jpg','jpeg', 'png', 'JPG']
        file_list = [fn for fn in os.listdir(bestellVorlagen_images)
              if any(fn.endswith(ext) for ext in included_extensions)]
        self.listWidget_orderTemplates.clear()
        self.listWidget_orderTemplates.addItems(file_list)
        self.listWidget_orderTemplates.setCurrentRow(0)
        self.listWidget_orderTemplates.repaint()
        QtCore.QCoreApplication.processEvents()
        
    def listPositivReports(self):        
        logging.info(cocr.dt() + 'listPositivReports()')  
        included_extensions = ['docx']
        file_list = [fn for fn in os.listdir(protocolsPathOk)
              if any(fn.endswith(ext) for ext in included_extensions)]
        self.listWidget_checkOK.clear()
        self.listWidget_checkOK.addItems(file_list)
        self.listWidget_checkOK.setCurrentRow(0)
        self.listWidget_checkOK.repaint()
        QtCore.QCoreApplication.processEvents()  
        
    def listNegativReports(self):        
        logging.info(cocr.dt() + 'listNegativReports()')  
        included_extensions = ['docx']
        file_list = [fn for fn in os.listdir(protocolsPathFail )
              if any(fn.endswith(ext) for ext in included_extensions)]
        self.listWidget_checkFail.clear()
        self.listWidget_checkFail.addItems(file_list)
        self.listWidget_checkFail.setCurrentRow(0)
        self.listWidget_checkFail.repaint()
        QtCore.QCoreApplication.processEvents()    
    
    

    #https://python-docx.readthedocs.io/en/latest/   
    
    #ToDo: kürzen..item ist im label  orror free or not über die df matrix!!
                
    def saveProtocol(self ):
        logging.info(cocr.dt() + 'saveProtocol()') 
        try:
            # we show the rectange over the originalTemplate searchStrings 
            path_of_image = self.label_currentSelectedTemplate.text()
            
            ocrTmpFile = ocrTmpFolder + 'imgPaddleOCR.png'   # images/tmp/imgPaddleOCR.png  for the 
            cv2.imwrite(ocrTmpFile, self._imgPaddleOCR)    
            
            secs = cocr.dateDifSeconds()
            wordFileName =  str(secs) + "_" +  os.path.splitext(os.path.basename(path_of_image))[0] + ".docx"       # 40075_emb_06A_01_ed_292481.docx
            
            if cocr.isAllFoundTrue(): # Error-Free - ALL pattern found
                protocolsPath = protocolsPathOk   # protocolsPath/ok/
                self.listWidget_checkOK.addItem(wordFileName)   # 40075_emb_06A_01_ed_292481.docx
                self.listWidget_checkOK.setCurrentRow(0)
                self.listWidget_checkOK.repaint()  
            else:
                protocolsPath = protocolsPathFail
                self.listWidget_checkFail.addItem(wordFileName)
                self.listWidget_checkFail.setCurrentRow(0)
                self.listWidget_checkFail.repaint()   
            
            cocr.writeWordProtocol(protocolsPath, path_of_image, wordFileName, ocrTmpFile)     
        except Exception as e:
            print(e)  
    
    
    def previewSelectedListObject(self):   
        self.i_sec = 0
        logging.info(cocr.dt() + 'previewSelectedListObject')
        cur_index = self.listWidget_orderTemplates.currentRow()
        item = self.listWidget_orderTemplates.item(cur_index)   
        if item is not None:        
            try: # To avoid divide by 0 we put it in try except
                ss =  'Current User Selection:' + item.text()
                logging.info(cocr.dt() + ss)
                self.textBrowser_log.append( ss) #Append text to the GUI              
                
                path_of_image = bestellVorlagen_images + item.text()
                self.label_currentSelectedTemplate.setText(path_of_image) 
                cocr.reNewPreviewRefBufferAndList() # preview Bestellvorlage AND reload referenceBuffer (DF)
                
            except Exception:
                traceback.print_exc()
    
    # gefunden.. neuen test freigen..appoval zurück setzen - run button
    def enableCamForNextDetection(self):
        self.pushButton_runTest.setText('New Label-Scan') 
        self.pushButton_runTest.setEnabled(False)
        self.stopCauseApproved = False
        self.previewSelectedListObject() # reset searchstring table        
        # LCD startet mit dem timer bei null ..zählt sec hoch        
        self.i_sec = 1
        self.lcdNumber_lcd.display(self.i_sec)
        self.timer2.start(1000)        
        print("current failTimer:" +  str(self.i_sec) )
       
    
    
    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, frame = self.cap.read()
        
        if ret == True:       
            self.update (frame) # zum filter window
        # Non-Stop-Video-Stream .. 
        framex = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(framex, framex.shape[1],framex.shape[0],framex.strides[0],QImage.Format_RGB888) 
        pixmap = QtGui.QPixmap.fromImage(img)
        pixmap = pixmap.scaled(300,300, QtCore.Qt.KeepAspectRatio)       
        self.label_miniCamView.setPixmap(pixmap)   
        
     
            
    def update(self, capFrame):
        """ This function will update the photo according to the 
            current values of blur and brightness and set it to photo label.
        """     
        # frame der cam
        
        if self.stopCauseApproved == False:  
            try:
                self._imgPaddleOCR = cocr.pp_ocrOnSingleImageCV2(_camScreenPosX, _camScreenPosY, ocrModel, capFrame)  #OCR + AMPEL      
                
                ################ imgPaddleOCR = capFrame # nur testen wegen crash in exe
               
                if cocr.isAllFoundTrue() == True:                
                    # write  proved over  the captureFrame 
                    font = cv2.FONT_HERSHEY_COMPLEX
                    cv2.putText(self._imgPaddleOCR,'APPROVED',(50,100),font,2,(50,205,50),3)  #text,coordinate,font,size of text,color,thickness of font
                    print('GEFUNDEN') 
                    # stop camera
                    self.timer2.stop()
                    self.stopCauseApproved = True   
                    self.pushButton_runTest.setEnabled(True)
                    self.pushButton_save.setEnabled(False)
                    self.textBrowser_log.append( 'LABEL OK - Select New Template and press RUN!') #Append text to the GUI                   
                    self.saveProtocol()  # errFree  True  
                else:
                    print('NICHT gefunden')
                    #here we check the failure timeout
                    if self.i_sec > int(self.lineEdit_timer.text()):    
                        self.timer2.stop()
                        self.stopCauseApproved = True   # freeze images
                        self.pushButton_runTest.setEnabled(True)
                        self.pushButton_save.setEnabled(False)
                        self.textBrowser_log.append( 'LABEL Failure - Could not detect Label on object in TIME!') #Append text to the GUI                   
                        self.saveProtocol()  # save failure protocol
                        cocr.msgBoxInfoOkCancel("Click RUN to start a new Label-Scan when ready!","failTimer - Automatic FailureProtocol!")
                    
                #image = imutils.resize(image,width=640)
                frame = cv2.cvtColor(self._imgPaddleOCR, cv2.COLOR_BGR2RGB)
                img = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)        
                pixmap = QtGui.QPixmap.fromImage(img)
                pixmap = pixmap.scaled(1200, 720, QtCore.Qt.KeepAspectRatio)                
                self.label_cameraLive.setPixmap(pixmap)    
            except Exception as e:
                print(e)
                logging.error(traceback.format_exc())    
            
          

#THIS sector is needed for stand alone mode 
        
def app():
    app = QtWidgets.QApplication(sys.argv)        
    win = MainWindow_ALI()
    win.show()    
    sys.exit(app.exec_())

app()   

 
        