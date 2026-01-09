#!/usr/bin/env python3
"""
Generate a Mintlify-compatible OpenAPI spec from the full API spec.
Filters to only include public endpoints and removes security schemes.
"""
import json
import sys
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DOCS_DIR = SCRIPT_DIR.parent
API_OPENAPI = Path("/Users/pierre/Sites/staminads/opensource/api/openapi.json")
OUTPUT_FILE = DOCS_DIR / "openapi.json"

# Endpoints to include (prefixes)
ALLOWED_PREFIXES = [
    '/api/analytics.',
    '/api/workspaces.',
    '/api/filters.',
]

def main():
    if not API_OPENAPI.exists():
        print(f"Error: {API_OPENAPI} not found. Run 'npm run openapi:generate' in the API first.")
        sys.exit(1)

    with open(API_OPENAPI) as f:
        spec = json.load(f)

    # Filter paths
    filtered_paths = {}
    for path, methods in spec['paths'].items():
        if any(path.startswith(prefix) for prefix in ALLOWED_PREFIXES):
            # Remove security from operations
            cleaned_methods = {}
            for method, op in methods.items():
                if isinstance(op, dict):
                    op = {k: v for k, v in op.items() if k != 'security'}
                cleaned_methods[method] = op
            filtered_paths[path] = cleaned_methods

    # Build clean spec (Mintlify-compatible)
    result = {
        'openapi': '3.0.3',
        'info': {
            'title': 'Staminads API',
            'description': 'Web analytics platform for tracking TimeScore metrics',
            'version': '1.0.0'
        },
        'servers': [
            {'url': 'https://your-instance.example.com', 'description': 'Your Staminads instance'}
        ],
        'paths': filtered_paths,
        'components': {
            'schemas': spec.get('components', {}).get('schemas', {})
        }
    }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"Generated {OUTPUT_FILE} with {len(filtered_paths)} endpoints")

if __name__ == '__main__':
    main()
