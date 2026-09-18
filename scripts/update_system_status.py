import os
import json
import urllib.request
from datetime import datetime

USERNAME = "PrabuArvindM"

def fetch_repo_count():
    url = f"https://api.github.com/users/{USERNAME}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Use token if available to avoid rate limits
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers['Authorization'] = f"token {token}"
        
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("public_repos", "Unknown")
    except Exception as e:
        print(f"Error fetching data: {e}")
        return "Unknown"

def update_svg(repo_count):
    svg_path = os.path.join(os.path.dirname(__file__), "..", "assets", "system-status.svg")
    
    if not os.path.exists(svg_path):
        print(f"SVG not found at {svg_path}")
        return
        
    with open(svg_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    from datetime import timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    
    # We will inject the dynamic info into the SVG.
    # Let's add a dynamic text block if it doesn't exist, or replace it if it does.
    
    # Find the closing </g> of the columns
    # Actually, let's just replace a placeholder.
    
    # For safety, we'll append to the SVG if not present.
    dynamic_element = f"""
  <!-- DYNAMIC_STATS_START -->
  <g transform="translate(620, 20)">
    <text x="0" y="0" font-family="'Fira Code', monospace" font-size="10" fill="#8892B0">LAST SYNC: {now}</text>
    <text x="0" y="15" font-family="'Fira Code', monospace" font-size="10" fill="#8892B0">REPOSITORIES: {repo_count}</text>
  </g>
  <!-- DYNAMIC_STATS_END -->
</svg>"""

    if "<!-- DYNAMIC_STATS_START -->" in content:
        import re
        content = re.sub(r'<!-- DYNAMIC_STATS_START -->.*<!-- DYNAMIC_STATS_END -->\n</svg>', dynamic_element, content, flags=re.DOTALL)
    else:
        content = content.replace("</svg>", dynamic_element)
        
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Updated SVG with repo count: {repo_count} at {now}")

if __name__ == "__main__":
    count = fetch_repo_count()
    update_svg(count)
