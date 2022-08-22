folder = uigetdir("C:\Users\emban\Documents\GitHub\EMC-Scrotation-Station\Face Rotation Paper\Data");
fileList = dir(fullfile(folder, '*.csv'));
total1 = 0;
total2 = 0;
count = 0;
len = 20;
for i = 3:length(fileList)
    table = readtable(fullfile(folder, fileList(i).name));
    total1 = total1 + mean(table{1:len, 3});
    total2 = total2 + mean(table{height(table) - len + 1:end, 3});
    count = count + 1;
end
diff = total2 - total1;
diff = diff / count;