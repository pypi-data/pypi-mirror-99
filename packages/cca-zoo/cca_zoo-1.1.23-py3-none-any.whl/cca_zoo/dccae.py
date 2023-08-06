"""
All of my deep architectures have forward methods inherited from pytorch as well as a method:

loss(): which calculates the loss given some inputs and model outputs i.e.

loss(inputs,model(inputs))

This allows me to wrap them all up in the deep wrapper. Obviously this isn't required but it is helpful
for standardising the pipeline for comparison
"""

from typing import Iterable

import torch
from torch import nn
from torch import optim
from torch.nn import functional as F

from cca_zoo.dcca import DCCA_base
from cca_zoo.deep_models import BaseEncoder, Encoder, BaseDecoder, Decoder
from cca_zoo.objectives import CCA


class DCCAE(DCCA_base):

    def __init__(self, latent_dims: int, objective=CCA, encoders: Iterable[BaseEncoder] = (Encoder, Encoder),
                 decoders: Iterable[BaseDecoder] = (Decoder, Decoder), r: float = 1e-3, learning_rate=1e-3, lam=0.5,
                 post_transform=True, schedulers: Iterable = None, optimizers: Iterable = None):
        super().__init__(latent_dims, post_transform=post_transform)
        self.encoders = nn.ModuleList(encoders)
        self.decoders = nn.ModuleList(decoders)
        self.lam = lam
        self.objective = objective(latent_dims, r=r)
        if optimizers is None:
            self.optimizers = [optim.Adam(list(self.encoders.parameters()) + list(self.decoders.parameters()),
                                          lr=learning_rate)]
        else:
            self.optimizers = optimizers
        assert (0 <= self.lam <= 1), "lam between 0 and 1"
        self.schedulers = []
        if schedulers:
            self.schedulers.extend(schedulers)

    def update_weights(self, *args):
        [optimizer.zero_grad() for optimizer in self.optimizers]
        loss = self.loss(*args)
        loss.backward()
        [optimizer.step() for optimizer in self.optimizers]
        return loss

    def forward(self, *args):
        z = self.encode(*args)
        return z

    def encode(self, *args):
        z = []
        for i, encoder in enumerate(self.encoders):
            z.append(encoder(args[i]))
        return tuple(z)

    def decode(self, *args):
        recon = []
        for i, decoder in enumerate(self.decoders):
            recon.append(decoder(args[i]))
        return tuple(recon)

    def loss(self, *args):
        z = self.encode(*args)
        recon = self.decode(*z)
        recon_loss = self.recon_loss(args[:len(recon)], recon)
        return self.lam * recon_loss + self.objective.loss(*z)

    @staticmethod
    def recon_loss(x, recon):
        recons = [F.mse_loss(recon_, x_, reduction='sum') for recon_, x_ in zip(recon, x)]
        return torch.stack(recons).sum(dim=0)
