import altair as alt
import pandas as pd
import streamlit as st

st.title("Illinois Building Inventory")

URL = (
    "https://raw.githubusercontent.com/"
    "UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(URL)
    df["Year Constructed"] = pd.to_numeric(
        df["Year Constructed"], errors="coerce"
    )
    df["Square Footage"] = pd.to_numeric(
        df["Square Footage"], errors="coerce"
    )
    return df[
        df["Year Constructed"].between(1800, 2026)
        & df["Square Footage"].gt(0)
    ].copy()


df = load_data()
alt.data_transformers.disable_max_rows()

st.markdown(f"[Dataset source]({URL})")
st.caption(
    "Both charts use records with positive floor area and construction "
    "years from 1800 through 2026."
)

agency = st.selectbox(
    "Choose an agency to update both visualizations",
    ["All agencies"] + sorted(df["Agency Name"].dropna().unique()),
)

if agency != "All agencies":
    df = df[df["Agency Name"] == agency].copy()

st.subheader("1. Building size and construction year")

scatter = (
    alt.Chart(df)
    .mark_circle(size=35, opacity=0.35, color="#087F8C")
    .encode(
        x=alt.X(
            "Year Constructed:Q",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(format="d"),
        ),
        y=alt.Y(
            "Square Footage:Q",
            scale=alt.Scale(type="log"),
            title="Floor area (square feet, log scale)",
        ),
    )
)

st.altair_chart(scatter, use_container_width=True)

st.write(
    "The first visualization highlights how building size varies with "
    "construction year. Each circle represents one inventory record. "
    "Construction year uses a linear horizontal scale, while floor area "
    "uses a logarithmic vertical scale because building sizes span a wide "
    "range. Transparent teal circles help reveal overlapping records "
    "without introducing unnecessary color categories. The agency dropdown "
    "filters the plotted records, providing interaction beyond zoom or "
    "tooltips. With more time, I would add small multiples to compare "
    "agencies directly."
)

st.subheader("2. Construction decades represented in the inventory")

df["Decade"] = (df["Year Constructed"].astype(int) // 10) * 10

counts = df.groupby("Decade").size()
decades = range(int(counts.index.min()), int(counts.index.max()) + 10, 10)

summary = (
    counts.reindex(decades, fill_value=0)
    .rename_axis("Decade")
    .reset_index(name="Records")
)

line = (
    alt.Chart(summary)
    .mark_line(point=True, color="#C16A28")
    .encode(
        x=alt.X(
            "Decade:Q",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(format="d", tickMinStep=10),
        ),
        y=alt.Y(
            "Records:Q",
            title="Number of inventory records",
            scale=alt.Scale(zero=True),
        ),
    )
)

st.altair_chart(line, use_container_width=True)

st.write(
    "The second visualization highlights which construction decades are "
    "most represented in the inventory. Orange points show record counts, "
    "and connecting lines emphasize changes between adjacent decades. "
    "The horizontal scale preserves equal spacing between decades, and "
    "the vertical count scale begins at zero. Decades without records "
    "are included as zeros. The agency dropdown also updates this chart. "
    "These totals describe buildings listed in the dataset rather than "
    "all historical construction. With more time, I would investigate "
    "whether records with missing construction years change the pattern."
)

st.caption(
    "Homework #5: These are new visualizations using a different dataset "
    "from my UFO project. No plots or write-up text were reused."
)
