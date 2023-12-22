import numpy as np

def calculate_delta(a, b):
    return np.mean(a) - np.mean(b)

def bootstrap(model_pred_1, model_pred_2, y_true, num_samples=1000):
    # Calculate observed delta
    observed_delta = calculate_delta(
        model_pred_1 == y_true, 
        model_pred_2 == y_true
    )
    
    # Initialize variables
    s = 0
    
    # Number of data points
    n = len(y_true)
    
    for _ in range(num_samples):
        # Draw a bootstrap sample
        indices = np.random.choice(n, size=n, replace=True)
        y_true_sample = y_true[indices]
        model_pred_1_sample = model_pred_1[indices]
        model_pred_2_sample = model_pred_2[indices]

        # Calculate delta_i
        delta_i = calculate_delta(
            model_pred_1_sample == y_true_sample, 
            model_pred_2_sample == y_true_sample
        )
        
        # Check if delta_i is greater than or equal to 2 * observed_delta
        if delta_i >= 2 * observed_delta:
            s += 1
    
    # Calculate p-value
    p_value = s / num_samples
    
    return p_value

