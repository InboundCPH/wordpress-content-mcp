# WordPress MCP Server - Setup Guide

Denne guide hjælper dig med at konfigurere og bruge WordPress MCP-serveren.

## Trin 1: Opret WordPress Application Password

### Hvorfor Application Password?

WordPress Application Passwords er en sikker måde at give eksterne applikationer adgang til dit WordPress-site uden at bruge dit hovedpassword. Det giver dig mulighed for:

- At tilbagekalde adgang når som helst
- At have forskellige passwords til forskellige applikationer
- At holde dit hovedpassword sikkert

### Sådan opretter du et Application Password

1. **Log ind på WordPress admin**
   - Gå til `https://inboundcph.dk/wp-admin`

2. **Gå til din brugerprofil**
   - Klik på dit navn i øverste højre hjørne
   - Vælg "Rediger profil" eller gå direkte til "Brugere" → "Profil"

3. **Find Application Passwords sektionen**
   - Scroll ned til bunden af siden
   - Find sektionen "Application Passwords"

4. **Opret nyt Application Password**
   - I feltet "New Application Password Name" indtast: `MCP Server`
   - Klik på "Add New Application Password"

5. **Kopier passwordet**
   - WordPress viser nu et nyt password (f.eks. `xxxx xxxx xxxx xxxx xxxx xxxx`)
   - **VIGTIGT**: Kopier dette password med det samme - det vises kun én gang!
   - Gem det sikkert (du skal bruge det i næste trin)

## Trin 2: Konfigurer .env fil

1. **Kopier example filen**
   ```bash
   cp .env.example .env
   ```

2. **Rediger .env filen**
   ```bash
   nano .env
   # eller brug din foretrukne editor
   ```

3. **Udfyld værdierne**
   ```env
   # WordPress Configuration
   WORDPRESS_URL=https://inboundcph.dk
   WORDPRESS_USERNAME=dit_wordpress_brugernavn
   WORDPRESS_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
   
   # OpenAI Configuration
   OPENAI_API_KEY=sk-...
   
   # Optional: Default settings
   DEFAULT_POST_STATUS=draft
   DEFAULT_LANGUAGE=da
   ```

   **Vigtigt:**
   - `WORDPRESS_USERNAME` er dit WordPress brugernavn (ikke email)
   - `WORDPRESS_APP_PASSWORD` er det password du kopierede i Trin 1
   - Behold mellemrummene i Application Password
   - `OPENAI_API_KEY` skal være din OpenAI API key

4. **Gem filen**
   - I nano: Tryk `Ctrl+X`, derefter `Y`, derefter `Enter`

## Trin 3: Test konfigurationen

### Test WordPress forbindelse

Opret en test fil `test_connection.py`:

```python
#!/usr/bin/env python3
"""Test WordPress connection."""

from src.api.wordpress_client import WordPressClient
from src.config.settings import settings

print(f"Testing connection to: {settings.WORDPRESS_URL}")
print(f"Username: {settings.WORDPRESS_USERNAME}")

try:
    client = WordPressClient()
    posts = client.get_posts(per_page=1)
    print(f"✓ Connection successful!")
    print(f"✓ Found {len(posts)} post(s)")
    if posts:
        print(f"  Latest post: {posts[0]['title']['rendered']}")
except Exception as e:
    print(f"✗ Connection failed: {str(e)}")
```

Kør testen:
```bash
python3 test_connection.py
```

Forventet output:
```
Testing connection to: https://inboundcph.dk
Username: dit_brugernavn
✓ Connection successful!
✓ Found 1 post(s)
  Latest post: Whitepaper: AI-centreret SEO
```

## Trin 4: Start MCP Server

### Lokal test

```bash
python3 mcp_server.py
```

Du skulle se:
```
INFO - WordPress MCP Server initialized for https://inboundcph.dk
INFO - Starting WordPress Content Management MCP Server...
INFO - Connected to: https://inboundcph.dk
INFO - Available tools: 12
```

### Tilføj til Manus

1. **Åbn Manus indstillinger**
   - Klik på indstillinger/settings
   - Gå til "MCP Servers"

2. **Tilføj ny server**
   - Klik "Add Server"
   - **Name**: `wordpress-content-management`
   - **Command**: `python3`
   - **Arguments**: `/sti/til/wordpress-content-mcp/mcp_server.py`
   - Eller brug `uv run` hvis du bruger uv:
     - **Command**: `uv`
     - **Arguments**: `run /sti/til/wordpress-content-mcp/mcp_server.py`

3. **Gem og genstart Manus**

## Trin 5: Test i Manus

Prøv følgende kommandoer i Manus:

### Liste posts
```
Hent de 5 seneste blog posts fra WordPress
```

### Generer blog post
```
Generer et blog indlæg om "AI i digital marketing" på dansk, 
med keywords "AI, marketing, automation". Gem det som draft.
```

### Forbedre indhold
```
Forbedre indlægget med ID 123 for bedre SEO og læsbarhed
```

### Søg i posts
```
Søg efter posts om "marketing" i WordPress
```

## Fejlfinding

### Problem: "Missing required configuration"

**Løsning:**
- Tjek at `.env` filen eksisterer
- Verificer at alle nødvendige variabler er udfyldt
- Sørg for at der ikke er ekstra mellemrum omkring værdierne

### Problem: "Authentication failed"

**Løsning:**
- Verificer at WordPress Application Password er korrekt kopieret
- Tjek at brugernavnet er korrekt (ikke email)
- Sørg for at brugeren har rettigheder til at oprette/redigere posts
- Prøv at oprette et nyt Application Password

### Problem: "OpenAI API error"

**Løsning:**
- Verificer at OPENAI_API_KEY er korrekt
- Tjek at du har credits på din OpenAI konto
- Prøv at teste API key direkte via OpenAI's website

### Problem: "Connection timeout"

**Løsning:**
- Tjek din internetforbindelse
- Verificer at WordPress-sitet er tilgængeligt
- Tjek om der er firewall/proxy problemer

## Sikkerhed

### Beskyt dine credentials

1. **Gem aldrig .env i Git**
   - `.env` er allerede i `.gitignore`
   - Verificer: `git status` skulle IKKE vise `.env`

2. **Brug kun Application Passwords**
   - Brug ALDRIG dit WordPress hovedpassword
   - Tilbagekald gamle passwords når de ikke bruges

3. **Begræns brugerrettigheder**
   - Brug en WordPress-bruger med kun nødvendige rettigheder
   - Overvej at oprette en dedikeret "API User"

4. **Roter credentials regelmæssigt**
   - Skift Application Password hver 3-6 måned
   - Opdater OpenAI API key hvis kompromitteret

## Næste skridt

Nu hvor din MCP-server er sat op, kan du:

1. **Udforske alle tools**
   - Læs README.md for komplet tool dokumentation
   - Eksperimenter med forskellige parametre

2. **Integrer med AI-seo-tools**
   - Kombiner WordPress content management med SEO-analyse
   - Opret automatiserede workflows

3. **Tilpas til dine behov**
   - Tilføj custom ACF field handling
   - Udvid med flere content types (pages, custom post types)
   - Integrer med andre services

## Support

Hvis du støder på problemer:

1. Tjek denne guide igen
2. Læs README.md for detaljeret dokumentation
3. Tjek logs for fejlmeddelelser
4. Verificer alle credentials er korrekte

---

**Held og lykke med din WordPress MCP-server! 🚀**

