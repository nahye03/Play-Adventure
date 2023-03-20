import cv2, os
import numpy as np
import fnmatch
from utils import image_resize




# read video
cap = cv2.VideoCapture(0)
ret, img = cap.read()


class user_custom():
    def __init__(self,model_path,img_path):
        super.__init__(self)
        # get facial classifiers

        face_cascade = cv2.CascadeClassifier(model_path+'/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(model_path+'/frontalEyes35x16.xml')

        # read images
        # hat = cv2.imread(img_path+"/hat/hat1_cap.PNG")
        # hat = cv2.imread(img_path+"/hat/hat2_cap.PNG")
        #
        # glasses = cv2.imread(img_path+"/glasses/glasses1_cap_big.PNG")
        # glasses = cv2.imread(img_path+"/glasses/glasses2_cap_big.PNG")
        #
        # # cloth=cv2.imread("../../imgs/cloth/cloth1.PNG")
        # cloth = cv2.imread(img_path+"/cloth/cloth2_cap.png")
        # # cloth=cv2.imread("../../imgs/cloth/cloth3.PNG")
        #
        # # get shape of acc
        # original_hat_h, original_hat_w, hat_channels = hat.shape
        # original_cloth_h, original_cloth_w, cloth_channels = cloth.shape
        #
        # # convert to gray
        # hat_gray = cv2.cvtColor(hat, cv2.COLOR_BGR2GRAY)
        # glasses_gray = cv2.cvtColor(glasses, cv2.COLOR_BGR2GRAY)
        # cloth_gray = cv2.cvtColor(cloth, cv2.COLOR_BGR2GRAY)
        #
        # # 모자 mask, inv_mask 만들기
        # # ret, original_mask = cv2.threshold(hat_gray, 10, 255, cv2.THRESH_BINARY_INV)  # 배경이 png일 때
        # ret, original_hat_mask = cv2.threshold(hat_gray, 250, 255, cv2.THRESH_BINARY)  # 배경이 흰색일 때?
        # original_hat_mask_inv = cv2.bitwise_not(original_hat_mask)
        #
        # # 안경 mask, inv_mask 만들기
        # # ret2, original_mask2 = cv2.threshold(glasses_gray, 10, 255, cv2.THRESH_BINARY_INV)  # 배경이 png일 때
        # ret, original_mask2 = cv2.threshold(glasses_gray, 250, 255, cv2.THRESH_BINARY)  # 배경이 흰색일 때?
        # original_mask_inv2 = cv2.bitwise_not(original_mask2)
        # kernel = np.ones((3, 3), np.uint8)  # 팽창, 침식에 사용할 커널
        #
        # # 옷 mask, inv_mask 만들기
        # ret, original_cloth_mask = cv2.threshold(cloth_gray, 250, 255, cv2.THRESH_BINARY)  # 배경이 흰색일 때?
        # original_cloth_mask_inv = cv2.bitwise_not(original_cloth_mask)
def wear_accs(img, hat=None, glasses=None, cloth=None):
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    if hat is not None:
        # 모자 합성하는 경우
        # print('모자를 착용중입니다.')
        # 얼굴 bbox 그리기

        # coordinates of face region
        face_w = w
        face_h = h
        face_x1 = x
        face_x2 = face_x1 + face_w
        face_y1 = y
        face_y2 = face_y1 + face_h

        # hat size in relation to face by scaling
        hat_width = int(1.5 * face_w)
        hat_height = int(hat_width * original_hat_h / original_hat_w)

        # setting location of coordinates of hat
        # hat_x1 = face_x2 - int(face_w / 2) - int(hat_width / 2)
        hat_x1 = int((face_x1 + face_x2) / 2 - hat_width / 2)
        hat_x2 = hat_x1 + hat_width
        hat_y1 = face_y1 - int(face_h * 0.6)
        hat_y2 = hat_y1 + hat_height

        # check to see if out of frame
        if hat_x1 < 0:
            hat_x1 = 0
        if hat_y1 < 0:
            hat_y1 = 0
        if hat_x2 > img_w:
            hat_x2 = img_w
        if hat_y2 > img_h:
            hat_y2 = img_h

        # Account for any out of frame changes
        hat_width = hat_x2 - hat_x1
        hat_height = hat_y2 - hat_y1

        # resize hat to fit on face
        hat = cv2.resize(hat, (hat_width, hat_height), interpolation=cv2.INTER_AREA)  # 모자
        mask = cv2.resize(original_hat_mask, (hat_width, hat_height), interpolation=cv2.INTER_AREA)  # 배경 영역만 흰색
        mask_inv = cv2.resize(original_hat_mask_inv, (hat_width, hat_height), interpolation=cv2.INTER_AREA)  # 모자 영역만 흰색

        # take ROI for hat from background that is equal to size of hat image
        roi = img[hat_y1:hat_y2, hat_x1:hat_x2]
        roi_bg = cv2.bitwise_and(roi, roi, mask=mask)
        roi_fg = cv2.bitwise_and(hat, hat, mask=mask_inv)

        # 열림 연산(침식->팽창)
        open = cv2.morphologyEx(roi_fg, cv2.MORPH_OPEN, kernel, iterations=4) # 모자 열림연산으로 불필요요소 제거
        hat_dst = cv2.add(roi_bg, open)

        # put back in original image
        img[hat_y1:hat_y2, hat_x1:hat_x2] = hat_dst

    elif glasses is not None:
        # 안경 합성하는 경우
        # print('안경을 착용중입니다.')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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

            # take ROI for hat from background that is equal to size of hat image
            roi_bg2 = cv2.bitwise_and(roi_eyes, roi_eyes, mask=mask2)
            roi_fg2 = cv2.bitwise_and(glasses2, glasses2, mask=mask_inv2)

            # 열림 연산(침식->팽창)
            open = cv2.morphologyEx(roi_fg2, cv2.MORPH_OPEN, kernel, iterations=4)
            dst = cv2.add(roi_bg2, open)

            roi_color[ey: ey + eh, ex: ex + ew] = dst

    elif cloth is not None:
        # 옷 합성하는 경우
        print('옷을 착용중입니다.')

        # 수경 부분 추가
        # 모자 합성하는 경우
        # print('모자를 착용중입니다.')
        # 얼굴 bbox 그리기

        # coordinates of face region
        face_w = w
        face_h = h
        face_x1 = x
        face_x2 = face_x1 + face_w
        face_y1 = y
        face_y2 = face_y1 + face_h

        # hat size in relation to face by scaling
        cloth_width = int(2.5 * face_w);
        cloth_height = int(cloth_width * original_cloth_h / original_cloth_w)

        # setting location of coordinates of hat
        cloth_x1 = int(face_x1- (cloth_width / 2 - face_w / 2 ))
        cloth_x2 = cloth_x1 + cloth_width
        cloth_y1 = face_y1 + int(face_h* 1.1 )
        cloth_y2 = cloth_y1 + cloth_height

        # check to see if out of frame
        if cloth_x1 < 0:
            cloth_x1 = 0
        if cloth_y1 < 0:
            cloth_y1 = 0
        if cloth_x2 > img_w:
            cloth_x2 = img_w
        if cloth_y2 > img_h:
            cloth_y2 = img_h

        # Account for any out of frame changes
        cloth_width = cloth_x2 - cloth_x1
        cloth_height = cloth_y2 - cloth_y1

        # resize hat to fit on face
        cloth = cv2.resize(cloth, (cloth_width, cloth_height), interpolation=cv2.INTER_AREA)  # 옷
        mask = cv2.resize(original_cloth_mask, (cloth_width, cloth_height), interpolation=cv2.INTER_AREA)  # 배경 영역만 흰색
        mask_inv = cv2.resize(original_cloth_mask_inv, (cloth_width, cloth_height), interpolation=cv2.INTER_AREA)  # 옷 영역만 흰색

        # take ROI for hat from background that is equal to size of hat image
        roi = img[cloth_y1:cloth_y2, cloth_x1:cloth_x2]
        roi_bg = cv2.bitwise_and(roi, roi, mask=mask)
        roi_fg = cv2.bitwise_and(cloth, cloth, mask=mask_inv)

        # 열림 연산(침식->팽창)
        open = cv2.morphologyEx(roi_fg, cv2.MORPH_OPEN, kernel, iterations=4)  # 모자 열림연산으로 불필요요소 제거
        cloth_dst = cv2.add(roi_bg, open)

        # put back in original image
        img[cloth_y1:cloth_y2, cloth_x1:cloth_x2] = cloth_dst


    return


# main함수
acc=True
init=0
while True:  # continue to run until user breaks loop

    # read each frame of video and convert to gray
    # if (frame % 10 == 1):
    ret, img = cap.read()

    if acc:
        if init==0:

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # find faces in image using classifier
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # for every face found: 얼굴 여러개 있으면 여러개 detect됨
    for (x, y, w, h) in faces:

        # 모자 합성
        # wear_accs(img, hat=hat)

        # 안경 합성
        #wear_accs(img, hat=None,glasses=glasses)

        #옷 합성
        wear_accs(img, cloth=cloth)

    # display image
    cv2.imshow('img', img)



    # if user pressed 'q' break
    if cv2.waitKey(1) == ord('q'):  #
        break;

cap.release()  # turn off camera
cv2.destroyAllWindows()  # close all windows