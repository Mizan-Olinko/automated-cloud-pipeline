import time
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from redis import Redis

# Bind to port 8080 for AWS Docker deployment mapping
PORT = 8080

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
                hits = "Database Connection Offline (Local Mode)"

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        portfolio_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Md Mizanur Rahman | Cloud & DevOps Engineer Portfolio</title>
            <style>
                :root {{
                    --bg-dark: #0f172a;
                    --card-bg: #1e293b;
                    --text-main: #f8fafc;
                    --text-muted: #94a3b8;
                    --accent-blue: #38bdf8;
                    --accent-green: #4ade80;
                    --border-color: rgba(255, 255, 255, 0.08);
                }}
                body {{
                    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
                    background-color: var(--bg-dark);
                    color: var(--text-main);
                    margin: 0;
                    padding: 40px 20px;
                    line-height: 1.6;
                }}
                .container {{ 
                    max-width: 950px; 
                    margin: 0 auto; 
                }}
                header {{ 
                    text-align: center; 
                    margin-bottom: 40px; 
                    border-bottom: 1px solid var(--border-color); 
                    padding-bottom: 30px; 
                }}
                h1 {{ 
                    color: var(--text-main); 
                    margin-bottom: 5px; 
                    font-size: 2.6rem; 
                    font-weight: 700;
                    letter-spacing: -0.025em;
                }}
                .subtitle {{
                    color: var(--accent-blue);
                    font-size: 1.25rem;
                    margin-top: 0;
                    font-weight: 500;
                    letter-spacing: 0.05em;
                    text-transform: uppercase;
                }}
                .contact-info {{
                    display: flex;
                    justify-content: center;
                    flex-wrap: wrap;
                    gap: 15px 25px;
                    margin-top: 15px;
                    font-size: 0.95rem;
                    color: var(--text-muted);
                }}
                .contact-info a {{
                    color: var(--accent-blue);
                    text-decoration: none;
                }}
                .contact-info a:hover {{
                    text-decoration: underline;
                }}
                .status-badge {{
                    display: inline-block;
                    background-color: rgba(74, 222, 128, 0.1);
                    color: var(--accent-green);
                    padding: 6px 16px;
                    border-radius: 20px;
                    font-size: 0.85rem;
                    font-weight: 600;
                    border: 1px solid rgba(74, 222, 128, 0.2);
                    margin-top: 15px;
                }}
                .counter-box {{
                    background: rgba(56, 189, 248, 0.06);
                    border: 1px solid rgba(56, 189, 248, 0.2);
                    padding: 15px;
                    text-align: center;
                    border-radius: 8px;
                    margin-bottom: 35px;
                    font-size: 1.1rem;
                    color: var(--text-main);
                }}
                .counter-box strong {{
                    color: var(--accent-blue);
                }}
                .section {{ 
                    background-color: var(--card-bg); 
                    padding: 30px; 
                    margin-bottom: 25px; 
                    border-radius: 12px; 
                    border: 1px solid var(--border-color);
                }}
                h2 {{ 
                    color: var(--accent-blue); 
                    margin-top: 0; 
                    border-bottom: 1px solid var(--border-color); 
                    padding-bottom: 10px; 
                    font-size: 1.5rem;
                    font-weight: 600;
                }}
                .grid {{ 
                    display: grid; 
                    grid-template-columns: 1fr 1fr; 
                    gap: 25px; 
                }}
                @media (max-width: 768px) {{
                    .grid {{ grid-template-columns: 1fr; }}
                }}
                .item {{
                    margin-bottom: 20px;
                }}
                .item:last-child {{
                    margin-bottom: 0;
                }}
                .item-title {{ 
                    font-size: 1.15rem;
                    font-weight: 600; 
                    color: var(--text-main);
                }}
                .item-sub {{
                    color: var(--accent-blue);
                    font-size: 0.95rem;
                    font-weight: 500;
                    margin: 2px 0 6px 0;
                }}
                .item-meta {{ 
                    color: var(--text-muted); 
                    font-size: 0.9rem; 
                    margin-bottom: 8px;
                }}
                .bullets {{
                    margin: 8px 0 0 0;
                    padding-left: 20px;
                    color: var(--text-muted);
                    font-size: 0.9rem;
                }}
                .bullets li {{
                    margin-bottom: 6px;
                }}
                .tech-stack {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin-top: 15px;
                }}
                .tech-stack span {{
                    background: rgba(56, 189, 248, 0.08);
                    color: var(--accent-blue);
                    padding: 4px 12px;
                    border-radius: 6px;
                    font-size: 0.8rem;
                    font-weight: 600;
                    border: 1px solid rgba(56, 189, 248, 0.15);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>Md Mizanur Rahman</h1>
                    <div class="subtitle">Cloud Systems & DevOps Engineer</div>
                    
                    <div class="contact-info">
                        <span>📍 London, UK (SE3)</span>
                        <span>✉️ <a href="mailto:mizanm65@gmail.com">mizanm65@gmail.com</a></span>
                        <span>📞 <a href="tel:07485181198">07485181198</a></span>
                        <span>💻 <a href="https://github.com/Mizan-Olinko" target="_blank">github.com/Mizan-Olinko</a></span>
                    </div>

                    <div class="status-badge">🚀 Active Production Deployment via GitHub Actions</div>
                </header>

                <div class="counter-box">
                    📊 Live Visitor Metric (Redis Backend Connection State): <strong>{hits}</strong>
                </div>

                <div class="section">
                    <h2>Professional Profile</h2>
                    <p style="margin: 0; color: var(--text-muted); font-size: 0.98rem;">
                        Results-driven Infrastructure and DevOps Engineer with a Master of Science in Computer Science specialized in Network Engineering. Hands-on experience designing and implementing highly available cloud architectures, optimizing continuous integration/continuous deployment (CI/CD) workflows, and automating complex infrastructure. Adept at bridging networking fundamentals with cutting-edge containerization and orchestration tooling to accelerate product delivery pipelines.
                    </p>
                </div>

                <div class="grid">
                    <div class="section">
                        <h2>Education & Certifications</h2>
                        
                        <div class="item">
                            <div class="item-title">MSc in Computer Science (Network Engineering)</div>
                            <div class="item-sub">University of Greenwich, London</div>
                            <div class="item-meta">Focus: Advanced Network Architectures, Routing Matrices, & Security</div>
                        </div>

                        <div class="item" style="border-top: 1px solid var(--border-color); padding-top: 15px;">
                            <div class="item-title">BSc in Computer Science</div>
                            <div class="item-sub">Computer Science & Engineering</div>
                            <div class="item-meta">Focus: Systems Programming, Computational Logic, & Database Design</div>
                        </div>

                        <div class="item" style="border-top: 1px solid var(--border-color); padding-top: 15px;">
                            <div class="item-title">Cisco Certified Network Associate (CCNA)</div>
                            <div class="item-sub">Cisco Systems</div>
                            <div class="item-meta">Credential ID: Routing, Switching, & Infrastructure Protection</div>
                        </div>
                    </div>

                    <div class="section">
                        <h2>Technical Toolkit</h2>
                        
                        <div class="item">
                            <div class="item-title">Infrastructure & Cloud Automation</div>
                            <div class="tech-stack">
                                <span>Terraform (IaC)</span>
                                <span>AWS Cloud</span>
                                <span>Docker</span>
                                <span>Docker Compose</span>
                                <span>Bash / Linux</span>
                            </div>
                        </div>

                        <div class="item" style="border-top: 1px solid var(--border-color); padding-top: 15px;">
                            <div class="item-title">CI/CD & Development</div>
                            <div class="tech-stack">
                                <span>GitHub Actions</span>
                                <span>Python</span>
                                <span>Git & GitHub Workflows</span>
                                <span>Dart & Flutter (Mobile)</span>
                                <span>Redis (NoSQL)</span>
                            </div>
                        </div>

                        <div class="item" style="border-top: 1px solid var(--border-color); padding-top: 15px;">
                            <div class="item-title">Networking Core</div>
                            <div class="tech-stack">
                                <span>TCP/IP Protocols</span>
                                <span>Subnetting & Routing</span>
                                <span>Firewall Policies</span>
                                <span>VPN & VPC Architecture</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>Featured DevOps Achievements</h2>
                    
                    <div class="item" style="margin-bottom: 25px;">
                        <div class="item-title">🤖 Multi-Stage Automated Git-to-EC2 CI/CD Pipeline</div>
                        <div class="item-sub">GitHub Actions, Docker, AWS EC2, Linux Systemd</div>
                        <ul class="bullets">
                            <li>Engineered a fully automated continuous integration and delivery pipeline triggered seamlessly upon code commits.</li>
                            <li>Automated multi-stage Docker builds to compile application images, tag them dynamically, and securely publish to Docker Hub.</li>
                            <li>Configured remote automation runners to target AWS London EC2 instances via secure alternative ports (Port 2222), execute system cleanups, pull production-ready container images, and bind host interfaces securely.</li>
                            <li>Designed systemd microservice configuration rules to cleanly release OS ports and allow containerized servers to safely claim resource interfaces on the host network.</li>
                        </ul>
                    </div>

                    <div class="item" style="border-top: 1px solid var(--border-color); padding-top: 20px;">
                        <div class="item-title">⚙️ Infrastructure as Code (IaC) AWS Environment Deployment</div>
                        <div class="item-sub">Terraform, AWS, Secure VPC Networking</div>
                        <ul class="bullets">
                            <li>Created declarative Terraform configurations to construct robust virtual topologies, including custom VPCs, secure subnets, and internet gateways.</li>
                            <li>Formulated dynamic Security Group network ingress and egress firewall rule sets, minimizing exposure risk to host systems while maintaining high application availability.</li>
                        </ul>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        # Write the clean, updated portfolio_html to the web output stream
        self.wfile.write(portfolio_html.encode('utf-8'))

print(f"Serving recruiter-ready portfolio on port {PORT}...")
with TCPServer(("", PORT), PortfolioHandler) as httpd:
    httpd.serve_forever()