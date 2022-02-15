import argparse
import os
import torch
from torch import nn
from torch.autograd import Variable

import Configration
from Encoder.data_loader import load_dataset


class Encoder(nn.Module):
    def __init__(self, dimension):
        size = 2800 if dimension == 2 else 6000
        super(Encoder, self).__init__()
        self.encoder = nn.Sequential(nn.Linear(size, 512), nn.PReLU(), nn.Linear(512, 256), nn.PReLU(),
                                     nn.Linear(256, 128), nn.PReLU(), nn.Linear(128, 28))

    def forward(self, x):
        x = self.encoder(x)
        return x


class Decoder(nn.Module):
    def __init__(self, dimension):
        super(Decoder, self).__init__()
        size = 2800 if dimension == 2 else 6000
        self.decoder = nn.Sequential(nn.Linear(28, 128), nn.PReLU(), nn.Linear(128, 256), nn.PReLU(),
                                     nn.Linear(256, 512), nn.PReLU(), nn.Linear(512, size))

    def forward(self, x):
        x = self.decoder(x)
        return x


mse_loss = nn.MSELoss()
lam = 1e-3


def loss_function(W, x, recons_x, h):
    mse = mse_loss(recons_x, x)
    """
        W is shape of N_hidden x N. So, we do not need to transpose it as opposed to 
        http://wiseodd.github.io/techblog/2016/12/05/contractive-autoencoder/
    """
    dh = h * (1 - h)  # N_batch x N_hidden
    contractive_loss = torch.sum(Variable(W) ** 2, dim=1).sum().mul_(lam)
    return mse + contractive_loss


def main(dataset_path, dimension, progress_bar, encPBar):
    print(dataset_path)
    obs = load_dataset(dataset_path, dimension, encPBar)
    args = Configration.functions.load_train_config()
    print("data load successfully")
    encoder = Encoder(dimension)
    decoder = Decoder(dimension)
    if torch.cuda.is_available():
        encoder.cuda()
        decoder.cuda()

    params = list(encoder.parameters()) + list(decoder.parameters())
    optimizer = torch.optim.Adagrad(params)
    total_loss = []
    for epoch in range(args['num_epochs']):
        print("epoch" + str(epoch))
        avg_loss = 0
        for i in range(0, len(obs), args['batch_size']):
            decoder.zero_grad()
            encoder.zero_grad()
            if i + args['batch_size'] < len(obs):
                inp = obs[i:i + args['batch_size']]
            else:
                inp = obs[i:]
            inp = torch.from_numpy(inp)
            inp = Variable(inp).cuda()
            # ===================forward=====================
            h = encoder(inp)
            output = decoder(h)
            keys = encoder.state_dict().keys()
            W = encoder.state_dict()[
                'encoder.6.weight']  # regularize or contracting last layer of encoder. Print keys to displace the
            # layers name.
            loss = loss_function(W, inp, output, h)
            # print("loss : ",loss.data)
            avg_loss = avg_loss + loss.data
            # ===================backward====================
            loss.backward()
            optimizer.step()
        print("--average loss:")
        print(avg_loss / (len(obs) / args['batch_size']))
        total_loss.append(avg_loss / (len(obs) / args['batch_size']))
        progress_bar.setProperty("value", epoch / 500 * 100)

    avg_loss = 0
    for i in range(len(obs) - 5000, len(obs), args['batch_size']):
        inp = obs[i:i + args['batch_size']]
        inp = torch.from_numpy(inp)
        inp = Variable(inp).cuda()
        # ===================forward=====================
        output = encoder(inp)
        output = decoder(output)
        loss = mse_loss(output, inp)
        avg_loss = avg_loss + loss.data
    # ===================backward====================
    print("--Validation average loss:")
    print(avg_loss / (5000 / args['batch_size']))
    if dimension == 3:
        torch.save(encoder.state_dict(), os.path.join('Models/encoders/3D', 'cae_encoder.pkl'))
        torch.save(decoder.state_dict(), os.path.join('Models/encoders/3D', 'cae_decoder.pkl'))
    else:
        torch.save(encoder.state_dict(), os.path.join('Models/encoders/2D', 'cae_encoder.pkl'))
        torch.save(decoder.state_dict(), os.path.join('Models/encoders/2D', 'cae_decoder.pkl'))

    torch.save(total_loss, 'total_loss.dat')



