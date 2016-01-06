# Note: the only pyval with capital initial is: None {Not here, but in the SCRIPT_NAME.xml}
# Note: list of values must be written in the quotation mark
from lxml import objectify, etree

cmls = objectify.Element("CheML",generation_date="12/15/2015", version="0.0.01")

f1 = objectify.SubElement(cmls, "f1", function = "INPUT", status = 'on')
cmls.f1.data_path = "benchmarks/homo_dump/sample_50/data_NOsmi_50.csv"
cmls.f1.data_delimiter = 'None'
cmls.f1.data_header = 0
cmls.f1.data_skiprows = 0
cmls.f1.target_path = "benchmarks/homo_dump/sample_50/homo_50.csv"
cmls.f1.target_delimiter = 'None'
cmls.f1.target_header = 'None'
cmls.f1.target_skiprows = 0


f2 = objectify.SubElement(cmls, "f2", function = "OUTPUT", status = 'on')
cmls.f2.path = "CheML.out"
cmls.f2.filename_pyscript = "CheML_PyScript.py"
cmls.f2.filename_logfile = "log.txt"
cmls.f2.filename_errorfile = "error.txt"

f3 = objectify.SubElement(cmls, "f3", function = "MISSING_VALUES", status = 'on')
cmls.f3.string_as_null = True
cmls.f3.missing_values = False
cmls.f3.inf_as_null = True
cmls.f3.strategy = "mean"

f4 = objectify.SubElement(cmls, "f4", function = "MISSING_VALUES", status = 'on')
cmls.f4.string_as_null = True
cmls.f4.missing_values = False
cmls.f4.inf_as_null = True
cmls.f4.strategy = "mean"

##########################################################################
objectify.deannotate(cmls)
etree.cleanup_namespaces(cmls)
with open('CMLS.xml', 'w') as outfile:
    outfile.write("%s" %etree.tostring(cmls, pretty_print=True))
