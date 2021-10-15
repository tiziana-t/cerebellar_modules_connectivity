from bsb.core import from_hdf5
from plotly import graph_objs as go
from bsb.plotting import plot_network

scaffold = from_hdf5("filename.hdf5")

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

    figure = plot_network(scaffold, cubic=False, from_memory=False)
