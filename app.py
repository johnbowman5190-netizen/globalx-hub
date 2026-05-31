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

# --- APPLICATION DATA BASE ---
AIRPORTS = {
    "KMIA": {"name": "Miami International", "lat": 25.793, "lon": -80.290, "region": "AMER"},
    "KJFK": {"name": "John F. Kennedy Intl", "lat": 40.641, "lon": -73.778, "region": "AMER"},
    "TNCM": {"name": "Princess Juliana Intl", "lat": 18.041, "lon": -63.109, "region": "AMER"},
    "KMCO": {"name": "Orlando International", "lat": 28.429, "lon": -81.309, "region": "AMER"},
    "SPJC": {"name": "Lima Jorge Chávez Intl", "lat": -12.022, "lon": -77.114, "region": "AMER"}, 
    "KSEA": {"name": "Seattle-Tacoma Intl", "lat": 47.449, "lon": -122.309, "region": "AMER"},   
    "PANC": {"name": "Anchorage Stevens Intl", "lat": 61.174, "lon": -150.016, "region": "AMER"},
    "KABQ": {"name": "Albuquerque Sunport", "lat": 35.040, "lon": -106.609, "region": "AMER"},
    "KRDU": {"name": "Raleigh-Durham Intl", "lat": 35.877, "lon": -78.787, "region": "AMER"},
    "EGLL": {"name": "London Heathrow", "lat": 51.470, "lon": -0.454, "region": "EUR"},
    "MDPC": {"name": "Punta Cana Intl", "lat": 18.567, "lon": -68.363, "region": "AMER"},
    "FDSK": {"name": "King Mswati III Intl", "lat": -26.357, "lon": 31.717, "region": "AFR"},
    "FAOR": {"name": "OR Tambo Intl (Joburg)", "lat": -26.139, "lon": 28.246, "region": "AFR"},
    "FACT": {"name": "Cape Town International", "lat": -33.964, "lon": 18.602, "region": "AFR"}
}

# --- ALL-SPORTS SEASONAL CONFIGURATOR ---
def get_seasonal_sports_profile():
    current_month = datetime.now().month
    
    # SUMMER PIPELINE (June, July, August)
    if current_month in [6, 7, 8]:
        return [
            {"client": "Professional Baseball Club", "roles": ["Manager", "Starting Pitcher", "All-Star Outfielder", "Hitting Coach", "Bullpen Catcher", "Team Orthopedist", "Head Athletic Trainer"]},
            {"client": "Professional Fastpitch Softball Team", "roles": ["Head Coach", "Ace Pitcher", "Infield Captain", "Dugout Coordinator", "Athletic Trainer"]},
            {"client": "Elite Soccer Squad (Summer Pre-Season Tour)", "roles": ["Technical Director", "Winger", "Center Back", "Goalkeeper", "Physiotherapist", "Kit Manager", "Executive Chef"]},
            {"client": "Track & Field National Championship Delegation", "roles": ["Head Coach", "Sprint Specialist", "High Jumper", "Relay Coordinator", "Massage Therapist", "Team Doctor"]},
            {"client": "Collegiate Swimming & Diving Championship Team", "roles": ["Head Coach", "Freestyle Swimmer", "Platform Diver", "Assistant Coach", "Nutritionist"]}
        ]
    # SPRING PIPELINE (February, March, April, May)
    elif current_month in [2, 3, 4, 5]:
        return [
            {"client": "NCAA Division 1 Basketball Team", "roles": ["Head Coach", "Point Guard", "Starting Center", "Assistant Coach", "Director of Basketball Ops", "Athletic Trainer", "Radio Play-by-Play"]},
            {"client": "Professional Basketball Club", "roles": ["Head Coach", "All-Star Guard", "Power Forward", "Assistant Coach", "Video Coordinator", "Team Physio"]},
            {"client": "Professional Hockey Club (NHL)", "roles": ["Head Coach", "Team Captain", "Goaltender", "Equipment Manager", "General Manager", "Physical Therapist", "Scouting Director"]},
            {"client": "Collegiate Men's Lacrosse Team", "roles": ["Head Coach", "Lead Attacker", "Goalie", "Midfielder", "Defensive Coordinator", "Athletic Trainer"]},
            {"client": "Professional Soccer Club (Regular Season)", "roles": ["Manager", "Striker", "Midfield Captain", "Goalkeeper coach", "Physiotherapist"]}
        ]
    # FALL/WINTER PIPELINE (September, October, November, December, January)
    else:
        return [
            {"client": "NCAA Gridiron Football Team", "roles": ["Head Coach", "Quarterback", "Defensive Coordinator", "Linebacker", "Athletic Trainer", "Equipment Manager", "Booster Member"]},
            {"client": "Professional Football Team", "roles": ["Head Coach", "Starting Quarterback", "Offensive Coordinator", "Special Teams Coordinator", "Head Athletic Trainer", "General Manager", "Media Liaison"]},
            {"client": "Collegiate Women's Volleyball Team", "roles": ["Head Coach", "Outside Hitter", "Setter", "Libero", "Assistant Coach", "Team Trainer"]},
            {"client": "Professional Soccer Club (Playoff Run)", "roles": ["Manager", "Designated Player", "Center Back", "Team Doctor", "PR Director"]}
        ]

NON_SPORTS_PROFILES = {
    "AMER": [
        {"client": "U.S. Government Logistics Charter", "roles": ["Logistics Commander", "Escort Officer", "Operations Chief", "Medical Coordinator", "Transport Liaison"]},
        {"client": "Cruise Line Crew Rotation Contract", "roles": ["Ship Captain", "Chief Engineer", "Hotel Director", "Cruise Director", "Deckhand", "Executive Chef"]},
        {"client": "Broadway Touring Production", "roles": ["Director", "Lead Actor", "Stage Manager", "Costume Designer", "Choreographer", "Audio Crew"]}
    ],
    "AFR": [
        {"client": "Luxury Eco-Safari Expedition", "roles": ["Tour Director", "Expedition Leader", "VIP Client", "Wildlife Photographer", "Travel Coordinator"]},
        {"client": "United Nations Humanitarian Mission", "roles": ["Envoy Chief", "Human Rights Officer", "Field Coordinator", "Press Secretary", "Security Detail"]},
        {"client": "Global Mining Executive Summit", "roles": ["Chief Executive", "Geology Director", "Operations VP", "Legal Counsel", "Board Member"]}
    ],
    "EUR": [
        {"client": "World Economic Forum Delegation", "roles": ["Delegate Chief", "Economic Advisor", "NGO Director", "Chief of Staff", "Security Analyst"]},
        {"client": "VIP Arena Music Tour Production", "roles": ["Lead Vocalist", "Guitarist", "Tour Manager", "Audio Engineer", "VIP Guest", "Backstage Coordinator"]}
    ]
}

# --- MATH CORE ---
def calculate_distance(orig, dest):
    if orig not in AIRPORTS or dest not in AIRPORTS:
        return random.randint(3500, 6800) if (orig == "FDSK" or dest == "FDSK") else random.randint(800, 2400)
    p1, p2 = AIRPORTS[orig], AIRPORTS[dest]
    lat1, lon1, lat2, lon2 = map(math.radians, [p1["lat"], p1["lon"], p2["lat"], p2["lon"]])
    a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2-lon1)/2)**2
    return round(2 * math.asin(math.sqrt(a)) * 3440.065)

def generate_charter_board():
    contracts = []
    current_loc = st.session_state.get("aircraft_location", "KMIA")
    current_region = AIRPORTS.get(current_loc, {"region": "AMER"})["region"]
    
    sports_pool = get_seasonal_sports_profile()
    
    for i in range(10):
        if i < 6:
            orig = current_loc
            orig_region = current_region
        else:
            orig = random.choice(list(AIRPORTS.keys()))
            orig_region = AIRPORTS[orig]["region"]
            
        # 50/50 balance split between high-priority Sports Charters and Regional Enterprise/Govt flights
        if random.random() < 0.5:
            profile = random.choice(sports_pool)
        else:
            profile_pool = NON_SPORTS_PROFILES.get(orig_region, NON_SPORTS_PROFILES["AMER"])
            profile = random.choice(profile_pool)
        
        available_dests = [a for a in AIRPORTS.keys() if a != orig]
        dest = random.choice(available_dests) if available_dests else "KMIA"
        
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
    st.write(f"Positioned at: `{st.session_state.aircraft_location}` | Current Sim Date: **{datetime.now().strftime('%B %Y')}**")
    
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
        st.write(f"📦 **Payload Totals:** {job['pax_count']} Passengers Checked In | {job['cargo_weight']}k lbs Cargo Load")

    sb_params = {
        "airline": "GXA", "fltnum": job['id'], "type": "A321",
        "orig": job['origin'], "dest": job['destination'],
        "pax": str(job['pax_count']), "cargo": str(job['cargo_weight']),
        "acts": "2", "type_of_flight": "N"
    }
    sb_url = "https://dispatch.simbrief.com/options?" + urllib.parse.urlencode(sb_params)
    st.link_button("🚀 Generate SimBrief Flight Plan Package", sb_url, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 💺 Mobile Cabin Map")
    st.caption("Legend: 👑 First Class | 🔴 Occupied Economy | 💺 Empty / Open Seat")
    
    seat_options = ["-- OR Inspect via Manifest Dropdown list --"]
    for seat_id, p_data in sorted(st.session_state.manifest.items()):
        seat_options.append(f"Seat {seat_id}: {p_data['name']} ({p_data['role']})")

    if st.session_state.selected_passenger:
        p_info = st.session_state.selected_passenger
        st.info(f"📋 **Passenger Record Card**\n\n**Seat:** `{p_info['seat']}`\n\n**Name:** `{p_info['name']}`\n\n**Assignment:** {p_info['role']}")
        if st.button("Dismiss Passenger Details", use_container_width=True):
            st.session_state.selected_passenger = None
            st.rerun()

    fc_text = "=== FIRST CLASS RECLINERS ===\n"
    for r in range(1, 5):
        row_str = f"Row {r}  "
        for letter in ["A", "C"]:
            row_str += "👑" if f"{r}{letter}" in st.session_state.manifest else "💺"
        row_str += "  [Aisle]  "
        for letter in ["D", "F"]:
            row_str += "👑" if f"{r}{letter}" in st.session_state.manifest else "💺"
        fc_text += row_str + "\n"
        
    y_text = "=== ECONOMY CABIN MAP ===\n"
    for r in range(5, 34):
        row_str = f"Row {r:02d}  "
        for letter in ["A", "B", "C"]:
            row_str += "🔴" if f"{r}{letter}" in st.session_state.manifest else "💺"
        row_str += "  [||]  "
        for letter in ["D", "E", "F"]:
            row_str += "🔴" if f"{r}{letter}" in st.session_state.manifest else "💺"
        y_text += row_str + "\n"
        
    st.code(fc_text, language="text")
    st.code(y_text, language="text")
        
    st.markdown("---")
    st.markdown("#### 📋 Mobile Passenger Selector")
    selected_seat_inspect = st.selectbox("Tap here to load a specific passenger file profile:", options=seat_options)
    if "-- OR Inspect" not in selected_seat_inspect:
        parsed_seat = selected_seat_inspect.split(":")[0].replace("Seat ", "").strip()
        if parsed_seat in st.session_state.manifest:
            st.session_state.selected_passenger = {"seat": parsed_seat, **st.session_state.manifest[parsed_seat]}
            st.rerun()
