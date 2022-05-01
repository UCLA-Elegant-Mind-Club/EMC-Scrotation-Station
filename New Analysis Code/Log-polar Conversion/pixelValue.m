function [pixVal, inRange, x, y] = pixelValue(radius, angle, img, width, height, useSigmoid)
    if nargin < 6; useSigmoid = false; end
    inRange = false;
    pixVal = 0;
    x = width/2 + 0.5 + cos(angle) * radius; 
    y = height/2 + 0.5 + sin(angle) * radius;
    if [x, y, -x, -y] > [1, 1, -width, -height]
        inRange = true;
        [x1, x2, y1, y2] = deal(floor(x), ceil(x), floor(y), ceil(y));
        
        if useSigmoid
            points1 = [img(y1,x1), img(y2,x1), img(y1,x1), img(y1,x2)];
            points2 = [img(y1,x2), img(y2,x2), img(y2,x1), img(y2,x2)];
            dif = abs(points2 - points1) * 0.998 + 0.001;
            base = power(1 - dif, 20);
            pos = [x - x1, x - x1, y - y1, y - y1] * 2 - 1;
            weight = 0.5 * (1 - base .^ -pos) ./ (1 + base .^ -pos) .* (1 + base) ./ (1 - base);
            weight = weight + 0.5;
        else
            weight = [1 - x + x1, 1 - x + x1, 1 - y + y1, 1 - y + y1];
        end

        topAvg = img(y1,x1) * weight(1) + img(y1,x2) * (1 - weight(1));
        bottomAvg = img(y2,x1) * weight(2) + img(y2,x2) * (1 - weight(2));
        vertWeight = (weight(3) + weight(4)) / 2;
        pixVal = topAvg * vertWeight + bottomAvg * (1 - vertWeight);
    end
end