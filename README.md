# simulation data transformation

This project is for transforming simulated muon transfers from various generators and batches to uniform format(s) for use in transferGAN training.

# Output file formats:

Output can be either 1 dimensional with only total momentum or 3 dimensional with momentum divided in cartesian vectors.
Currently supported file types:
- HDF5
- TIFF

# Transformation options:
- hit location redistribution, used for spreading out data from single point source
  - maximum move
  - pixelization size
  - scaling
- momentum scaling and data accuracy
  - logarithmic scaling maximum value
  - float32 "images" supported by rest of the chain

# Requirements

- numpy

# Logarithmic scaling mathematics

$$ Log(E+1) = L x , x = pixel value from 0 to 1$$
$$ Log(2 TeV + 1) = L$$

# Code ownership
This code is work done for [Muon-Solutions Oy]{https://muon-solutions.com}. The company owns all rights to the code and has agreed to publish it under GPL-3 license.
