import streamlit as st
import matplotlib.pyplot as plt
import random

# Set page layout
st.set_page_config(layout="wide")

# --- Assumptions ---
assumptions = """
- 🛎️ Reception, 🩺 Doctor 1, 🩺 Doctor 2, 💊 Pharmacy.
- Each department must be assigned to a unique location.
- 20 patients arrive randomly, with an average interval of 0.4 hours (24 minutes).
- Clinic operates for a 12-hour shift (clinic closes after 12.0 hours).
- Reception takes 0.15 hours (9 minutes) per patient.
- Doctor consultation takes 0.25–0.5 hours (15–30 minutes), two doctors available.
- Pharmacy takes 0.08 hours (5 minutes) per patient.
- Distances are calculated as Manhattan distance.
"""
st.markdown(
    "<h1 style='text-align: center;'>🏥 Clinic Facility Layout Problem</h1>",
    unsafe_allow_html=True
)
st.expander("Show Details", expanded=False).markdown(assumptions)
st.markdown("<br>", unsafe_allow_html=True)

# Define grid size
grid_size = 3
locations = {(i * grid_size + j + 1): (i, j) for i in range(grid_size) for j in range(grid_size)}

departments = ["🛎️ Reception", "🩺 Doctor 1", "🩺 Doctor 2", "💊 Pharmacy"]

# Layout + Assignments
col1, col2 = st.columns([1, 1])

with col1:
    fig, ax = plt.subplots(figsize=(6, 6))
    for loc, (x, y) in locations.items():
        ax.scatter(y, x, s=500, color="lightgrey")
        ax.text(y, x, f"L_{loc}", ha='center', va='center', fontsize=8)
    
    # Draw Entry and Exit Points
    entry_point = (0, 0)
    exit_point = (grid_size - 1, grid_size - 1)
    ax.scatter(entry_point[1], entry_point[0], s=700, color="green")
    ax.text(entry_point[1], entry_point[0], "Entry", ha='center', va='center', fontsize=9, weight='bold', color='white')
    ax.scatter(exit_point[1], exit_point[0], s=700, color="red")
    ax.text(exit_point[1], exit_point[0], "Exit", ha='center', va='center', fontsize=9, weight='bold', color='white')
    
    ax.set_xticks(range(grid_size))
    ax.set_yticks(range(grid_size))
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlim(-0.5, grid_size - 0.5)
    ax.set_ylim(-0.5, grid_size - 0.5)
    ax.set_title("Clinic Layout (3x3 Grid)")
    st.pyplot(fig)

with col2:
    st.subheader("Assign Departments to Locations")
    
    # Predefined suboptimal default for 3x3 grid
    default_layout = {
        "🛎️ Reception": 9,
        "🩺 Doctor 1": 1,
        "🩺 Doctor 2": 3,
        "💊 Pharmacy": 7
    }

    dept_assignments = {}
    for dept in departments:
        loc = st.selectbox(
            f"{dept} Location",
            options=list(locations.keys()),
            index=list(locations.keys()).index(default_layout[dept]),
            key=dept
        )
        dept_assignments[dept] = loc

    if len(set(dept_assignments.values())) < 4:
        st.warning("⚠️ Departments must be assigned to unique locations.")
    else:
        st.success("✅ Departments assigned. Ready to simulate.")
        
        # Simulation Button
        if st.button("Run Simulation"):
            # Simulation Parameters
            num_patients = 20   
            clinic_close_time = 12.0  # 12 hours
            patient_arrival_rate = 0.4  # average 0.4 hours (24 minutes)

            def calc_distance(loc1, loc2):
                # Accept both location numbers and coordinates (for Entry/Exit)
                if isinstance(loc1, int):
                    x1, y1 = locations[loc1]
                else:
                    x1, y1 = loc1
                
                if isinstance(loc2, int):
                    x2, y2 = locations[loc2]
                else:
                    x2, y2 = loc2
                
                return abs(x1 - x2) + abs(y1 - y2)

            patients_seen = 0
            patients_left = 0
            total_distance = 0
            current_time = 0.0
            doctor_busy_time = [0.0, 0.0]

            for _ in range(1, num_patients + 1):
                arrival_time = current_time + random.uniform(0.2, 0.6)  # random between 12 and 36 minutes
                if arrival_time > clinic_close_time:
                    patients_left += 1
                    continue

                current_time = arrival_time
                # Entry to Reception
                total_distance += calc_distance(entry_point, dept_assignments["🛎️ Reception"])
                current_time += 0.15  # Reception: 9 minutes
                # Reception to Doctor
                total_distance += calc_distance(dept_assignments["🛎️ Reception"], dept_assignments["🩺 Doctor 1"])
                min_wait = min(doctor_busy_time)
                doctor_idx = doctor_busy_time.index(min_wait)
                current_time += min_wait
                doctor_busy_time = [max(0.0, t - min_wait) for t in doctor_busy_time]
                consult_time = random.uniform(0.25, 0.5)  # 15–30 minutes
                doctor_busy_time[doctor_idx] = consult_time
                current_time += consult_time
                # Doctor to Pharmacy
                total_distance += calc_distance(dept_assignments[f"🩺 Doctor {doctor_idx+1}"], dept_assignments["💊 Pharmacy"])
                current_time += 0.08  # Pharmacy: 5 minutes
                # Pharmacy to Exit
                total_distance += calc_distance(dept_assignments["💊 Pharmacy"], exit_point)
                
                if current_time <= clinic_close_time:
                    patients_seen += 1
                else:
                    patients_left += 1

            st.subheader("📊 Simulation Results")
            st.write(f"👨‍⚕️ **Patients Seen:** {patients_seen}")
            st.write(f"🚶‍♂️ **Patients Left Without Service:** {patients_left}")
            st.write(f"🦶 **Total Distance Walked (Simplified):** {total_distance}")