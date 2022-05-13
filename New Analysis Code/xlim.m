function varargout = xlim(varargin)
    varargout = matlab.graphics.internal.ruler.rulerFunctions(mfilename, nargout, varargin);
    readXControl.processXTicks();
    