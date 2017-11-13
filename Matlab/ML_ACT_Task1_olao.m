clc;
clear;

X = -50:0.1:50;

i = 1;
for x = X
    Y(i) = yplot(x);
    i = i + 1;
end
plot(X, Y);

function answer = yplot(x)
    a = x;
    b = -x.^3/factorial(3);
    c = x.^5/factorial(5);
    d = -x.^7/factorial(7);
    answer = a + b + c + d;
end
