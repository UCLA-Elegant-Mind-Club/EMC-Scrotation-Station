currDir = fullfile(fileparts(pwd), 'Data', 'temp');
destination = uigetdir(fileparts(currDir), 'Choose folder to add shortcuts to.');
while true
    currDir = uigetdir(fileparts(currDir), 'Choose target folder.');
    if currDir + "" == "0"; break; end
    path = strsplit(currDir, filesep);
    index = find(path + "" == "EMC-Scrotation-Station");
    name = inputdlg('What to name shortcut file: ', 'Shortcut Name', 1, path(end));
    if length(name) == 0; continue; end
    fileID = fopen(fullfile(destination, name{1} + " - Shortcut.txt"),'w');
    fprintf(fileID, '%s', join(path(index + 1 : end) + "",'\'));
    fclose(fileID);
end