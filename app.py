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
    "PANC": {"name": "Anchorage Stevens Intl", "lat": 61.174, "lon": -150.016}  
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
    current_loc = st.session_state.aircraft_location
    
    for i in range(4):
        profile = random.choice(CHARTER_PROFILES)
        orig = random.choice(list(AIRPORTS.keys()))
        dest = random.choice([a for a in AIRPORTS.keys() if a != orig])
        
        client_dist = calculate_distance(orig, dest)
        ferry_dist = calculate_distance(current_loc, orig)
        
        if client_dist > 3100:  # Range Cap
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
st.sidebar.metric(label="Current Aircraft Location", value=st.session_state.aircraft_location)
sb_user = st.sidebar.text_input("SimBrief Username", value="VirtualPilot")

if st.sidebar.button("🔄 Refresh Contract Board"):
    st.session_state.board = generate_charter_board()
    st.session_state.active_contract = None
    st.rerun()

# --- MAIN APP ROUTING ---
if st.session_state.active_contract is None:
    st.header("Available Charter Contracts Desk")
    st.write("Select a contract below. Yellow paths require a ferry leg from N657NK's current location.")
    
    for job in st.session_state.board:
        with st.container(border=True):
            col1, col2, col3 = st.columns([2.5, 2, 1.5])
            with col1:
                st.markdown(f"### {job['client']}")
                st.caption(f"**ID:** `{job['id']}` | Airframe: `N657NK` (A321ceos)")
            with col2:
                st.write(f"🛣️ **Route:** `{job['origin']}` ➔ `{job['destination']}` ({job['client_dist']} NM)")
                if job['ferry_time'] > 0:
                    st.warning(f"✈️ Ferry Required: {st.session_state.aircraft_location} ➔ {job['origin']} (+{job['ferry_time']}h)")
                else:
                    st.success(f"✅ On-site at {job['origin']}")
            with col3:
                st.markdown(f"### ${job['payout']:,}")
                if st.button("Accept & Inspect Flight", key=job['id'], use_container_width=True):
                    st.session_state.active_contract = job
                    st.session_state.manifest = generate_manifest(job['pax_count'], job['roles_pool'])
                    st.rerun()
else:
    job = st.session_state.active_contract
    st.header(f"Active Dispatch: {job['id']} - {job['client']}")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Decline/Return to Board", use_container_width=True):
            st.session_state.active_contract = None
            st.rerun()
    with c2:
        if st.button("🏁 Log Flight Complete (Relocate Plane)", type="primary", use_container_width=True):
            st.session_state.aircraft_location = job['destination']
            st.session_state.active_contract = None
            st.session_state.board = generate_charter_board()
            st.rerun()

    with st.container(border=True):
        st.markdown("##### ⚙️ Airframe Configuration Manifest File")
        b1, b2, b3 = st.columns(3)
        b1.caption("💺 CABIN CONFIG: **Fenix Two-Class (16F / 173Y)**")
        b2.caption("⛽ AUX FUEL TANKS: **2 ACTs Installed**")
        b3.caption(f"📦 PAYLOAD TOTALS: **{job['pax_count']} Pax | {job['cargo_weight']}k lbs Cargo**")

    sb_params = {
        "airline": "GXA", "fltnum": job['id'], "type": "A321",
        "orig": job['origin'], "dest": job['destination'],
        "pax": str(job['pax_count']), "cargo": str(job['cargo_weight']),
        "acts": "2", "type_of_flight": "N"
    }
    sb_url = "https://dispatch.simbrief.com/options?" + urllib.parse.urlencode(sb_params)
    st.link_button("🚀 Generate SimBrief Flight Plan Package", sb_url, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 💺 Interactive Cabin Map")
    
    st.caption("💠 First Class Recliners")
    for r in range(1, 5):
        cols = st.columns([1, 1, 0.5, 1, 0.5, 1, 1])
        cols[3].markdown(f"<p style='text-align:center;font-size:11px;color:#b3a27f;'><b>{r}</b></p>", unsafe_allow_html=True)
        fc_map = {"A": 0, "C": 1, "D": 5, "F": 6}
        for letter, col_idx in fc_map.items():
            sid = f"{r}{letter}"
            if sid in st.session_state.manifest:
                p = st.session_state.manifest[sid]
                cols[col_idx].button(f"👑{letter}", key=f"s_{sid}", help=f"{p['name']}\n{p['role']}")
            else:
                cols[col_idx].button(f"{letter}", key=f"s_{sid}", disabled=True)

    st.markdown("<div style='border-top:1px dashed red; margin:10px 0;'></div>", unsafe_allow_html=True)
    
    st.caption("✈️ Economy Cabin")
    for r in range(5, 34):
        cols = st.columns([1, 1, 1, 0.7, 1, 1, 1])
        cols[3].markdown(f"<p style='text-align:center;font-size:11px;color:gray;'><b>{r}</b></p>", unsafe_allow_html=True)
        e_letters = ["A", "B", "C", "D", "E", "F"]
        col_idxs = [0, 1, 2, 4, 5, 6]
        for letter, col_idx in zip(e_letters, col_idxs):
            sid = f"{r}{letter}"
            if sid in st.session_state.manifest:
                p = st.session_state.manifest[sid]
                cols[col_idx].button(f"🔴{letter}", key=f"s_{sid}", help=f"{p['name']}\n{p['role']}")
            else:
                cols[col_idx].button(f"{letter}", key=f"s_{sid}", disabled=True)