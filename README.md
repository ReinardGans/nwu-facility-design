# 🏥 Clinic Facility Layout Problem

This project is a simple interactive simulation of a clinic facility layout using Streamlit. Users can assign departments to locations on a 3x3 grid and simulate patient flow through the clinic.

## Features
- Assign Reception, Doctor 1, Doctor 2, and Pharmacy to unique locations on a 3x3 grid
- Visualize the clinic layout and department assignments
- Simulate patient arrivals, consultations, and pharmacy visits
- View results for patients seen, left without service, and total distance walked

## Assumptions
- 20 patients arrive randomly, average interval 0.4 hours (24 minutes)
- Clinic operates for a 12-hour shift
- Reception: 0.15 hours per patient
- Doctor: 0.25–0.5 hours per patient, two doctors available
- Pharmacy: 0.08 hours per patient
- Distances are calculated as Manhattan distance

## Getting Started
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run hospital-simulation.py
   ```

## License
MIT
