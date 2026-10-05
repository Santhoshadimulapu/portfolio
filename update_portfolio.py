"""Usage: python update_portfolio.py index.html
Writes index.updated.html next to the input, with content synced to the new resume."""
import re, sys, pathlib

src = pathlib.Path(sys.argv[1])
h = src.read_text(encoding="utf-8")

def rep(old, new):
    global h
    if old not in h:
        print("WARNING: not found ->", old[:60])
    h = h.replace(old, new)

# Hero + stats
rep("building production-grade systems — JWT auth, Redis concurrency, real-time WebSocket platforms.",
    "building production-grade, AI-enabled systems — Redis concurrency, real-time WebSocket platforms, ML-powered features.")
rep('8<span>.</span>08', '8<span>.</span>18')
rep('<div class="stat-num">2<span></span></div>', '<div class="stat-num">3<span></span></div>')
rep('Production Systems Shipped', 'Projects Built')
rep('160<span>+</span>', '170<span>+</span>')

# Skills
rep('<span class="tag">Socket.IO</span>',
    '<span class="tag">Socket.IO</span>\n        <span class="tag">FastAPI</span>\n        <span class="tag">SQLAlchemy</span>')
rep('<span class="tag">Tailwind CSS</span>', '<span class="tag">CSS</span>')
rep('<span class="tag">Docker</span>',
    '<span class="tag">Docker (Basic)</span>\n        <span class="tag">GitHub Actions</span>\n        <span class="tag">VS Code</span>')

# Projects: renumber, then add the new one at the top
rep('<div class="project-num">02</div>', '<div class="project-num">03</div>')
rep('<div class="project-num">01</div>', '<div class="project-num">02</div>')

new_project = '''<a class="project-item reveal" href="https://github.com/Santhoshadimulapu" target="_blank">
      <div class="project-num">01</div>
      <div class="project-body">
        <h3 class="project-name">Climate-Resilient Agriculture Platform</h3>
        <p class="project-desc">An AI-powered advisory platform that turns soil photos, environmental data, and farmer queries into personalized farming decisions — in English, Telugu, and Hindi. In progress since Aug 2026.</p>
        <div class="project-highlights">
          <span class="highlight-item">AI soil scanner for soil health classification from photos</span>
          <span class="highlight-item">Crop selection, fertilizer recommendations, and yield predictions</span>
          <span class="highlight-item">Context-aware chatbot with real-time weather integration</span>
          <span class="highlight-item">Multilingual support to remove language barriers for rural farmers</span>
        </div>
        <div class="project-tech">
          <span class="tech-pill">React</span>
          <span class="tech-pill">FastAPI</span>
          <span class="tech-pill">SQLAlchemy</span>
          <span class="tech-pill">Python</span>
        </div>
      </div>
      <div class="project-arrow">↗</div>
    </a>

    '''
rep('<a class="project-item reveal" href="https://hospital-mini-project.vercel.app/"',
    new_project + '<a class="project-item reveal" href="https://hospital-mini-project.vercel.app/"')

rep('<span class="highlight-item">JWT + RBAC for Patient, Doctor, and Admin workflows</span>',
    '<span class="highlight-item">Real-time queue wait-time estimates for patients</span>\n          '
    '<span class="highlight-item">JWT + RBAC with role-based dashboards for Patient, Doctor, and Admin</span>')

# StudyCollab: 100+ -> 1000+
rep('100+ concurrent WebSocket', '1000+ concurrent WebSocket')

# Education: 8.18 CGPA, add SSC card, 3 columns
rep('<div class="edu-grade">8.08</div>', '<div class="edu-grade">8.18</div>')
rep('.edu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }',
    '.edu-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }')
ssc = '''
    <div class="edu-card">
      <div class="edu-year">2020 → 2021</div>
      <div class="edu-degree">SSC (Class X)</div>
      <div class="edu-institution">Sri Chaitanya School</div>
      <div class="edu-grade">100%</div>
      <div class="edu-grade-label">Percentage</div>
    </div>'''
h = re.sub(r'(89\.5%</div>\s*<div class="edu-grade-label">Percentage</div>\s*</div>)',
           lambda m: m.group(1) + ssc, h, count=1)

# Certifications (replaced) + Club activities (new)
def cert(name, meta, badge):
    return f'''    <div class="cert-item">
      <div>
        <div class="cert-name">{name}</div>
        <div class="cert-issuer">{meta}</div>
      </div>
      <span class="cert-badge">{badge}</span>
    </div>
'''

certs = (
    cert("Agentblazer Champion 2025", "Salesforce Trailhead · 19+ Agentforce badges completed", "Salesforce")
  + cert("AWS Academy Graduate — Cloud Foundations", "AWS Academy · Sep 2026", "AWS")
  + cert("IBM AI Fundamentals", "IBM SkillsBuild · 2026", "IBM")
  + cert("Google AI/ML Virtual Internship", "AICTE · Practical ML &amp; AI through structured industry projects", "AICTE")
  + cert("Introduction to Machine Learning", "NPTEL · Elite grade — supervised &amp; unsupervised learning, model evaluation", "Elite")
)
club = (
    cert("Content Team Member — Coding Cubs", "Anurag University · Blog posts, problem editorials &amp; workshop guides for 200+ members", "200+ readers")
  + cert("Workshops &amp; Contests", "Organized hands-on coding workshops and competitive programming events", "Organizer")
)

block = f'''<div class="certs-list reveal">
{certs}  </div>
</section>

<!-- Club Activities -->
<section class="certs">
  <div class="section-label reveal">Community</div>
  <div class="section-title reveal">Club activity.</div>
  <div class="certs-list reveal">
{club}  </div>
</section>'''

h, n = re.subn(r'<div class="certs-list reveal">.*?</section>', lambda m: block, h, count=1, flags=re.S)
if n == 0:
    print("WARNING: certifications block not found")

out = src.with_name("index.updated.html")
out.write_text(h, encoding="utf-8")
print("Wrote", out)
