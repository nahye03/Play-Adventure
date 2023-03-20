import fnmatch

import cv2
import natsort
import numpy as np
import os
import mediapipe as mp
from values import *


class user_custom():
  def __init__(self, model_path, img_path, img_shape):
    super().__init__()
    # get facial classifiers
    self.face_cascade = cv2.CascadeClassifier(model_path + '/haarcascade_frontalface_default.xml')
    self.eye_cascade = cv2.CascadeClassifier(model_path + '/frontalEyes35x16.xml')

    # init information
    self.img_w, self.img_h = img_shape
    # print(self.img_w, self.img_h)
    # read images
    self.hats = []
    self.glasses = []
    self.clothes = []
    self.backgrounds=[]

    [self.hats.append('/hats/' + filename) for filename in os.listdir(img_path + '/hats') if
     fnmatch.fnmatch(filename, '*_cap.png')]
    [self.glasses.append('/glasses/' + filename) for filename in os.listdir(img_path + '/glasses') if
     fnmatch.fnmatch(filename, '*_cap.png')]
    [self.clothes.append('/clothes/' + filename) for filename in os.listdir(img_path + '/clothes') if
     fnmatch.fnmatch(filename, '*_cap.png')]
    [self.backgrounds.append(filename) for filename in os.listdir(img_path) if
     fnmatch.fnmatch(filename, 'scene*.png')]

    self.hats=natsort.natsorted(self.hats)
    self.glasses=natsort.natsorted(self.glasses)
    self.clothes=natsort.natsorted(self.clothes)
    self.backgrounds=natsort.natsorted(self.backgrounds)

    self.kernel = np.ones((3, 3), np.uint8)  # 팽창, 침식에 사용할 커널

  def face_detect(self, img, eyes=False):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces)==0:
        if eyes:
            return 0,0,0,0,0
        else:
            return {"face_shape": (0, 0), "face_point1": (0, 0), "face_point2": (0, 0)}

    x, y, w, h = faces[0]
    # 얼굴 ROI 시각화
    # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if eyes:
        return x, y, w, h, gray

    # 얼굴 좌표
    face_w = w
    face_h = h
    face_x1 = x
    face_x2 = face_x1 + face_w
    face_y1 = y
    face_y2 = face_y1 + face_h

    #print("find face :) ",face_w,face_h)
    return {"face_shape": (face_w, face_h), "face_point1": (face_x1, face_y1), "face_point2": (face_x2, face_y2)}

  def wear_hat(self, idx, img):
    origin_img = img.copy()

    face_w, face_h = self.face_detect(origin_img)['face_shape']
    face_x1, face_y1 = self.face_detect(origin_img)['face_point1']
    face_x2, face_y2 = self.face_detect(origin_img)['face_point2']

    if face_w == 0 and face_h == 0:
      #print("Could not find face :(")
      return origin_img

    hat = cv2.imread(img_path + self.hats[idx])
    original_hat_h, original_hat_w, hat_channels = hat.shape
    hat_gray = cv2.cvtColor(hat, cv2.COLOR_BGR2GRAY)

    # mask 생성
    ret, original_hat_mask = cv2.threshold(hat_gray, 250, 255, cv2.THRESH_BINARY)  # 배경이 흰색일 때?
    original_hat_mask_inv = cv2.bitwise_not(original_hat_mask)

    hat_width = int(1.5 * face_w)
    hat_height = int(hat_width * original_hat_h / original_hat_w)

    # 모자 좌표 설정
    hat_x1 = int((face_x1 + face_x2) / 2 - hat_width / 2)
    hat_x2 = hat_x1 + hat_width
    hat_y1 = face_y1 - int(face_h * 0.7)
    hat_y2 = hat_y1 + hat_height

    # img 영역을 벗어났는지 검사
    if hat_x1 < 0:
      hat_x1 = 0
    if hat_y1 < 0:
      hat_y1 = 0
    if hat_x2 > self.img_w:
      hat_x2 = self.img_w
    if hat_y2 > self.img_h:
      hat_y2 = self.img_h

    hat_width = hat_x2 - hat_x1
    hat_height = hat_y2 - hat_y1

    # 얼굴크기에 맞추어 모자사이즈 조정
    hat = cv2.resize(hat, (hat_width, hat_height), interpolation=cv2.INTER_AREA)  # 모자
    mask = cv2.resize(original_hat_mask, (hat_width, hat_height), interpolation=cv2.INTER_AREA)  # 배경 영역만 흰색
    mask_inv = cv2.resize(original_hat_mask_inv, (hat_width, hat_height), interpolation=cv2.INTER_AREA)  # 모자 영역만 흰색

    roi = origin_img[hat_y1:hat_y2, hat_x1:hat_x2]
    roi_bg = cv2.bitwise_and(roi, roi, mask=mask)
    roi_fg = cv2.bitwise_and(hat, hat, mask=mask_inv)

    open = cv2.morphologyEx(roi_fg, cv2.MORPH_OPEN, self.kernel, iterations=4)  # 모자 열림연산으로 불필요요소 제거
    hat_dst = cv2.add(roi_bg, open)

    origin_img[hat_y1:hat_y2, hat_x1:hat_x2] = hat_dst
    return origin_img

  def wear_cloth(self, idx, img):
    origin_img = img.copy()

    face_w, face_h = self.face_detect(origin_img)['face_shape']
    face_x1, face_y1 = self.face_detect(origin_img)['face_point1']
    face_x2, face_y2 = self.face_detect(origin_img)['face_point2']

    if face_w == 0 and face_h == 0:
      return origin_img

    cloth = cv2.imread(img_path + self.clothes[idx])
    original_cloth_h, original_cloth_w, cloth_channels = cloth.shape
    cloth_gray = cv2.cvtColor(cloth, cv2.COLOR_BGR2GRAY)

    # mask 생성
    ret, original_cloth_mask = cv2.threshold(cloth_gray, 250, 255, cv2.THRESH_BINARY)  # 배경이 흰색일 때?
    original_cloth_mask_inv = cv2.bitwise_not(original_cloth_mask)

    cloth_width = int(2.5 * face_w);
    cloth_height = int(cloth_width * original_cloth_h / original_cloth_w)

    # 옷 좌표 설정

    cloth_x1 = int(face_x1 - (cloth_width / 2 - face_w / 2))
    cloth_x2 = cloth_x1 + cloth_width
    cloth_y1 = face_y1 + int(face_h * 1.1)
    cloth_y2 = cloth_y1 + cloth_height

    # img 영역을 벗어났는지 검사
    if cloth_x1 < 0:
      cloth_x1 = 0
    if cloth_y1 < 0:
      cloth_y1 = 0
    if cloth_x2 > self.img_w:
      cloth_x2 = self.img_w
    if cloth_y2 > self.img_h:
      cloth_y2 = self.img_h

    cloth_width = cloth_x2 - cloth_x1
    cloth_height = cloth_y2 - cloth_y1

    # 얼굴크기에 맞추어 모자사이즈 조정
    cloth = cv2.resize(cloth, (cloth_width, cloth_height), interpolation=cv2.INTER_AREA)  # 옷
    mask = cv2.resize(original_cloth_mask, (cloth_width, cloth_height), interpolation=cv2.INTER_AREA)  # 배경 영역만 흰색
    mask_inv = cv2.resize(original_cloth_mask_inv, (cloth_width, cloth_height),
                          interpolation=cv2.INTER_AREA)  # 옷 영역만 흰색

    roi = origin_img[cloth_y1:cloth_y2, cloth_x1:cloth_x2]
    roi_bg = cv2.bitwise_and(roi, roi, mask=mask)
    roi_fg = cv2.bitwise_and(cloth, cloth, mask=mask_inv)

    open = cv2.morphologyEx(roi_fg, cv2.MORPH_OPEN, self.kernel, iterations=4)  # 모자 열림연산으로 불필요요소 제거
    cloth_dst = cv2.add(roi_bg, open)

    # return cloth_x1,cloth_y1,cloth_x2,cloth_y2,cloth_dst
    origin_img[cloth_y1:cloth_y2, cloth_x1:cloth_x2] = cloth_dst
    return origin_img

  def wear_glasses(self, idx, img):
    origin_img = img.copy()

    x, y, w, h, gray = self.face_detect(origin_img, eyes=True)
    if x==0:
        return origin_img
    # 얼굴 검출
    roi_gray = gray[y:y + h, x:x + h]
    roi_color = origin_img[y:y + h, x:x + h]

    # 눈 영역 검출
    eyes = self.eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.5, minNeighbors=5)
    if len(eyes) == 0:
      return origin_img
    ex, ey, ew, eh = eyes[0]

    # 안경 이미지 load , mask 생성
    glasses = cv2.imread(img_path + self.glasses[idx])
    glasses_gray = cv2.cvtColor(glasses, cv2.COLOR_BGR2GRAY)

    ret, original_mask2 = cv2.threshold(glasses_gray, 250, 255, cv2.THRESH_BINARY)  # 배경이 흰색일 때?
    original_mask_inv2 = cv2.bitwise_not(original_mask2)

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
    open = cv2.morphologyEx(roi_fg2, cv2.MORPH_OPEN, self.kernel, iterations=4)
    glasses_dst = cv2.add(roi_bg2, open)

    roi_color[ey: ey + eh, ex: ex + ew] = glasses_dst
    return origin_img

  def backgroud_video(self,idx,origin_img,selfie_segmentation):
    origin_img = cv2.cvtColor(cv2.flip(origin_img, 1), cv2.COLOR_BGR2RGB)

    origin_img.flags.writeable = False
    results = selfie_segmentation.process(origin_img)
    origin_img.flags.writeable = True
    image = cv2.cvtColor(origin_img, cv2.COLOR_RGB2BGR)

    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.5

    bg_image = cv2.imread(img_path+self.backgrounds[idx],cv2.IMREAD_COLOR)
    bg_image= cv2.resize(bg_image, (self.img_w,self.img_h), interpolation = cv2.INTER_CUBIC)
    #bg_image[:] = BG_COLOR
    output_image = np.where(condition, image, bg_image)

    return output_image


# if __name__=='__main__':
#
#     model_path=model_path
#     img_path=img_path
#
#     cap=cv2.VideoCapture(0)
#
#     video_width = int(width / 2)  # 683
#     video_height = height  # 768
#
#     # 클래스 객체 생성
#     u = user_custom(model_path, img_path, (video_width,video_height))
#     # 배경전환을 위한 초기화
#     mp_drawing = mp.solutions.drawing_utils
#     mp_selfie_segmentation = mp.solutions.selfie_segmentation
#
#     hat_on = True
#     glasses_on = True
#     cloth_on = True
#     background_on=True
#     idx = 0
#
#     with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
#       while cap.isOpened():
#           ret, img = cap.read()
#           img = cv2.resize(img, (video_width, video_height), interpolation=cv2.INTER_CUBIC)
#
#           if background_on or hat_on or glasses_on or cloth_on :
#               custom_img=img.copy()
#
#               if background_on:
#                 print('가상 배경 적용@@')
#                 custom_img = u.backgroud_video(idx,custom_img,selfie_segmentation)
#               if hat_on:
#                 #print('모자 착용@@')
#                 custom_img=u.wear_hat(idx,custom_img)
#               elif glasses_on:
#                 #print('안경 착용@@')
#                 custom_img=u.wear_glasses(idx,custom_img)
#               if cloth_on:
#                 #print('옷 착용@@')
#                 custom_img=u.wear_cloth(idx,custom_img)
#
#
#               cv2.imshow('img', custom_img)
#
#           else:
#               cv2.imshow('img',img)
#
#           if cv2.waitKey(5) & 0xFF == 27:
#             break
#       cap.release()  # turn off camera
#       cv2.destroyAllWindows()  # close all windows