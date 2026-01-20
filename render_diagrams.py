#!/usr/bin/env python3
"""
Convert mermaid diagrams to PNG using mermaid.ink online service
"""

import requests
import base64
import re
from pathlib import Path

def extract_diagrams(md_file):
    """Extract mermaid diagrams and titles from markdown."""
    content = Path(md_file).read_text()
    
    # Find section headers
    heading_pattern = r'## (.*?)\n'
    diagram_pattern = r'```mermaid\n(.*?)\n```'
    
    headings_with_pos = [(m.start(), m.group(1)) for m in re.finditer(heading_pattern, content)]
    diagrams_with_pos = [(m.start(), m.group(1)) for m in re.finditer(diagram_pattern, content, re.DOTALL)]
    
    result = []
    for heading_idx, (heading_pos, heading_text) in enumerate(headings_with_pos):
        # Find diagram after this heading but before next heading
        next_heading_pos = headings_with_pos[heading_idx + 1][0] if heading_idx + 1 < len(headings_with_pos) else float('inf')
        
        for diagram_pos, diagram_code in diagrams_with_pos:
            if heading_pos < diagram_pos < next_heading_pos:
                result.append((heading_text.strip(), diagram_code.strip()))
                break
    
    return result

def render_diagram(mermaid_code, output_path):
    """Render using mermaid.ink service."""
    try:
        # Encode the diagram code in base64 for mermaid.ink
        encoded = base64.b64encode(mermaid_code.encode()).decode()
        url = f"https://mermaid.ink/img/{encoded}"
        
        print(f"  Downloading...", end=" ", flush=True)
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(output_path).write_bytes(response.content)
            print(f"✓")
            return True
        else:
            print(f"✗ (HTTP {response.status_code})")
            return False
    except requests.exceptions.Timeout:
        print(f"✗ (Timeout)")
        return False
    except Exception as e:
        print(f"✗ ({e})")
        return False

def main():
    md_file = "UML_Behavioral_Diagram.md"
    diagrams = extract_diagrams(md_file)
    
    if not diagrams:
        print(f"No diagrams found in {md_file}")
        return
    
    print(f"Found {len(diagrams)} diagram(s)\n")
    
    output_dir = Path("diagrams")
    success_count = 0
    
    for i, (title, code) in enumerate(diagrams, 1):
        safe_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '_')
        output_file = output_dir / f"{i:02d}_{safe_title}.png"
        
        print(f"[{i}/{len(diagrams)}] {title}")
        print(f"  → {output_file}... ", end="", flush=True)
        
        if render_diagram(code, str(output_file)):
            success_count += 1
    
    print(f"\nResult: {success_count}/{len(diagrams)} diagrams rendered successfully")
    if success_count > 0:
        print(f"PNG files saved to ./{output_dir}/ directory")

if __name__ == "__main__":
    main()
