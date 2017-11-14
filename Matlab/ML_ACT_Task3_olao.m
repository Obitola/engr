clear;
clc;

x1 = 0:2:10;
x2 = 0:1:10;
x3 = 0:0.01:10;

i = 1;
for x = x1
    y1(i) = sin(x);
    i = i + 1;
end

i = 1;
for x = x2
    y2(i) = sin(x);
    i = i + 1;
end

i = 1;
for x = x3
    y3(i) = sin(x);
    i = i + 1;
end

plot(x1,y1,x2,y2,x3,y3);