import logging
import math
import os

# import matplotlib
# import matplotlib.pyplot as plt
import numpy as np
import torch



def mmd2(x1, y1, x2, y2, ratio1, ratio2, beta = 1.0):
    """
    maximum mean discrepancy (MMD) based on Gaussian kernel
    function for keras models (pytorch backend)
    
    - Gretton, Arthur, et al. "A kernel method for the two-sample-problem."
    Advances in neural information processing systems. 2007.

    - code adapted from https://github.com/wzell/mann/blob/master/models/maximum_mean_discrepancy.py#L23-L39
    """
    # ratio11 = torch.outer(ratio1, ratio1)
    ratio12 = torch.outer(ratio1, ratio2)
    ratio21 = torch.outer(ratio2, ratio1)

    x1x1 = gaussian_kernel(x1, x2, beta)
    x1x2 = gaussian_kernel(x1, y2, beta)
    x2x1 = gaussian_kernel(x2, y1, beta)
    x2x2 = gaussian_kernel(y1, y2, beta)

    diff = x1x1 * ratio12 -  x1x2 * ratio12 - x2x1 * ratio21 + x2x2 * ratio12  
    diff = diff.mean()
    return diff


def mmd(x1, x2, ratio, beta = 1.0):
    """
    maximum mean discrepancy (MMD) based on Gaussian kernel
    function for keras models (pytorch backend)
    
    - Gretton, Arthur, et al. "A kernel method for the two-sample-problem."
    Advances in neural information processing systems. 2007.

    - code adapted from https://github.com/wzell/mann/blob/master/models/maximum_mean_discrepancy.py#L23-L39
    """
    ratio_outer = torch.outer(ratio, ratio)
    x1x1 = gaussian_kernel(x1, x1, beta)
    x1x2 = gaussian_kernel(x1, x2, beta)
    x2x2 = gaussian_kernel(x2, x2, beta)
    # diff = x1x1.mean() - 2 * x1x2.mean() + x2x2.mean()
    diff = x1x1 - 2 * x1x2 + x2x2 
    diff = diff * ratio_outer
    diff = diff.mean()
    return diff

# maybe merged into the same mmd 
def mmd_r2(x1, x2, ratio1, ratio2, beta = 1.0):
    """
    maximum mean discrepancy (MMD) based on Gaussian kernel
    function for keras models (pytorch backend)
    
    - Gretton, Arthur, et al. "A kernel method for the two-sample-problem."
    Advances in neural information processing systems. 2007.

    - code adapted from https://github.com/wzell/mann/blob/master/models/maximum_mean_discrepancy.py#L23-L39
    """
    r11 = torch.outer(ratio1, ratio1)
    r12 = torch.outer(ratio1, ratio2)
    r22 = torch.outer(ratio2, ratio2)

    x1x1 = gaussian_kernel(x1, x1, beta)
    x1x2 = gaussian_kernel(x1, x2, beta)
    x2x2 = gaussian_kernel(x2, x2, beta)
    # diff = x1x1.mean() - 2 * x1x2.mean() + x2x2.mean()
    diff = x1x1 * r11 - 2 * x1x2 * r12 + x2x2 * r22
    # diff = diff * ratio_outer
    diff = diff.mean()
    return diff


def gaussian_kernel(x1, x2, beta = 1.0):
    r = torch.unsqueeze(x1, 1)
    return torch.exp( -beta * torch.square(r - x2).sum(axis=-1))



def tc(tensor):
    return tensor.detach().cpu().numpy()

    
def makedirs(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def get_logger(
    logpath, filepath, package_files=[], displaying=True, saving=True, debug=False
):
    logger = logging.getLogger()
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logger.setLevel(level)
    if saving:
        info_file_handler = logging.FileHandler(logpath, mode="a")
        info_file_handler.setLevel(level)
        logger.addHandler(info_file_handler)
    if displaying:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        logger.addHandler(console_handler)
    logger.info(filepath)
    with open(filepath, "r") as f:
        logger.info(f.read())

    for f in package_files:
        logger.info(f)
        with open(f, "r") as package_f:
            logger.info(package_f.read())

    return logger


def sample_z(m, n, std=10.0):
    s1 = np.random.normal(0, std, size=[m, n])
    # s1 = np.random.uniform(-std, std, size=[m, n])
    s1 = torch.from_numpy(s1).float()
    return s1


def keep_grad(output, input, grad_outputs=None):
    return torch.autograd.grad(
        output, input, grad_outputs=grad_outputs, retain_graph=True, create_graph=True
    )[0]




# can be moved to sysflow 
# tools for visualization
import matplotlib
from matplotlib.lines import Line2D 
def plot_grad_flow(named_parameters):
    '''Plots the gradients flowing through different layers in the net during training.
    Can be used for checking for possible gradient vanishing / exploding problems.
    
    Usage: Plug this function in Trainer class after loss.backwards() as 
    "plot_grad_flow(self.model.named_parameters())" to visualize the gradient flow'''
    ave_grads = []
    max_grads= []
    layers = []
    for n, p in named_parameters:
        if(p.requires_grad) and ("bias" not in n):
            layers.append(n)
            ave_grads.append(p.grad.abs().mean())
            max_grads.append(p.grad.abs().max())
    plt.bar(np.arange(len(max_grads)), max_grads, alpha=0.1, lw=1, color="c")
    plt.bar(np.arange(len(max_grads)), ave_grads, alpha=0.1, lw=1, color="b")
    plt.hlines(0, -0.5, len(ave_grads)+0.5, lw=2, color="k" )
    plt.xticks(range(0,len(ave_grads), 1), layers)
    plt.xlim(left=-0.5, right=len(ave_grads)-0.5)
    plt.ylim(bottom = -0.001, top=0.10) # zoom in on the lower gradient regions
    plt.xlabel("Layers")
    plt.ylabel("average gradient")
    plt.title("Gradient flow")
    plt.grid(True)
    plt.legend([Line2D([0], [0], color="c", lw=4),
                Line2D([0], [0], color="b", lw=4),
                Line2D([0], [0], color="k", lw=4)], ['max-gradient', 'mean-gradient', 'zero-gradient'])
    plt.tight_layout()
    plt.show()

