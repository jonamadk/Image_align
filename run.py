import cv2
import numpy as np


def check_horizontal_and_vertical(image):
    # print("image is ", image)
    input_image = cv2.imread(image)
    cv2.imshow("input image", input_image)
    print(input_image)

    height, width , _ = input_image.shape
    print("height is {} and width is {}".format(height, width))

    if height > width:
        image_orientation = "Potrait"
        return input_image
    
    elif height == width:
        
        image_orientation = "Sqaure"
        return input_image
    
    else:
        image_orientation= "landescape"
        img_rotate_90_clockwise = cv2.rotate(input_image, cv2.ROTATE_90_CLOCKWISE)
        return img_rotate_90_clockwise


def correct_image_alignment():

    image = check_horizontal_and_vertical(r"C:\Users\adkma\Documents\learn_flask\app\static\uploads" )
    # image = check_horizontal_and_vertical()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imshow("is", thresh)
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    print("computed angle" , angle)
    if angle >-45 and angle<1:
        print("choosen 1st")
        angle = angle
    elif angle > 45:
        angle = 90-angle
        print("choosen 2nd")
    else:
        angle = - angle
        print("chossen 3rd")
    print("choosen angle to rotate" , angle)
    (h, w) = image.shape[:2]
    center = (w/2 , h/2 )
    Image_rotation = cv2.getRotationMatrix2D(center, angle, 1.0)

    rotated = cv2.warpAffine(image, Image_rotation, (w, h),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    cv2.imwrite('output.jpg', rotated)
    cv2.imshow("output", rotated)

    cv2.waitKey(0)

correct_image_alignment()