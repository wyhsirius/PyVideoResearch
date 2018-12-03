""" Define and parse commandline arguments """
import argparse
import os


def parse():
    print('parsing arguments')
    parser = argparse.ArgumentParser(description='PyTorch Charades Training')

    # Experiment parameters
    parser.add_argument('--name', default='test')
    parser.add_argument('--resume', default='', help='path to latest checkpoint (default: none)')
    parser.add_argument('-e', '--evaluate', dest='evaluate', action='store_true', help='evaluate on validation sets')
    parser.add_argument('--cache-dir', default='./cache/')
    parser.add_argument('--metric', default='CharadesmAPvalvideo', help='metric to find best model')
    parser.add_argument('--metrics', default='top1_metric;top5_metric', help='metrics during training and validation')
    parser.add_argument('--videometrics', default='charades_map_metric;videotop1_metric;videotop5_metric')

    # Data parameters
    parser.add_argument('--data', default='/scratch/gsigurds/Charades_v1_rgb/', help='path to dataset')
    parser.add_argument('--valdata', default='')
    parser.add_argument('--dataset', default='fake', help='name of dataset under datasets/')
    parser.add_argument('--train-file', default='./Charades_v1_train.csv')
    parser.add_argument('--val-file', default='./Charades_v1_test.csv')
    parser.add_argument('--label-file', default='', help='path to list of labels for dataset')
    parser.add_argument('--temporal-segments', default=3, type=int, help='for loading data for TSN')

    # Model parameters
    parser.add_argument('--arch', '-a', default='alexnet', help='model architecture: ')
    parser.add_argument('--input-size', default=224, type=int)
    parser.add_argument('--dropout', default=0, type=float, help='[0-1], 0 = leave defaults')
    parser.add_argument('--pretrained', dest='pretrained', action='store_true', help='use pre-trained model')
    parser.add_argument('--pretrained-weights', default='')
    parser.add_argument('--nclass', default=157, type=int)
    parser.add_argument('--wrapper', default='async_tf_base',
                        help='child of nn.Module that wraps the base arch. ''default_wrapper'' for no wrapper')
    parser.add_argument('--criterion', default='async_tf_criterion', help=' ''default_criterion'' for sigmoid loss')

    # System parameters
    parser.add_argument('-j', '--workers', default=4, type=int, help='number of data loading workers (default: 4)')
    parser.add_argument('--print-freq', '-p', default=10, type=int, help='print frequency (default: 10)')
    parser.add_argument('--world-size', default=1, type=int, help='number of distributed processes')
    parser.add_argument('--dist-url', default='tcp://224.66.41.62:23456', help='url for distributed training')
    parser.add_argument('--dist-backend', default='gloo', help='distributed backend')
    parser.add_argument('--manual-seed', default=0, type=int)
    parser.add_argument('--no-logger', dest='no_logger', action='store_true')
    parser.add_argument('--disable-cudnn-benchmark', action='store_true', help='in case it is causing problems')
    parser.add_argument('--disable-cudnn', action='store_true', help='in case it is causing problems')

    # Training parameters
    parser.add_argument('--epochs', default=20, type=int, help='number of total epochs to run')
    parser.add_argument('--start-epoch', default=0, type=int, help='manual epoch number (useful on restarts)')
    parser.add_argument('-b', '--batch-size', default=256, type=int, help='mini-batch size (default: 256)')
    parser.add_argument('--video-batch-size', default=-1, type=int, help='size for video testing, -1 for whole batch')
    parser.add_argument('--lr', '--learning-rate', default=1e-3, type=float, help='initial learning rate')
    parser.add_argument('--lr-decay-rate', default='6', type=str)
    parser.add_argument('--momentum', default=0.9, type=float, help='momentum')
    parser.add_argument('--weight-decay', '--wd', default=1e-4, type=float, help='weight decay (default: 1e-4)')
    parser.add_argument('--balanceloss', dest='balanceloss', action='store_true')
    parser.add_argument('--freeze-batchnorm', dest='freeze_batchnorm', action='store_true')
    parser.add_argument('--train-size', default=1.0, type=float)
    parser.add_argument('--val-size', default=1.0, type=float)
    parser.add_argument('--accum-grad', default=1, type=int)
    parser.add_argument('--warmups', default=0, type=int)
    parser.add_argument('--no-val-video', dest='no_val_video', action='store_true')
    parser.add_argument('--synchronous', dest='synchronous', action='store_true')

    # Asynchronous Temporal Fields Parameters
    parser.add_argument('--temporal-weight', default=1.0, type=float)
    parser.add_argument('--temporalloss-weight', default=1.0, type=float)
    parser.add_argument('--memory-decay', default=0.9, type=float)
    parser.add_argument('--memory-size', default=20, type=int)
    parser.add_argument('--sigma', default=150, type=float)
    parser.add_argument('--nhidden', default=10, type=int)
    parser.add_argument('--adjustment', dest='adjustment', action='store_true')
    parser.add_argument('--originalloss-weight', default=1, type=float)
    parser.add_argument('--window-smooth', default=3, type=int)
    parser.add_argument('--videoloss', dest='videoloss', action='store_true')

    # AVA FRCNN Parameters
    parser.add_argument('--freeze-head', action='store_true')
    parser.add_argument('--freeze-base', action='store_true')

    # Actor Observer Parameters
    parser.add_argument('--decay', default=0.9, type=float)

    args = parser.parse_args()
    args.distributed = args.world_size > 1
    args.cache = args.cache_dir + args.name + '/'
    if args.valdata == '':
        args.valdata = args.data
    if not os.path.exists(args.cache):
        os.makedirs(args.cache)
    if args.wrapper == 'default':
        args.wrapper = 'default_wrapper'
    if args.criterion == 'default':
        args.criterion = 'default_criterion'

    return args
