# Test rental affordability
import json, sys
sys.path.insert(0, "src")

# Import and test
from rental_agent import __version__
print(f"Rental Agent v{__version__}")

# Test affordability calculation
from rental_agent.server import rental_affordability
import asyncio

async def test():
    result = await rental_affordability(85000, 500)
    data = json.loads(result)
    assert data["max_rent_30_percent"] > 0
    assert data["monthly_gross"] == 7083.33
    print(f"✅ Affordability test passed: ${data['max_rent_30_percent']}/mo max rent")
    
    # Test roommate calculator
    roommate_result = await rental_roommate_calculator(3000, json.dumps([
        {"name": "Alice", "room_size_sqft": 200, "income": 80000},
        {"name": "Bob", "room_size_sqft": 150, "income": 60000},
    ]), "combined")
    rdata = json.loads(roommate_result)
    assert len(rdata["splits"]) == 2
    total = sum(s["rent"] for s in rdata["splits"])
    assert abs(total - 3000) < 1
    print(f"✅ Roommate test passed: ${total:.2f} total (should be $3,000)")

# Need the actual function reference
from rental_agent.server import rental_roommate_calculator, rental_affordability
asyncio.run(test())
