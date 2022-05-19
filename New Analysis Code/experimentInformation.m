function [folderName, axes, refDist, analysisTypes, dataDir, ...
    protOrder, protNames, colors, linestyles, markers] = experimentInformation()

    useTemplate = questdlg("Load fields from template csv/excel file?");
    switch useTemplate
        case 'Yes'; [file, path] = uigetfile("*.csv;*.xlsx", ...
                "Choose Analysis Template", "Templates");
        case 'No'; [file, path] = deal("Empty Analysis Template.xlsx", pwd);
        otherwise; file = 0;
    end
    if file + "" == "0"; fprintf("Analysis Canceled\n"); return
    else; fprintf("Reading template file: " + file + "\n");
        template = readtable(fullfile(path, file)); end
    
    format shortg;
    folderName = inputdlg('All analysis files will be organized into a folder with this name:', ...
        'Analysis Folder Name', [1 60], template{1,1});
    
    
    analysisTypes = ["Linear", "Log", "Distance", "Absolute Value"];
    axes = inputdlg([sprintf("(Leave x-axes blank to exclude analysis\n\nEnter y-axis label"), ...
        "Enter label for " + analysisTypes + " Analysis"], 'Axes Names', [1 60], [template{:,3}]);
    include = ~ismember(axes, '');
    axes = axes(include);
    analysisTypes = analysisTypes(include(2:end));
    
    refDist = inputdlg('Enter expected location of kink:', ...
        'Kink Location', [1 60], template{1,6} + "");
    
    dataDir = uigetdir(fullfile(fileparts(pwd), 'Data'), "Choose Group Data Folder that contains Protocols");
    dataDir = dir(dataDir);
    protNames = {dataDir(3:end).name};
    order = template{:, 8};
    order = order(~isnan(order));
    
    protOrder = zeros(length(protNames), 1);
    for start = 1:10:length(protNames)
        last = min(start + 9, length(protNames));
        message = sprintf("Found " + length(protNames) + " protocols. " + ...
            "Choose their order in legend (0 to exclude):\n\n" + protNames(start));
        protOrder(start:last) = str2double(inputdlg({message, protNames{start + 1:last}}, ...
            "Plotting Order", [1 60], [order(start:end); zeros(length(protNames), 1)] + ""));
    end
    newTemplate = cell2table(cell(0,width(template)), 'VariableNames', template.Properties.VariableNames);
    newProtNames = cell(0);
    for i = 1:max(protOrder)
        for j = 1:length(protOrder)
            if i == protOrder(j)
                if j > length(order)
                    row = repmat({''}, 1, width(template));
                    row{7} = protNames{j};
                    row{10} = '-';
                    newTemplate = [newTemplate; row];
                else
                    newTemplate = [newTemplate; table2cell(template(j,:))];
                end
                newProtNames = [newProtNames; protNames(j)];
                newDataDir(i,1) = dataDir(j+2);
            end
        end
    end
    dataDir = [dataDir(1:2); newDataDir];
    protNames = inputdlg(newProtNames, "Rename Protocols", [1 60], newTemplate{:,7});
    
    message = sprintf("Choose from these colors: gray, red, blue, light blue,maroon, black, green:\n\n");
    
    
    colors = inputdlg([{message + protNames(1)}; protNames(2:end)], ...
        'Choose plotting colors', [1 60], newTemplate{:,9});
    
    message = sprintf("Choose from these linestyles: ''-'' (solid) or ''--'' (dashed):\n\n");
    linestyles = inputdlg([{message + protNames(1)}; protNames(2:end)], ...
        'Choose line drawing styles', [1 60], newTemplate{:,10});
    
    message = sprintf("Choose from these markers: 'o', ''d'', ''s'', ''h'', ''^'', ''*'':\n\n");
    markers = inputdlg([{message + protNames(1)}; protNames(2:end)], ...
        'Choose marker plotting shapes', [1 60], [{'o', 'd', 's', 'h', '^', '*'}, repmat({''}, 1, length(protNames))]);
end