dirName = "C:\Users\emban\Documents\Elegant Mind Research\Rotation Analysis\Remote Senior Data";
folderName = "For analysis";
folderPath = fullfile(dirName, folderName);
newFolderPath = folderPath + " - Shifted";
folder = dir(folderPath);
for subNum = 3:length(folder)
    subFolder = fullfile(folderPath,folder(subNum).name);
    mkdir(newFolderPath, folder(subNum).name);
    fileList = dir(fullfile(subFolder, '*.csv'));
    for fileNum = 1:length(fileList)
        fileName = fullfile(subFolder, fileList(fileNum).name);
        table = shiftData(fileName, 3, -40);
        writetable(table, fullfile(newFolderPath, ...
            folder(subNum).name, fileList(fileNum).name));
    end
end

function [table] = shiftData(fileName, yCol, shift)
    table = readtable(fileName);
    matrix = table2array(table);
    matrix(:, yCol) = matrix(:, yCol) + shift;
    table = array2table(matrix,"VariableNames",table.Properties.VariableNames);
end
