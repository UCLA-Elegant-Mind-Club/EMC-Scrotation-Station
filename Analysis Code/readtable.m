function t = readtable(filename, varargin)
    global readX;
    [varargin{1:2:end}] = convertStringsToChars(varargin{1:2:end});
    names = varargin(1:2:end);
    try
        if any(strcmpi(names,"Format"))
            t = matlab.io.internal.legacyReadtable(filename,varargin);
        else
            func = matlab.io.internal.functions.FunctionStore.getFunctionByName('readtable');
            C = onCleanup(@()func.WorkSheet.clear());
            t = func.validateAndExecute(filename,varargin{:});
        end
    catch ME
        throw(ME)
    end

    matrix = table2array(t);
    if ~exist("readX") || length(readX) == 0
        return;
    elseif readX + "" == "log"
        matrix(:, 2) = log(matrix(:, 2));
    elseif readX + "" == "distance"
        matrix(:, 2) = 1.4 * tan(8 * pi/180) ./ tan(matrix(:, 2) * pi/180);
    end
    t = array2table(matrix, "VariableNames", t.Properties.VariableNames);
end