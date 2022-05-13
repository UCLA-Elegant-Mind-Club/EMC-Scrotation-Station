function listing = dir(name)
    parentDir = fileparts(pwd);
    listing = builtin('dir', name);
    for i = length(listing):-1:3
        if listing(i).name + "" == ".DS_Store"
            listing = [listing(1:i-1); listing(i+1:end)];
        end
        len = length(listing(i).name);
        if len < 14; continue; end
        if extractBetween(listing(i).name, len - 13, len) == "- Shortcut.txt"
            fileID = fopen(fullfile(listing(i).folder, listing(i).name), 'r');
            pathString = textscan(fileID,'%s','Delimiter','\');
            pathString = fullfile(parentDir, join([pathString{:} + ""], filesep));
            [path, file] = fileparts(pathString);
            listing(i) = struct('name', file, 'folder', path, 'date', listing(i).date, ...
                'bytes', 0, 'isdir', 1, 'datenum', listing(i).datenum);
        end
    end
end