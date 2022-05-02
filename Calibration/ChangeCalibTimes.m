monitorLabel = 'Mon 1';
newTime = 91.54;

calibFile = 'monitors.csv';
monTable = readtable(calibFile,'Delimiter','comma');
monitorNum = find([monTable{:,1} + ""] == monitorLabel + "");
oldTime = monTable{monitorNum, 21};
monTable{monitorNum, 21} = newTime;

dataFolder = rmDSStore(dir(fullfile(fileparts(pwd), 'Data')));
for group = 3:length(dataFolder)
    groupFolder = rmDSStore(dir(fullfile(dataFolder(group).folder, dataFolder(group).name)));
    for protocol = 3:length(groupFolder)
        protocolFolder = dir(fullfile(groupFolder(protocol).folder, groupFolder(protocol).name, "*[Mon " + monitorNum + "].csv"));
        for file = 1:length(protocolFolder)
            try
                fileName = fullfile(protocolFolder(file).folder, protocolFolder(file).name);
                table = readtable(fileName);
                table{:,3} = table{:, 3} - oldTime + newTime;
                writetable(table, fileName);
            catch
                disp("Failed to modify time for file: " + fileName);
            end
        end
    end
end
writetable(monTable, calibFile);

function folder = rmDSStore(folder)
    if folder(3).name + "" == ".DSStore"
        folder = folder([1,2,4:end]);
    end
end