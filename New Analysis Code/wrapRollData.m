folderName = uigetdir(fullfile(fileparts(pwd), 'Data'));
folder = dir(folderName);
for subNum = 3:length(folder)
    subFolder = fullfile(folderName,folder(subNum).name);
    fileList = dir(fullfile(subFolder, '*.csv'));
    for fileNum = 1:length(fileList)
        fileName = fullfile(subFolder, fileList(fileNum).name);
        wrapData(fileName, 2, 180, -180);
    end
end

function [] = wrapData(fileName, xCol, input, output)
    table = readtable(fileName);
    matrix = table2array(table);
    if height(matrix) <= 0 || ismember(output, matrix(:,xCol))
        return;
    end
    for i = 1:height(matrix)
        if matrix(i, xCol) == input
            row = matrix(i, :);
            row(xCol) = output;
            dlmwrite(fileName, row, '-append')
        end
    end
end
