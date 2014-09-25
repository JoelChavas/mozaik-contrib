# -*- coding: iso-8859-15 -*-
"""
docstring goes here
"""
import quantities as qt
import numpy
import numpy.random
import mozaik.storage.queries as queries
from mozaik.visualization.plotting import (Plotting, GSynPlot,RasterPlot,PerNeuronAnalogSignalScatterPlot,
                                           VmPlot, ConductanceSignalListPlot,
                                           AnalogSignalListPlot,OverviewPlot,PerNeuronValueScatterPlot,PlotTuningCurve,PerNeuronValuePlot)
                                           
from mozaik.analysis.analysis import TrialToTrialCrossCorrelationOfAnalogSignalList                                    
from parameters import ParameterSet
import matplotlib.gridspec as gridspec
from mozaik.visualization.simple_plot import SpikeRasterPlot, SpikeHistogramPlot
from mozaik.tools.mozaik_parametrized import MozaikParametrized
from mozaik.tools.circ_stat import circular_dist
from mozaik.visualization.simple_plot import StandardStyle
import pylab
from mozaik.controller import Global

class KremkowOverviewFigure(Plotting):
    required_parameters = ParameterSet({
        'sheet_name': str,  # the name of the sheet for which to plot
        'neuron': int,  # which neuron to show
    })

    def subplot(self, subplotspec):
        plots = {}
        gs = gridspec.GridSpecFromSubplotSpec(12, 18, subplot_spec=subplotspec,
                                              hspace=1.0, wspace=1.0)
        
        assert queries.equal_stimulus(self.datastore,['trial'])        
        
        lgn_on_dsv = queries.param_filter_query(self.datastore, sheet_name='X_ON')
        lgn_off_dsv = queries.param_filter_query(self.datastore, sheet_name='X_OFF')
        lgn_spikes_a = [[s.spiketrains[0:2] for s in lgn_on_dsv.get_segments()],
                      [s.spiketrains[0:2] for s in lgn_off_dsv.get_segments()]]
        lgn_spikes_b = [[s.spiketrains[2:4] for s in lgn_on_dsv.get_segments()],
                      [s.spiketrains[2:4] for s in lgn_off_dsv.get_segments()]]
        
        plots['LGN_SRP1'] = (SpikeRasterPlot(lgn_spikes_a),gs[1:4, 0:5],{'x_axis' : False, 'x_label': None,'colors':['#FACC2E', '#0080FF']})
        plots['LGN_SHP1'] = (SpikeHistogramPlot(lgn_spikes_a),gs[4:5, 0:5],{'x_axis' : False, 'x_label': None,'colors':['#FACC2E', '#0080FF']})
        plots['LGN_SRP2'] = (SpikeRasterPlot(lgn_spikes_b),gs[7:10, 0:5],{'x_axis' : False, 'x_label': None,'colors':['#FACC2E', '#0080FF']})
        plots['LGN_SHP2'] = (SpikeHistogramPlot(lgn_spikes_b),gs[10:11, 0:5],{'colors':['#FACC2E', '#0080FF']})
                     
        dsv1 = queries.param_filter_query(self.datastore,sheet_name=self.parameters.sheet_name)
        #print self.parameters.neuron
        #sp = [[[s.get_spiketrain(self.parameters.neuron)] for s in dsv1.get_segments()]]
        
        plots['V1_SRP1'] = (RasterPlot(dsv1,ParameterSet({'sheet_name' : self.parameters.sheet_name, 'spontaneous' : True,'neurons' : [self.parameters.neuron],'trial_averaged_histogram': False})),gs[:3, 6:14],{'x_axis' : False, 'x_label': None})
        plots['V1_SHP1'] = (RasterPlot(dsv1,ParameterSet({'sheet_name' :self.parameters.sheet_name, 'spontaneous' : True,'neurons' : [self.parameters.neuron],'trial_averaged_histogram': False})),gs[:3, 6:14],{'x_axis' : False, 'x_label': None})

        p = {}
        p['title']=None
        p['x_axis']=None
        p['x_label']=None
        plots['Vm_Plot'] = (VmPlot(dsv1, ParameterSet({'sheet_name': self.parameters.sheet_name,'neuron': self.parameters.neuron, 'spontaneous' : True})),gs[4:8, 6:14],p)                                  
        p = {}
        p['title']=None
        plots['Gsyn_Plot'] = (GSynPlot(dsv1, ParameterSet({'sheet_name': self.parameters.sheet_name,'neuron': self.parameters.neuron,'spontaneous' : True})),gs[8:12, 6:14],p)                                  
        plots['GSTA_Plot'] = (ConductanceSignalListPlot(queries.TagBasedQuery(ParameterSet({'tags': ['GSTA']})).query(dsv1),ParameterSet({'normalize_individually': True, 'neurons' : [self.parameters.neuron]})),gs[7:10, 15:],{})                                  
        
        #p = {}
        #p['mean'] = False
        #AnalogSignalListPlot(dsv, ParameterSet({'sheet_name': self.parameters.sheet_name,
        #                                        'ylabel': 'AC (norm)'})).subplot(gs[2:5, 15:], p)

        return plots

class StimulusResponseComparison(Plotting):
    required_parameters = ParameterSet({
        'sheet_name': str,  # the name of the sheet for which to plot
        'neuron': int,  # which neuron to show
    })

    def subplot(self, subplotspec):
        plots = {}
        gs = gridspec.GridSpecFromSubplotSpec(6, 18, subplot_spec=subplotspec,
                                              hspace=1.0, wspace=1.0)
        
        orr = list(set([MozaikParametrized.idd(s).orientation for s in queries.param_filter_query(self.datastore,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=100).get_stimuli()]))                
        l4_exc_or = self.datastore.get_analysis_result(identifier='PerNeuronValue',value_name = 'LGNAfferentOrientation', sheet_name = 'V1_Exc_L4')
        
        dsv = queries.param_filter_query(self.datastore,st_name='FullfieldDriftingSinusoidalGrating',st_orientation=orr[numpy.argmin([circular_dist(o,l4_exc_or[0].get_value_by_id(self.parameters.neuron),numpy.pi)  for o in orr])],st_contrast=100)             
        plots['Gratings'] = (OverviewPlot(dsv, ParameterSet({'sheet_name': self.parameters.sheet_name,'neuron': self.parameters.neuron,'spontaneous' : True, 'sheet_activity' : {}})),gs[0:2,:],{'x_label': None})
        dsv = queries.param_filter_query(self.datastore,st_name='DriftingGratingWithEyeMovement')            
        plots['GratingsWithEM'] = (OverviewPlot(dsv, ParameterSet({'sheet_name': self.parameters.sheet_name,'neuron': self.parameters.neuron, 'spontaneous' : True,'sheet_activity' : {}})),gs[2:4,:],{})
        dsv = queries.param_filter_query(self.datastore,st_name='NaturalImageWithEyeMovement')            
        plots['NIwEM'] = (OverviewPlot(dsv, ParameterSet({'sheet_name': self.parameters.sheet_name,'neuron': self.parameters.neuron,'spontaneous' : True, 'sheet_activity' : {}})),gs[4:6,:],{'x_label': None})
        
        
        return plots
        

class OrientationTuningSummary(Plotting):
    required_parameters = ParameterSet({})

    def subplot(self, subplotspec):
        plots = {}
        gs = gridspec.GridSpecFromSubplotSpec(20, 15, subplot_spec=subplotspec,
                                              hspace=1.0, wspace=1.0)
        
        
        analog_ids = sorted(numpy.random.permutation(queries.param_filter_query(self.datastore,sheet_name="V1_Exc_L4").get_segments()[0].get_stored_esyn_ids()))
        analog_ids_inh = sorted(numpy.random.permutation(queries.param_filter_query(self.datastore,sheet_name="V1_Inh_L4").get_segments()[0].get_stored_esyn_ids()))
        
        dsv1 = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['LGNAfferentOrientation'],sheet_name='V1_Exc_L4')
        dsv2 = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['orientation preference of Firing rate'],sheet_name='V1_Exc_L4',st_contrast=100,analysis_algorithm='GaussianTuningCurveFit')
        plots['Or_corr_exc'] = (PerNeuronValueScatterPlot(dsv1+dsv2, ParameterSet({})),gs[0:4,3:5],{'x_label' : 'OR measured','y_label' : 'OR set','x_lim': (0.0,numpy.pi),'y_lim' : (0.0,numpy.pi), 'cmp' : None})
        dsv1 = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['LGNAfferentOrientation'],sheet_name='V1_Inh_L4')
        dsv2 = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['orientation preference of Firing rate'],sheet_name='V1_Inh_L4',st_contrast=100,analysis_algorithm='GaussianTuningCurveFit')
        plots['Or_corr_ing'] = (PerNeuronValueScatterPlot(dsv1+dsv2, ParameterSet({})),gs[0:4,5:7],{'x_label' : 'OR measured','y_label' : None,'x_lim': (0.0,numpy.pi),'y_lim' : (0.0,numpy.pi), 'cmp' : None})
        
        
                
        dsv = queries.param_filter_query(self.datastore,value_name=['orientation HWHH of Firing rate'],sheet_name=['V1_Exc_L4','V1_Inh_L4'])    
        plots['HWHH'] = (PerNeuronValueScatterPlot(dsv, ParameterSet({})),gs[0:4,8:12],{'x_lim': (0,50),'y_lim' : (0,50),'identity_line' : True, 'x_label' : 'HWHH Cont. 100%','y_label' : 'HWHH Cont. 50%', 'cmp' : None})

        dsv = queries.param_filter_query(self.datastore,st_name='FullfieldDriftingSinusoidalGrating',analysis_algorithm=['TrialAveragedFiringRate'])
        plots['ExcORTCMean'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids), 'sheet_name' : 'V1_Exc_L4','centered'  : True,'mean' : True,'pool' : False,'polar' : False})),gs[6:10,:3],{'title' : None,'x_label' : None , 'y_label' : 'EXC\nfiring rate (sp/s)','colors' : ['#FFAB00','#000000']})
        plots['ExcORTC1'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids[0:7]), 'sheet_name' : 'V1_Exc_L4','centered'  : True,'mean' : False,'pool' : False,'polar' : False})),gs[6:8,3:],{'title' : None,'x_label' : None,'y_axis' : False,'x_axis' : False, 'x_ticks' : False,'colors' : ['#FFAB00','#000000']})
        plots['ExcORTC2'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids[7:14]), 'sheet_name' : 'V1_Exc_L4','centered'  : True,'mean' : False,'pool' : False,'polar': False})),gs[8:10,3:],{'title' : None,'x_label' : None,'y_axis' : False,'x_axis' : False,'colors' : ['#FFAB00','#000000']})

        plots['InhORTCMean'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids_inh), 'sheet_name' : 'V1_Inh_L4','centered'  : True,'mean' : True,'pool' : False,'polar' : False})),gs[11:15,:3],{'title' : None, 'y_label' : 'INH\nfiring rate (sp/s)','colors' : ['#FFAB00','#000000']})
        plots['InhORTC1'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids_inh[0:7]), 'sheet_name' : 'V1_Inh_L4','centered'  : True,'mean' : False,'pool' : False,'polar' : False})),gs[11:13,3:],{'title' : None,'x_label' : None,'y_axis' : False,'x_axis' : False,'colors' : ['#FFAB00','#000000']})
        #plots['InhORTC2'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids_inh[7:14]), 'sheet_name' : 'V1_Inh_L4','centered'  : True,'mean' : False,'pool' : False,'polar' : False})),gs[13:15,3:],{'title' : None,'y_axis' : None,'colors' : ['#FFAB00','#000000']})

        
        dsv = queries.param_filter_query(self.datastore,value_name=['orientation HWHH of Firing rate'],sheet_name=['V1_Exc_L4'])    
        plots['HWHHHistogramExc'] = (PerNeuronValuePlot(dsv, ParameterSet({'cortical_view' : False})),gs[17:,1:7],{'title' : 'Excitatory' , 'x_lim' : (0.0,50.0), 'x_label' : 'HWHH'})
        dsv = queries.param_filter_query(self.datastore,value_name=['orientation HWHH of Firing rate'],sheet_name=['V1_Inh_L4'])    
        plots['HWHHHistogramInh'] = (PerNeuronValuePlot(dsv, ParameterSet({'cortical_view' : False})),gs[17:,8:14],{'title' : 'Inhibitory' , 'x_lim' : (0.0,50.0), 'x_label' : 'HWHH'})

        return plots
        

class ConductanceAndVmTuningSummary(Plotting):
    required_parameters = ParameterSet({
        'many' : bool, # If true it will show 4 times as many (but twice as small) example neurons
    })

    def subplot(self, subplotspec):
        plots = {}
        gs = gridspec.GridSpecFromSubplotSpec(16, 14, subplot_spec=subplotspec,
                                              hspace=1.0, wspace=1.0)
        
        analog_ids = sorted(queries.param_filter_query(self.datastore,sheet_name="V1_Exc_L4").get_analysis_result()[0].ids)
                
        dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F0_Exc_Cond-Mean(ECond)','F0_Inh_Cond-Mean(ICond)'],sheet_name='V1_Exc_L4')

        plots['MeanF0'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids), 'sheet_name' : 'V1_Exc_L4','centered'  : True,'mean' : True,'pool' : True,'polar' : True})),gs[:4,:3],{'legend' : True, 'y_label': 'F0(Cond)' ,'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F0_Exc_Cond-Mean(ECond) contrast : 100' : '#FF0000' , 'F0_Exc_Cond-Mean(ECond) contrast : 50' : '#FFACAC','F0_Inh_Cond-Mean(ICond) contrast : 100' : '#0000FF' , 'F0_Inh_Cond-Mean(ICond) contrast : 50' : '#ACACFF'}})

        dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F1_Exc_Cond','F1_Inh_Cond'],sheet_name='V1_Exc_L4')
        plots['MeanF1'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids), 'sheet_name' : 'V1_Exc_L4','centered'  : True,'mean' : True,'pool' : True,'polar' : True})),gs[4:8,:3],{'y_label': 'F1(Cond)','title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F1_Exc_Cond contrast : 100' : '#FF0000' , 'F1_Exc_Cond contrast : 50' : '#FFACAC','F1_Inh_Cond contrast : 100' : '#0000FF' , 'F1_Inh_Cond contrast : 50' : '#ACACFF'}})

        dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F0_Vm-Mean(VM)'],sheet_name='V1_Exc_L4')
        plots['MeanVMF0'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids), 'sheet_name' : 'V1_Exc_L4','centered'  : True,'mean' : True,'pool' : True,'polar' : True})),gs[8:12,:3],{'y_label': 'F0(Vm)' ,'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F0_Vm-Mean(VM) contrast : 100' : '#000000' , 'F0_Vm-Mean(VM) contrast : 50' : '#ACACAC'}})

        dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F1_Vm'],sheet_name='V1_Exc_L4')
        plots['MeanVMF1'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids), 'sheet_name' : 'V1_Exc_L4','centered'  : True,'mean' : True,'pool' : True,'polar' : True})),gs[12:16,:3],{'y_label': 'F1(Vm)','title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F1_Vm contrast : 100' : '#000000' , 'F1_Vm contrast : 50' : '#ACACAC'}})
        
        if True:
            if self.parameters.many:
                dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F0_Exc_Cond','F0_Inh_Cond'],sheet_name='V1_Exc_L4')
                plots['F0a'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids[0:10]), 'sheet_name' : 'V1_Exc_L4','centered'  : False,'mean' : False,'pool' : True,'polar' : True})),gs[:2,3:],{'y_label': None,'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F0_Exc_Cond contrast : 100' : '#FF0000' , 'F0_Exc_Cond contrast : 50' : '#FFACAC','F0_Inh_Cond contrast : 100' : '#0000FF' , 'F0_Inh_Cond contrast : 50' : '#ACACFF'}})

                dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F0_Exc_Cond','F0_Inh_Cond'],sheet_name='V1_Exc_L4')
                plots['F0b'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids[10:20]), 'sheet_name' : 'V1_Exc_L4','centered'  : False,'mean' : False,'pool' : True,'polar' : True})),gs[2:4,3:],{'y_label': None,'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F0_Exc_Cond contrast : 100' : '#FF0000' , 'F0_Exc_Cond contrast : 50' : '#FFACAC','F0_Inh_Cond contrast : 100' : '#0000FF' , 'F0_Inh_Cond contrast : 50' : '#ACACFF'}})


                dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F1_Exc_Cond','F1_Inh_Cond'],sheet_name='V1_Exc_L4')
                plots['F1a'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids[0:10]), 'sheet_name' : 'V1_Exc_L4','centered'  : False,'mean' : False,'pool' : True,'polar' : True})),gs[4:6,3:],{'y_label': None,'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F1_Exc_Cond contrast : 100' : '#FF0000' , 'F1_Exc_Cond contrast : 50' : '#FFACAC','F1_Inh_Cond contrast : 100' : '#0000FF' , 'F1_Inh_Cond contrast : 50' : '#ACACFF'}})

                dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F1_Exc_Cond','F1_Inh_Cond'],sheet_name='V1_Exc_L4')
                plots['F1b'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids[10:20]), 'sheet_name' : 'V1_Exc_L4','centered'  : False,'mean' : False,'pool' : True,'polar' : True})),gs[6:8,3:],{'y_label': None,'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F1_Exc_Cond contrast : 100' : '#FF0000' , 'F1_Exc_Cond contrast : 50' : '#FFACAC','F1_Inh_Cond contrast : 100' : '#0000FF' , 'F1_Inh_Cond contrast : 50' : '#ACACFF'}})


                dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F0_Vm-Mean(VM)'],sheet_name='V1_Exc_L4')
                plots['VMF0a'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids[0:10]), 'sheet_name' : 'V1_Exc_L4','centered'  : False,'mean' : False,'pool' : True,'polar' : True})),gs[8:10,3:],{'y_label': None ,'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F0_Vm-Mean(VM) contrast : 100' : '#000000' , 'F0_Vm-Mean(VM) contrast : 50' : '#ACACAC'}})

                dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F0_Vm-Mean(VM)'],sheet_name='V1_Exc_L4')
                plots['VMF0b'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids[10:20]), 'sheet_name' : 'V1_Exc_L4','centered'  : False,'mean' : False,'pool' : True,'polar' : True})),gs[10:12,3:],{'y_label': None ,'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F0_Vm-Mean(VM) contrast : 100' : '#000000' , 'F0_Vm-Mean(VM) contrast : 50' : '#ACACAC'}})


                dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F1_Vm'],sheet_name='V1_Exc_L4')
                plots['VMF1a'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids[0:10]), 'sheet_name' : 'V1_Exc_L4','centered'  : False,'mean' : False,'pool' : True,'polar' : True})),gs[12:14,3:],{'y_label': None,'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F1_Vm contrast : 100' : '#000000' , 'F1_Vm contrast : 50' : '#ACACAC'}})

                dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F1_Vm'],sheet_name='V1_Exc_L4')
                plots['VMF1b'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids[10:20]), 'sheet_name' : 'V1_Exc_L4','centered'  : False,'mean' : False,'pool' : True,'polar' : True})),gs[14:16,3:],{'y_label': None,'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F1_Vm contrast : 100' : '#000000' , 'F1_Vm contrast : 50' : '#ACACAC'}})

            else:
                #dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F0_Exc_Cond-Mean(ECond)','F0_Inh_Cond-Mean(ICond)'],sheet_name='V1_Exc_L4')
                #plots['F0'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids[:5]), 'sheet_name' : 'V1_Exc_L4','centered'  : False,'mean' : False,'pool' : False,'polar' : False})),gs[:4,3:],{'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'contrast : 100' : '#FF0000' , 'contrast : 50' : '#FFACAC'}})

                #dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F1_Exc_Cond','F1_Inh_Cond'],sheet_name='V1_Exc_L4')
                #plots['F1'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(analog_ids[:5]), 'sheet_name' : 'V1_Exc_L4','centered'  : False,'mean' : False,'pool' : False,'polar' : False})),gs[5:9,3:],{'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'contrast : 100' : '#FF0000' , 'contrast : 50' : '#FFACAC'}})
                
                neurons = [0,1,2,3,4,5]
                #neurons = [5,15,3,38,18,24]
                #neurons = [30,31,32,33,34,35,36,37,38,39,40]
                
                dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F0_Exc_Cond-Mean(ECond)','F0_Inh_Cond-Mean(ICond)'],sheet_name='V1_Exc_L4')
                plots['F0'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(numpy.array(analog_ids)[neurons]), 'sheet_name' : 'V1_Exc_L4','centered'  : False,'mean' : False,'pool' : True,'polar' : True})),gs[:4,3:],{'legend' : False, 'y_label': None ,'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F0_Exc_Cond-Mean(ECond) contrast : 100' : '#FF0000' , 'F0_Exc_Cond-Mean(ECond) contrast : 50' : '#FFACAC','F0_Inh_Cond-Mean(ICond) contrast : 100' : '#0000FF' , 'F0_Inh_Cond-Mean(ICond) contrast : 50' : '#ACACFF'}})

                dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F1_Exc_Cond','F1_Inh_Cond'],sheet_name='V1_Exc_L4')
                plots['F1'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(numpy.array(analog_ids)[neurons]), 'sheet_name' : 'V1_Exc_L4','centered'  : False,'mean' : False,'pool' : True,'polar' : True})),gs[4:8,3:],{'y_label': None,'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F1_Exc_Cond contrast : 100' : '#FF0000' , 'F1_Exc_Cond contrast : 50' : '#FFACAC','F1_Inh_Cond contrast : 100' : '#0000FF' , 'F1_Inh_Cond contrast : 50' : '#ACACFF'}})

                dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F0_Vm-Mean(VM)'],sheet_name='V1_Exc_L4')
                plots['VMF0'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(numpy.array(analog_ids)[neurons]), 'sheet_name' : 'V1_Exc_L4','centered'  : False,'mean' : False,'pool' : True,'polar' : True})),gs[8:12,3:],{'y_label': None ,'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F0_Vm-Mean(VM) contrast : 100' : '#000000' , 'F0_Vm-Mean(VM) contrast : 50' : '#ACACAC'}})

                dsv = queries.param_filter_query(self.datastore,identifier='PerNeuronValue',value_name=['F1_Vm'],sheet_name='V1_Exc_L4')
                plots['VMF1'] = (PlotTuningCurve(dsv, ParameterSet({'parameter_name' : 'orientation', 'neurons': list(numpy.array(analog_ids)[neurons]), 'sheet_name' : 'V1_Exc_L4','centered'  : False,'mean' : False,'pool' : True,'polar' : True})),gs[12:16,3:],{'y_label': None,'title' : None, 'x_ticks' : None, 'x_label' : None,'colors': {'F1_Vm contrast : 100' : '#000000' , 'F1_Vm contrast : 50' : '#ACACAC'}})
                

        return plots
        


class BarComparisonPlot(StandardStyle):
    def __init__(self, values,**param):
        StandardStyle.__init__(self,**param)
        self.values = values

    def plot(self):
        width = 1.0/len(self.values.keys())/2.0
        x = numpy.linspace(0+width,1-width,len(self.values.keys()))
        
        self.axis.bar(x-width/2.0,self.values.values(),width = width,color='k')
        self.x_lim = [0,1.0]
        self.x_tick_labels = self.values.keys()
        self.x_ticks = x
        self.x_tick_style="Custom"

class TrialToTrialVariabilityComparison(Plotting):

    def subplot(self, subplotspec):
        plots = {}
        gs = gridspec.GridSpecFromSubplotSpec(6, 18, subplot_spec=subplotspec,hspace=1.0, wspace=1.0)
        
        var_gr = 0
        var_ni = 0
        std_gr = 0
        std_ni = 0
                
        orr = list(set([MozaikParametrized.idd(s).orientation for s in queries.param_filter_query(self.datastore,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=100).get_stimuli()]))        
        l4_exc_or = self.datastore.get_analysis_result(identifier='PerNeuronValue',value_name = 'LGNAfferentOrientation', sheet_name = 'V1_Exc_L4')
        
        
        # lets calculate spont. activity trial to trial variability
        # we assume that the spontaneous activity had already the spikes removed
        #queries.param_filter_query(self.datastore,st_name='InternalStimulus',st_direct_stimulation_name='None',sheet_name='V1_Exc_L4',ads_unique=True).print_content(full_ADS=True)
        
        
        dsv = queries.param_filter_query(self.datastore,st_name='InternalStimulus',st_direct_stimulation_name='None',sheet_name='V1_Exc_L4',analysis_algorithm='ActionPotentialRemoval',ads_unique=True)
        ids = dsv.get_analysis_result()[0].ids
        sp = {}
        for idd in ids:
            s = dsv.get_analysis_result()[0].get_asl_by_id(idd).magnitude
            sp[idd] = numpy.mean(1/numpy.std([s[i*int(len(s)/10):(i+1)*int(len(s)/10)] for i in xrange(0,10)],axis=0,ddof=1))

            
            
        #lets calculate the mean of trial-to-trial variances across the neurons in the datastore for gratings 
        dsv = queries.param_filter_query(self.datastore,st_name='FullfieldDriftingSinusoidalGrating',sheet_name='V1_Exc_L4',st_contrast=100,analysis_algorithm='TrialVariability',y_axis_name='Vm (no AP) trial-to-trial variance')
        assert queries.equal_ads(dsv, except_params=['stimulus_id'])
        ids = dsv.get_analysis_result()[0].ids
        
        for i in ids:
            # find the or pereference of the neuron
            o = orr[numpy.argmin([circular_dist(o,l4_exc_or[0].get_value_by_id(i),numpy.pi) for o in orr])]
            a = numpy.mean(1/numpy.sqrt(queries.param_filter_query(dsv,st_orientation=o,ads_unique=True).get_analysis_result()[0].get_asl_by_id(i).magnitude))
            var_gr = var_gr + a / sp[i]
            std_gr = std_gr + a
        var_gr = var_gr / len(ids)
        std_gr = std_gr / len(ids)
        
        
        
        #lets calculate the mean of trial-to-trial variances across the neurons in the datastore for gratings 
        dsv = queries.param_filter_query(self.datastore,st_name='NaturalImageWithEyeMovement',sheet_name='V1_Exc_L4',y_axis_name='Vm (no AP) trial-to-trial variance',ads_unique=True)
        ids = dsv.get_analysis_result()[0].ids
        var_ni = numpy.mean([numpy.mean(1/numpy.sqrt(dsv.get_analysis_result()[0].get_asl_by_id(i).magnitude)) / sp[i] for i in ids])
        plots['Bar'] = (BarComparisonPlot({"NI" : var_ni*100.0, "GR" : var_gr*100.0}),gs[:,:],{})
        return plots


class SNRAnalysis(Plotting):
        """
        SNR Analysis replicated from:
        Baudot, P., Levy, M., Marre, O., Monier, C., Pananceau, M., & Frégnac, Y. (2013). Animation of natural scene by virtual eye-movements evokes high precision and low noise in V1 neurons. Frontiers in neural circuits, 7(December), 206. doi:10.3389/fncir.2013.00206
        
        Differences:
        
        * The wavelet kernel has more cycles than on pictures in the paper (but follows the sigma*frequency=2 equation stated in methods).
        * I subtract the mean of the Vm for the given stimulus presentation to get rid of the edge effects.
        """
        
        required_parameters = ParameterSet({
            'neuron': int,  # neurond id 
        })

        
        def plot(self):
            self.fig = pylab.figure(facecolor='w', **self.fig_param)
            gs = gridspec.GridSpec(1, 1)
            gs.update(left=0.07, right=0.97, top=0.9, bottom=0.1)
            gs = gs[0,0]
            
            gs = gridspec.GridSpecFromSubplotSpec(4, 5,subplot_spec=gs)

            orr = list(set([MozaikParametrized.idd(s).orientation for s in queries.param_filter_query(self.datastore,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=100).get_stimuli()]))        
            l4_exc_or = self.datastore.get_analysis_result(identifier='PerNeuronValue',value_name = 'LGNAfferentOrientation', sheet_name = 'V1_Exc_L4')

            
            col = orr[numpy.argmin([circular_dist(o,l4_exc_or[0].get_value_by_id(self.parameters.neuron),numpy.pi)  for o in orr])]
            #segs = queries.param_filter_query(self.datastore,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=100,st_orientation=col,sheet_name='V1_Exc_L4').get_segments()
            #signals = [seg.get_vm(self.parameters.neuron) for seg in segs] 
            dsv = queries.param_filter_query(self.datastore,st_name='FullfieldDriftingSinusoidalGrating',sheet_name='V1_Exc_L4',st_contrast=100,analysis_algorithm='ActionPotentialRemoval',st_orientation=col)
            assert queries.ads_with_equal_stimuli(dsv,except_params=["trial"])
            adss = dsv.get_analysis_result()
            signals = [ads.get_asl_by_id(self.parameters.neuron) for ads in adss] 
            
            (signal,noise,snr) = self.wavelet_decomposition(signals)
            
            ax = pylab.subplot(gs[0,0:2])            
            for s in signals:
                ax.plot(s,c='k')
            pylab.ylabel('Vm')
            pylab.title("Gratings",fontsize=20)
            pylab.xlim(0,len(signals[0]))
            pylab.ylim(-80,-50)
            
            ax = pylab.subplot(gs[1,0:2])            
            ax.imshow(signal,aspect='auto',origin='lower')
            pylab.ylabel('Signal')
             
            ax = pylab.subplot(gs[2,0:2])            
            ax.imshow(noise,aspect='auto',origin='lower')
            pylab.ylabel('Noise')

            ax = pylab.subplot(gs[3,0:2])            
            ax.imshow(snr,aspect='auto',origin='lower')
            pylab.ylabel('SNR')
            pylab.xlabel('time')
            
            
            #segs = queries.param_filter_query(self.datastore,st_name='NaturalImageWithEyeMovement',sheet_name='V1_Exc_L4').get_segments()
            #signals = [seg.get_vm(self.parameters.neuron) for seg in segs] 
            dsv = queries.param_filter_query(self.datastore,st_name='NaturalImageWithEyeMovement',sheet_name='V1_Exc_L4',analysis_algorithm='ActionPotentialRemoval')
            assert queries.ads_with_equal_stimuli(dsv,except_params=["trial"])
            adss = dsv.get_analysis_result()
            signals = [ads.get_asl_by_id(self.parameters.neuron) for ads in adss] 
           
            (signal_ni,noise_ni,snr_ni) = self.wavelet_decomposition(signals)
            
            ax = pylab.subplot(gs[0,2:4])            
            for s in signals:
                ax.plot(s,c='k')
            pylab.xlim(0,len(signals[0]))                
            pylab.ylim(-80,-50)
            pylab.title("NI",fontsize=20)
            ax = pylab.subplot(gs[1,2:4])            
            ax.imshow(signal_ni,aspect='auto',origin='lower')

            ax = pylab.subplot(gs[2,2:4])            
            ax.imshow(noise_ni,aspect='auto',origin='lower')

            ax = pylab.subplot(gs[3,2:4])            
            ax.imshow(snr_ni,aspect='auto',origin='lower')
            pylab.xlabel('time')
            
            ax = pylab.subplot(gs[1,4])            
            ax.plot(numpy.mean(signal,axis=1),label="GR")
            ax.plot(numpy.mean(signal_ni,axis=1),label="NI")
            ax.set_xscale('log')
            ax.set_yscale('log')
            pylab.legend()
            
            ax = pylab.subplot(gs[2,4])            
            ax.plot(numpy.mean(noise,axis=1))
            ax.plot(numpy.mean(noise_ni,axis=1))
            ax.set_xscale('log')
            ax.set_yscale('log')
            
            ax = pylab.subplot(gs[3,4])            
            ax.plot(numpy.mean(snr,axis=1))
            ax.plot(numpy.mean(snr_ni,axis=1))
            ax.set_xscale('log')
            ax.set_yscale('log')
            pylab.xlabel("frequency")
            
            
            if self.plot_file_name:
               pylab.savefig(Global.root_directory+self.plot_file_name)              

            
        def gabor_wavelet(self,f,sf):
            sigma = 2.0/f
            x = numpy.linspace(-2 * sigma, 2 * sigma, 4*sigma*sf+1) 
            y = 1/numpy.sqrt(f) * numpy.exp(-2*numpy.pi*1j*f*x)*numpy.exp(-numpy.power(x/sigma,2))
            y = y/numpy.sum(numpy.abs(y))
            return y

        def wavelet_decomposition(self,signals):
            import scipy.signal
            
            signal = []
            noise = []
            snr = []
            for freq in xrange(1,75):
                dec = numpy.array([scipy.signal.fftconvolve(s-numpy.mean(s),self.gabor_wavelet(freq,s.sampling_rate.rescale(qt.Hz).magnitude),mode='same') for s in signals])
                l = len(dec[0])
                l1 = len(signals[0])
                if l > l1:
                   dec  = [d[int((l-l1)/2):int((l-l1)/2)+l1]  for d in dec] 
                m = numpy.mean(dec,axis=0)
                signal.append(numpy.absolute(m))
                noise.append(numpy.mean(numpy.absolute(dec - m),axis=0))
                snr.append(numpy.divide(signal[-1], noise[-1]))
            return (numpy.array(signal),numpy.array(noise),numpy.array(snr))


class TrialCrossCorrelationAnalysis(Plotting):
        """
        Trial-to-trial crosscorrelation analysis replicated from figure 4D:
        Baudot, P., Levy, M., Marre, O., Monier, C., Pananceau, M., & Frégnac, Y. (2013). Animation of natural scene by virtual eye-movements evokes high precision and low noise in V1 neurons. Frontiers in neural circuits, 7(December), 206. doi:10.3389/fncir.2013.00206
        
        Differences:
        
        Notes:
        It assumes that the TrialToTrialCrossCorrelationOfPSTHandVM analysis was run on natural images, and that it was run with the 2.0 ms  bin lentgth for calculating of PSTH
        and that the optimal preferred orientation for all the neurons for which the .
        """
        
        required_parameters = ParameterSet({
            'neurons': list,  # The list of neurons to include in the analysis
            'window_length' : int, #ms
        })

        
        def plot(self):
            self.fig = pylab.figure(facecolor='w', **self.fig_param)
            gs = gridspec.GridSpec(1, 1)
            gs.update(left=0.07, right=0.97, top=0.9, bottom=0.1)
            gs = gs[0,0]
            gs = gridspec.GridSpecFromSubplotSpec(1, 2,subplot_spec=gs)

            orr = list(set([MozaikParametrized.idd(s).orientation for s in queries.param_filter_query(self.datastore,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=100).get_stimuli()]))        
            l4_exc_or = self.datastore.get_analysis_result(identifier='PerNeuronValue',value_name = 'LGNAfferentOrientation', sheet_name = 'V1_Exc_L4')
            
            for neuron_idd in self.parameters.neurons:
                col = orr[numpy.argmin([circular_dist(o,l4_exc_or[0].get_value_by_id(neuron_idd),numpy.pi)  for o in orr])]
                dsv =  queries.param_filter_query(self.datastore,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=100,st_orientation=col,sheet_name='V1_Exc_L4',analysis_algorithm='ActionPotentialRemoval')
                TrialToTrialCrossCorrelationOfAnalogSignalList(dsv,ParameterSet({'neurons' : [neuron_idd]}),tags=['helper']).analyse()
                dsv =  queries.param_filter_query(self.datastore,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=100,st_orientation=col,sheet_name='V1_Exc_L4',analysis_algorithm='PSTH')
                TrialToTrialCrossCorrelationOfAnalogSignalList(dsv,ParameterSet({'neurons' : [neuron_idd]}),tags=['helper']).analyse()
                
                
            dsv =  queries.tag_based_query(self.datastore,['helper'])   
            dsv1 =  queries.param_filter_query(dsv,y_axis_name='trial-trial cross-correlation of Vm (no AP)',st_name='FullfieldDriftingSinusoidalGrating',st_contrast=100,st_orientation=col,sheet_name='V1_Exc_L4')
            vm_cc_gr = numpy.mean(numpy.array([asl.asl[0] for asl in dsv1.get_analysis_result()]),axis=0)
            dsv1 =  queries.param_filter_query(dsv,y_axis_name='trial-trial cross-correlation of psth (bin=2.0)')
            psth_cc_gr = numpy.mean(numpy.array([asl.asl[0] for asl in dsv1.get_analysis_result()]),axis=0)
            
            
            #queries.param_filter_query(self.datastore,analysis_algorithm='TrialToTrialCrossCorrelationOfAnalogSignalList').print_content(full_ADS=True)
            
            dsv =  queries.param_filter_query(self.datastore,y_axis_name='trial-trial cross-correlation of Vm (no AP)',st_name="NaturalImageWithEyeMovement",ads_unique=True)
            vm_cc_ni = numpy.mean(numpy.array(dsv.get_analysis_result()[0].asl),axis=0)
            dsv =  queries.param_filter_query(self.datastore,y_axis_name='trial-trial cross-correlation of psth (bin=2.0)',st_name="NaturalImageWithEyeMovement",ads_unique=True)
            psth_cc_ni = numpy.mean(numpy.array(dsv.get_analysis_result()[0].asl),axis=0)
            
            z = int(min(self.parameters.window_length,len(vm_cc_gr-1)/2,len(vm_cc_ni-1)/2)/2)*2
                
            ax = pylab.subplot(gs[0,0])       
            ax.plot(numpy.linspace(-z,z,2*z+1),vm_cc_gr[int(len(vm_cc_gr)/2)-z:int(len(vm_cc_gr)/2)+z+1],label="Gratings")
            ax.plot(numpy.linspace(-z,z,2*z+1),vm_cc_ni[int(len(vm_cc_ni)/2)-z:int(len(vm_cc_ni)/2)+z+1],label="Natural images")
            pylab.legend()
            pylab.title("VM")
            pylab.xlabel("time (ms)")
            pylab.ylabel("corr coef")
            
            ax = pylab.subplot(gs[0,1])
            ax.plot(numpy.linspace(-z,z,z+1),psth_cc_gr[int(len(psth_cc_gr)/2)-z/2:int(len(psth_cc_gr)/2)+z/2+1],label="Gratings")
            ax.plot(numpy.linspace(-z,z,z+1),psth_cc_ni[int(len(psth_cc_ni)/2)-z/2:int(len(psth_cc_ni)/2)+z/2+1],label="Natural images")
            pylab.legend()
            pylab.title("Spikes")
            pylab.xlabel("time (ms)")
            if self.plot_file_name:
               pylab.savefig(Global.root_directory+self.plot_file_name)              
                


class FanoFactor_Baudot_et_al(Plotting):
    """
    Fano factor analysis replicated from figure 4C:
    Baudot, P., Levy, M., Marre, O., Monier, C., Pananceau, M., & Frégnac, Y. (2013). Animation of natural scene by virtual eye-movements evokes high precision and low noise in V1 neurons. Frontiers in neural circuits, 7(December), 206. doi:10.3389/fncir.2013.00206
    
    Notes:
    ------
    It assumes all neurons for which Vm was recorded had 0 degree orientation preference!!!!
    """

    def subplot(self, subplotspec):
        plots = {}
        gs = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=subplotspec,hspace=1.0, wspace=1.0)

        dsv = queries.param_filter_query(self.datastore,value_name='Fano Factor (spike count (bin=13.0))')   
        a= queries.param_filter_query(dsv,analysis_algorithm='TrialToTrialFanoFactorOfAnalogSignal',st_name="NaturalImageWithEyeMovement").get_analysis_result()[0].values
        b= queries.param_filter_query(dsv,analysis_algorithm='TrialToTrialFanoFactorOfAnalogSignal',st_name="FullfieldDriftingSinusoidalGrating",st_orientation=0).get_analysis_result()[0].values
        
        a = a[~numpy.isnan(a)]
        b = b[~numpy.isnan(b)]
        
        plots['Bar'] = (BarComparisonPlot({"NI" : numpy.mean(a), "GR" : numpy.mean(b)}),gs[:,:],{})
        return plots



class MeanVsVarainceOfVM(Plotting):
    """
    Shows the realtionship between the trial-to-trial mean and varaince of the Vm, after spike removal.
    """
    
    required_parameters = ParameterSet({
            'neurons': list,  # The list of neurons to include in the analysis
        })

    def subplot(self, subplotspec):
        plots = {}
        gs = gridspec.GridSpecFromSubplotSpec(20, 1, subplot_spec=subplotspec,hspace=1.0, wspace=1.0)
        
        dsv = queries.param_filter_query(self.datastore,y_axis_name=['Vm (no AP) trial-to-trial mean','Vm (no AP) trial-to-trial variance'],st_name="NaturalImageWithEyeMovement")
        plots['plot1'] = (PerNeuronAnalogSignalScatterPlot(dsv,ParameterSet({'neurons' : self.parameters.neurons})),gs[2:10,0],{})
        dsv = queries.param_filter_query(self.datastore,y_axis_name=['Vm (no AP) trial-to-trial mean','Vm (no AP) trial-to-trial variance'],st_name="FullfieldDriftingSinusoidalGrating",st_orientation=0,st_contrast=100)
        plots['plot2'] = (PerNeuronAnalogSignalScatterPlot(dsv,ParameterSet({'neurons' : self.parameters.neurons})),gs[12:,0],{})
        return plots
