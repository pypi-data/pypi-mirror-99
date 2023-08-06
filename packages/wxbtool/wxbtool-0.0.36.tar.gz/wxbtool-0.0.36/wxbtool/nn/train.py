# -*- coding: utf-8 -*-

import os
import argparse
import importlib
import logging
import resource

from pathlib import Path

import arrow
import numpy as np
import sys
import torch as th
import torch.nn as nn

from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader

from wxbtool.util.plotter import plot


rlimit = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (2048, rlimit[1]))


parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gpu", type=str, default='0', help="index of gpu")
parser.add_argument("-c", "--n_cpu", type=int, default=64, help="number of cpu threads to use during batch generation")
parser.add_argument("-b", "--batch_size", type=int, default=64, help="size of the batches")
parser.add_argument("-e", "--epoch", type=int, default=0, help="current epoch to start training from")
parser.add_argument("-n", "--n_epochs", type=int, default=200, help="number of epochs of training")
parser.add_argument("-m", "--module", type=str, default='wxbtool.zoo.unet.t850d3', help="module of the metrological model to load")
parser.add_argument("-l", "--load", type=str, default='', help="dump file of the metrological model to load")
parser.add_argument("-k", "--check", type=str, default='', help="checkpoint file to load")
parser.add_argument("-r", "--rate", type=float, default=0.001, help="learning rate")
parser.add_argument("-w", "--weightdecay", type=float, default=0.0, help="weight decay")
parser.add_argument("-d", "--data", type=str, default='', help="url of the dataset server")
opt = parser.parse_args()

os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpu

print('cudnn:', th.backends.cudnn.version())

np.core.arrayprint._line_width = 150
np.set_printoptions(linewidth=np.inf)

early_stopping = 5
best = np.inf
eval_by_epoch = np.inf
count = 0

mdm = None
try:
    mdm = importlib.import_module(opt.module, package=None)
except ImportError as e:
    print('failure when loading model')
    sys.exit(1)

name = mdm.model.name
time_str = arrow.now().format('YYYYMMDD_HHmmss')
model_path = Path(f'./trains/{name}-{time_str}')
model_path.mkdir(exist_ok=True, parents=True)
log_file = model_path / Path('train.log')

logging.basicConfig(level=logging.INFO, filename=log_file, filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info(str(opt))


embbed = False
scheduler = None


def train_model(mdl, lr=0.001, wd=0.0, callback=None):
    global scheduler
    optimizer = th.optim.Adam(mdl.parameters(), lr=lr, weight_decay=wd)
    scheduler = ReduceLROnPlateau(optimizer, 'min')

    try:
        if not embbed and opt.load != '':
            dump = th.load(opt.load, map_location='cpu')
            mdl.load_state_dict(dump)
    except ImportError as e:
        logger.exception(e)
        sys.exit(1)

    if not embbed and th.cuda.is_available():
        mdl = mdl.cuda()

    def train(epoch, mdl):
        global eval_by_epoch
        mdl.train()
        dataloader = DataLoader(mdl.dataset_train, batch_size=opt.batch_size, shuffle=True, num_workers=opt.n_cpu)
        loss_per_epoch = 0.0
        for step, sample in enumerate(dataloader):
            inputs, targets = sample

            inputs = {
                v: th.as_tensor(inputs[v], dtype=th.float32) for v in mdl.setting.vars
            }
            targets = {
                v: th.as_tensor(targets[v], dtype=th.float32) for v in mdl.setting.vars
            }

            if not embbed and th.cuda.is_available():
                inputs = {
                    v: inputs[v].cuda() for v in mdl.setting.vars
                }
                targets = {
                    v: targets[v].cuda() for v in mdl.setting.vars
                }
                mdl.constant = mdl.constant.cuda()
                mdl.weight = mdl.weight.cuda()

            optimizer.zero_grad()
            results = mdl(*[], **inputs)
            loss = mdl.lossfun(inputs, results, targets)
            loss.backward()
            optimizer.step()

            logger.info(f'Epoch: {epoch + 1:03d} | Step: {step + 1:03d} | Loss: {loss.item()}')

            loss_per_epoch += loss.item() * list(results.values())[0].size()[0]

        logger.info(f'Epoch: {epoch + 1:03d} | Train Loss: {loss_per_epoch / mdl.train_size}')

        # evaluation
        loss_eval = evaluate(epoch)
        logger.info(f'Epoch: {epoch + 1:03d} | Eval loss: {loss_eval}')
        scheduler.step(loss_eval)
        eval_by_epoch = loss_eval

        if callback is not None:
            callback(epoch, loss_eval)

        global best, count
        if loss_eval.item() >= best:
            count += 1
        else:
            count = 0
            best = loss_eval

        if count == early_stopping:
            logger.info('early stopping reached, best loss is {:5f}'.format(best))

    def evaluate(epoch):
        mdl.eval()
        dataloader = DataLoader(mdl.dataset_eval, batch_size=opt.batch_size, shuffle=True, num_workers=opt.n_cpu)
        loss_per_epoch = 0.0
        rmse_per_epoch_t = 0.0
        for step, sample in enumerate(dataloader):
            inputs, targets = sample

            inputs = {
                v: th.as_tensor(inputs[v], dtype=th.float32) for v in mdl.setting.vars
            }
            targets = {
                v: th.as_tensor(targets[v], dtype=th.float32) for v in mdl.setting.vars
            }

            if th.cuda.is_available():
                inputs = {
                    v: inputs[v].cuda() for v in mdl.setting.vars
                }
                targets = {
                    v: targets[v].cuda() for v in mdl.setting.vars
                }
                mdl.constant = mdl.constant.cuda()
                mdl.weight = mdl.weight.cuda()

            with th.no_grad():
                results = mdl(*[], **inputs)
                loss = mdl.lossfun(inputs, results, targets)
                logger.info(f'Epoch: {epoch + 1:03d} | Step: {step + 1:03d} | Loss: {loss.item()}')
                loss_per_epoch += loss.item() * list(results.values())[0].size()[0]

                _, tgt = mdl.get_targets(**targets)
                _, rst = mdl.get_results(**results)
                tgt = tgt.detach().cpu().numpy().reshape(-1, 1, 32, 64)
                rst = rst.detach().cpu().numpy().reshape(-1, 1, 32, 64)
                rmse = np.sqrt(np.mean(mdl.weight.cpu().numpy() * (rst - tgt) * (rst - tgt)))
                logger.info(f'Epoch: {epoch + 1:03d} | Step: {step + 1:03d} | Loss: {loss.item()} | Temperature RMSE: {rmse}')
                rmse_per_epoch_t += np.nan_to_num(rmse * list(results.values())[0].size()[0])

        rmse_total = rmse_per_epoch_t / mdl.eval_size
        logger.info(f'Epoch: {epoch + 1:03d} | Eval Loss: {loss_per_epoch / mdl.eval_size}')
        logger.info(f'Epoch: {epoch + 1:03d} | Eval RMSE: {rmse_total}')

        vars_in, _ = mdl.get_inputs(**inputs)
        for bas, var in enumerate(mdl.setting.vars_in):
            for ix in range(mdl.setting.input_span):
                img = vars_in[var][0, ix].detach().cpu().numpy().reshape(32, 64)
                plot(var, open('%s_inp_%d.png' % (var, ix), mode='wb'), img)

        vars_fc, _ = mdl.get_results(**results)
        vars_tg, _ = mdl.get_targets(**targets)
        for bas, var in enumerate(mdl.setting.vars_out):
            fcst = vars_fc[var][0].detach().cpu().numpy().reshape(32, 64)
            tgrt = vars_tg[var][0].detach().cpu().numpy().reshape(32, 64)
            plot(var, open('%s_fcs.png' % var, mode='wb'), fcst)
            plot(var, open('%s_tgt.png' % var, mode='wb'), tgrt)

        th.save(mdl.state_dict(), model_path / f'm_rmse{rmse_total:0.8f}_epoch{epoch + 1:03d}.mdl')
        glb = list(model_path.glob('*.mdl'))
        if len(glb) > 6:
            for p in sorted(glb)[-3:]:
                os.unlink(p)

        th.save({
            'net': mdl.state_dict(),
            'optimizer': optimizer.state_dict(),
        }, model_path / f'z_epoch{epoch + 1:03d}.chk')
        glb = list(model_path.glob('*.chk'))
        if len(glb) > 1:
            os.unlink(sorted(glb)[0])

        return rmse_total

    try:
        for epoch in range(opt.n_epochs):
            train(epoch, mdl)
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    if mdm != None:
        if opt.data != '':
            mdm.model.load_dataset('train', 'client', url=opt.data)
        else:
            mdm.model.load_dataset('train', 'server')

        train_model(mdm.model, lr=opt.rate, wd=opt.weightdecay)

    print('Training Finished!')
