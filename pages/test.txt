import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Chart Builder", layout="wide")

# ---------------------------
# Sidebar – color palettes
# ---------------------------
st.sidebar.header("🎨 Color options")
PALETTES = {
    "Pastel": px.colors.qualitative.Pastel,
    "Bold": px.colors.qualitative.Bold,
    "Set2": px.colors.qualitative.Set2,
    "Dark2": px.colors.qualitative.Dark2,
    "Vivid": px.colors.qualitative.Vivid,
    "Safe": px.colors.qualitative.Safe,
    "Prism": px.colors.qualitative.Prism,
    "Alphabet": px.colors.qualitative.Alphabet,
}
palette_name = st.sidebar.selectbox("Color palette", list(PALETTES.keys()))
palette = PALETTES[palette_name]

# ---------------------------
# Tabs
# ---------------------------
tab1, tab2, tab3 = st.tabs(["1) Chart Builder", "2) (Empty)", "3) (Empty)"])

with tab1:
    st.title("📊 Chart Builder")

    # 0) Chart title
    st.subheader("0) Chart title")
    chart_title = st.text_input("Chart title", value="")

    # 0.5) Y-axis label (bar chart)
    st.subheader("0.5) Y-axis label (bar chart only)")
    y_axis_label = st.text_input("Y-axis label", value="")

    # 1) Table size
    st.subheader("1) Set table size")
    c1, c2 = st.columns(2)
    with c1:
        n_value_cols = st.number_input("Number of value columns", 1, 10, 3, 1)
    with c2:
        n_rows = st.number_input("Number of series (rows)", 1, 50, 5, 1)

    # 2) Chart type
    st.subheader("2) Choose chart type")
    chart_type = st.radio("Chart type", ["Bar chart", "Pie chart"], horizontal=True)

    # Internal column names
    internal_value_cols = [f"Value_{i}" for i in range(1, int(n_value_cols) + 1)]

    # 2.5) Legend label editor
    st.subheader("2.5) Rename legend labels (value columns)")
    st.caption("Value 컬럼의 표시 이름(legend)을 수정하세요.")

    if "value_col_labels" not in st.session_state or len(st.session_state["value_col_labels"]) != len(internal_value_cols):
        st.session_state["value_col_labels"] = [f"Category {i}" for i in range(1, int(n_value_cols) + 1)]

    labels_df = st.data_editor(
        pd.DataFrame({
            "Column": internal_value_cols,
            "Legend label": st.session_state["value_col_labels"],
        }),
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        disabled=["Column"],
        key="labels_editor",
    )

    st.session_state["value_col_labels"] = labels_df["Legend label"].astype(str).tolist()
    col_label_map = dict(zip(internal_value_cols, st.session_state["value_col_labels"]))

    # 3) Data input sheet
    st.subheader("3) Enter your data (Series + Values)")
    st.caption("첫 열은 Series(계열 이름), 값 열에는 숫자를 입력하세요.")

    sheet_cols = ["Series"] + internal_value_cols
    df_input = st.data_editor(
        pd.DataFrame([[""] * len(sheet_cols) for _ in range(int(n_rows))], columns=sheet_cols),
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        key="sheet_data",
    )

    # Pie value selection
    pie_value_internal = None
    if chart_type == "Pie chart":
        display_names = [col_label_map[c] for c in internal_value_cols]
        display_to_internal = dict(zip(display_names, internal_value_cols))
        chosen = st.selectbox("Choose value column for pie chart", display_names)
        pie_value_internal = display_to_internal[chosen]

    # 4) Generate button
    st.subheader("4) Generate chart")
    generate = st.button("📈 Generate chart")

    if generate:
        df = df_input.copy()
        df["Series"] = df["Series"].astype(str).replace("nan", "").str.strip()

        for c in internal_value_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        df = df.loc[~((df["Series"] == "") & (df[internal_value_cols].isna().all(axis=1)))]

        if df.empty:
            st.warning("No valid data to plot.")
        else:
            title_to_show = chart_title.strip() if chart_title else None

            if chart_type == "Bar chart":
                long_df = df.melt(
                    id_vars="Series",
                    value_vars=internal_value_cols,
                    var_name="Category",
                    value_name="Value",
                ).dropna(subset=["Value"])

                long_df["Category"] = long_df["Category"].map(col_label_map)

                if long_df.empty:
                    st.warning("No numeric values for bar chart.")
                else:
                    fig = px.bar(
                        long_df,
                        x="Series",
                        y="Value",
                        color="Category",
                        barmode="group",
                        color_discrete_sequence=palette,
                        title=title_to_show,
                    )
                    fig.update_layout(
                        height=520,
                        title=dict(x=0.5, xanchor="center", font=dict(size=24)),
                        yaxis_title=y_axis_label if y_axis_label else "Value",
                        legend_title_text="",
                        margin=dict(l=20, r=20, t=80, b=20),
                    )
                    st.plotly_chart(fig, use_container_width=True)

            else:  # Pie chart
                pie_df = df[["Series", pie_value_internal]].dropna(subset=[pie_value_internal])

                if pie_df.empty:
                    st.warning("No numeric values for pie chart.")
                else:
                    fig = px.pie(
                        pie_df,
                        names="Series",
                        values=pie_value_internal,
                        color_discrete_sequence=palette,
                        title=title_to_show if title_to_show else col_label_map[pie_value_internal],
                    )
                    fig.update_layout(
                        height=520,
                        title=dict(x=0.5, xanchor="center", font=dict(size=24)),
                        margin=dict(l=20, r=20, t=80, b=20),
                    )
                    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.empty()

with tab3:
    st.empty()
