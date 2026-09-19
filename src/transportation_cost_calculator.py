"""
Transportation Cost Calculator

Calculates loading capacity and transportation costs
based on product volume/weight and destination distance.
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ============================================================
# Constants
# ============================================================
VOLUME_CAPACITY = 18.5       # m³
WEIGHT_CAPACITY = 2.0        # tons
RATE_PER_TON_KM = 16680      # Rial per ton-km
INSURANCE = 12_000_000       # Rial
RAHDARI_PCT = 0.175          # 17.5%
LOADING_PCT = 0.15           # 15%

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "main.xlsx"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Core calculation functions
# ============================================================
def calculate_quantity_by_volume(volume_m3, vehicle_volume_capacity):
    if volume_m3 <= 0:
        return np.inf
    return vehicle_volume_capacity / volume_m3


def calculate_quantity_by_weight(weight_ton, vehicle_weight_capacity):
    if weight_ton <= 0:
        return np.inf
    return vehicle_weight_capacity / weight_ton


def calculate_final_quantity(
    volume_m3, weight_ton, vehicle_volume_capacity, vehicle_weight_capacity
):
    qv = calculate_quantity_by_volume(volume_m3, vehicle_volume_capacity)
    qw = calculate_quantity_by_weight(weight_ton, vehicle_weight_capacity)
    quantity = min(qv, qw)
    return np.nan if np.isinf(quantity) else quantity


def calculate_loaded_weight(final_quantity, product_weight_ton, vehicle_weight_capacity):
    loaded = final_quantity * product_weight_ton
    return min(loaded, vehicle_weight_capacity)


def identify_limiting_factor(
    volume_m3, weight_ton, vehicle_volume_capacity, vehicle_weight_capacity
):
    if volume_m3 <= 0:
        return "weight"
    if weight_ton <= 0:
        return "volume"

    qv = vehicle_volume_capacity / volume_m3
    qw = vehicle_weight_capacity / weight_ton
    return "volume" if qv <= qw else "weight"


def calculate_base_transportation_cost(loaded_weight_ton, distance_km, rate_per_ton_km):
    weight = max(float(loaded_weight_ton), 0)
    distance = float(distance_km)
    return weight * distance * rate_per_ton_km


def calculate_final_transportation_cost(
    loaded_weight_ton, distance_km, rate_per_ton_km,
    insurance, road_adjustment, loading_adjustment
):
    base = calculate_base_transportation_cost(
        loaded_weight_ton, distance_km, rate_per_ton_km
    )
    subtotal = base + insurance
    return subtotal * (1 + road_adjustment) * (1 + loading_adjustment)


def calc_cost(weight, km):
    """Vectorized cost calculation used in the pipeline."""
    w = np.maximum(np.asarray(weight, dtype=float), 0)
    km = np.asarray(km, dtype=float)
    base = w * km * RATE_PER_TON_KM
    return (base + INSURANCE) * (1 + RAHDARI_PCT) * (1 + LOADING_PCT)


# ============================================================
# Data loading & cleaning
# ============================================================
def load_data(data_path=None):
    if data_path is None:
        data_path = DATA_PATH

    df_loc = pd.read_excel(data_path, sheet_name="Loc")
    df_data = pd.read_excel(data_path, sheet_name="Data")

    # Product data
    df_data = df_data.rename(columns={
        "عنوان گروه ارسال کالا": "shipping_group",
        "کد گروه ارسال کالا": "shipping_group_code",
        "کد کالا": "product_code",
        "نام کالا": "product_name",
        "گروه محصول": "product_group",
        "حجم": "volume_m3",
        "تناژ": "weight_ton",
    })[[
        "shipping_group", "shipping_group_code", "product_code",
        "product_name", "product_group", "volume_m3", "weight_ton"
    ]].copy()

    df_data["volume_m3"] = pd.to_numeric(df_data["volume_m3"], errors="coerce").fillna(0)
    df_data["weight_ton"] = pd.to_numeric(df_data["weight_ton"], errors="coerce").fillna(0)
    df_data = df_data[~((df_data["volume_m3"] <= 0) & (df_data["weight_ton"] <= 0))].copy()

    # Location data
    df_loc = df_loc.rename(columns={
        "منطقه": "region",
        "استان مقصد": "dest_province",
        "شهر مقصد": "dest_city",
        "KM": "km",
    })
    df_loc["km"] = pd.to_numeric(df_loc["km"], errors="coerce")
    df_loc = df_loc.dropna(subset=["km"]).copy()

    return df_data, df_loc


def add_capacity_columns(df_data):
    df = df_data.copy()

    df["final_qty"] = [
        calculate_final_quantity(v, w, VOLUME_CAPACITY, WEIGHT_CAPACITY)
        for v, w in zip(df["volume_m3"], df["weight_ton"])
    ]

    df["loaded_weight_ton"] = [
        calculate_loaded_weight(q, w, WEIGHT_CAPACITY)
        for q, w in zip(df["final_qty"], df["weight_ton"])
    ]

    df["limiting_factor"] = [
        identify_limiting_factor(v, w, VOLUME_CAPACITY, WEIGHT_CAPACITY)
        for v, w in zip(df["volume_m3"], df["weight_ton"])
    ]

    return df


# ============================================================
# Main pipeline
# ============================================================
def run(data_path=None):
    df_data, df_loc = load_data(data_path)
    df_data = add_capacity_columns(df_data)

    # Province median distance
    prov_km = (
        df_loc.groupby(["dest_province", "region"], as_index=False)
        .agg(km_median=("km", "median"))
    )

    # City level
    city_km = df_loc[["dest_province", "dest_city", "region", "km"]].drop_duplicates()

    # Shipping group summary
    group_stats = (
        df_data.groupby(["shipping_group", "shipping_group_code"], as_index=False)
        .agg(
            n_products=("product_code", "count"),
            median_loaded_weight=("loaded_weight_ton", "median"),
            max_loaded_weight=("loaded_weight_ton", "max"),
        )
    )

    print(f"Products : {len(df_data)}")
    print(f"Groups   : {len(group_stats)}")
    print(f"Provinces: {len(prov_km)}")
    print(f"Cities   : {len(city_km)}")

    # 1. Product capacity
    out1 = RESULTS_DIR / "01_Product_Capacity.xlsx"
    df_data.to_excel(out1, index=False)
    print(f"Saved: {out1.name}")

    # 2. Group summary
    out2 = RESULTS_DIR / "02_Group_Summary.xlsx"
    group_stats.to_excel(out2, index=False)
    print(f"Saved: {out2.name}")

    # 3. Group × Province
    df_group_prov = group_stats.merge(prov_km, how="cross")
    df_group_prov["total_cost_rial"] = calc_cost(
        df_group_prov["median_loaded_weight"], df_group_prov["km_median"]
    )
    df_group_prov["total_cost_toman"] = df_group_prov["total_cost_rial"] / 10
    out3 = RESULTS_DIR / "03_Group_x_Province.xlsx"
    df_group_prov.to_excel(out3, index=False)
    print(f"Saved: {out3.name}  shape={df_group_prov.shape}")

    # 4. Group × City
    df_group_city = group_stats.merge(city_km, how="cross")
    df_group_city["total_cost_rial"] = calc_cost(
        df_group_city["median_loaded_weight"], df_group_city["km"]
    )
    df_group_city["total_cost_toman"] = df_group_city["total_cost_rial"] / 10
    out4 = RESULTS_DIR / "04_Group_x_City.xlsx"
    df_group_city.to_excel(out4, index=False)
    print(f"Saved: {out4.name}  shape={df_group_city.shape}")

    # 5. Product × Province
    chunks = []
    chunk_size = 2000
    for i in range(0, len(df_data), chunk_size):
        chunk = df_data.iloc[i:i + chunk_size][[
            "shipping_group", "shipping_group_code", "product_code", "product_name",
            "product_group", "volume_m3", "weight_ton", "final_qty",
            "loaded_weight_ton", "limiting_factor"
        ]]
        merged = chunk.merge(prov_km, how="cross")
        merged["total_cost_rial"] = calc_cost(
            merged["loaded_weight_ton"], merged["km_median"]
        )
        merged["total_cost_toman"] = merged["total_cost_rial"] / 10
        chunks.append(merged)

    df_prod_prov = pd.concat(chunks, ignore_index=True)

    out5_csv = RESULTS_DIR / "05_Product_x_Province_FULL.csv"
    df_prod_prov.to_csv(out5_csv, index=False)
    print(f"Saved: {out5_csv.name}  shape={df_prod_prov.shape}")

    out5_xlsx = RESULTS_DIR / "05_Product_x_Province_Sample.xlsx"
    df_prod_prov.head(30000).to_excel(out5_xlsx, index=False)
    print(f"Saved: {out5_xlsx.name}")

    print("\nDone.")
    return {
        "products": df_data,
        "groups": group_stats,
        "group_province": df_group_prov,
        "group_city": df_group_city,
        "product_province": df_prod_prov,
    }


if __name__ == "__main__":
    run()