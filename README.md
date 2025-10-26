# WordPress Content Management MCP Server

En intelligent MCP-server til styring og optimering af WordPress-indhold med AI-drevne funktioner.

## Funktioner

### 📝 Post Management
- Liste, hent, opret, opdater og slet WordPress-indlæg
- Fuld support for ACF (Advanced Custom Fields)
- Håndtering af kategorier, tags og featured images
- Søgning i indlæg

### 🤖 AI Content Generation
- Generer komplette blog posts med AI
- Forbedre eksisterende indhold (SEO, læsbarhed, struktur)
- SEO-optimering af titler og meta descriptions
- Support for flere sprog (dansk, engelsk, svensk, etc.)

### 🔧 Utility Functions
- Hent kategorier og tags
- Søg i posts
- Validering og fejlhåndtering

## Installation

### 1. Installer dependencies

```bash
pip install -r requirements.txt
```

### 2. Konfigurer miljøvariabler

Opret en `.env` fil i projektets rodmappe:

```bash
cp .env.example .env
```

Rediger `.env` filen med dine credentials:

```env
WORDPRESS_URL=https://inboundcph.dk
WORDPRESS_USERNAME=dit_brugernavn
WORDPRESS_APP_PASSWORD=dit_app_password
OPENAI_API_KEY=din_openai_api_key
```

### 3. Opret WordPress Application Password

1. Log ind på WordPress admin
2. Gå til **Brugere** → **Profil**
3. Scroll ned til **Application Passwords**
4. Indtast et navn (f.eks. "MCP Server")
5. Klik **Add New Application Password**
6. Kopier det genererede password til `.env` filen

## Brug

### Start MCP Server

```bash
python mcp_server.py
```

### Brug med Manus AI

1. Tilføj serveren til Manus:
   - Åbn Manus indstillinger
   - Gå til MCP Servers
   - Tilføj ny server med stien til `mcp_server.py`

2. Brug serveren i Manus:
   ```
   "Generer et blog indlæg om AI i marketing"
   "Hent de 10 seneste blog posts"
   "Forbedre indlægget med ID 123 for bedre læsbarhed"
   ```

## Tilgængelige MCP Tools

### Post Management

#### `list_posts`
Liste WordPress-indlæg med filtrering.

**Parameters:**
- `per_page` (int) - Antal indlæg per side (default: 10)
- `page` (int) - Side nummer (default: 1)
- `status` (string) - Post status (default: "publish")
- `search` (string) - Søgetekst
- `categories` (string) - Kommaseparerede kategori IDs

**Eksempel:**
```python
list_posts(per_page=5, status="draft")
```

#### `get_post`
Hent specifikt indlæg med alle detaljer inkl. ACF felter.

**Parameters:**
- `post_id` (int) - Post ID

**Eksempel:**
```python
get_post(post_id=123)
```

#### `create_post`
Opret nyt WordPress-indlæg.

**Parameters:**
- `title` (string) - Post titel
- `content` (string) - Post indhold (HTML)
- `status` (string) - Post status (default: "draft")
- `excerpt` (string) - Post uddrag
- `categories` (string) - Kommaseparerede kategori IDs
- `tags` (string) - Kommaseparerede tag IDs
- `acf_fields` (string) - JSON string af ACF felter

**Eksempel:**
```python
create_post(
    title="Min nye blog post",
    content="<p>Dette er indholdet...</p>",
    status="draft",
    categories="1,5"
)
```

#### `update_post`
Opdater eksisterende indlæg.

**Parameters:**
- `post_id` (int) - Post ID
- `title` (string) - Ny titel
- `content` (string) - Nyt indhold
- `status` (string) - Ny status
- (+ alle andre felter fra create_post)

**Eksempel:**
```python
update_post(
    post_id=123,
    title="Opdateret titel",
    status="publish"
)
```

#### `delete_post`
Slet indlæg (flytter til papirkurv som standard).

**Parameters:**
- `post_id` (int) - Post ID
- `force` (bool) - Permanent sletning (default: false)

**Eksempel:**
```python
delete_post(post_id=123, force=False)
```

### AI Content Generation

#### `generate_blog_post`
Generer komplet blog post med AI.

**Parameters:**
- `topic` (string) - Emne/topic
- `keywords` (string) - Kommaseparerede SEO keywords
- `tone` (string) - Tone (professional, casual, friendly) (default: "professional")
- `length` (string) - Længde (short, medium, long) (default: "medium")
- `language` (string) - Sprog (da, en, sv) (default: "da")
- `save_as_draft` (bool) - Gem som draft (default: true)

**Eksempel:**
```python
generate_blog_post(
    topic="AI i digital marketing",
    keywords="AI, marketing, automation",
    tone="professional",
    length="medium",
    language="da",
    save_as_draft=True
)
```

#### `improve_post_content`
Forbedre eksisterende indhold med AI.

**Parameters:**
- `post_id` (int) - Post ID
- `improvements` (string) - Kommaseparerede forbedringer (seo, readability, structure, grammar)
- `save_changes` (bool) - Gem ændringer (default: false)

**Eksempel:**
```python
improve_post_content(
    post_id=123,
    improvements="seo,readability",
    save_changes=False
)
```

#### `optimize_post_seo`
SEO-optimer post (titel, meta description).

**Parameters:**
- `post_id` (int) - Post ID
- `target_keywords` (string) - Kommaseparerede target keywords
- `save_changes` (bool) - Gem ændringer (default: false)

**Eksempel:**
```python
optimize_post_seo(
    post_id=123,
    target_keywords="SEO, marketing, strategi",
    save_changes=False
)
```

### Utility Tools

#### `get_categories`
Hent alle kategorier.

**Eksempel:**
```python
get_categories()
```

#### `get_tags`
Hent alle tags.

**Eksempel:**
```python
get_tags()
```

#### `search_posts`
Søg i posts.

**Parameters:**
- `query` (string) - Søgetekst
- `search_in` (string) - Felter at søge i (title, content, excerpt)

**Eksempel:**
```python
search_posts(
    query="marketing",
    search_in="title,content"
)
```

## Projektstruktur

```
wordpress-content-mcp/
├── README.md                  # Denne fil
├── requirements.txt           # Python dependencies
├── .env.example              # Eksempel på miljøvariabler
├── .env                      # Dine miljøvariabler (git ignored)
├── mcp_server.py             # Hovedfil for MCP server
├── src/
│   ├── config/
│   │   └── settings.py       # Konfiguration
│   ├── api/
│   │   └── wordpress_client.py  # WordPress REST API client
│   ├── services/
│   │   ├── post_service.py   # Post management
│   │   └── content_generator.py  # AI content generation
│   ├── models/
│   │   └── post.py           # Data models
│   └── utils/
│       └── validators.py     # Validering
└── tests/
    └── test_wordpress_client.py
```

## Sikkerhed

- **Credentials**: Gem aldrig credentials i kode. Brug altid `.env` fil.
- **Application Passwords**: Brug WordPress Application Passwords i stedet for dit hovedpassword.
- **Git**: `.env` filen er automatisk ignoreret i `.gitignore`.
- **Permissions**: Giv kun nødvendige rettigheder til WordPress-brugeren.

## Fejlfinding

### "Missing required configuration"
- Tjek at `.env` filen eksisterer og indeholder alle nødvendige variabler
- Verificer at værdierne er korrekte

### "Authentication failed"
- Verificer at WordPress Application Password er korrekt
- Tjek at brugernavnet er korrekt
- Sørg for at brugeren har rettigheder til at oprette/redigere posts

### "OpenAI API error"
- Verificer at OPENAI_API_KEY er korrekt
- Tjek at du har credits på din OpenAI konto

## Integration med AI-seo-tools

Denne MCP-server kan integreres med jeres eksisterende AI-seo-tools MCP-server for at:

1. **SEO-analyse af genereret indhold**
   - Brug `analyze_google_serp` til at tjekke konkurrence
   - Brug `generate_query_strategy` til keyword research

2. **Content optimization workflow**
   ```
   1. Generer queries med AI-seo-tools
   2. Generer blog post med wordpress-content-mcp
   3. Analyser SEO med AI-seo-tools
   4. Optimer post med wordpress-content-mcp
   5. Publicer
   ```

## Support

For problemer eller spørgsmål:
1. Tjek denne dokumentation
2. Verificer `.env` konfiguration
3. Tjek logs for fejlmeddelelser

## Licens

Proprietary - InboundCPH A/S

---

*Udviklet til InboundCPH's WordPress content management workflow*

