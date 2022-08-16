import ProcessingLib
import seaborn
import matplotlib
import Tensorflow as tf
import pandas
import numpy

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.utils.tensorboard import SummaryWriter
#import h5py
from torch.autograd import Variable
import sys, argparse, shutil, pickle, os, copy, math
from collections import OrderedDict
#import ont

dna_default = [[-1, 320, 0, 3, 1, 1, 0], [-1, 320, 1, 3, 3, 1, 1], [-1, 384, 1, 6, 1, 1, 1], [-1, 448, 1, 9, 1, 1, 1], [-1, 512, 1, 12, 1, 1, 1], [-1, 576, 1, 15, 1, 1, 1], [-1, 640, 1, 18, 1, 1, 1], [-1, 704, 1, 21, 1, 1, 1], [-1, 768, 1, 24, 1, 1, 1], [-1, 832, 1, 27, 1, 1, 1], [-1, 896, 1, 30, 1, 1, 1], [-1, 960, 1, 33, 1, 1, 1]]

class Cheeks(nn.module):
    def __init__(self, config=None, arch=None, seqlen=4096, debug=False):
        super().__init__()

        self.seqlen = seqlen
        self.vocab = config.vocab
        self.bn = nn.BatchNorm1d


        # [P, Channels, Separable, kernel_size, stride, sqex, dropout]
        # P = -1 kernel_size//2, 0 none, >0 used as padding
        # Channels
        # seperable = 0 False, 1 True
        # kernel_size
        # stride
        # sqex = 0 False, 1 True
        # dropout = 0 False, 1 True

        if arch is None: arch = dna_default

        #activation = activation_function(config.activation.lower())
        #sqex_activation = activation_function(config.sqex_activation.lower())

        self.convlayers = nn.Sequential()
        in_channels = 1
        convsize = self.seqlen

        for i, layer in enumerate(arch):
            paddingarg = layer[0]
            out_channels = layer[1]
            seperable = layer[2]
            kernel = layer[3]
            stride = layer[4]
            sqex = layer[5]
            dodropout = layer[6]
            expansion = True

            if dodropout:
                dropout = config.dropout
            else:
                dropout = 0
            if sqex:
                squeeze = config.sqex_reduction
            else:
                squeeze = 0

            if paddingarg == -1:
                padding = kernel // 2
            else:
                padding = paddingarg
            if i == 0: expansion = False

            convsize = (convsize + (padding * 2) - (kernel - stride)) // stride
            if debug:
                print("padding:", padding, "seperable:", seperable, "ch", out_channels, "k:", kernel, "s:", stride,
                      "sqex:", sqex, "drop:", dropout, "expansion:", expansion)
                print("convsize:", convsize)
            self.convlayers.add_module("conv" + str(i),
                                       convblock(in_channels, out_channels, kernel, stride=stride, padding=padding,
                                                 seperable=seperable, activation=activation, expansion=expansion,
                                                 dropout=dropout, squeeze=squeeze, sqex_activation=sqex_activation,
                                                 residual=True))
            in_channels = out_channels
            self.final_size = out_channels

        self.final = nn.Linear(self.final_size, len(self.vocab))
        if debug: print("Finished init network")

    def forward(self, x):
        # x = self.embedding(x)
        x = self.convlayers(x)
        x = x.permute(0, 2, 1)
        x = self.final(x)
        x = torch.nn.functional.log_softmax(x, 2)
        return x.permute(1, 0, 2)



