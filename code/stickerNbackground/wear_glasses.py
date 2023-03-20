import cv2
import numpy as np
from utils import image_resize


# get facial classifiers
face_cascade = cv2.CascadeClassifier('./haar_models/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./haar_models/frontalEyes35x16.xml')


# read images
witch = cv2.imread("../../imgs/hat1.PNG")
witch = cv2.imread("../../imgs/hat2.PNG")
witch = np.array(witch)
# glasses = cv2.imread("../../imgs/glasses1_cap_big.PNG")
glasses = cv2.imread("../../imgs/glasses/glasses2_cap_big.PNG")

# get shape of witch
original_witch_h, original_witch_w, witch_channels = witch.shape


# convert to gray
witch_gray = cv2.cvtColor(witch, cv2.COLOR_BGR2GRAY)
glasses_gray = cv2.cvtColor(glasses, cv2.COLOR_BGR2GRAY)


# create mask and inverse mask of witch
# ret, original_mask = cv2.threshold(witch_gray, 10, 255, cv2.THRESH_BINARY_INV)  # 배경이 png일 때
ret, original_mask = cv2.threshold(witch_gray, 250, 255, cv2.THRESH_BINARY)  # 배경이 흰색일 때?
original_mask_inv = cv2.bitwise_not(original_mask)


# ret2, original_mask2 = cv2.threshold(glasses_gray, 10, 255, cv2.THRESH_BINARY_INV)  # 배경이 png일 때
ret, original_mask2 = cv2.threshold(glasses_gray, 250, 255, cv2.THRESH_BINARY)  # 배경이 흰색일 때?
original_mask_inv2 = cv2.bitwise_not(original_mask2)

# read video
cap = cv2.VideoCapture(0)
ret, img = cap.read()
img_h, img_w = img.shape[:2]

frame = 0
while True:  # continue to run until user breaks loop

    # read each frame of video and convert to gray
    if (frame % 10 == 1):
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # find faces in image using classifier
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # for every face found:
        for (x, y, w, h) in faces:

            # # 얼굴 bbox 그리기
            # img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # # coordinates of face region
            # face_w = w
            # face_h = h
            # face_x1 = x
            # face_x2 = face_x1 + face_w
            # face_y1 = y
            # face_y2 = face_y1 + face_h
            #
            # # witch size in relation to face by scaling
            # witch_width = int(1.5 * face_w)
            # witch_height = int(witch_width * original_witch_h / original_witch_w)
            #
            # # setting location of coordinates of witch
            # # witch_x1 = face_x2 - int(face_w / 2) - int(witch_width / 2)
            # witch_x1 = int((face_x1 + face_x2) / 2 - witch_width / 2)
            # witch_x2 = witch_x1 + witch_width
            # witch_y1 = face_y1 - int(face_h * 0.6)
            # witch_y2 = witch_y1 + witch_height
            #
            # # check to see if out of frame
            # if witch_x1 < 0:
            #     witch_x1 = 0
            # if witch_y1 < 0:
            #     witch_y1 = 0
            # if witch_x2 > img_w:
            #     witch_x2 = img_w
            # if witch_y2 > img_h:
            #     witch_y2 = img_h
            #
            # # Account for any out of frame changes
            # witch_width = witch_x2 - witch_x1
            # witch_height = witch_y2 - witch_y1
            #
            # # resize witch to fit on face
            # witch = cv2.resize(witch, (witch_width, witch_height), interpolation=cv2.INTER_AREA)
            # mask = cv2.resize(original_mask, (witch_width, witch_height), interpolation=cv2.INTER_AREA)
            # mask_inv = cv2.resize(original_mask_inv, (witch_width, witch_height), interpolation=cv2.INTER_AREA)
            #
            # # take ROI for witch from background that is equal to size of witch image
            # roi = img[witch_y1:witch_y2, witch_x1:witch_x2]
            #
            # # original image in background (bg) where witch is not
            # roi_bg = cv2.bitwise_and(roi, roi, mask=mask)
            # roi_fg = cv2.bitwise_and(witch, witch, mask=mask_inv)
            #
            # # 열림 연산(침식->팽창)
            # kernel = np.ones((3, 3), np.uint8)
            # open = cv2.morphologyEx(roi_fg, cv2.MORPH_OPEN, kernel, iterations=4)
            # dst = cv2.add(roi_bg, open)
            #
            # # put back in original image
            # img[witch_y1:witch_y2, witch_x1:witch_x2] = dst


            # 안경 합성
            roi_gray = gray[y:y + h, x:x + h]
            roi_color = img[y:y + h, x:x + h]

            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.5, minNeighbors=5)
            for (ex, ey, ew, eh) in eyes:
                # print("눈 정보: ", ex, ey, ew, eh)
                # cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                eh = int(eh * 0.9)

                roi_eyes = roi_color[ey: ey + eh, ex: ex + ew]
                glasses2 = cv2.resize(glasses, (ew, eh), interpolation=cv2.INTER_AREA)


                mask2 = cv2.resize(original_mask2, (ew, eh), interpolation=cv2.INTER_AREA)  # 배경 영역만 흰색
                mask_inv2 = cv2.resize(original_mask_inv2, (ew, eh), interpolation=cv2.INTER_AREA)  # 모자 영역만 흰색

                # take ROI for witch from background that is equal to size of witch image
                roi_bg2 = cv2.bitwise_and(roi_eyes, roi_eyes, mask=mask2)
                roi_fg2 = cv2.bitwise_and(glasses2, glasses2, mask=mask_inv2)

                # print('roi ', np.shape(roi_eyes))
                # print('roi_bg ', np.shape(roi_bg2))
                # print('mask2', np.shape(mask2))
                # print('roi_fg', np.shape(roi_fg2))
                # print('glasses', np.shape(glasses))
                # print('glasses2', np.shape(glasses2))
                # print('mask_inv2', np.shape(mask_inv2))

                # cv2.imshow('roi', roi_eyes)
                # cv2.imshow('roi_bg', roi_bg2)
                # cv2.imshow('roi_fg', roi_fg2)
                # cv2.imshow('glasses', glasses2)
                # cv2.imshow('mask_inv2', mask_inv2)


                # 열림 연산(침식->팽창)
                kernel = np.ones((3, 3), np.uint8)
                open = cv2.morphologyEx(roi_fg2, cv2.MORPH_OPEN, kernel, iterations=4)
                dst = cv2.add(roi_bg2, open)


                roi_color[ey: ey + eh, ex: ex + ew] = dst

    # display image
    cv2.imshow('img', img)

    frame += 1

    # if user pressed 'q' break
    if cv2.waitKey(1) == ord('q'):  #
        break;

cap.release()  # turn off camera
cv2.destroyAllWindows()  # close all windows