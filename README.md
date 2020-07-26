# Deepfake-Detection
This repository explores DeepFake detection efficacy to optical flow on FaceForensics++ dataset, and compares traditional dense optical flow technique known as Farneback optical flow as well as some of the recent deep learning-based optical flow estimators such as FlowNet, PWC-Net, and SPyNet. Besides, this repository compares the classification performance of pairwise optical flow-based networks to temporal networks employing RNN, LSTM, and Attention networks. The detail comparison is [here](https://github.com/cyshih704/Deepfake-Detection/blob/master/report/Deepfake-Detection.pdf)


## Results
Test accuracy for CNN-based models trained to classify single units of input as “real” or “fake”.
| CNN      | Farneback     | FlowNet2.0 | SPyNet   | PWC-Net  |
| -------- | --------      | --------   | -------- | -------- |
| ResNet18 | 68.90         | 62.26      | 72.79    | 61.21    |
| VGG11    | 72.83         | 63.30      | 70.83    | **62.31**|
| VGG11bn  | **78.87**     | **63.80**  | **77.05**| 62.01    |

Accuracies for models trained to classify sequences of 50 Farneback flow images as “real” or “fake”
| RNN            | Feature Extractor  | Train Acc.| Valid Acc. | Test Acc.    |
| --------       | --------           | --------  | --------   | --------     |
| LSTM           | ResNet18 w/o ft    | 84.65     | 88.57      | 87.50        |
| BiLSTM         | ResNet18 w/o ft    | 81.94     | 88.21      | 87.50        |
| LSTM           | VGG11bn w/o ft     | 96.87     | 97.50      | 95.36        |
| LSTM           | VGG11bn w/ ft      | 93.75     | 95.00      | 96.07        |
| Self-Attention | VGG11bn w/o ft     | 96.53     | 96.79      | **96.43**    |

## Data Preparation
Get the download script [here](https://github.com/ondyari/FaceForensics)
- Download all video with compression rate factor 23
```
python3 download/download-Faceforensics.py ./download -d all -c c23 -t videos
```
The structure of Faceforencsics is as follows


```
├── Faceforensics
    ├── manipulated_sequences
    └── original_sequences
```


## Usage
Set the path in **env.py**
```
DOWNLOAD_DIR: path to Faceforensics/, which contains manipulated_suquences/ and original_sequences/
PREPRO_DIR: empty folder, the folder to save proprocessed data
```

### Data Preprocessing
- Randomly sample 20 pairs of consecutive frames from each video (for CNN models)
- Get first 50 pairs of consecutive frames from each video (for RNN models)
- Crop face region according to the first frame
```
python3 crop_face.py
```

- Save optical flow generated by different methods (Farneback, FlowNet2.0, SPyNet, PWC-Net) on sampled consecutive image as npy file
  - clone [PWC-Net repository](https://github.com/sniklaus/pytorch-pwc) at root directory and download the pretrained model
  - clone [SPyNet repository](https://github.com/sniklaus/pytorch-spynet) at root directory and download the pretrained model
  - clone [FlowNet2.0 repository](https://github.com/NVIDIA/flownet2-pytorch) at root directory and download the pretrained model
```
python3 save_flow.py
```
- Save consecutive flow into a file (used for RNN model)
```
python3 save_seq_flow.py
```

### Train
- Train the CNN model on randomly sampled optical flow in the videos
- Classifier: Vgg11 or Resnet18
- Input: Types of input is necessary to be set in **dataloader/dataloader.py** manually

#### train for CNN model
```
python3 train.py -b <BATCH_SIZE> -e <EPOCH> -m <SAVED_MODEL_NAME> -l <MODEL_PATH> -n <NUM_DATA> -cpu
    -b <BATCH_SIZE>
        batch size used for training and validation
    -e <EPOCH>
        the number of epoch for training and validation
    -m <SAVED_MODEL_NAME>
        the model name (be saved in SAVED_MODEL_PATH)
    -l <MODEL_PATH>
        specified the model path if you want to load previous model
    -n <NUM_DATA>
        the number of data used for training. (set -1 if you want to use all the training data (85898))
    -cpu
        if you want to use CPU to train
```
#### train for RNN model
```
python3 train.py -b <BATCH_SIZE> -e <EPOCH> -m <SAVED_MODEL_NAME> -l <MODEL_PATH> -n <NUM_DATA> -cpu
    -b <BATCH_SIZE>
        batch size used for training and validation
    -e <EPOCH>
        the number of epoch for training and validation
    -m <SAVED_MODEL_NAME>
        the model name (be saved in SAVED_MODEL_PATH)
    -l <MODEL_PATH>
        specified the model path if you want to load previous model
    -n <NUM_DATA>
        the number of data used for training. (set -1 if you want to use all the training data (85898))
    -cpu
        if you want to use CPU to train
    -f
        finetune pretrained CNN model or not
```

### Test
- Evaluate the model on test split of Faceforensics++
#### test for CNN model
```
python3 test.py -l <MODEL_PATH> -cpu
    -l <MODEL_PATH>
        the path of loaded model
    -cpu   
        if you want to use CPU to test
```
#### test for RNN model
```
python3 test_seq.py -l <MODEL_PATH> -cpu
    -l <MODEL_PATH>
        the path of loaded model
    -cpu   
        if you want to use CPU to test
```
