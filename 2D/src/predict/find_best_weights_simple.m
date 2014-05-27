function [weights, other] = find_best_weights_simple(depth, mask_stack, gt_img_in, activation_energy)
% function to find best set of weights in a simple way
% based on find_optimal_weights

% input checks
assert(all(gt_img_in(:)<=1));
assert(all(gt_img_in(:)>=0));

% removing the pixels which are def. empty and which no-one cares about
gt_filled = fill_grid_from_depth(depth, size(mask_stack, 1), 0.5);

% reshaping the inputs to be nice
mask_stack_trans = permute(mask_stack, [3, 1, 2]);
mask_stack_trans = double(mask_stack_trans(:, :));
gt_img_flat = double(gt_img_in(:)');
gt_filled_flat = gt_filled(:)';

% removing the pixels which are def. empty and which no-one cares about
%to_remove = gt_filled_flat == 0 | (gt_img_flat==0 & all(mask_stack_trans==0, 1));
%gt_img_flat(to_remove) = [];
%mask_stack_trans(:, to_remove) = [];
%size(mask_stack_trans)

% computing size of the GT masks etc
size_prediction = sum(mask_stack_trans>0.5, 2);

N = size(mask_stack_trans, 1);
gt_img_repmat = repmat(gt_img_flat>0.5, N, 1);

size_true_positive = sum(mask_stack_trans>0.5 & gt_img_repmat, 2);

% computing the weights
weights = size_true_positive ./ size_prediction;
weights(isnan(weights)) = 0;

% forming outputs
%weights(weights <= weights_threshold) = 0;
%{
v_w = 0.5;
t_w = 0.99;
b = (v_w - t_w^2) / (t_w - t_w^2);
a = 1 - b;
t = 0:0.01:1;
f = @(x)(max(a * x.^2 + b * x, 0));
%}
%weights = f(weights);

assert(activation_energy<=1);
f = @(x)(max((x-activation_energy)./(1-activation_energy), 0));
weights = f(weights);



%other.simple_classification = round(weights) == 1;

% simple method of combining the basis shapes (creating union)
%other.simple_image = any(mask_stack(:, :, other.simple_classification), 3);
other.size_prediction = size_prediction;
other.size_true_positive = size_true_positive;
% complex method, allowing for continuous weight values
%[other.simple_image,  T]= noisy_or(mask_stack, 3, weights);
[other.softmax_image,  T]= soft_max(mask_stack, 3, 10, weights);

% doing the probability
probs = weights / sum(weights);
[~,  temp]= noisy_or(mask_stack, 3, probs);
other.summed_image = sum(temp, 3);


other.simple_weights = sum(T, 3);