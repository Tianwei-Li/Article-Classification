function [] = accurate()

xvector1 = [1,2,3,4,5];  % NB_stem, TNB, CNB, NB
yvector1 = [0.6455, 0.653, 0.667, 0.6775, 0.68];



% Create figure
figure1 = figure;

% Create axes
axes1 = axes('Parent',figure1,...
    'XTickLabel',{'NB with stem','TNB','CNB','NB','SVM'},...
    'XTick',[1 2 3 4 5]);

%% Uncomment the following line to preserve the Y-limits of the axes
ylim(axes1,[0.6 0.7]);
box(axes1,'on');
hold(axes1,'all');

% Create xlabel
xlabel({'algorithms'});

% Create ylabel
ylabel({'accuracy'});

% Create bar
bar1 = bar(xvector1,yvector1,'ShowBaseLine','off','FaceColor','interp',...
    'BarWidth',0.2);
baseline1 = get(bar1,'BaseLine');
set(baseline1,'Visible','off');

end
