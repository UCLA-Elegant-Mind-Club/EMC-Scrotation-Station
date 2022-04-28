If the data has not automatically been shifted by the time delay, modify and run the shiftTimes.m script
Run wrapRollData.m to wrap roll reaction times from -180 to 180 degrees (both refer to the same orientation).
Run the AggregateAnalysis_version3.m script to obtain all initial plots and parameters.
To replot only the aggregated data, run the RePlotAggregate.m script after specifying drawing preferences.
To replot only chi-square histograms, run the isolatedHistograms.m script

After obtaining Aggregate Parameters for all protocols, assemble them into a table with the same rows format as the given example.
Then run the groupParamComparison.m in the same folder after specifying preferences for slopes and/or intercepts.
