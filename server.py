#!/usr/bin/env python3
"""Rental Agent MCP — AI-powered rental search, analysis, and neighborhood intelligence."""

import json, re, math, urllib.parse
from datetime import datetime
from mcp.server import Server, stdio_server
import httpx

server = Server("rental-agent-mcp")

# ─── OSM Overpass API helpers ────────────────────────────────────────────────

async def _osm_query(query):
    """Query OpenStreetMap Overpass API."""
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post("https://overpass-api.de/api/interpreter", data={"data": query})
        resp.raise_for_status()
        return resp.json()

async def _geocode_location(location):
    """Geocode a location name to lat/lon using Nominatim."""
    headers = {"User-Agent": "RentalAgentMCP/1.0 (jackpost1388@wshu.net)"}
    params = {"q": location, "format": "json", "limit": 1}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get("https://nominatim.openstreetmap.org/search", params=params, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]
    return None, None, None

async def _search_web(query, max_results=5):
    """Search the web for rental listings."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    params = {"q": query, "format": "json"}
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        try:
            resp = await client.get("https://api.duckduckgo.com/", params={**params, "no_html": "1", "skip_disambig": "1"}, headers=headers)
            data = resp.json()
            results = []
            # Parse abstract
            if data.get("AbstractText"):
                results.append({"title": data.get("Heading", ""), "snippet": data["AbstractText"], "source": data.get("AbstractSource", "")})
            # Parse related topics
            for topic in data.get("RelatedTopics", [])[:max_results]:
                if "Text" in topic:
                    results.append({"title": topic.get("Text", "")[:100], "snippet": topic.get("Text", "")})
                elif "Topics" in topic:
                    for sub in topic["Topics"][:3]:
                        results.append({"title": sub.get("Text", "")[:100], "snippet": sub.get("Text", "")})
            return results
        except:
            return []

# ─── Tools ───────────────────────────────────────────────────────────────────

@server.tool(
    name="rental_search_listings",
    description="Search for rental listings in a city or area. Returns current listings from web search.",
    input_schema={
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City, state or neighborhood (e.g. 'Austin TX', 'Brooklyn NY')"},
            "min_price": {"type": "integer", "description": "Minimum monthly rent"},
            "max_price": {"type": "integer", "description": "Maximum monthly rent"},
            "bedrooms": {"type": "integer", "description": "Number of bedrooms"},
            "max_results": {"type": "integer", "description": "Max results", "default": 5}
        },
        "required": ["location"]
    }
)
async def rental_search_listings(location: str, min_price: int = None, max_price: int = None, bedrooms: int = None, max_results: int = 5) -> str:
    try:
        query = f"apartments for rent in {location}"
        if bedrooms: query += f" {bedrooms} bedroom"
        if min_price: query += f" ${min_price}"
        if max_price: query += f" under ${max_price}"
        
        results = await _search_web(query, max_results)
        
        return json.dumps({
            "location": location,
            "query": query,
            "results": results[:max_results] if results else ["No rental listings found via web search. Try a different location or use a rental site directly."],
            "note": "Results are from web search. For best results, use rental sites like Zillow, Apartments.com, or Realtor.com."
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "isError": True}, indent=2)

@server.tool(
    name="rental_neighborhood_report",
    description="Get a comprehensive neighborhood report: amenities, transit, safety context, schools, and demographics.",
    input_schema={
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "Neighborhood or city (e.g. 'Williamsburg Brooklyn', 'Downtown Austin')"}
        },
        "required": ["location"]
    }
)
async def rental_neighborhood_report(location: str) -> str:
    try:
        lat, lon, display = await _geocode_location(location)
        if not lat:
            return json.dumps({"error": f"Could not geocode '{location}'", "isError": True}, indent=2)
        
        # Get nearby amenities via OSM
        radius = 1000  # meters
        amenity_query = f"""
        [out:json];
        (
            node["amenity"~"restaurant|cafe|bar|pub|supermarket|gym|park|school|hospital|pharmacy|bank|library"]({lat-radius/111000},{lon-radius/111000},{lat+radius/111000},{lon+radius/111000});
            way["amenity"~"restaurant|cafe|bar|pub|supermarket|gym|park|school|hospital|pharmacy|bank|library"]({lat-radius/111000},{lon-radius/111000},{lat+radius/111000},{lon+radius/111000});
        );
        out center;
        """
        amenities_data = await _osm_query(amenity_query)
        
        # Count amenities by type
        amenity_counts = {}
        for element in amenities_data.get("elements", []):
            a_type = element.get("tags", {}).get("amenity", "other")
            amenity_counts[a_type] = amenity_counts.get(a_type, 0) + 1
        
        # Get transit stops
        transit_query = f"""
        [out:json];
        (
            node["highway"="bus_stop"]({lat-radius/111000},{lon-radius/111000},{lat+radius/111000},{lon+radius/111000});
            node["railway"="station"]({lat-radius/111000},{lon-radius/111000},{lat+radius/111000},{lon+radius/111000});
            node["station"="subway"]({lat-radius/111000},{lon-radius/111000},{lat+radius/111000},{lon+radius/111000});
        );
        out count;
        """
        transit_data = await _osm_query(transit_query)
        transit_count = len(transit_data.get("elements", []))
        
        # Nearby parks
        park_query = f"""
        [out:json];
        (
            way["leisure"="park"]({lat-radius/111000},{lon-radius/111000},{lat+radius/111000},{lon+radius/111000});
            relation["leisure"="park"]({lat-radius/111000},{lon-radius/111000},{lat+radius/111000},{lon+radius/111000});
        );
        out count;
        """
        park_data = await _osm_query(park_query)
        park_count = len(park_data.get("elements", []))
        
        return json.dumps({
            "neighborhood": display[:100] if display else location,
            "coordinates": {"lat": round(lat, 4), "lon": round(lon, 4)},
            "walkability": {
                "restaurants": amenity_counts.get("restaurant", 0),
                "cafes": amenity_counts.get("cafe", 0),
                "bars": amenity_counts.get("bar", 0) + amenity_counts.get("pub", 0),
                "supermarkets": amenity_counts.get("supermarket", 0),
                "gyms": amenity_counts.get("gym", 0),
                "parks_nearby": park_count,
                "pharmacies": amenity_counts.get("pharmacy", 0),
                "libraries": amenity_counts.get("library", 0),
            },
            "transit": {"transit_stops_nearby": transit_count, "note": "Includes bus stops, train/subway stations within ~1km"},
            "schools_nearby": amenity_counts.get("school", 0),
            "hospitals_nearby": amenity_counts.get("hospital", 0),
            "walkability_note": "Higher amenity counts = more walkable. 5+ restaurants + cafes in 1km = very walkable.",
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "isError": True}, indent=2)

@server.tool(
    name="rental_affordability",
    description="Calculate how much rent you can afford based on income and expenses.",
    input_schema={
        "type": "object",
        "properties": {
            "annual_income": {"type": "number", "description": "Your annual pre-tax income in USD"},
            "monthly_debt": {"type": "number", "description": "Monthly debt payments (loans, credit cards)", "default": 0},
            "rule": {"type": "string", "enum": ["30_percent", "50_30_20", "custom"], "description": "Budget rule to use", "default": "30_percent"}
        },
        "required": ["annual_income"]
    }
)
async def rental_affordability(annual_income: float, monthly_debt: float = 0, rule: str = "30_percent") -> str:
    try:
        monthly_gross = annual_income / 12
        monthly_net = monthly_gross * 0.75  # Approximate take-home after tax
        
        if rule == "30_percent":
            max_rent = monthly_gross * 0.30
            after_debt = max_rent - monthly_debt
            safe_rent = max(0, after_debt)
            return json.dumps({
                "annual_income": annual_income,
                "monthly_gross": round(monthly_gross, 2),
                "monthly_net_estimate": round(monthly_net, 2),
                "rule": "30% of gross income",
                "max_rent_30_percent": round(max_rent, 2),
                "monthly_debt": monthly_debt,
                "safe_rent_after_debt": round(safe_rent, 2),
                "recommendation": f"Based on the 30% rule, you can afford up to ${max_rent:,.0f}/month rent. After debt payments, a safe budget is ${safe_rent:,.0f}/month.",
                "note": "This is a guideline. Landlords typically require income ≥ 3x rent."
            }, indent=2)
        
        elif rule == "50_30_20":
            needs_budget = monthly_net * 0.50
            max_rent = needs_budget - monthly_debt
            safe_rent = max(0, max_rent * 0.60)  # Rent should be ~60% of needs budget
            return json.dumps({
                "annual_income": annual_income,
                "monthly_net_estimate": round(monthly_net, 2),
                "rule": "50/30/20 budget: 50% needs, 30% wants, 20% savings",
                "needs_budget_total": round(needs_budget, 2),
                "max_rent_in_needs": round(max(0, max_rent), 2),
                "recommended_rent": round(safe_rent, 2),
                "recommendation": f"With the 50/30/20 rule and estimated take-home of ${monthly_net:,.0f}/mo, you have ${needs_budget:,.0f} for all needs. Recommended rent: ${safe_rent:,.0f}/mo."
            }, indent=2)
        
        else:
            return json.dumps({"error": "Unknown budget rule", "isError": True}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "isError": True}, indent=2)

@server.tool(
    name="rental_compare",
    description="Compare multiple rental options side by side with scores.",
    input_schema={
        "type": "object",
        "properties": {
            "listings_json": {"type": "string", "description": "JSON array of listings: [{\"name\":\"...\",\"price\":2000,\"bedrooms\":2,\"sqft\":1000,\"neighborhood\":\"...\"}]"}
        },
        "required": ["listings_json"]
    }
)
async def rental_compare(listings_json: str) -> str:
    try:
        listings = json.loads(listings_json)
        if not listings:
            return json.dumps({"error": "No listings provided", "isError": True}, indent=2)
        
        analyzed = []
        for i, l in enumerate(listings):
            price = l.get("price", 0)
            bedrooms = l.get("bedrooms", 1)
            sqft = l.get("sqft", 0)
            
            price_per_bed = price / max(bedrooms, 1)
            price_per_sqft = price / max(sqft, 1) if sqft > 0 else 0
            
            # Score (0-100): lower price = better, more space = better
            score = 50  # baseline
            if price < 1500: score += 15
            elif price < 2500: score += 5
            elif price > 4000: score -= 10
            if bedrooms >= 2: score += 5
            if sqft > 800: score += 5
            if price_per_sqft < 2: score += 10
            elif price_per_sqft > 4: score -= 5
            
            analyzed.append({
                "name": l.get("name", f"Option {i+1}"),
                "price": price,
                "bedrooms": bedrooms,
                "sqft": sqft,
                "price_per_bedroom": round(price_per_bed, 2),
                "price_per_sqft": round(price_per_sqft, 2),
                "score": min(100, max(0, score)),
            })
        
        # Sort by score descending
        analyzed.sort(key=lambda x: x["score"], reverse=True)
        
        return json.dumps({
            "comparison": analyzed,
            "best_option": analyzed[0]["name"] if analyzed else None,
            "best_score": analyzed[0]["score"] if analyzed else 0,
        }, indent=2)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON format. Expected: [{\"name\":\"...\",\"price\":2000,...}]", "isError": True}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "isError": True}, indent=2)

@server.tool(
    name="rental_roommate_calculator",
    description="Calculate fair rent split between roommates based on room size, income, or custom factors.",
    input_schema={
        "type": "object",
        "properties": {
            "total_rent": {"type": "number", "description": "Total monthly rent"},
            "roommates_json": {"type": "string", "description": "JSON: [{\"name\":\"Alice\",\"room_size_sqft\":150,\"income\":50000},{\"name\":\"Bob\",\"room_size_sqft\":120,\"income\":60000}]"},
            "method": {"type": "string", "enum": ["equal", "by_room", "by_income", "combined"], "default": "by_room"}
        },
        "required": ["total_rent", "roommates_json"]
    }
)
async def rental_roommate_calculator(total_rent: float, roommates_json: str, method: str = "by_room") -> str:
    try:
        roommates = json.loads(roommates_json)
        if not roommates:
            return json.dumps({"error": "No roommates provided", "isError": True}, indent=2)
        
        if method == "equal":
            share = total_rent / len(roommates)
            splits = [{"name": r["name"], "rent": round(share, 2), "percentage": round(100/len(roommates), 1)} for r in roommates]
        
        elif method == "by_room":
            total_sqft = sum(r.get("room_size_sqft", 100) for r in roommates)
            if total_sqft == 0: total_sqft = len(roommates) * 100
            splits = []
            for r in roommates:
                share = total_rent * r.get("room_size_sqft", 100) / total_sqft
                splits.append({"name": r["name"], "room_sqft": r.get("room_size_sqft", 100), "rent": round(share, 2), "percentage": round(share/total_rent*100, 1)})
        
        elif method == "by_income":
            total_income = sum(r.get("income", 50000) for r in roommates)
            if total_income == 0: total_income = len(roommates) * 50000
            splits = []
            for r in roommates:
                share = total_rent * r.get("income", 50000) / total_income
                splits.append({"name": r["name"], "income": r.get("income", 0), "rent": round(share, 2), "percentage": round(share/total_rent*100, 1)})
        
        else:  # combined: 50% by room, 50% by income
            total_sqft = sum(r.get("room_size_sqft", 100) for r in roommates)
            total_income = sum(r.get("income", 50000) for r in roommates)
            if total_sqft == 0: total_sqft = len(roommates) * 100
            if total_income == 0: total_income = len(roommates) * 50000
            splits = []
            for r in roommates:
                room_share = total_rent * 0.5 * r.get("room_size_sqft", 100) / total_sqft
                income_share = total_rent * 0.5 * r.get("income", 50000) / total_income
                splits.append({"name": r["name"], "rent": round(room_share + income_share, 2), "percentage": round((room_share+income_share)/total_rent*100, 1), "room_share": round(room_share, 2), "income_share": round(income_share, 2)})
        
        return json.dumps({"total_rent": total_rent, "method": method, "splits": splits}, indent=2)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON format for roommates", "isError": True}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "isError": True}, indent=2)

@server.tool(
    name="rental_lease_analyzer",
    description="Analyze a lease document for key terms, fees, and red flags.",
    input_schema={
        "type": "object",
        "properties": {
            "lease_text": {"type": "string", "description": "Full text of the lease agreement"}
        },
        "required": ["lease_text"]
    }
)
async def rental_lease_analyzer(lease_text: str) -> str:
    try:
        text = lease_text.lower()
        analysis = {
            "terms": {},
            "fees": [],
            "red_flags": [],
            "key_clauses": [],
        }
        
        # Rent amount
        rent_match = re.search(r'rent[:\s]*\$?([\d,]+(?:\.\d{2})?)', text)
        if rent_match: analysis["terms"]["monthly_rent"] = rent_match.group(1)
        
        # Lease duration
        duration_match = re.search(r'(\d+)[-\s]?(month|year)[-\s]?(lease|term)', text)
        if duration_match: analysis["terms"]["lease_term"] = f"{duration_match.group(1)} {duration_match.group(2)}"
        
        # Security deposit
        deposit_match = re.search(r'(security deposit|deposit)[:\s]*\$?([\d,]+)', text)
        if deposit_match: analysis["terms"]["security_deposit"] = deposit_match.group(2)
        
        # Late fee
        if 'late fee' in text or 'late payment' in text:
            fee_match = re.search(r'late (fee|payment)[:\s]*\$?([\d,]+)', text)
            analysis["fees"].append(f"Late fee: ${fee_match.group(2) if fee_match else 'Check lease'}")
        
        # Pet fee
        if 'pet' in text:
            pet_match = re.search(r'pet (fee|deposit|rent)[:\s]*\$?([\d,]+)', text)
            analysis["fees"].append(f"Pet fee: ${pet_match.group(2) if pet_match else 'Present - check amount'}")
        
        # Red flags
        if 'no sublease' in text or 'no subletting' in text:
            analysis["red_flags"].append("No subleasing allowed — can't rent out if you leave")
        if 'no guests' in text or 'guest' in text and 'limit' in text:
            analysis["red_flags"].append("Guest restrictions — check guest policy")
        if 'eviction' in text:
            analysis["red_flags"].append("Eviction clauses present — review grounds for eviction carefully")
        if 'inspection' in text and '24' not in text and '48' not in text:
            analysis["red_flags"].append("Short/no notice for inspections — check your state's minimum notice requirement")
        
        # Key clauses
        if 'utilities' in text:
            analysis["key_clauses"].append("Utilities clause present — check what's included")
        if 'parking' in text:
            analysis["key_clauses"].append("Parking clause present")
        if 'maintenance' in text or 'repair' in text:
            analysis["key_clauses"].append("Maintenance/repair clause present")
        if 'renew' in text:
            analysis["key_clauses"].append("Renewal terms present")
        if 'terminat' in text:
            analysis["key_clauses"].append("Termination/break clause present")
        
        if not analysis["red_flags"]:
            analysis["red_flags"].append("No obvious red flags detected (but this is not legal advice)")
        
        return json.dumps(analysis, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "isError": True}, indent=2)

@server.tool(
    name="rental_commute_analysis",
    description="Estimate commute time and cost between a location and workplace.",
    input_schema={
        "type": "object",
        "properties": {
            "from_location": {"type": "string", "description": "Your rental location or neighborhood"},
            "to_location": {"type": "string", "description": "Your workplace or destination"},
            "commute_days_per_month": {"type": "integer", "description": "Days you commute per month", "default": 20}
        },
        "required": ["from_location", "to_location"]
    }
)
async def rental_commute_analysis(from_location: str, to_location: str, commute_days_per_month: int = 20) -> str:
    try:
        # Geocode both locations
        from_lat, from_lon, from_display = await _geocode_location(from_location)
        to_lat, to_lon, to_display = await _geocode_location(to_location)
        
        if not from_lat or not to_lat:
            return json.dumps({"error": "Could not geocode one or both locations", "isError": True}, indent=2)
        
        # Calculate straight-line distance (km)
        dlat = to_lat - from_lat
        dlon = to_lon - from_lon
        a = math.sin(dlat/2)**2 + math.cos(from_lat) * math.cos(to_lat) * math.sin(dlon/2)**2
        distance_km = 6371 * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance_mi = distance_km * 0.621371
        
        # Estimate drive time (~50 km/h average city speed)
        drive_min = distance_km / 50 * 60
        
        # Estimate transit time (~30 km/h average)
        transit_min = distance_km / 30 * 60 + 10  # +10 for walking/waiting
        
        # Monthly cost estimate (driving: $0.60/mile IRS rate)
        monthly_miles = distance_mi * 2 * commute_days_per_month
        driving_cost = monthly_miles * 0.60
        transit_cost = distance_km * 2 * commute_days_per_month * 0.15  # ~$0.15/km transit
        
        return json.dumps({
            "from": from_display[:100],
            "to": to_display[:100],
            "distance_km": round(distance_km, 1),
            "distance_miles": round(distance_mi, 1),
            "estimated_drive_time_minutes": round(drive_min),
            "estimated_transit_time_minutes": round(transit_min),
            "monthly_cost_estimate": {
                "driving": round(driving_cost, 2),
                "transit": round(transit_cost, 2),
            },
            "note": "Estimates based on straight-line distance. Actual times depend on routes and traffic."
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "isError": True}, indent=2)

@server.tool(
    name="rental_market_trends",
    description="Get rental market trends and price comparisons for a city.",
    input_schema={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name (e.g. 'Austin, TX')"}
        },
        "required": ["city"]
    }
)
async def rental_market_trends(city: str) -> str:
    try:
        results = await _search_web(f"average rent in {city} 2024 2025 apartment", 3)
        
        trends = {
            "city": city,
            "source": "Web search results below",
            "note": "For accurate current data, check Zillow Rent Index, ApartmentList, or Rent.com.",
            "web_results": results[:3],
            "estimated_affordability": {},
        }
        
        # Income estimates for major cities
        income_estimates = {
            "new york": 85000, "san francisco": 120000, "los angeles": 75000,
            "chicago": 65000, "austin": 75000, "seattle": 85000, "boston": 80000,
            "denver": 70000, "miami": 60000, "portland": 65000, "nashville": 60000,
            "atlanta": 62000, "phoenix": 58000, "dallas": 65000, "houston": 60000,
        }
        
        city_lower = city.lower().split(",")[0].strip()
        for key, income in income_estimates.items():
            if key in city_lower or city_lower in key:
                trends["estimated_affordability"] = {
                    "median_income_estimate": income,
                    "max_affordable_rent_30_percent": round(income / 12 * 0.30),
                }
                break
        
        return json.dumps(trends, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "isError": True}, indent=2)

def main():
    import anyio
    async def run():
        async with stdio_server() as streams:
            await server.run(streams[0], streams[1], server.create_initialization_options())
    anyio.run(run)

if __name__ == "__main__":
    main()
