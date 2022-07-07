
f =@(x,y) x.^2 + .5 .* y.^2;
xgradient =@(x,y) 2.*x;
ygradient =@(x,y) y;

x0 = 10;
y0 = 10;


num_data_points = 11;
x_list = zeros(1,num_data_points);
y_list = zeros(1,num_data_points);
z_list = zeros(1,num_data_points);



x=x0;
y=y0;
theta = [0:.001:2*pi()]; 


hold all

for i=1:num_data_points
    x_list(1,i) = x;
    y_list(1,i) = y;
    z_list(1,i) = f(x,y);

    
    x = x - .1 * xgradient(x, y);
    y = y - .1 * ygradient(x,y);
    
    
%     plot(cos(theta), sqrt(f(x,y) ./ .5) .* sin(theta));
        

end

colormap winter
[X, Y] = meshgrid(-100:.1:100,-100:.1:100);
z=f(X,Y);
contour(X,Y,z,z_list(1,:))

plot(x_list, y_list, '-ko', 'linewidth', 3, 'markersize', 8, 'markerfacecolor', 'k');

grid on
axis equal

xlim([-3,13])
ylim([-3,13])

epsilon = .5;
for i=1:num_data_points
    textstring = sprintf('x = %.2f, y = %.2f', x_list(1,i), y_list(1,i));
    xtemp = x_list(1,i)+epsilon;
    ytemp = y_list(1,i);
    text(xtemp, ytemp, textstring);
    
    
end