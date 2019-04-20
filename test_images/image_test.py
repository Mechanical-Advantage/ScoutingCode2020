import cv2
import numpy
import math


amodel_points = [
    # Left target
    (-5.938, 2.938, 0.0), # top left
    (-4.063, 2.375, 0.0), # top right
    (-7.375, -2.500, 0.0), # bottom left
    (-5.438, -2.938, 0.0), # bottom right


    # Right target
    (3.938, 2.375, 0.0), # top left
    (5.875, 2.875, 0.0), # top right
    (5.375, -2.938, 0.0), # bottom left
    (7.313, -2.500, 0.0), # bottom right
]


model_points = numpy.array(amodel_points)

aimage_points = [
    (138.000, 121.000),
    (173.000, 129.000),
    (122.000, 210.000),
    (157.000, 216.000),
    (292.000, 125.000),
    (319.000, 115.000),
    (314.000, 200.000),
    (339.000, 190.000),
]
image_points = numpy.array(aimage_points)

#camera_matrix =numpy.array([[329.49123792544623, 0.0, 168.96618562196542],
#                            [0.00, 329.49123792544623, 156.180131529639],
#                            [0.0000, 0.0000, 1.000)]]
camera_matrix = numpy.array([[512.0486676110471, 0.0, 305.52035364138726], [0.0, 515.3532387199512, 262.41020845383434], [0.0, 0.0, 1.0]])
#print(camera_matrix)

dist_coeffs = numpy.array([0.08454318371194253, -0.24818779001569383, 0.002509250787445395, 0.0033838430868377263, 0.12424667264216427])

#print(model_points)
#print(image_points)
image_size = (640,480)
(ret, rvec, tvec) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)
#print(tvec[2])
x = tvec[0][0]
z = tvec[2][0]
# distance in the horizontal plane between camera and target
distance = math.sqrt(x**2 + z**2)
# horizontal angle between camera center line and target
angle1 = math.atan2(x, z)
rot, _ = cv2.Rodrigues(rvec)
rot_inv = rot.transpose()
pzero_world = numpy.matmul(rot_inv, -tvec)
angle2 = math.atan2(pzero_world[0][0], pzero_world[2][0])
#print(pzero_world[0][0], pzero_world[2][0])
print("Distance: ", distance, "Angle1: ", numpy.degrees(angle1), "Angle 2: ", numpy.degrees(angle2),"\r\nX Offset: ", x, "Z Offset: ",z)
