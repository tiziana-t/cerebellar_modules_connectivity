from bsb.core import from_hdf5, merge
from bsb.output import HDF5Formatter
from bsb.config import JSONConfig
import json
from bsb.reporting import set_verbosity

set_verbosity(3)

filename_h5 = "300x_200z_DCN_IO.hdf5"
filename_h51 = "300x_200z.hdf5"
filename_merged = "test.hdf5"

scaffold1 = from_hdf5(filename_h5)
scaffold2 = from_hdf5(filename_h51)

scaffolds = [scaffold1, scaffold2]

scaffold3 = merge(filename_merged, *scaffolds)

#Reconfiguring configuration json with labels
#The labels used here are the ones currently assigned by merge function in \bsb\core.py 
with open("additional.json", "r") as f:
  conf_to_add = json.loads(f.read())

if "connection_types" in conf_to_add:
    print("Adding connection to configuration...")
    cfg_json["connection_types"]["parallel_to_purkinje_labelled"] = conf_to_add["connection_types"]["parallel_to_purkinje_labelled"]

with open('merged.json', 'w') as outfile:
    json.dump(cfg_json, outfile, indent = 3)

config = JSONConfig("merged.json")
HDF5Formatter.reconfigure(filename_merged, config)

scaffold_merged = from_hdf5(filename_merged)

target_ct_name = 'parallel_to_purkinje_labelled'
target_ct = scaffold_merged.configuration.connection_types[target_ct_name]
scaffold_merged.connect_type(target_ct)
scaffold_merged.compile_output()              
