#!/usr/bin/env python3
import requests
import base64
import re
from pathlib import Path

content = Path('UML_Class_Diagram.md').read_text()
match = re.search(r'```mermaid\n(.*?)\n```', content, re.DOTALL)

if match:
    mermaid_code = match.group(1).strip()
    encoded = base64.b64encode(mermaid_code.encode()).decode()
    url = f'https://mermaid.ink/img/{encoded}'
    
    print('Rendering Class Diagram...', end=' ', flush=True)
    response = requests.get(url, timeout=30)
    
    if response.status_code == 200:
        Path('diagrams').mkdir(exist_ok=True)
        Path('diagrams/05_Class_Diagram.png').write_bytes(response.content)
        print('✓')
    else:
        print(f'✗ (HTTP {response.status_code})')
else:
    print('No mermaid diagram found')
