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
    '/api/export.',
]

def add_export_user_events_response(paths):
    """Add detailed response schema with example for export.userEvents endpoint."""
    if '/api/export.userEvents' not in paths:
        return

    paths['/api/export.userEvents']['get']['responses']['200'] = {
        'description': 'List of user events with pagination cursor',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'data': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'id': {'type': 'string'},
                                    'session_id': {'type': 'string'},
                                    'user_id': {'type': 'string'},
                                    'name': {'type': 'string', 'enum': ['screen_view', 'goal']},
                                    'path': {'type': 'string'},
                                    'created_at': {'type': 'string', 'format': 'date-time'},
                                    'updated_at': {'type': 'string', 'format': 'date-time'},
                                    'referrer': {'type': 'string'},
                                    'referrer_domain': {'type': 'string'},
                                    'is_direct': {'type': 'boolean'},
                                    'landing_page': {'type': 'string'},
                                    'landing_domain': {'type': 'string'},
                                    'landing_path': {'type': 'string'},
                                    'utm_source': {'type': 'string'},
                                    'utm_medium': {'type': 'string'},
                                    'utm_campaign': {'type': 'string'},
                                    'utm_term': {'type': 'string'},
                                    'utm_content': {'type': 'string'},
                                    'utm_id': {'type': 'string'},
                                    'utm_id_from': {'type': 'string'},
                                    'channel': {'type': 'string'},
                                    'channel_group': {'type': 'string'},
                                    'stm_1': {'type': 'string'},
                                    'stm_2': {'type': 'string'},
                                    'stm_3': {'type': 'string'},
                                    'stm_4': {'type': 'string'},
                                    'stm_5': {'type': 'string'},
                                    'stm_6': {'type': 'string'},
                                    'stm_7': {'type': 'string'},
                                    'stm_8': {'type': 'string'},
                                    'stm_9': {'type': 'string'},
                                    'stm_10': {'type': 'string'},
                                    'device': {'type': 'string'},
                                    'browser': {'type': 'string'},
                                    'browser_type': {'type': 'string'},
                                    'os': {'type': 'string'},
                                    'country': {'type': 'string'},
                                    'region': {'type': 'string'},
                                    'city': {'type': 'string'},
                                    'language': {'type': 'string'},
                                    'timezone': {'type': 'string'},
                                    'goal_name': {'type': 'string'},
                                    'goal_value': {'type': 'number'},
                                    'goal_timestamp': {'type': 'string', 'format': 'date-time', 'nullable': True},
                                    'page_number': {'type': 'integer'},
                                    'duration': {'type': 'integer'},
                                    'max_scroll': {'type': 'integer'},
                                }
                            }
                        },
                        'next_cursor': {'type': 'string', 'nullable': True},
                        'has_more': {'type': 'boolean'}
                    }
                },
                'example': {
                    'data': [
                        {
                            'id': '019412ab-1234-7def-8000-abcdef123456',
                            'session_id': '019412ab-5678-7abc-8000-123456abcdef',
                            'user_id': 'user_12345',
                            'name': 'screen_view',
                            'path': '/pricing',
                            'created_at': '2025-01-20T14:30:00.000Z',
                            'updated_at': '2025-01-20T14:32:15.000Z',
                            'referrer': 'https://www.google.com/search?q=analytics',
                            'referrer_domain': 'www.google.com',
                            'is_direct': False,
                            'landing_page': 'https://example.com/',
                            'landing_domain': 'example.com',
                            'landing_path': '/',
                            'utm_source': 'google',
                            'utm_medium': 'cpc',
                            'utm_campaign': 'brand_2025',
                            'utm_term': '',
                            'utm_content': '',
                            'utm_id': '',
                            'utm_id_from': '',
                            'channel': 'Google Ads',
                            'channel_group': 'Paid Search',
                            'stm_1': 'premium',
                            'stm_2': '',
                            'stm_3': '',
                            'stm_4': '',
                            'stm_5': '',
                            'stm_6': '',
                            'stm_7': '',
                            'stm_8': '',
                            'stm_9': '',
                            'stm_10': '',
                            'device': 'Desktop',
                            'browser': 'Chrome',
                            'browser_type': 'standard',
                            'os': 'macOS',
                            'country': 'US',
                            'region': 'California',
                            'city': 'San Francisco',
                            'language': 'en-US',
                            'timezone': 'America/Los_Angeles',
                            'goal_name': '',
                            'goal_value': 0,
                            'goal_timestamp': None,
                            'page_number': 2,
                            'duration': 135,
                            'max_scroll': 75
                        }
                    ],
                    'next_cursor': 'eyJ0IjoxNzA1NzYwMjAwMDAwLCJpIjoiMDE5NDEyYWItMTIzNC03ZGVmLTgwMDAtYWJjZGVmMTIzNDU2In0=',
                    'has_more': True
                }
            }
        }
    }


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

    # Add custom response schemas
    add_export_user_events_response(filtered_paths)

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
