w = 1;
b = 1;

eta = 1e-1;
cost = 1;
training_data = [0 ,0; 1, 0; 2, 0; 3, 1; 4, 1; 5, 1];

max_number_of_epochs = 1e7;
cost_over_epochs = zeros([max_number_of_epochs,1]);

for i = [1:max_number_of_epochs]
    f = 1 ./ (1 + exp(-(w .* training_data(:,1) + b)));
    cost = .5 * norm((training_data(:,2) - f),2);
    cost_over_epochs(i, 1) = cost;
    
    dcostw = -(training_data(:,2) - f) .* (1 + exp(-(w .* training_data(:,1) + b))).^-2 .* (training_data(:,1) .* exp(-(w .* training_data(:,1) + b)));
    dcostb = -(training_data(:,2) - f) .* (1 + exp(-(w .* training_data(:,1) + b))).^-2 .* (exp(-(w .* training_data(:,1) + b)));
    
    dcostw = sum(dcostw);
    dcostb = sum(dcostb);
    
    w = w - eta * dcostw;
    b = b - eta * dcostb;  
end

figure()
titlestring = sprintf("Christopher Morris: w = %.3f and b = %.3f", w, b);

xrange = [-3:8];
yrange = (1 + exp(-(w .* xrange + b))).^-1;

plot(xrange, yrange, 'k', 'linewidth', 3);
title(titlestring);

xlim([-3,8])
ylim([-1,2])

figure()
plot([1:max_number_of_epochs], cost_over_epochs);
title('Cost per Epoch');
