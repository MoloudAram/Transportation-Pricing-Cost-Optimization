# Business Insights

This section summarizes the main practical findings that can be drawn from the transportation cost model.

## Capacity Constraints

Most products fall into one of two categories:

- **Volume-limited**: the truck fills up by space before reaching the weight limit. These products leave unused weight capacity.
- **Weight-limited**: the truck reaches the 2-ton limit while still having free volume.

Knowing the dominant constraint for each product (and shipping group) helps in two ways:
- Better load planning when mixing different products on the same truck.
- Identifying products that systematically under-utilize the vehicle.

## Cost Drivers

Transportation cost is driven mainly by two factors:

1. **Loaded weight** – heavier effective loads increase the base cost.
2. **Distance** – longer routes (especially to distant provinces) raise the cost significantly.

Because insurance and the percentage-based surcharges are applied on top of the base cost, long-distance shipments become disproportionately expensive.

## Province vs City Level

- Province-level costs (using median distance) are useful for high-level planning and budgeting.
- City-level costs show meaningful differences inside the same province. In some cases the cost gap between two cities in one province is large enough to affect pricing decisions.

## Shipping Group Perspective

Grouping products by shipping group reduces the number of combinations and makes the cost matrix more manageable for commercial teams. The median loaded weight of the group is a reasonable proxy for typical shipments of that group.

## Practical Uses

The outputs can support:

- Setting or reviewing freight rates by destination
- Comparing the cost of shipping different product groups to the same region
- Spotting destinations that are structurally expensive
- Estimating the impact of changes in product mix or packaging (volume/weight)

## Limitations

- The model assumes one vehicle type (Khawar).
- No multi-stop routes or return loads are considered.
- Actual commercial rates are not published here; only the calculation logic is shown.

These insights are based on the structure of the data and the cost formula. Actual numbers will vary with the specific product and location files used.