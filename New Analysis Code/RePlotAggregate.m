clear all;
close all;

global readX;

%% Experiment Information
[dName, axNames, refD, readXValues, listing, ...
    protOrder, protocolNames, colors, linestyle] = experimentInformation();
myDir = listing(1).folder;
S = {'o', 'd', 's', 'h', '^', '*'};
refD = str2num(refD{1});
axes{2} = axNames{1};
%% Choose Large Meta Folder
if listing(3).name + "" == ".DS_Store"
    listing = listing([1,2,4:end]);
end

for ii = 3:length(listing)
    subFolder(ii-2).subfolder = listing(ii).name;
    files = dir(fullfile(myDir, listing(ii).name, '*.csv'));
    for j = length(files):-1:1
        if lower(extractBetween(files(j).name + "    ", 1, 4)) == "test"
            files = [files(1:j-1); files(j+1:end)];
        end
    end
    fileList(ii-2).files = files;
end

timeInfo = floor(clock);
timeInfo = "[" + timeInfo(2) + "-" + timeInfo(3) + "] ";

for i = 1:length(readXValues)
    readX = lower(readXValues(i));
    axes{1} = axNames{i + 1};
    switch readX
        case "linear"
            refDist = refD;
            dirName = dName + " (linear)";
        case "log"
            refDist = log2(refD);
            dirName = dName + " (log)";
        case "distance"
            refDist = 1.4 * tan(8 * pi/180) / tan(refD * pi/180);
            dirName = dName + " (distance)";
        case "absolute value"
            refDist = abs(refD);
            dirName = dName + " (abs value)";
        otherwise
            refDist = refD;
            dirName = dName;
    end

    
    %% Sort Through Data
    masterAngles = [];
    for k = 1:length(fileList)
        data=[];
        RT=[];
        
        folderPath = fullfile(listing(k+2).folder, listing(k+2).name);
        addpath(folderPath);
        for ii = 1:length(fileList(k).files)
            file = fileList(k).files(ii).name;
            fprintf(1, 'Now Reading %s\n' , fileList(k).files(ii).name);
            data = table2array(readtable(fileList(k).files(ii).name));
            dist = data(:,2);
            correct = data(:,1);
            angles = unique(dist);
            RT = data(:,3);
            idn = find(correct == 0);
            RT(idn) = 0;
            masterAngles = [masterAngles; angles];
            masterAngles = unique(masterAngles);
            for jj = 1:length(angles)
                idx = find(dist == angles(jj));
                RT_IDX = RT(idx);
                RT_IDX = RT_IDX(RT_IDX~=0);
                correct_IDX = correct(idx);
                angleRT_Raw(k).protocol(ii).subject(jj).data = RT(idx);
                angleRT_Incorrect(k).protocol(ii).subject(jj).data = sum(correct_IDX(:) == 0);
                angleRT_IncorrectPerc(k).protocol(ii).subject(jj).data = sum(correct_IDX(:) == 0)/...
                    length(RT_IDX);
                RT_IDX = RT_IDX(RT_IDX~=0);
                [RT_IDX_RMO, TF] = rmoutliers(RT_IDX, 'quartiles');
                angleRT_RMO(k).protocol(ii).subject(jj).data = RT_IDX_RMO;
                angleRT_outlier(k).protocol(ii).subject(jj).data = sum(TF);
                angleRT_Mean(k).protocol(ii).subject(jj).data = mean(RT_IDX_RMO);
                angleRT_StdErr(k).protocol(ii).subject(jj).data = std(RT_IDX_RMO)/...
                    sqrt(length(RT_IDX_RMO));
            end
        end    
    end

    %% Hypothesis Testing/Error Analysis
    [incorrectHypArray] = hypothesisTesting_v3(fileList, listing,...
        angleRT_Raw, masterAngles);
    
    %% Normalize Data
    for ii = 1: length(fileList)
        data=[];
        RT=[];
        
        protocolRT_allSub(ii).data =[];
        protocolStd_allSub(ii).data = [];
        for jj = 1:length(fileList(ii).files)
            protocolRT_allSub(ii).data = [protocolRT_allSub(ii).data, angleRT_Mean(ii).protocol(jj).subject.data];
            protocolStd_allSub(ii).data = [protocolStd_allSub(ii).data, angleRT_StdErr(ii).protocol(jj).subject.data];
            
        end 
    
        ProtocolRT_Mean(ii).data = sum(protocolRT_allSub(ii).data./protocolStd_allSub(ii).data)/sum(1./protocolStd_allSub(ii).data);  
    
        
        for jj = 1:length(fileList(ii).files)
            data = table2array(readtable(fileList(ii).files(jj).name));
            dist = data(:,2);
            angles = unique(dist);
            protocolRT_indvSub(ii).subject(jj).data = [];
            protocolStd_indvSub(ii).subject(jj).data= [];
            for k = 1:length(angles)
            protocolRT_indvSub(ii).subject(jj).data = [protocolRT_indvSub(ii).subject(jj).data, angleRT_Mean(ii).protocol(jj).subject(k).data];
            protocolStd_indvSub(ii).subject(jj).data = [protocolStd_indvSub(ii).subject(jj).data, angleRT_StdErr(ii).protocol(jj).subject(k).data];
            end
            
        end 
    
            
            for jj = 1:length(fileList(ii).files)
                if ismember(0, protocolStd_indvSub(ii).subject(jj).data)
                    disp("File " + fileList(ii).files(jj).name + " is bugged.");
                    keyboard;
                end
                ProtocolRTind_Mean(ii).subject(jj).data = sum(protocolRT_indvSub(ii).subject(jj).data./protocolStd_indvSub(ii).subject(jj).data)/sum(1./protocolStd_indvSub(ii).subject(jj).data);  
                data = table2array(readtable(fileList(ii).files(jj).name));
                dist = data(:,2);
                angles = unique(dist);
                
                
            for k = 1:length(angles)
                angleRT_Norm(ii).protocol(jj).subject(k).data = angleRT_Mean(ii).protocol(jj).subject(k).data - ProtocolRTind_Mean(ii).subject(jj).data + ProtocolRT_Mean(ii).data;
            end
        end
    end
    
    %% Aggregate Analysis
    masterAngles = [];
    handles = [];
    for k = 1:length(fileList)
        data=[];
        RT=[];
       folderPath = fullfile(listing(k+2).folder, listing(k+2).name);
       addpath(folderPath);
       clear angles;
       clear masterAngles;
       for ii = 1:length(fileList(k).files)
           fprintf(1, 'Now Reading %s\n' , fileList(k).files(ii).name);
            data = table2array(readtable(fileList(k).files(ii).name));
            dist = data(:,2);
            angles = unique(dist);
          
            masterAngles = [angles];
            masterAngles = unique(masterAngles);
            
            
            for jj = 1:length(angles)
                idx = find(masterAngles == angles(jj));
                aggregateMeans(ii, idx, k) = angleRT_Norm(k).protocol(ii).subject(jj).data;
                aggregateSTDE(ii,idx,k) = angleRT_StdErr(k).protocol(ii).subject(jj).data;
            end
       end
    end 
    % aggregateMeans(find(incorrectHypArray >= 0.05 & incorrectHypArray <= 1)) = NaN;
    % aggregateSTDE(find(incorrectHypArray >= 0.05 & incorrectHypArray <= 1)) = NaN;
    aggregateMeans(aggregateMeans == 0) = NaN;
    aggregateSTDE(aggregateSTDE == 0) = NaN;
    
    for k = 1:length(fileList)
        data=[];
        RT=[];
           for ii = 1:length(fileList(k).files)
           fprintf(1, 'Now Reading %s\n' , fileList(k).files(ii).name);
            data = table2array(readtable(fileList(k).files(ii).name));
            dist = data(:,2);
            angles = unique(dist);
            
            masterAngles = [angles];
            masterAngles = unique(masterAngles);
           end
        for jj = 1:length(masterAngles)
            protocolWeightedMean(k, jj) = sum(aggregateMeans(:,jj,k)./aggregateSTDE(:,jj,k), ...
                'omitnan')/sum(1./aggregateSTDE(:,jj,k) , 'omitnan');
            protocolStdErr(k,jj) = std(aggregateMeans(:,jj,k)/...
                sqrt(length(aggregateMeans(:,jj,k))),...
                'omitnan').* (length(angles)./(length(angles)-1));
        end
    end
    for k = 1:length(fileList)
        data=[];
        RT=[];
           for ii = 1:length(fileList(k).files)
           fprintf(1, 'Now Reading %s\n' , fileList(k).files(ii).name);
            data = table2array(readtable(fileList(k).files(ii).name));
            dist = data(:,2);
            angles = unique(dist);
          
            masterAngles = [angles];
            masterAngles = unique(masterAngles);
           end
    
    
        protocolChiFitPos(k) = chiSquareFunction(masterAngles(masterAngles >= refDist)...
            ,protocolWeightedMean(k,find(masterAngles >= refDist))...
            ,protocolStdErr(k,find(masterAngles >= refDist)));
        protocolChiFitNeg(k) = chiSquareFunction(masterAngles(masterAngles <= refDist)...
            ,protocolWeightedMean(k,find(masterAngles <= refDist))...
            ,protocolStdErr(k,find(masterAngles <= refDist)));
    end
    
    %%  Aggregate Plotting
    figure();
    aggregatePlotting_v3(fileList, masterAngles, protocolWeightedMean, colors,...
        protocolStdErr,protocolChiFitPos, protocolChiFitNeg, linestyle,protocolNames, S,...
        axes, refDist, '');
end
