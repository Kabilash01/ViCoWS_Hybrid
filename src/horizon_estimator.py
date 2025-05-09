def estimate_prediction_horizon(headway_m, vsv_kmh):
    if vsv_kmh <= 0:
        return float('inf')  # Vehicle is stopped
    vsv_ms = vsv_kmh / 3.6
    time_to_collision = headway_m / vsv_ms
    return time_to_collision