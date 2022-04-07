function [fileName] = FolderNameGenerator()
prompt = {'Your Name' ; 'Experiment Information'};
dlgtitle = 'Experiment Information';
dims = [2 60; 2 60];
definput = {'Rotation', '6 protocols' };
format shortg;
dateTime = clock;
dateTime = fix(dateTime);
dateTime = join(string(dateTime), '-');
userInput = inputdlg(prompt,dlgtitle,dims,definput);
userInput = regexprep(userInput, ' ', '_');
fileName = join(strjoin([join(string(userInput), '-'), dateTime], '-'), '-' );
end