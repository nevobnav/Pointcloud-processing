from laspy.file import File
import numpy as np
import pclpy
from pclpy import pcl
#import pclpy.pcl_visualization

f = File( r"C:\Users\laptop\Google Drive\Google Drive\Shared folder Tasos-VanBoven\Sample_data\Broccoli\35m\Rijweg_stalling1-8-5.las", mode='r')
#f = pclpy.read(r"C:\Users\laptop\Google Drive\Google Drive\Shared folder Tasos-VanBoven\Sample_data\Broccoli\35m\Rijweg_stalling1-8-5.las", "PointXYZRGBA")


# check las file version
# RGB contains
if f._header.data_format_id in (2, 3, 5):
    red = (f.red)
    green = (f.green)
    blue = (f.blue)
    # 16bit to convert 8bit data(data Storage First 8 bits case)
    red = np.right_shift(red, 8).astype(np.uint8)
    green = np.right_shift(green, 8).astype(np.uint8)
    blue = np.right_shift(blue, 8).astype(np.uint8)
    # (data Storage After 8 bits case)
    # red = red.astype(np.uint8)
    # green = green.astype(np.uint8)
    # blue = blue.astype(np.uint8)
    red = red.astype(np.uint32)
    green = green.astype(np.uint32)
    blue = blue.astype(np.uint32)
    rgb = np.left_shift(red, 16) + np.left_shift(green, 8) + np.left_shift(blue, 0)
    ptcloud = np.vstack((f.x, f.y, f.z, rgb)).transpose()
    
    cloud = pcl.search.KdTree.PointXYZRGBA()
    
    #########################################cloud = pcl.PointCloud_PointXYZRGBA()
    # set raw points
    # cloud.from_array(np.array(ptcloud, dtype=np.float32))
    # set point centered
    mean_param = np.concatenate([np.mean(ptcloud, 0)[0:3], np.zeros(1)])
    ptcloud_centred = ptcloud - mean_param
    # print(ptcloud_centred)
    cloud.from_array(np.array(ptcloud_centred, dtype=np.float32))
    
    cloud.np(ptcloud_centred, dtype=np.float32)


    ## Visualization
    visual = pcl.pcl_visualization.CloudViewing()
    visual.ShowColorACloud(cloud, b'cloud')

    v = True
    while v:
        v=not(visual.WasStopped())
#a=pclpy.Viewer(ptcloud)
