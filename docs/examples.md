# Examples

## 1. Full Apartment Hunting Workflow

An AI agent helping a user find an apartment in Austin, TX:

```
User: "I'm moving to Austin for a job paying $85,000. Need a 2BR under $2,000."

Agent actions:
1. rental_affordability(85000) → max rent ~$2,125/mo
2. rental_search_listings("Austin TX", max_price=2000, bedrooms=2)
3. rental_neighborhood_report("Downtown Austin")
4. rental_commute_analysis("Downtown Austin", "Silicon Hills")
5. rental_market_trends("Austin, TX")
```

## 2. Comparing Two Apartments

```
User: "Which is better: $1,800 1BR in Brooklyn or $2,200 2BR in Queens?"

Agent:
rental_compare([
  {"name": "Brooklyn 1BR", "price": 1800, "bedrooms": 1, "sqft": 600, "neighborhood": "Brooklyn"},
  {"name": "Queens 2BR", "price": 2200, "bedrooms": 2, "sqft": 900, "neighborhood": "Queens"}
])
```

## 3. Roommate Rent Split

```
User: "Three of us renting a $3,000 apartment. Alice has the master (200 sqft), 
Bob has medium (150 sqft), I have small (100 sqft). Alice makes $80k, 
Bob makes $60k, I make $50k. What's fair?"

Agent:
rental_roommate_calculator(3000, [
  {"name": "Alice", "room_size_sqft": 200, "income": 80000},
  {"name": "Bob", "room_size_sqft": 150, "income": 60000},
  {"name": "You", "room_size_sqft": 100, "income": 50000}
], "combined")
```

## 4. Lease Review

```
User: "I got a lease. Can you check it for red flags?"

Agent: rental_lease_analyzer(lease_text)

The analyzer checks for:
✓ Late fees
✓ Pet fees/deposits
✓ Subleasing restrictions
✓ Guest policies
✓ Eviction clauses
✓ Inspection notice periods
✓ Utility inclusions
✓ Maintenance terms
✓ Renewal terms
✓ Early termination clauses
```
