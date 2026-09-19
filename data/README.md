# Data

This folder contains the input data required to run the calculator.

## Expected file

**File:** `main.xlsx`

The workbook must contain two sheets:

### Sheet: `Data`
Product master data.

| Original column (Persian) | Used as | Description |
|---------------------------|---------|-------------|
| عنوان گروه ارسال کالا | shipping_group | Shipping group name |
| کد گروه ارسال کالا | shipping_group_code | Shipping group code |
| کد کالا | product_code | Product code |
| نام کالا | product_name | Product name |
| گروه محصول | product_group | Product category |
| حجم | volume_m3 | Volume in m³ |
| تناژ | weight_ton | Weight in tons |

Rows where both volume and weight are zero (or missing) are excluded during processing.

### Sheet: `Loc`
Destination distances.

| Original column (Persian) | Used as | Description |
|---------------------------|---------|-------------|
| منطقه | region | Region |
| استان مقصد | dest_province | Destination province |
| شهر مقصد | dest_city | Destination city |
| KM | km | Distance in kilometers |

Rows with non-numeric or missing KM values are dropped.

## Notes

- Real operational data is proprietary and is not published in this repository.
- Place your own `main.xlsx` in this folder (or in `data/raw/`) before running the scripts.