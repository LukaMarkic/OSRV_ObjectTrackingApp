
import numpy as np
import cv2
import os
import time
import datetime
from window_create import selectTracker
from video_select import getVideo
from window_create import chooseToRecord

#Metoda za crtanje pravokutnika koji prati objekt
def drawBox(box, frame, frameColor = (0,255,0), frameWidth = 2):
    start_point = (int(box[0]), int(box[1]))
    end_point = (int(box[0] + box[2]), int(box[1] + box[3]))
    cv2.rectangle(frame, start_point, end_point, frameColor, frameWidth)

#Metoda za centrirani prikaz tekstualnog zapisa na zaslonu
def putCenteredText(text, frame, resolution, color = (10,10,10), width = 1):
    textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, .65, 1)[0]
    cv2.putText(frame, text, ((resolution[0]-textsize[0])//2-textsize[0]//2, (resolution[1]-textsize[1])-10), cv2.FONT_HERSHEY_SIMPLEX, .65, color, width)



#Predefinirane vrijednosti
prev_frame_time = 0
new_frame_time = 0
spaceKey = 32  #ASCII vrijadnost razmaka
exitKey = 27   #ASCII vrijednost tipke ESC
OBJECT_TRACKERS = {
	"CSRT": cv2.legacy.TrackerCSRT_create,
	"KCF": cv2.legacy.TrackerKCF_create,
	"BOOSTING": cv2.legacy.TrackerBoosting_create,
	"MIL": cv2.legacy.TrackerMIL_create,
	"TLD": cv2.legacy.TrackerTLD_create,
	"MEDIANFLOW": cv2.legacy.TrackerMedianFlow_create,
	"MOSSE": cv2.legacy.TrackerMOSSE_create
}


#Dohvati video sekvencu i metodu (algoritam) praćenja objekta te odabir opcionalne pohrane
filePath = getVideo()
trackerType = selectTracker()
recordVideoStatus = chooseToRecord()
fileName = (os.path.basename(filePath).split('/')[-1]).split('.')[0]

#Provjera je li postoji unutar output direktorija direktorij s nazivom odabrane metode praćenja u kojem će biti spremljeni video zapisi
outputDirectoryExist = os.path.exists(f'output//{trackerType}')
if recordVideoStatus and not outputDirectoryExist:
    os.makedirs(f'output//{trackerType}')

#Učitaj video i omogući zapisivanje video sekvence
video = cv2.VideoCapture(filePath)
ret, frame = video.read()
fpsVideo = video.get(cv2.CAP_PROP_FPS)
print(f'FPS ucitanog video zapisa je: {fpsVideo}')
resolution = (int(video.get(3)),int(video.get(4)))

#Pokreni snimanje video zapisa ako je navedeno odabrano
if recordVideoStatus:
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    saveFilePath = f'.//output//{trackerType}//video_tracking_{fileName}-{trackerType} {datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.mp4'
    output = cv2.VideoWriter(saveFilePath, fourcc, fpsVideo, resolution)

if not ret:
    print('Nije moguće otvoriti video')

#Inicializacija multitracker instance
trackers = cv2.legacy.MultiTracker_create()

#Prolazak kroz svaki kadar snimke video sekvence
while(1):
    _, frame = video.read()
    if frame is None:
        break
    
    #Izračun FPS-a
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time

    #Za svaki kadar osvježimo dostupnu instancu trackers
    ret, boxes = trackers.update(frame)

    if ret:
        for box in boxes:
            drawBox(box, frame)
         
    else:

        #Detektriramo objekte u instanci trackers čiji je okvir različit od nule te osvježimo instancu trackers postavljenjem tih objekata u instancu
        #ovo je potrebno odraditi kako bi se obogućio prikaz više objekata kada individualni tracker prestane pratiti objekt
        
        bound_boxes = trackers.getObjects()
        index = np.where(bound_boxes.sum(axis= 1) != 0)[0]
        bound_boxes = bound_boxes[index]
        trackers = cv2.legacy.MultiTracker_create()
        for bound_box in bound_boxes:
            trackers.add(tracker,frame,bound_box)
            
        cv2.putText(frame, "Pogreska pri pracenju objekta!", (120,60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,0,255),1)

    #Prikaz tipa algoritam za praćenje i vrijednosti parametra FPS na zaslonu
    cv2.putText(frame, f"Tracker type: {trackerType}", (20,30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (50,170,50), 2)
    cv2.putText(frame, "FPS : " + str(int(fps)), (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (50,170,50),2)
    
    key = cv2.waitKey(30)
    
    if key == exitKey:
        break

    #pritisni s ili S kako bi se video sekvenca pauzirala
    elif key == ord("s") or key == ord("S"):
        while(1):

            putCenteredText(text = "Za izlaz iz pauziranog moda dvostruko pritisnite razmak [space]" , frame = frame, resolution = resolution)
            
            #Odaberi okvira (Region of intrest - ROI) oko objekata kojeg želimo pratiti
            roi = cv2.selectROI(f"Pracenje objekata - {trackerType}", frame, fromCenter=False, showCrosshair=True)
            cv2.rectangle(frame, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0,255,0), 2)
           

            #Ako smo odabrali objekt predaj ga instaci trackers
            if(roi[2] != 0 and roi[3] != 0):
                tracker = OBJECT_TRACKERS[trackerType]()
                trackers.add(tracker, frame, roi) 
            
            #Provjeri je pritisnuta tipka space kako bi se nastavila video sekvenca
            secondKey = cv2.waitKey()
            if secondKey == spaceKey:
                break
    else:
        putCenteredText(text = "Za pauziranje pritisnite tipku s", frame = frame, resolution = resolution)
        
    cv2.imshow(f"Pracenje objekata - {trackerType}", frame)
    if recordVideoStatus:
        output.write(frame)

video.release()
#Spremi video sekvencu i zatvori zaslone
if recordVideoStatus:
    output.release()
cv2.destroyAllWindows()


