folderName = fullfile(fileparts(pwd), 'Data', 'Scaling plus Rotation');
folder = dir(folderName);
if folder(3).name + "" == ".DS_Store"; folder = folder([1,2,4:end]); end
for i = 4:length(folder)
    test = folder(i);
    rmdir(fullfile(folderName, folder(i).name), 's');
end
subFolder = fullfile(folderName,folder(3).name);
fileList = dir(fullfile(subFolder, '*.csv'));
for fileNum = 1:length(fileList)
    if extractBetween(fileList(fileNum).name, 1, 4) ~= "Test"
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