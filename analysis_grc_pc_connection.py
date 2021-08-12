import os, sys
from scaffold.core import Scaffold
from scaffold.config import JSONConfig
from scaffold.output import HDF5Formatter
from scaffold.core import from_hdf5
from scaffold.reporting import set_verbosity
import numpy as np
import time 
import matplotlib.pyplot as plt

set_verbosity(3)

filename_h5 = "300x_200z_DCN_IO.hdf5"

#fai anche questo se trova errore di qualche connessione non riconosciuta 
#configuration_object = JSONConfig("mouse_lingula_30_1_base_per_goc_conn_mod_goc.json")
#HDF5Formatter.reconfigure(filename_h5, configuration_object)

scaffold = from_hdf5(filename_h5)


#PLOT GrC (pf) - PC CONNECTION
#- ASSE X: mf_id. -Asse y: distanza del glom connesso alla mf.

grc = scaffold.get_placement_set('granule_cell')
grc_ids = grc.identifiers    #tutti gli ids delle GrC
print(len(grc_ids))
id_first_grc = grc_ids[0]
grc_pos = grc.positions   #contiene le 3 coordinate x y z di tutte le GrC. 

pc =  scaffold.get_placement_set('purkinje_cell')
pc_ids = pc.identifiers    #tutti gli ids delle pc
print(len(grc_ids))
id_first_pc = pc_ids[0]
pc_pos = pc.positions    #shape: 20097,3, ovverso contiene le posizione x,y,z di tutte le pc

grc_conn_ids=scaffold.get_connectivity_set("parallel_fiber_to_purkinje").from_identifiers   
pc_conn_ids = scaffold.get_connectivity_set("parallel_fiber_to_purkinje").to_identifiers   

distance_list = []
distance_x_list=[]
distance_y_list=[]
distance_z_list =[]

#per ogni connessione
for i in range(len(grc_conn_ids)):
    grc_pos = grc.positions[np.where(grc.identifiers == grc_conn_ids[i])]
    pc_pos = pc.positions[np.where (pc.identifiers == pc_conn_ids[i])]
    dif = pc_pos - grc_pos
    distance = ( sum( (dif)**2)  )**0.5
    print(i, '- GrC', grc_pos, 'pc', pc_pos, '-- distance:', distance)
    #print(dif[0,0])
    #print(dif[0,1])
    #print(dif[0,2])
    dif_x = abs(dif[0,0])
    dif_y = abs(dif[0,1])
    dif_z = abs(dif[0,2])
    #print( 'diff x y z:', dif_x, dif_y, dif_z)
    distance_list.append(distance)      #euclidean distance bw grc center and pc
    distance_x_list.append(dif_x)
    distance_y_list.append(dif_y)
    distance_z_list.append(dif_z)

#ma a cosa serve fare questo?
dist = []
for i in range(len(distance_list)):
    d = (sum ( (distance_list[i])**2 ))**0.5
    print ( i, d )
    dist.append( d )

mean_distance = np.mean(dist)
min_distance = np.min(dist)
max_distance = np.max(dist)
std_dist = np.std(dist)

mean_distance_x = np.mean(distance_x_list)
min_distance_x = np.min(distance_x_list)
max_distance_x = np.max(distance_x_list)
std_dist_x = np.std(distance_x_list)

mean_distance_y = np.mean(distance_y_list)
min_distance_y = np.min(distance_y_list)
max_distance_y = np.max(distance_y_list)
std_dist_y = np.std(distance_y_list)


mean_distance_z = np.mean(distance_z_list)
min_distance_z = np.min(distance_z_list)
max_distance_z = np.max(distance_z_list)
std_dist_z = np.std(distance_z_list)

std_dist = np.std(distance_list)

print('3D distance (euclidean) - mean:', mean_distance, '+-', std_dist, 'max:', max_distance, 'min: ',min_distance)
print('Distance x - mean:', mean_distance_x, '+-', std_dist_x,  'max:', max_distance_x, 'min : ',min_distance_x)
print('Distance y - mean:', mean_distance_y, '+-', std_dist_y,'max:', max_distance_y, 'min : ',min_distance_y)
print('Distance z - mean:', mean_distance_z, '+-', std_dist_z,'max:', max_distance_z, 'min : ',min_distance_z)


    

a = np.array(grc_conn_ids)
b = np.array(dist)
plt.scatter(a,b, s=2)   #s per modificare la dimensione del marker
plt.xlabel('GrC id')
plt.ylabel('GrC-PC 3D distance')
plt.title('3D distances - connection GrC-PC')
plt.show()


a_x = np.array(grc_conn_ids)
b_x = np.array(distance_x_list)
plt.scatter(a_x,b_x, s=2)
plt.xlabel('GrC id')
plt.ylabel('x distance |GrC-PC|')
plt.title('x distances  -  connection GrC-PC')
plt.show()

a_y = np.array(grc_conn_ids)
b_y = np.array(distance_y_list)
plt.scatter(a_y,b_y, s=2)
plt.xlabel('GrC id')
plt.ylabel('y distance |GrC-PF|')
plt.title('y distances  -  connection GrC-PC')
plt.show()


a_z = np.array(grc_conn_ids)
b_z = np.array(distance_z_list)
plt.scatter(a_z,b_z, s=2)
plt.xlabel('GrC id')
plt.ylabel('z distance |GrC-PC|')
plt.title('z distances  -  connection GrC-PC')
plt.show()