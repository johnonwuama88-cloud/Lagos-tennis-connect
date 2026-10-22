import csv
from datetime import datetime
import os
import pandas as pd
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
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🎾 Lagos Tennis Connect")
st.write(
    "Welcome to Lagos' premier tennis community, court booking, coaching,"
    " matchmaking, and support staff hub!"
)

# Database files
PLAYERS_CSV = "registered_players.csv"
BOOKINGS_CSV = "court_bookings.csv"
COACHES_CSV = "registered_coaches.csv"
MATCHES_CSV = "matchmaking_board.csv"
STAFF_CSV = "support_staff.csv"

# Fee Regulation Cap (Maximum allowed hourly rate in Naira)
MAX_HOURLY_RATE = 15000


# --- NAVIGATION TABS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Register Profile",
    "👥 Player Directory",
    "🎾 Book a Court",
    "👨‍🏫 Coach Directory",
    "🤝 Matchmaking Board",
    "⚖️ Umpires & Staff",
])

# --- TAB 1: REGISTRATION FORM ---
with tab1:
  st.subheader("Player Registration Form")

  with st.form("registration_form"):
    full_name = st.text_input("Enter your Full Name:")
    phone_number = st.text_input("Enter your Phone / WhatsApp Number:")

    lagos_area = st.selectbox(
        "Where are you based in Lagos?",
        [
            "Lekki / Ajah",
            "Victoria Island / Ikoyi",
            "Ikeja / Mainland",
            "Surulere",
        ],
    )

    skill_level = st.selectbox(
        "Your Tennis Skill Level:",
        ["Beginner", "Intermediate", "Advanced"],
    )

    submit_button = st.form_submit_button("Complete Registration")

    if submit_button:
      if full_name == "" or phone_number == "":
        st.error("Please provide your name and phone number.")
      else:
        file_exists = os.path.exists(PLAYERS_CSV)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        with open(PLAYERS_CSV, mode="a", newline="", encoding="utf-8") as file:
          writer = csv.writer(file)
          if not file_exists:
            writer.writerow(
                ["Timestamp", "Full Name", "Phone", "Lagos Area", "Skill"]
            )
          writer.writerow(
              [timestamp, full_name, phone_number, lagos_area, skill_level]
          )

        st.success(
            f"Welcome, {full_name}! You are successfully registered in the"
            " database."
        )

# --- TAB 2: PLAYER DIRECTORY ---
with tab2:
  st.subheader("Registered Tennis Community Directory")
  st.write("Browse fellow tennis players in Lagos and connect!")

  if os.path.exists(PLAYERS_CSV) and os.path.getsize(PLAYERS_CSV) > 0:
    try:
      df = pd.read_csv(PLAYERS_CSV)
      if df.empty:
        st.info("No players registered yet. Be the first to sign up in Tab 1!")
      else:
        st.metric(label="Total Active Players in Lagos", value=len(df))
        display_df = df[["Full Name", "Lagos Area", "Skill", "Phone"]]
        st.dataframe(display_df, use_container_width=True)
    except pd.errors.EmptyDataError:
      st.info("No players registered yet. Be the first to sign up in Tab 1!")
  else:
    st.info("Directory is currently empty. Register your profile in Tab 1 first!")

# --- TAB 3: COURT BOOKING SYSTEM ---
with tab3:
  st.subheader("Book a Tennis Court")
  st.write(
      "Select a premier court in Lagos, pick your date, and lock in your match"
      " slot."
  )

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
            f"Booking Confirmed! 🎉 {court_choice} is locked in for"
            f" {booker_name} on {booking_date} ({time_slot})."
        )

  st.markdown("---")
  st.subheader("📅 Recent Court Bookings")

  if os.path.exists(BOOKINGS_CSV) and os.path.getsize(BOOKINGS_CSV) > 0:
    try:
      b_df = pd.read_csv(BOOKINGS_CSV)
      if b_df.empty:
        st.info("No bookings made yet.")
      else:
        st.dataframe(
            b_df[["Player Name", "Court Venue", "Date", "Time Slot"]],
            use_container_width=True,
        )
    except pd.errors.EmptyDataError:
      st.info("No bookings made yet.")
  else:
    st.info("No bookings recorded yet.")

# --- TAB 4: COACH DIRECTORY & FEE REGULATION TRACKER ---
with tab4:
  st.subheader("Verified Lagos Coaches & Fee Regulation")
  st.warning(
      "🛡️ **Community Pricing Policy:** To protect players from exploitation,"
      f" Lagos Tennis Connect enforces a strict maximum coaching rate cap of"
      f" **₦{MAX_HOURLY_RATE:,} per hour**. Coaches charging above this limit"
      " will not be listed."
  )

  with st.expander("➕ Register as a Community Coach"):
    with st.form("coach_form"):
      coach_name = st.text_input("Coach Full Name:")
      coach_phone = st.text_input("Phone / WhatsApp Number:")
      coach_area = st.selectbox(
          "Primary Training Location / Club:",
          [
              "Ikoyi Club",
              "Lagos Lawn Tennis Club",
              "Lekki / Ajah Estates",
              "Ikeja GRA",
              "Surulere",
          ],
      )
      hourly_rate = st.number_input(
          "Proposed Hourly Rate (₦):",
          min_value=1000,
          max_value=50000,
          value=10000,
          step=500,
      )

      coach_submit = st.form_submit_button("Submit Coach Application")

      if coach_submit:
        if coach_name == "" or coach_phone == "":
          st.error("Please fill in all required fields.")
        elif hourly_rate > MAX_HOURLY_RATE:
          st.error(
              f"❌ Application Rejected: Your rate of ₦{hourly_rate:,} exceeds"
              f" the maximum community cap of ₦{MAX_HOURLY_RATE:,}/hr. Please"
              " lower your rate to comply."
          )
        else:
          c_exists = os.path.exists(COACHES_CSV)
          c_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

          with open(COACHES_CSV, mode="a", newline="", encoding="utf-8") as c_file:
            c_writer = csv.writer(c_file)
            if not c_exists:
              c_writer.writerow([
                  "Timestamp",
                  "Coach Name",
                  "Location",
                  "Hourly Rate (₦)",
                  "Phone",
              ])
            c_writer.writerow(
                [c_timestamp, coach_name, coach_area, hourly_rate, coach_phone]
            )

          st.success(
              f"🎉 Congratulations Coach {coach_name}! Your rates comply with"
              " our fee regulation policy and you are now listed in the"
              " directory."
          )

  st.markdown("---")
  st.subheader("📋 Regulated Coach Directory")
  st.write(
      "All coaches listed below are verified and strictly compliant with our"
      " fair pricing policy."
  )

  if os.path.exists(COACHES_CSV) and os.path.getsize(COACHES_CSV) > 0:
    try:
      c_df = pd.read_csv(COACHES_CSV)
      if c_df.empty:
        st.info("No coaches registered yet.")
      else:
        st.metric(label="Verified Regulated Coaches", value=len(c_df))
        st.dataframe(
            c_df[["Coach Name", "Location", "Hourly Rate (₦)", "Phone"]],
            use_container_width=True,
        )
    except pd.errors.EmptyDataError:
      st.info("No coaches registered yet.")
  else:
    st.info("No verified coaches recorded yet.")

# --- TAB 5: MATCHMAKING & HITTING PARTNER BOARD ---
with tab5:
  st.subheader("Matchmaking & Hitting Partner Board")
  st.write(
      "Looking for a match or hitting session this week? Post an open challenge"
      " or find a partner!"
  )

  with st.expander("➕ Post a Match Request / Challenge"):
    with st.form("match_form"):
      challenger_name = st.text_input("Your Full Name:")
      challenger_phone = st.text_input("Your WhatsApp / Phone Number:")

      match_type = st.selectbox(
          "Match Type:",
          [
              "Singles Competitive Match",
              "Doubles Partner Needed",
              "Casual Rally / Hitting Session",
          ],
      )

      preferred_location = st.selectbox(
          "Preferred Venue / Area:",
          [
              "Ikoyi Club",
              "Lagos Lawn Tennis Club",
              "Lekki Phase 1 Courts",
              "VGC Courts",
              "National Stadium Surulere",
          ],
      )

      match_date = st.date_input("Preferred Date:")

      extra_notes = st.text_input(
          "Additional Notes (e.g., 'Available around 7 AM for a fast rally'):"
      )

      match_submit = st.form_submit_button("Post Match Request")

      if match_submit:
        if challenger_name == "" or challenger_phone == "":
          st.error("Please enter your name and phone number.")
        else:
          m_exists = os.path.exists(MATCHES_CSV)
          m_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

          with open(MATCHES_CSV, mode="a", newline="", encoding="utf-8") as m_file:
            m_writer = csv.writer(m_file)
            if not m_exists:
              m_writer.writerow([
                  "Timestamp",
                  "Player Name",
                  "Match Type",
                  "Location",
                  "Date",
                  "Notes",
                  "Phone",
              ])
            m_writer.writerow([
                m_timestamp,
                challenger_name,
                match_type,
                preferred_location,
                str(match_date),
                extra_notes,
                challenger_phone,
            ])

          st.success(
              "Success! Your match request has been posted to the community"
              " board. 🎾"
          )

  st.markdown("---")
  st.subheader("🔥 Live Open Matches & Hitting Requests")
  st.write(
      "Browse open challenges below and reach out via phone/WhatsApp to accept"
      " a match!"
  )

  if os.path.exists(MATCHES_CSV) and os.path.getsize(MATCHES_CSV) > 0:
    try:
      m_df = pd.read_csv(MATCHES_CSV)
      if m_df.empty:
        st.info("No open match requests right now. Be the first to post one!")
      else:
        st.metric(label="Active Open Challenges", value=len(m_df))
        st.dataframe(
            m_df[
                [
                    "Player Name",
                    "Match Type",
                    "Location",
                    "Date",
                    "Notes",
                    "Phone",
                ]
            ],
            use_container_width=True,
        )
    except pd.errors.EmptyDataError:
      st.info("No open match requests right now. Be the first to post one!")
  else:
    st.info("No match requests recorded yet. Post yours above!")

# --- TAB 6: UMPIRES & SUPPORT STAFF REGISTRY ---
with tab6:
  st.subheader("Umpires & Ball Boys Registry")
  st.write(
      "Register as professional match support staff or find certified umpires"
      " and ball crews for your tournaments."
  )

  with st.expander("➕ Register as Support Staff"):
    with st.form("staff_form"):
      staff_name = st.text_input("Full Name:")
      staff_phone = st.text_input("WhatsApp / Phone Number:")

      staff_role = st.selectbox(
          "Support Role:",
          [
              "Certified Umpire",
              "Line Judge",
              "Ball Boy / Girl Crew",
          ],
      )

      staff_area = st.selectbox(
          "Preferred Venue / Area:",
          [
              "Ikoyi Club",
              "Lagos Lawn Tennis Club",
              "Lekki Phase 1 Courts",
              "VGC Courts",
              "National Stadium Surulere",
          ],
      )

      daily_rate = st.number_input(
          "Expected Daily Fee (₦):",
          min_value=1000,
          max_value=30000,
          value=5000,
          step=500,
      )

      staff_submit = st.form_submit_button("Submit Staff Registration")

      if staff_submit:
        if staff_name == "" or staff_phone == "":
          st.error("Please enter your name and phone number.")
        else:
          s_exists = os.path.exists(STAFF_CSV)
          s_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

          with open(STAFF_CSV, mode="a", newline="", encoding="utf-8") as s_file:
            s_writer = csv.writer(s_file)
            if not s_exists:
              s_writer.writerow([
                  "Timestamp",
                  "Staff Name",
                  "Role",
                  "Location",
                  "Daily Fee (₦)",
                  "Phone",
              ])
            s_writer.writerow([
                s_timestamp,
                staff_name,
                staff_role,
                staff_area,
                daily_rate,
                staff_phone,
            ])

          st.success(
              f"Success! You are now registered as a {staff_role} in Lagos"
              " Tennis Connect. 🎉"
          )

  st.markdown("---")
  st.subheader("📋 Available Support Staff Directory")
  st.write(
      "Browse verified umpires, line judges, and ball crews available for"
      " booking."
  )

  if os.path.exists(STAFS_CSV := STAFF_CSV) and os.path.getsize(STAFF_CSV) > 0:
    try:
      s_df = pd.read_csv(STAFF_CSV)
      if s_df.empty:
        st.info("No support staff registered yet.")
      else:
        st.metric(label="Registered Support Staff", value=len(s_df))
        st.dataframe(
            s_df[["Staff Name", "Role", "Location", "Daily Fee (₦)", "Phone"]],
            use_container_width=True,
        )
    except pd.errors.EmptyDataError:
      st.info("No support staff registered yet.")
  else:
    st.info("No support staff recorded yet. Register above!")