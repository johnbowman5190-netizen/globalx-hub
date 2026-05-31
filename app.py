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
    "EGLL": {"name": "London Heathrow", "lat": 51.470, "lon": -0.454},
    "MDPC": {"name": "Punta Cana Intl", "lat": 18.567, "lon": -68.363},
    "KABQ": {"name": "Albuquerque Sunport", "lat": 35.040, "lon": -106.609}
}

CHARTER_PROFILES = [
    {"client": "NCAA Football Team", "roles": ["Head Coach", "Quarterback", "Defensive Coordinator", "Linebacker", "Athletic Trainer", "Equipment Manager", "Booster Member"]},
    {"client": "U.S. Government Logistics", "roles": ["Logistics Commander", "Escort Officer", "Operations Chief", "Medical Coordinator", "Transport Liaison"]},
    {"client": "Inter Miami CF Support Group", "roles": ["Club President", "Ultra Supporter", "VIP Sponsor", "Media Content Creator", "Security Head"]},
    {"client": "Cruise Line Crew Rotation", "roles": ["Ship Captain", "Chief Engineer", "Hotel Director", "Cruise Director", "Deckhand", "Executive Chef"]},
    {"client": "VIP Music Tour Charter", "roles": ["Lead Vocalist", "Guitarist", "Tour Manager", "Audio Engineer", "VIP Guest", "Backstage Coordinator"]},
    {"client": "International Corporate Summit", "roles": ["Chief Executive", "VP of Operations", "Regional Director", "Keynote Speaker"]},
    {"client": "Formula 1 Pit Crew", "roles": ["Team Principal", "Lead Driver", "Race Engineer", "Pit Mechanic", "Tire Specialist"]}
]

# --- MATH CORE ---
def calculate_distance(orig, dest):
    if orig not in AIRPORTS or dest not in AIRPORTS:
        return random.randint(800, 2400) # Intelligent fallback distance if custom ICAO is missing coordinates
    p1, p2 = AIRPORTS[orig], AIRPORTS[dest]
    lat1, lon1, lat2, lon2 = map(math.radians, [p1["lat"], p1["lon"], p2["lat"], p2["lon"]])
    a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2-lon1)/2)**2
    return round(2 * math.asin(math.sqrt(a)) * 3440.065)

def generate_charter_board():
    contracts = []
    current_loc = st.session_state.get("aircraft_location", "KMIA")
    
    # Generate 10 total dynamic contracts
    for i in range(10):
        profile = random.choice(CHARTER_PROFILES)
        
        # Smart pairing: Force 60% of contracts to depart directly from wherever the user typed
        if i < 6:
            orig = current_loc
        else:
            orig = random.choice(list(AIRPORTS.keys()))
            
        # Select target destination
        available_dests = [a for a in AIRPORTS.keys() if a != orig]
        dest = random.choice(available_dests) if available_dests else "KMIA"
        
        client_dist = calculate_distance(orig, dest)
        ferry_dist = calculate_distance(current_loc, orig)
        
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
    st.write(f"Showing up to {len(st.session_state.board)} active missions linked to base tracking locator: `{st.session_state.aircraft_location}`")
    
    for job in st.session_state.board:
        with st.container(border=True):
            st.markdown(f"### {job['client']}")
            st.caption(f"**ID:** `{job['id']}` | Airframe: `N657NK` (A321ceo)")
            st.write(f"🛣️ **Route:** `{job['origin']}` ➔ `{job['destination']}` ({job['client_dist']} NM)")
            
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

    with st.container(border=True):
        st.markdown("##### ⚙️ Configuration Profile")
        st.write(f"💺 **Cabin Layout:** Fenix Two-Class (16F / 173Y)")
        st.write(f"📦 **Payload:** {job['pax_count']} Passengers | {job['cargo_weight']}k lbs Cargo Load")

    sb_params = {
        "airline": "GXA", "fltnum": job['id'], "type": "A321",
        "orig": job['origin'], "dest": job['destination'],
        "pax": str(job['pax_count']), "cargo": str(job['cargo_weight']),
        "acts": "2", "type_of_flight": "N"
    }
    sb_url = "https://dispatch.simbrief.com/options?" + urllib.parse.urlencode(sb_params)
    st.link_button("🚀 Generate SimBrief Flight Plan Package", sb_url, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 💺 Interactive Cabin HUD")
    st.caption("Tap any assigned colored seat below to pop open the passenger manifest details card instantly!")
    
    # --- ACTIVE POP-UP MODAL CARD ---
    if st.session_state.selected_passenger:
        p_info = st.session_state.selected_passenger
        with st.status(f"📋 Manifest Verified: Seat {p_info['seat']}", expanded=True, state="success"):
            st.write(f"👤 **Passenger Name:** `{p_info['name']}`")
            st.write(f"🎟️ **Manifest Assignment/Role:** {p_info['role']}")
            st.write("✅ *Security Clearance Logged - Ready for Boarding Flight deck integration.*")
            if st.button("Dismiss Card", use_container_width=True):
                st.session_state.selected_passenger = None
                st.rerun()

    # --- FIRST CLASS GENERATOR ---
    st.write("**First Class Cabin (Rows 1-4)**")
    for r in range(1, 5):
        c1, c2, c_aisle, c3, c4 = st.columns([1, 1, 0.6, 1, 1])
        
        # Seat A
        sid_A = f"{r}A"
        if sid_A in st.session_state.manifest:
            if c1.button(f"👑 {sid_A}", key=f"btn_{sid_A}", use_container_width=True):
                st.session_state.selected_passenger = {"seat": sid_A, **st.session_state.manifest[sid_A]}
                st.rerun()
        else:
            c1.button(f"💺 {sid_A}", key=f"btn_{sid_A}", disabled=True, use_container_width=True)
            
        # Seat C
        sid_C = f"{r}C"
        if sid_C in st.session_state.manifest:
            if c2.button(f"👑 {sid_C}", key=f"btn_{sid_C}", use_container_width=True):
                st.session_state.selected_passenger = {"seat": sid_C, **st.session_state.manifest[sid_C]}
                st.rerun()
        else:
            c2.button(f"💺 {sid_C}", key=f"btn_{sid_C}", disabled=True, use_container_width=True)

        # Aisle
        c_aisle.markdown(f"<p style='text-align:center;color:gray;font-size:12px;margin-top:6px;'>R{r}</p>", unsafe_allow_html=True)

        # Seat D
        sid_D = f"{r}D"
        if sid_D in st.session_state.manifest:
            if c3.button(f"👑 {sid_D}", key=f"btn_{sid_D}", use_container_width=True):
                st.session_state.selected_passenger = {"seat": sid_D, **st.session_state.manifest[sid_D]}
                st.rerun()
        else:
            c3.button(f"💺 {sid_D}", key=f"btn_{sid_D}", disabled=True, use_container_width=True)
            
        # Seat F
        sid_F = f"{r}F"
        if sid_F in st.session_state.manifest:
            if c4.button(f"👑 {sid_F}", key=f"btn_{sid_F}", use_container_width=True):
                st.session_state.selected_passenger = {"seat": sid_F, **st.session_state.manifest[sid_F]}
                st.rerun()
        else:
            c4.button(f"💺 {sid_F}", key=f"btn_{sid_F}", disabled=True, use_container_width=True)

    # --- ECONOMY CLASS GENERATOR ---
    st.markdown("<br>**Economy Cabin (Rows 5-33)**", unsafe_allow_html=True)
    for r in range(5, 34):
        c1, c2, c3, c_aisle, c4, c5, c6 = st.columns([1, 1, 1, 0.6, 1, 1, 1])
        
        letters_left = ["A", "B", "C"]
        cols_left = [c1, c2, c3]
        for l, col in zip(letters_left, cols_left):
            sid = f"{r}{l}"
            if sid in st.session_state.manifest:
                if col.button(f"🔴 {l}", key=f"btn_{sid}", use_container_width=True):
                    st.session_state.selected_passenger = {"seat": sid, **st.session_state.manifest[sid]}
                    st.rerun()
            else:
                col.button(f"💺 {l}", key=f"btn_{sid}", disabled=True, use_container_width=True)
                
        c_aisle.markdown(f"<p style='text-align:center;color:gray;font-size:11px;margin-top:6px;'>{r:02d}</p>", unsafe_allow_html=True)
        
        letters_right = ["D", "E", "F"]
        cols_right = [c4, c5, c6]
        for l, col in zip(letters_right, cols_right):
            sid = f"{r}{l}"
            if sid in st.session_state.manifest:
                if col.button(f"🔴 {l}", key=f"btn_{sid}", use_container_width=True):
                    st.session_state.selected_passenger = {"seat": sid, **st.session_state.manifest[sid]}
                    st.rerun()
            else:
                col.button(f"💺 {l}", key=f"btn_{sid}", disabled=True, use_container_width=True)
