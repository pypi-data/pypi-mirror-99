import torch
import numpy as np
from torch import nn, optim
from torch.nn.parallel import DistributedDataParallel

from ..utils.progress import Progress



class Module(nn.Module):
    """base module for every model
    """
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        
        # call `__init__` of `nn.Module`
        super(Module, instance).__init__()

        return instance
    
    def __init__(self):
        """define model struct
        """
        pass
    

    def fit(self, loader, epoch = 10, callback = None):
        """train model

        Args:
            loader (DataLoader): loader for training model
            epoch (int): number of epoch for training loop
        """
        optimizer = self.optimizer()

        # init progress bar
        p = Progress(loader)

        for ep in range(epoch):
            p.prefix = f"Epoch:{ep}"

            loss = 0.
            for i, batch in enumerate(p, start = 1):
                # step fit
                l = self.fit_step(batch)
                
                optimizer.zero_grad()
                l.backward()
                optimizer.step()

                loss += (l.item() - loss) / i
                p.suffix = 'loss:{:.4f}'.format(loss)
            
            if callable(callback):
                callback(ep, loss)
    
    def fit_step(self, batch, *args, **kwargs):
        """step for fitting
        Args:
            batch (Any): batch data from dataloader
        
        Returns:
            Tensor: loss of this step
        """
        x, y = batch
        y_hat = self.__call__(x)
        loss = nn.functional.mse_loss(y_hat, y)
        return loss

    def optimizer(self):
        """config optimizer

        Returns:
            Optimizer
        """
        return optim.Adam(self.parameters(), lr = 1e-3)
    
    def save(self, path):
        """save model
        """
        torch.save(self.state_dict(), path)
    
    def load(self, path):
        """load model
        """
        state = torch.load(path)
        self.load_state_dict(state)
    
    def distributed(self, backend = None, **kwargs):
        """get distributed model
        """
        if not torch.distributed.is_initialized():
            if backend is None:
                # choose a backend
                backend = 'nccl' if torch.distributed.is_nccl_available() else 'gloo'

            torch.distributed.init_process_group(backend, **kwargs)
        
        return DistModule(self)
        


class DistModule(DistributedDataParallel):
    """distributed module class
    """
    def fit(self, *args, **kwargs):
        return self.module.fit(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        return self.module.save(*args, **kwargs)
    
    def load(self, *args, **kwargs):
        return self.module.load(*args, **kwargs)
    
    
