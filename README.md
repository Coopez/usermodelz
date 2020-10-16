# Melting Active Retrieval

Description:
Implemented in this repository you find a experimental set up build in OpenSesame to run two distinct modification of the intelligent learning system SlimStampen.
In one of the experiments (partially) active retrieval from almost forgotten items is promoted by presenting the participant with increasingly obvious hints.
In the other experiment, participants can alter item's initial forgetting rate if they think at first encounter already that an item is particularly easy or particularly difficult

Requirements:

## Set up:

With anaconda (cross-platform) run:

### create an environment
conda create -n opensesame-py3 python=3.7

conda activate opensesame-py3

### set path and install packages
conda config --add channels cogsci --add channels conda-forge

conda install python-opensesame opensesame-extension-osweb opensesame-plugin-psychopy psychopy rapunzel python-pygaze

pip3 install soundfile pygame yolk3k opensesame-extension-osf python-qtpip http://files.cogsci.nl/expyriment-0.10.0+opensesame2-py3-none-any.whl

## Run
start OpenSesame by running:
opensesame

In the UI of opensesame open the experiment file "MeltingActiveRetrievalAlpha.osexp" that you have downloaded from this repository.
In the initial prompts please indicate the participant number that we allocated to you 
and also indicate the location to which the log file can be saved. Please send us this log file after the experiment.
