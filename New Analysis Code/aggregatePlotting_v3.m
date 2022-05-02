function [] = aggregatePlotting_v3(fileList, masterAngles, protocolWeightedMean, colors,...
    protocolStdErr,protocolChiFitPos, protocolChiFitNeg, linestyle,protocolNames, S,...
    axes, refDist, saveDir)

allAngles = [];
for ii = 1:length(fileList)
    data = table2array(readtable(fileList(ii).files(1).name));
    dist = data(:,2);
    angles = unique(dist);

    allAngles = unique([allAngles; angles]);
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
    % Plot outside graph for legend
    h(ii) = plot(2000, 'LineWidth', 1, 'MarkerFaceColor', colors{ii}, 'color', colors{ii}, ...
        'LineStyle', linestyle{ii}, 'MarkerSize', 5, 'DisplayName', protocolNames{ii},...
        'Marker', S{ii}); hold on;
end

hold on;
xlabel(axes{1});
ylabel(axes{2});
box on;

set(gcf, 'Position',  [20, 20, 700, 800]);
legend(h, 'Location', 'Northeastoutside', 'AutoUpdate', 'off');
xRange = max(allAngles) - min(allAngles);
xlim([min(allAngles) - xRange * 0.1, max(allAngles) + xRange * 0.1]);
ylim([400 800]);
set(gca, 'fontsize', 14);
%xticks([-180:60:180]);
saveas(gcf, fullfile(pwd, saveDir, strcat('Aggregate', '.png')));
