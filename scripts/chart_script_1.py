import plotly.graph_objects as go
import plotly.express as px

# Data from the provided JSON
data = {
    "files": [
        {"name": "ocr-validation-tool/", "type": "root", "level": 0},
        {"name": "ocr_validation_app.py", "type": "main", "level": 1, "description": "Main Streamlit app"},
        {"name": "requirements.txt", "type": "config", "level": 1, "description": "Dependencies"},
        {"name": "README.md", "type": "docs", "level": 1, "description": "Documentation"},
        {"name": "PROJECT_OVERVIEW.md", "type": "docs", "level": 1, "description": "File listing"},
        {"name": ".gitignore", "type": "config", "level": 1, "description": "Git ignore"},
        {"name": "ocr_validation_cli.py", "type": "utility", "level": 1, "description": "CLI version"},
        {"name": "create_sample_images.py", "type": "utility", "level": 1, "description": "Test image generator"},
        {"name": "run.sh", "type": "utility", "level": 1, "description": "Unix/Mac startup script"},
        {"name": "run.bat", "type": "utility", "level": 1, "description": "Windows startup script"},
        {"name": "ocr_workflow_chart.png", "type": "generated", "level": 1, "description": "Workflow diagram"},
        {"name": ".streamlit/", "type": "folder", "level": 1},
        {"name": "config.toml", "type": "config", "level": 2, "description": "Streamlit config"},
        {"name": "secrets_sample.toml", "type": "config", "level": 2, "description": "API key template"}
    ]
}

# Define colors for different file types as specified
color_map = {
    'root': '#13343B',      # Dark cyan for root folder
    'folder': '#13343B',    # Dark cyan for folders
    'main': '#1FB8CD',      # Blue for main application files
    'config': '#FFC185',    # Orange for configuration files
    'docs': '#ECEBD5',      # Green for documentation files
    'utility': '#944454',   # Purple for utility files
    'generated': '#964325'  # Gray for generated files
}

# Create the tree structure text with proper indentation
tree_lines = []
colors = []
hover_texts = []
y_positions = []

# Tree symbols for visual structure
tree_symbols = {
    'root': '',
    'branch': '├── ',
    'last_branch': '└── ',
    'indent': '    '
}

# Process files and create tree structure
for i, item in enumerate(data['files']):
    name = item['name']
    level = item['level']
    file_type = item['type']
    
    # Create tree line with proper indentation and symbols
    if level == 0:
        # Root folder
        tree_line = name
    elif level == 1:
        # Check if this is the last item at level 1
        remaining_level1 = [f for f in data['files'][i+1:] if f['level'] == 1]
        if len(remaining_level1) == 0:
            tree_line = '└── ' + name
        else:
            tree_line = '├── ' + name
    elif level == 2:
        # Sub-items (currently only .streamlit folder contents)
        # Check if this is the last item at level 2
        remaining_level2 = [f for f in data['files'][i+1:] if f['level'] == 2]
        if len(remaining_level2) == 0:
            tree_line = '    └── ' + name
        else:
            tree_line = '    ├── ' + name
    
    tree_lines.append(tree_line)
    colors.append(color_map[file_type])
    
    # Create hover text with description
    hover_text = f"{name}"
    if 'description' in item:
        hover_text += f"<br>{item['description']}"
    hover_text += f"<br>Type: {file_type}"
    hover_texts.append(hover_text)
    
    # Y position (reverse order for top-to-bottom display)
    y_positions.append(len(data['files']) - i)

# Create scatter plot for text positioning
fig = go.Figure()

# Add text annotations for each file/folder
for i, (line, color, hover_text, y_pos) in enumerate(zip(tree_lines, colors, hover_texts, y_positions)):
    fig.add_trace(go.Scatter(
        x=[0],
        y=[y_pos],
        mode='markers+text',
        text=line,
        textposition='middle right',
        textfont=dict(
            family='Courier New, monospace',
            size=14,
            color=color
        ),
        marker=dict(
            size=1,
            color='rgba(0,0,0,0)'  # Transparent markers
        ),
        hovertemplate=hover_text + '<extra></extra>',
        showlegend=False,
        cliponaxis=False
    ))

# Update layout for clean tree display
fig.update_layout(
    title="OCR Tool Directory Tree",
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-0.5, 8]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[0, len(data['files']) + 1]
    ),
    plot_bgcolor='white',
    showlegend=False
)

# Save the chart
fig.write_image("ocr_file_tree.png")