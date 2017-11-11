
g = 9.81;
angle = 53.13;
anglef = angle*pi/180;
k = 1000;
coef = 0.3;
mass = 5;


distance = [1:0.1:10];
deflect = [];

for i = [1:length(distance)]
    deflect(i) = deflection(g, anglef, k, coef, i, mass);
end

figure(1)
plot(distance, deflect)
title('Displacement vs Deflection')
ylabel('Deflection')
xlabel('Displacement')
grid()

%%
g = 9.81;
angle = [(pi/10),0.1,(pi/2)];
k = 1000;
coef = 0.3;
mass = 5;
distance = 0.75;
deflect = [];

for i = [1:length(angle)]
    deflect(i) = deflection(g, i, k, coef, distance, mass);

end

figure(2)
plot(angle, deflect)
title('Angle vs Deflection')
ylabel('Deflection')
xlabel('Angle')
grid()

%%



g = 9.81;
angle = 53.13*pi/180;
k = [50:50:5050];
coef = 0.3;
mass = 5;
distance = .75;
deflect = []

for i = [1:length(k)]
    deflect(i) = deflection(g, angle, i, coef, distance, mass);
end


figure(3)
plot( k, deflect)
title('Spring Constant vs Deflection')
ylabel('Deflection')
xlabel('Spring Constant')
grid()



%%

g = 9.81;
angle = 53.13*pi/180;
k = 1000;
coef = [0:0.2:1.2]
mass = 5
distance = .75
deflect = []

for i = [1:length(coef)]
    deflect(i) = deflection(g, angle, k, i, distance, mass);
end

figure(4)
plot( coef, deflect)
title('Coefficient vs Deflection')
ylabel('Deflection')
xlabel('Coefficient')
grid()

%%    
    
g = 9.81;
angle = 53.13*pi/180;
k = 1000;
coef = 0.3;
mass = [1:0.5:25]
distance = .75
deflect = []

for i = [1:length(mass)]
    deflect(i) = deflection(g, angle, k, coef, distance, i);
end
            

figure(5)
plot( mass, deflect)
title('Mass vs Deflection')
ylabel('Deflection')
xlabel('Mass')
grid()
function defl = deflection(g,angle,k,coef,distance,mass)
    defl = sqrt((2*mass*g*distance*sin(angle)-coef*mass*distance*g*cos(angle))/k);
end