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
    if True:
        
        analog_ids = param_filter_query(data_store,sheet_name="V1_Exc_L4").get_segments()[0].get_stored_esyn_ids()
        analog_ids_inh = param_filter_query(data_store,sheet_name="V1_Inh_L4").get_segments()[0].get_stored_esyn_ids()

        #find neuron with preference closet to 0  
        NeuronAnnotationsToPerNeuronValues(data_store,ParameterSet({})).analyse()
        l4_exc_or = data_store.get_analysis_result(identifier='PerNeuronValue',value_name = 'LGNAfferentOrientation', sheet_name = 'V1_Exc_L4')
        l4_exc_phase = data_store.get_analysis_result(identifier='PerNeuronValue',value_name = 'LGNAfferentPhase', sheet_name = 'V1_Exc_L4')
        l4_exc = analog_ids[numpy.argmin([circular_dist(o,numpy.pi/2,numpy.pi)  for (o,p) in zip(l4_exc_or[0].get_value_by_id(analog_ids),l4_exc_phase[0].get_value_by_id(analog_ids))])]
        l4_inh_or = data_store.get_analysis_result(identifier='PerNeuronValue',value_name = 'LGNAfferentOrientation', sheet_name = 'V1_Inh_L4')
        l4_inh_phase = data_store.get_analysis_result(identifier='PerNeuronValue',value_name = 'LGNAfferentPhase', sheet_name = 'V1_Inh_L4')
        l4_inh = analog_ids_inh[numpy.argmin([circular_dist(o,numpy.pi/2,numpy.pi)  for (o,p) in zip(l4_inh_or[0].get_value_by_id(analog_ids_inh),l4_inh_phase[0].get_value_by_id(analog_ids_inh))])]
        l4_exc_or_many = numpy.array(l4_exc_or[0].ids)[numpy.nonzero(numpy.array([circular_dist(o,numpy.pi/2,numpy.pi)  for (o,p) in zip(l4_exc_or[0].values,l4_exc_phase[0].values)]) < 0.1)[0]]

        print "Prefered orientation of plotted exc neurons:"
        print 'index ' + str(l4_exc)
        print "Prefered phase of plotted exc neurons:"
        print l4_exc_phase[0].get_value_by_id(l4_exc)
        print "Prefered orientation of plotted inh neurons:"
        print l4_inh_phase[0].get_value_by_id(l4_inh)
        print 'index ' + str(l4_inh)
        print "Prefered phase of plotted inh neurons:"
        print l4_exc_phase[0].get_value_by_id(l4_exc)
    
    if True:
            #data_store.remove_ads_from_datastore()
            
            dsv = param_filter_query(data_store,sheet_name='V1_Exc_L4')
            ActionPotentialRemoval(dsv,ParameterSet({'window_length' : 10.0})).analyse()
            TrialAveragedFiringRate(param_filter_query(data_store,sheet_name=['V1_Exc_L4','V1_Inh_L4'],st_name="FullfieldDriftingSinusoidalGrating"),ParameterSet({})).analyse()
                    
            dsv = param_filter_query(data_store,st_name='FullfieldDriftingSinusoidalGrating',analysis_algorithm='TrialAveragedFiringRate',sheet_name=['V1_Exc_L4','V1_Inh_L4'])    
            GaussianTuningCurveFit(dsv,ParameterSet({'parameter_name' : 'orientation'})).analyse()
            dsv = param_filter_query(data_store,st_name='FullfieldDriftingSinusoidalGrating',sheet_name=['V1_Exc_L4','V1_Inh_L4'])   
            Analog_F0andF1(dsv,ParameterSet({})).analyse()
            data_store.save()
        
            #Analog_MeanSTDAndFanoFactor(data_store,ParameterSet({})).analyse()
            #data_store.save()
            PSTH(param_filter_query(data_store,sheet_name='V1_Exc_L4'),ParameterSet({'bin_length' : 2.0 })).analyse()
            
            
            GSTA(param_filter_query(data_store,sheet_name='V1_Exc_L4',st_name='InternalStimulus',direct_stimulation_name='None'),ParameterSet({'neurons' : [l4_exc], 'length' : 250.0 }),tags=['GSTA']).analyse()
            GSTA(param_filter_query(data_store,sheet_name='V1_Exc_L4',st_name='FullfieldDriftingSinusoidalGrating',st_orientation=[0,numpy.pi/2]),ParameterSet({'neurons' : [l4_exc], 'length' : 250.0 }),tags=['GSTA']).analyse()
            GSTA(param_filter_query(data_store,sheet_name='V1_Inh_L4',st_name='FullfieldDriftingSinusoidalGrating',st_orientation=[0,numpy.pi/2]),ParameterSet({'neurons' : [l4_inh], 'length' : 250.0 }),tags=['GSTA']).analyse()            
            GSTA(param_filter_query(data_store,sheet_name='V1_Exc_L4',st_name='NaturalImageWithEyeMovement'),ParameterSet({'neurons' : [l4_exc], 'length' : 250.0 }),tags=['GSTA']).analyse()
            
            #data_store.print_content(full_ADS=True)
            
            #Precision(param_filter_query(data_store,sheet_name='V1_Exc_L4'),ParameterSet({'neurons' : [l4_exc], 'bin_length' : 10.0 })).analyse()

            dsv = param_filter_query(data_store,st_name='NaturalImageWithEyeMovement',sheet_name='V1_Exc_L4',analysis_algorithm='ActionPotentialRemoval')
            TrialVariability(dsv,ParameterSet({'vm': False,  'cond_exc': False, 'cond_inh': False})).analyse()
            dsv = param_filter_query(data_store,st_name='FullfieldDriftingSinusoidalGrating',sheet_name='V1_Exc_L4',st_contrast=100,analysis_algorithm='ActionPotentialRemoval')            
            TrialVariability(dsv,ParameterSet({'vm': False,  'cond_exc': False, 'cond_inh': False})).analyse()

            
            dsv = param_filter_query(data_store,st_name='FullfieldDriftingSinusoidalGrating',analysis_algorithm='TrialAveragedFiringRate',sheet_name=['V1_Exc_L4','V1_Inh_L4'])  
            PeriodicTuningCurvePreferenceAndSelectivity_VectorAverage(dsv,ParameterSet({'parameter_name' : 'orientation'})).analyse()
        
            #pnv = param_filter_query(data_store,st_name='InternalStimulus',sheet_name='V1_Exc_L4',analysis_algorithm=['Analog_MeanSTDAndFanoFactor'],value_name='Mean(ECond)',st_direct_stimulation_name='None').get_analysis_result()
            #dsv = param_filter_query(data_store,st_name='FullfieldDriftingSinusoidalGrating',sheet_name='V1_Exc_L4',analysis_algorithm=['Analog_F0andF1'],value_name='F0_Exc_Cond')
            #SubtractPNVfromPNVS(pnv,dsv,ParameterSet({})).analyse()

            #pnv = param_filter_query(data_store,st_name='InternalStimulus',sheet_name='V1_Exc_L4',analysis_algorithm=['Analog_MeanSTDAndFanoFactor'],value_name='Mean(ICond)',st_direct_stimulation_name='None').get_analysis_result()
            #dsv = param_filter_query(data_store,st_name='FullfieldDriftingSinusoidalGrating',sheet_name='V1_Exc_L4',analysis_algorithm=['Analog_F0andF1'],value_name='F0_Inh_Cond')
            #SubtractPNVfromPNVS(pnv,dsv,ParameterSet({})).analyse()

            #pnv = param_filter_query(data_store,st_name='InternalStimulus',sheet_name='V1_Exc_L4',analysis_algorithm=['Analog_MeanSTDAndFanoFactor'],value_name='Mean(VM)',st_direct_stimulation_name='None').get_analysis_result()
            #dsv = param_filter_query(data_store,st_name='FullfieldDriftingSinusoidalGrating',sheet_name='V1_Exc_L4',analysis_algorithm=['Analog_F0andF1'],value_name='F0_Vm')
            #SubtractPNVfromPNVS(pnv,dsv,ParameterSet({})).analyse()

            TrialToTrialCrossCorrelationOfAnalogSignalList(param_filter_query(data_store,sheet_name='V1_Exc_L4',st_name="NaturalImageWithEyeMovement",analysis_algorithm='ActionPotentialRemoval'),ParameterSet({'neurons' : list(analog_ids)})).analyse()
            TrialToTrialCrossCorrelationOfAnalogSignalList(param_filter_query(data_store,sheet_name='V1_Exc_L4',st_name="NaturalImageWithEyeMovement",analysis_algorithm='PSTH'),ParameterSet({'neurons' : list(analog_ids)})).analyse()

            data_store.save()
    
    dsv = param_filter_query(data_store,analysis_algorithm='TrialToTrialCrossCorrelationOfAnalogSignalList')                
    dsv.print_content(full_ADS=True)

    if True: # PLOTTING
        #TrialCrossCorrelationAnalysis(data_store,ParameterSet({'neurons' : list(analog_ids), 'window_length' : 10.0}),fig_param={"dpi" : 100,"figsize": (25,12)},plot_file_name="trial-to-trial-cross-correlation.png").plot()
        #SNRAnalysis(data_store,ParameterSet({"neuron" : analog_ids[0]}),fig_param={'dpi' : 100,'figsize': (25,12)},plot_file_name='SNR1.png').plot()                        
        #SNRAnalysis(data_store,ParameterSet({"neuron" : analog_ids[1]}),fig_param={'dpi' : 100,'figsize': (25,12)},plot_file_name='SNR2.png').plot()                        
        #SNRAnalysis(data_store,ParameterSet({"neuron" : analog_ids[2]}),fig_param={'dpi' : 100,'figsize': (25,12)},plot_file_name='SNR3.png').plot()                        

        #dsv = param_filter_query(data_store,st_name=['InternalStimulus'])        
        #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[0], 'sheet_activity' : {}, 'spontaneous': False, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (28,12)},plot_file_name='SSExcAnalog.png').plot()
        #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Inh_L4', 'neuron' : analog_ids_inh[0], 'sheet_activity' : {}, 'spontaneous': False, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (28,12)},plot_file_name='SSInhAnalog.png').plot()    

        if True:
            
            dsv = param_filter_query(data_store,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=100)    
            OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : l4_exc, 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="Exc2.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[0], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="Exc3.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[1], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="Exc4.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[2], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="Exc5.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[3], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="Exc6.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[4], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="Exc7.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[5], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="Exc8.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[6], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="Exc9.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[7], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="Exc10.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})

            RasterPlot(dsv,
                        ParameterSet({
                            'sheet_name' : 'X_ON', 
                            'neurons' : sorted(param_filter_query(data_store,sheet_name="X_ON").get_segments()[0].get_stored_spike_train_ids())[0:10], 
                            'trial_averaged_histogram': False, 
                            'spontaneous': False
                                }),
                        fig_param={'dpi' : 100,'figsize': (14,12)},
                        plot_file_name="LGNOn_grating.png").plot()
                        
            #RasterPlot(dsv,
                        #ParameterSet({
                            #'sheet_name' : 'V1_Exc_L4', 
                            #'neurons' : sorted(param_filter_query(data_store,sheet_name="V1_Exc_L4").get_segments()[0].get_stored_spike_train_ids())[0:10], 
                            #'trial_averaged_histogram': False, 
                            #'spontaneous': False
                                #}),
                        #fig_param={'dpi' : 100,'figsize': (14,12)},
                        #plot_file_name="V1_Exc_grating.png").plot()
                        
            #ActivityMovie(dsv,
                          #ParameterSet({
                              #'bin_width' : 10,
                              #'scatter': True,
                              #'resolution': 1,
                              #'sheet_name': 'X_ON'
                                  #}), 
                          #fig_param={'dpi' : 50,'figsize': (28,12)},
                          #plot_file_name="LGNOn_movie").plot()
            
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Inh_L4', 'neuron' : l4_inh, 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (14,12)},plot_file_name="Inh.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'X_ON', 'neuron' : sorted(param_filter_query(data_store,sheet_name="X_ON").get_segments()[0].get_stored_esyn_ids())[0], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (14,12)},plot_file_name="LGN0On.png").plot()
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'X_OFF', 'neuron' : sorted(param_filter_query(data_store,sheet_name="X_OFF").get_segments()[0].get_stored_esyn_ids())[0], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (14,12)},plot_file_name="LGN0Off.png").plot()
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'X_ON', 'neuron' : sorted(param_filter_query(data_store,sheet_name="X_ON").get_segments()[0].get_stored_esyn_ids())[1], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (14,12)},plot_file_name="LGN1On.png").plot()
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'X_OFF', 'neuron' : sorted(param_filter_query(data_store,sheet_name="X_OFF").get_segments()[0].get_stored_esyn_ids())[1], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (14,12)},plot_file_name="LGN1Off.png").plot()
            
            #TrialAveragedFiringRate(param_filter_query(data_store,sheet_name=['X_ON'],st_name="DriftingSinusoidalGratingDisk"),ParameterSet({})).analyse()
            
            ##dsv = param_filter_query(data_store,st_name='DriftingSinusoidalGratingDisk',analysis_algorithm=['TrialAveragedFiringRate'])    
            #PlotTuningCurve(dsv,ParameterSet({'parameter_name' : 'spatial_frequency', 'neurons': list(sorted(param_filter_query(data_store,sheet_name="X_ON").get_segments()[0].get_stored_esyn_ids())), 'sheet_name' : 'X_ON','centered'  : False,'mean' : False})).plot({'TuningCurve F0_Inh_Cond.y_lim' : (0,180) , 'TuningCurve F0_Exc_Cond.y_lim' : (0,80)})

            
            #import pylab
            #pylab.show()
        
        if False:
            dsv = param_filter_query(data_store,st_name='NaturalImageWithEyeMovement')            
            OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : l4_exc, 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="NatExc2.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[0], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="NatExc3.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[1], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="NatExc4.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[2], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="NatExc5.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[3], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="NatExc6.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[4], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="NatExc7.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[5], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="NatExc8.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[6], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="NatExc9.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[7], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="NatExc10.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            
            #OverviewPlot(dsv,ParameterSet({'sheet_name' : 'X_ON', 'neuron' : sorted(param_filter_query(data_store,sheet_name="X_ON").get_segments()[0].get_stored_esyn_ids())[0], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (14,12)},plot_file_name="LGN0On.png").plot()
            #import pylab
            #pylab.show()
        
        if False:
            dsv = param_filter_query(data_store,st_name='DriftingSineGratingWithEyeMovement')    
            OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : l4_exc, 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="DGExc2.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[0], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="DGExc3.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[1], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="DGExc4.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[2], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="DGExc5.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[3], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="DGExc6.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[4], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="DGExc7.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[5], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="DGExc8.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[6], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="DGExc9.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})
            OverviewPlot(dsv,ParameterSet({'sheet_name' : 'V1_Exc_L4', 'neuron' : analog_ids[7], 'sheet_activity' : {}, 'spontaneous': False}),fig_param={'dpi' : 100,'figsize': (19,12)},plot_file_name="DGExc10.png").plot({'Vm_plot.y_lim' : (-67,-56),'Conductance_plot.y_lim' : (0,35.0)})

        # tuninc curves
        dsv = param_filter_query(data_store,st_name='FullfieldDriftingSinusoidalGrating',analysis_algorithm=['TrialAveragedFiringRate','Analog_F0andF1'])    
        PlotTuningCurve(dsv,ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids), 'sheet_name' : 'V1_Exc_L4','centered'  : True,'mean' : False,'polar' : False, 'pool' : False}),fig_param={'dpi' : 100,'figsize': (25,12)},plot_file_name="TCExc.png").plot({'TuningCurve F0_Exc_Cond.y_lim' : (0,180) , 'TuningCurve F0_Exc_Cond.y_lim' : (0,80)})
        PlotTuningCurve(dsv,ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids_inh), 'sheet_name' : 'V1_Inh_L4','centered'  : True,'mean' : False,'polar' : False, 'pool' : False}),fig_param={'dpi' : 100,'figsize': (25,12)},plot_file_name="TCInh.png").plot({'TuningCurve F0_Inh_Cond.y_lim' : (0,180) , 'TuningCurve F0_Exc_Cond.y_lim' : (0,80)})
        
        #dsv = param_filter_query(data_store,st_name='FullfieldDriftingSinusoidalGrating',analysis_algorithm=['Analog_MeanSTDAndFanoFactor'])    
        #PlotTuningCurve(dsv,ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids), 'sheet_name' : 'V1_Exc_L4','centered'  : True,'mean' : False,'polar' : False, 'pool' : False}),fig_param={'dpi' : 100,'figsize': (25,12)},plot_file_name="TCExcA.png").plot()
        #PlotTuningCurve(dsv,ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids_inh), 'sheet_name' : 'V1_Inh_L4','centered'  : True,'mean' : False,'polar' : False, 'pool' : False}),fig_param={'dpi' : 100,'figsize': (25,12)},plot_file_name="TCInhA.png").plot()

        
        #dsv = param_filter_query(data_store,st_name='FullfieldDriftingSinusoidalGrating',analysis_algorithm=['TrialVariability'])    
        #PlotTuningCurve(dsv,ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids), 'sheet_name' : 'V1_Exc_L4', 'centered'  : True,'mean' : False,'polar' : False, 'pool' : False})).plot()
        
        #dsv = param_filter_query(data_store,st_name='FullfieldDriftingSinusoidalGrating',analysis_algorithm=['TrialVariability'])    
        #PlotTuningCurve(dsv,ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids_inh), 'sheet_name' : 'V1_Inh_L4', 'centered'  : True,'mean' : False,'polar' : False, 'pool' : False})).plot()
        
        import pylab
        pylab.show()






