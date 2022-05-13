function t = readtable(filename, varargin)
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

    try
        matrix = table2array(t);
        matrix = readXControl.processMatrix(matrix);
        t = array2table(matrix, "VariableNames", t.Properties.VariableNames);
    catch; end
end