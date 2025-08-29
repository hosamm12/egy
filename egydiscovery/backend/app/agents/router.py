from typing import Dict, Any
def smart_route(prompt: str, params: Dict[str, Any] | None = None) -> str:
    params = params or {}
    if 'agent' in params and params['agent']: return params['agent']
    low = prompt.lower()
    if any(k in low for k in ['lead','buyer','prospect']): return 'leadgen'
    if any(k in low for k in ['research','scan','find']): return 'research'
    return 'default'
def run_default(prompt: str, params: Dict[str, Any]): return {"echo": prompt, "agent": "default"}
def run_leadgen(prompt: str, params: Dict[str, Any]): return {"items":[{"name":"Example","platform":"instagram","score":0.8}], "agent":"leadgen"}
def run_research(prompt: str, params: Dict[str, Any]): return {"summary": f"Researched: {prompt}", "agent":"research"}
def run(prompt: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    agent = smart_route(prompt, params)
    if agent == 'leadgen': return run_leadgen(prompt, params)
    if agent == 'scrape': return run_scrape(prompt, params)
    if agent == 'enrich': return run_enrich(prompt, params)
    if agent == 'research': return run_research(prompt, params)
    return run_default(prompt, params)

from bs4 import BeautifulSoup
import requests, re

def run_scrape(prompt: str, params: Dict[str, Any]):
    # Expect a URL in params or in prompt
    url = params.get("url")
    if not url:
        m = re.search(r'https?://\S+', prompt)
        url = m.group(0) if m else None
    if not url:
        return {"error":"No URL detected", "agent":"scrape"}
    try:
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string if soup.title else ""
        text = " ".join((t.get_text(" ", strip=True) for t in soup.find_all(["p","li","h1","h2","h3"]) ))[:2000]
        return {"url": url, "title": title, "extract": text, "agent":"scrape"}
    except Exception as e:
        return {"error": str(e), "agent":"scrape"}

def run_enrich(prompt: str, params: Dict[str, Any]):
    # Simple enrichment scoring based on keyword matches (stub)
    payload = params.get("payload") or {}
    score = 0
    text = (payload.get("bio") or payload.get("extract") or prompt or "").lower()
    if "photography" in text or "videography" in text: score += 40
    if "hurghada" in text: score += 30
    if "booking" in text or "inquiry" in text: score += 20
    if "contact" in text or "email" in text: score += 10
    return {"score": min(score,100), "agent":"enrich"}
