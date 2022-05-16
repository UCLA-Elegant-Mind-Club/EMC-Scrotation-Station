function [incorrectHypArray] = hypothesisTesting_v3(fileList, listing,...
    angleRT_Raw, masterAngles)
numOptions = 1/3;
for k = 1:length(fileList)
    folderPath = fullfile(listing(k+2).folder, listing(k+2).name);
    addpath(folderPath);
    for ii = 1:length(fileList(k).files)
        data = table2array(readtable(fullfile(fileList(k).files(ii).folder, ...
            fileList(k).files(ii).name)));
        dist = data(:,2);
        angles = unique(dist);
        for jj = 1:length(angleRT_Raw(k).protocol(ii).subject)
            idx = find(masterAngles == angles(jj));
            testingArray = logical([angleRT_Raw(k).protocol(ii).subject(jj).data]);
            hypothesisArray(ii, idx, k) = sum(testingArray)/length(testingArray);
            [~, p] = ttest(logical([angleRT_Raw(k).protocol(ii).subject(jj).data]),...
                numOptions, 'Tail', 'right');
            idx = find(masterAngles == angles(jj));
            incorrectHypArray(ii, idx, k) = p;
        end
    end
end
end