**\# Global Population Analysis Dashboard**

This project is an interactive web dashboard for analyzing global population data. Built with Streamlit, Pandas, and Plotly, it transforms a raw CSV dataset into a multi-page tool for exploring demographic trends.

The primary goal is to demonstrate end-to-end data project skills: from data cleaning and feature engineering in a Jupyter Notebook to building and deploying a user-friendly, interactive dashboard.

\## 📸 Project Showcase
<img width="1843" height="747" alt="Country Comparison" src="https://github.com/user-attachments/assets/08e6847b-55b7-4b3b-96c3-b4193102e604" />
<img width="1796" height="687" alt="Data Rankings" src="https://github.com/user-attachments/assets/a49f8ec1-e882-49bd-b158-0ac3169445c9" />
<img width="1818" height="715" alt="Global Map" src="https://github.com/user-attachments/assets/574a3cec-0f36-4449-bac0-51ba937fa599" />
<img width="959" height="412" alt="Global Overview" src="https://github.com/user-attachments/assets/54c53f84-f7e8-4651-b68f-c2886636022c" />
<img width="1801" height="621" alt="PopvsDensity" src="https://github.com/user-attachments/assets/59d0626c-0493-4841-9b12-5816f6c7fe82" />
<img width="1822" height="604" alt="Sex Ratios" src="https://github.com/user-attachments/assets/77cbd9f2-8abe-4498-854c-c8a563f25c08" />

✨ Key Features

The dashboard is organized into four distinct tabs for a clear user experience:

**🌎 Global Overview:**

A fully interactive Plotly Choropleth map to visualize metrics like population, density, and dependency ratios by country.

High-level global metric cards for total population, average density, and average sex ratio.

Expandable "Top 10" and "Bottom 10" lists for various metrics.

**📈 Demographic Deep-Dive:**

Age Structure Analysis: An interactive scatter plot comparing the percentage of young (0-14) vs. old (60+) populations, colored by continent.

Gender Analysis: A histogram showing the global distribution of sex ratios.

Density vs. Population: A log-scale scatter plot to analyze the relationship between a country's total population and its density.

**🔍 Country-Specific Analysis:**

A drill-down tool allowing users to select a single country using dropdown filters (by continent, then country).

Displays key metrics and a donut chart of the selected country's age structure (Youth, Working-Age, Elderly).

**🆚 Country Comparison:**

A powerful comparison tool using a \`st.multiselect\` widget.

Generates a faceted bar chart to compare multiple countries side-by-side across key demographic metrics, with independent y-axes for accurate comparison.

\## 📊 Data & Feature Engineering

The dashboard runs on a cleaned and enriched dataset. The original data was processed in a Jupyter Notebook (\`data_exploration.ipynb\`) to create more insightful metrics.

**Original Columns:**

\`\['Country', 'Population Aged 0 to 14 (%)', 'Population Aged 60 and Over (%)', 'Population density', 'Population(in millions)', 'Female Population(in millions)', 'Male Population(in millions)', 'Sex ratio (males per 100 females)'\]\`

**New Engineered Features:**

Working-Age Population (15-59) %: Calculated as \`100 - (% 0-14) - (% 60+)\`.

Youth Dependency Ratio: The number of young dependents for every 100 working-age people.

Old-Age Dependency Ratio: The number of elderly dependents for every 100 working-age people.

Total Dependency Ratio: The total number of dependents.

ISO Alpha-3 Codes: Generated using the \`country-converter\` library to enable mapping.

Continent: Generated using \`country-converter\` and \`pycountry-convert\` for filtering and grouping.

**\## 🛠️ Tech Stack**

Core: Python

Web Framework: Streamlit

Data Manipulation: Pandas

Data Visualization: Plotly Express

Data Preprocessing: Jupyter Notebook

Utilities: \`country-converter\` & \`pycountry-convert\` (for geographic data enrichment)

\## 💻 How to Run Locally

1\. Clone the repository:

\`\`\`bash

git clone <https://github.com/your-username/your-repo-name.git>

cd your-repo-name

\`\`\`

2\. Create a virtual environment (Recommended):

\`\`\`bash

python -m venv venv

source venv/bin/activate # On Windows: venv\\Scripts\\activate

\`\`\`

3\. Install the required packages:

\`\`\`bash

pip install -r requirements.txt

\`\`\`

4\. Run the Streamlit app:

\`\`\`bash

streamlit run app.py

\`\`\`

5\. Open your browser and go to \`<http://localhost:8501\`>
