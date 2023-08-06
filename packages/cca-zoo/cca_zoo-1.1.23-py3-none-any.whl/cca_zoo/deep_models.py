from abc import abstractmethod
from math import sqrt
from typing import Iterable, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

'''
I've included some standard models for the DCCA encoders and DCCAE decoders. 
We have a FCN, CNN and GNN which we can compare.
Particular thanks for the basic structure to:
https://github.com/Michaelvll/DeepCCA/blob/master/DeepCCAModels.py
'''


class BaseEncoder(nn.Module):
    @abstractmethod
    def __init__(self, latent_dims: int, variational: bool = False):
        super(BaseEncoder, self).__init__()
        self.variational = variational
        self.latent_dims = latent_dims

    @abstractmethod
    def forward(self, x):
        pass


class BaseDecoder(nn.Module):
    @abstractmethod
    def __init__(self, latent_dims: int):
        super(BaseDecoder, self).__init__()
        self.latent_dims = latent_dims

    @abstractmethod
    def forward(self, x):
        pass


class Encoder(BaseEncoder):
    def __init__(self, latent_dims: int, variational: bool = False, feature_size: int = 784,
                 layer_sizes: Iterable = None):
        super(Encoder, self).__init__(latent_dims, variational=variational)
        if layer_sizes is None:
            layer_sizes = [128]
        layers = []

        # first layer
        layers.append(nn.Sequential(
            nn.Linear(feature_size, layer_sizes[0]),
            nn.ReLU()
        ))

        # other layers
        for l_id in range(len(layer_sizes) - 1):
            layers.append(nn.Sequential(
                nn.Linear(layer_sizes[l_id], layer_sizes[l_id + 1]),
                nn.ReLU()
            ))
        self.layers = nn.Sequential(*layers)

        if self.variational:
            self.fc_mu = nn.Linear(layer_sizes[-1], latent_dims)
            self.fc_var = nn.Linear(layer_sizes[-1], latent_dims)
        else:
            self.fc = nn.Linear(layer_sizes[-1], latent_dims)

    def forward(self, x):
        x = self.layers(x)
        if self.variational:
            mu = self.fc_mu(x)
            logvar = self.fc_var(x)
            return mu, logvar
        else:
            x = self.fc(x)
            return x


class Decoder(BaseDecoder):
    def __init__(self, latent_dims: int, feature_size: int = 784, layer_sizes: list = None, norm_output: bool = False):
        super(Decoder, self).__init__(latent_dims)
        if layer_sizes is None:
            layer_sizes = [128]
        layers = []

        layers.append(nn.Sequential(
            nn.Linear(latent_dims, layer_sizes[0]),
            nn.Sigmoid()
        ))

        for l_id in range(len(layer_sizes)):
            if l_id == len(layer_sizes) - 1:
                if norm_output:
                    layers.append(nn.Sequential(
                        nn.Linear(layer_sizes[l_id], feature_size),
                        nn.Sigmoid()
                    ))
                else:
                    layers.append(nn.Sequential(
                        nn.Linear(layer_sizes[l_id], feature_size),
                    ))
            else:
                layers.append(nn.Sequential(
                    nn.Linear(layer_sizes[l_id], layer_sizes[l_id + 1]),
                    nn.ReLU()
                ))
        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        x = self.layers(x)
        return x


class CNNEncoder(BaseEncoder):
    def __init__(self, latent_dims: int, variational: bool = False, feature_size: Iterable = (28, 28),
                 channels: list = None, kernel_sizes: list = None,
                 stride: list = None,
                 padding: list = None):
        super(CNNEncoder, self).__init__(latent_dims, variational=variational)
        if channels is None:
            channels = [1, 1]
        if kernel_sizes is None:
            kernel_sizes = [5] * (len(channels))
        if stride is None:
            stride = [1] * (len(channels))
        if padding is None:
            padding = [2] * (len(channels))
        # assume square input
        conv_layers = []
        current_size = feature_size[0]
        current_channels = 1
        for l_id in range(len(channels) - 1):
            conv_layers.append(nn.Sequential(  # input shape (1, current_size, current_size)
                nn.Conv2d(
                    in_channels=current_channels,  # input height
                    out_channels=channels[l_id],  # n_filters
                    kernel_size=kernel_sizes[l_id],  # filter size
                    stride=stride[l_id],  # filter movement/step
                    padding=padding[l_id],
                    # if want same width and length of this image after Conv2d, padding=(kernel_size-1)/2 if
                    # stride=1
                ),  # output shape (out_channels, current_size, current_size)
                nn.ReLU(),  # activation
            ))
            current_size = current_size
            current_channels = channels[l_id]

        if self.variational:
            self.fc_mu = nn.Sequential(
                nn.Linear(int(current_size * current_size * current_channels), latent_dims),
            )
            self.fc_var = nn.Sequential(
                nn.Linear(int(current_size * current_size * current_channels), latent_dims),
            )
        else:
            self.fc = nn.Sequential(
                nn.Linear(int(current_size * current_size * current_channels), latent_dims),
            )
        self.conv_layers = nn.Sequential(*conv_layers)

    def forward(self, x):
        x = self.conv_layers(x)
        x = x.reshape((x.shape[0], -1))
        if self.variational:
            mu = self.fc_mu(x)
            logvar = self.fc_var(x)
            return mu, logvar
        else:
            x = self.fc(x)
            return x


class CNNDecoder(BaseDecoder):
    def __init__(self, latent_dims: int, feature_size: Iterable = (28, 28), channels: list = None, kernel_sizes=None,
                 strides=None,
                 paddings=None, norm_output: bool = False):
        super(CNNDecoder, self).__init__(latent_dims)
        if channels is None:
            channels = [1, 1]
        if kernel_sizes is None:
            kernel_sizes = [5] * len(channels)
        if strides is None:
            strides = [1] * len(channels)
        if paddings is None:
            paddings = [2] * len(channels)

        if norm_output:
            activation = nn.Sigmoid()
        else:
            activation = nn.ReLU()

        conv_layers = []
        current_channels = 1
        current_size = feature_size[0]
        # Loop backward through decoding layers in order to work out the dimensions at each layer - in particular the first
        # linear layer needs to know B*current_size*current_size*channels
        for l_id, (channel, kernel, stride, padding) in reversed(
                list(enumerate(zip(channels, kernel_sizes, strides, paddings)))):
            conv_layers.append(nn.Sequential(
                nn.ConvTranspose2d(
                    in_channels=channel,  # input height
                    out_channels=current_channels,
                    kernel_size=kernel_sizes[l_id],
                    stride=strides[l_id],  # filter movement/step
                    padding=paddings[l_id],
                    # if want same width and length of this image after Conv2d, padding=(kernel_size-1)/2 if
                    # stride=1
                ),
                activation,
            ))
            current_size = current_size
            current_channels = channel

        # reverse layers as constructed in reverse
        self.conv_layers = nn.Sequential(*conv_layers[::-1])
        self.fc_layer = nn.Sequential(
            nn.Linear(latent_dims, int(current_size * current_size * current_channels)),
        )

    def forward(self, x):
        x = self.fc_layer(x)
        x = x.reshape((x.shape[0], self.conv_layers[0][0].in_channels, -1))
        x = x.reshape(
            (x.shape[0], self.conv_layers[0][0].in_channels, int(sqrt(x.shape[-1])), int(sqrt(x.shape[-1]))))
        x = self.conv_layers(x)
        return x


# https://github.com/nicofarr/brainnetcnnVis_pytorch/blob/master/BrainNetCnnGoldMSI.py
class E2EBlock(nn.Module):
    def __init__(self, in_planes, planes, size, bias=False):
        super(E2EBlock, self).__init__()
        self.d = size
        self.cnn1 = torch.nn.Conv2d(in_planes, planes, (1, self.d), bias=bias)
        self.cnn2 = torch.nn.Conv2d(in_planes, planes, (self.d, 1), bias=bias)

    def forward(self, x):
        a = self.cnn1(x)
        b = self.cnn2(x)
        return torch.cat([a] * self.d, 3) + torch.cat([b] * self.d, 2)


class E2EBlockReverse(nn.Module):
    def __init__(self, in_planes, planes, size, bias=False):
        super(E2EBlockReverse, self).__init__()

        self.d = size
        self.cnn1 = torch.nn.ConvTranspose2d(in_planes, planes, (1, self.d), bias=bias)
        self.cnn2 = torch.nn.ConvTranspose2d(in_planes, planes, (self.d, 1), bias=bias)

    def forward(self, x):
        a = self.cnn1(x)
        b = self.cnn2(x)
        return torch.cat([a] * self.d, 3) + torch.cat([b] * self.d, 2)


# BrainNetCNN Network for fitting Gold-MSI on LSD dataset
class BrainNetEncoder(BaseEncoder):
    def __init__(self, latent_dims: int, variational: bool = False, feature_size: Tuple[int] = (200, 200)):
        super(BrainNetEncoder, self).__init__(latent_dims, variational=variational)
        assert (feature_size[0] == feature_size[1])
        self.d = feature_size[0]
        self.e2econv1 = E2EBlock(1, 32, self.d, bias=True)
        self.e2econv2 = E2EBlock(32, 64, self.d, bias=True)
        self.E2N = torch.nn.Conv2d(64, 1, (1, self.d))
        self.N2G = torch.nn.Conv2d(1, 256, (self.d, 1))
        self.dense1 = torch.nn.Linear(256, 128)
        self.dense2 = torch.nn.Linear(128, 30)
        self.dense3 = torch.nn.Linear(30, latent_dims)

    def forward(self, x):
        out = F.leaky_relu(self.e2econv1(x), negative_slope=0.33)  # B,32,200,200
        out = F.leaky_relu(self.e2econv2(out), negative_slope=0.33)  # B,64,200,200
        out = F.leaky_relu(self.E2N(out), negative_slope=0.33)  # B,1,200,1
        out = F.dropout(F.leaky_relu(self.N2G(out), negative_slope=0.33), p=0.5)  # B,256,1,1
        out = out.view(out.shape[0], -1)  # B,256
        out = F.dropout(F.leaky_relu(self.dense1(out), negative_slope=0.33), p=0.5)
        out = F.dropout(F.leaky_relu(self.dense2(out), negative_slope=0.33), p=0.5)
        out = F.leaky_relu(self.dense3(out), negative_slope=0.33)
        return out


class BrainNetDecoder(BaseDecoder):
    def __init__(self, latent_dims: int, feature_size: Tuple[int] = (200, 200)):
        super(BrainNetDecoder, self).__init__(latent_dims)
        assert (feature_size[0] == feature_size[1])
        self.d = feature_size[0]
        self.e2econv1 = E2EBlock(32, 1, self.d, bias=True)
        self.e2econv2 = E2EBlock(64, 32, self.d, bias=True)
        self.E2N = torch.nn.ConvTranspose2d(1, 64, (1, self.d))
        self.N2G = torch.nn.ConvTranspose2d(256, 1, (self.d, 1))
        self.dense1 = torch.nn.Linear(128, 256)
        self.dense2 = torch.nn.Linear(30, 128)
        self.dense3 = torch.nn.Linear(latent_dims, 30)

    def forward(self, x):
        out = F.dropout(F.leaky_relu(self.dense3(x), negative_slope=0.33), p=0.5)
        out = F.dropout(F.leaky_relu(self.dense2(out), negative_slope=0.33), p=0.5)
        out = F.leaky_relu(self.dense1(out), negative_slope=0.33)
        out = out.view(out.size(0), out.size(1), 1, 1)
        out = F.dropout(F.leaky_relu(self.N2G(out), negative_slope=0.33), p=0.5)
        out = F.leaky_relu(self.E2N(out), negative_slope=0.33)
        out = F.leaky_relu(self.e2econv2(out), negative_slope=0.33)
        out = F.leaky_relu(self.e2econv1(out), negative_slope=0.33)
        return out


class LinearEncoder(BaseEncoder):
    def __init__(self, input_size: int, output_size: int, variational: bool = False):
        super(LinearEncoder, self).__init__(input_size, output_size, variational=variational)
        self.linear = nn.Linear(output_size, input_size)

    def forward(self, x):
        out = self.linear(x)
        return out


class LinearDecoder(BaseDecoder):
    def __init__(self, input_size: int, output_size: int):
        super(LinearDecoder, self).__init__(input_size, output_size)
        self.linear = nn.Linear(output_size, input_size)

    def forward(self, x):
        out = self.linear(x)
        return out
