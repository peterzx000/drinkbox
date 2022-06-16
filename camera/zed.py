import sys
from cv2 import IMWRITE_EXR_TYPE_FLOAT
import pyzed.sl as sl

class cam:
    
    def __init__(self):

        # Create a ZED camera object
        self.zed = sl.Camera()

        # Set configuration parameters
        input_type = sl.InputType()
        if len(sys.argv) >= 2 :
            input_type.set_from_svo_file(sys.argv[1])
        init = sl.InitParameters(input_t=input_type)
        # init.camera_resolution = sl.RESOLUTION.HD1080
        init.camera_resolution = sl.RESOLUTION.HD2K
        # init.depth_mode = sl.DEPTH_MODE.PERFORMANCE
        init.camera_fps = 1
        init.depth_mode = sl.DEPTH_MODE.ULTRA
        init.coordinate_units = sl.UNIT.MILLIMETER

        # Open the camera
        err = self.zed.open(init)
        if err != sl.ERROR_CODE.SUCCESS :
            print(repr(err))
            self.zed.close()
            exit(1)

        # Set runtime parameters after opening the camera
        self.runtime = sl.RuntimeParameters()
        # self.runtime.sensing_mode = sl.SENSING_MODE.FILL
        self.runtime.sensing_mode = sl.SENSING_MODE.STANDARD
        self.image_size = self.zed.get_camera_information().camera_resolution

        # image_size.width = image_size.width /2
        # image_size.height = image_size.height /2

        # Declare your sl.Mat matrices
        self.image_zed = sl.Mat(self.image_size.width, self.image_size.height, sl.MAT_TYPE.U8_C4)
        self.depth_zed = sl.Mat(self.image_size.width, self.image_size.height, sl.MAT_TYPE.F32_C1)
        self.point_cloud = sl.Mat()


    def image(self) :

        err = self.zed.grab(self.runtime)
        if err == sl.ERROR_CODE.SUCCESS :
            # Retrieve the left image, depth image in the half-resolution
            self.zed.retrieve_image(self.image_zed, sl.VIEW.LEFT, sl.MEM.CPU, self.image_size)
            self.zed.retrieve_measure(self.depth_zed, sl.MEASURE.DEPTH)
            self.zed.retrieve_measure(self.point_cloud, sl.MEASURE.XYZRGBA, sl.MEM.CPU, self.image_size)
            # To recover data from sl.Mat to use it with opencv, use the get_data() method
            # It returns a numpy array that can be used as a matrix with opencv
            image_ocv = self.image_zed.get_data()
            depth_ocv = self.depth_zed.get_data()
            # cv2.imshow("output", image_ocv)

            return image_ocv,depth_ocv,self.point_cloud