classdef readXControl
    methods(Static)
        function exists = checkReadX(readX)
            exists = exist("readX", 'var') && ~isempty(readX);
        end

        function matrix = processMatrix(matrix)
            global readX;
            if ~readXControl.checkReadX(readX); return;
            elseif readX + "" == "log"
                matrix(:, 2) = log2(matrix(:, 2));
            elseif readX + "" == "distance"
                matrix(:, 2) = 1.4 * tan(8 * pi/180) ./ tan(matrix(:, 2) * pi/180);
            elseif readX + "" == "absolute value"
                matrix(:, 2) = abs(matrix(:,2));
                copy = matrix;
                copy(:,2) = -copy(:,2);
                matrix = [matrix; copy];
            end
        end

        function processXTicks()
            global readX;
            if ~readXControl.checkReadX(readX); return;
            elseif readX + "" == "log"
                ticks = xticks;
                ticks = ticks(mod(ticks, 1) == 0);
                xticks(ticks);
                xticklabels(pow2(ticks));
            end
        end
    end
end