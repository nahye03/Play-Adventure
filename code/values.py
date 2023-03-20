width = 1366
height = 768

menu_height = 50

video_height = height - menu_height

font ='맑은 고딕'

img_path = '../imgs/'
video_path = '../videos/'
save_video_path="../my_video/"

page1_image = img_path + 'login_page.png'

page2_video = video_path + '감정.mp4'
page2_image = img_path + "emotion.png"

page3_images=["page3_img1.png","page3_img2.png","page3_img3.png","page3_img4.png","page3_img5.png","page3_img6.png","page3_img7.png"]
page3_video = video_path + '01_김구.mp4'

skip_image = img_path + "skip_button.png"

#페이지6_꾸미기
page6_image = img_path + "makeup_button.png"
page6_image2 = img_path + "makeup_finish_button.png"
clothes_path = ["clothes/cloth1.png",'clothes/cloth2.png','clothes/cloth3.png']
hats_path = ["hats/hat1.png",'hats/hat2.png']
glasses_path = ["glasses/glasses1.png",'glasses/glasses2.png']

page6_video = ['0.꾸미기/꾸미기_01.설명.mp4','0.꾸미기/꾸미기_02.설명.mp4','0.꾸미기/꾸미기_02.대기.mp4','0.꾸미기/꾸미기_03.설명.mp4','0.꾸미기/꾸미기_03.대기.mp4','0.꾸미기/꾸미기_04.설명.mp4','0.꾸미기/꾸미기_05.설명.mp4','0.꾸미기/꾸미기_05.대기.mp4']

# 모자, 안경 합성용 이미지
model_path="stickerNbackground/haar_models"

# 3씬_미션
scene_3_2 = video_path + "3씬/08_미션 1_2 이미지_김구 사진 찍힐 때 영상_순서3.mp4"
scene_sound = video_path + "3씬/08_미션 1_2 이미지_음악_순서2.mp3"
stamp_sound = video_path + "도장 찍는 효과음.mp3"
capture_sound = video_path + '3씬/audio.mp3'

mission_stamp = img_path + "mission_stamp.jpg"
stamp = img_path + "stamp.png"

photo_sound = video_path + "사진 찍는 효과음.mp3"

# 미션 이미지
mission_clock = img_path + "mission_drag.png"
mission_sign = img_path + "mission_sign.png"
mission_speech = img_path + "speech_img.png"
mission_photo = img_path + "mission_photo.png"

camera = img_path + "camera_icon.png"

left_hand = img_path + "left_hand.png"
right_hand = img_path + "right_hand.png"

clock1 = img_path + "clock1.png"
clock2 = img_path + "clock2.png"

clock_backsound = video_path + "6씬/미션3_시계_음악.mp3"

#page 7
scene1_video = ['1씬/01_김구.mp4','1씬/01_대기.mp4','1씬/02_김구.mp4','1씬/02_대기.mp4','1씬/03_김구.mp4','1씬/03_대기.mp4','1씬/04_김구.mp4','1씬/04_화면 블랙아웃.mp4']
scene2_video = ['2씬/05_김구.mp4','2씬/05_대기.mp4','2씬/06_김구.mp4','2씬/06_대기.mp4','2씬/07_김구.mp4','2씬/07_대기.mp4']
scene3_video =['3씬/08_윤봉길 책상 scene.mp4']
scene4_video = ['4씬/09_김구.mp4','4씬/09_대기.mp4','4씬/10_김구.mp4','4씬/10_대기.mp4','4씬/11_김구.mp4','4씬/11_대기.mp4','4씬/11_화면블랙아웃.mp4']
scene5_video = ['5씬/#5_영상.mp4','5씬/배경왼쪽.png']
scene6_video = ['6씬/12_김구.mp4','6씬/12_대기.mp4','6씬/13_김구.mp4','6씬/13_대기.mp4','6씬/14_김구.mp4','6씬/14_대기.mp4','6씬/14_떠남.mp4','6씬/15_김구.mp4','6씬/미션4.mp4']

scene1_text = ['(답답한듯 목소리가 높아진다) 저도 조국 독립을 위해서 아내와 두 아들을 두고 여기 중국, 상해까지 왔습니다!',
               '선생님 (열정적으로 간절히) 앞으로 이봉창의사와 같은 독립운동 계획이 있으면 반드시 반드시! 저에게 맡겨 주십시오',
               '선생님....전 조국을 위해서라면 언제든 희생할 준비가 되어있습니다.',
               '감사합니다.']
scene2_text = ['(누가들을까 목소리를 낮추지만 분노해 있다.)아니 이게 뭡니까 선생님!',
               '일본이 중국과 싸워이겼다는 상해전투소식을 들었습니다. (이를 갈며)왜놈들...의기양양해서는....',
               '(벅차서)할랍니다. 제가 일왕을 처단하겠습니다. 준비만 해주십시요.',
               '좋습니다.']
scene4_text = ['오늘 그 왜놈의 대장도 식장을 설치하는데 왔겠지요. (분노하며)내게 폭탄만 있었다면 당장 해버리는 건데....',
               '(당황하며 부끄럽게)아닙니다. 그놈을 생각하니 불현듯 그런 생각이 나서요. 내일 일에 왜 자신이 없어요. 있습니다.',
               '선생님. 저는 지금 굳건합니다. 그리고...']
scene5_text = ['저는 그 어느 때보다 마음이 고요합니다. 선생님']
scene6_text = ['선생님, 이 시계는 6원을 주고 산 비싼 시계인데, 선생님 시계는 2원짜리니 제 것하고 바꿉시다.',
               '저는 이제 1시간 밖에 살지 못합니다. 제 시계는 앞으로 한 시간 밖에는 쓸 데가 없을 거예요.',
               '선생님 그리고 이거….(돈을 건넨다.)',
               '자동차 값을 하고도 5, 6원이 남아요. 그리고 이거....(편지를 주며)제 아들 둘에게 꼭 좀 부탁드립니다.',
               '(윤봉길은 김구에게 돈과 편지를 쥐어주고 자동차를 타고 떠난다.)']

page7_image = img_path + "next_button.png"
page7_last_video = video_path + "마지막 역사 영상.mp4"

#save_page
yes_button_img = img_path +"yes_button.png"
no_button_img = img_path +"no_button.png"

#page8
page8_image = img_path + "kimgu.png"
page8_play_img = img_path + "play_button.png"
page8_home_img = img_path + "home_button.png"