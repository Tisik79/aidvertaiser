"""Shared OAuth callback server for browser-based authentication.

This module provides a local HTTP server that handles OAuth callbacks from both
Google and Meta authentication flows. It runs in a background thread and supports:

    - Google OAuth (authorization code flow via /callback/google)
    - Meta OAuth (implicit flow with fragment extraction via /callback)

Token Caching:
    Tokens are persistently cached to ~/.unified-ads-mcp/ directory.
"""

import json
import sys
import threading
import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse, parse_qs

# Token storage (in-memory for current session)
_tokens: dict[str, dict] = {}
_server: Optional[HTTPServer] = None
_server_thread: Optional[threading.Thread] = None
_port: int = 8888

# Persistent token cache directory
TOKEN_CACHE_DIR = Path.home() / ".unified-ads-mcp"


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP request handler for OAuth callbacks from Google and Meta."""

    def log_message(self, format: str, *args) -> None:
        """Suppress default HTTP logging."""
        pass

    def do_GET(self) -> None:
        """Handle GET requests for OAuth callbacks."""
        parsed = urlparse(self.path)

        if parsed.path == "/callback/google":
            self._handle_google_callback(parsed)
        elif parsed.path == "/callback/meta":
            self._handle_meta_callback(parsed)
        elif parsed.path == "/callback":
            # Meta uses fragment - serve JS to extract it
            self._serve_meta_fragment_handler()
        elif parsed.path == "/health":
            self._send_json({"status": "ok", "port": _port})
        else:
            self.send_error(404, "Not Found")

    def do_POST(self) -> None:
        """Handle POST requests for Meta token submission."""
        if self.path == "/callback/meta":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                if "access_token" in data:
                    token_data = {
                        "access_token": data["access_token"],
                        "expires_in": data.get("expires_in", 3600),
                        "created_at": int(time.time()),
                    }
                    _tokens["meta"] = token_data
                    save_token("meta", token_data)
                    self._send_json({"status": "success"})
                    print("[OAuth] Meta token received and saved", file=sys.stderr)
                else:
                    self._send_json(
                        {"status": "error", "message": "No token in request"}
                    )
            except json.JSONDecodeError as e:
                self._send_json({"status": "error", "message": f"Invalid JSON: {e}"})
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)})
        else:
            self.send_error(404, "Not Found")

    def _handle_google_callback(self, parsed) -> None:
        """Handle Google OAuth callback with authorization code."""
        params = parse_qs(parsed.query)

        if "code" in params:
            code = params["code"][0]
            _tokens["google_code"] = code
            print("[OAuth] Google authorization code received", file=sys.stderr)
            self._send_success_page(
                "Google Ads Authentication Successful",
                "Your Google Ads account has been connected. You can close this window.",
            )
        elif "error" in params:
            error = params.get("error", ["Unknown error"])[0]
            error_desc = params.get("error_description", [""])[0]
            self._send_error_page(
                "Google Ads Authentication Failed", f"Error: {error}. {error_desc}"
            )
        else:
            self._send_error_page(
                "Google Ads Authentication Failed",
                "No authorization code received in the callback.",
            )

    def _handle_meta_callback(self, parsed) -> None:
        """Handle Meta OAuth callback with token or code in query params.

        This handles two cases:
        1. Token passed as query param (rare, but possible)
        2. Authorization code passed as query param (code flow)
        """
        params = parse_qs(parsed.query)

        if "access_token" in params:
            # Token directly in query params
            token_data = {
                "access_token": params["access_token"][0],
                "expires_in": int(params.get("expires_in", [3600])[0]),
                "created_at": int(time.time()),
            }
            _tokens["meta"] = token_data
            save_token("meta", token_data)
            print("[OAuth] Meta token received via query params", file=sys.stderr)
            self._send_success_page(
                "Meta Ads Authentication Successful",
                "Your Meta Ads account has been connected. You can close this window.",
            )
        elif "code" in params:
            # Authorization code flow - store code for exchange
            _tokens["meta_code"] = params["code"][0]
            print("[OAuth] Meta authorization code received", file=sys.stderr)
            self._send_success_page(
                "Meta Ads Authentication Successful",
                "Your Meta Ads account has been connected. You can close this window.",
            )
        elif "error" in params:
            error = params.get("error", ["Unknown error"])[0]
            error_desc = params.get("error_description", [""])[0]
            self._send_error_page(
                "Meta Ads Authentication Failed",
                f"Error: {error}. {error_desc}",
            )
        else:
            self._send_error_page(
                "Meta Ads Authentication Failed",
                "No token or authorization code received.",
            )

    def _serve_meta_fragment_handler(self) -> None:
        """Serve HTML page that extracts token from URL fragment.

        Meta's implicit OAuth flow returns the access token in the URL fragment,
        which is not sent to the server. This page uses JavaScript to extract
        the token and POST it to /callback/meta.
        """
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meta Ads Authentication</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            text-align: center;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            backdrop-filter: blur(10px);
        }
        .spinner {
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 1rem auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .success { color: #4ade80; }
        .error { color: #f87171; }
    </style>
</head>
<body>
    <div class="container">
        <h1 id="title">Processing Authentication...</h1>
        <div class="spinner" id="spinner"></div>
        <p id="message">Please wait while we complete the authentication.</p>
    </div>
    <script>
        async function handleAuth() {
            const hash = window.location.hash.substring(1);
            const params = new URLSearchParams(hash);
            const token = params.get('access_token');
            const expiresIn = params.get('expires_in');

            const title = document.getElementById('title');
            const spinner = document.getElementById('spinner');
            const message = document.getElementById('message');

            if (token) {
                try {
                    const response = await fetch('/callback/meta', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            access_token: token,
                            expires_in: parseInt(expiresIn) || 3600
                        })
                    });

                    const result = await response.json();

                    if (result.status === 'success') {
                        title.className = 'success';
                        title.textContent = 'Meta Ads Authentication Successful!';
                        spinner.style.display = 'none';
                        message.textContent = 'Your Meta Ads account has been connected. You can close this window.';
                    } else {
                        throw new Error(result.message || 'Unknown error');
                    }
                } catch (error) {
                    title.className = 'error';
                    title.textContent = 'Authentication Failed';
                    spinner.style.display = 'none';
                    message.textContent = 'Error: ' + error.message;
                }
            } else {
                const error = params.get('error') || 'No access token received';
                const errorDesc = params.get('error_description') || '';
                title.className = 'error';
                title.textContent = 'Authentication Failed';
                spinner.style.display = 'none';
                message.textContent = error + (errorDesc ? ': ' + errorDesc : '');
            }
        }

        handleAuth();
    </script>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(html.encode("utf-8")))
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _send_success_page(self, title: str, message: str) -> None:
        """Send a success HTML page."""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
            color: white;
        }}
        .container {{
            text-align: center;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            backdrop-filter: blur(10px);
        }}
        .checkmark {{
            font-size: 4rem;
            margin-bottom: 1rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="checkmark">&#x2714;</div>
        <h1>{title}</h1>
        <p>{message}</p>
    </div>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(html.encode("utf-8")))
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _send_error_page(self, title: str, message: str) -> None:
        """Send an error HTML page."""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
        }}
        .container {{
            text-align: center;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            backdrop-filter: blur(10px);
        }}
        .x-mark {{
            font-size: 4rem;
            margin-bottom: 1rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="x-mark">&#x2718;</div>
        <h1>{title}</h1>
        <p>{message}</p>
    </div>
</body>
</html>"""
        self.send_response(400)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(html.encode("utf-8")))
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _send_json(self, data: dict) -> None:
        """Send a JSON response."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)


def start_oauth_server(port: int = 8888) -> int:
    """Start the OAuth callback server if not already running.

    The server runs in a daemon thread and will automatically stop when
    the main program exits.

    Args:
        port: Starting port to try (will increment if unavailable).

    Returns:
        The actual port the server is running on.

    Raises:
        RuntimeError: If no available port could be found.
    """
    global _server, _server_thread, _port

    if _server is not None:
        return _port

    # Try to find an available port
    for p in range(port, port + 100):
        try:
            _server = HTTPServer(("localhost", p), OAuthCallbackHandler)
            _port = p
            break
        except OSError:
            continue
    else:
        raise RuntimeError(
            f"Could not find available port for OAuth server in range {port}-{port + 99}"
        )

    # Start server in background thread
    _server_thread = threading.Thread(
        target=_server.serve_forever, daemon=True, name="OAuthCallbackServer"
    )
    _server_thread.start()

    print(f"[OAuth] Callback server started on port {_port}", file=sys.stderr)
    return _port


def stop_oauth_server() -> None:
    """Stop the OAuth callback server if running."""
    global _server, _server_thread

    if _server is not None:
        _server.shutdown()
        _server = None
        _server_thread = None
        print("[OAuth] Callback server stopped", file=sys.stderr)


def get_google_auth_code() -> Optional[str]:
    """Get the Google authorization code if available.

    Returns:
        The authorization code string, or None if not yet received.
    """
    return _tokens.get("google_code")


def get_meta_token() -> Optional[dict]:
    """Get the Meta access token data if available.

    Returns:
        Dictionary with 'access_token', 'expires_in', 'created_at' keys,
        or None if not yet received.
    """
    return _tokens.get("meta")


def clear_tokens() -> None:
    """Clear all in-memory tokens."""
    _tokens.clear()


def open_auth_url(url: str) -> bool:
    """Open authentication URL in the default browser.

    Args:
        url: The OAuth authorization URL to open.

    Returns:
        True if browser was opened successfully, False otherwise.
    """
    try:
        return webbrowser.open(url)
    except Exception as e:
        print(f"[OAuth] Failed to open browser: {e}", file=sys.stderr)
        return False


def save_token(platform: str, token_data: dict) -> None:
    """Save token data to persistent cache.

    Args:
        platform: Platform identifier ('google' or 'meta').
        token_data: Dictionary containing token information.
    """
    TOKEN_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = TOKEN_CACHE_DIR / f"{platform}_token.json"

    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(token_data, f, indent=2)
        # Set restrictive permissions (readable only by owner)
        cache_file.chmod(0o600)
    except Exception as e:
        print(f"[OAuth] Failed to save {platform} token: {e}", file=sys.stderr)


def load_token(platform: str) -> Optional[dict]:
    """Load token data from persistent cache.

    Args:
        platform: Platform identifier ('google' or 'meta').

    Returns:
        Dictionary containing token information, or None if not found or invalid.
    """
    cache_file = TOKEN_CACHE_DIR / f"{platform}_token.json"

    if not cache_file.exists():
        return None

    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[OAuth] Failed to load {platform} token: {e}", file=sys.stderr)
        return None


def delete_token(platform: str) -> bool:
    """Delete a cached token file.

    Args:
        platform: Platform identifier ('google' or 'meta').

    Returns:
        True if token was deleted, False if it didn't exist.
    """
    cache_file = TOKEN_CACHE_DIR / f"{platform}_token.json"

    if cache_file.exists():
        try:
            cache_file.unlink()
            return True
        except Exception as e:
            print(f"[OAuth] Failed to delete {platform} token: {e}", file=sys.stderr)
    return False
