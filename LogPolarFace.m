clear newFullImg;
fullImg = im2double(imread("mainRotated.png"));
for pixel = 1:size(fullImg, 3)
    img = fullImg(:, :, pixel);
    for i = 1:2
        width = size(img, 2);
        if mod(width,2) ~= 0
            col = img(:, width/2 + 0.5);
            img = [img(:, 1:width/2 - 0.5), col, img(:, width/2 + 0.5 : end)];
        end
        img = img.';
    end
    width = size(img, 2);
    height = size(img, 1);
    newImg = ones(height, width);
    numPix = zeros(height, width);
    midX = width/2 + 0.5;
    midY = height/2 + 0.5;
    buffer = 100;
    maxDist = log(sqrt((width - midX)^2 + (height - midY)^2) + buffer) - log(buffer);
    debug = false;
    
    for x = 1: width
        for y = 1: height
            dist = ceil((log(sqrt((x - midX)^2 + (y - midY)^2) + buffer) - log(buffer)) ...
                / maxDist * width/2) + width/2;
            pol = ceil((atan((y - midY)/(x - midX)) / pi + 0.5) * height);
            if x > midX
                dist = width - dist + 1;
                pol = height - pol + 1;
            end
            nPix = numPix(pol, dist);
            numPix(pol, dist) = nPix + 1;
            newImg(pol, dist) = img(y, x);
        end
    end
    newFullImg(:, :, pixel) = newImg;
end
imshow(newFullImg);


