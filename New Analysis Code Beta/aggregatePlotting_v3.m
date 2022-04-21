function [] = aggregatePlotting_v3(fileList, masterAngles, protocolWeightedMean, colors,...
    protocolStdErr,protocolChiFitPos, protocolChiFitNeg, linestyle,protocolNames, S,...
    axes, refDist, saveDir)

for ii = 1:length(fileList)
    data = table2array(readtable(fileList(ii).files(1).name));
    dist = data(:,2);
    angles = unique(dist);
    
    masterAngles = angles;
    scatter(masterAngles, protocolWeightedMean(ii,1:length(angles)), S{ii}, 'filled', 'MarkerFaceColor',...
       colors{ii}, 'MarkerEdgeColor', colors{ii}, 'LineWidth', 1);
   S{ii}
    hold on;
    errorbar(masterAngles, protocolWeightedMean(ii,1:length(angles)),...
        protocolStdErr(ii,1:length(angles)), S{ii}, 'Color', colors{ii}, 'LineWidth', 1, 'Capsize', 0);
    hold on;
    plot(masterAngles(masterAngles>=refDist),masterAngles(masterAngles>=refDist)*...
        protocolChiFitPos(ii).slope + protocolChiFitPos(ii).intercept, 'LineWidth', 1,...
        'LineStyle', linestyle{ii}, 'color', colors{ii});
    hold on;
    plot(masterAngles(masterAngles<=refDist),masterAngles(masterAngles<=refDist)*...
        protocolChiFitNeg(ii).slope + protocolChiFitNeg(ii).intercept, 'LineWidth', 1,...
        'LineStyle', linestyle{ii}, 'color', colors{ii});
    hold on;
    xlabel(axes{1});
    ylabel(axes{2});
    box on;
    
    set(gcf, 'Position',  [20, 20, 700, 800]);
    h(ii) = plot(2000, 'LineWidth', 1, 'MarkerFaceColor', colors{ii}, 'color', colors{ii}, ...
     'LineStyle', linestyle{ii}, 'MarkerSize', 5, 'DisplayName', protocolNames{ii},...
     'Marker', S{ii}); hold on;
    legend(h, 'Location', 'Northeastoutside', 'AutoUpdate', 'off');
    xRange = max(masterAngles) - min(masterAngles);
    xlim([min(masterAngles) - xRange * 0.1, max(masterAngles) + xRange * 0.1]);
    ylim([300 900]);
    set(gca, 'fontsize', 14);
    %xticks([-180:60:180]);
    saveas(gcf, fullfile(pwd, saveDir, strcat('Aggregate', '.png')));
end
