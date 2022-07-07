f =@(x,y) x.^2 + .5 .* y.^2;
xgradient =@(x,y) 2.*x;
ygradient =@(x,y) y;

x0 = 10;
y0 = 10;


num_data_points = 20;
x_list = zeros(1,num_data_points);
y_list = zeros(1,num_data_points);
z_list = zeros(1,num_data_points);

x=x0;
y=y0;
theta = [0:.001:2*pi()]; 


hold all

rand_seq_accept = randi([0,1], num_data_points, 1);

x_random_list = zeros(1, num_data_points);
y_random_list = zeros(1, num_data_points);


x_rand = x0;
y_rand = y0;

for i=1:num_data_points
    x_random_list(1,i) = x_rand;
    y_random_list(1,i) = y_rand;
    
    x_rand = x_rand - .1 * rand_seq_accept(i,1) * xgradient(x_rand,y_rand);
    y_rand = y_rand - .1 * (1 - rand_seq_accept(i,1)) * ygradient(x_rand,y_rand);
    
end

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
contour(X,Y,z,z_list(1,:));

plot(x_list, y_list, '-ko', 'linewidth', 3, 'markersize', 8, 'markerfacecolor', 'k');
plot(x_random_list, y_random_list, '-o', 'linewidth', 3, 'markersize', 8, 'markerfacecolor', 'white');

xlim([-3,13])
ylim([-3,13])

epsilon = 2;

textlist = {};
for i=1:num_data_points
    textstring = sprintf('Point %.0f: x = %.2f, y = %.2f', i, x_random_list(1,i), y_random_list(1,i));
    textlist{i} = textstring;
    xtemp = 10.5; %x_random_list(1,i)+epsilon;
    ytemp = 12 - i/2;   y_random_list(1,i);
    
    
    text(xtemp, ytemp, textstring);
%     annotation('textarrow', [x_random_list(1,i), 11], [y_random_list(1,i), y_random_list(1,i)], 'string', textstring);

end
% legend(textlist, 'Location', 'northeast', 'NumColumns', 1)
% legend(textlist)

grid on
axis square