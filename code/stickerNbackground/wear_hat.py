import cv2
import numpy as np


# get facial classifiers
face_cascade = cv2.CascadeClassifier('./haar_models/haarcascade_frontalface_default.xml')


# read images
witch = cv2.imread('../../imgs/hat/hat1_cap.PNG')  # 모자 이미지가 깔끔하지 않음
# witch = cv2.imread('../../imgs/hat2_cap.PNG')
witch = np.array(witch)

# get shape of witch
original_witch_h, original_witch_w, witch_channels = witch.shape


# convert to gray
witch_gray = cv2.cvtColor(witch, cv2.COLOR_BGR2GRAY)

# create mask and inverse mask of witch
# ret, original_mask = cv2.threshold(witch_gray, 10, 255, cv2.THRESH_BINARY_INV)  # 배경이 png일 때
ret, original_mask = cv2.threshold(witch_gray, 250, 255, cv2.THRESH_BINARY)  # 배경이 흰색일 때
original_mask_inv = cv2.bitwise_not(original_mask)

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

            # coordinates of face region
            face_w = w
            face_h = h
            face_x1 = x
            face_x2 = face_x1 + face_w
            face_y1 = y
            face_y2 = face_y1 + face_h

            # witch size in relation to face by scaling
            witch_width = int(1.5 * face_w)
            witch_height = int(witch_width * original_witch_h / original_witch_w)

            # setting location of coordinates of witch
            # witch_x1 = face_x2 - int(face_w / 2) - int(witch_width / 2)
            witch_x1 = int((face_x1 + face_x2) / 2 - witch_width / 2)
            witch_x2 = witch_x1 + witch_width
            witch_y1 = face_y1 - int(face_h * 0.6)
            witch_y2 = witch_y1 + witch_height

            # check to see if out of frame
            if witch_x1 < 0:
                witch_x1 = 0
            if witch_y1 < 0:
                witch_y1 = 0
            if witch_x2 > img_w:
                witch_x2 = img_w
            if witch_y2 > img_h:
                witch_y2 = img_h

            # Account for any out of frame changes
            witch_width = witch_x2 - witch_x1
            witch_height = witch_y2 - witch_y1

            # resize witch to fit on face
            witch = cv2.resize(witch, (witch_width, witch_height), interpolation=cv2.INTER_AREA)  # 모자
            mask = cv2.resize(original_mask, (witch_width, witch_height), interpolation=cv2.INTER_AREA)  # 배경 영역만 흰색
            mask_inv = cv2.resize(original_mask_inv, (witch_width, witch_height), interpolation=cv2.INTER_AREA)  # 모자 영역만 흰색
            # cv2.imshow('witch', witch)
            # cv2.imshow('mask', mask)
            # cv2.imshow('mask_inv', mask_inv)

            # take ROI for witch from background that is equal to size of witch image
            roi = img[witch_y1:witch_y2, witch_x1:witch_x2]
            roi_bg = cv2.bitwise_and(roi, roi, mask=mask)
            roi_fg = cv2.bitwise_and(witch, witch, mask=mask_inv)

            # print('roi ', np.shape(roi))
            # print('roi_bg ', np.shape(roi_bg))

            # print('witch', np.shape(witch))
            # print('mask_inv', np.shape(mask_inv))
            # print('roi_fg', np.shape(roi_fg))
            # cv2.imshow('roi', roi)
            # cv2.imshow('roi_bg', roi_bg)
            # cv2.imshow('roi_fg', roi_fg)

            # 열림 연산(침식->팽창)
            kernel = np.ones((3, 3), np.uint8)
            open = cv2.morphologyEx(roi_fg, cv2.MORPH_OPEN, kernel, iterations=4)
            dst = cv2.add(roi_bg, open)

            # put back in original image
            img[witch_y1:witch_y2, witch_x1:witch_x2] = dst

            break
    # display image
    cv2.imshow('img', img)

    frame += 1

    # if user pressed 'q' break
    if cv2.waitKey(1) == ord('q'):  #
        break;

cap.release()  # turn off camera
cv2.destroyAllWindows()  # close all windows