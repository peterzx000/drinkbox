import sys
from model import estimateAI
import camera.zed as zed
import cv2
import numpy as np
import modbus.modbus_tcp_client as modbus
import time
import UI.UI as UI
sys.path.append('../')


# class Thread(UI.QThread):
#     def __init__(self):
#         super(Thread,self).__init__()
#     def run(self):
#         #

class drink_box:

    def __init__(self) -> None:
        self.configData = {
            "model":{"object":{
                "configPath":"./model/detectron2Configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml",
                "weightPath":"./cookie_model/model_2199999.pth",
                "label":["choc","chocball","dad","box"],
                "threshold":0.9
            }
            }
        }
        self.connect = modbus.modbus('172.31.1.87')
        self.connect.connect()
        self.cam = zed.cam()
        self.aiTubeModel = estimateAI.model(self.configData['model']['object'],'Model',mask=True)
        self.aiTubeModel.action('load')
        self.setUI()

    def setUI(self):
        self.UI = UI.UI()
        self.UI.start.clicked.connect(self.start)
        self.UI.stop.clicked.connect(self.stop)
        self.UI.show()

    def start(self):
        self.connect.write_word()

    def stop(self):
        self.connect.write_word()
    
    def mask2mid(self,mask):
        image = np.zeros([1080,1920,3],dtype=np.uint8)
        image.fill(255)
        for i in range(len(mask[0])):
            cv2.circle(image, mask[0][i],mask[1][i], 1, (0,0,0), 1)
        image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        image = cv2.GaussianBlur(image,(5,5),0)
        image = cv2.Canny(image,50,100)
        contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour = contours[0]
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.05 * perimeter, True)
        
        return (np.sum(approx,axis=0)/4).astype(int)

    def calibration(self,point):
        return point

    def wait_robot(self):
        robot_run = False
        while not robot_run:
            robot_run = self.connect.read_bit()
        self.connect.write_word()

    def auto_place(self):
        pass

    def main(self):
        while True:
            self.cam1()
            self.cam2()
            self.auto_place()

    def cam1(self):
        modelResult = self.modelResult()
        midpoint = self.object_mid(modelResult['mask'])
        min_z = self.highest_point(midpoint,self.depth)
        self.writetype(modelResult['label'][min_z[1]])
        self.sline(midpoint[min_z[1]])

    def modelResult(self):
        self.img,self.depth,self.pc = self.cam.image()
        modelResult = self.aiTubeModel.estimate(self.img)
        while modelResult==[]:
            self.img,self.depth,self.pc = self.cam.image()
            modelResult = self.aiTubeModel.estimate(self.img)
            time.sleep(0.1)
        return modelResult

    def object_mid(self,mask):
        midpoint = []
        for i in mask:
            midpoint.append(self.mask2mid(i))
        return midpoint


    def writetype(self,label):
        if label=='test':
            type_box = 0
        self.connect.write_word(type_box,0)

    def sline(self,point):
        p = self.calibration(point)
        for i in range(3):
            self.connect.write_word(i+1,p[i])

    def cam2(self):
        modelResult = self.modelResult()
        midpoint = self.object_mid(modelResult['mask'])
        min_z = self.highest_point(midpoint,self.depth)
        self.writetype(modelResult['label'][min_z[1]])
        self.sline(midpoint[min_z[1]])

    def highest_point(self,mid,depth):
        min = [9999,-1]
        for j in range(len(mid)):
            i = mid[j]
            if min[0]>depth(i[1],i[0]):
                min[0] = depth(i[1],i[0])
                min[1] = i
        return min