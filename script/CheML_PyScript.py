########################### INPUT
import numpy as np
import pandas as pd

data = pd.read_csv('benchmarks/homo_dump/sample_50/data_NOsmi_50.csv',
                   sep = None,
                   skiprows = 0,
                   header = 0)
target = pd.read_csv('benchmarks/homo_dump/sample_50/homo_50.csv',
                     sep = None,
                     skiprows = 0,
                     header = None)
###########################

########################### OUTPUT
from cheml import initialization

output_directory, log_file, error_file = initialization.output(output_directory = 'CheML.out',
                                                               logfile = 'log.txt',
                                                               errorfile = 'error.txt')
###########################

########################### MISSING_VALUES
from cheml import preprocessing

missval = preprocessing.missing_values(strategy = 'zero',
                                       string_as_null = True,
                                       inf_as_null = True,
                                       missing_values = False)
data = missval.fit(data)
target = missval.fit(target)
data, target = missval.transform(data, target)
###########################

########################### StandardScaler
from sklearn.preprocessing import StandardScaler

StandardScaler_API = StandardScaler(copy = True,
                                    with_mean = True,
                                    with_std = True)
StandardScaler_API_data, data = preprocessing.transformer_dataframe(transformer = StandardScaler_API,
                                                                    df = data)
###########################

########################### MinMaxScaler
from sklearn.preprocessing import MinMaxScaler

MinMaxScaler_API = MinMaxScaler(copy = True,
                                feature_range = (0,1))
MinMaxScaler_API_data, data = preprocessing.transformer_dataframe(transformer = MinMaxScaler_API,
                                                                  df = data)
###########################

########################### MaxAbsScaler
from sklearn.preprocessing import MaxAbsScaler

MaxAbsScaler_API = MaxAbsScaler(copy = True)
MaxAbsScaler_API_data, data = preprocessing.transformer_dataframe(transformer = MaxAbsScaler_API,
                                                                  df = data)
###########################

########################### RobustScaler
from sklearn.preprocessing import RobustScaler

RobustScaler_API = RobustScaler(with_centering = True,
                                copy = True,
                                with_scaling = True)
RobustScaler_API_data, data = preprocessing.transformer_dataframe(transformer = RobustScaler_API,
                                                                  df = data)
###########################

########################### Normalizer
from sklearn.preprocessing import Normalizer

Normalizer_API = Normalizer(copy = True,
                            norm = 'l2')
Normalizer_API_data, data = preprocessing.transformer_dataframe(transformer = Normalizer_API,
                                                                df = data)
###########################

########################### Binarizer
from sklearn.preprocessing import Binarizer

Binarizer_API = Binarizer(threshold = 0.0,
                          copy = True)
Binarizer_API_data, data = preprocessing.transformer_dataframe(transformer = Binarizer_API,
                                                               df = data)
###########################

########################### OneHotEncoder
from sklearn.preprocessing import OneHotEncoder

OneHotEncoder_API = OneHotEncoder(dtype = np.float,
                                  handle_unknown = 'error',
                                  sparse = True,
                                  categorical_features = 'all',
                                  n_values = 'auto')
OneHotEncoder_API_data, data = preprocessing.transformer_dataframe(transformer = OneHotEncoder_API,
                                                                   df = data)
###########################

########################### PolynomialFeatures
from sklearn.preprocessing import PolynomialFeatures

PolynomialFeatures_API = PolynomialFeatures(include_bias = True,
                                            interaction_only = False,
                                            degree = 2)
PolynomialFeatures_API_data, data = preprocessing.transformer_dataframe(transformer = PolynomialFeatures_API,
                                                                        df = data)
###########################

########################### FunctionTransformer
from sklearn.preprocessing import FunctionTransformer

FunctionTransformer_API = FunctionTransformer(validate = True,
                                              accept_sparse = False,
                                              func = None,
                                              pass_y = False)
FunctionTransformer_API_data, data = preprocessing.transformer_dataframe(transformer = FunctionTransformer_API,
                                                                         df = data)
###########################

########################### VarianceThreshold
from sklearn.feature_selection import VarianceThreshold

VarianceThreshold_API = VarianceThreshold(threshold = 0.0)
VarianceThreshold_API_data, data = preprocessing.selector_dataframe(transformer = VarianceThreshold_API,
                                                                    df = data,
                                                                    tf = target)
###########################

########################### SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.feature_selection import SelectKBest

SelectKBest_API = SelectKBest(k = 10,
                              score_func = f_regression)
SelectKBest_API_data, data = preprocessing.selector_dataframe(transformer = SelectKBest_API,
                                                              df = data,
                                                              tf = target)
###########################

########################### SelectPercentile
from sklearn.feature_selection import SelectPercentile

SelectPercentile_API = SelectPercentile(percentile = 10,
                                        score_func = f_regression)
SelectPercentile_API_data, data = preprocessing.selector_dataframe(transformer = SelectPercentile_API,
                                                                   df = data,
                                                                   tf = target)
###########################

########################### SelectFpr
from sklearn.feature_selection import SelectFpr

SelectFpr_API = SelectFpr(alpha = 0.05,
                          score_func = f_regression)
SelectFpr_API_data, data = preprocessing.selector_dataframe(transformer = SelectFpr_API,
                                                            df = data,
                                                            tf = target)
###########################

########################### SelectFdr
from sklearn.feature_selection import SelectFdr

SelectFdr_API = SelectFdr(alpha = 0.05,
                          score_func = f_regression)
SelectFdr_API_data, data = preprocessing.selector_dataframe(transformer = SelectFdr_API,
                                                            df = data,
                                                            tf = target)
###########################

########################### SelectFwe
from sklearn.feature_selection import SelectFwe

SelectFwe_API = SelectFwe(alpha = 0.05,
                          score_func = f_regression)
SelectFwe_API_data, data = preprocessing.selector_dataframe(transformer = SelectFwe_API,
                                                            df = data,
                                                            tf = target)
###########################

########################### RFE
from sklearn.feature_selection import RFE

RFE_API = RFE(step = 1,
              estimator = _API,
              verbose = 0,
              estimator_params = None,
              n_features_to_select = None)
RFE_API_data, data = preprocessing.selector_dataframe(transformer = RFE_API,
                                                      df = data,
                                                      tf = target)
###########################

########################### RFECV
from sklearn.feature_selection import RFECV

RFECV_API = RFECV(scoring = None,
                  verbose = 0,
                  step = 1,
                  estimator_params = None,
                  estimator = _API,
                  cv = None)
RFECV_API_data, data = preprocessing.selector_dataframe(transformer = RFECV_API,
                                                        df = data,
                                                        tf = target)
###########################

