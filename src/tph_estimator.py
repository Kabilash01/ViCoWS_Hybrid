# src/tph_estimator.py

def estimate_prediction_horizon(headway, vsv, vlv):
    """
    Estimate Prediction Horizon (Tph) using headway and relative speed.
    
    Returns:
        tph (float): Estimated time in seconds
        level (str): 'Critical', 'Warning', or 'Safe'
    """
    try:
        relative_speed = abs(vsv - vlv)
        if relative_speed < 1e-2:
            tph = float('inf')  # Vehicles are moving at the same speed
        else:
            tph = headway / relative_speed
    except ZeroDivisionError:
        tph = float('inf')

    # Interpret risk levels
    if tph < 1.5:
        level = "Critical"
    elif tph < 2.5:
        level = "Warning"
    else:
        level = "Safe"

    return round(tph, 2), level
