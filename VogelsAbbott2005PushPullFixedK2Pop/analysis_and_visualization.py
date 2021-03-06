import numpy
import mozaik
from mozaik.visualization.plotting import *
from mozaik.analysis.technical import NeuronAnnotationsToPerNeuronValues
from mozaik.analysis.analysis import *
from mozaik.storage.queries import *
from mozaik.storage.datastore import PickledDataStore


def perform_analysis_and_visualization(data_store):
    analog_ids = param_filter_query(data_store,sheet_name="V1_Exc_L4").get_segments()[0].get_stored_esyn_ids()
    analog_ids_inh = param_filter_query(data_store,sheet_name="V1_Inh_L4").get_segments()[0].get_stored_esyn_ids()
    spike_ids = param_filter_query(data_store,sheet_name="V1_Exc_L4").get_segments()[0].get_stored_spike_train_ids()
    spike_ids_inh = param_filter_query(data_store,sheet_name="V1_Inh_L4").get_segments()[0].get_stored_spike_train_ids()
    
    if True: # PLOTTING
            activity_plot_param =    {
                   'frame_rate' : 5,  
                   'bin_width' : 5.0, 
                   'scatter' :  True,
                   'resolution' : 0
            }       
            
            
            PSTH(param_filter_query(data_store,st_direct_stimulation_name="None",st_name=['InternalStimulus']),ParameterSet({'bin_length' : 5.0})).analyse()
            TrialAveragedFiringRate(param_filter_query(data_store,st_direct_stimulation_name="None",st_name=['InternalStimulus']),ParameterSet({})).analyse()
            Irregularity(param_filter_query(data_store,st_direct_stimulation_name="None",st_name=['InternalStimulus']),ParameterSet({})).analyse()
            NeuronToNeuronAnalogSignalCorrelations(param_filter_query(data_store,analysis_algorithm='PSTH'),ParameterSet({'convert_nan_to_zero' : True})).analyse()
            PopulationMean(data_store,ParameterSet({})).analyse()
            
            data_store.print_content(full_ADS=True)
            
            OverviewPlot(data_store,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[0], 'sheet_activity' : {}}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name='ExcAnalog.png').plot({'Vm_plot.y_lim' : (-80,-50),'Conductance_plot.y_lim' : (0,500.0)})
            OverviewPlot(data_store,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[1], 'sheet_activity' : {}}),fig_param={'dpi' : 100,'figsize': (19,12)}).plot({'Vm_plot.y_lim' : (-80,-50),'Conductance_plot.y_lim' : (0,500.0)})    
            OverviewPlot(data_store,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[2], 'sheet_activity' : {}}),fig_param={'dpi' : 100,'figsize': (19,12)}).plot({'Vm_plot.y_lim' : (-80,-50),'Conductance_plot.y_lim' : (0,500.0)})
            
            
            OverviewPlot(data_store,ParameterSet({'sheet_name' : 'V1_Inh_L4', 'neuron' : analog_ids_inh[0], 'sheet_activity' : {}}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name='InhAnalog.png').plot({'Vm_plot.y_lim' : (-80,-50),'Conductance_plot.y_lim' : (0,500.0)})
            OverviewPlot(data_store,ParameterSet({'sheet_name' : 'V1_Inh_L4', 'neuron' : analog_ids_inh[1], 'sheet_activity' : {}}),fig_param={'dpi' : 100,'figsize': (19,12)}).plot({'Vm_plot.y_lim' : (-80,-50),'Conductance_plot.y_lim' : (0,500.0)})
            OverviewPlot(data_store,ParameterSet({'sheet_name' : 'V1_Inh_L4', 'neuron' : analog_ids_inh[2], 'sheet_activity' : {}}),fig_param={'dpi' : 100,'figsize': (19,12)}).plot({'Vm_plot.y_lim' : (-80,-50),'Conductance_plot.y_lim' : (0,500.0)},)
            
            RasterPlot(data_store,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neurons' : spike_ids,'trial_averaged_histogram': False}),fig_param={'dpi' : 100,'figsize': (17,5)},plot_file_name='ExcRaster.png').plot({'SpikeRasterPlot.group_trials':True})
            RasterPlot(data_store,ParameterSet({'sheet_name' : 'V1_Inh_L4', 'neurons' : spike_ids_inh,'trial_averaged_histogram': False}),fig_param={'dpi' : 100,'figsize': (17,5)},plot_file_name='InhRaster.png').plot({'SpikeRasterPlot.group_trials':True})
            
            import pylab
            pylab.show()
            
            
    
