import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data (Replace with your CSV path)
@st.cache_data
def load_data():
    return pd.read_csv('All_Teams_updated.csv')

df = load_data()


# Create a Single Tab
tab1, = st.tabs(["📊 Player Stats"])

# Helper function to safely get values or return 0 if column doesn't exist
def get_value(filtered_data, column_name):
    return filtered_data[column_name].values[0] if column_name in filtered_data.columns else 0

# Tab for Player Stats
with tab1:
    # Streamlit App Title
    st.title("🏏 Player Stats Dashboard")
    st.header("View Player Stats")

    # Creating columns for side-by-side layout
    col1, col2, col3 = st.columns([1.5, 1.5, 1])

    with col1:
        # Select Team
        team_name = st.selectbox("🏏 Select Team:", df['Player_Team'].unique())

    with col2:
        # Filter Players by Team
        team_players = df[df['Player_Team'] == team_name]['Player'].unique()
        player_name = st.selectbox("👤 Select Player:", team_players)

    with col3:
        # Select Player Type (Batsman/Bowler)
        player_type = st.radio("🔎 Select Type:", ["Batsman", "Bowler"])

    # Filter Data for Selected Player
    filtered_data = df[(df['Player'] == player_name) & (df['Player_Team'] == team_name)]

    if filtered_data.empty:
        st.warning(f"No data found for {player_name} in {team_name}.")
    else:
        
        if player_type == "Batsman":
            # Extract Batting Data
            batsman_data = pd.DataFrame({
                'Format': ['IPL', 'Test', 'ODI', 'T20'],
                'Matches': [get_value(filtered_data, f'Matches_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'Innings': [get_value(filtered_data, f'batting_Innings_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'Balls': [get_value(filtered_data, f'batting_Balls_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'Runs': [get_value(filtered_data, f'batting_Runs_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'Average': [get_value(filtered_data, f'batting_Average_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'Strike Rate': [get_value(filtered_data, f'batting_SR_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                "Duck's" : [get_value(filtered_data, f'batting_Ducks_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                "NOT OUT" : [get_value(filtered_data, f'batting_Not Out_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                "4's" : [get_value(filtered_data, f'batting_Fours_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                "6's" : [get_value(filtered_data, f'batting_Sixes_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                '50s': [get_value(filtered_data, f'batting_50s_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                '100s': [get_value(filtered_data, f'batting_100s_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                '200s': [get_value(filtered_data, f'batting_200s_{fmt}') if fmt != 'T20' else 0 for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                '300s': [get_value(filtered_data, f'batting_300s_Test') if fmt == 'Test' else 0 for fmt in ['IPL', 'Test', 'ODI', 'T20']]
            })
            st.subheader(f"Batting Stats for {player_name} ({team_name})")
            st.dataframe(batsman_data)

            # Extract Data Matches vs innings
            formats = ['Test', 'ODI', 'T20', 'IPL']
            matches = [get_value(filtered_data, f'Matches_{fmt}') for fmt in formats]
            innings = [get_value(filtered_data, f'batting_Innings_{fmt}') for fmt in formats]
            
            # Create DataFrame
            comparison_data = pd.DataFrame({
                'Format': formats,
                'Matches': matches,
                'Innings': innings
            })
            
            # Melt Data
            comparison_data_melted = comparison_data.melt(id_vars='Format', var_name='Category', value_name='Count')
            
            # Plot Grouped Bar Chart
            fig_comparison = px.bar(
                comparison_data_melted,
                x='Format',
                y='Count',
                color='Category',
                barmode='group',
                title=f'{player_name} - Matches vs Innings Across Formats',
                labels={'Count': 'Number of Matches/Innings', 'Format': 'Match Format'}
            )
            
            st.plotly_chart(fig_comparison)

            ## Balls Vs Runs
            formats = ['IPL', 'Test', 'ODI', 'T20']
            runs = [get_value(filtered_data, f'batting_Runs_{fmt}') for fmt in formats]
            balls = [get_value(filtered_data, f'batting_Balls_{fmt}') for fmt in formats]
            
            # Create DataFrame
            line_data = pd.DataFrame({
                'Format': formats,
                'Runs': runs,
                'Balls Faced': balls
            })
            
            # Melt Data for Plotly
            line_data_melted = line_data.melt(id_vars='Format', var_name='Metric', value_name='Count')
            
            # Plot Line Chart
            fig_line = px.line(
                line_data_melted,
                x='Format',
                y='Count',
                color='Metric',
                markers=True,
                title=f'{player_name} - Runs vs Balls Faced Across Formats'
            )
            
            # Display Chart in Streamlit
            st.plotly_chart(fig_line)
            
            # Extract Player Data for Pie Chart runs across all formats
            player_data = df[df['Player'] == player_name].iloc[0]
            run_columns = ['batting_Runs_Test', 'batting_Runs_ODI', 'batting_Runs_T20', 'batting_Runs_IPL']
            runs_data = player_data[run_columns]
            plot_data = pd.DataFrame({'Format': ['Test', 'ODI', 'T20', 'IPL'], 'Runs': runs_data.values})

            # Plot Pie Chart
            fig = px.pie(plot_data, names='Format', values='Runs', title=f'{player_name} - Distribution of Batting Runs Across all Formats')
            st.plotly_chart(fig)

            highest_scores = [get_value(filtered_data, f'batting_Highest_{fmt}') for fmt in ['Test', 'ODI', 'T20', 'IPL']]

            highest_score_data = pd.DataFrame({
                'Format': ['Test', 'ODI', 'T20', 'IPL'],
                'Highest Score': highest_scores
            })
            fig_radial = px.line_polar(
                highest_score_data,
                r='Highest Score',
                theta='Format',
                line_close=True,
                title=f'{player_name} - Highest Scores Across Formats (Radial Chart)',
                markers=True,
                color_discrete_sequence=['#FF5733']  # You can change the color code
            )
            
            st.plotly_chart(fig_radial)

            # Bar Chart for 4s and 6s
            fours_sixes_data = pd.DataFrame({
                'Format': ['IPL', 'Test', 'ODI', 'T20'],
                "4's": [get_value(filtered_data, f'batting_Fours_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                "6's": [get_value(filtered_data, f'batting_Sixes_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']]
            })
            
            # Melting Data to Plot
            fours_sixes_data_melted = fours_sixes_data.melt(id_vars='Format', var_name='Shot Type', value_name='Count')
            
            # Plotting using Plotly
            fig_fours_sixes = px.bar(
                fours_sixes_data_melted,
                x='Format',
                y='Count',
                color='Shot Type',
                title=f'{player_name} - 4s and 6s Across Formats',
                barmode='group',
                labels={'Count': 'Number of Shots', 'Format': 'Match Format'}
            )
            
            st.plotly_chart(fig_fours_sixes)

            # Data Extraction 50,100,200,300,400
            formats = ['Test', 'ODI', 'T20', 'IPL']
            fifties = [get_value(filtered_data, f'batting_50s_{fmt}') for fmt in formats]
            hundreds = [get_value(filtered_data, f'batting_100s_{fmt}') for fmt in formats]
            double_hundreds = [get_value(filtered_data, f'batting_200s_{fmt}') for fmt in formats]
            triple_hundreds = [get_value(filtered_data, f'batting_300s_{fmt}') for fmt in formats]
            four_hundreds = [get_value(filtered_data, f'batting_400s_{fmt}') for fmt in formats]
            
            # Create DataFrame
            comparison_data = pd.DataFrame({
                'Format': formats,
                '50s': fifties,
                '100s': hundreds,
                '200s': double_hundreds,
                '300s': triple_hundreds,
                '400s' : four_hundreds
            })
            
            # Melt Data for Plotly
            comparison_data_melted = comparison_data.melt(id_vars='Format', var_name='Category', value_name='Count')
            
            # Plot Grouped Bar Chart
            fig_comparison = px.bar(
                comparison_data_melted,
                x='Format',
                y='Count',
                color='Category',
                barmode='group',
                title=f'{player_name} - Milestones Across Formats (Grouped Bar Chart)',
                labels={'Count': 'Number of Milestones', 'Format': 'Match Format'}
            )
            
            # Display Chart in Streamlit
            st.plotly_chart(fig_comparison)

            # Data Extraction ducks vs notouts
            formats = ['IPL', 'Test', 'ODI', 'T20']
            not_outs = [get_value(filtered_data, f'batting_Not Out_{fmt}') for fmt in formats]
            ducks = [get_value(filtered_data, f'batting_Ducks_{fmt}') for fmt in formats]
            
            # Create DataFrame
            comparison_data = pd.DataFrame({
                'Format': formats,
                'Not Outs': not_outs,
                'Ducks': ducks
            })
            
            # Melt Data for Plotly
            comparison_data_melted = comparison_data.melt(id_vars='Format', var_name='Category', value_name='Count')
            
            # Plot Grouped Bar Chart
            fig_comparison = px.bar(
                comparison_data_melted,
                x='Format',
                y='Count',
                color='Category',
                barmode='group',
                title=f'{player_name} - Not Outs vs Ducks Across Formats',
                labels={'Count': 'Number of Instances', 'Format': 'Match Format'}
            )
            
            # Display Chart in Streamlit
            st.plotly_chart(fig_comparison)
            

        else:
            # Extract Bowling Data
            bowler_data = pd.DataFrame({
                'Format': ['IPL', 'Test', 'ODI', 'T20'],
                'Matches': [get_value(filtered_data, f'Matches_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'Innings': [get_value(filtered_data, f'bowling_{fmt}_Innings') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'Balls': [get_value(filtered_data, f'bowling_{fmt}_Balls') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'Runs': [get_value(filtered_data, f'bowling_{fmt}_Runs') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'Maidens': [get_value(filtered_data, f'bowling_{fmt}_Maidens') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'Wickets': [get_value(filtered_data, f'bowling_{fmt}_Wickets') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'Average': [get_value(filtered_data, f'bowling_{fmt}_Avg') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'Economy': [get_value(filtered_data, f'bowling_{fmt}_Eco') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'Strike Rate': [get_value(filtered_data, f'bowling_{fmt}_SR') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'BBI': [get_value(filtered_data, f'bowling_{fmt}_BBI') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                'BBM': [get_value(filtered_data, f'bowling_{fmt}_BBM') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                '4W': [get_value(filtered_data, f'bowling_{fmt}_4w') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                '5W': [get_value(filtered_data, f'bowling_{fmt}_5w') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
                '10W': [get_value(filtered_data, f'bowling_{fmt}_10w') for fmt in ['IPL', 'Test', 'ODI', 'T20']],
            })
            st.subheader(f"Bowling Stats for {player_name} ({team_name})")
            st.dataframe(bowler_data)

            # Bar Chart for Matches Played
            matches_data = pd.DataFrame({
                'Format': ['IPL', 'Test', 'ODI', 'T20'],
                'Matches': [get_value(filtered_data, f'Matches_{fmt}') for fmt in ['IPL', 'Test', 'ODI', 'T20']]
            })
            fig_matches = px.bar(matches_data, x='Format', y='Matches', title=f'{player_name} - Matches Played Across Formats', color='Format')
            st.plotly_chart(fig_matches)
            
            # Extract the player data
            player_data = df[df['Player'] == player_name].iloc[0]
            wickets_columns = ['bowling_Test_Wickets','bowling_ODI_Wickets','bowling_T20_Wickets','bowling_IPL_Wickets']
            runs_data = player_data[wickets_columns]
            
            # Create a DataFrame for Plotly
            plot_data = pd.DataFrame({'Format': ['Test', 'ODI', 'T20', 'IPL'], 'Runs': runs_data.values})
            fig = px.pie(plot_data, names='Format', values='Runs', title=f'{player_name} - Distribution of Bowling Wickets Across all Formats')
            st.plotly_chart(fig)