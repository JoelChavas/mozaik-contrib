# -*- coding: utf-8 -*-
"""
This is implementation of model of push-pull connectvity: 
Jens Kremkow: Correlating Excitation and Inhibition in Visual Cortical Circuits: Functional Consequences and Biological Feasibility. PhD Thesis, 2009.
"""
import sys
from pyNN import nest
from mozaik.controller import run_workflow, setup_logging
import mozaik
from model import PushPullCCModel
from experiments import create_experiments
from mozaik.storage.datastore import Hdf5DataStore,PickledDataStore
from analysis_and_visualization import perform_analysis_and_visualization
from parameters import ParameterSet


try:
    from mpi4py import MPI
except ImportError:
    MPI = None
if MPI:
    mpi_comm = MPI.COMM_WORLD
MPI_ROOT = 0

logger = mozaik.getMozaikLogger()

if True:
    data_store,model = run_workflow('FFI',PushPullCCModel,create_experiments)
    model.connectors['V1L4ExcL4ExcConnection'].store_connections(data_store)    
    model.connectors['V1L4ExcL4InhConnection'].store_connections(data_store)    
    model.connectors['V1L4InhL4ExcConnection'].store_connections(data_store)    
    model.connectors['V1L4InhL4InhConnection'].store_connections(data_store)    
    model.connectors['V1AffConnectionOn'].store_connections(data_store)    
    model.connectors['V1AffConnectionOff'].store_connections(data_store)    
    model.connectors['V1AffInhConnectionOn'].store_connections(data_store)    
    model.connectors['V1AffInhConnectionOff'].store_connections(data_store)    
    data_store.save()
    
else: 
    setup_logging()
    data_store = PickledDataStore(load=True,parameters=ParameterSet({'root_directory':'FFI_test_____', 'store_stimuli' : False}),replace=True)
    logger.info('Loaded data store')
    data_store.save()

if mpi_comm.rank == MPI_ROOT:
    perform_analysis_and_visualization(data_store)
