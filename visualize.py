import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import itertools

# 初始化
np.random.seed(42)
num_values = 5

dim_values = {
    "Factory": ["ShanghaiPlant", "SingaporeSite", "BeijingFactory", "BerlinHub", "TexasUnit"],
    "ProcessUnit": ["BoilerRoom", "HVACZone", "CoolingTower", "PackagingLine", "AssemblyArea"],
    "Entity": [
        "AHU", "Chiller", "Zone", "Pump", "Room",  # 含 Equipment, System, Space
    ],
    "EntityType": ["Equipment", "System", "Space"],  # 新增：用于标记 Entity 类型
    "Phenomenon": ["steam", "light", "electricity", "gas", "liquid"],
    "Quantity": ["temp", "flow", "power", "pressure", "humidity"],
    "Role": ["entering", "leaving", "setpoint", "feedback", "calculated"],
    "ContextType": ["Technical", "Business", "Hybrid"],
    "ContextLocation": ["Field", "NonField", "Mixed"]
}


combinations = list(itertools.product(
    dim_values["Factory"],
    dim_values["ProcessUnit"],
    dim_values["Entity"],
    dim_values["Phenomenon"],
    dim_values["Quantity"],
    dim_values["Role"],
    dim_values["ContextType"],
    dim_values["ContextLocation"]
))

df = pd.DataFrame(combinations, columns=[
    "Factory", "ProcessUnit", "Entity",
    "Phenomenon", "Quantity", "Role",
    "ContextType", "ContextLocation"
])
df["ContextGroup"] = df["ContextType"] + ", " + df["ContextLocation"]

# 编码
for col in ["Factory", "ProcessUnit", "Entity", "Phenomenon", "Quantity", "Role"]:
    df[col + "_idx"] = df[col].astype("category").cat.codes

# RGB 映射
def map_to_color(row):
    r = int(255 * row["Phenomenon_idx"] / 4)
    g = int(255 * row["Quantity_idx"] / 4)
    b = int(255 * row["Role_idx"] / 4)
    return f"rgb({r},{g},{b})"
df["ColorRGB"] = df.apply(map_to_color, axis=1)

# 内嵌后三维坐标
offset = 0.15
df["X_embed"] = df["Factory_idx"] + offset * df["Phenomenon_idx"]
df["Y_embed"] = df["ProcessUnit_idx"] + offset * df["Quantity_idx"]
df["Z_embed"] = df["Entity_idx"] + offset * df["Role_idx"]

# Dash 应用
app = Dash(__name__)
app.title = "Semantic Address Space Explorer"

app.layout = html.Div([
    html.H1("Semantic Address Space (Embedded + Expandable)"),
    html.Div([
        html.Label("Context Type"),
        dcc.Dropdown(id="context-type", options=[{"label": c, "value": c} for c in dim_values["ContextType"]], value="Technical"),
        html.Label("Context Location"),
        dcc.Dropdown(id="context-location", options=[{"label": c, "value": c} for c in dim_values["ContextLocation"]], value="Field"),
    ], style={"width": "22%", "float": "left", "padding": "10px"}),
    html.Div([
        dcc.Graph(id="main-graph"),
        html.Hr(),
        html.Div(id="selection-label", style={"fontWeight": "bold"}),
        dcc.Graph(id="drill-graph")
    ], style={"width": "75%", "display": "inline-block", "padding": "0 20px"})
])

@app.callback(
    Output("main-graph", "figure"),
    Input("context-type", "value"),
    Input("context-location", "value"),
)
def update_graph(context_type, context_location):
    filtered = df[(df["ContextType"] == context_type) & (df["ContextLocation"] == context_location)]

    fig = px.scatter_3d(
        filtered,
        x="X_embed",
        y="Y_embed",
        z="Z_embed",
        color="ColorRGB",
        color_discrete_map="identity",
        hover_data=["Factory", "ProcessUnit", "Entity", "Phenomenon", "Quantity", "Role"]
    )
    fig.update_layout(
        title="Semantic Address Space with Embedded Expansion",
        scene=dict(
            xaxis=dict(
                title="Factory",
                tickmode='array',
                tickvals=[i + offset * 2 for i in range(num_values)],
                ticktext=dim_values["Factory"]
            ),
            yaxis=dict(
                title="ProcessUnit",
                tickmode='array',
                tickvals=[i + offset * 2 for i in range(num_values)],
                ticktext=dim_values["ProcessUnit"]
            ),
            zaxis=dict(
                title="Entity",
                tickmode='array',
                tickvals=[i + offset * 2 for i in range(num_values)],
                ticktext=dim_values["Entity"]
            )
        )
    )

    return fig

@app.callback(
    Output("drill-graph", "figure"),
    Output("selection-label", "children"),
    Input("main-graph", "clickData")
)
def show_detail(clickData):
    if clickData is None:
        return px.scatter_3d(), ""

    pt = clickData["points"][0]
    f, p, e = pt["customdata"][0], pt["customdata"][1], pt["customdata"][2]
    filtered = df[(df["Factory"] == f) & (df["ProcessUnit"] == p) & (df["Entity"] == e)]

    fig = px.scatter_3d(
        filtered,
        x="Phenomenon_idx",
        y="Quantity_idx",
        z="Role_idx",
        color="ColorRGB",
        color_discrete_map="identity",
        hover_data=["Phenomenon", "Quantity", "Role"]
    )

    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title="Phenomenon",
                tickmode='array',
                tickvals=list(range(len(dim_values["Phenomenon"]))),
                ticktext=dim_values["Phenomenon"]
            ),
            yaxis=dict(
                title="Quantity",
                tickmode='array',
                tickvals=list(range(len(dim_values["Quantity"]))),
                ticktext=dim_values["Quantity"]
            ),
            zaxis=dict(
                title="Role",
                tickmode='array',
                tickvals=list(range(len(dim_values["Role"]))),
                ticktext=dim_values["Role"]
            )
        ),
        title="Phenomenon × Quantity × Role"
    )
    return fig, f"🔍 Expanded: {f} → {p} → {e}"

if __name__ == '__main__':
    app.run(debug=True, port=8051)
