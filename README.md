# Transportation Pricing & Cost Optimization

## Real-World Logistics Analytics Case Study

A real-world logistics analytics case study focused on transportation
capacity planning, freight cost calculation, and pricing standardization.

---

## Business Problem

Transportation pricing in large-scale logistics operations can become
complex when multiple factors influence the final cost, including:

- Product dimensions and weight
- Vehicle capacity
- Transportation distance
- Destination
- Shipping group
- Loading and unloading costs
- Road transportation charges

The objective was to develop a structured and transparent pricing
calculation framework that could support logistics planning and
transportation cost optimization.

---

## Analytical Approach

The solution follows the following workflow:

1. Product Master Data Preparation
2. Volume & Weight Analysis
3. Vehicle Capacity Constraint Analysis
4. Loading Quantity Calculation
5. Limiting Factor Detection
6. Destination & Distance Mapping
7. Transportation Cost Calculation
8. Shipping Group × Province Pricing
9. Shipping Group × City Pricing
10. Product × Province Pricing
11. Standardized Pricing Tables

---

## Business Logic

The maximum loading quantity is determined by the limiting vehicle
capacity constraint:

- Volume capacity
- Weight capacity

The effective loading quantity is determined by whichever constraint
is reached first.

This allows the model to identify whether transportation efficiency
is primarily constrained by volume or weight.

---

## Technology

- Python
- Pandas
- NumPy
- Excel
- Data Analysis
- Logistics Analytics
- Transportation Cost Modeling

---

## Project Structure

...
