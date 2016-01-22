#!/usr/bin/env python

PROGRAM_NAME = "CheML"
PROGRAM_VERSION = "v0.0.1"
REVISION_DATE = "2015-06-23"
AUTHORS = "Johannes Hachmann (hachmann@buffalo.edu) and Mojtaba Haghighatlari (mojtabah@buffalo.edu)"
CONTRIBUTORS = " "
DESCRIPTION = "ChemML is a machine learning and informatics program suite for the chemical and materials sciences."

# Version history timeline (move to CHANGES periodically):
# v0.0.1 (2015-06-02): complete refactoring of original CheML code in new package format


###################################################################################################
#TODO:
# -restructure more general functions into modules
###################################################################################################

import sys
import os
import time
import copy
import argparse
from lxml import objectify, etree
from sct_utils import isfloat, islist, istuple, isnpdot, std_datetime_str

#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
"""*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*

 									CheML FUNCTIONS 		

#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#"""
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*									  

def _block_finder(script, blocks={}, it=-1):
    for line in script:
        if '##' in line:
            it += 1    
            blocks[it] = [line]
            continue
        elif '#' not in line and '%' in line:
            blocks[it].append(line)
            continue
    return blocks

def _functions(line):
    if '%' in line:
        function = line[line.index('##')+2:line.index('%')].strip()
    else:
        function = line[line.index('##')+2:].strip()
    return function

def _options(blocks, it=-1):
    cmls = []
    for i in xrange(len(blocks)):
        it += 1
        block = blocks[i]
        cmls.append({"function": _functions(block[0]),
                     "parameters": {}})
        for line in block:
            while '%%' in line:
                line = line[line.index('%%')+2:].strip()
                if '%' in line:
                    args = line[:line.index('%')].strip()
                else:
                    args = line.strip()
                param = args[:args.index('=')].strip()
                val = args[args.index('=')+1:].strip()
                exec("cmls[it]['parameters']['%s']"%param+'='+'"%s"'%val)
    return cmls
    
def main(SCRIPT_NAME):
    """main:
        Driver of ChemML
    """
    global cmls
    global imports
    global cmlnb
    global it
    
    script = open(SCRIPT_NAME,'r')
    script = script.readlines()
    blocks = _block_finder(script)
    cmls = _options(blocks)
    
    ## CHECK SCRIPT'S REQUIREMENTS    
    called_functions = [block["function"] for block in cmls]
    if "INPUT" not in called_functions:
        raise RuntimeError("cheml requires input data")
        # TODO: check typical error names		

    ## PYTHON SCRIPT
    if "OUTPUT" in called_functions:
        output_ind = called_functions.index("OUTPUT")
        pyscript_file = cmls[output_ind]['parameters']['filename_pyscript'][1:-1]
    else:
        pyscript_file = "CheML_PyScript.py"
    cmlnb = {"blocks": [],
             "date": std_datetime_str('date'),
             "time": std_datetime_str('time'),
             "file_name": pyscript_file,
             "version": "1.1.0"
            }
    imports = []    
    it = -1
    
    ## implementing orders
    functions = {'INPUT'                : INPUT,
                 'OUTPUT'               : OUTPUT,
                 'MISSING_VALUES'       : MISSING_VALUES,
                 'StandardScaler'       : StandardScaler,
                 'MinMaxScaler'         : MinMaxScaler,
                 'MaxAbsScaler'         : MaxAbsScaler,
                 'RobustScaler'         : RobustScaler,
                 'Normalizer'           : Normalizer,
                 'Binarizer'            : Binarizer,
                 'OneHotEncoder'        : OneHotEncoder,
                 'PolynomialFeatures'   : PolynomialFeatures,
                 'FunctionTransformer'  : FunctionTransformer,
                 'VarianceThreshold'    : VarianceThreshold,
                 'SelectKBest'          : SelectKBest,
                 'SelectPercentile'     : SelectPercentile,
                 'SelectFpr'            : SelectFpr,
                 'SelectFdr'            : SelectFdr,
                 'SelectFwe'            : SelectFwe,
                 'RFE'                  : RFE,
                 'RFECV'                : RFECV,
                 'SelectFromModel'      : SelectFromModel
                 
                }

    for block in cmls:
        if block['function'] not in functions:
            raise NameError("name %s is not defined"%block['function'])
        else:
            it += 1
            cmlnb["blocks"].append({"function": block['function'],
                                    "imports": [],
                                    "source": []
                                    })
            functions[block['function']](block)
    
    ## write files
    pyscript = open(pyscript_file,'w',0)
    for block in cmlnb["blocks"]:
        pyscript.write(banner('begin', block["function"]))
        for line in block["imports"]:
            pyscript.write(line)
        pyscript.write('\n')
        for line in block["source"]:
            pyscript.write(line)
        pyscript.write(banner('end', block["function"]))
        pyscript.write('\n')
        
    print "\n"
    print "NOTES:"
    print "* The python script with name '%s' has been stored in the current directory."\
        %pyscript_file
    print "** list of required 'package: module's in the python script:", imports
    print "\n"

    return 0    #successful termination of program
    
##################################################################################################

def write_split(line):
    """(write_split):
        Write the invoked line of python code in multiple lines.
    """ 
    pran_ind = line.index('(')
    function = line[:pran_ind+1]
    options = line[pran_ind+1:].split(';')
    spaces = len(function)
    lines = [function + options[0]+',\n'] + [' ' * spaces + options[i] +',\n' for i in range(1,len(options)-1)] + [' ' * spaces + options[-1]+'\n']
    return lines

##################################################################################################

def banner(state, function):
    """(banner):
        Sign begin and end of a function.
    """
    secondhalf = 71-len(function)-2-27 
    if state == 'begin':
        line = '#'*27 + ' ' + function + '\n'
        return line
    if state == 'end':
        line = '#'*27 + '\n'
        return line 
	
##################################################################################################

def gen_skl_preprocessing(block, skl_funct, skl_class, cml_funct, interface, frames):
    if cml_funct:
        if "cheml: %s"%cml_funct not in imports:
            cmlnb["blocks"][it]["imports"].append("from cheml import %s\n"%cml_funct)
            imports.append("cheml: %s"%cml_funct)    
    if "sklearn: %s"%skl_funct not in imports:
        cmlnb["blocks"][it]["imports"].append("from sklearn.%s import %s\n"%(skl_class,skl_funct))
        imports.append("sklearn: %s"%skl_funct)
    
    line = "%s_%s = %s(" %(skl_funct,'API',skl_funct)
    param_count = 0
    for parameter in block["parameters"]:
        param_count += 1
        line += """;%s = %s"""%(parameter,block["parameters"][parameter])
    line += ')'
    line = line.replace('(;','(')
    
    if param_count > 1 :
        cmlnb["blocks"][it]["source"] += write_split(line)
    else:
        cmlnb["blocks"][it]["source"].append(line + '\n')
    
    for frame in frames:
        line = """%s_%s_%s, %s = preprocessing.%s(transformer = %s_%s;df = %s)"""\
            %(skl_funct,'API',frame,frame,interface,skl_funct,'API',frame)
        cmlnb["blocks"][it]["source"] += write_split(line)

##################################################################################################

def gen_skl_featureselection(block, skl_funct, skl_class, cml_funct, interface, frames):
    if cml_funct:
        if "cheml: %s"%cml_funct not in imports:
            cmlnb["blocks"][it]["imports"].append("from cheml import %s\n"%cml_funct)
            imports.append("cheml: %s"%cml_funct)    
    if "sklearn: %s"%skl_funct not in imports:
        cmlnb["blocks"][it]["imports"].append("from sklearn.%s import %s\n"%(skl_class,skl_funct))
        imports.append("sklearn: %s"%skl_funct)
    
    line = "%s_%s = %s(" %(skl_funct,'API',skl_funct)
    param_count = 0
    for parameter in block["parameters"]:
        param_count += 1
        line += """;%s = %s"""%(parameter,block["parameters"][parameter])
    line += ')'
    line = line.replace('(;','(')
    
    if param_count > 1 :
        cmlnb["blocks"][it]["source"] += write_split(line)
    else:
        cmlnb["blocks"][it]["source"].append(line + '\n')
    
    line = """%s_%s_%s, %s = preprocessing.%s(transformer = %s_%s;df = %s;tf = %s)"""\
        %(skl_funct,'API','data','data',interface,skl_funct,'API','data','target')
    cmlnb["blocks"][it]["source"] += write_split(line)

##################################################################################################

def INPUT(block):
    """(INPUT):
		Read input files.
		pandas.read_csv: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
    """
    cmlnb["blocks"][it]["imports"].append("import numpy as np\n")
    imports.append("numpy")
    
    cmlnb["blocks"][it]["imports"].append("import pandas as pd\n")
    imports.append("pandas")
    
    line = "data = pd.read_csv(%s;sep = %s;skiprows = %s;header = %s)"\
        %(block["parameters"]["data_path"], block["parameters"]["data_delimiter"],\
        block["parameters"]["data_skiprows"], block["parameters"]["data_header"])
    cmlnb["blocks"][it]["source"] += write_split(line)
    
    line = "target = pd.read_csv(%s;sep = %s;skiprows = %s;header = %s)"\
        %(block["parameters"]["target_path"], block["parameters"]["target_delimiter"],\
        block["parameters"]["target_skiprows"],block["parameters"]["target_header"])
    cmlnb["blocks"][it]["source"] += write_split(line) 	
									
									###################
def OUTPUT(block):
    """(OUTPUT):
		Open output files.
    """
    if "cheml: initialization" not in imports:
        cmlnb["blocks"][it]["imports"].append("from cheml import initialization\n")
        imports.append("cheml: initialization")
    line = "output_directory, log_file, error_file = initialization.output(output_directory = %s;logfile = %s;errorfile = %s)"\
        %(block["parameters"]["path"], block["parameters"]["filename_logfile"],\
        block["parameters"]["filename_errorfile"])
    cmlnb["blocks"][it]["source"] += write_split(line)
									
									###################
def MISSING_VALUES(block):
    """(MISSING_VALUES):
		Handle missing values.
    """
    if "cheml: preprocessing" not in imports:
        cmlnb["blocks"][it]["imports"].append("from cheml import preprocessing\n")
        imports.append("cheml: preprocessing")
    line = """missval = preprocessing.missing_values(strategy = %s;string_as_null = %s;inf_as_null = %s;missing_values = %s)"""\
        %(block["parameters"]["strategy"],block["parameters"]["string_as_null"],\
        block["parameters"]["inf_as_null"],block["parameters"]["missing_values"])
    cmlnb["blocks"][it]["source"] += write_split(line)
    line = """data = missval.fit(data)"""
    cmlnb["blocks"][it]["source"].append(line + '\n')
    line = """target = missval.fit(target)"""
    cmlnb["blocks"][it]["source"].append(line + '\n')
    if block["parameters"]["strategy"][1:-1] in ['zero', 'ignore', 'interpolate']:
        line = """data, target = missval.transform(data, target)"""
        cmlnb["blocks"][it]["source"].append(line + '\n')
    elif block["parameters"]["strategy"][1:-1] in ['mean', 'median', 'most_frequent']:
        if "sklearn: Imputer" not in imports:
            cmlnb["blocks"][it]["imports"].append("from sklearn.preprocessing import Imputer\n")
            imports.append("sklearn: Imputer")
        line = """imp = Imputer(strategy = %s;missing_values = 'NaN';axis = 0;verbose = 0;copy = True)"""\
            %(block["parameters"]["strategy"])
        cmlnb["blocks"][it]["source"] += write_split(line)
        line = """imp_data, data = preprocessing.Imputer_dataframe(imputer = imp;df = data)"""
        cmlnb["blocks"][it]["source"] += write_split(line)
        line = """imp_target, target = preprocessing.Imputer_dataframe(imputer = imp;df = target)"""
        cmlnb["blocks"][it]["source"] += write_split(line)
									
									###################
def StandardScaler(block):
    """(StandardScaler):
		http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html#sklearn.preprocessing.StandardScaler
    """
    skl_funct = 'StandardScaler'
    cml_funct = 'preprocessing'
    skl_class = 'preprocessing'
    interface = 'transformer_dataframe'
    frames=['data']  # ,'target'
    
    gen_skl_preprocessing(block, skl_funct, skl_class, cml_funct, interface, frames)    
									
									###################
def MinMaxScaler(block):
    """(MinMaxScaler):
        http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html#sklearn.preprocessing.MinMaxScaler    
    """
    skl_funct = 'MinMaxScaler'
    cml_funct = 'preprocessing'
    skl_class = 'preprocessing'
    interface = 'transformer_dataframe'
    frames=['data']  # ,'target'
    
    gen_skl_preprocessing(block, skl_funct, skl_class, cml_funct, interface, frames)    
									
									###################
def MaxAbsScaler(block):
    """(MaxAbsScaler):
        http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MaxAbsScaler.html#sklearn.preprocessing.MaxAbsScaler    
    """
    skl_funct = 'MaxAbsScaler'
    cml_funct = 'preprocessing'
    skl_class = 'preprocessing'
    interface = 'transformer_dataframe'
    frames=['data']  # ,'target'
    
    gen_skl_preprocessing(block, skl_funct, skl_class, cml_funct, interface, frames)    
									
									###################
def RobustScaler(block):
    """(RobustScaler):
        http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.RobustScaler.html#sklearn.preprocessing.RobustScaler    
    """
    skl_funct = 'RobustScaler'
    cml_funct = 'preprocessing'
    skl_class = 'preprocessing'
    interface = 'transformer_dataframe'
    frames=['data']  # ,'target'
    
    gen_skl_preprocessing(block, skl_funct, skl_class, cml_funct, interface, frames)    

									###################
def Normalizer(block):
    """(Normalizer):
        http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.Normalizer.html#sklearn.preprocessing.Normalizer    
    """
    skl_funct = 'Normalizer'
    cml_funct = 'preprocessing'
    skl_class = 'preprocessing'
    interface = 'transformer_dataframe'
    frames=['data']  # ,'target'
    
    gen_skl_preprocessing(block, skl_funct, skl_class, cml_funct, interface, frames)    

									###################
def Binarizer(block):
    """(Binarizer):
        http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.Binarizer.html#sklearn.preprocessing.Binarizer    
    """
    skl_funct = 'Binarizer'
    cml_funct = 'preprocessing'
    skl_class = 'preprocessing'
    interface = 'transformer_dataframe'
    frames=['data']  # ,'target'
    
    gen_skl_preprocessing(block, skl_funct, skl_class, cml_funct, interface, frames)    

									###################
def OneHotEncoder(block):
    """(OneHotEncoder):
        http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html    
    """
    skl_funct = 'OneHotEncoder'
    cml_funct = 'preprocessing'
    skl_class = 'preprocessing'
    interface = 'transformer_dataframe'
    frames=['data']  # ,'target'
    
    gen_skl_preprocessing(block, skl_funct, skl_class, cml_funct, interface, frames)    

									###################
def PolynomialFeatures(block):
    """(PolynomialFeatures):
        http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html#sklearn.preprocessing.PolynomialFeatures   
    """
    skl_funct = 'PolynomialFeatures'
    cml_funct = 'preprocessing'
    skl_class = 'preprocessing'
    interface = 'transformer_dataframe'
    frames=['data']  # ,'target'
    
    gen_skl_preprocessing(block, skl_funct, skl_class, cml_funct, interface, frames)    

									###################
def FunctionTransformer(block):
    """(FunctionTransformer):
        http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.FunctionTransformer.html#sklearn.preprocessing.FunctionTransformer   
    """
    skl_funct = 'FunctionTransformer'
    cml_funct = 'preprocessing'
    skl_class = 'preprocessing'
    interface = 'transformer_dataframe'
    if block["parameters"]["pass_y"]=='True' :
        frames=['data','target']  # ,'target'
    else:
        frames=['data']  # ,'target'
    
    gen_skl_preprocessing(block, skl_funct, skl_class, cml_funct, interface, frames)    

									###################
def VarianceThreshold(block):
    """(VarianceThreshold):
        http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.VarianceThreshold.html#sklearn.feature_selection.VarianceThreshold    
    """
    skl_class = 'feature_selection'
    skl_funct = 'VarianceThreshold'
    cml_funct = 'preprocessing'
    interface = 'selector_dataframe'
    frames=['data']  # ,'target'
    
    gen_skl_featureselection(block, skl_funct, skl_class, cml_funct, interface, frames)    

									###################
def SelectKBest(block):
    """(SelectKBest):
        http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html#sklearn.feature_selection.SelectKBest   
    """
    skl_class = 'feature_selection'
    skl_funct = 'SelectKBest'
    cml_funct = 'preprocessing'
    interface = 'selector_dataframe'
    frames=['data']  # ,'target'
    
    if "sklearn: %s"%block["parameters"]["score_func"] not in imports:
        cmlnb["blocks"][it]["imports"].append("from sklearn.%s import %s\n"%(skl_class,block["parameters"]["score_func"]))
        imports.append("sklearn: %s"%block["parameters"]["score_func"])
    
    gen_skl_featureselection(block, skl_funct, skl_class, cml_funct, interface, frames)    

									###################
def SelectPercentile(block):
    """(SelectPercentile):
        http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectPercentile.html#sklearn.feature_selection.SelectPercentile  
    """
    skl_class = 'feature_selection'
    skl_funct = 'SelectPercentile'
    cml_funct = 'preprocessing'
    interface = 'selector_dataframe'
    frames=['data']  # ,'target'
    
    if "sklearn: %s"%block["parameters"]["score_func"] not in imports:
        cmlnb["blocks"][it]["imports"].append("from sklearn.%s import %s\n"%(skl_class,block["parameters"]["score_func"]))
        imports.append("sklearn: %s"%block["parameters"]["score_func"])
    
    gen_skl_featureselection(block, skl_funct, skl_class, cml_funct, interface, frames)    

									###################
def SelectFpr(block):
    """(SelectFpr):
        http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectFpr.html#sklearn.feature_selection.SelectFpr 
    """
    skl_class = 'feature_selection'
    skl_funct = 'SelectFpr'
    cml_funct = 'preprocessing'
    interface = 'selector_dataframe'
    frames=['data']  # ,'target'
    
    if "sklearn: %s"%block["parameters"]["score_func"] not in imports:
        cmlnb["blocks"][it]["imports"].append("from sklearn.%s import %s\n"%(skl_class,block["parameters"]["score_func"]))
        imports.append("sklearn: %s"%block["parameters"]["score_func"])
    
    gen_skl_featureselection(block, skl_funct, skl_class, cml_funct, interface, frames)    

									###################
def SelectFdr(block):
    """(SelectFdr):
        http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectFdr.html#sklearn.feature_selection.SelectFdr 
    """
    skl_class = 'feature_selection'
    skl_funct = 'SelectFdr'
    cml_funct = 'preprocessing'
    interface = 'selector_dataframe'
    frames=['data']  # ,'target'
    
    if "sklearn: %s"%block["parameters"]["score_func"] not in imports:
        cmlnb["blocks"][it]["imports"].append("from sklearn.%s import %s\n"%(skl_class,block["parameters"]["score_func"]))
        imports.append("sklearn: %s"%block["parameters"]["score_func"])
    
    gen_skl_featureselection(block, skl_funct, skl_class, cml_funct, interface, frames)    

									###################
def SelectFwe(block):
    """(SelectFwe):
        http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectFwe.html#sklearn.feature_selection.SelectFwe
    """
    skl_class = 'feature_selection'
    skl_funct = 'SelectFwe'
    cml_funct = 'preprocessing'
    interface = 'selector_dataframe'
    frames=['data']  # ,'target'
    
    if "sklearn: %s"%block["parameters"]["score_func"] not in imports:
        cmlnb["blocks"][it]["imports"].append("from sklearn.%s import %s\n"%(skl_class,block["parameters"]["score_func"]))
        imports.append("sklearn: %s"%block["parameters"]["score_func"])
    
    gen_skl_featureselection(block, skl_funct, skl_class, cml_funct, interface, frames)    

									###################
def RFE(block):
    """(RFE):
        http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFE.html#sklearn.feature_selection.RFE
    """
    skl_class = 'feature_selection'
    skl_funct = 'RFE'
    cml_funct = 'preprocessing'
    interface = 'selector_dataframe'
    frames=['data']  # ,'target'
    
    # Note: This function and its parameters must be called before RFECV in the script file
    block["parameters"]["estimator"] = '%s_API'%block["parameters"]["estimator"][1:-1]
    gen_skl_featureselection(block, skl_funct, skl_class, cml_funct, interface, frames)    

									###################
def RFECV(block):
    """(RFECV):
        http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFECV.html#sklearn.feature_selection.RFECV
    """
    skl_class = 'feature_selection'
    skl_funct = 'RFECV'
    cml_funct = 'preprocessing'
    interface = 'selector_dataframe'
    frames=['data']  # ,'target'
    
    # Note: This function and its parameters must be called before RFECV in the script file
    block["parameters"]["estimator"] = '%s_API'%block["parameters"]["estimator"][1:-1]
    gen_skl_featureselection(block, skl_funct, skl_class, cml_funct, interface, frames)    

									###################
def SelectFromModel(block):
    """(SelectFromModel):
        http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectFromModel.html#sklearn.feature_selection.SelectFromModel
    """
    skl_class = 'feature_selection'
    skl_funct = 'SelectFromModel'
    cml_funct = 'preprocessing'
    interface = 'selector_dataframe'
    frames=['data']  # ,'target'
    
    # Note: This function and its parameters must be called before RFECV in the script file
    block["parameters"]["estimator"] = '%s_API'%block["parameters"]["estimator"][1:-1]
    gen_skl_featureselection(block, skl_funct, skl_class, cml_funct, interface, frames)    


#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
"""*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
 
 									  CheML PySCRIPT		
																						
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#"""
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*					

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="ChemML will be started by specifying a script file as a todo list")
    parser.add_argument("-i", type=str, required=True, help="input directory: must include the script file name and its format")                    		
    args = parser.parse_args()            		
    SCRIPT_NAME = args.i      
    main(SCRIPT_NAME)   #numbering of sys.argv is only meaningful if it is launched as main
    
else:
    sys.exit("Sorry, must run as driver...")



								  


	


