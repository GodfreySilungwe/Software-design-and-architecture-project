#!/usr/bin/env python3
"""
Export mermaid diagrams from UML_Behavioral_Diagram.md to PNG images
using kroki.io or mermaid.ink online service
"""

import requests
import base64
import re
from pathlib import Path

# Read the behavioral diagram file
diagram_file = Path("UML_Behavioral_Diagram.md")
content = diagram_file.read_text()

# Extract mermaid diagrams
# Pattern: ```mermaid\n...```
pattern = r'```mermaid\n(.*?)\n```'
matches = re.finditer(pattern, content, re.DOTALL)

diagrams = []
for i, match in enumerate(matches, 1):
    mermaid_code = match.group(1)
    diagrams.append((f"diagram_{i}", mermaid_code))

print(f"Found {len(diagrams)} mermaid diagrams")

# Export each diagram using mermaid.ink
for name, mermaid_code in diagrams:
    # Encode diagram
    encoded = base64.b64encode(mermaid_code.encode()).decode()
    
    # Use mermaid.ink service
    url = f"https://mermaid.ink/img/{encoded}"
    
    try:
        print(f"Exporting {name}...", end=" ")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            output_file = Path(f"diagrams/{name}.png")
            output_file.parent.mkdir(exist_ok=True)
            output_file.write_bytes(response.content)
            print(f"✓ Saved to {output_file}")
        else:
            print(f"✗ Failed (HTTP {response.status_code})")
    except Exception as e:
        print(f"✗ Error: {e}")

print("\nDone! Images saved to ./diagrams/ directory")
