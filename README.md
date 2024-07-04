# simulation data transformation

This project is for transforming simulated muon transfers from various generators and batches to uniform format(s) for use in transferGAN training.

Original data is produced by simulating muons going through material

# Output file formats:

Output can be either 1 dimensional with only total momentum or 3 dimensional with momentum divided in cartesian vectors.
Currently supported file types:
- HDF5
- TIFF

# Transformation options:
- hit location redistribution, used for spreading out data from single point source
  - maximum move for the starting point of the muon in one dimension
  - pixelization size
  - scaling
- momentum scaling and data accuracy
  - logarithmic scaling maximum value
  - float32 "images" supported by rest of the chain

# Requirements

- numpy
- h5py
- imageio

# Algorithm:

Original simulation data had muons coming from a single point source, which clumped all of the data in one point. To fix it this code randomly moves the starting position of the muon in cartesian coordinates if this is desired.

After this random move the location is pixelized to desired maximum pixel size with scaling. With 1-1 scaling each pixel corresponds a centimeter in the data.

Then the momentum/energy (which are practically the same for relativistic muons), is transformed to a logarithmic scale.

## Logarithmic scaling mathematics

$$ \log(E+1) = L x , x = \textrm{pixel value from } 0\textrm{ to }1$$

$$ \log(\textrm{Maximum muon momentum } + 1) = L$$

Last part is saving the data in a user selected format.

# Code ownership
This code is work done for [Muon-Solutions Oy](https://muon-solutions.com). The company owns all rights to the code and has agreed to publish it under GPL-3 license.
