"""This file is for options reading and recording.

It owns a lot to this source: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix
"""

import argparse
import pathlib
import os

class Options():
    """This class defines options for the data transformations from simulations to input data for the GAN"""

    def __init__(self):
        """Reset the class; indication for the class has not been initialized"""

        self.initialized = False

    def initialize(self, parser):
        """Define the options"""
        # input data options
        parser.add_argument('--datadir', required=True, type=pathlib.Path, help='path to directory with the data (subdirectories)')
        # transformations
        parser.add_argument('--rnd_order', dest='rnd_order', action='store_true', help='random muon order')
        parser.add_argument('--scaling', type=float, default=1, help='data scaling for pixelization')
        parser.add_argument('--max_E', type=float, default=2e12, help='maximum muon energy/momentum for log-transformation')
        parser.add_argument('--pixels', type=int, default=256, help='amount of pixels in one direction for "image" transformation')
        parser.add_argument('--maxMove', type=float, default=20, help='how much muons are moved randomly before scaling and pixelization (cm)')

        # output
        parser.add_argument('--max_events', type=int, help='maximum number of events created')
        parser.add_argument('--max_event_size', type=int, default=50, help='maximum number of muons in a single event')
        parser.add_argument('--random_size', dest='random_size', action='store_true', help='Random event size') # random event size
        parser.add_argument('--output', type=str, default='hdf5', choices=['tiff','hdf5'],help='Output format [tiff | hdf5]')
        parser.add_argument('--out_dir', required=True, help='output directory')
        parser.add_argument('--test_split', type=int, default=10, choices=range(0,21), help='percentage of test data, max 20')
        parser.add_argument('--valid_split', type=int, default=10, choices=range(0,21), help='percentage of validation data, max 20')
        parser.add_argument('--run_name', type=str, required=True, help='output name')

        self.initialized = True

        return parser
    
    def gather_options(self):
        """Initialize parser and gather options"""

        if not self.initialized:
            parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            parser = self.initialize(parser)

        self.parser = parser

        return parser.parse_args()
    
    def save_options(self, opt):
        """Print and save options for later reconstruction of the analysis chain and generate output directory"""

        message = ''
        message += '----------------- Options ---------------\n'
        for k, v in sorted(vars(opt).items()):
            comment = ''
            default = self.parser.get_default(k)
            if v != default:
                comment = '\t[default: %s]' % str(default)
            message += '{:>25}: {:<30}{}\n'.format(str(k), str(v), comment)
        message += '----------------- End -------------------'

        # generate output directory

        if not os.path.exists(opt.out_dir):
            os.makedirs(opt.out_dir)

        # save to the disk

        file_name = os.path.join(opt.out_dir, 'options.txt')
        with open(file_name, 'wt') as opt_file:
            opt_file.write(message)
            opt_file.write('\n')

    def parse(self):
        "Parse options and save them"

        opt = self.gather_options()

        self.save_options(opt)

        self.opt = opt
        
        return self.opt
