import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("ipl_cleaned.csv")

st.set_page_config(page_title="IPL Team Dashboard", layout="centered")

# Title
st.title("\U0001F3CF IPL Team Performance Dashboard")
st.markdown("Explore detailed analysis of each IPL team's journey, match wins, toss outcomes, and trophies.")

# Team selection
teams = sorted(pd.unique(df['team1'].dropna().tolist() + df['team2'].dropna().tolist()))
team_short_names = {
    "Royal Challengers Bengaluru": "RCB",
    "Chennai Super Kings": "CSK",
    "Mumbai Indians": "MI",
    "Kolkata Knight Riders": "KKR",
    "Delhi Capitals": "DC",
    "Rajasthan Royals": "RR",
    "Sunrisers Hyderabad": "SRH",
    "Lucknow Super Giants": "LSG",
    "Gujarat Titans": "GT",
    "Punjab Kings": "PBKS",
    "Deccan Chargers": "DC",
    "Pune Warriors": "PW",
    "Rising Pune Supergiant": "RPS",
    "Kochi Tuskers Kerala": "KTK"
}

selected_team = st.selectbox("Select your IPL team", teams)

if selected_team:
    short_name = team_short_names.get(selected_team, "")
    st.header(f"📊 Insights for {selected_team} ({short_name})")
    team_matches = df[(df['team1'] == selected_team) | (df['team2'] == selected_team)]

    # 1. Top 5 Player of the Match for selected team
    st.subheader("\U0001F3C5 Top 5 Player of the Match Awards")
    top_players = team_matches['player_of_match'].value_counts().head(5)
    fig1, ax1 = plt.subplots()
    ax1.bar(top_players.index, top_players.values, color='salmon')
    ax1.set_ylabel("Awards")
    ax1.set_title("Top 5 Player of the Match Winners")
    st.pyplot(fig1)

    # 2. Matches Won per Season
    st.subheader("\U0001F4C6 Matches Won per Season")
    team_wins = df[df['winner'] == selected_team]
    wins_per_season = team_wins['season'].value_counts().sort_index()
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(wins_per_season.index.astype(str), wins_per_season.values, marker='o', color='green')
    ax2.set_xlabel("Season")
    ax2.set_ylabel("Wins")
    ax2.set_title(f"{selected_team} - Matches Won per Season")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # 3. Winning Style: Runs vs Wickets
    st.subheader("\U0001F4CA Winning Style")
    style_counts = team_wins['result'].value_counts()
    fig3, ax3 = plt.subplots()
    style_counts.plot(kind='bar', color=['skyblue', 'pink'], ax=ax3)
    ax3.set_ylabel("Number of Matches")
    ax3.set_title("Wins by Runs vs Wickets")
    plt.xticks(rotation=0)
    st.pyplot(fig3)

    # 4. First vs Second Innings Wins
    st.subheader("⚔️ 1st vs 2nd Innings Wins")
    first_bat_win = team_wins[(team_wins['toss_winner'] == selected_team) & (team_wins['toss_decision'] == 'bat')].shape[0]
    second_bat_win = team_wins.shape[0] - first_bat_win
    fig4, ax4 = plt.subplots()
    ax4.bar(["1st Innings", "2nd Innings"], [first_bat_win, second_bat_win], color=['blue', 'orange'])
    ax4.set_ylabel("Wins")
    ax4.set_title("Batting Innings Wins")
    st.pyplot(fig4)

    # 5. Toss Wins vs Match Wins After Toss Win
    st.subheader("\U0001FA99 Toss Wins vs Match Wins After Toss Win")
    toss_wins_df = df[df['toss_winner'] == selected_team]
    total_tosses_won = toss_wins_df.shape[0]
    matches_won_after_toss = toss_wins_df[toss_wins_df['winner'] == selected_team].shape[0]
    toss_win_pct = round((matches_won_after_toss / total_tosses_won) * 100, 2) if total_tosses_won > 0 else 0.0
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("\U0001F3AF Tosses Won", total_tosses_won)
    with col2:
        st.metric("✅ Matches Won After Toss", matches_won_after_toss)
    with col3:
        st.metric("\U0001F4CA Win % After Toss", f"{toss_win_pct}%")
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    ax5.bar(["Tosses Won", "Matches Won After Toss"], [total_tosses_won, matches_won_after_toss], color=['skyblue', 'lightgreen'])
    ax5.set_ylabel("Count")
    ax5.set_title(f"{selected_team} - Toss Wins vs Match Wins After Toss")
    st.pyplot(fig5)

    # 6. IPL Trophies (Champions)
    st.subheader("\U0001F3C6 IPL Trophy Count")

    # Filter for finals
    final_matches = df[df['match_type'].str.lower() == 'final']

    # Count trophies
    trophies = final_matches[final_matches['winner'] == selected_team].shape[0]

    # Manually add 1 trophy for RCB (2025)
    if selected_team == "Royal Challengers Bengaluru":
        trophies += 1
        st.success(f"**{selected_team} has won {trophies} IPL trophy{'ies' if trophies != 1 else ''}.**\n\n\U0001F3C6 2025")
    else:
        trophy_emojis = "\U0001F3C6" * trophies if trophies > 0 else "No trophies yet \U0001F97A"
        st.success(f"**{selected_team} has won {trophies} IPL trophy{'ies' if trophies != 1 else ''}.**\n\n{trophy_emojis}")


    # 7. Most Successful Chasers
    st.subheader("\U0001F3C1 Most Successful Chase Teams (Top 5)")
    chasing_wins = df[df['result'] == 'wickets']
    top_chasers = chasing_wins['winner'].value_counts().head(5)
    fig6, ax6 = plt.subplots()
    ax6.bar(top_chasers.index, top_chasers.values, color='lightgreen')
    ax6.set_title("Top 5 Most Successful Chasing Teams")
    ax6.set_ylabel("Wins while Chasing")
    plt.xticks(rotation=90)
    st.pyplot(fig6)

    # 8. Top 5 Player of Match (Overall Seasons )
    st.subheader("\U0001F947 Overall Top 5 Player of the Match Winners")
    top_pom = df['player_of_match'].value_counts().head(5)
    fig7, ax7 = plt.subplots()
    ax7.bar(top_pom.index, top_pom.values, color='skyblue')
    ax7.set_ylabel("Awards")
    ax7.set_title("Top 5 Overall Player of the Match Winners")
    st.pyplot(fig7)
