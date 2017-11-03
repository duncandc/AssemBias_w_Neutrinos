"""
process ROCKSTAR halo catalogues from Bolshoi
"""

#load packages
from __future__ import print_function, division

import numpy as np
import re
import sys
import os

from halotools import sim_manager

base_save_dir = './' #location the processed catalogs will be stored

from hlist_header_reader import read_header

def main():
    
    #set ascii file to process
    filepath = './'
    if len(sys.argv)>1:
        filename = sys.argv[1]
    else:
        filename = 'out_66_massless.list'
    
    #unzip the file if it needs to be
    if filename[-3:] == '.gz':
        was_zipped = True
        os.system("gunzip -f " + filepath + filename)
        filename = filename[:-3]
    else:
        was_zipped = False

    cols, d = read_header(filename)
    
    #set some properties
    simname = 'MassiveNuS'
    version = filename.split('.')[0]
    Lbox = 512.0
    particle_mass = np.float(d['Particle mass'])
    halo_finder='Rockstar'
    
    #set the location and filename of the reduced catalogue
    savepath = base_save_dir
    savename = simname+ '_' + version + '.hdf5'
    
    #extract the scale factor of the snapshot from the filename
    scale_factor = float(re.findall(r"[-+]?\d*\.\d+|\d+",filename)[0])
    redshift = 1.0/scale_factor -1.0
    
    columns_to_keep_dict = {'halo_id':              (0, 'i8'),
                            'halo_descid':          (1, 'i8'),
                            'halo_mvir':            (2, 'f4'),
                            'halo_vmax':            (3, 'f4'),
                            'halo_vrms':            (4, 'f4'),
                            'halo_rvir':            (5, 'f4'),
                            'halo_rs':              (6, 'f4'),
                            'halo_np':              (7, 'f4'),
                            'halo_x':               (8, 'f4'),
                            'halo_y':               (9, 'f4'),
                            'halo_z':               (10, 'f4'),
                            'halo_vx':              (11, 'f4'),
                            'halo_vy':              (12, 'f4'),
                            'halo_vz':              (13, 'f4'),
                            'halo_jx':              (14, 'f4'),
                            'halo_jy':              (15, 'f4'),
                            'halo_jz':              (16, 'f4'),
                            'halo_spin':            (17, 'f4'),
                            'halo_rs_klypin':       (18, 'f4'),
                            'halo_mvir_all':        (19, 'f4'),
                            'halo_m200b':           (20, 'f4'),
                            'halo_m200c':           (21, 'f4'),
                            'halo_m500c':           (22, 'f4'),
                            'halo_m2500c':          (23, 'f4'),
                            'halo_xoff':            (24, 'f4'),
                            'halo_voff':            (25, 'f4'),
                            'halo_spin_bullock':    (26, 'f4'),
                            'halo_b_to_a':          (27, 'f4'),
                            'halo_c_to_a':          (28, 'f4'),
                            'halo_ax':              (29, 'f4'),
                            'halo_ay':              (30, 'f4'),
                            'halo_az':              (31, 'f4'),
                            'halo_b_to_a_500c':     (32, 'f4'),
                            'halo_c_to_a_500c':     (33, 'f4'),
                            'halo_ax_500c':         (34, 'f4'),
                            'halo_ay_500c':         (35, 'f4'),
                            'halo_az_500c':         (36, 'f4'),
                            'halo_T/|U|':           (37, 'f4'),
                            'halo_m_pe_Behroozi':   (38, 'f4'),
                            'halo_m_pe_diemer':     (39, 'f4'),
                            'halo_halfmass_radius': (40, 'f4')
                            }
    
    columns_to_convert_from_kpc_to_mpc = ['halo_rvir','halo_rs','halo_halfmass_radius']
    
    #apply cuts to catalogue
    #row_cut_min_dict = {'halo_mpeak': particle_mass*100}
    #processing_notes = ("all halos with halo_mpeak < 50 times the particle mass were \n"
    #                    "thrown out during the initial catalogue reduction.")
    processing_notes = ("no cuts were made.")

    #read in catalogue and save results
    reader = sim_manager.RockstarHlistReader(filepath+filename, columns_to_keep_dict,\
        savepath+savename, simname, halo_finder, redshift, version, Lbox, particle_mass,\
        processing_notes=processing_notes,\
        overwrite=True) 
    
    reader.read_halocat(columns_to_convert_from_kpc_to_mpc, write_to_disk = True, update_cache_log = True)
    
    if was_zipped:
        os.system("gzip " + filepath + filename)


if __name__ == '__main__':
    main()