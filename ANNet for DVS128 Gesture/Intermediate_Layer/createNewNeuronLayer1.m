function neuron = createNewNeuronLayer1(SIMU,TRANSPO,nSteps)
nNeur=SIMU.L1_nNeurons;
for idx=1:nNeur
    neuron(idx).nextFiring = int32(-1);
    neuron(idx).firingTime = int32(zeros(1,ceil(nSteps*0.1)));
    neuron(idx).nFiring = uint32(0);
    neuron(idx).weight={};
    
    neuron(idx).weight{1} = rand(TRANSPO.DVS_x,TRANSPO.DVS_y,TRANSPO.twindow)*(SIMU.L1_initWmax-SIMU.L1_initWmin)+SIMU.L1_initWmin;
    
    neuron(idx).threshold=SIMU.L1_threshold;
    neuron(idx).resetPotential=SIMU.L1_resetPotentialFactor*neuron(idx).threshold;
    neuron(idx).lastComputedPotential=0;
    neuron(idx).lastComputationTime=int32(0);
    
    neuron(idx).iWeight=neuron(idx).threshold*SIMU.L1_wiFactor*ones(1,nNeur);
    neuron(idx).DNWeight=SIMU.L1_DNWeight;
    
    neuron(idx).refractoryPeriod=int32(SIMU.L1_refractoryPeriod);
    
    %for potential and weight history
    neuron(idx).PotHist = zeros(1,ceil(SIMU.PotHistDuration/SIMU.PotHistStep)+1);
    neuron(idx).WHist=cell(ceil(SIMU.WHistDuration/SIMU.WHistStep),length(TRANSPO));
    for t=1:(ceil(SIMU.WHistDuration/SIMU.WHistStep))
        neuron(idx).WHist{t,1} = zeros(TRANSPO.DVS_x,TRANSPO.DVS_y,TRANSPO.twindow);
    end
    
    %utils for STDP
    neuron(idx).lastPostSpike=int32(-1);
    neuron(idx).lastInhibition=int32(-1);
    
end

end
