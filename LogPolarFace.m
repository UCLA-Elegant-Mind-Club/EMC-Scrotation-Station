[file, path] = uigetfile({'*.png;*.jpg'}, 'Select an image to convert');

img = im2double(imread(fullfile(path, file)));
height = size(img, 1);
width = size(img, 2);
depth = size(img, 3);
midX = width/2 + 0.5;
midY = height/2 + 0.5;

%% Cortical area (resultant image dimensions)
cortWidth = 900; %% left and right brain are separated
cortHeight = 1800;
newImg = zeros(cortWidth * 2, cortHeight);

%% expCoef determines how exponential distance is represented in the cortex
% larger numbers mean greater area on cortex is mapped to the foveal region
expCoef = 100;

%% compression refers to how much an image should be scaled down
% a compression of 2 will mean that a circle with radius of 1800 px
% occupies a cortical pattern with a width of 900 px. Values < 1 will scale up the image
compression = 0.5;

stepDraw = false;
testImg = zeros(height, width);

for pixel = 1:depth
    imgSlice = img(:, :, pixel);
    newImgSlice = ones(cortWidth * 2, cortHeight);
    
    for pol = 1: cortHeight
        %% Left Side of cortical image
        for dist = 1: cortWidth
            radius = (power(expCoef, 1 - dist/cortWidth) - 1) / (expCoef - 1);
            radius = radius * cortWidth * 2 * compression;

            angle = (90 + pol / cortHeight * 180) * pi/180;
            x = cos(angle) * radius + midX;
            y = sin(angle) * radius + midY;
            if [x, y, -x, -y] > [1, 1, -width, -height]
                [x1, x2, y1, y2] = deal(floor(x), ceil(x), floor(y), ceil(y));
                weights = [x-x1, x2-x, y-y1, y2-y];
                topAvg = imgSlice(y1,x1) * weights(1) + imgSlice(y1,x2) * weights(2);
                bottomAvg = imgSlice(y2,x1) * weights(1) + imgSlice(y2,x2) * weights(2);
                newImgSlice(pol, dist) = topAvg * weights(3) + bottomAvg * weights(4);
                testImg(floor(y), floor(x)) = 1;
            end
        end

        %% Right side of cortical image
        for dist = cortWidth + 1: 2 * cortWidth
            radius = (power(expCoef, dist/cortWidth - 1) - 1) / (expCoef - 1);
            radius = radius * cortWidth * 2 * compression;

            angle = (90 - pol / cortHeight * 180) * pi/180;
            x = midX + cos(angle) * radius;
            y = midY + sin(angle) * radius;
            if [x, y, -x, -y] > [1, 1, -width, -height]
                [x1, x2, y1, y2] = deal(floor(x), ceil(x), floor(y), ceil(y));
                weights = [x-x1, x2-x, y-y1, y2-y];
                topAvg = imgSlice(y1,x1) * weights(1) + imgSlice(y1,x2) * weights(2);
                bottomAvg = imgSlice(y2,x1) * weights(1) + imgSlice(y2,x2) * weights(2);
                newImgSlice(pol, dist) = topAvg * weights(3) + bottomAvg * weights(4);
                testImg(floor(y), floor(x)) = 1;
            end
        end
    end
    newImg(:, :, pixel) = newImgSlice;
end
imshow(newImg);
figure();
imshow(testImg);
