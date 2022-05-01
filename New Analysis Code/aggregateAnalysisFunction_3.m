function [angleRT_Raw] = aggregateAnalysisFunction_3(color)
%% Input Options
[subjectNames, protocol, attention] = InputOptions();
folderName = strcat('Subject Plots Folder', {' '}, attention, {' '}, protocol);
mkdir(folderName{1});
%% User-Interface getDirectory / Plot Data
myDir = uigetdir; %gets directory
myFiles = dir(fullfile(myDir,'*.csv'));
C = {[0.5020 0.5020 0.5020],[0 0 0],[1.0000    0.4118    0.1608], [0.6353    0.0784    0.1843],  [0.0745    0.6235    1.0000], [0 0 1]};
L = {'-', '--', '-', '--', '-', '--'};
dn = { 'Covert SRT', 'Overt SRT', 'Covert 2 CRT', 'Overt 2 CRT', 'Covert 3 CRT', 'Overt 3 CRT'};
S = {'o', 'd', '*', '^', 's', 'h'};
% plotSeparate = true/false
plotSeparate = true;
[angleRT_init, angleRT_Raw, incorrectPerc, rt_Avg_Struct,stats, rt_Structure_raw,...
    angles, angleRTMean, IncorrectStruct, IncorrectPercStruct, masterAngles]...
    = PlotSubjectData(subjectNames, attention, protocol,myDir, myFiles, plotSeparate,...
    folderName, color);
masterAngles = unique(masterAngles);
%% Organize Data
[OutputParamStats, IncorrectTest] = ...
    organizeData(myFiles, myDir, subjectNames,stats, incorrectPerc, masterAngles);
%% Test for Normality
[normalityTableLillie, normalityJB] = normalityTest(myFiles, myDir, angleRT_Raw, angles);
%% Hypothesis Testing
% num options (# of buttons / choices)
numOptions = 1/3;
[incorrectHypArray] = hypothesisTesting(myFiles, myDir, angles, numOptions,...
    angleRT_Raw, masterAngles);
%% Plotting Incorrect Percentages
cd(folderName{1});
for k = 1:length(myFiles)
    clear angles;
    baseFileName = myFiles(k).name;
    fullFileName = fullfile(myDir, baseFileName);
    data = table2array(readtable(fullFileName));
    dist = data(:,2);
    angles = unique(dist);
    figure();
    clear stdE_binom;
    clear binom_Prob;
    for ii = 1:length(angles)
        angleRT_Raw(k).subject(ii).data(angleRT_Raw(k).subject(ii).data == 0) = NaN;
        
        binomial_prob(k).data(ii).data =length(find(isnan(angleRT_Raw(k).subject(ii).data)))...
            /length(angleRT_Raw(k).subject(ii).data);
        binomProb(ii) = length(find(isnan(angleRT_Raw(k).subject(ii).data)))...
            /length(angleRT_Raw(k).subject(ii).data);
        standardErr_binom(k).data(ii).data = sqrt(binomial_prob(k).data(ii).data .* ...
            (1-binomial_prob(k).data(ii).data) ./ length(angleRT_Raw(k).subject(ii).data));
        stdE_binom(ii) = sqrt(binomial_prob(k).data(ii).data .* ...
            (1-binomial_prob(k).data(ii).data) ./ length(angleRT_Raw(k).subject(ii).data));
    end
    idx = [];
    for ii = 1:length(angles)
        idx = [idx,find(angles(ii) == transpose(masterAngles))];
    end
    bar(angles, IncorrectTest(k+1, idx(1)+1:idx(end)+1)*100);
    hold on;
%     errorbar(angles, IncorrectTest(k+1,2:end)*100, 100.*[standardErr_binom(k).data.data],...
%         'o', 'Color', 'r', 'MarkerFaceColor', 'r');
    errorbar(angles, IncorrectTest(k+1,idx(1)+1:idx(end)+1)*100, 100.*[stdE_binom],...      
        'o', 'Color', 'r', 'MarkerFaceColor', 'r');
    ylim([0 100]);
    xlabel('Eccentricity (°)');
    ylabel('Percentage Incorrect');
    title(strcat('Subject',{' '}, string(k),{' '}, 'Incorrect Percentage' ));
    fileName = strcat('Subject','_', string(k),'_', 'Incorrect Percentage.png' );
    saveas(gcf, fileName);
end
clear stdE_binom;
clear standardError_binom;
cd ..
%% Output Data to xlsx
cd(folderName{1});
T = struct2table(OutputParamStats);
filename = 'OutputParameters.xlsx';
writetable(T,filename,'Sheet',1);
T2 = array2table(incorrectHypArray(2:end, :));
T2.Properties.VariableNames = {'Subject', '-60', '-45', '-30', '-15'...
    '0', '15', '30', '45', '60'};
filename = 'Hypothesis_Testing_Values.xlsx';
writetable(T2, filename, 'Sheet', 1);
cd .. ;
%% Aggregate Plot Single Condition
[AggregateMeans, AggregateStd, aggregateRT, angleRT_New, aggregateSubjectMeans...,
    aggregatePosFit, aggregateNegFit, aggregateStd_E] =...
    AggregateAnalysisFunction(myFiles, myDir, angleRT_Raw,folderName, color, masterAngles);

%% ANOVA test
[pAnova, tblAnova, anovaStats] = anova1(aggregateSubjectMeans);
multCompare = multcompare(anovaStats);
%% Three-way ANOVA Test
angleAnova= [];
RTAnova = [];
subjectAnova = [];
observationNum = [];
for k = 1:length(myFiles)
    clear angles;
    clear dist;
    baseFileName = myFiles(k).name;
    fullFileName = fullfile(myDir, baseFileName);
    data = table2array(readtable(fullFileName));
    dist = data(:,2);
    RT = data(:,3);
    angleAnova = [angleAnova; dist];
    RTAnova = [RTAnova; RT];
    subjectAnova = [subjectAnova; k*ones([length(dist), 1])];
    observationNum = [observationNum; transpose(1:1:length(dist))];
end
RTAnova(RTAnova == 0) = NaN;
%% N-way Analysis of Variance
[p_anovaN, tbl_anovaN, stats_anovaN] = ...
    anovan(RTAnova, {angleAnova, subjectAnova, observationNum},...
    'varnames',{'Eccentricity','Subject', 'Observation Number'});

