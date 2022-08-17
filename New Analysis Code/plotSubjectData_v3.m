function [outputParamStats, protocolOutput, h] = plotSubjectData_v3(fileList,listing,...
    angleRT_Mean, angleRT_StdErr, myDir, linestyle, protocolNames, S, axes, colors,...
    masterAngles, refDist, plotSeparate, saveDir)
close all
for k = 1:length(fileList)
    %mkdir(protocolNames{k});
    for ii = 1:length(fileList(k).files)
        data = table2array(readtable(fullfile(fileList(k).files(ii).folder, ...
            fileList(k).files(ii).name)));
        dist = data(:,2);
        angles = unique(dist);
        
     
        
        masterAngles = [masterAngles; angles];
        masterAngles = unique(masterAngles);
        %{
        if strcmp(plotSeparate, 'True')
            figure((k-1)*length(fileList(k).files) + ii);
        elseif strcmp(plotSeparate, 'False')
            figure(ii);
        end
        hold on;
        try
        scatter(angles, [angleRT_Mean(k).protocol(ii).subject.data], S{k}, 'filled', ...
            'LineWidth', 1, 'MarkerFaceColor',colors{k}, 'MarkerEdgeColor', colors{k});
        catch
            sprintf("error");
        end
        hold on;
        errorbar(angles, [angleRT_Mean(k).protocol(ii).subject.data],...
            [angleRT_StdErr(k).protocol(ii).subject.data], S{k}, 'Color', colors{k},...
            'LineWidth', 1, 'CapSize', 0);
        addpath(myDir, '\..\..');
        %}
        fprintf(k + ", " + ii);
        PosChiSquare = chiSquareFunction(angles(angles >= refDist), ...
            [angleRT_Mean(k).protocol(ii).subject(find(angles >=refDist)).data],...
            [angleRT_StdErr(k).protocol(ii).subject(find(angles>=refDist)).data]);
        NegChiSquare = chiSquareFunction(angles(angles <= refDist), ...
            [angleRT_Mean(k).protocol(ii).subject(find(angles <=refDist)).data],...
            [angleRT_StdErr(k).protocol(ii).subject(find(angles<=refDist)).data]);

        %{
        plot(angles(angles >= refDist), angles(angles >= refDist)*PosChiSquare.slope +...
            PosChiSquare.intercept, 'LineWidth', 1, 'LineStyle', linestyle{k},...
            'color', colors{k});
        hold on;
        plot(angles(angles <= refDist), angles(angles <= refDist)*NegChiSquare.slope +...
            NegChiSquare.intercept, 'LineWidth', 1, 'LineStyle', linestyle{k},...
            'color', colors{k});
        xlabel(axes{1});
        ylabel(axes{2});
        
        box on;
        
        set(gcf, 'Position',  [20, 20, 600, 800]);
        h = plot(2000, 'LineWidth', 1, 'MarkerFaceColor', colors{k}, 'color', colors{k}, ...
          'LineStyle', linestyle{k}, 'MarkerSize', 5, 'DisplayName', protocolNames{k},...
          'Marker', S{k}); hold on;
        if strcmp(plotSeparate, 'True')
            legend(h, 'Location', 'Northeastoutside');
        end
        xRange = masterAngles(end) - masterAngles(1);
        xlim([(masterAngles(1)- xRange * 0.1) (masterAngles(end)+ xRange * 0.1)]);
        ylim([300 900]);
        set(gca, 'fontsize', 14);
        %xticks([-180:30:180]);
        if strcmp(plotSeparate, 'True')
            title(strcat('Subject', {' '}, string(ii), {' '}, 'B/BBB'));
            saveas(gcf, fullfile(pwd, saveDir, protocolNames{k},strcat('Subject', '_',...
                string(ii),{' '},string(protocolNames{k}), '.png')));
        elseif strcmp(plotSeparate, 'False')
            title(strcat('Subject', {' '}, string(ii)));
        end
        %}

        outputParamStats(k).slopePos(ii) = PosChiSquare.slope;
        outputParamStats(k).slopePosErr(ii) = PosChiSquare.slopeErr;
        outputParamStats(k).slopeNeg(ii) = NegChiSquare.slope;
        outputParamStats(k).slopeNegErr(ii) = NegChiSquare.slopeErr;
        outputParamStats(k).interceptPos(ii) = PosChiSquare.intercept;
        outputParamStats(k).interceptPosErr(ii) = PosChiSquare.interceptErr;
        outputParamStats(k).interceptNeg(ii) = NegChiSquare.intercept;
        outputParamStats(k).interceptNegErr(ii) = NegChiSquare.interceptErr;
        outputParamStats(k).chi2valPos(ii) = PosChiSquare.chi2Val;
        outputParamStats(k).redChi2Pos(ii) = PosChiSquare.redChiSquare;
        outputParamStats(k).chi2valNeg(ii) = NegChiSquare.chi2Val;
        outputParamStats(k).redChi2Neg(ii) = NegChiSquare.redChiSquare;
        outputParamStats(k).R_Pos(ii) = PosChiSquare.R;
        outputParamStats(k).R_Neg(ii) = NegChiSquare.R;
    end
end
%{
if strcmp(plotSeparate, 'False')
    for k = 1:length(fileList)
        %mkdir(protocolNames{k});
        for ii = 1:length(fileList(k).files)
            figure(ii);
            h(k) = plot(2000, 'LineWidth', 1, 'MarkerFaceColor', colors{k}, 'color', colors{k}, ...
             'LineStyle', linestyle{k}, 'MarkerSize', 5, 'DisplayName', protocolNames{k},...
             'Marker', S{k}); hold on;
        H(k) = legend(h, 'Location', 'Northeastoutside');
        mkdir(fullfile(saveDir, "Separate Subject Plots"));
        saveas(gcf, fullfile(pwd, saveDir, 'Separate Subject Plots' ,strcat('Subject', '_',...
                string(ii), '.png')));
        end
    end
end
%}
for k = 1:length(fileList)
    outputParamStats(k).slopePos = [outputParamStats(k).slopePos]';
    outputParamStats(k).slopePosErr = [outputParamStats(k).slopePosErr]';
    outputParamStats(k).slopeNeg = [outputParamStats(k).slopeNeg]';
    outputParamStats(k).slopeNegErr = [outputParamStats(k).slopeNegErr]';
    outputParamStats(k).interceptPos = [outputParamStats(k).interceptPos]';
    outputParamStats(k).interceptPosErr = [outputParamStats(k).interceptPosErr]';
    outputParamStats(k).interceptNeg = [outputParamStats(k).interceptNeg]';
    outputParamStats(k).interceptNegErr = [outputParamStats(k).interceptNegErr]';
    outputParamStats(k).chi2valPos = [outputParamStats(k).chi2valPos]';
    outputParamStats(k).redChi2Pos = [outputParamStats(k).redChi2Pos]';
    outputParamStats(k).chi2valNeg = [outputParamStats(k).chi2valNeg]';
    outputParamStats(k).redChi2Neg = [outputParamStats(k).redChi2Neg]';
    outputParamStats(k).R_Pos = [outputParamStats(k).R_Pos]';
    outputParamStats(k).R_Neg = [outputParamStats(k).R_Neg]';
end

for ii = 1:length(protocolNames)
    protocolOutput(ii).table = struct2table(outputParamStats(ii));
end
h = 0;
end