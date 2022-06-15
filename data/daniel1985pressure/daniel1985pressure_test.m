%% Surface fit
% This data is quite small but it may serve for demonstration purposes.
load daniel1985pressure_data
pressure=daniel1985pressure{:,1};
duration=daniel1985pressure{:,2};
damage=daniel1985pressure{:,3};

% Convert units
pressure=pressure*133.322/1000; % to kPa
duration=duration*60; %to minutes


% try removing data sample 1 to see what changes (This sample is an oulier).
 pressure=pressure(2:end);
 duration=duration(2:end);
 damage=damage(2:end);

%% fit data
sf = fit([duration, pressure],damage,'poly11','robust','LAR')
plot(sf,[duration,pressure],damage)

%% transfer model to python
% k_c=-10.09;k_t=1.603;k_p=0.01813;k_t2=-0.04975; k_pt=-0.001018;k_p2=-7.172e-06;
% q_tp=k_c + k_t*t + k_p*P + k_t2*t**2 + k_pt*t*P + k_p2*P**2
