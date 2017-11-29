clear;
clc;

disp('DO in Wabash in ml/L')
disp('Day    DO')
disp('-----------')

days = 1:20;
for i = 1:20
	within(i) = ' ';
end

for t = days
	do(t) = round(finddo(t),2);
	if do(t) <= 8 && do(t) >= 6
		within(t) = '*';
    end
end

for i = days
    fprintf('%-6d %-4.2f %-1s\n',i, do(i), within(i))
end
	
function x = finddo(t)
    DOsat = 9;
    k1 = 0.2;
    k2 = 0.4;
    li = 25;
    di = 4;
	x = DOsat - (k1*li/(k2-k1)) * (exp(-k1*t)-exp(-k2*t)) - di*exp(-k2*t);
end
