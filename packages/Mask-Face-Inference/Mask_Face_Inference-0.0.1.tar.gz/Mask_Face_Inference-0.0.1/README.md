
sample:
recognition = FaceRecognitionMaskV2()
if recognition.dectect(img1_path, img2_path) < 0.1:
    print("same people")
else:
    print("not same people")