import numpy
import mozaik
import pylab
from mozaik.visualization.plotting import *
from mozaik.analysis.technical import NeuronAnnotationsToPerNeuronValues
from mozaik.analysis.analysis import *
from mozaik.analysis.vision import *
from mozaik.storage.queries import *
from mozaik.storage.datastore import PickledDataStore
from mozaik.tools.circ_stat import circular_dist
import sys, os
sys.path.append(os.environ['HOME'] + '/mozaik-contrib')
from Kremkow_plots import *

def perform_analysis_and_visualization(data_store):

    if True: # PLOTTING

        if True:
            dsv = param_filter_query(data_store,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=100)    
            RasterPlot(dsv,
                        ParameterSet({
                            'sheet_name' : 'X_ON', 
                            'neurons' : sorted(param_filter_query(data_store,sheet_name="X_ON").get_segments()[0].get_stored_spike_train_ids())[0:9], 
                            'trial_averaged_histogram': False, 
                            'spontaneous': False
                                }),
                        fig_param={'dpi' : 100,'figsize': (14,12)},
                        plot_file_name="LGNOn_grating.png").plot()
            ActivityMovie(dsv,
                          ParameterSet({
                              'bin_width' : 50,
                              'scatter': True,
                              'resolution': 20,
                              'sheet_name': 'X_ON'
                                  }), 
                          fig_param={'dpi' : 50,'figsize': (28,12)},
                          plot_file_name="LGNOn_movie").plot()
            #RasterPlot(dsv,
                        #ParameterSet({
                            #'sheet_name' : 'X_OFF', 
                            #'neurons' : sorted(param_filter_query(data_store,sheet_name="X_OFF").get_segments()[0].get_stored_spike_train_ids())[0:9], 
                            #'trial_averaged_histogram': False, 
                            #'spontaneous': False
                                #}),
                        #fig_param={'dpi' : 100,'figsize': (14,12)},
                        #plot_file_name="LGNOff_grating.png").plot()
        #if True:
            #dsv = param_filter_query(data_store,st_name='NaturalImageWithEyeMovement')            
            #RasterPlot(dsv,
                       #ParameterSet({
                           #'sheet_name' : 'X_ON', 
                           #'neurons' : sorted(param_filter_query(data_store,sheet_name="X_ON").get_segments()[0].get_stored_spike_train_ids()), 
                           #'trial_averaged_histogram': False, 
                           #'spontaneous': False
                               #}),
                       #fig_param={'dpi' : 100,'figsize': (14,12)},
                       #plot_file_name="LGNOn_natural.png").plot()
            
        
        import pylab
        pylab.show()






