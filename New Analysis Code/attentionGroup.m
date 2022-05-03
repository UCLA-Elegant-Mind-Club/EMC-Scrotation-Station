subFolder = uigetdir(fullfile(fileparts(pwd), 'Data'));
fileList = dir(fullfile(subFolder, '*.csv'));
for fileNum = 1:length(fileList)
    remakeFile(subFolder, fileList(fileNum).name, 5, 2, 3, 4, 6, 1);
end

function [] = remakeFile(folder, fileName, correctCol, dirCol, eccCol, timeCol, sizeCol, targetCol)
    table = readtable(fullfile(folder, fileName));
    for row = 1:height(table)
        data = table{row, :};
        size = str2num(data(sizeCol));
        dir = data(dirCol);
        data = data([correctCol, eccCol, timeCol, targetCol]);
        data(2) = data(2) * (dir - 1);
        mkdir(folder + "-size " + size);
        writematrix(data, fullfile(folder + "-size " + size, fileName), 'WriteMode','append');
    end
end