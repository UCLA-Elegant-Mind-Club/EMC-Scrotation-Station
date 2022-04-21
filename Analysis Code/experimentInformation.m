function [protocolNames, colors, linestyle, axes, refDist] = experimentInformation()
% get: protocolNames
% get: colors
% get: linestyles
% get x and y axes
% get markers
rotationNames = ["Chinese Roll RT", "English Roll RT", "Faces Pitch RT", ...
    "Faces Roll RT", "Faces Yaw RT", "Thai Roll RT"];
rotationColors = ["black", "green", "blue", "magenta", "red", "yellow"];
prompt = {'Enter x axis', 'Enter y axis'};
dlgtitle = 'Input';
dims = [2 35];
definput = {'Angle of Rotation (°)', 'Reaction Time (ms)'};
axes = inputdlg(prompt,dlgtitle,dims,definput);

prompt = {'Enter reference angle/distance'};
dlgtitle = 'Input';
dims = [2 35];
definput = {'0'};
refDist = inputdlg(prompt, dlgtitle, dims, definput);

prompt = {'Enter Number of Protocols:'};
dlgtitle = 'Input';
dims = [1 35];
definput = {'6'};
answer = inputdlg(prompt,dlgtitle,dims,definput);
Answer = str2num(answer{1});
if strcmp(answer,'3')
    answer = questdlg({'Is your experiment Eccentricity vs. RT?' 'Pitch/Roll/Yaw'})
    if strcmp(answer,'Yes')
        protocolNames = {'Pitch'; 'Roll'; 'Yaw'};
        answer = questdlg({'Are you satisfied with the default colors:'...
            'Pitch = Red' 'Roll = Yellow' 'Yaw = Blue'});
        if strcmp(answer,'Yes')
            colors = {[0.86275 0.27451 0.27451];[0.64706 0.20392 0.64314];[0.15686 0.57647 0.93333]};
        elseif strcmp(answer, 'No')            
            strArray = strings(1,Answer);
            defInputStr = strings(1,Answer);
            for ii = 1:Answer
                strArray(ii) = strcat('Enter Name of Color for Protocol', {' '}, string(ii), ':');
                strArray2 = cellstr(strArray);
                defInputStr(ii)  = rotationColors(ii);
                defInputStr2 = cellstr(defInputStr);
            end
            prompt = strArray2;
            dlgtitle = 'Choose from these colors: gray, red, blue, light blue,maroon, black, green';
            dims = [1 35];
            definput = defInputStr2;
            answer = inputdlg(prompt,dlgtitle,dims,defInputStr2);
            colors = answer;       
        end
        answer = questdlg({'Are you satisfied with the default linestyles:'...
            'Pitch = - (single dash)' 'Roll SRT = - (single dash)'...
            'Yaw = - (single dash)'});
        if strcmp(answer, 'Yes')
            linestyle = {'-'; '-'; '-'};
        elseif strcmp(answer, 'No')
            clear strArray;
            clear defInputStr;
            clear strArray2;
            clear defInputStr2;
            strArray = strings(1,Answer);
            defInputStr = strings(1,Answer);
            for ii = 1:Answer
                strArray(ii) = strcat('Enter Linestyle for Protocol', {' '}, string(ii), ':');
                strArray2 = cellstr(strArray);
                defInputStr(ii)  = '--';
                defInputStr2 = cellstr(defInputStr);
            end
            prompt = strArray2;
            dlgtitle = 'Choose from these linestyles: ''-'' or ''--'' (single/double dash)';
            dims = [1 35];
            definput = defInputStr2;
            answer = inputdlg(prompt,dlgtitle,dims,defInputStr2);
            linestyle = answer;    
        end
    elseif strcmp(answer,'No')
        prompt = {'Enter Name of Protocol 1:', 'Enter Name of Protocol 2:',...
            'Enter Name of Protocol 3:'};
        dlgtitle = 'Input';
        dims = [1 35];
        definput = {'Protocol 1', 'Protocol 2', 'Protocol 3'};
        answer = inputdlg(prompt,dlgtitle,dims,definput);
        protocolNames = answer;
        
        strArray = strings(1,Answer);
        defInputStr = strings(1,Answer);
        for ii = 1:Answer
            strArray(ii) = strcat('Enter Name of Color for Protocol', {' '}, string(ii), ':');
            strArray2 = cellstr(strArray);
            defInputStr(ii)  = 'black';
            defInputStr2 = cellstr(defInputStr);
        end
        prompt = strArray2;
        dlgtitle = 'Choose from these colors: gray, red, blue, light blue,maroon, black, green';
        dims = [1 35];
        definput = defInputStr2;
        answer = inputdlg(prompt,dlgtitle,dims,defInputStr2);
        colors = answer;
        clear strArray;
        clear defInputStr;
        clear strArray2;
        clear defInputStr2;
        strArray = strings(1,Answer);
        defInputStr = strings(1,Answer);
        for ii = 1:Answer
            strArray(ii) = strcat('Enter Linestyle for Protocol', {' '}, string(ii), ':');
            strArray2 = cellstr(strArray);
            defInputStr(ii)  = '--';
            defInputStr2 = cellstr(defInputStr);
        end
        prompt = strArray2;
        dlgtitle = 'Choose from these linestyles: ''-'' or ''--'' (single/double dash)';
        dims = [1 35];
        definput = defInputStr2;
        answer = inputdlg(prompt,dlgtitle,dims,defInputStr2);
        linestyle = answer; 
    end
        
elseif strcmp(answer,'4')
    answer = questdlg({'Is your experiment Eccentricity vs. RT?' 'Pitch/Roll/Yaw/Azimuth'});
    if strcmp(answer,'Yes')
        protocolNames = {'Pitch'; 'Roll'; 'Yaw'; 'Eccentricity'};
        answer = questdlg({'Are you satisfied with the default colors:'...
            'Pitch = Red' 'Roll = Yellow' 'Yaw = Blue' 'Ecc = Green'});
        if strcmp(answer,'Yes')
            colors = {[0.86275 0.27451 0.27451];[1 0.78824 0];[0.15686 0.57647 0.93333]; [0.05098 0.63529 0.035294]};
        elseif strcmp(answer, 'No')             
            strArray = strings(1,Answer);
            defInputStr = strings(1,Answer);
            for ii = 1:Answer
                strArray(ii) = strcat('Enter Name of Color for Protocol', {' '}, string(ii), ':');
                strArray2 = cellstr(strArray);
                defInputStr(ii)  = 'black';
                defInputStr2 = cellstr(defInputStr);
            end
            prompt = strArray2;
            dlgtitle = 'Choose from these colors: gray, red, blue, light blue,maroon, black, green';
            dims = [1 35];
            definput = defInputStr2;
            answer = inputdlg(prompt,dlgtitle,dims,defInputStr2);
            colors = answer;       
        end
        answer = questdlg({'Are you satisfied with the default linestyles:'...
            'Pitch = - (single dash)' 'Roll SRT = - (single dash)'...
            'Yaw = - (single dash)' 'Ecc = - (single dash)'});
        if strcmp(answer, 'Yes')
            linestyle = {'-'; '-'; '-';'-'};
        elseif strcmp(answer, 'No')
            clear strArray;
            clear defInputStr;
            clear strArray2;
            clear defInputStr2;
            strArray = strings(1,Answer);
            defInputStr = strings(1,Answer);
            for ii = 1:Answer
                strArray(ii) = strcat('Enter Linestyle for Protocol', {' '}, string(ii), ':');
                strArray2 = cellstr(strArray);
                defInputStr(ii)  = '--';
                defInputStr2 = cellstr(defInputStr);
            end
            prompt = strArray2;
            dlgtitle = 'Choose from these linestyles: ''-'' or ''--'' (single/double dash)';
            dims = [1 35];
            definput = defInputStr2;
            answer = inputdlg(prompt,dlgtitle,dims,defInputStr2);
            linestyle = answer;    
        end
    elseif strcmp(answer,'No')
        prompt = {'Enter Name of Protocol 1:', 'Enter Name of Protocol 2:',...
            'Enter Name of Protocol 3:', 'Enter Name of Protcol 4'};
        dlgtitle = 'Input';
        dims = [1 35];
        definput = {'Protocol 1', 'Protocol 2', 'Protocol 3', 'Protocol 4'};
        answer = inputdlg(prompt,dlgtitle,dims,definput);
        protocolNames = answer;
        
        strArray = strings(1,Answer);
        defInputStr = strings(1,Answer);
        for ii = 1:Answer
            strArray(ii) = strcat('Enter Name of Color for Protocol', {' '}, string(ii), ':');
            strArray2 = cellstr(strArray);
            defInputStr(ii)  = 'black';
            defInputStr2 = cellstr(defInputStr);
        end
        prompt = strArray2;
        dlgtitle = 'Choose from these colors: gray, red, blue, light blue,maroon, black, green';
        dims = [1 35];
        definput = defInputStr2;
        answer = inputdlg(prompt,dlgtitle,dims,defInputStr2);
        colors = answer;
    end    
    
else
    answer = str2num(answer{1});
    Answer = answer;
    strArray = strings(1,answer);
    defInputStr = strings(1,answer);
    for ii = 1:answer
        strArray(ii) = strcat('Enter Name of Protocol', {' '}, string(ii), ':');
         strArray2 = cellstr(strArray);
        defInputStr(ii) = rotationNames(ii);
        defInputStr2 = cellstr(defInputStr);
    end
    prompt = strArray2;
    dlgtitle = 'Input';
    dims = [1 35];
    definput = defInputStr2;
    answer = inputdlg(prompt,dlgtitle,dims,defInputStr2);
    protocolNames = answer;
    clear strArray;
    clear defInputStr;
    clear strArray2;
    clear defInputStr2;
    strArray = strings(1,Answer);
    defInputStr = strings(1,Answer);
    for ii = 1:Answer
        strArray(ii) = strcat('Enter Name of Color for Protocol', {' '}, string(ii), ':');
        strArray2 = cellstr(strArray);
        defInputStr(ii)  = rotationColors(ii);
        defInputStr2 = cellstr(defInputStr);
    end
    prompt = strArray2;
    dlgtitle = 'Choose from these colors: gray, red, blue, light blue,maroon, black, green';
    dims = [1 35];
    definput = defInputStr2;
    answer = inputdlg(prompt,dlgtitle,dims,defInputStr2);
    colors = answer;
    
    clear strArray;
    clear defInputStr;
    clear strArray2;
    clear defInputStr2;
    strArray = strings(1,Answer);
    defInputStr = strings(1,Answer);
    for ii = 1:Answer
        strArray(ii) = strcat('Enter Linestyle for Protocol', {' '}, string(ii), ':');
        strArray2 = cellstr(strArray);
        defInputStr(ii)  = '--';
        defInputStr2 = cellstr(defInputStr);
    end
    prompt = strArray2;
    dlgtitle = 'Choose from these linestyles: ''-'' or ''--'' (single/double dash)';
    dims = [1 35];
    definput = defInputStr2;
    answer = inputdlg(prompt,dlgtitle,dims,defInputStr2);
    linestyle = answer;
end