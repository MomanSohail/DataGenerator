import torch
import torch.nn as nn
import os

import Configration.functions
from Train.data_loader import load_dataset
from Train.model import MLP
from torch.autograd import Variable


def to_var(x, volatile=False):
    if torch.cuda.is_available():
        x = x.cuda()
    return Variable(x, volatile=volatile)


def get_input(i, data, targets, bs):
    if i + bs < len(data):
        bi = data[i:i + bs]
        bt = targets[i:i + bs]
    else:
        bi = data[i:]
        bt = targets[i:]

    return torch.from_numpy(bi), torch.from_numpy(bt)


def main(dataset_path, dimension, progress_bar, TDP):

    # Build data loader
    dataset, targets = load_dataset(dataset_path, dimension, TDP)
    args = Configration.functions.load_train_config()
    # Build the Models
    mlp = MLP(28+dimension*2, dimension)

    if torch.cuda.is_available():
        mlp.cuda()

    # Loss and Optimizer
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adagrad(mlp.parameters())

    # Train the Models
    total_loss = []
    sm = 100  # start saving Models after 100 epochs
    for epoch in range(args['num_epochs']):
        print("epoch" + str(epoch))
        avg_loss = 0
        for i in range(0, len(dataset), args['batch_size']):
            # Forward, Backward and Optimize
            mlp.zero_grad()
            bi, bt = get_input(i, dataset, targets, args['batch_size'])
            bi = to_var(bi)
            bt = to_var(bt)
            bo = mlp(bi)
            loss = criterion(bo, bt)
            avg_loss = avg_loss + loss.data
            loss.backward()
            optimizer.step()
        print("--average loss:")
        print(avg_loss / (len(dataset) / args['batch_size']))
        total_loss.append(avg_loss / (len(dataset) / args['batch_size']))
        # Save the Models
        if epoch == sm:
            model_path = 'mlp_100_4000_PReLU_ae_dd' + str(sm) + '.pkl'
            torch.save(mlp.state_dict(), os.path.join(args['model_path'], model_path))
            sm = sm + 50  # save model after every 50 epochs from 100 epoch ownwards
            progress_bar.setProperty("value", epoch / 500 * 100)
    torch.save(total_loss, 'total_loss.dat')
    model_path = 'mlp_100_4000_PReLU_ae_dd_final.pkl'
    torch.save(mlp.state_dict(), os.path.join(args['model_path'], model_path))

