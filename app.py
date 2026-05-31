import streamlit as st
import random
import urllib.parse
import math

# --- NATIVE APP THEME STYLING ---
st.set_page_config(
    page_title="Global X N657NK Hub",
    page_icon="✈️",
    layout="wide"
)

# --- APPLICATION DATA BASE ---
AIRPORTS = {
    "KMIA": {"name": "Miami International", "lat": 25.793, "lon": -80.290},
    "KJFK": {"name": "John F. Kennedy Intl", "lat": 40.641, "lon": -73.778},
    "TNCM": {"name": "Princess Juliana Intl", "lat": 18.041, "lon": -63.109},
    "KMCO": {"name": "Orlando International", "lat": 28.429, "lon": -81.309},
    "SPJC": {"name": "Lima Jorge Chávez Intl", "lat": -12.022, "lon": -77.114}, 
    "KSEA": {"name": "Seattle-Tacoma Intl", "lat": 47.449, "lon": -122.309},   
    "PANC": {"name": "Anchorage Stevens Intl", "lat": 61.174, "lon": -150.016},
    "TEXP": {"name": "Hamilton Island", "lat": -20.353, "lon": 148.951},
    "EGLL": {"name": "London Heathrow", "lat": 51.470, "lon": -0.454},
    "MDPC": {"name": "Punta Cana Intl", "lat": 18.567, "lon": -68.363}
}

CHARTER_PROFILES = [
    {
        "client": "NCAA Football Team",
        "roles": ["Head Coach", "Quarterback", "Defensive Coordinator", "Linebacker", "Athletic Trainer", "Equipment Manager", "Booster Member", "Kicker", "Sports Journalist"]
    },
    {
        "client": "U.S. Government Logistics",
        "roles": ["Logistics Commander", "Escort Officer", "Operations Chief", "Medical Coordinator", "Transport Liaison"]
    },
    {
        "client": "Inter Miami CF Support Group",
        "roles": ["Club President", "Ultra Supporter", "VIP Sponsor", "Media Content Creator", "Security Head", "Fan Member"]
    },
    {
        "client": "Cruise Line Crew Rotation",
        "roles": ["Ship Captain", "Chief Engineer", "Hotel Director", "Cruise Director", "Deckhand", "Executive Chef", "Steward"]
    },
    {
        "client": "VIP Music Tour Charter",
        "roles": ["Lead Vocalist", "Guitarist", "Tour Manager", "Audio Engineer", "VIP Guest", "Backstage Coordinator"]
    },
    {
        "client": "International Corporate Summit",
        "roles": ["Chief Executive", "VP of Operations", "Regional Director", "Keynote Speaker", "Board Member"]
    },
    {
        "client": "Formula 1 Pit Crew",
        "roles": ["Team Principal", "Lead Driver", "Race Engineer", "Pit Mechanic", "Tire Specialist", "PR Manager"]
    }
]

# --- MATH CORE ---
def calculate_distance(orig, dest):
    p1, p2 = AIRPORTS[orig], AIRPORTS[dest]
    lat1, lon1, lat2, lon2 = map(math.radians, [p1["lat"], p1["lon"], p2["lat"], p2["lon"]])
    a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2-lon1)/2)**2
    return round(2 * math.asin(math.sqrt(a)) * 3440.065)

def generate_charter_board():
    contracts = []
    current_loc = st.session_state.get("aircraft_location", "KMIA")
    
    # Attempting to generate a rich list of up to 10 options
    for i in range(25): 
        if len(contracts) >= 10:
            break
            
        profile = random.choice(CHARTER_PROFILES)
        orig = random.choice(list(AIRPORTS.keys()))
        dest = random.choice([a for a in AIRPORTS.keys() if a != orig])
        
        client_dist = calculate_distance(orig, dest)
        ferry_dist = calculate_distance(current_loc, orig)
        
        if client_dist > 4000:  # Range Cap expansion for global ports
            continue 
            
        client_time = round((client_dist / 440.0) + 0.3, 1)
        ferry_time = round((ferry_dist / 440.0) + 0.3, 1) if ferry_dist > 30 else 0
        pax_count = random.randint(40, 189)
        
        cargo_weight = round(min(pax_count * 32, 7500) / 1000.0, 1)
        payout = round((client_time * 7800) + (ferry_time * 4500))
        
        contracts.append({
            "id": f"GX{random.randint(100,999)}",
            "client": profile["client"],
            "origin": orig,
            "destination": dest,
            "client_dist": client_dist,
            "ferry_dist": ferry_dist,
            "client_time": client_time,
            "ferry_time": ferry_time,
            "payout": payout,
            "roles_pool": profile["roles"],
            "pax_count": pax_count,
            "cargo_weight": cargo_weight
        })
    return contracts

def generate_manifest(pax_count, roles_pool):
    first_names = ["James", "Mary", "John", "Patricia", "Carlos", "Sofia", "Mateo", "Elena", "Marcus", "Emily"]
    last_names = ["Smith", "Johnson", "Brown", "Garcia", "Miller", "Davis", "Rodriguez", "Lopez"]
    
    first_seats = [f"{r}{l}" for r in range(1, 5) for l in ["A", "C", "D", "F"]]
    economy_seats = []
    for r in range(5, 34):
        for l in ["A", "B", "C", "D", "E", "F"]:
            if len(economy_seats) < 173:
                economy_seats.append(f"{r}{l}")
                
    total_pax = min(pax_count, 189)
    f_count = min(total_pax, 16)
    e_count = total_pax - f_count
    
    assigned_f = random.sample(first_seats, f_count)
    assigned_e = random.sample(economy_seats, e_count)
    manifest = {}
    
    for seat in assigned_f:
        role = roles_pool[0] if roles_pool else "VIP Guest"
        roles_pool = roles_pool[1:] + [roles_pool[0]] if roles_pool else []
        manifest[seat] = {"name": f"{random.choice(first_names)} {random.choice(last_names)}", "role": f"⭐ First Class: {role}"}
        
    for seat in assigned_e:
        role = random.choice(roles_pool) if (roles_pool and random.random() > 0.4) else "Passenger/Staff"
        manifest[seat] = {"name": f"{random.choice(first_names)} {random.choice(last_names)}", "role": role}
        
    return manifest

# --- SESSION INITIALIZATION ---
if "aircraft_location" not in st.session_state:
    st.session_state.aircraft_location = "KMIA"
if "active_contract" not in st.session_state:
    st.session_state.active_contract = None
if "board" not in st.session_state:
    st.session_state.board = generate_charter_board()

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.title("✈️ N657NK Control")

# Location selector fix
airport_list = list(AIRPORTS.keys())
selected_loc = st.sidebar.selectbox(
    "Current Aircraft Location", 
    options=airport_list, 
    index=airport_list.index(st.session_state.aircraft_location)
)
if selected_loc != st.session_state.aircraft_location:
    st.session_state.aircraft_location = selected_loc
    st.session_state.board = generate_charter_board()
    st.rerun()

sb_user = st.sidebar.text_input("SimBrief Username", value="VirtualPilot")

if st.sidebar.button("🔄 Refresh Contract Board", use_container_width=True):
    st.session_state.board = generate_charter_board()
    st.session_state.active_contract = None
    st.rerun()

# --- MAIN APP ROUTING ---
if st.session_state.active_contract is None:
    st.header("Available Charter Contracts Desk")
    st.write(f"Showing up to {len(st.session_state.board)} custom contracts departing from or pairing near your current hub.")
    
    for job in st.session_state.board:
        with st.container(border=True):
            st.markdown(f"### {job['client']}")
            st.caption(f"**ID:** `{job['id']}` | Airframe: `N657NK` (A321ceo)")
            st.write(f"🛣️ **Route:** `{job['origin']}` ➔ `{job['destination']}` ({job['client_dist']} NM)")
            
            # Recalculate ferry leg reactively based on modern position selector
            job['ferry_dist'] = calculate_distance(st.session_state.aircraft_location, job['origin'])
            job['ferry_time'] = round((job['ferry_dist'] / 440.0) + 0.3, 1) if job['ferry_dist'] > 30 else 0
            
            if job['ferry_time'] > 0:
                st.warning(f"✈️ Ferry Required: {st.session_state.aircraft_location} ➔ {job['origin']} (+{job['ferry_time']}h)")
            else:
                st.success(f"✅ On-site at {job['origin']}")
                
            st.markdown(f"**Payout:** ${job['payout']:,}")
            if st.button("Accept & Inspect Flight", key=job['id'], use_container_width=True):
                st.session_state.active_contract = job
                st.session_state.manifest = generate_manifest(job['pax_count'], job['roles_pool'])
                st.rerun()
else:
    job = st.session_state.active_contract
    st.header(f"Active Dispatch: {job['id']}")
    st.subheader(job['client'])
    
    if st.button("⬅️ Decline/Return to Board", use_container_width=True):
        st.session_state.active_contract = None
        st.rerun()
        
    if st.button("🏁 Log Flight Complete (Relocate Plane)", type="primary", use_container_width=True):
        st.session_state.aircraft_location = job['destination']
        st.session_state.active_contract = None
        st.session_state.board = generate_charter_board()
        st.rerun()

    with st.container(border=True):
        st.markdown("##### ⚙️ Configuration Profile")
        st.write
