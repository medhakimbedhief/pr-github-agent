#!/usr/bin/env python3
"""
Simple webhook server for GitHub Actions events.
Stores events in a JSON file that the MCP server can read.
"""

import json
from datetime import datetime
from pathlib import Path
from aiohttp import web

# File to store events
EVENTS_FILE = Path(__file__).parent / "github_events.json"


async def handle_webhook(request):
    """Handle incoming GitHub webhook"""
    try:
        # Read the raw body first
        body = await request.read()

        # Log request details for debugging
        print(f"\n{'='*60}")
        print(f"📥 Incoming webhook")
        print(
            f"Event Type: {request.headers.get('X-GitHub-Event', 'unknown')}")
        print(f"Content-Length: {request.headers.get('Content-Length', '0')}")
        print(f"Body size: {len(body)} bytes")
        print(f"{'='*60}\n")

        # Handle empty body
        if not body:
            print("⚠️  Empty body received")
            return web.json_response({"error": "Empty request body"}, status=400)
        print(f"📄 Body (first 500 chars): {body[:500].decode('utf-8')}")
        # Parse JSON from body
        data = json.loads(body.decode('utf-8'))

        # Create event record
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": request.headers.get("X-GitHub-Event", "unknown"),
            "action": data.get("action"),
            "workflow_run": data.get("workflow_run"),
            "check_run": data.get("check_run"),
            "repository": data.get("repository", {}).get("full_name"),
            "sender": data.get("sender", {}).get("login")
        }

        print(f"✅ Event recorded: {event['event_type']} - {event['action']}")

        # Load existing events
        events = []
        if EVENTS_FILE.exists() and EVENTS_FILE.stat().st_size > 0 and event['action'] == "completed":
            try:
                with open(EVENTS_FILE, 'r') as f:
                    print(f"ℹ️  Loading existing events from {EVENTS_FILE}")
                    events = json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️  Events file was corrupted, starting fresh")
                events = []
        else:
            print(f"ℹ️  Events file does not exist or is empty, creating new one")

        # Add new event and keep last 100
        events.append(event)
        events = events[-100:]

        # Save events
        with open(EVENTS_FILE, 'w') as f:
            if "completed" in event:
                print(f"ℹ️  Saving events to {EVENTS_FILE}")
            json.dump(events, f, indent=2)

        return web.json_response({"status": "received"})
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"Raw body: {body[:500] if body else 'EMPTY'}")
        return web.json_response({"error": str(e)}, status=400)
    except Exception as e:
        print(f"❌ Error: {e}")
        return web.json_response({"error": str(e)}, status=400)

# Create app and add route
app = web.Application()
app.router.add_post('/webhook/github', handle_webhook)

if __name__ == '__main__':
    print("🚀 Starting webhook server on http://localhost:8080")
    print("📝 Events will be saved to:", EVENTS_FILE)
    print("🔗 Webhook URL: https://upload-hottest-forge-swap.trycloudflare.com")
    web.run_app(app, host='localhost', port=8080)
