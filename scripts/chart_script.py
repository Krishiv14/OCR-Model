import plotly.graph_objects as go
import plotly.express as px
import json

# Parse the workflow data with shorter, clearer text
workflow_data = {
    "workflow_steps": [
        {"step": "Start", "type": "start", "description": "User opens Streamlit app"},
        {"step": "API Setup", "type": "process", "description": "Enter Moondream API key"},
        {"step": "Upload", "type": "process", "description": "Upload test & master images"},
        {"step": "Extract", "type": "process", "description": "Moondream processes both images"},
        {"step": "Compare", "type": "decision", "description": "Are texts identical?"},
        {"step": "Pass", "type": "result_pass", "description": "Validation successful"},
        {"step": "Fail", "type": "result_fail", "description": "Validation failed"},
        {"step": "Analysis", "type": "process", "description": "Show character differences"},
        {"step": "End", "type": "end", "description": "Display final results"}
    ]
}

# Define positions for each step with better spacing
positions = {
    "Start": (0, 10),
    "API Setup": (0, 8.5),
    "Upload": (0, 7),
    "Extract": (0, 5.5),
    "Compare": (0, 4),
    "Pass": (-2.5, 2.5),
    "Fail": (2.5, 2.5),
    "Analysis": (2.5, 1),
    "End": (0, 0)
}

# Define colors - using more distinct green for start/end and pass
type_colors = {
    "start": "#5D878F",    # Cyan (more green-looking)
    "end": "#5D878F",      # Cyan (more green-looking)
    "process": "#1FB8CD",  # Strong cyan (blue)
    "decision": "#FFC185", # Light orange
    "result_pass": "#5D878F", # Cyan (more green-looking)
    "result_fail": "#B4413C"  # Moderate red
}

# Define connections (from step to step)
connections = [
    ("Start", "API Setup"),
    ("API Setup", "Upload"),
    ("Upload", "Extract"),
    ("Extract", "Compare"),
    ("Compare", "Pass"),
    ("Compare", "Fail"),
    ("Fail", "Analysis"),
    ("Analysis", "End"),
    ("Pass", "End")
]

# Create the figure
fig = go.Figure()

# Add connection lines with thicker arrows
for start_step, end_step in connections:
    start_pos = positions[start_step]
    end_pos = positions[end_step]
    
    # Add arrow line
    fig.add_trace(go.Scatter(
        x=[start_pos[0], end_pos[0]],
        y=[start_pos[1], end_pos[1]],
        mode='lines',
        line=dict(color='#13343B', width=3),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add arrowhead
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    length = (dx**2 + dy**2)**0.5
    
    if length > 0:
        # Normalize direction
        dx_norm = dx / length
        dy_norm = dy / length
        
        # Arrow position (closer to end point)
        arrow_x = end_pos[0] - 0.3 * dx_norm
        arrow_y = end_pos[1] - 0.3 * dy_norm
        
        fig.add_annotation(
            x=arrow_x,
            y=arrow_y,
            ax=start_pos[0],
            ay=start_pos[1],
            xref='x',
            yref='y',
            axref='x',
            ayref='y',
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=3,
            arrowcolor='#13343B',
            showarrow=True,
            text="",
        )

# Add shapes and text for each step
for step_data in workflow_data["workflow_steps"]:
    step_name = step_data["step"]
    step_type = step_data["type"]
    description = step_data["description"]
    
    x, y = positions[step_name]
    color = type_colors[step_type]
    
    # Add shapes based on type with larger sizes
    if step_type in ["start", "end"]:
        # Oval shape (larger)
        fig.add_shape(
            type="circle",
            x0=x-1.0, y0=y-0.5,
            x1=x+1.0, y1=y+0.5,
            fillcolor=color,
            line=dict(color="white", width=3),
        )
    elif step_type == "decision":
        # Diamond shape (larger)
        fig.add_shape(
            type="path",
            path=f"M {x},{y-0.6} L {x+1.0},{y} L {x},{y+0.6} L {x-1.0},{y} Z",
            fillcolor=color,
            line=dict(color="white", width=3),
        )
    else:
        # Rectangle shape (larger)
        fig.add_shape(
            type="rect",
            x0=x-1.0, y0=y-0.5,
            x1=x+1.0, y1=y+0.5,
            fillcolor=color,
            line=dict(color="white", width=3),
        )
    
    # Add text with better formatting
    fig.add_annotation(
        x=x, y=y,
        text=f"<b>{step_name}</b>",
        showarrow=False,
        font=dict(size=14, color="white"),
        align="center"
    )

# Add larger labels for decision branches
fig.add_annotation(
    x=-1.2, y=3.2,
    text="<b>Yes</b>",
    showarrow=False,
    font=dict(size=12, color="white"),
    bgcolor="#5D878F",
    bordercolor="white",
    borderwidth=2,
    borderpad=4
)

fig.add_annotation(
    x=1.2, y=3.2,
    text="<b>No</b>",
    showarrow=False,
    font=dict(size=12, color="white"),
    bgcolor="#B4413C",
    bordercolor="white",
    borderwidth=2,
    borderpad=4
)

# Update layout
fig.update_layout(
    title="OCR Validation Workflow",
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[-4, 4]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[-0.5, 11]
    ),
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

fig.write_image("ocr_workflow_chart.png")