import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import torch  # pytorch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler
from torch.autograd import Variable


class MyLSTM(nn.Module):
    def __init__(self, num_classes, input_size, hidden_size, num_layers, seq_length):
        super(MyLSTM, self).__init__()
        self.num_classes = num_classes  # number of classes
        self.num_layers = num_layers  # number of layers
        self.input_size = input_size  # input size
        self.hidden_size = hidden_size  # hidden state
        self.seq_length = seq_length  # sequence length

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                            num_layers=num_layers, batch_first=True)  # lstm
        self.fc_1 = nn.Linear(hidden_size, 128)  # fully connected 1
        self.fc = nn.Linear(128, num_classes)  # fully connected last layer

        self.relu = nn.ReLU()

    def forward(self, x):
        h_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size))  # hidden state
        c_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size))  # internal state
        # Propagate input through LSTM
        output, (hn, cn) = self.lstm(x, (h_0, c_0))  # lstm with input, hidden, and internal state
        hn = hn.view(-1, self.hidden_size)  # reshaping the data for Dense layer next
        out = self.relu(hn)
        out = self.fc_1(out)  # first Dense
        out = self.relu(out)  # relu
        out = self.fc(out)  # Final Output
        return out


class Single_Variable_LSTM:
    def __init__(self, train_y: np.ndarray, prev_days_for_train, device: str = None):
        """
        :param train_y: 仅支持一维数组
        :param prev_days_for_train: 用于前几天的数据预测下一天的数据
        :param device: cpu or cuda
        """
        self.num_epochs = 1000  # 1000 epochs
        self.learning_rate = 0.001  # 0.001 lr

        self.input_size = prev_days_for_train  # number of features
        self.hidden_size = max(1, int(2 * prev_days_for_train))  # number of features in hidden state
        self.num_layers = 1  # number of stacked lstm layers

        self.num_classes = 1  # number of output classes

        # 将值通过MinMaxScaler进行缩放
        self.scaler = MinMaxScaler()
        self.train_y = train_y
        if type(train_y) == pd.DataFrame:
            self.scaler.fit(train_y.values.reshape(-1, 1))
        else:
            self.scaler.fit(train_y.reshape(-1, 1))
        self.train_y = self.transform_data(train_y).astype(np.float32)

        # 将前面的prev_days_for_train天的数据作为输入，并且要记得将self.train_y的数据向后移动prev_days_for_train位
        self.prev_days_for_train = prev_days_for_train
        self.train_x = self.create_dataset(self.train_y, self.prev_days_for_train)
        self.train_y = self.train_y[self.prev_days_for_train:]
        self.init_pred = self.train_y[-self.prev_days_for_train:].copy()

        self.train_x_tensors = Variable(torch.Tensor(self.train_x))
        self.train_x_tensors = torch.reshape(self.train_x_tensors,
                                             (self.train_x_tensors.shape[0], 1, self.train_x_tensors.shape[1]))
        self.train_y_tensors = Variable(torch.Tensor(self.train_y))

        if device is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device

        self.lstm = MyLSTM(self.num_classes, self.input_size, self.hidden_size, self.num_layers,
                           self.train_x_tensors.shape[1])  # our lstm class

        self.criterion = torch.nn.MSELoss()  # mean-squared error for regression
        self.optimizer = torch.optim.Adam(self.lstm.parameters(), lr=self.learning_rate)  # adam optimizer

    def train(self):
        """
        训练模型
        :return: 训练后模型的预测结果
        """
        outputs = None
        for epoch in range(self.num_epochs):
            outputs = self.lstm.forward(self.train_x_tensors)  # forward pass
            self.optimizer.zero_grad()  # caluclate the gradient, manually setting to 0

            # obtain the loss function
            loss = self.criterion(outputs, self.train_y_tensors)

            loss.backward()  # calculates the loss of the loss function

            self.optimizer.step()  # improve from loss, i.e backprop
            if epoch % 100 == 0:
                print("Epoch: %d, loss: %1.5f" % (epoch, loss.item()))
        return self.inv_transform_data(torch.squeeze(outputs, 1).detach().cpu().numpy().reshape(-1, 1))

    def test(self, test_y):
        """
        :param test_y: 一维数组
        :return:
        """
        y = np.concatenate((self.init_pred, self.transform_data(test_y)), axis=0)
        x_test = self.create_dataset(y.copy(), self.prev_days_for_train)  # old transformers

        x_test = Variable(torch.Tensor(x_test))  # converting to Tensors

        # reshaping the dataset
        x_test = torch.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))

        train_predict = self.lstm(x_test)  # forward pass
        train_predict = train_predict.data.numpy()  # numpy conversion
        return self.scaler.inverse_transform(train_predict)

    def predict(self, predict_days, update=False):
        """
        :param predict_days: 预测未来几天的数据
        :param update: 是否要一边预测一边使用预测数据更新模型
        :return:
        """

        def single_predict(X):
            new_x = Variable(torch.Tensor(X))
            new_x_final = torch.reshape(new_x, (new_x.shape[0], 1, new_x.shape[1]))
            return self.lstm(new_x_final)

        def update_model(X, y):
            new_x = Variable(torch.Tensor(X))
            new_y = Variable(torch.Tensor(y))

            new_x_final = torch.reshape(new_x, (new_x.shape[0], 1, new_x.shape[1]))

            for epoch in range(self.num_epochs):
                outputs = self.lstm.forward(new_x_final)

                self.optimizer.zero_grad()
                loss = self.criterion(outputs, new_y)
                loss.backward()
                self.optimizer.step()

        pred = []
        predict_x = torch.from_numpy(self.init_pred.copy().reshape(1, -1))
        # predict_x = torch.unsqueeze(torch.from_numpy(predict_x), 0)
        for _ in range(predict_days):
            predict_y = single_predict(predict_x)
            pred.append(predict_y[0][0].item())
            if update is True:
                update_model(predict_x, predict_y)
            predict_x = torch.cat((predict_x, predict_y), 1)
            predict_x = predict_x[:, 1:]
            if _ % 10 == 0:
                print(f'predict {_} days')
        start_index = self.prev_days_for_train + self.train_x.shape[0]
        return start_index, start_index + predict_days, self.inv_transform_data(np.array(pred).reshape(-1, 1))

    def create_dataset(self, df, train_days):
        result = []
        for i in range(len(df) - train_days):
            result.extend(df[i:i + train_days])
        result = np.array(result, dtype=np.float32)
        result = result.reshape(-1, train_days)
        return result

    def get_train_data(self):
        # print('this.train_y=', self.train_y)
        return self.prev_days_for_train, self.prev_days_for_train + self.train_x.shape[0] - 1, self.inv_transform_data(
            self.train_y)

    def transform_data(self, data):
        if type(data) == pd.DataFrame:
            return self.scaler.transform(data.values.reshape(-1, 1))
        elif type(data) == np.ndarray:
            return self.scaler.transform(data.reshape(-1, 1))
        else:
            raise TypeError("data type must be pd.DataFrame or np.ndarray")

    def inv_transform_data(self, data):
        # print('data=',data)
        return self.scaler.inverse_transform(data)