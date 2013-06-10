#!/usr/local/bin/ipython -i 
from mozaik.framework.experiment import *
from mozaik.framework.population_selector import RCRandomPercentage
from parameters import ParameterSet
    
def create_experiments(model):
    return              [
                           #Spontaneous Activity 
                           #MeasureSpontaneousActivity(model,duration=147*7,num_trials=15),

                           #GRATINGS
                           #MeasureOrientationTuningFullfield(model,num_orientations=2,spatial_frequency=0.8,temporal_frequency=2,grating_duration=147*7,contrasts=[5,10,20,30,40,50,60,70,80,90,100],num_trials=5),
                           #MeasureOrientationTuningFullfield(model,num_orientations=2,spatial_frequency=0.8,temporal_frequency=2,grating_duration=147*7,contrasts=[100],num_trials=1),
                           MeasureOrientationTuningFullfield(model,num_orientations=2,spatial_frequency=0.8,temporal_frequency=2,grating_duration=147*7,contrasts=[100],num_trials=2),
                       
                           #IMAGES WITH EYEMOVEMENT
                           #MeasureNaturalImagesWithEyeMovement(model,stimulus_duration=147*7,num_trials=15),

                           #GRATINGS WITH EYEMOVEMENT
                           #MeasureDriftingSineGratingWithEyeMovement(model,spatial_frequency=0.8,temporal_frequency=2,stimulus_duration=147*7,num_trials=15,contrast=100),
                        ]

