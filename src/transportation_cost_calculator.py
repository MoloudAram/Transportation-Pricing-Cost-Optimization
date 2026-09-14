"""
Transportation Cost Calculator

Reusable calculation functions for the transportation
pricing and cost optimization project.
"""

import numpy as np


def calculate_quantity_by_volume(
    volume_m3,
    vehicle_volume_capacity
):
    """
    Calculate maximum loading quantity based on vehicle volume.
    """
    if volume_m3 <= 0:
        return np.inf

    return vehicle_volume_capacity / volume_m3


def calculate_quantity_by_weight(
    weight_ton,
    vehicle_weight_capacity
):
    """
    Calculate maximum loading quantity based on vehicle weight.
    """
    if weight_ton <= 0:
        return np.inf

    return vehicle_weight_capacity / weight_ton


def calculate_final_quantity(
    volume_m3,
    weight_ton,
    vehicle_volume_capacity,
    vehicle_weight_capacity
):
    """
    Calculate feasible loading quantity based on
    both volume and weight constraints.
    """

    quantity_by_volume = calculate_quantity_by_volume(
        volume_m3,
        vehicle_volume_capacity
    )

    quantity_by_weight = calculate_quantity_by_weight(
        weight_ton,
        vehicle_weight_capacity
    )

    quantity = min(
        quantity_by_volume,
        quantity_by_weight
    )

    if np.isinf(quantity):
        return np.nan

    return quantity


def calculate_loaded_weight(
    final_quantity,
    product_weight_ton,
    vehicle_weight_capacity
):
    """
    Calculate loaded weight while respecting
    vehicle weight capacity.
    """

    loaded_weight = (
        final_quantity *
        product_weight_ton
    )

    return min(
        loaded_weight,
        vehicle_weight_capacity
    )


def identify_limiting_factor(
    volume_m3,
    weight_ton,
    vehicle_volume_capacity,
    vehicle_weight_capacity
):
    """
    Identify whether volume or weight is the
    primary loading constraint.
    """

    if volume_m3 <= 0:
        return "weight"

    if weight_ton <= 0:
        return "volume"

    quantity_by_volume = (
        vehicle_volume_capacity /
        volume_m3
    )

    quantity_by_weight = (
        vehicle_weight_capacity /
        weight_ton
    )

    if quantity_by_volume <= quantity_by_weight:
        return "volume"

    return "weight"


def calculate_base_transportation_cost(
    loaded_weight_ton,
    distance_km,
    rate_per_ton_km
):
    """
    Calculate base transportation cost.
    """

    weight = max(
        float(loaded_weight_ton),
        0
    )

    distance = float(distance_km)

    return (
        weight *
        distance *
        rate_per_ton_km
    )


def calculate_final_transportation_cost(
    loaded_weight_ton,
    distance_km,
    rate_per_ton_km,
    insurance,
    road_adjustment,
    loading_adjustment
):
    """
    Calculate final transportation cost.

    Commercial parameters are passed as arguments
    instead of being hard-coded.
    """

    base_cost = calculate_base_transportation_cost(
        loaded_weight_ton,
        distance_km,
        rate_per_ton_km
    )

    subtotal = (
        base_cost +
        insurance
    )

    return (
        subtotal *
        (1 + road_adjustment) *
        (1 + loading_adjustment)
    )