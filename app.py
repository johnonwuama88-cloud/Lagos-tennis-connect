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
            use_container_width=True,
        )
    except Exception:
      pass

# --- TAB 4: COACH DIRECTORY ---
with tab4:
  st.subheader("Verified Lagos Coaches & Fee Regulation")
  st.warning(
      "🛡️ **Community Pricing Policy:** Maximum allowed coaching rate is"
      f" **₦{MAX_HOURLY_RATE:,} per hour**."
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
              f" the limit of ₦{MAX_HOURLY_RATE:,}/hr."
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

          st.success(f"🎉 Coach {coach_name} registered successfully!")

  if os.path.exists(COACHES_CSV) and os.path.getsize(COACHES_CSV) > 0:
    try:
      c_df = pd.read_csv(COACHES_CSV)
      if not c_df.empty:
        st.subheader("📋 Regulated Coach Directory")
        st.dataframe(
            c_df[["Coach Name", "Location", "Hourly Rate (₦)", "Phone"]],
            use_container_width=True,
        )
    except Exception:
      pass

# --- TAB 5: MATCHMAKING, PREDICTIONS, WHATSAPP SHARE & LADDER ---
with tab5:
  st.subheader("⚔️ Matches, Score Predictions & Lagos Tennis Ladder")

  umpire_options = ["None / Self-Officiated"]
  crew_options = ["None"]
  if os.path.exists(STAFF_CSV) and os.path.getsize(STAFF_CSV) > 0:
    try:
      s_data = pd.read_csv(STAFF_CSV)
      umpires = s_data[s_data["Role"] == "Certified Umpire"][
          "Staff Name"
      ].tolist()
      crews = s_data[s_data["Role"] == "Ball Boy / Girl Crew"][
          "Staff Name"
      ].tolist()
      if umpires:
        umpire_options.extend(umpires)
      if crews:
        crew_options.extend(crews)
    except Exception:
      pass

  with st.expander("🔥 Post a Challenge & Predict Score", expanded=True):
    with st.form("match_challenge_form"):
      c1, c2 = st.columns(2)
      with c1:
        player_1 = st.text_input("Player 1 (Challenger):")
        player_2 = st.text_input("Player 2 (Opponent):")
        court_venue = st.selectbox(
            "Agreed Court Venue:",
            [
                "Ikoyi Club 1938",
                "Lagos Lawn Tennis Club",
                "Lekki Peninsula Tennis Courts",
                "National Stadium Surulere",
                "VGC Tennis Courts",
            ],
        )
        match_date = st.date_input("Match Date:")

      with c2:
        game_format = st.selectbox(
            "Select Match Format:",
            [
                "1 Set (First to 6 Games, Tie-Break at 6-6)",
                "Best of 3 Sets (Full Match)",
                "Fast4 Format (First to 4 Games)",
                "Game of 4 (Pro Set)",
                "10-Point Super Tie-Break Match",
            ],
        )
        assigned_umpire = st.selectbox("Assigned Umpire:", umpire_options)
        assigned_ballboy = st.selectbox("Assigned Ball Boy/Crew:", crew_options)
        predicted_score = st.text_input(
            "Predicted Score:", placeholder="6-0 (6 Luv)"
        )

      challenger_phone = st.text_input("Challenger WhatsApp / Phone Number:")
      challenge_submit = st.form_submit_button("Submit Challenge & Prediction")

      if challenge_submit:
        if player_1 == "" or player_2 == "":
          st.error("Please enter both player names.")
        else:
          m_exists = os.path.exists(MATCHES_CSV)
          m_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

          with open(MATCHES_CSV, mode="a", newline="", encoding="utf-8") as m_file:
            m_writer = csv.writer(m_file)
            if not m_exists:
              m_writer.writerow([
                  "Timestamp",
                  "Player 1",
                  "Player 2",
                  "Venue",
                  "Date",
                  "Match Format",
                  "Assigned Umpire",
                  "Assigned Ball Boy",
                  "Predicted Score",
                  "Phone",
              ])
            m_writer.writerow([
                m_timestamp,
                player_1,
                player_2,
                court_venue,
                str(match_date),
                game_format,
                assigned_umpire,
                assigned_ballboy,
                predicted_score,
                challenger_phone,
            ])

          st.success(
              f"🔥 Challenge Posted! {player_1} vs {player_2} at {court_venue}."
          )

  if os.path.exists(MATCHES_CSV) and os.path.getsize(MATCHES_CSV) > 0:
    try:
      m_df = pd.read_csv(MATCHES_CSV)
      if not m_df.empty:
        st.markdown("### 📊 Scheduled Fixtures & WhatsApp Share")
        for idx, row in m_df.iterrows():
          p1 = row.get("Player 1", "P1")
          p2 = row.get("Player 2", "P2")
          m_date = row.get("Date", "")
          m_venue = row.get("Venue", "")
          pred = row.get("Predicted Score", "")

          st.write(
              f"🎾 **{p1} vs {p2}** | 📅 {m_date} at {m_venue} | 🎯 Pred: `{pred}`"
          )

          share_text = (
              f"🎾 *Lagos Tennis Challenge!* {p1} vs {p2} on {m_date} at"
              f" {m_venue}. Predicted Score: {pred}. Join us on Lagos Tennis"
              " Connect!"
          )
          wa_url = f"https://api.whatsapp.com/send?text={quote(share_text)}"
          st.markdown(f"[📲 **Share Challenge to WhatsApp**]({wa_url})")
          st.markdown("---")
    except Exception:
      pass

  st.markdown("---")
  st.subheader("🏆 Submit Final Match Result & Live Ladder")

  with st.expander("📝 Record Final Score (Earn Points for Ladder)"):
    with st.form("result_form"):
      res_p1 = st.text_input("Winner Name:")
      res_p2 = st.text_input("Runner-Up Name:")
      final_score = st.text_input("Actual Final Score (e.g., 6-2, 6-4):")
      res_venue = st.selectbox(
          "Venue Played:",
          [
              "Ikoyi Club 1938",
              "Lagos Lawn Tennis Club",
              "Lekki Phase 1 Courts",
              "National Stadium",
              "VGC Courts",
          ],
      )

      res_submit = st.form_submit_button("Record Match Result")

      if res_submit:
        if res_p1 == "" or res_p2 == "":
          st.error("Please provide both player names.")
        else:
          r_exists = os.path.exists(RESULTS_CSV)
          r_time = datetime.now().strftime("%Y-%m-%d %H:%M")
          with open(
              RESULTS_CSV, mode="a", newline="", encoding="utf-8"
          ) as r_file:
            r_writer = csv.writer(r_file)
            if not r_exists:
              r_writer.writerow(
                  ["Timestamp", "Winner", "RunnerUp", "Score", "Venue"]
              )
            r_writer.writerow([r_time, res_p1, res_p2, final_score, res_venue])
          st.success(
              f"Result recorded! {res_p1} awarded 3 Ladder Points, {res_p2}"
              " awarded 1 Point!"
          )

  if os.path.exists(RESULTS_CSV) and os.path.getsize(RESULTS_CSV) > 0:
    try:
      r_df = pd.read_csv(RESULTS_CSV)
      if not r_df.empty:
        st.markdown("### 🥇 Official Lagos Tennis Ladder Rankings")

        scores_dict = {}
        for _, row in r_df.iterrows():
          winner = str(row["Winner"]).strip()
          runner = str(row["RunnerUp"]).strip()

          scores_dict[winner] = scores_dict.get(winner, 0) + 3
          scores_dict[runner] = scores_dict.get(runner, 0) + 1

        ladder_df = pd.DataFrame(
            list(scores_dict.items()), columns=["Player Name", "Total Points"]
        )
        ladder_df = ladder_df.sort_values(
            by="Total Points", ascending=False
        ).reset_index(drop=True)
        ladder_df.index += 1

        st.dataframe(ladder_df, use_container_width=True)
    except Exception:
      pass

# --- TAB 6: EQUIPMENT MARKETPLACE & STRINGING SERVICES ---
with tab6:
  st.subheader("🛒 Equipment, Gear & Stringing Marketplace")
  st.write(
      "Buy/sell tennis gear or locate certified racket stringers in Lagos!"
  )

  with st.expander("➕ List Item or Stringing Service"):
    with st.form("gear_form"):
      listing_type = st.selectbox(
          "Listing Type:",
          [
              "Racket Stringing Service",
              "Used / New Racket for Sale",
              "Tennis Balls & Accessories",
              "Apparel & Shoes",
          ],
      )
      seller_name = st.text_input("Name / Business Name:")
      item_title = st.text_input("Item / Service Title:")
      price_naira = st.number_input(
          "Price / Service Fee (₦):", min_value=500, value=15000, step=500
      )
      contact_phone = st.text_input("WhatsApp / Phone Number:")
      item_location = st.selectbox(
          "Location in Lagos:",
          [
              "Ikoyi / VI",
              "Lekki / Ajah",
              "Ikeja / Mainland",
              "Surulere",
          ],
      )

      gear_submit = st.form_submit_button("Post Listing")

      if gear_submit:
        g_exists = os.path.exists(GEAR_CSV)
        g_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(GEAR_CSV, mode="a", newline="", encoding="utf-8") as g_file:
          g_writer = csv.writer(g_file)
          if not g_exists:
            g_writer.writerow([
                "Timestamp",
                "Type",
                "Title",
                "Price",
                "Seller",
                "Location",
                "Phone",
            ])
          g_writer.writerow([
              g_time,
              listing_type,
              item_title,
              price_naira,
              seller_name,
              item_location,
              contact_phone,
          ])
        st.success("Listing posted to marketplace!")

  if os.path.exists(GEAR_CSV) and os.path.getsize(GEAR_CSV) > 0:
    try:
      g_df = pd.read_csv(GEAR_CSV)
      if not g_df.empty:
        st.markdown("### 📦 Available Gear & Services")
        st.dataframe(
            g_df[["Type", "Title", "Price", "Seller", "Location", "Phone"]],
            use_container_width=True,
        )
    except Exception as e:
      st.error(f"Error loading marketplace: {e}")

# --- TAB 7: LAGOS SOCIAL CUP TOURNAMENT HUB ---
with tab7:
  st.subheader("🏆 Lagos Tennis Connect Social Cup")
  st.info(
      "🎉 **Upcoming Event:** Registration is open for the inaugural **Lagos"
      " Tennis Connect Social Cup** hosted at Lagos Lawn Tennis Club, Onikan!"
  )

  with st.form("tournament_form"):
    t_name = st.text_input("Full Name:")
    t_phone = st.text_input("WhatsApp Number:")
    t_category = st.selectbox(
        "Tournament Category:",
        [
            "Men's Singles (Open)",
            "Women's Singles (Open)",
            "Doubles Championship",
            "Veterans / Seniors (45+)",
        ],
    )
    t_club = st.text_input("Home Club / Area:")

    t_submit = st.form_submit_button("Register for Tournament")

    if t_submit:
      if t_name == "" or t_phone == "":
        st.error("Please enter your name and phone number.")
      else:
        to_exists = os.path.exists(TOURNAMENT_CSV)
        to_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(
            TOURNAMENT_CSV, mode="a", newline="", encoding="utf-8"
        ) as to_file:
          to_writer = csv.writer(to_file)
          if not to_exists:
            to_writer.writerow(
                ["Timestamp", "Name", "Phone", "Category", "Club"]
            )
          to_writer.writerow([to_time, t_name, t_phone, t_category, t_club])
        st.success(
            f"🎉 Congratulations {t_name}! You are registered for the"
            f" {t_category}."
        )

  if os.path.exists(TOURNAMENT_CSV) and os.path.getsize(TOURNAMENT_CSV) > 0:
    try:
      to_df = pd.read_csv(TOURNAMENT_CSV)
      if not to_df.empty:
        st.markdown("### 📋 Confirmed Tournament Entries")
        st.dataframe(
            to_df[["Name", "Category", "Club"]], use_container_width=True
        )
    except Exception as e:
      st.error(f"Error loading tournament entries: {e}")

# --- TAB 8: PRIVACY POLICY & COMPLIANCE ---
with tab8:
  st.subheader("🔒 Privacy Policy & Terms of Service")
  st.write("Effective Date: October 2026 | **Lagos Tennis Connect**")

  st.markdown("""
    ### 1. Information We Collect
    Lagos Tennis Connect collects user-provided details strictly for local community tennis coordination in Lagos.

    ### 2. How We Use Your Data
    * To facilitate player matchmaking, court bookings, ladder rankings, coach directories, and tournament entries.

    ### 3. Security & Control
    All uploaded image files and CSV databases are handled securely. Users retain full rights to update or request removal of their personal details.
    """)