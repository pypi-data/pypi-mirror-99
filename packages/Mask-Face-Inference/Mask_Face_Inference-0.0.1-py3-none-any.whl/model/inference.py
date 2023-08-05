# encoding = utf-8
import torch
import os
import copy
from PIL import Image
import shutil
import numpy as np
import dlib
import cv2
import sys
from config_mask import config
import torchvision.transforms as transforms
from torch.nn.modules.distance import PairwiseDistance
from model.CBAM_Face_attention_Resnet_maskV2 import resnet18_cbam, resnet50_cbam, resnet101_cbam, resnet34_cbam, \
    resnet152_cbam


class FaceRecognitionMaskV2():
    def __init__(self):
        super(FaceRecognitionMaskV2, self).__init__()
        self.pwd = os.path.abspath(__file__ + '../../')
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        pwd = os.path.abspath('../')
        version = 'V2'
        self.mask = False  # 是否给人脸戴口罩
        # img1_path = os.path.join(pwd, 'Layer_show', 'George_W_Bush_0001.jpg')
        # # img1_path = os.path.join(pwd, 'Layer_show', 'Michael_Douglas_0003.jpg')
        # img2_path = os.path.join(pwd, 'Layer_show', 'George_W_Bush_0003.jpg')

        self.model = resnet34_cbam(pretrained=False, showlayer=False, num_classes=128)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_path = os.path.join(pwd, '')
        # x = [int(i.split('_')[4]) for i in os.listdir(model_path) if version in i]
        # x.sort()
        # for i in os.listdir(model_path):
        #     if (len(x) != 0) and ('epoch_' + str(x[-1]) in i) and (version in i):
        #         model_pathi = os.path.join(model_path, i)
        #         break

        model_pathi = os.path.join(model_path, 'model_V2.pt')
        print(model_path)
        if os.path.exists(model_pathi) and (version in model_pathi):
            if torch.cuda.is_available():
                model_state = torch.load(model_pathi)
            else:
                model_state = torch.load(model_pathi, map_location='cpu')
            self.model.load_state_dict(model_state['model_state_dict'])
            start_epoch = model_state['epoch']
            print('loaded %s' % model_pathi)
        else:
            print('不存在预训练模型！')
            sys.exit(0)

        if torch.cuda.is_available():
            self.model.cuda()

        self.model.eval()

        self.test_data_transforms = transforms.Compose([
            transforms.Resize([config['image_size'], config['image_size']]),  # resize
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.5, 0.5, 0.5],
                std=[0.5, 0.5, 0.5]
            )
        ])

        self.isame = 1
        self.threshold = 0.9
        self.detector = dlib.get_frontal_face_detector()
        predicter_path = config['predicter_path']
        self.predictor = dlib.shape_predictor(predicter_path)
        self.img_size = config['image_size']
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        # masked = os.path.join(pwd, 'Layer_show', 'mask')
        # notmasked = os.path.join(pwd, 'Layer_show', 'notmask')
        #
        # delete = input('是否删除文件？ Y or N')
        # if (delete.upper() == 'Y') and (self.mask == True):
        #     os.system('rm -rf %s' % masked)
        #     os.mkdir(masked)
        # elif (delete.upper() == 'Y') and (self.mask == False):
        #     os.system('rm -rf %s' % notmasked)
        #     os.mkdir(notmasked)

    def preprocess(self, image_path, detector, predictor, img_size, cl, mask=True):
        image = dlib.load_rgb_image(image_path)
        face_img, TF = None, 0
        # 人脸对齐、切图
        dets = detector(image, 1)
        if len(dets) == 1:
            faces = dlib.full_object_detections()
            faces.append(predictor(image, dets[0]))
            images = dlib.get_face_chips(image, faces, size=img_size)

            image = np.array(images[0]).astype(np.uint8)
            # face_img = Image.fromarray(image).convert('RGB')  #
            face_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            # 生成人脸mask
            dets = detector(image, 1)
            if len(dets) == 1:
                point68 = predictor(image, dets[0])
                landmarks = list()
                INDEX = [0, 2, 14, 16, 17, 18, 19, 24, 25, 26]
                eyebrow_list = [19, 24]
                eyes_list = [36, 45]
                eyebrow = 0
                eyes = 0

                for eb, ey in zip(eyebrow_list, eyes_list):
                    eyebrow += point68.part(eb).y
                    eyes += point68.part(ey).y
                add_pixel = int(eyes / 2 - eyebrow / 2)

                for idx in INDEX:
                    x = point68.part(idx).x
                    if idx in eyebrow_list:
                        y = (point68.part(idx).y - 2 * add_pixel) if (point68.part(idx).y - 2 * add_pixel) > 0 else 0
                    else:
                        y = point68.part(idx).y
                    landmarks.append((x, y))
                belows = []
                for i in range(2, 15, 1):
                    belows.append([point68.part(i).x, point68.part(i).y])
                belows = np.array(belows)
                colors = [(200, 183, 144), (163, 150, 134), (172, 170, 169), \
                          (167, 168, 166), (173, 171, 170), (161, 161, 160), \
                          (170, 162, 162)]
                # cl = np.random.choice(len(colors), 1)[0]
                # cl = 0
                if mask:
                    cv2.fillConvexPoly(face_img, belows, colors[cl])
                else:
                    pass
        return Image.fromarray(face_img).convert('RGB')

    def ishowm(self, ima, imb):
        imgone = np.asarray(ima)
        imgtwo = np.asarray(imb)
        imgone = cv2.cvtColor(imgone, cv2.COLOR_RGB2BGR)
        imgtwo = cv2.cvtColor(imgtwo, cv2.COLOR_RGB2BGR)
        cv2.putText(imgtwo, 'lay', (1, 25), self.font, 1, [0, 0, 255], 2)
        imgall = np.concatenate([imgone, imgtwo], axis=1)
        if False:
            cv2.namedWindow('images')
            cv2.resizeWindow('images', 600, 600)
            cv2.imshow('images', imgall)
            cv2.waitKey(0)
            cv2.destroyWindow('images')
        return imgall

    def dectect(self, img1_path, img2_path):
        ima = self.preprocess(img1_path, self.detector, self.predictor, self.img_size, 1, self.mask)
        imb = self.preprocess(img2_path, self.detector, self.predictor, self.img_size, 3, self.mask)
        imb_ = copy.deepcopy(imb)
        ima_ = copy.deepcopy(ima)
        ima, imb = self.test_data_transforms(ima), self.test_data_transforms(imb)
        if torch.cuda.is_available():
            data_a = ima.unsqueeze(0).cuda()
            data_b = imb.unsqueeze(0).cuda()
        else:
            data_a, data_b = ima.unsqueeze(0), imb.unsqueeze(0)

        imgall = self.ishowm(ima_, imb_)

        output_a, output_b = self.model(data_a), self.model(data_b)
        output_a = torch.div(output_a, torch.norm(output_a))
        output_b = torch.div(output_b, torch.norm(output_b))
        l2_distance = PairwiseDistance(2)  # .cuda()
        distance = l2_distance.forward(output_a, output_b)
        print('从两张图片提取出来的特征向量的欧氏距离是：%1.3f' % distance)
        # cv2.putText(imgall, 'dis:%1.4f' % distance, (1, 19), self.font, 0.6, [0, 0, 255], 1)
        # imgall = Image.fromarray(imgall).convert('RGB')

        # imgall.save(os.path.join(self.pwd, 'Layer_show', 'notmask', 'dis%1.3f_faceshow_%s.jpg' % (distance, "V2")))
        # path = os.path.join(os.path.join(self.pwd, 'Layer_show'))
        # for i in os.listdir(path):
        #     if os.path.isfile(os.path.join(path, i)) and '000' not in i:
        #         shutil.move(os.path.join(path, i), os.path.join(path, 'notmask', i))

        return distance
