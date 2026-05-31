import streamlit as st
import random
import urllib.parse
import math
from datetime import datetime

# --- NATIVE APP THEME STYLING ---
st.set_page_config(
    page_title="Global X N657NK Hub",
    page_icon="✈️",
    layout="wide"
)

# --- EXPANDED EXACT AIRPORT DATABASE ---
AIRPORTS = {
    "KMIA": {"name": "Miami International", "lat": 25.793, "lon": -80.290, "region": "AMER", "subregion": "FL"},
    "KMCO": {"name": "Orlando International", "lat": 28.429, "lon": -81.309, "region": "AMER", "subregion": "FL"},
    "KJFK": {"name": "John F. Kennedy Intl", "lat": 40.641, "lon": -73.778, "region": "AMER", "subregion": "NY"},
    "KSEA": {"name": "Seattle-Tacoma Intl", "lat": 47.449, "lon": -122.309, "region": "AMER", "subregion": "WEST"},   
    "KABQ": {"name": "Albuquerque Sunport", "lat": 35.040, "lon": -106.609, "region": "AMER", "subregion": "WEST"},
    "PANC": {"name": "Anchorage Stevens Intl", "lat": 61.174, "lon": -150.016, "region": "AMER", "subregion": "WEST"},
    "KRDU": {"name": "Raleigh-Durham Intl", "lat": 35.877, "lon": -78.787, "region": "AMER", "subregion": "CAROLINAS"},
    "KRIC": {"name": "Richmond International", "lat": 37.505, "lon": -77.320, "region": "AMER", "subregion": "VIRGINIA"},
    "KMSY": {"name": "Louis Armstrong New Orleans", "lat": 29.993, "lon": -90.258, "region": "AMER", "subregion": "SOUTH"},
    "TNCM": {"name": "Princess Juliana Intl", "lat": 18.041, "lon": -63.109, "region": "AMER", "subregion": "CARIB"},
    "MDPC": {"name": "Punta Cana Intl", "lat": 18.567, "lon": -68.363, "region": "AMER", "subregion": "CARIB"},
    "SPJC": {"name": "Lima Jorge Chávez Intl", "lat": -12.022, "lon": -77.114, "region": "AMER", "subregion": "SOUTHAMER"}, 
    "EGLL": {"name": "London Heathrow", "lat": 51.470, "lon": -0.454, "region": "EUR", "subregion": "EUR"},
    "FDSK": {"name": "King Mswati III Intl", "lat": -26.357, "lon": 31.717, "region": "AFR", "subregion": "AFR"},
    "FAOR": {"name": "OR Tambo Intl (Joburg)", "lat": -26.139, "lon": 28.246, "region": "AFR", "subregion": "AFR"},
    "FACT": {"name": "Cape Town International", "lat": -33.964, "lon": 18.602, "region": "AFR", "subregion": "AFR"}
}

# --- HYPER-LOCALIZED SPORT & CORPORATE TEAMS ---
SUBREGION_PROFILES = {
    "CAROLINAS": [
        {"client": "Duke Blue Devils Men's Basketball (NCAA)", "roles": ["Jon Scheyer", "Starting Point Guard", "Shooting Guard", "Director of Basketball Ops", "Athletic Trainer"]},
        {"client": "NC State Wolfpack Football (NCAA)", "roles": ["Head Coach", "Starting Quarterback", "Linebacker", "Running Back", "Equipment Manager", "Booster Member"]},
        {"client": "Carolina Hurricanes (NHL)", "roles": ["Rod Brind'Amour", "Team Captain", "Starting Goalie", "Equipment Manager", "Physical Therapist"]}
    ],
    "VIRGINIA": [
        {"client": "VCU Rams Basketball (NCAA)", "roles": ["Head Coach", "Starting Guard", "Forward", "Athletic Trainer", "Athletics Director"]},
        {"client": "Richmond Spiders Football (NCAA)", "roles": ["Head Coach", "Quarterback", "Defensive Coordinator", "Booster Club President"]},
        {"client": "Virginia Cavaliers Baseball (NCAA)", "roles": ["Head Coach", "Starting Pitcher", "All-American Catcher", "Infielder"]}
    ],
    "FL": [
        {"client": "Miami Dolphins (NFL)", "roles": ["Mike McDaniel", "Tua Tagovailoa", "Tyreek Hill", "Head Athletic Trainer", "General Manager"]},
        {"client": "Inter Miami CF (MLS)", "roles": ["Head Coach", "Star Forward", "Midfielder", "Team Doctor", "Logistics Coordinator"]},
        {"client": "Orlando Magic (NBA)", "roles": ["Head Coach", "All-Star Forward", "Point Guard", "Video Coordinator", "Team Trainer"]}
    ],
    "NY": [
        {"client": "New York Yankees (MLB)", "roles": ["Aaron Judge", "Gerrit Cole", "Manager Aaron Boone", "Hitting Coach", "Bullpen Catcher", "Team Orthopedist"]},
        {"client": "Boston Red Sox (MLB)", "roles": ["Rafael Devers", "Manager Alex Cora", "First Base Coach", "Athletic Trainer"]}
    ],
    "SOUTH": [
        {"client": "LSU Tigers Football (NCAA)", "roles": ["Head Coach", "Starting Quarterback", "Wide Receiver", "Defensive Coordinator", "Equipment Manager"]},
        {"client": "New Orleans Saints (NFL)", "roles": ["Head Coach", "Quarterback", "Safety", "Team Trainer", "Media Liaison"]}
    ],
    "WEST": [
        {"client": "Seattle Mariners (MLB)", "roles": ["Manager", "Star Centerfielder", "Starting Ace", "Bullpen Coach", "Trainer"]},
        {"client": "Vegas Golden Knights (NHL)", "roles": ["Head Coach", "Team Captain", "Goaltender", "Equipment Manager", "Physical Therapist"]}
    ]
}

GLOBAL_GENERIC_PROFILES = {
    "AMER": [
        {"client": "FEMA Emergency Logistics Command", "roles": ["Logistics Commander", "Escort Officer", "Operations Chief", "Medical Coordinator"]},
        {"client": "Royal Caribbean Crew Rotation", "roles": ["Ship Captain", "Chief Engineer", "Hotel Director", "Cruise Director", "Deckhand"]},
        {"client": "Hamilton Broadway Touring Production", "roles": ["Company Director", "Lead Actor", "Stage Manager", "Costume Designer", "Audio Crew"]}
    ],
    "AFR": [
        {"client": "Singita Luxury Eco-Safari Expedition", "roles": ["Tour Director", "Expedition Leader", "VIP Lodge Guest", "Wildlife Photographer"]},
        {"client": "United Nations Humanitarian Mission (WFP)", "roles": ["Envoy Chief", "Field Coordinator", "Press Secretary", "Security Detail"]},
        {"client": "Anglo American Mining Corporate Summit", "roles": ["Chief Executive", "Geology Director", "Operations VP", "Legal Counsel"]}
    ],
    "EUR": [
        {"client": "World Economic Forum Delegation", "roles": ["Delegate Chief", "Economic Advisor", "NGO Director", "Chief of Staff"]},
        {"client": "Coldplay Music Tour Production", "roles": ["Chris Martin", "Tour Manager", "Audio Engineer", "Lighting Director", "VIP Guest"]}
    ]
}

# --- MATH CORE ---
def calculate_distance(orig, dest):
    if orig not in AIRPORTS or dest not in AIRPORTS:
        return random.randint(800, 2400)
    p1, p2 = AIRPORTS[orig], AIRPORTS[dest]
    lat1, lon1, lat2, lon2 = map(math.radians, [p1["lat"], p1["lon"], p2["lat"], p2["lon"]])
    a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2-lon1)/2)**2
    return round(2 * math.asin(math.sqrt(a)) * 3440.065)

def generate_charter_board():
    contracts = []
    current_loc = st.session_state.get("aircraft_location", "KMIA")
    
    current_airport_data = AIRPORTS.get(current_loc, {"region": "AMER", "subregion": "FL"})
    current_region = current_airport_data["region"]
    current_subregion = current_airport_data["subregion"]
    
    current_month = datetime.now().month
    
    for i in range(10):
        if i < 6:
            orig = current_loc
            orig_region = current_region
            orig_subregion = current_subregion
        else:
            orig = random.choice(list(AIRPORTS.keys()))
            orig_region = AIRPORTS[orig]["region"]
            orig_subregion = AIRPORTS[orig]["subregion"]
            
        # Select Profile with precise local awareness
        profile_pool = []
        if orig_subregion in SUBREGION_PROFILES:
            # Verify sport season compatibility
            if current_month in [6, 7, 8]:  # Summer: Only grab MLB / Soccer Tours
                profile_pool = [p for p in SUBREGION_PROFILES[orig_subregion] if "MLB" in p["client"] or "Soccer" in p["client"] or "Baseball" in p["client"]]
            elif current_month in [2, 3, 4, 5]:  # Spring: Basketball / NHL
                profile_pool = [p for p in SUBREGION_PROFILES[orig_subregion] if "Basketball" in p["client"] or "NHL" in p["client"] or "Lacrosse" in p["client"]]
            else:  # Fall/Winter: Football
                profile_pool = [p for p in SUBREGION_PROFILES[orig_subregion] if "Football" in p["client"] or "Volleyball" in p["client"]]
                
        if not profile_pool:
            profile_pool = GLOBAL_GENERIC_PROFILES.get(orig_region, GLOBAL_GENERIC_PROFILES["AMER"])
            
        profile = random.choice(profile_pool)
        
        # Sports stay domestic, corporate flights are global
        if "NCAA" in profile["client"] or "NFL" in profile["client"] or "MLB" in profile["client"] or "NHL" in profile["client"] or "NBA" in profile["client"]:
            available_dests = [a for a in AIRPORTS.keys() if a != orig and AIRPORTS[a]["region"] == orig_region]
        else:
            available_dests = [a for a in AIRPORTS.keys() if a != orig]
            
        if not available_dests:
            available_dests = ["KMIA"]
            
        dest = random.choice(available_dests)
        client_dist = calculate_distance(orig, dest)
        pax_count = random.randint(40, 189)
        
        client_time = round((client_dist / 440.0) + 0.3, 1)
        cargo_weight = round(min(pax_count * 32, 7500) / 1000.0, 1)
        
        contracts.append({
            "id": f"GX{random.randint(100,999)}",
            "client": profile["client"],
            "origin": orig,
            "destination": dest,
            "client_dist": client_dist,
            "client_time": client_time,
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
        role = random.choice(roles_pool) if (roles_pool and random.random() > 0.4) else "Staff / Passenger"
        manifest[seat] = {"name": f"{random.choice(first_names)} {random.choice(last_names)}", "role": role}
        
    return manifest

# --- SESSION INITIALIZATION ---
if "aircraft_location" not in st.session_state:
    st.session_state.aircraft_location = "KMIA"
if "active_contract" not in st.session_state:
    st.session_state.active_contract = None
if "selected_passenger" not in st.session_state:
    st.session_state.selected_passenger = None
if "board" not in st.session_state:
    st.session_state.board = generate_charter_board()

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.title("✈️ N657NK Control")

typed_loc = st.sidebar.text_input("Current Aircraft Location", value=st.session_state.aircraft_location).upper().strip()
if typed_loc != st.session_state.aircraft_location and len(typed_loc) >= 3:
    st.session_state.aircraft_location = typed_loc
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
    st.write(f"Positioned at: `{st.session_state.aircraft_location}` | Season Layout Active: **{datetime.now().strftime('%B %Y')}**")
    
    for job in st.session_state.board:
        with st.container(border=True):
            st.markdown(f"### {job['client']}")
            st.caption(f"**ID:** `{job['id']}` | Airframe: `N657NK` (A321ceo)")
            st.write(f"🛣️ **Route:** `{job['origin']}` ➔ `{job['destination']}` ({job['client_dist']} NM)")
            
            if st.session_state.aircraft_location == job['origin']:
                st.success(f"✅ On-site at {job['origin']} - No Ferry Flight Needed")
                job['payout'] = round(job['client_time'] * 7800)
            else:
                ferry_dist = calculate_distance(st.session_state.aircraft_location, job['origin'])
                ferry_time = round((ferry_dist / 440.0) + 0.3, 1)
                st.warning(f"✈️ Ferry Required: {st.session_state.aircraft_location} ➔ {job['origin']} (+{ferry_time}h)")
                job['payout'] = round((job['client_time'] * 7800) + (ferry_time * 4500))
                
            st.markdown(f"**Payout:** ${job['payout']:,}")
            if st.button("Accept & Inspect Flight", key=job['id'], use_container_width=True):
                st.session_state.active_contract = job
                st.session_state.manifest = generate_manifest(job['pax_count'], job['roles_pool'])
                st.session_state.selected_passenger = None
                st.rerun()
else:
    job = st.session_state.active_contract
    st.header(f"Active Dispatch: {job['id']}")
    st.subheader(job['client'])
    
    col_back, col_comp = st.columns(2)
    with col_back:
        if st.button("⬅️ Decline/Return to Board", use_container_width=True):
            st.session_state.active_contract = None
            st.rerun()
    with col_comp:
        if st.button("🏁 Log Flight Complete (Relocate Plane)", type="primary", use_container_width=True):
            st.session_state.aircraft_location = job['destination']
            st.session_state.active_contract = None
            st.session_state.board = generate_charter_board()
            st.rerun()

    f_total, e_total = 0, 0
    for seat_id in st.session_state.manifest.keys():
        if seat_id.endswith(("A", "B", "C", "D", "E", "F")):
            row_num = int(''.join(filter(str.isdigit, seat_id)))
            if row_num <= 4:
                f_total += 1
            else:
                e_total += 1

    with st.container(border=True):
        st.markdown("##### ⚙️ Configuration Profile & Cabin Load Summary")
        st.write(f"💺 **First Class:** {f_total} / 16 Occupied (`👑`) | **{16 - f_total} Open** (`💺`)")
        st.write(f"🔴 **Economy Cabin:** {e_total} / 173 Occupied (`🔴`) | **{173 - e_total} Open** (`💺`)")

    sb_params = {
        "airline": "GXA", "fltnum": job['id'], "type": "A321",
        "orig": job['origin'], "dest": job['destination'],
        "pax": str(job['pax_count']), "cargo": str(job['cargo_weight']),
        "acts": "2", "type_of_flight": "N"
    }
    sb_url = "https://dispatch.simbrief.com/options?" + urllib.parse.urlencode(sb_params)
    st.link_button("🚀 Generate SimBrief Flight Plan Package", sb_url, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 💺 Clickable Mobile Map Hud")
    st.caption("Tap any seat code directly to load that passenger's real-time file pop-up below:")

    # --- FULLY TAPPABLE MATRIX OVERLAY FOR IPHONE SCREEN PROPORTIONS ---
    st.markdown("**👑 FIRST CLASS SECTIONS**")
    for r in range(1, 5):
        cols = st.columns([1, 1, 1, 1, 1])
        with cols[0]: st.write(f"**Row {r}**")
        idx = 1
        for letter in ["A", "C", "D", "F"]:
            seat_id = f"{r}{letter}"
            is_occ = seat_id in st.session_state.manifest
            btn_label = f"👑 {seat_id}" if is_occ else f"💺 {seat_id}"
            with cols[idx]:
                if st.button(btn_label, key=f"btn_{seat_id}", use_container_width=True):
                    if is_occ:
                        st.session_state.selected_passenger = {"seat": seat_id, **st.session_state.manifest[seat_id]}
                    else:
                        st.session_state.selected_passenger = {"seat": seat_id, "name": "Open Seat", "role": "Unoccupied Assignment"}
                    st.rerun()
            idx += 1

    st.markdown("**🔴 ECONOMY SECTIONS**")
    for r in range(5, 34):
        cols = st.columns([1, 1, 1, 1, 1, 1, 1])
        with cols[0]: st.write(f"**R{r:02d}**")
        idx = 1
        for letter in ["A", "B", "C", "D", "E", "F"]:
            seat_id = f"{r}{letter}"
            is_occ = seat_id in st.session_state.manifest
            btn_label = f"🔴 {letter}" if is_occ else f"💺 {letter}"
            with cols[idx]:
                if st.button(btn_label, key=f"btn_{seat_id}", use_container_width=True):
                    if is_occ:
                        st.session_state.selected_passenger = {"seat": seat_id, **st.session_state.manifest[seat_id]}
                    else:
                        st.session_state.selected_passenger = {"seat": seat_id, "name": "Open Seat", "role": "Unoccupied Assignment"}
                    st.rerun()
            idx += 1
            
    # --- DYNAMIC POP-UP MANIFEST FILE CARD ---
    if st.session_state.selected_passenger:
        p_info = st.session_state.selected_passenger
        st.markdown("---")
        with st.container(border=True):
            st.markdown(f"### 📋 Secure Passenger Manifest Record: Seat {p_info['seat']}")
            st.write(f"👤 **Full Name:** `{p_info['name']}`")
            st.write(f"🎟️ **Assignment Profile:** {p_info['role']}")
            if st.button("Dismiss Profile Record", use_container_width=True):
                st.session_state.selected_passenger = None
                st.rerun()
