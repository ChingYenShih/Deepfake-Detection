import os
from torch.utils.data import Dataset, DataLoader
import numpy as np
import cv2
import torch
from dataloader.utils import get_image_path
from skimage import io
from PIL import Image as pil_image

#from env import PREPRO_DIR
#PREPRO_DIR = '/home/tmt/ML_data/preproc_frames'

ALL_DATASETS = ['youtube', 'Face2Face']
FAKE_DATASETS = ['Face2Face', 'FaceSwap', 'NeuralTextures', 'Deepfakes']
# split, batch_size, shuffle, num_workers=8

def get_loader(split, batch_size, shuffle, num_data, num_workers=8):
    dataset = DeepfakeDataset(split, 'all', num_data=num_data)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)
    return loader
    
class DeepfakeDataset(Dataset):
    """Deepfake dataset."""

    def __init__(self, split, dataset, num_data):
        np.random.seed(0)

        self.x_path = []
        self.y = []
        #self.transforms = image_transform()
        if dataset == 'all':
            for dataset in ALL_DATASETS:
                img_path = get_image_path(dataset, 'c23', split)
                label = [0]*len(img_path) if dataset != 'youtube' else [1]*len(img_path)

                if num_data != -1:
                    indices = np.random.choice(len(img_path), size=num_data, replace=False)
                    img_path = list(np.array(img_path)[indices])
                    label = list(np.array(label)[indices])

                self.x_path += img_path
                self.y += label
        else:
            self.x_path = get_image_path(dataset, 'c23', split)
            self.y = [0]*len(self.x_path) if dataset != 'youtube' else [1]*len(self.x_path)

            if num_data != -1:
                indices = np.random.choice(self.x_path, size=num_data, replace=False)
                self.x_path = np.array(self.x_path)[indices]
                self.y = np.array(self.y)[indices]

        print('The length of {} dataset: {}'.format(split, len(self.x_path)))


    def __len__(self):
        return len(self.y)

    def __getitem__(self, i):

        first_img = cv2.cvtColor(cv2.imread(os.path.join(self.x_path[i], '1.png')), cv2.COLOR_BGR2RGB)
        second_img = cv2.cvtColor(cv2.imread(os.path.join(self.x_path[i], '2.png')), cv2.COLOR_BGR2RGB)

        first_img = cv2.resize(first_img, (256, 256)).transpose(2, 0, 1) # c, h, w
        second_img = cv2.resize(second_img, (256, 256)).transpose(2, 0, 1) # c, h, w

        label = self.y[i]
        
        return torch.FloatTensor(first_img), torch.FloatTensor(second_img), torch.Tensor([label]).float()

if __name__ == '__main__':
    #a = get_image_path('Face2Face', 'c23', 'val')
    dataset = DeepfakeDataset('train', 'youtube')
    loader = DataLoader(dataset, batch_size=32)
    for img1, img2, label in loader:
        print(img1.size(), img2.size(), label)