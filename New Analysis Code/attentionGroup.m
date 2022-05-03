subFolder = uigetdir(fullfile(fileparts(pwd), 'Data'));
fileList = dir(fullfile(subFolder, '*.csv'));
for fileNum = 1:length(fileList)
    fileName = fullfile(subFolder, fileList(fileNum).name);
    remakeFile(fileName, 2, 180, -180);
end

function [] = remakeFile(fileName, correctCol, dirCol, eccCol, sizeCol, targetCol)
    table = readtable(fileName);
    allSizes = [];
    for row = 1:height(table)
        size = str2num(table(row, sizeCol));
        allSizes = unique[allSizes; size];
        if xVal(xSepIndex) == i
            data = [data; [table{j, 1}, xVal(xWriteIndex), table{j, 3:end}]];
        end
        end
        tab = array2table(data, 'VariableNames', table.Properties.VariableNames);
        mkdir(folder + "-" + folderSuffix + " " + i);
        writetable(tab, fullfile(folder + "-" + folderSuffix + " " + i, fileName));
    end
end