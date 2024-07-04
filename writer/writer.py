"""Class defining the writer"""

import imageio.v3 as iio
import numpy as np
import h5py
import os

class Writer():

 
    def __init__(self, opt):
        self.pixels = opt.pixels
        self.outdir = opt.out_dir
        self.run_name = opt.run_name
        self.vallimit = opt.valid_split/100.0
        self.trainlimit = 1-opt.test_split/100.0
        if opt.output == 'hdf5':
            self.usehdf = True
            filepath=os.path.join(opt.out_dir,opt.run_name)+'.hdf5'
            self.hdf = h5py.File(filepath,'w')
            testlength = 2*np.ceil(opt.eventcount * opt.test_split / 100.0)
            trainlength = opt.eventcount
            vallenght = 2*np.ceil(opt.eventcount * opt.valid_split / 100.0)
            width = 2*opt.pixels
            height = opt.pixels
            self.width = width
            self.height = height
            self.testset = self.hdf.create_dataset("testdata",(testlength,width,height),maxshape=(None,width,height), chunks=(1,width,height),compression="lzf")
            self.trainset = self.hdf.create_dataset("traindata",(trainlength,width,height),maxshape=(None,width,height), chunks=(1,width,height),compression="lzf")
            self.valset = self.hdf.create_dataset("valdata",(vallenght,width,height),maxshape=(None,width,height),chunks=(1,width,height),compression="lzf")

    def Write(self,data):
        counter = 1
        val_counter = 0
        test_counter = 0
        train_counter = 0

        for event in data:
            array_in = np.zeros((self.pixels,self.pixels))
            array_out = np.zeros((self.pixels,self.pixels))

            for muon in event:
                array_in[muon[3],muon[4]]=muon[5]
                array_out[muon[1],muon[2]]=muon[0]

            rnd = np.random.rand()
            namestring = str(counter)+".tif"
            if rnd < self.vallimit:
                namestring = "val/"+namestring
                if self.usehdf:
                    array = np.concatenate((array_in, array_out),axis=0 )
                    self.valset[val_counter]=array
                    val_counter+=1
            elif rnd < self.trainlimit:
                namestring = "train/"+namestring
                if self.usehdf:
                    array = np.concatenate((array_in, array_out),axis=0 )
                    self.trainset[train_counter]=array
                    train_counter+=1
            else:
                namestring = "test/"+namestring
                if self.usehdf:
                    array = np.concatenate((array_in, array_out),axis=0 )
                    self.testset[test_counter]=array
                    test_counter+=1

            if not self.usehdf:
                namein = os.path.join(self.outdir,'A',namestring)
                nameout = os.path.join(self.outdir,'B',namestring)
                iio.imwrite(namein,np.float32(array_in),plugin="tifffile")
                iio.imwrite(nameout,np.float32(array_out),plugin="tifffile")
                counter+=1

        if self.usehdf:
            self.valset.resize((val_counter,self.width,self.height))
            self.trainset.resize((train_counter,self.width,self.height))
            self.testset.resize((test_counter,self.width,self.height))