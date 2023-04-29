import torch
import torchaudio
import librosa
import torch.nn as nn
import numpy as np


class SpeechRecognitionModel(nn.Module):
    def __init__(self, num_classes):
        super(SpeechRecognitionModel, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=(3,3), stride=(1,1), padding=(1,1)),
            nn.BatchNorm2d(32),
            nn.GELU(),
            nn.MaxPool2d(kernel_size=(2,2), stride=(2,2)),
            nn.Conv2d(32, 32, kernel_size=(3,3), stride=(1,1), padding=(1,1)),
            nn.BatchNorm2d(32),
            nn.GELU(),
            nn.Conv2d(32, 32, kernel_size=(3,3), stride=(1,1), padding=(1,1)),
            nn.BatchNorm2d(32),
            nn.GELU(),
            nn.MaxPool2d(kernel_size=(2,2), stride=(2,2)),
        )
        
        self.rnn_1 = nn.LSTM(input_size=1024, 
                    hidden_size=128, 
                    num_layers=1, 
                    batch_first=True, 
                    bidirectional=True)
        
        self.dropout = nn.Dropout(0.3)
        
        self.rnn_2 = nn.GRU(input_size=256, 
                    hidden_size=256, 
                    num_layers=1, 
                    batch_first=True, 
                    bidirectional=True)
        
        self.fc = nn.Sequential(
            nn.Linear(512, num_classes),
        )
        self.softmax = nn.LogSoftmax(dim=2)

    def forward(self, x):
        x = self.conv(x)
        x = x.permute(0, 3, 1, 2)
        x = x.view(x.size(0), x.size(1), -1)
        x, _ = self.rnn_1(x)
        x = self.dropout(x)
        x, _ = self.rnn_2(x)
        x = self.dropout(x)
        x = self.fc(x)
        x = self.softmax(x)
        return x


class ModelInit:
    def __init__(self, path='model.pth', device_type='cpu'):
        if device_type == 'cuda':
            use_cuda = torch.cuda.is_available()
            if use_cuda:
                print('using cuda')
                self.device = torch.device("cuda")
            else:
                print('Невозможно использовать GPU, выбран CPU')
                self.device = torch.device("cpu")
        else:
            self.device = torch.device("cpu")
            print('Использовано CPU')
            
        self.model = SpeechRecognitionModel(35)
        self.model.load_state_dict(torch.load(path))
        self.model.to(self.device)
        self.model.eval()
        self.audio_transforms = torchaudio.transforms.MelSpectrogram()
        
        self.char_map = {"а": 0, "б": 1, "в": 2, "г": 3, "д": 4, "е": 5, "ё": 6, "ж": 7, "з": 8, "и": 9, "й": 10,
                  "к": 11, "л": 12, "м": 13, "н": 14, "о": 15, "п": 16, "р": 17, "с": 18, "т": 19, "у": 20,
                  "ф": 21, "ч": 22, "ц": 23, "ш": 24, "щ": 25, "ъ": 26, "ы": 27, "ь": 28, "э": 29, "ю": 30,
                  "я": 31, "х": 32, " ": 33}
        
        self.index_map = {}
        for key, value in self.char_map.items():
            self.index_map[value] = key
        print("Инициализация завершена")

    def int_to_text(self, labels):
        string = []
        for i in labels:
            string.append(self.index_map[i])
        return ''.join(string)
        
    def predict(self, audio_path):
        audio = librosa.load(audio_path, sr=16000)[0]
        audio = audio[np.newaxis, :]
        audio = torch.Tensor(audio)
        audio = self.audio_transforms(audio).squeeze(0)
        spectrogram_tensor = audio.unsqueeze(0).unsqueeze(0)
        spectrogram_tensor.to(self.device)
        
        with torch.no_grad():
            output = self.model(spectrogram_tensor)
            arg_maxes = torch.argmax(output, dim=2)
            decodes = []
            for i, args in enumerate(arg_maxes):
                decode = []
                for j, index in enumerate(args):
                    if index != 34:
                        if True and j != 0 and index == args[j -1]:
                            continue
                        decode.append(index.item())
                decodes.append(self.int_to_text(decode))
                
        return decodes[0]
        