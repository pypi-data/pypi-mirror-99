import pandas as pd
import numpy as np
import math

class SparseTensor:
    """Wrapper around a pandas DataFrame to represent a sparse tensor

       The DataFrame should have N index columns (int type) and 1 value column (float type)
       N is the dimensionality of the tensor

       You can also specify the shape of the tensor. If you don't it is detected automatically.
    """
       
    def __init__(self, data, shape = None):
        if type(data) == SparseTensor:
            self.data = data.data
            self.nnz = data.nnz

            if shape is not None:
                self.shape = shape
            else:
                self.shape = data.shape
        elif type(data) == pd.DataFrame:
            self.data = data
            self.nnz = len(data.index)

            idx_column_names = list(filter(lambda c: data[c].dtype==np.int64 or data[c].dtype==np.int32, data.columns))
            val_column_names = list(filter(lambda c: data[c].dtype==np.float32 or data[c].dtype==np.float64, data.columns))


            if len(val_column_names) != 1:
                error_msg = "tensor has {} float columns but must have exactly 1 value column.".format(len(val_column_names))
                raise ValueError(error_msg)

            if shape is not None:
                self.shape = shape
            else:
                self.shape = [data[c].max() + 1 for c in idx_column_names]
        else:
            error_msg = "Unsupported sparse tensor data type: {}".format(data)
            raise ValueError(error_msg)

        self.ndim = len(self.shape)

class PyNoiseConfig:
    def __init__(self, noise_type = "fixed", precision = 5.0, sn_init = 1.0, sn_max = 10.0, threshold = 0.5): 
        self.noise_type = noise_type
        self.precision = precision
        self.sn_init = sn_init
        self.sn_max = sn_max
        self.threshold = threshold

class FixedNoise(PyNoiseConfig):
    def __init__(self, precision = 5.0): 
        PyNoiseConfig.__init__(self, "fixed", precision)

class SampledNoise(PyNoiseConfig):
    def __init__(self, precision = 5.0): 
        PyNoiseConfig.__init__(self, "sampled", precision)

class AdaptiveNoise(PyNoiseConfig):
    def __init__(self, sn_init = 5.0, sn_max = 10.0): 
        PyNoiseConfig.__init__(self, "adaptive", sn_init = sn_init, sn_max = sn_max)

class ProbitNoise(PyNoiseConfig):
    def __init__(self, threshold = 0.): 
        PyNoiseConfig.__init__(self, "probit", threshold = threshold)

class StatusItem:
    """Short set of parameters indicative for the training progress.
    
    Attributes
    ----------

    phase : { "Burnin", "Sampling" }

    iter : int
        Current iteration in current phase

    phase_iter : int
        Number of iterations in this phase

    model_norms : list of float
        Norm of each U/V matrix

    rmse_avg : float
        Averag RMSE for test matrix across all samples

    rmse_1sample : float
        RMSE for test matrix of last sample

    train_rmse : float
        RMSE for train matrix of last sample

    auc_1sample : float
        ROC AUC of the test matrix of the last sample
        Only available if you provided a threshold.

    auc_avg : float
        Averag ROC AUC of the test matrix accross all samples
        Only available if you provided a threshold.

    elapsed_iter : float
        Number of seconds the last sampling iteration took

    nnz_per_sec : float
        Compute performance indicator; number of non-zero elements in train processed per second

    samples_per_sec : float
        Compute performance indicator; number of rows and columns in U/V processed per second


    """
    
    def __init__(self, phase, iter, phase_iter, model_norms, rmse_avg, rmse_1sample, train_rmse, auc_1sample, auc_avg, elapsed_iter, nnz_per_sec, samples_per_sec):
        self.phase = phase.decode('UTF-8')
        self.iter = iter
        self.phase_iter = phase_iter
        self.model_norms = model_norms
        self.rmse_avg = rmse_avg
        self.rmse_1sample = rmse_1sample
        self.train_rmse = train_rmse
        self.auc_1sample = auc_1sample
        self.auc_avg = auc_avg
        self.elapsed_iter = elapsed_iter
        self.nnz_per_sec = nnz_per_sec
        self.samples_per_sec = samples_per_sec

    def __str__(self):
        model_norms_str = ",".join("%d: %.2f" % (i,m) for i,m in enumerate(self.model_norms))

        if  math.isnan(self.auc_1sample):
            auc_str = ""
        else:
            auc_str = "AUC: %.2f (1sample: %.2f) " % (self.auc_avg, self.auc_1sample)

        return "%7s: %3d/%d RMSE: %.2f (1samp: %.2f) %sU: [ %s ] took %.1fs" % (
            self.phase, self.iter, self.phase_iter, self.rmse_avg, self.rmse_1sample,
            auc_str, model_norms_str, self.elapsed_iter)

    def __repr__(self):
        return str(self)
