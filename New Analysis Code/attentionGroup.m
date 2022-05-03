subFolder = uigetdir(fullfile(fileparts(pwd), 'Data'));
fileList = dir(fullfile(subFolder, '*.csv'));
for fileNum = 1:length(fileList)
    %remakeFile(subFolder, fileList(fileNum).name, 5, 2, 3, 4, 6, 1);
    constantEcc(subFolder, fileList(fileNum).name, 5, 2, 3, 4, 6, 1);
end

function [] = remakeFile(folder, fileName, correctCol, dirCol, eccCol, timeCol, sizeCol, targetCol)
    tab = readtable(fullfile(folder, fileName));
    for row = 1:height(tab)
        data = table2cell(tab(row, :));
        size = data{sizeCol};
        dir = data{dirCol};
        data = [data([correctCol, eccCol, timeCol]), 0];
        data{2} = data{2} * (dir - 1);
        data{3} = data{3} * 1000;
        data = cell2table(data, 'VariableNames', {'Correct', 'Size', 'RT', 'Target'});
        mkdir(folder + "-size " + size);
        writetable(data, fullfile(folder + "-size " + size, fileName), 'WriteMode','append');
    end
end

function [] = constantEcc(folder, fileName, correctCol, dirCol, eccCol, timeCol, sizeCol, targetCol)
    mkdir(folder + " - reorganized");
    tab = readtable(fullfile(folder, fileName));
    for row = 1:height(tab)
        data = table2cell(tab(row, :));
        data = [data([correctCol, sizeCol, timeCol]), 0];
        data{3} = data{3} * 1000;
        data = cell2table(data, 'VariableNames', {'Correct', 'Size', 'RT', 'Target'});
        writetable(data, fullfile(folder + " - reorganized", fileName), 'WriteMode','append');
    end
end