close all;
%% Setup
numProtocols = 6;
% Make sure to have 2 yTickLabels per protocol
yTickLabels = {'Counterclockwise', 'Clockwise', 'Leftwards', 'Rightwards', 'Downwards', 'Upwards', ...
    'Counterclockwise', 'Clockwise', 'Counterclockwise', 'Clockwise', 'Counterclockwise', 'Clockwise'};
protocolMarkers = ['o', 'd', 's', 'h', '^', '*'];
groupColors = struct('A', [0.8 0.5 0], 'B', [0 0.75 0.1], 'C', [0 0 0.95], 'D', [0.6 0 0.75], 'Aggregate', 'red');
markerSize = 5;
table = readtable("Rotation Parameters.csv");

fig = figure();
hold on;
set(gca, 'XGrid', 'on');

graphingSlopes = false;
if graphingSlopes
    cols = [4, 11];
    xBounds = [-0.5 4];
    title("Comparison of Slopes between Experimental Group");
    xlabel("Slope (ms/°)");
    %for slopes, negate left slopes
    process = @(right, row, data) (right * 2 - 1) * data{row, cols(right + 1)};
else
    cols = [6, 13];
    xBounds = [375 625];
    title("Comparison of Intercepts between Experimental Group");
    xlabel("Intercept (ms)");
    %for intercepts, treat normally
    process = @(right, row, data) data{row, cols(right + 1)};
end

%% Draw points in order in table

data = table2cell(table);
protocols = cell(1,numProtocols);
yPos = -0.1;
borderPos = zeros(numProtocols + 1,1);
protocolNum = 0; row = 0;
backtrack = true; protocolStart = 1;
while row <= height(data)
    row = row + 1;a
    if row == height(data) + 1 || strlength(data{row,1}) > 0
        protocolNum = protocolNum + 1;
        if backtrack    % continue and draw left side data
            if row <= height(data); protocols{ceil(protocolNum/2)} = data{row,1}; end
            backtrack = false;
            protocolStart = row;
            line(xBounds, [yPos + 0.1, yPos + 0.1], 'color', 'black', ...
                'HandleVisibility','off', 'LineWidth', 0.15);
        else            % go back and draw in right side data
            backtrack = true;
            row = protocolStart;
            line(xBounds, [yPos + 0.1, yPos + 0.1], 'color', [0.1 0.1 0.1], ...
                'HandleVisibility','off', 'LineWidth', 0.15, 'LineStyle', '--');
        end
        borderPos(protocolNum) = yPos + 0.1;
        yPos = yPos + 0.3;
    end
    if row <= height(data)
        color = groupColors.(data{row, 2});
        pointData = process(backtrack, row, data);
        if(data{row,2} == "Aggregate")
            mSize = markerSize + 5;
            markerType = 'pentagram';
            edgeColor = 'black';
        else
            markerType = protocolMarkers(ceil(protocolNum/2));
            mSize = markerSize;
            edgeColor = color;
        end
        errorbar(pointData, yPos, data{row, cols(backtrack + 1) + 1}, 'horizontal', ...
            'Marker', markerType, 'Color', edgeColor, 'MarkerFaceColor', color, ...
            'MarkerSize', mSize, 'LineStyle','none', 'CapSize', 0, 'HandleVisibility','off');
        yPos = yPos + 0.1;
    end
end
yPos = yPos - 0.2;
fig.Position = [250 -100 800 1000];
currPos = fig.CurrentAxes.Position;
shift = 0.1;
set(gca, 'Position', [currPos(1) + shift, currPos(2), currPos(3) - shift, currPos(4)]);
set(gca, 'YDir','reverse')

%% Create legend
groups = fieldnames(groupColors);
markerType = ['oooop'];
for i = 1:length(groups)
    color = groupColors.(groups{i});
    if groups(i) == "Aggregate"; edgeColor = 'black';
    else; edgeColor = color; groups{i} = "Group " + groups{i}; end
    legendPoints(i) = scatter(xBounds(1) - xBounds(2), i, 'filled', markerType(i), ...
        'MarkerEdgeColor', edgeColor, 'MarkerFaceColor', color, 'HandleVisibility','off');
end
leg = legend(legendPoints, groups, 'Location', 'northeast');
legend Box on;
leg.AutoUpdate = false;

%% Setup y axis (Run after resizing)
axis([xBounds, 0 yPos])
line([0 0], [0 yPos], 'Color', [0.4 0.4 0.4]);

try delete(yLbl); catch; end
yLbl = ylabel("Protocol");
set(gca,'YTickLabel', yTickLabels);
set(gca,'YTick', (borderPos(2:end) + borderPos(1:end-1))/2);

try delete(protocolText); catch; end
bufferDist = xBounds(1) - yLbl.Position(1);
protocolText = text(ones(length(protocols), 1) * yLbl.Position(1) - bufferDist * 0.1, borderPos(2:2:end), protocols,...
    'VerticalAlignment','middle','HorizontalAlignment','center');
set(protocolText,'Rotation',90);
%yLbl.Position(1) = yLbl.Position(1) - 10;
yLbl.Position(1) = yLbl.Position(1) - bufferDist * 0.2;
refresh;
