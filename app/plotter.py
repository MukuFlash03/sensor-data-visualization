import plotly.graph_objs as go
from plotly.subplots import make_subplots


def plot_data(allData):

    # Create subplots
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Temperature", "pH Value", "Distilled Oxygen", "Pressure"))

    # Add traces
    trace1 = go.Scatter(x=[row[0] for row in allData[0]], y=[row[1] for row in allData[0]], mode='lines', name='Temperature')
    fig.add_trace(trace1, row=1, col=1)
    fig.update_xaxes(title_text="Time", row=1, col=1)
    fig.update_yaxes(title_text="Temperature (Celsius)", row=1, col=1)

    trace2 = go.Scatter(x=[row[0] for row in allData[1]], y=[row[1] for row in allData[1]], mode='lines', name='pH')
    fig.add_trace(trace2, row=1, col=2)
    fig.update_xaxes(title_text="Time", row=1, col=2)
    fig.update_yaxes(title_text="pH Value", row=1, col=2)

    trace3 = go.Scatter(x=[row[0] for row in allData[2]], y=[row[1] for row in allData[2]], mode='lines', name='Distilled_O2')
    fig.add_trace(trace3, row=2, col=1)
    fig.update_xaxes(title_text="Time", row=2, col=1)
    fig.update_yaxes(title_text="Distilled Oxygen (%)", row=2, col=1)

    trace4 = go.Scatter(x=[row[0] for row in allData[3]], y=[row[1] for row in allData[3]], mode='lines', name='Pressure')
    fig.add_trace(trace4, row=2, col=2)
    fig.update_xaxes(title_text="Time", row=2, col=2)
    fig.update_yaxes(title_text="Pressure (psi)", row=2, col=2)

    fig.update_layout(
        height=800, width=1200, 
        title=dict(text='Parameters Time-Series Plots', x=0.5, y=0.5),
        margin=dict(l=50, r=50, t=50, b=50)
    )

    return fig