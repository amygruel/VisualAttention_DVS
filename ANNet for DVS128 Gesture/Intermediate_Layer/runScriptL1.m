%file names
inputFile='gesture_data.mat';
inputFolder='../data/';

AN_simu_name='ANtest';
AN_saveFolder='../Attention_Neuron/';

L1_simu_name='L1test';
L1_saveFolder='';

%load files
load([inputFolder inputFile]);
format long g;
signal.data = gesturedata;
signal.nSignals=1;
signal.dt=1.25e-5;
signal.start=0;
signal.line_size=size(signal.data,2);
signal.col_size=size(signal.data,1);
signal.stop=round(max(max(signal.data)));

ANfile=[ AN_simu_name '_on_' inputFile];
load([AN_saveFolder ANfile],'spikeTrainAN');

%prepare parameters
simuparameter;
PARAM_L1=createParamLayer1(SIMU);
SPIKETRANSPOSITION=prepareSpikeTransposition(SIMU,signal);
INPUTSPIKES=prepareInputSpikes(spikeTrainAN,1/signal.dt);
neuron = createNewNeuronLayer1(SIMU,SPIKETRANSPOSITION,signal.stop);

%run simulation
%start=signal.start/signal.dt;
start=signal.start;
stop=start+signal.stop;
tic
[neuron]=STDPFromSignalAndSpikes(neuron,struct(signal),INPUTSPIKES,SPIKETRANSPOSITION,PARAM_L1,start,stop);
toc

%save results
spikeTrainL1=convertNeuronToSpikeTrain(neuron,signal.dt);
L1Weight=[neuron.weight];
L1PotHist=reshape([neuron.PotHist],numel(neuron(1).PotHist),numel(neuron));
L1WHist=[neuron.WHist];

resultfile=[L1_saveFolder L1_simu_name '_on_' inputFile];
save(resultfile,'spikeTrainL1','L1Weight','SIMU','AN_simu_name','L1PotHist','L1WHist');

