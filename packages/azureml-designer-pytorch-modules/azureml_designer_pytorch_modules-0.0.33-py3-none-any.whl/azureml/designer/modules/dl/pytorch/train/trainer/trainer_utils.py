import datetime
import os
import torch
from mpi4py import MPI
from azureml.studio.core.logger import logger
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data.dataloader import default_collate

_MASTER_NODE_ENV_NAME = 'AZ_BATCH_MASTER_NODE'


class DistributedConfig():
    def __init__(self, master_node):
        self.master_node = master_node
        self.distributed = self.master_node is not None and torch.cuda.is_available()
        self.rank = MPI.COMM_WORLD.Get_rank() if self.distributed else 0
        self.world_size = MPI.COMM_WORLD.Get_size() if self.distributed else 0
        self.local_rank = self.rank % torch.cuda.device_count() if self.distributed else 0
        self.dist_url = f'tcp://{self.master_node}' if self.distributed else None

    @classmethod
    def create(cls):
        master_node = os.environ.get(_MASTER_NODE_ENV_NAME, None)
        return cls(master_node)


def init_distributed_mode(rank, world_size, local_rank, dist_url):
    torch.cuda.set_device(local_rank)
    logger.info(f'Distributed init (rank {rank}, local_rank {local_rank}): {dist_url}.')
    os.environ['NCCL_BLOCKING_WAIT'] = '1'
    torch.distributed.init_process_group(backend='nccl',
                                         init_method=dist_url,
                                         world_size=world_size,
                                         rank=rank,
                                         timeout=datetime.timedelta(seconds=600))
    torch.distributed.barrier()


def is_first_rank(rank=None):
    if rank is None:
        return not torch.distributed.is_initialized() or torch.distributed.get_rank() == 0
    else:
        return rank == 0


def accuracy(output, target, topk=(1, )):
    """Computes the top k accuracy"""
    maxk = min(max(topk), output.shape[1])
    size = target.size(0)
    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.reshape(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
        res.append(correct_k / size)
    return res


def reduce_tensor(tensor):
    rt = tensor.clone()
    torch.distributed.all_reduce(rt, op=torch.distributed.ReduceOp.SUM)
    rt /= torch.distributed.get_world_size() if torch.distributed.is_initialized() else 1
    return rt


def calc_ips(batch_size, time):
    """Training throughput. Calculate images per second."""
    world_size = torch.distributed.get_world_size() if torch.distributed.is_initialized() else 1
    tbs = world_size * batch_size
    return tbs / time


def safe_default_collate(batch):
    filtered_batch = [x for x in batch if x is not None]
    if len(filtered_batch) == 0:
        return []
    return default_collate(filtered_batch)


def get_padding_batch(loader):
    padding_batch = None
    for batch in loader:
        if len(batch) > 0:
            padding_batch = batch
            break
    # TODO: raise error if padding batch is None
    return padding_batch


class AverageMeter(object):
    """Computes and stores the average and current value
    Copied from: https://github.com/pytorch/examples/blob/master/imagenet/main.py
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def get_polynomial_decay_schedule_with_warmup(optimizer,
                                              num_warmup_steps,
                                              num_training_steps,
                                              lr_warmup,
                                              lr_init=0.0001,
                                              lr_end=1e-7,
                                              power=1.0,
                                              last_epoch=-1):
    """
    Create a schedule with a learning rate that decreases as a polynomial decay from the initial lr set in the
    optimizer to end lr defined by `lr_end`, after a warmup period during which it increases linearly from 0 to the
    initial lr set in the optimizer.
    Args:
        optimizer (:class:`~torch.optim.Optimizer`):
            The optimizer for which to schedule the learning rate.
        num_warmup_steps (:obj:`int`):
            The number of steps for the warmup phase.
        num_training_steps (:obj:`int`):
            The total number of training steps.
        lr_end (:obj:`float`, `optional`, defaults to 1e-7):
            The end LR.
        power (:obj:`float`, `optional`, defaults to 1.0):
            Power factor.
        last_epoch (:obj:`int`, `optional`, defaults to -1):
            The index of the last epoch when resuming training.
    Note: `power` defaults to 1.0 as in the fairseq implementation, which in turn is based on the original BERT
    implementation at
    https://github.com/google-research/bert/blob/f39e881b169b9d53bea03d2d341b31707a6c052b/optimization.py#L37
    Return:
        :obj:`torch.optim.lr_scheduler.LambdaLR` with the appropriate schedule.
    """
    def lr_lambda(current_step: int):
        if current_step <= num_warmup_steps:
            return (lr_init + (lr_warmup - lr_init) * current_step / num_warmup_steps) / lr_init
        else:
            lr_range = lr_warmup - lr_end
            decay_steps = num_training_steps - num_warmup_steps
            pct_remaining = 1 - (current_step - num_warmup_steps) / decay_steps
            decay = lr_range * pct_remaining**power + lr_end
            return decay / lr_init  # as LambdaLR multiplies by lr_init

        # if current_step < num_warmup_steps:
        #     return float(current_step) / float(max(1, num_warmup_steps))
        # elif current_step > num_training_steps:
        #     return lr_end / lr_init  # as LambdaLR multiplies by lr_init
        # else:

    return LambdaLR(optimizer, lr_lambda, last_epoch)
