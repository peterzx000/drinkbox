from tkinter.constants import N
from detectron2.config import get_cfg
from detectron2.engine.defaults import DefaultPredictor
from detectron2.data import DatasetCatalog,MetadataCatalog
from detectron2.utils.visualizer import Visualizer,GenericMask
import time
import numpy as np


class model:
    def __init__(self,config,modelName,mask=False):
        self.cfg = get_cfg()
        self.cfg.merge_from_file(config['configPath'])
        self.cfg.INPUT.FORMAT = 'RGB'      
        self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(config['label'])
        # self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
        self.cfg.MODEL.WEIGHTS = config['weightPath']
        self.cfg.freeze()
        self.predicter = None
        DatasetCatalog.register(modelName, self.mataDataFunc)
        MetadataCatalog.get(modelName).set(thing_classes=config['label'])
        self.metadata = MetadataCatalog.get(modelName)
        self.threshold = config['threshold']
        self.isMask = mask
    def mataDataFunc(self):
        return {}
    def action(self,act):
        if act=='load':
            if self.predicter==None:
                self.predicter = DefaultPredictor(self.cfg)
                return 'AI model loading finish'
            else:
                return 'Model is loaded'
        elif act=='del':
            if self.predicter!=None:
                self.predicter=None
                return 'Delete AI model finish'
            else:
                return 'Model is None'
            
    def estimate(self,image):
        if self.predicter!=None:
            startTime = time.time()
            output = self.predicter(image)
            endTime = (time.time()-startTime)
            fps = int(1/endTime)
            output = output['instances'].to('cpu')
            output = output[output.scores > self.threshold]
            if len(output)>0:
                visualizer = Visualizer(image, metadata=self.metadata)
                modelOutImg = visualizer.draw_instance_predictions(output).get_image()
                # polygons = visualizer._convert_masks(output._fields['pred_masks'])
                bbox=[]
                objectClass = output.pred_classes.numpy().tolist()
                for b in output.pred_boxes.__iter__():
                    bbox.append(b.numpy().astype('int').tolist())


                if self.isMask:
                    maskSource = np.array(output.pred_masks)
                    allMask=[]
                    for m in maskSource:
                        maskIndex = np.where(m==True)
                        
                        mask = [maskIndex[1],maskIndex[0]]
                        allMask.append(mask)
                    return {'image':modelOutImg,'bbox':bbox,'objectClass':objectClass,'fps':fps,'mask':allMask,'label':visualizer.label}
                    
                else:
                    return {'image':modelOutImg,'bbox':bbox,'objectClass':objectClass,'fps':fps}
                
            else:
                return []
        else:
            print('nothing')
            return []