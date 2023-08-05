# 配置文件
config = dict()



# 测试路径（不戴口罩）
# config['train_data_path'] = 'datasets_test/test_train'
# config['train_data_index'] = 'datasets_test/test_train.csv'
# config['train_triplets_path'] = 'datasets/test_train.npy'
# config['LFW_data_path'] = 'datasets_test/lfw_funneled'
# config['LFW_pairs'] = 'datasets_test/LFW_pairs.txt'

config['resume_path'] = 'model_V2.pt'

config['model'] = 34 # 18 34 50 101 152
config['optimizer'] = 'adagrad'      # sgd\adagrad\rmsprop\adam
config['predicter_path'] = 'shape_predictor_68_face_landmarks.dat'

config['Learning_rate'] = 0.00001
config['image_size'] = 256        # inceptionresnetv2————299
config['epochs'] = 50          #验证集的AUC达到最大时就可以停止训练了不要过拟合

config['train_batch_size'] = 32#130
config['test_batch_size'] = 32

config['margin'] = 0.5
config['embedding_dim'] = 128
config['pretrained'] = False
config['save_last_model'] = True
config['num_train_triplets'] = 50000   #git clone代码里面的图片数量少所以三元组数量少，下载全部图片数据以后，需要设置为100000
config['num_workers'] = 0


config['train_data_path'] = '../famous-enterprises/week6/Datasets/vggface2_train_face_mask'
config['mask_data_path'] = '../famous-enterprises/week6/Datasets/vggface2_train_mask_mask'
config['train_data_index'] = '../famous-enterprises/week6/Datasets/vggface2_train_face_mask.csv'
config['train_triplets_path'] = '../famous-enterprises/week6/Datasets/training_triplets_' + str(config['num_train_triplets']) + 'mask.npy'
config['test_pairs_paths'] = '../famous-enterprises/week6/Datasets/test_pairs.npy'
config['LFW_data_path'] = '../famous-enterprises/week6/Datasets/lfw_funneled'
config['LFW_pairs'] = '../famous-enterprises/week6/Datasets/LFW_pairs.txt'
