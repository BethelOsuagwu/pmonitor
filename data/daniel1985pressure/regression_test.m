%% Linear modelling
% This data is quite small but it may serve for demonstration purposes.
load daniel1985pressure_data
pressure=daniel1985pressure{:,1};
duration=daniel1985pressure{:,2};
damage=daniel1985pressure{:,3};

% Convert units
pressure=pressure*133.322/1000; % to kPa
duration=duration*60; %to minutes
% In the models below we will exclude observation 1 as this observation
% did not lead to injury. 


%% Fit data stepwise with generalised linear model to rapidly guide model selection
gm_stepwise = stepwiseglm([duration, pressure],damage,'constant','upper','interactions','exclude',[1])
%gm_stepwise2=gm_stepwise.removeTerms('1')% Create new model without the constant term.

%% Fit data with generalised linear model (This is the one we will report)
modelspec = 'Damage ~ Duration+Pressure ';
gm = fitglm(daniel1985pressure,modelspec,'distribution','normal','exclude',[1])
gm.plotResiduals
R_squared=gm.Rsquared
[p,F,dfn]=coefTest(gm)
coeff_95percent_confi=coefCI(gm)

%% Had we included the first observation, we could use the followng to identify it as the first outlier
% outlier = find(isoutlier(gm.Residuals.Raw))

%% Interpretation
% The model f-test in linear model tests your model against the model with
% only the constant term:
% https://www.statisticshowto.com/probability-and-statistics/f-statistic-value-test/
% https://www.statisticssolutions.com/reporting-statistics-in-apa-format/
%
% Example: F(dfn,dfd) if a=number of coef in the model, including the intercept and N is number of  observations, then
%   a-1=dfn->degrees of freedom numerator/regression degree of freedom
%   N-a=dfd -> degrees of freedom denominator / degree of freedon of error
%   
%   So in our case: https://uk.mathworks.com/help/stats/understanding-linear-regression-outputs.html
%   The model was statistically significant,R^2=0.6476(adj, 0.5934), F(2,13)=11.9435, p=0.0011.
%   The duration  and pressure magnitude terms were estimated to be
%   c1=0.14938(t=4.8837, p=0.00029865, SE=0.030588 ) c2=0.0014787(t=3.3372, p=0.0053512, SE=0.0004431) repectively
%   The intercept term, c0, 0.55323, did not reach significance (t=1.1514, p=0.27029, SE=0.48047).
% 

