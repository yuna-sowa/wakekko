import http.server, threading, time, os, sys
from pathlib import Path

PORT = 8765
ROOT = Path(__file__).parent.parent
OUT  = ROOT / "screenshot" / "wakekko-screenshot.png"

os.chdir(ROOT)

handler = http.server.SimpleHTTPRequestHandler
handler.log_message = lambda *a: None
httpd = http.server.HTTPServer(("localhost", PORT), handler)
t = threading.Thread(target=httpd.serve_forever)
t.daemon = True
t.start()
time.sleep(1)

try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 393, "height": 852})
        page.goto(f"http://localhost:{PORT}")
        page.wait_for_timeout(2000)
        OUT.parent.mkdir(exist_ok=True)
        page.screenshot(path=str(OUT))
        browser.close()
    print(f"saved: {OUT}")
finally:
    httpd.shutdown()
