close all;
filenames = ["Faces_Roll", "Faces_Yaw", "Faces_Pitch"];
%filenames = ["English_Roll_RT", "Thai_Roll_RT", "Chinese_Roll_RT"];
titles = replace(filenames, "_", " ");
folder = uigetdir(pwd);
filenames = fullfile(folder, "Output-Parameters_for_" + filenames + ".xlsx");

for i = 1:3
    figure(i)
    hold on;
    table = readtable(filenames(i));
    matrix = table2array(table);
    allredchi = sort([matrix(:,10); matrix(:,12)]);
    Histogram = histfit(allredchi,10,'gamma');
    pd = gamfit(allredchi,10);

    ms = MultiStart;
    gampoint = @(x) -gampdf(x, pd(1), pd(2));
    problem = createOptimProblem('fmincon', 'x0', 1, ...
        'objective', gampoint, 'lb' , 0, 'ub', 3);
    params = run(ms,problem,25);

    xlim([0 10]);
    ylim([0 35]);
    xlabel("Reduced Chi Squares")
    ylabel("Frequency")
    title(titles(i));
    subtitle(sprintf("Gamma Distribution: a = %.2f, b = %.2f, max = %.2f", pd(1), pd(2), params(1)));
end