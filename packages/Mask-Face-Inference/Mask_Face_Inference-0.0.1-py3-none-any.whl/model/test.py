import os

from model.inference import FaceRecognitionMaskV2

pwd = os.path.abspath('../')
img1_path = os.path.join(pwd, '../Layer_show', 'Zic_0001.jpg')
# img1_path = os.path.join(pwd, 'Layer_show', 'Michael_Douglas_0003.jpg')
img2_path = os.path.join(pwd, '../Layer_show', 'Zic_0003.jpg')

recognition = FaceRecognitionMaskV2()
if recognition.dectect(img1_path, img2_path) < 0.1:
    print("同一个人")
else:
    print("不是同一个人")
