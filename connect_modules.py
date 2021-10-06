from bsb.core import from_hdf5, Scaffold, merge
from plotly import graph_objs as go
import numpy as np

filename_h5 = "300x_200z_DCN_IO.hdf5"
filename_h51 = "300x_200z.hdf5"

scaffold1 = from_hdf5(filename_h5)
scaffold2 = from_hdf5(filename_h51)

scaffolds = [scaffold1, scaffold2]


scaffold3 = merge("test.hdf5", *scaffolds)

#Plotting scaffolds to check merge functioning

def scaffold_plotter(scaffold):

    grc = scaffold.get_placement_set('granule_cell')
    print(len(grc))
    grc_ids = grc.identifiers   #tutti gli ids delle GrC
    print(len(grc_ids))
    id_first_grc = grc_ids[0]
    grc_pos = grc.positions   

    pc =  scaffold.get_placement_set('purkinje_cell')
    pc_ids = pc.identifiers    
    print(len(pc_ids))
    id_first_pc = pc_ids[0]
    pc_pos = pc.positions    

    grc_conn_ids=scaffold.get_connectivity_set("parallel_fiber_to_purkinje").from_identifiers   
    pc_conn_ids = scaffold.get_connectivity_set("parallel_fiber_to_purkinje").to_identifiers   

    go.Figure(go.Scatter3d(x=grc_pos[:,0],y=grc_pos[:,1], z=grc_pos[:,2])).show()
    go.Figure(go.Scatter3d(x=pc_pos[:,0],y=pc_pos[:,1], z=pc_pos[:,2])).show()

scaffold_plotter(scaffold1)
scaffold_plotter(scaffold2)
scaffold_plotter(scaffold3)

#Connecting pf and PC
cs = scaffold3.get_connectivity_set('parallel_fiber_to_purkinje')
from_ids = cs.from_identifiers
#sel_from_ids = seleziona solo quelli che abbiamo la label dello scaffold1
to_ids = cs.to_identifiers
##sel_to_ids = seleziona solo quelli che abbiamo la label dello scaffold2
conn_data = np.column_stack((sel_from_ids, sel_to_ids))
scaffold3.connect_cells(connection_strategy, conn_data)