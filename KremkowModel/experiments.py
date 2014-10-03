#!/usr/local/bin/ipython -i 
from mozaik.experiments import *
from mozaik.experiments.vision import *
from mozaik.sheets.population_selector import RCRandomPercentage
from parameters import ParameterSet
    
def create_experiments(model):
    return              [
                           #Spontaneous Activity 
                           NoStimulation(model,duration=6*147*7),

                           #GRATINGS
                           #MeasureOrientationTuningFullfield(model,num_orientations=2,spatial_frequency=0.8,temporal_frequency=2,grating_duration=147*7,contrasts=[5,10,20,30,40,50,60,70,80,90,100],num_trials=5),
                           #MeasureOrientationTuningFullfield(model,num_orientations=10,spatial_frequency=0.8,temporal_frequency=2,grating_duration=147*7,contrasts=[100],num_trials=15),
                           #MeasureOrientationTuningFullfield(model,num_orientations=10,spatial_frequency=0.8,temporal_frequency=2,grating_duration=147*7*2,contrasts=[50,100],num_trials=10),
                           MeasureOrientationTuningFullfield(model,num_orientations=3,spatial_frequency=0.8,temporal_frequency=2,grating_duration=147*7,contrasts=[100],num_trials=2),
                       
                           #MeasureFrequencySensitivity(model,orientation=0,spatial_frequencies=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5],temporal_frequencies=[2.0],grating_duration=147*7*2,contrasts=[100],num_trials=1),
                           
                           #MeasureFrequencySensitivity(model,orientation=0,spatial_frequencies=[0.01,0.8,1.5],temporal_frequencies=[2.0],grating_duration=147*7*2,contrasts=[100],num_trials=1),                           
                           
                           #IMAGES WITH EYEMOVEMENT
                           #MeasureNaturalImagesWithEyeMovement(model,stimulus_duration=3*147*7,num_trials=2),

                           #GRATINGS WITH EYEMOVEMENT
                           #MeasureDriftingSineGratingWithEyeMovement(model,spatial_frequency=0.8,temporal_frequency=2,stimulus_duration=147*7,num_trials=10,contrast=100),
                        ]

