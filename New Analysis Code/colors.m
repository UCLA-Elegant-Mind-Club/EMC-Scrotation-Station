color = [0.4 0.8 0.2];
shadeFactor = 0.5; %makes darker, between 0 (black) - 1 (normal)
newcolor = color .* shadeFactor;

tintFactor = 0.75; %makes lighter, between 0 (white) - 1 (normal)
dif = 1 - newcolor;
newcolor = 1 - dif * tintFactor;

figure();
hold on;
scatter(0, 0, 1000, color, 'square', 'filled');
scatter(1, 0, 1000, newcolor, 'square', 'filled');
xlim([-5 7]);