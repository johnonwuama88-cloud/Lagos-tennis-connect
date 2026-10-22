import csv
from datetime import datetime
import os
from urllib.parse import quote
import pandas as pd
from PIL import Image
import streamlit as st

# --- CUSTOM CSS STYLING ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFF9F5;
    }
    .stButton>button {
        background-color: #FF5722;
        color: white;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        width: 100%;
    }
    h3 {
        color: #D32F2F;
    }
    .status-card {
        padding: 10px;
        border-radius: 8px;
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        margin-bottom: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🎾 Lagos Tennis Connect")
st.write(
    "Welcome to Lagos' ultimate tennis platform — court bookings, coaching,"
    " matchmaking, ladder rankings, equipment marketplace, and tournaments!"
)

# Database files
PLAYERS_CSV = "registered_players.csv"
BOOKINGS_CSV = "court_bookings.csv"
COACHES_CSV = "registered_coaches.csv"
MATCHES_CSV = "matchmaking_board.csv"
RESULTS_CSV = "match_results.csv"
STAFF_CSV = "support_staff.csv"
GEAR_CSV = "equipment_marketplace.csv"
TOURNAMENT_CSV = "tournament_entries.csv"
COURT_STATUS_CSV = "court_conditions.csv"
UPLOADS_DIR = "uploaded_photos"

# Ensure upload directory exists
if not os.path.exists(UPLOADS_DIR):
  os.makedirs(UPLOADS_DIR)

# Fee Regulation Cap (Maximum allowed hourly rate in Naira)
MAX_HOURLY_RATE = 15000

# --- NAVIGATION TABS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📝 Register Profile",
    "👥 Player Directory",
    "🎾 Book & Weather",
    "👨‍🏫 Coach Directory",
    "⚔️ Matches & Ladder",
    "🛒 Gear & Stringing",
    "🏆 Lagos Social Cup",
    "🔒 Privacy Policy",
])

# --- TAB 1: PLAYER REGISTRATION FORM ---
with tab1:
  st.subheader("Player Profile Registration")

  with st.form("registration_form"):
    col1, col2 = st.columns(2)

    with col1:
      full_name = st.text_input("Full Name:")
      phone_number = st.text_input("Phone / WhatsApp Number:")
      dob = st.date_input(
          "Date of Birth:",
          min_value=datetime(1940, 1, 1),
          max_value=datetime.now(),
      )
      state_of_origin = st.text_input(
          "State of Origin (e.g., Anambra, Lagos, Delta):"
      )

    with col2:
      lagos_area = st.selectbox(
          "Base Location in Lagos:",
          [
              "Lekki / Ajah",
              "Victoria Island / Ikoyi",
              "Ikeja / Mainland",
              "Surulere",
          ],
      )
      skill_level = st.selectbox(
          "Tennis Skill Level:", ["Beginner", "Intermediate", "Advanced"]
      )
      profession = st.text_input(
          "Profession / Occupation (e.g., Software Engineer, Banker):"
      )

    bio = st.text_area(
        "Short Bio / About Yourself:",
        placeholder=(
            "Tell the community about your tennis goals, playing style, or"
            " hobbies..."
        ),
    )
    profile_photo = st.file_uploader(
        "Upload Profile Picture (JPG/PNG):", type=["png", "jpg", "jpeg"]
    )

    submit_button = st.form_submit_button("Complete Registration")

    if submit_button:
      if full_name == "" or phone_number == "":
        st.error("Please provide your name and phone number.")
      else:
        photo_filename = "default.png"
        if profile_photo is not None:
          photo_filename = (
              f"{full_name.replace(' ', '_').lower()}_{profile_photo.name}"
          )
          photo_path = os.path.join(UPLOADS_DIR, photo_filename)
          with open(photo_path, "wb") as f:
            f.write(profile_photo.getbuffer())

        file_exists = os.path.exists(PLAYERS_CSV)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        with open(PLAYERS_CSV, mode="a", newline="", encoding="utf-8") as file:
          writer = csv.writer(file)
          if not file_exists:
            writer.writerow([
                "Timestamp",
                "Full Name",
                "Phone",
                "Lagos Area",
                "Skill",
                "DOB",
                "State of Origin",
                "Profession",
                "Bio",
                "Photo Filename",
            ])
          writer.writerow([
              timestamp,
              full_name,
              phone_number,
              lagos_area,
              skill_level,
              str(dob),
              state_of_origin,
              profession,
              bio,
              photo_filename,
          ])

        st.success(
            f"Welcome, {full_name}! Your complete profile is now registered."
        )

# --- TAB 2: PLAYER DIRECTORY ---
with tab2:
  st.subheader("Registered Player Community Directory")

  if os.path.exists(PLAYERS_CSV) and os.path.getsize(PLAYERS_CSV) > 0:
    try:
      df = pd.read_csv(PLAYERS_CSV)
      if df.empty:
        st.info("No players registered yet. Be the first to sign up in Tab 1!")
      else:
        st.metric(label="Total Registered Players in Lagos", value=len(df))

        st.markdown("### 🔍 View Player Detailed Profile")
        player_names = df["Full Name"].dropna().tolist()

        selected_player = st.selectbox(
            "Select a player to view full profile details:", player_names
        )

        if selected_player:
          player_data = df[df["Full Name"] == selected_player].iloc[0]

          with st.container():
            st.markdown("---")
            p_col1, p_col2 = st.columns([1, 2])

            with p_col1:
              photo_file = str(player_data.get("Photo Filename", "default.png"))
              photo_path = os.path.join(UPLOADS_DIR, photo_file)

              if os.path.exists(photo_path) and photo_file != "default.png":
                img = Image.open(photo_path)
                st.image(
                    img, caption=player_data["Full Name"], use_column_width=True
                )
              else:
                st.info("📷 No photo uploaded.")

            with p_col2:
              st.markdown(f"## {player_data['Full Name']}")
              st.markdown(
                  f"**🎾 Skill Level:** `{player_data.get('Skill', 'N/A')}`"
              )
              st.markdown(
                  f"**📍 Location:**"
                  f" `{player_data.get('Lagos Area', 'N/A')}`"
              )
              st.markdown(
                  f"**💼 Profession:**"
                  f" `{player_data.get('Profession', 'N/A')}`"
              )
              st.markdown(
                  f"**🏛️ State of Origin:**"
                  f" `{player_data.get('State of Origin', 'N/A')}`"
              )
              st.markdown(
                  f"**🎂 Date of Birth:** `{player_data.get('DOB', 'N/A')}`"
              )
              st.markdown(
                  f"**📞 Phone / WhatsApp:** `{player_data.get('Phone', 'N/A')}`"
              )

            st.markdown("### 📝 Player Bio")
            bio_text = player_data.get("Bio", "")
            if pd.isna(bio_text) or str(bio_text).strip() == "":
              st.write("*No bio provided yet.*")
            else:
              st.info(f'"{bio_text}"')

        st.markdown("---")
        st.markdown("### 📋 Full Community List")
        cols_to_show = [
            col
            for col in [
                "Full Name",
                "Lagos Area",
                "Skill",
                "Profession",
                "State of Origin",
                "Phone",
            ]
            if col in df.columns
        ]
        st.dataframe(df[cols_to_show], use_container_width=True)

    except Exception as e:
      st.error(f"Error reading directory: {e}")
  else:
    st.info("Directory is currently empty. Register your profile in Tab 1 first!")

# --- TAB 3: COURT BOOKING & WEATHER / COURT ALERTS ---
with tab3:
  st.subheader("🎾 Court Bookings & Live Court Alerts")

  st.markdown("### 🌦️ Real-Time Lagos Court Condition Alerts")
  st.write(
      "Check or report live court conditions across Lagos before heading out!"
  )

  with st.expander("📢 Report Court Weather / Condition Update"):
    with st.form("court_status_form"):
      status_venue = st.selectbox(
          "Venue:",
          [
              "Ikoyi Club 1938",
              "Lagos Lawn Tennis Club (Onikan)",
              "Lekki Peninsula Tennis Courts",
              "National Stadium Courts (Surulere)",
              "VGC Tennis Courts",
          ],
      )
      condition_status = st.selectbox(
          "Court Condition:",
          [
              "🟢 Playable - Dry & Sun Shining",
              "🟡 Caution - Slightly Damp / Drying Up",
              "🔴 Unplayable - Raining / Flooded Courts",
          ],
      )
      status_notes = st.text_input(
          "Quick Note (e.g., 'Court 3 wet, Courts 1 & 2 dry'):"
      )
      reporter_name = st.text_input("Your Name:")

      status_submit = st.form_submit_button("Post Live Condition Update")

      if status_submit:
        st_exists = os.path.exists(COURT_STATUS_CSV)
        st_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(
            COURT_STATUS_CSV, mode="a", newline="", encoding="utf-8"
        ) as st_file:
          st_writer = csv.writer(st_file)
          if not st_exists:
            st_writer.writerow(
                ["Timestamp", "Venue", "Status", "Notes", "Reporter"]
            )
          st_writer.writerow([
              st_time,
              status_venue,
              condition_status,
              status_notes,
              reporter_name,
          ])
        st.success("Condition report posted successfully!")

  if os.path.exists(COURT_STATUS_CSV) and os.path.getsize(COURT_STATUS_CSV) > 0:
    try:
      cs_df = pd.read_csv(COURT_STATUS_CSV)
      if not cs_df.empty:
        st.write("**Recent Community Updates:**")
        st.dataframe(
            cs_df.tail(3)[["Timestamp", "Venue", "Status", "Notes"]],
            use_container_width=True,
        )
    except Exception:
      pass

  st.markdown("---")
  st.subheader("📅 Book a Tennis Court Slot")

  with st.form("booking_form"):
    booker_name = st.text_input("Your Full Name (As registered):")
    court_choice = st.selectbox(
        "Choose Tennis Court Venue:",
        [
            "Ikoyi Club 1938 (Ikoyi)",
            "Lagos Lawn Tennis Club (Lagos Island)",
            "Lekki Peninsula Tennis Courts (Lekki Phase 1)",
            "National Stadium Courts (Surulere)",
            "VGC Tennis Courts (Ajah)",
        ],
    )
    booking_date = st.date_input("Select Match Date:")
    time_slot = st.selectbox(
        "Select Time Slot:",
        [
            "06:00 AM - 08:00 AM (Morning Session)",
            "08:00 AM - 10:00 AM (Morning Session)",
            "04:00 PM - 06:00 PM (Evening Session)",
            "06:00 PM - 08:00 PM (Floodlight Session)",
        ],
    )

    booking_submit = st.form_submit_button("Confirm Court Booking")

    if booking_submit:
      if booker_name == "":
        st.error("Please enter your name to confirm the booking.")
      else:
        b_exists = os.path.exists(BOOKINGS_CSV)
        b_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        with open(BOOKINGS_CSV, mode="a", newline="", encoding="utf-8") as b_file:
          b_writer = csv.writer(b_file)
          if not b_exists:
            b_writer.writerow(
                ["Timestamp", "Player Name", "Court Venue", "Date", "Time Slot"]
            )
          b_writer.writerow(
              [
                  b_timestamp,
                  booker_name,
                  court_choice,
                  str(booking_date),
                  time_slot,
              ]
          )

        st.success(
            f"Booking Confirmed! 🎉 {court_choice} locked for {booker_name} on"
            f" {booking_date} ({time_slot})."
        )

  if os.path.exists(BOOKINGS_CSV) and os.path.getsize(BOOKINGS_CSV) > 0:
    try:
      b_df = pd.read_csv(BOOKINGS_CSV)
      if not b_df.empty:
        st.markdown("### 📋 Scheduled Court Bookings")
        st.dataframe(
            b_df[["Player Name", "Court Venue", "Date", "Time Slot"]],