import pandas as pd
import country_converter as coco
import plotly.express as px
import streamlit as st
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
import warnings

# --- 1. PAGE CONFIGURATION ---
# Set the page configuration. This must be the first Streamlit command.
st.set_page_config(
    page_title="Global Population Dashboard",
    page_icon="🌎",
    layout="wide",  # Use the full page width
    initial_sidebar_state="expanded",
)

# --- 2. DATA LOADING ---
# Cache the data loading to improve performance.
@st.cache_data
def load_data(file_path):
    """
    Loads the cleaned CSV file.
    The file is expected to be in the same directory as the app script.
    """
    try:
        df = pd.read_csv(file_path)
        # Ensure 'Continent' column exists, if not, this will raise an error handled below
        if 'Continent' not in df.columns:
            st.error("Dataset is missing the required 'Continent' column.")
            return None
        # Ensure numeric columns are numeric
        numeric_cols = ['Population(in millions)', 'Population density', 'Total Dependency Ratio', 'Sex ratio (males per 100 females)']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna(subset=numeric_cols)
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found.")
        st.info("Please make sure the file is in the same directory as your Streamlit app.py script.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return None

# --- Set Plotly's default template to Streamlit's theme ---
px.defaults.template = "streamlit"

# --- 3. MAIN APPLICATION ---
st.title("🌎 Global Population Dashboard")
st.markdown("An interactive dashboard to analyze global population demographics.")

# Load the data
DATA_FILE = "cleanednewglobal1.csv"
df = load_data(DATA_FILE)

# If data loading fails, stop the app
if df is None:
    st.stop()
    
# --- 4. CREATE TABS FOR ORGANIZATION ---
tab1, tab2, tab3, tab4 = st.tabs(
    ["Global Overview 🗺️", "Demographic Deep-Dive 📈", "Country-Specific Analysis 🔍", "Country Comparison 🆚"]
)

# --- TAB 1: GLOBAL OVERVIEW ---
with tab1:
    st.header("Global Demographic Overview")

    # Top-level metrics
    st.markdown("### Key Global Metrics")
    total_pop = df['Population(in millions)'].sum()
    avg_density = df['Population density'].mean()
    avg_sex_ratio = df['Sex ratio (males per 100 females)'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Population", f"{total_pop:,.0f} Million")
    col2.metric("Avg. Population Density", f"{avg_density:,.2f} / km²")
    col3.metric("Avg. Sex Ratio", f"{avg_sex_ratio:,.1f} m / 100 f")

    st.markdown("---")  # Visual separator

    # Interactive Choropleth Map
    st.subheader("Interactive Global Map")
    map_metric = st.selectbox(
        'Select a metric to display on the map:',
        ('Population(in millions)', 'Population density', 'Total Dependency Ratio', 'Sex ratio (males per 100 females)'),
        key='map_metric_select'
    )

    fig_map = px.choropleth(
        df,
        locations="iso_alpha3",       # Use the ISO alpha-3 code
        color=map_metric,             # The column to color-code
        hover_name="Country",         # What to show on hover
        color_continuous_scale=px.colors.sequential.Plasma, # Color scale
        title=f'Global Map of {map_metric}'
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0)) # Fit map better
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")

    # Top/Bottom 10 Lists in expanders
    st.subheader("Data Rankings")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.expander("Top 10 Most Populous Countries"):
            st.dataframe(df.nlargest(10, 'Population(in millions)')[['Country', 'Population(in millions)']])

    with col2:
        with st.expander("Top 10 Most Densely Populated"):
            st.dataframe(df.nlargest(10, 'Population density')[['Country', 'Population density']])

    with col3:
        with st.expander("Top 10 'Youngest' Countries (by Youth Dependency)"):
            st.dataframe(df.nlargest(10, 'Youth Dependency Ratio')[['Country', 'Youth Dependency Ratio']])

# --- TAB 2: DEMOGRAPHIC DEEP-DIVE ---
with tab2:
    st.header("📈 Demographic Deep-Dive")
    st.markdown("Analyze relationships between different demographic variables.")

    # Age Structure Analysis
    st.subheader("Age Structure: Young vs. Old Population")
    st.markdown("This scatter plot shows the relationship between the youth and elderly populations. Countries are colored by continent.")
    fig_age = px.scatter(
        df,
        x='Population Aged 0 to 14 (%)',
        y='Population Aged 60 and Over (%)',
        color='Continent',
        hover_name='Country',
        title='Age Structure: Young vs. Old Population (%)'
    )
    st.plotly_chart(fig_age, use_container_width=True)

    st.markdown("---")

    # Gender Analysis
    st.subheader("Global Distribution of Sex Ratios")
    st.markdown("This histogram shows the frequency of different sex ratios (males per 100 females). The red dashed line marks a 1:1 ratio (100).")
    fig_sex_ratio = px.histogram(
        df,
        x='Sex ratio (males per 100 females)',
        title='Distribution of Sex Ratios Worldwide',
        nbins=50
    )
    fig_sex_ratio.add_vline(x=100, line_dash="dash", line_color="red") # Add a line at 100
    st.plotly_chart(fig_sex_ratio, use_container_width=True)

    st.markdown("---")

    # Density vs. Population
    st.subheader("Population vs. Density (Logarithmic Scale)")
    st.markdown("Are the most populous countries also the most dense? This log-scale plot helps visualize the relationship for all countries.")
    fig_density = px.scatter(
        df,
        x='Population(in millions)',
        y='Population density',
        log_x=True,  # Use log scale for clarity
        log_y=True,  # Use log scale for clarity
        color='Continent',
        hover_name='Country',
        title='Population (Millions) vs. Population Density (Log Scale)',
        labels={'Population(in millions)': 'Population (in millions, log)', 'Population density': 'Population Density (log)'}
    )
    st.plotly_chart(fig_density, use_container_width=True)

# --- TAB 3: COUNTRY-SPECIFIC ANALYSIS ---
with tab3:
    st.header("🔍 Country-Specific Analysis")
    st.markdown("Drill down into the demographic profile of a single country.")

    # User Input: Filters for continent and country
    col1, col2 = st.columns(2)
    with col1:
        # Sort continents list alphabetically, handle 'Other'
        continents = sorted(df['Continent'].unique())
        if 'Other' in continents:
            continents.remove('Other')
            continents.append('Other')
        
        selected_continent = st.selectbox('Filter by Continent:', ['All'] + continents)
    
    with col2:
        if selected_continent == 'All':
            country_list = sorted(df['Country'].unique())
        else:
            country_list = sorted(df[df['Continent'] == selected_continent]['Country'].unique())
        
        selected_country = st.selectbox('Select a Country:', country_list)

    st.markdown("---")

    # Get the data for that country
    country_data = df[df['Country'] == selected_country].iloc[0]

    # Display metrics
    st.subheader(f"Demographic Profile for {selected_country}")
    
    # Use two separate st.columns calls with different variable names
    met_col1, met_col2, met_col3 = st.columns(3)
    met_col1.metric("Total Population", f"{country_data['Population(in millions)']:,.1f} M")
    met_col2.metric("Population Density", f"{country_data['Population density']:,.1f} / km²")
    met_col3.metric("Sex Ratio (m/100f)", f"{country_data['Sex ratio (males per 100 females)']:,.1f}")

    met_col4, met_col5, met_col6 = st.columns(3)
    met_col4.metric("Working-Age (15-59)", f"{country_data['Working-Age (15-59) %']:,.1f}%")
    met_col5.metric("Youth Dependency", f"{country_data['Youth Dependency Ratio']:,.1f}%")
    met_col6.metric("Old-Age Dependency", f"{country_data['Old-Age Dependency Ratio']:,.1f}%")

    st.markdown("---")

    # Age Breakdown Donut Chart
    st.subheader(f"Population Age Structure for {selected_country}")
    age_data = pd.DataFrame({
        'Category': ['Aged 0-14', 'Aged 15-59 (Working Age)', 'Aged 60+'],
        'Percentage': [
            country_data['Population Aged 0 to 14 (%)'],
            country_data['Working-Age (15-59) %'],
            country_data['Population Aged 60 and Over (%)']
        ]
    })
    fig_donut = px.pie(
        age_data, 
        names='Category', 
        values='Percentage', 
        title='Population Age Structure', 
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_donut, use_container_width=True)


# --- TAB 4: COUNTRY COMPARISON ---
with tab4:
    st.header("🆚 Country Comparison")
    st.markdown("Select two or more countries to compare their key metrics side-by-side.")

    # User Input: Multiselect for countries
    countries_to_compare = st.multiselect(
        'Select countries to compare:',
        options=sorted(df['Country'].unique()),
        default=['United States of America', 'China', 'India', 'Kenya']  # Use the user's original default
    )

    if countries_to_compare:
        comp_df = df[df['Country'].isin(countries_to_compare)]

        # We need to "melt" the dataframe for Plotly to make a good grouped bar chart
        comp_df_melted = comp_df.melt(
            id_vars='Country',
            value_vars=['Population(in millions)', 'Population density', 'Total Dependency Ratio', 'Sex ratio (males per 100 females)'],
            var_name='Metric',
            value_name='Value'
        )

        st.subheader("Metric Comparison Chart")
        # Create the faceted bar chart
        fig_comp = px.bar(
            comp_df_melted,
            x='Country',  # Put Country on X-axis for better grouping
            y='Value',
            color='Country',
            barmode='group',
            title='Country Comparison by Metric',
            facet_col='Metric',  # Create a separate plot for each Metric
            facet_col_wrap=2,    # Wrap facets into 2 columns
            height=700           # Taller plot for better readability
        )
        
        fig_comp.update_yaxes(matches=None) # Allow y-axes to be independent (e.g., population in M vs. ratio in %)
        fig_comp.update_xaxes(showticklabels=True) # Ensure x-axis labels are shown
        fig_comp.update_layout(yaxis_title=None) # Remove "Value" as y-axis title
        
        st.plotly_chart(fig_comp, use_container_width=True)

        # Also show the raw data table
        st.subheader("Raw Data Comparison")
        st.dataframe(comp_df.set_index('Country'))
    else:
        st.info("Please select at least one country to start the comparison.")