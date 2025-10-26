# Railway Deployment Guide

## 🚀 Quick Deploy til Railway

Repository er nu klar til deployment på Railway: https://github.com/InboundCPH/wordpress-content-mcp

### Trin 1: Opret Railway Projekt

1. **Log ind på Railway**
   - Gå til https://railway.app
   - Log ind med din GitHub konto

2. **Opret nyt projekt**
   - Klik "New Project"
   - Vælg "Deploy from GitHub repo"
   - Vælg `InboundCPH/wordpress-content-mcp`
   - Railway starter automatisk deployment

### Trin 2: Konfigurer Environment Variables

Efter projektet er oprettet, tilføj følgende miljøvariabler:

1. **Gå til projekt Settings → Variables**

2. **Tilføj disse variabler:**

```
WORDPRESS_URL=https://inboundcph.dk
WORDPRESS_USERNAME=dit_wordpress_brugernavn
WORDPRESS_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
OPENAI_API_KEY=sk-...
DEFAULT_POST_STATUS=draft
DEFAULT_LANGUAGE=da
```

3. **Gem variablerne**
   - Railway vil automatisk redeploy med de nye variabler

### Trin 3: Verificer Deployment

1. **Tjek deployment status**
   - Gå til "Deployments" tab
   - Vent til status er "Success" (grøn)

2. **Tjek logs**
   - Klik på den seneste deployment
   - Se logs for at verificere at serveren startede korrekt
   - Du skulle se: "WordPress MCP Server initialized for https://inboundcph.dk"

3. **Test health endpoint** (hvis HTTP endpoint er aktiveret)
   - Railway giver dig en URL (f.eks. `your-app.railway.app`)
   - Besøg URL'en for at tjekke status

### Trin 4: Brug MCP Serveren

#### Option A: Lokal Manus med Railway Backend

Hvis du vil bruge Railway som backend, men køre Manus lokalt:

1. **Få Railway service URL**
   - Gå til projekt Settings → Networking
   - Kopier den offentlige URL

2. **Konfigurer Manus**
   - Tilføj MCP server med Railway URL
   - Brug HTTP/SSE transport

#### Option B: Lokal MCP Server (Anbefalet)

For bedre performance og lavere latency:

1. **Klon repository lokalt**
   ```bash
   git clone https://github.com/InboundCPH/wordpress-content-mcp.git
   cd wordpress-content-mcp
   ```

2. **Konfigurer .env**
   ```bash
   cp .env.example .env
   nano .env
   # Udfyld credentials
   ```

3. **Kør lokalt**
   ```bash
   python3 mcp_server.py
   ```

4. **Tilføj til Manus**
   - Tilføj som lokal MCP server
   - Peg på `mcp_server.py`

### Auto-Deploy ved Git Push

Railway er nu konfigureret til at auto-deploy ved hver push til main branch:

```bash
# Lav ændringer
git add .
git commit -m "Update: beskrivelse af ændringer"
git push origin main

# Railway deployer automatisk
```

### Monitoring og Logs

**Se logs:**
- Gå til Railway dashboard
- Klik på dit projekt
- Gå til "Deployments" tab
- Klik på en deployment for at se logs

**Metrics:**
- Railway viser automatisk CPU, memory og network metrics
- Gå til "Metrics" tab for at se performance

### Rollback ved Fejl

Hvis en deployment fejler:

1. **Gå til Deployments tab**
2. **Find den sidste working deployment**
3. **Klik på "..." menu**
4. **Vælg "Redeploy"**

### Fejlfinding

#### "Build failed"

**Problem:** Dependencies kan ikke installeres

**Løsning:**
- Tjek at `requirements.txt` er korrekt
- Se build logs for specifikke fejl
- Verificer at Python version er kompatibel

#### "Application crashed"

**Problem:** Serveren crasher ved start

**Løsning:**
- Tjek at alle environment variables er sat
- Se runtime logs for fejlmeddelelser
- Verificer at WordPress credentials er korrekte

#### "Out of memory"

**Problem:** Serveren bruger for meget memory

**Løsning:**
- Upgrade Railway plan for mere memory
- Optimer koden for lavere memory forbrug
- Tjek for memory leaks i logs

### Railway Pricing

**Hobby Plan (Gratis):**
- $5 gratis credits per måned
- Perfekt til udvikling og test
- Automatisk sleep efter inaktivitet

**Pro Plan ($20/måned):**
- $20 credits per måned
- Ingen sleep
- Bedre performance
- Prioriteret support

### Sikkerhed på Railway

**Best Practices:**

1. **Environment Variables**
   - Brug ALDRIG hardcoded credentials
   - Alle secrets i Railway environment variables

2. **Private Repository** (valgfrit)
   - Overvej at gøre repository private
   - Gå til GitHub repo settings → Danger Zone → Change visibility

3. **Access Control**
   - Begræns adgang til Railway projektet
   - Inviter kun nødvendige team members

4. **Secrets Rotation**
   - Skift WordPress Application Password regelmæssigt
   - Opdater OpenAI API key ved behov

### Support

**Railway Support:**
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app
- Status: https://status.railway.app

**Projekt Support:**
- GitHub Issues: https://github.com/InboundCPH/wordpress-content-mcp/issues
- Documentation: Se README.md

---

## 📋 Checklist for Railway Deployment

- [ ] Railway konto oprettet og linket til GitHub
- [ ] Repository deployed til Railway
- [ ] Environment variables konfigureret
- [ ] Deployment success (grøn status)
- [ ] Logs verificeret - server startede korrekt
- [ ] MCP server tilføjet til Manus (lokal eller Railway)
- [ ] Test kommandoer virker i Manus
- [ ] Auto-deploy verificeret (push til main)

---

**Din WordPress MCP server er nu live på Railway! 🎉**

