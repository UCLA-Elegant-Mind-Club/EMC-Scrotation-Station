folderName = uigetdir;
folder = dir(folderName);
for subNum = 3:length(folder)
    subFolder = fullfile(folderName,folder(subNum).name);
    fileList = dir(fullfile(subFolder, '*.csv'));
    for fileNum = 1:length(fileList)
        sepData(subFolder, fileList(fileNum).name, 2);
    end
end

function [] = sepData(folder, fileName, xCol)
    table = readtable(fullfile(folder, fileName));
    allXVals = extractBetween(table{:, xCol} + "", "(", ")");
    for i = [4,8,16]
        data = [];
        for j = 1:height(table)
            xVal = str2num(allXVals(j));
            if xVal(1) == i
                data = [data; [table{j, 1}, xVal(2), table{j, 3:end}]];
            end
        end
        tab = array2table(data, 'VariableNames', table.Properties.VariableNames);
        mkdir(folder + "-scale " + i);
        writetable(tab, fullfile(folder + "-scale " + i, fileName));
    end
end