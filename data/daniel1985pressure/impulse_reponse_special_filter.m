%% Impulse response of the simplified monitoring filter (special filter)
beta=0.0166;% An example beta
u=ones(1,350);% Unit step function
h=[];% Response
for n=1:length(u)
    h(n)=(beta+1)*((1-beta)^n)*u(n);
end

plot((1:length(h)),h)
title('Impulse response of the simplified monitoring filter (special filter)')
ylabel('Amplitude');
xlabel('Samples')
