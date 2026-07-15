import time
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from redis import Redis

PORT = 9090

# Connect to the Redis container using its service name from the docker-compose network
cache = None
for i in range(10):
    try:
        cache = Redis(host='my-db-backend', port=6379, socket_connect_timeout=2)
        cache.ping()
        break
    except Exception:
        time.sleep(1)

class PortfolioHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Increment the hit counter in Redis database
        hits = 0
        if cache:
            try:
                hits = cache.incr('hits')
            except Exception:
                hits = "Database Connection Offline"

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        portfolio_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mizan-Olinko | Cloud & DevOps Stack</title>
            <style>
                :root {{
                    --bg-dark: #0f172a;
                    --card-bg: #1e293b;
                    --text-main: #f8fafc;
                    --text-muted: #94a3b8;
                    --accent-blue: #38bdf8;
                    --accent-green: #4ade80;
                }}
                body {{
                    font-family: 'Segoe UI', sans-serif;
                    background-color: var(--bg-dark);
                    color: var(--text-main);
                    margin: 0;
                    padding: 40px 20px;
                    line-height: 1.6;
                }}
                .container {{ max-width: 900px; margin: 0 auto; }}
                header {{ text-align: center; margin-bottom: 40px; border-bottom: 2px solid var(--card-bg); padding-bottom: 20px; }}
                h1 {{ color: var(--accent-blue); margin-bottom: 5px; font-size: 2.3rem; }}
                .status-badge {{
                    display: inline-block;
                    background-color: rgba(74, 222, 128, 0.1);
                    color: var(--accent-green);
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 0.95rem;
                    font-weight: bold;
                    border: 1px solid var(--accent-green);
                    margin-top: 10px;
                }}
                .counter-box {{
                    background: rgba(56, 189, 248, 0.1);
                    border: 1px dashed var(--accent-blue);
                    padding: 15px;
                    text-align: center;
                    border-radius: 8px;
                    margin-bottom: 30px;
                    font-size: 1.2rem;
                }}
                .section {{ background-color: var(--card-bg); padding: 25px; margin-bottom: 25px; border-radius: 12px; }}
                h2 {{ color: var(--accent-blue); margin-top: 0; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px; }}
                .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
                .item-title {{ font-weight: bold; }}
                .item-meta {{ color: var(--text-muted); font-size: 0.9rem; }}
                .tech-stack span {{
                    display: inline-block;
                    background: rgba(56, 189, 248, 0.05);
                    color: var(--accent-blue);
                    padding: 4px 10px;
                    border-radius: 6px;
                    font-size: 0.85rem;
                    margin: 4px;
                    border: 1px solid rgba(56, 189, 248, 0.15);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>Mizan-Olinko</h1>
                    <p style="color:var(--text-muted);margin:0;">Cloud Systems & DevOps Engineer</p>
                    <div class="status-badge">🚀 Microservices Stack Active via Docker Compose</div>
                </header>

                <div class="counter-box">
                    📊 Total Portfolio Page Views (Tracked in Redis): <strong>{hits}</strong>
                </div>

                <div class="grid">
                    <div class="section">
                        <h2>Academic Foundation</h2>
                        <div class="item-title">MSc in Computer Science (Network Engineering)</div>
                        <div class="item-meta">Advanced Network Architecture & Routing Matrix</div>
                        <br>
                        <div class="item-title">BSc in Computer Science</div>
                        <div class="item-meta">Systems Programming & Computational Logic</div>
                    </div>

                    <div class="section">
                        <h2>Certifications & Toolkit</h2>
                        <div class="item-title">Cisco Certified Network Associate (CCNA)</div>
                        <div class="item-meta">Routing, Switching & Infrastructure Security</div>
                        <br>
                        <div class="tech-stack">
                            <span>Terraform IaC</span>
                            <span>Docker Compose</span>
                            <span>Redis DB</span>
                            <span>AWS Cloud</span>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(b"<h1>Mizan-Olinko's CI/CD Pipeline is Fully Alive!</h1>")

print(f"Serving portfolio microservice securely on port {PORT}...")
with TCPServer(("", PORT), PortfolioHandler) as httpd:
    httpd.serve_forever()