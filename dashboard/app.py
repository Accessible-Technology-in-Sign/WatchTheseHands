import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from db_connection import db

app = dash.Dash(__name__)
app.title = "Annotation Dashboard"

app.layout = html.Div([
    html.Div([
        html.H1("Annotation Dashboard", 
                style={'textAlign': 'center', 'marginBottom': '30px', 'color': '#2c3e50'}),
        
        html.Div([
            html.Div([
                html.Label("Select Sign:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
                dcc.Dropdown(
                    id='sign-dropdown',
                    options=[{'label': 'All Signs', 'value': 'All Signs'}] + 
                            [{'label': sign, 'value': sign} for sign in db.get_all_signs()],
                    value='All Signs',
                    style={'marginBottom': '20px'}
                )
            ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
            
            html.Div([
                html.Label("Select Annotator:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
                dcc.Dropdown(
                    id='user-dropdown',
                    options=[{'label': 'All Users', 'value': 'All Users'}] + 
                            [{'label': user, 'value': user} for user in db.get_all_users()],
                    value='All Users',
                    style={'marginBottom': '20px'}
                )
            ], style={'width': '48%', 'display': 'inline-block'})
        ], style={'marginBottom': '30px'}),
        
        html.Div([
            html.Div(id='sign-stats', style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
            html.Div(id='user-stats', style={'width': '48%', 'display': 'inline-block'})
        ], style={'marginBottom': '30px'}),
        
        html.Div([
            html.Div([
                html.H3("Label Distribution by Sign", 
                       style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#34495e'}),
                dcc.Graph(id='sign-pie-chart')
            ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
            
            html.Div([
                html.H3("Label Distribution by Annotator", 
                       style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#34495e'}),
                dcc.Graph(id='user-pie-chart')
            ], style={'width': '48%', 'display': 'inline-block'})
        ])
        
    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})
])

@callback(
    [Output('sign-pie-chart', 'figure'),
     Output('user-pie-chart', 'figure'),
     Output('sign-stats', 'children'),
     Output('user-stats', 'children')],
    [Input('sign-dropdown', 'value'),
     Input('user-dropdown', 'value')]
)
def update_charts(selected_sign, selected_user):
    """Update charts based on dropdown selections"""
    
    sign_labels = db.get_labels_by_sign(selected_sign)
    sign_stats = db.get_sign_stats(selected_sign)
    
    user_labels = db.get_labels_by_user(selected_user)
    user_stats = db.get_user_stats(selected_user)
    
    if sign_labels:
        sign_fig = px.pie(
            values=list(sign_labels.values()),
            names=list(sign_labels.keys()),
            title=f"Labels for {selected_sign}",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        sign_fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        sign_fig.update_layout(
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.01),
            margin=dict(l=20, r=20, t=40, b=20)
        )
    else:
        sign_fig = go.Figure()
        sign_fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        sign_fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
    
    if user_labels:
        user_fig = px.pie(
            values=list(user_labels.values()),
            names=list(user_labels.keys()),
            title=f"Labels by {selected_user}",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        user_fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        user_fig.update_layout(
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.01),
            margin=dict(l=20, r=20, t=40, b=20)
        )
    else:
        user_fig = go.Figure()
        user_fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        user_fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
    
    sign_stats_card = html.Div([
        html.H4(f"{selected_sign} Statistics", style={'color': '#2c3e50', 'marginBottom': '10px'}),
        html.P(f"Total Annotations: {sign_stats.get('total_annotations', 0)}"),
        html.P(f"Unique Users: {sign_stats.get('unique_users', 0)}"),
        html.P(f"Unique Videos: {sign_stats.get('unique_videos', 0)}")
    ], style={
        'backgroundColor': '#ecf0f1',
        'padding': '15px',
        'borderRadius': '8px',
        'border': '1px solid #bdc3c7'
    })
    
    user_stats_card = html.Div([
        html.H4(f"{selected_user} Statistics", style={'color': '#2c3e50', 'marginBottom': '10px'}),
        html.P(f"Total Annotations: {user_stats.get('total_annotations', 0)}"),
        html.P(f"Unique Signs: {user_stats.get('unique_signs', 0)}"),
        html.P(f"Unique Videos: {user_stats.get('unique_videos', 0)}")
    ], style={
        'backgroundColor': '#ecf0f1',
        'padding': '15px',
        'borderRadius': '8px',
        'border': '1px solid #bdc3c7'
    })
    
    return sign_fig, user_fig, sign_stats_card, user_stats_card

if __name__ == '__main__':
    print("Starting Annotation Dashboard...")
    print("Dashboard will be available at: http://127.0.0.1:8050")
    print("Make sure your MySQL database is running!")
    
    try:
        app.run_server(debug=True, host='127.0.0.1', port=8050)
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
    except Exception as e:
        print(f"Error starting dashboard: {e}")
    finally:
        db.close()
