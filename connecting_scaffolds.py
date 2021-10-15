from bsb.core import from_hdf5, Scaffold, merge
from bsb.output import HDF5Formatter
from bsb.config import JSONConfig
from plotly import graph_objs as go
import numpy as np
import json

filename_h5 = "300x_200z_DCN_IO.hdf5"
filename_h51 = "300x_200z.hdf5"
filename_merged = "test.hdf5"

scaffold1 = from_hdf5(filename_h5)
scaffold2 = from_hdf5(filename_h51)

target_ct_name = 'parallel_fiber_to_purkinje'
target_ct = scaffold2.configuration.connection_types[target_ct_name]
print(target_ct)

scaffolds = [scaffold1, scaffold2]
labels = ['first', 'second']

scaffold3 = merge(filename_merged, *scaffolds)

#Reconfiguring configuration json with labels
cfg_json = json.loads(scaffold3.configuration._raw)
cfg_json["connection_types"]["parallel_fiber_to_purkinje"]["from_cell_types"] = [
    {"type": "granule_cell", "compartments": ["parallel_fiber"], "with_label": "merged_1"}
    ]
cfg_json["connection_types"]["parallel_fiber_to_purkinje"]["to_cell_types"] = [
    {"type": "purkinje_cell", "compartments": ["pf_targets"], "with_label": "merged_2"}
    ]
config = JSONConfig(stream=json.dumps(cfg_json))
HDF5Formatter.reconfigure(filename_merged, config)

#Connecting pf and PC
target_ct_name = 'parallel_fiber_to_purkinje'
target_ct = scaffold3.configuration.connection_types[target_ct_name]
scaffold3.connect_type(target_ct)


