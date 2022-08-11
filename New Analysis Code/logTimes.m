myDir = uigetdir; %gets directory
listing = dir(myDir);
mkdir(myDir + " distance");
for folder = 3:length(listing)
    mkdir(fullfile(myDir + " half", listing(folder).name));
    sublisting = dir(fullfile(myDir, listing(folder).name, '*.csv'));
    for file = 3:length(sublisting)
        table = readtable(fullfile(myDir, listing(folder).name, sublisting(file).name));
        matrix = table2array(table);
        matrix(:, 2) = (matrix(:, 2))/2;
        table = array2table(matrix, "VariableNames", table.Properties.VariableNames);
        writetable(table, fullfile(myDir + " half", listing(folder).name, sublisting(file).name));
    end
end