# Kom i Gang med WordPress MCP Server

## 🚀 Hurtig Start (5 minutter)

### Trin 1: Opret WordPress Application Password

1. Log ind på https://inboundcph.dk/wp-admin
2. Gå til din brugerprofil (øverste højre hjørne → "Rediger profil")
3. Scroll ned til "Application Passwords"
4. Indtast navn: "MCP Server"
5. Klik "Add New Application Password"
6. **Kopier passwordet** (vises kun én gang!)

### Trin 2: Konfigurer Serveren

```bash
# Naviger til projektet
cd wordpress-content-mcp

# Kopier example fil
cp .env.example .env

# Rediger .env fil
nano .env
```

Udfyld følgende:
```env
WORDPRESS_URL=https://inboundcph.dk
WORDPRESS_USERNAME=dit_brugernavn
WORDPRESS_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
OPENAI_API_KEY=sk-...
```

Gem filen (Ctrl+X, Y, Enter)

### Trin 3: Test Forbindelsen

```bash
python3 test_mcp_tools.py
```

Forventet output: ✓ Connection successful!

### Trin 4: Start Serveren

```bash
python3 mcp_server.py
```

Du skulle se:
```
INFO - WordPress MCP Server initialized for https://inboundcph.dk
INFO - Available tools: 12
```

### Trin 5: Tilføj til Manus

1. Åbn Manus indstillinger
2. Gå til "MCP Servers"
3. Klik "Add Server"
4. Udfyld:
   - **Name**: wordpress-content-management
   - **Command**: python3
   - **Arguments**: /fuld/sti/til/wordpress-content-mcp/mcp_server.py
5. Gem og genstart Manus

## ✅ Test i Manus

Prøv disse kommandoer:

```
Hent de 5 seneste blog posts fra WordPress
```

```
Generer et blog indlæg om "AI i marketing" på dansk, gem som draft
```

```
Søg efter posts om "SEO"
```

## 📚 Næste Skridt

- Læs **README.md** for komplet API dokumentation
- Se **WORKFLOWS.md** for praktiske eksempler
- Læs **DEPLOYMENT.md** for produktion deployment

## 🆘 Problemer?

### "Missing required configuration"
→ Tjek at .env filen er korrekt udfyldt

### "Authentication failed"
→ Verificer WordPress Application Password

### "OpenAI API error"
→ Tjek OpenAI API key

Se **SETUP_GUIDE.md** for detaljeret fejlfinding.

---

**Held og lykke! 🎉**
