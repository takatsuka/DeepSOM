% surface of figure 8 klein
a = 1;
t1 = -pi : pi/12 : pi;
t2 = -pi : pi/12 : pi;
[u,v] = meshgrid(t1, t2);
x = (cos(u).*(a+sin(v).*cos(u/2)-sin(2*v).*sin(u/2)/2));
y = (sin(u).*(a+sin(v).*cos(u/2)-sin(2*v).*sin(u/2)/2));
z = (sin(u/2).*sin(v)+cos(u/2).*sin(2*v)/2);
surf(x,y,z)

% randomly generate points
v = -pi*rand(1, 2000)*pi;
u = -pi*rand(1, 2000)*pi;

x = (cos(u).*(a+sin(v).*cos(u/2)-sin(2*v).*sin(u/2)/2));
y = (sin(u).*(a+sin(v).*cos(u/2)-sin(2*v).*sin(u/2)/2));
z = (sin(u/2).*sin(v)+cos(u/2).*sin(2*v)/2);
scatter3(x,y,z);