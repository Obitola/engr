\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ pi / 180;
k = 1000;
f = 0.3;
m = 5;

drange = 0:0.1:1;
trange = (pi/10):(pi/1800):(pi/2);
krange = 50:50:5050;
frange = 0:0.2:1.2;
mrange = 1:0.5:25;


i = 1;
for x = drange
    deflection1(i) = calculate(x,t,k,f,m);
    i = i + 1;
end
subplot(3,2,1);
plot(drange,deflection1);

i = 1;
for x = trange
    deflection2(i) = calculate(d,x,k,f,m);
    i = i + 1;
end
subplot(3,2,2);
plot(trange, deflection2);

i = 1;
for x = krange
    deflection3(i) = calculate(d,t,x,f,m);
    i = i + 1;
end
subplot(3,2,3);
plot(krange, deflection3);

i = 1;
for x = frange
    deflection4(i) = calculate(d,t,k,x,m);
    i = i + 1;
end
subplot(3,2,4);
plot(frange, deflection4);

i = 1;
for x = mrange
    deflection5(i) = calculate(d,t,k,f,x);
    i = i + 1;
end
subplot(3,2,5);
plot(mrange, deflection5);

function x = calculate(d, t, k, f, m)
    g = 9.8
    a = 0.5 * k;
	b = m * g * (cos(t) * f - sin(t));
	c = d * m * g * (cos(t) * f - sin(t));
	x = (-b + sqrt(b.^2 - 4 * a * c))/(2 * a);
end