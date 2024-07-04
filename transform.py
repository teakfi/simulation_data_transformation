"""Transform the simulation data to usable form for transferGAN

This script is for running the transformation with optional arguments:

--data input data directory
--scaling scaling for pixelization
--max_E maximum muon energy for logarithmic transformation
--pixels amount of pixels in output
--maxMove maximum movement of origo in input location randomization
--max_event_size maximum number of muons in a single event
--random_size is the event size random or maximum
--output output type: tiff or hdf5
--out_dir name of the output directory"""

from options.options import Options
from datareader.reader import DataReader
from transform.transform import Transform
from writer.writer import Writer

if __name__ == '__main__':
    opt = Options().parse()
    muons = DataReader().read_data(opt)
    transformer = Transform(opt)

    transformed = transformer.Run(muons)

    opt.eventcount = len(transformed)

    writer = Writer(opt)
    writer.Write(transformed)

    print("tested")