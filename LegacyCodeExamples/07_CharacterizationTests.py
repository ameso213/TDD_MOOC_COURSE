# 07_CharacterizationTests.py
# Real-life example: Snapshot testing a UI component library.
# Tests capture HTML output, alerting to unintended changes.

# Using a simple dict as "snapshot"
def render_button(label):
    return f"<button>{label}</button>"

# Characterization test (manual snapshot)
# snapshot = render_button("Click me")  # "<button>Click me</button>"
# assert render_button("Click me") == snapshot

# Real-life example: Golden master testing for a data export tool.
# Tests verify exact output files match.

def export_data(data):
    # Complex logic
    return "\n".join(f"{k}: {v}" for k, v in data.items())

# Characterization
# master = export_data({"name": "John", "age": 30})
# # master = "name: John\nage: 30"
# assert export_data({"name": "John", "age": 30}) == master

# After refactor, ensure output matches master.