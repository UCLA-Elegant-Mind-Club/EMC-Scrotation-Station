folderName = fullfile(fileparts(pwd), 'Data', 'Scaling plus Rotation');
folder = dir(folderName);
for i = 4:length(folder)
    test = folder(i);
    rmdir(fullfile(folderName, folder(i).name), 's');
end
subFolder = fullfile(folderName,folder(3).name);
fileList = dir(fullfile(subFolder, '*.csv'));
for fileNum = 1:length(fileList)
    if extractBetween(fileList(fileNum).name, 1, 4) ~= "Test"
        sepData(subFolder, fileList(fileNum).name, 2, 1, [4, 8, 16], 2, 'scale');
        sepData(subFolder, fileList(fileNum).name, 2, 2, [-180:30:180], 1, 'roll');
    end
end

function [] = sepData(folder, fileName, xCol, xSepIndex, xSepVals, xWriteIndex, folderSuffix)
    table = readtable(fullfile(folder, fileName));
    allXVals = extractBetween(table{:, xCol} + "", "(", ")");
    for i = xSepVals(:).'
        data = [];
        for j = 1:height(table)
            xVal = str2num(allXVals(j));
            if xVal(xSepIndex) == i
                data = [data; [table{j, 1}, xVal(xWriteIndex), table{j, 3:end}]];
            end
        end
        tab = array2table(data, 'VariableNames', table.Properties.VariableNames);
        mkdir(folder + "-" + folderSuffix + " " + i);
        writetable(tab, fullfile(folder + "-" + folderSuffix + " " + i, fileName));
    end
end