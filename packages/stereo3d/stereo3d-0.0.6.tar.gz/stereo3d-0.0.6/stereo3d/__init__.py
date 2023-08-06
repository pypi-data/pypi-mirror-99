"""Stereo3D module"""
import os
import sys
import time
import traceback
import numpy as np
import cv2
from pymsgbox import prompt, alert
from pyntcloud import PyntCloud
try:
    from i3drsgm import I3DRSGM
    I3DRSGM_IMPORTED = True
except ImportError:
    I3DRSGM = None
    I3DRSGM_IMPORTED = False
import pandas as pd


class Stereo3D():
    def __init__(self, stereo_camera, stereo_calibration,
                 stereo_matcher=None, show_window=True):
        """
        Initialisation function for PickPlace3D. Defines the devices used.
        If you would like to use the methods without connecting
        a camera then initaialise Stereo3D as 's3D = Stereo3D()'.
        :param left_cal_file:
            filepath to left image calibration file (e.g. left.yaml)
        :param right_cal_file:
            filepath to right image calibration file (e.g. right.yaml)
        :param stereo_camera:
            stereo camera used for generating 3D and 2D detection
        :type left_cal_file: string
        :type right_cal_file: string
        :type stereo_camera: StereoCapture.StereoCapture
        """
        self.change_camera(stereo_camera)
        self.stereo_calibration = stereo_calibration
        self.Q = self.stereo_calibration.stereo_cal["q"]

        self.image_left = None
        self.image_right = None
        self.rect_image_left = None
        self.rect_image_right = None
        self.disparity = None
        self.depth = None

        self.EXIT_CODE_QUIT = -1
        self.EXIT_CODE_GRAB_3D_SUCCESS = 1
        self.EXIT_CODE_FAILED_TO_GRAB_3D = -2

        self.save_index = 0

        self.cv_window_name_Controls = "[Stereo3D] Controls"
        self.cv_window_name_Images = "[Stereo3D] Images"

        self.show_window = show_window
        if self.show_window:
            cv2.namedWindow(self.cv_window_name_Controls, cv2.WINDOW_NORMAL)
            # cv2.namedWindow(self.cv_window_name_Images, cv2.WINDOW_NORMAL)

            cv2.setMouseCallback(
                self.cv_window_name_Images, self.on_window_mouse)

            cv2.resizeWindow(self.cv_window_name_Controls, 400, 0)

        self.matcher_name = ""
        self.change_matcher(stereo_matcher)

        # Once init has been called matcher can be changed e.g.
        # s3D = Stereo3D()
        # s3D.ply_header = "ply..."
        self.ply_header = (
            "ply\n"
            "format ascii 1.0\n"
            "element vertex %(vert_num)d\n"
            "property float x\n"
            "property float y\n"
            "property float z\n"
            "property uchar red\n"
            "property uchar green\n"
            "property uchar blue\n"
            "end_header\n")

        self.frame_count = 0

    def change_camera(self, stereo_camera):
        self.stereo_camera = stereo_camera

    def change_matcher(self, stereo_matcher):
        default_min_disp = 1000
        default_num_disparities = 20
        default_block_size = 12
        default_uniqueness_ratio = 15
        default_texture_threshold = 15
        default_speckle_size = 0
        default_speckle_range = 500

        if (stereo_matcher is None):
            self.matcher = cv2.StereoBM_create()
            calc_block = (2 * default_block_size + 5)
            self.matcher.setBlockSize(calc_block)
            self.matcher.setMinDisparity(int(default_min_disp - 1000))
            self.matcher.setNumDisparities(16*(default_num_disparities+1))
            self.matcher.setUniquenessRatio(default_uniqueness_ratio)
            self.matcher.setTextureThreshold(default_texture_threshold)
            self.matcher.setSpeckleWindowSize(default_speckle_size)
            self.matcher.setSpeckleRange(default_speckle_range)
        else:
            if stereo_matcher == "BM":
                self.matcher_name = stereo_matcher
                self.matcher = cv2.StereoBM_create()
                calc_block = (2 * default_block_size + 5)
                self.matcher.setBlockSize(calc_block)
                self.matcher.setMinDisparity(int(default_min_disp - 1000))
                self.matcher.setNumDisparities(16*(default_num_disparities+1))
                self.matcher.setUniquenessRatio(default_uniqueness_ratio)
                self.matcher.setTextureThreshold(default_texture_threshold)
                self.matcher.setSpeckleWindowSize(default_speckle_size)
                self.matcher.setSpeckleRange(default_speckle_range)
            elif stereo_matcher == "SGBM":
                self.matcher_name = stereo_matcher
                self.matcher = cv2.StereoSGBM_create()
                calc_block = (2 * default_block_size + 5)
                self.matcher.setBlockSize(calc_block)
                self.matcher.setMinDisparity(int(default_min_disp - 1000))
                self.matcher.setNumDisparities(16*(default_num_disparities+1))
                self.matcher.setUniquenessRatio(default_uniqueness_ratio)
                # self.matcher.setTextureThreshold(default_texture_threshold)
                self.matcher.setSpeckleWindowSize(default_speckle_size)
                self.matcher.setSpeckleRange(default_speckle_range)
            elif stereo_matcher == "I3DRSGM":
                if I3DRSGM_IMPORTED:
                    self.matcher_name = stereo_matcher
                    self.matcher = I3DRSGM()
                    self.matcher.setWindowSize(11)
                    self.matcher.setMinDisparity(0)
                    self.matcher.setDisparityRange(16*120)
                    self.matcher.setPyamidLevel(6)
                else:
                    raise Exception("Failed to import I3DRSGM")
            else:
                self.matcher = stereo_matcher

        if self.show_window:
            cv2.destroyWindow(self.cv_window_name_Controls)
            cv2.namedWindow(self.cv_window_name_Controls, cv2.WINDOW_NORMAL)

            cv2.createTrackbar(
                "Min disp", self.cv_window_name_Controls,
                default_min_disp, 2000, self.on_min_disparity_trackbar)
            cv2.createTrackbar(
                "Disp", self.cv_window_name_Controls,
                default_num_disparities, 30, self.on_num_disparities_trackbar)
            cv2.createTrackbar(
                "Blck sze", self.cv_window_name_Controls,
                default_block_size, 100, self.on_block_size_trackbar)

            cv2.createTrackbar(
                "Uniq", self.cv_window_name_Controls,
                default_uniqueness_ratio, 100,
                self.on_uniqueness_ratio_trackbar)
            if stereo_matcher == "BM":
                cv2.createTrackbar(
                    "Texture", self.cv_window_name_Controls,
                    default_texture_threshold, 100,
                    self.on_texture_threshold_trackbar)

            cv2.createTrackbar(
                "Sp size", self.cv_window_name_Controls,
                default_speckle_size, 500, self.on_speckle_size_trackbar)
            cv2.createTrackbar(
                "Sp range", self.cv_window_name_Controls,
                default_speckle_range, 1000, self.on_speckle_range_trackbar)

    def connect(self):
        """
        Connect to devices needed for the pick and place process.
        :returns: success
        :rtype: bool
        """
        res = self.stereo_camera.connect()
        return res

    def gen3D(self, left_image, right_image):
        if self.matcher_name == "I3DRSGM":
            if I3DRSGM_IMPORTED:
                _, disparity = self.matcher.forwardMatch(left_image, right_image)
                disparity = -disparity.astype(np.float32)
                disparity[disparity==99999]=0.0
                disparity[disparity<=0]=0.0
                disparity = np.nan_to_num(disparity, nan=0.0,posinf=0.0,neginf=0.0)
            else:
                raise Exception("Failed to import I3DRSGM")
        else:
            disparity = self.matcher.compute(left_image, right_image)
            disparity = disparity.astype(np.float32) / 16.0
        return disparity

    def genDepth(self, disparity):
        depth = cv2.reprojectImageTo3D(disparity, self.Q)
        return depth

    def write_ply(self, filename, disp, depth, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.float32(image)
        image = image/255

        mask = disp > disp.min()
        points = depth[mask]
        image = image[mask]

        # TODO replace this with better filter in-case
        # 3D is every large an this becomes invalid
        points[points >= 100] = 0
        points[points <= -100] = 0

        points = points.reshape(-1, 3)
        image = image.reshape(-1, 3)

        points = np.hstack((points, image))

        cloud = PyntCloud(pd.DataFrame(
            # same arguments that you are passing to visualize_pcl
            data=points,
            columns=["x", "y", "z", "red", "green", "blue"]))

        cloud.to_file(filename)

    def scale_disparity(self, disparity):
        minV, maxV, _, _ = cv2.minMaxLoc(disparity)
        if maxV - minV != 0:
            scaled_disp = cv2.convertScaleAbs(
                disparity, alpha=255.0/(maxV - minV),
                beta=-minV * 255.0/(maxV - minV))
            return scaled_disp
        else:
            return np.zeros(disparity.shape, np.uint8)

    def on_min_disparity_trackbar(self, val):
        min_disp = int(val - 1000)
        self.matcher.setMinDisparity(min_disp)

    def on_block_size_trackbar(self, val):
        if self.matcher_name == "I3DRSGM":
            if I3DRSGM_IMPORTED:
                self.matcher.setWindowSize(2 * val + 5)
            else:
                raise Exception("Failed to import I3DRSGM")
        else:
            self.matcher.setBlockSize(2 * val + 5)

    def on_num_disparities_trackbar(self, val):
        if self.matcher_name == "I3DRSGM":
            if I3DRSGM_IMPORTED:
                self.matcher.setDisparityRange(16*((val*10)+1))
            else:
                raise Exception("Failed to import I3DRSGM")
        else:
            self.matcher.setNumDisparities(16*(val+1))

    def on_texture_threshold_trackbar(self, val):
        if self.matcher_name != "I3DRSGM":
            self.matcher.setTextureThreshold(val)

    def on_uniqueness_ratio_trackbar(self, val):
        if self.matcher_name != "I3DRSGM":
            self.matcher.setUniquenessRatio(val)

    def on_speckle_size_trackbar(self, val):
        if self.matcher_name != "I3DRSGM":
            self.matcher.setSpeckleWindowSize(val)

    def on_speckle_range_trackbar(self, val):
        if (self.matcher_name != "I3DRSGM"):
            self.matcher.setSpeckleRange(val)

    def on_window_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("click")

    def grab3D(self, isRectified=False):
        res, image_left, image_right = self.stereo_camera.grab()
        if res:
            self.image_left = image_left
            self.image_right = image_right
            if isRectified:
                self.rect_image_left = self.image_left
                self.rect_image_right = self.image_right
            else:
                self.rect_image_left, self.rect_image_right = \
                    self.stereo_calibration.rectify_pair(
                        image_left, image_right)

            disp = self.gen3D(self.rect_image_left, self.rect_image_right)
            self.disparity = disp

            return True, disp
        else:
            print("Failed to grab stereo image pair")
            return False, None

    def save_point_cloud(self, disparity, image,
                         defaultSaveFolder="", points_file_string="output.ply",
                         confirm_folder=True):
        # prompt user for save location
        resp = defaultSaveFolder
        if confirm_folder:
            try:
                resp = prompt(
                    text='Saving 3D Point Cloud to path: ',
                    title='Save 3D Point Cloud', default=defaultSaveFolder)
            except AssertionError:
                _, _, tb = sys.exc_info()
                traceback.print_tb(tb)  # Fixed format
                tb_info = traceback.extract_tb(tb)
                filename, line, func, text = tb_info[-1]

                err_msg = 'An error occurred on line {} in statement {}'
                err_msg = err_msg.format(line, text)
                print(err_msg)
                err_msg = 'Will use default save folder: {}'
                err_msg = err_msg.format(defaultSaveFolder)
                print(err_msg)
        if (resp is not None and disparity is not None and image is not None):
            # define name of output point cloud ply file
            ply_filename = os.path.join(resp, points_file_string)

            # generate depth from disparity
            print("Generating depth from disparity...")
            depth = self.genDepth(disparity)
            print("Saving point cloud...")
            # write 3D data to ply with color from image on points
            self.write_ply(ply_filename, disparity, depth, image)
            print("Point cloud save complete.")
            if confirm_folder:
                alert('3D point cloud saved.', 'Save 3D Point Cloud')
        else:
            print("invalid prompt response or disparity/image is empty")

    def save_all_current(self, saveFolder):
        confirm_folder = False
        left_file_string = str(self.save_index)+"_l.png"
        right_file_string = str(self.save_index)+"_r.png"
        self.stereo_camera.save_images(
            self.image_left, self.image_right,
            saveFolder, left_file_string, right_file_string,
            confirm_folder)

        left_file_string = "rect_"+str(self.save_index)+"_l.png"
        right_file_string = "rect_"+str(self.save_index)+"_r.png"
        self.stereo_camera.save_images(
            self.rect_image_left, self.rect_image_right,
            saveFolder, left_file_string, right_file_string,
            confirm_folder)

        points_file_string = "points_"+str(self.save_index)+".ply"
        self.save_point_cloud(
            self.disparity, self.rect_image_left,
            saveFolder, points_file_string, confirm_folder)

    def run_frame_no_gui(self, saveFolder, isRectified=False):
        # grab 3D disparity from stereo camera
        res, _ = self.grab3D(isRectified)
        if res:
            self.save_all_current(saveFolder)
        return res

    def run_frame(self, defaultSaveFolder="", isRectified=False,
                  confirm_folder=True, colormap=cv2.COLORMAP_JET):
        # grab 3D disparity from stereo camera
        res, disp = self.grab3D(isRectified)
        if res:
            self.frame_count += 1
            # prepare images for displaying
            display_image = np.zeros((640, 480), np.uint8)

            rect_image_left_resized = \
                self.stereo_camera.image_resize(
                    self.rect_image_left, height=640)
            rect_image_right_resized = \
                self.stereo_camera.image_resize(
                    self.rect_image_right, height=640)

            disp_resized = self.scale_disparity(
                self.stereo_camera.image_resize(disp, height=640))
            disp_black_mask = disp_resized <= 0
            # apply color map to disparity
            disp_colormap = cv2.applyColorMap(disp_resized, colormap)
            disp_colormap[disp_black_mask != 0] = [0, 0, 0]

            left_right_dual_gray = np.concatenate(
                (rect_image_left_resized, rect_image_right_resized), axis=1)
            left_right_dual = cv2.cvtColor(
                left_right_dual_gray, cv2.COLOR_GRAY2RGB)

            (lr_dual_h, lr_dual_w, _) = left_right_dual.shape
            (d_h, d_w, _) = disp_colormap.shape

            spacer_width_raw = (lr_dual_w - d_w)
            if (spacer_width_raw % 2) == 0:
                # even
                spacer_width_1 = int((spacer_width_raw / 2))
                spacer_width_2 = int((spacer_width_raw / 2))
            else:
                # odd
                spacer_width_1 = int((spacer_width_raw / 2))
                spacer_width_2 = int((spacer_width_raw / 2) + 1)

            disp_spacer_1 = np.zeros((640, spacer_width_1, 3), np.uint8)
            disp_spacer_2 = np.zeros((640, spacer_width_2, 3), np.uint8)
            disp_spaced = np.concatenate(
                (disp_spacer_1, disp_colormap, disp_spacer_2), axis=1)

            display_image = np.concatenate(
                (disp_spaced, left_right_dual), axis=0)
            display_image_resize = self.stereo_camera.image_resize(
                display_image, height=640)

            font = cv2.FONT_HERSHEY_DUPLEX
            bottomLeftCornerOfText = (10, 20)
            fontScale = 0.4
            fontColor = (255, 255, 255)
            lineType = 1

            cv2.putText(
                display_image_resize, 'Frame: {}'.format(self.frame_count),
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)

            if self.show_window:
                # display disparity with stereo images
                cv2.imshow(self.cv_window_name_Images, display_image_resize)

        k = cv2.waitKey(1)
        if k == ord('q'):  # exit if 'q' key pressed
            return self.EXIT_CODE_QUIT
        elif k == ord('s'):  # save stereo image pair
            left_file_string = str(self.save_index)+"_l.png"
            right_file_string = str(self.save_index)+"_r.png"
            self.stereo_camera.save_images(
                self.image_left, self.image_right,
                defaultSaveFolder, left_file_string, right_file_string,
                confirm_folder)
            self.save_index += 1
        elif k == ord('r'):  # save rectified stereo image pair
            left_file_string = "rect_"+str(self.save_index)+"_l.png"
            right_file_string = "rect_"+str(self.save_index)+"_r.png"
            self.stereo_camera.save_images(
                self.rect_image_left, self.rect_image_right,
                defaultSaveFolder, left_file_string, right_file_string,
                confirm_folder)
            self.save_index += 1
        elif k == ord('p'):  # save 3D data as point cloud
            points_file_string = "points_"+str(self.save_index)+".ply"
            self.save_point_cloud(
                self.disparity, self.rect_image_left,
                defaultSaveFolder, points_file_string,
                confirm_folder)
            self.save_index += 1
        elif k == ord('1'):  # change tp OpenCV BM
            self.change_matcher("BM")
        elif k == ord('2'):  # change to OpenCV SGBM
            self.change_matcher("SGBM")
        if self.show_window:
            window_image_prop = cv2.getWindowProperty(
                self.cv_window_name_Images, cv2.WND_PROP_VISIBLE)
            window_control_prop = cv2.getWindowProperty(
                self.cv_window_name_Images, cv2.WND_PROP_VISIBLE)
            if window_image_prop < 1:
                return self.EXIT_CODE_QUIT
            if window_control_prop < 1:
                return self.EXIT_CODE_QUIT

        if res:
            return self.EXIT_CODE_GRAB_3D_SUCCESS
        else:
            return self.EXIT_CODE_FAILED_TO_GRAB_3D

    def run(self, defaultSaveFolder="", isRectified=False,
            frame_delay=0, confirm_folder=True, colormap=cv2.COLORMAP_JET):
        # connect to stereo camera
        connected = False
        while(not connected):
            connected = self.connect()
            time.sleep(1)
        if self.show_window:
            cv2.namedWindow(self.cv_window_name_Images, cv2.WINDOW_NORMAL)
        while(True):
            exit_code = self.run_frame(
                defaultSaveFolder, isRectified, confirm_folder, colormap)
            if (exit_code == self.EXIT_CODE_QUIT):
                break
            if (exit_code == self.EXIT_CODE_FAILED_TO_GRAB_3D):
                time.sleep(1)
            time.sleep(frame_delay)

        self.stereo_camera.close()
