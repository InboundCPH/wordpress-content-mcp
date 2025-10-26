# WordPress Content Management MCP Server - Projekt Oversigt

## Hvad er dette projekt?

En intelligent MCP (Model Context Protocol) server der gør det muligt for AI-assistenter som Manus at administrere WordPress-indhold. Serveren kombinerer WordPress REST API med OpenAI's GPT-4 for at tilbyde kraftfulde content management funktioner.

## Nøglefunktioner

### ✅ Implementeret

1. **Post Management**
   - Liste, hent, opret, opdater, slet WordPress-indlæg
   - Fuld support for ACF (Advanced Custom Fields)
   - Kategorier og tags håndtering
   - Søgning i posts

2. **AI Content Generation**
   - Generer komplette blog posts med GPT-4
   - Intelligent titel og excerpt generation
   - Multi-sprog support (dansk, engelsk, svensk, etc.)
   - Konfigurerbar tone og længde

3. **Content Improvement**
   - Forbedre eksisterende indhold for SEO
   - Øge læsbarhed
   - Strukturere indhold bedre
   - Grammatik og stavekontrol

4. **SEO Optimization**
   - Generer SEO-optimerede titler
   - Opret meta descriptions
   - Keyword optimization
   - Content gap analysis

5. **Utility Functions**
   - Hent kategorier og tags
   - Søg i posts
   - Validering og fejlhåndtering

## Teknisk Stack

- **Python 3.11+**
- **FastMCP** - MCP server framework
- **OpenAI GPT-4** - Content generation
- **WordPress REST API** - WordPress integration
- **Pydantic** - Data validation
- **Requests** - HTTP client

## Projektstruktur

```
wordpress-content-mcp/
├── README.md                    # Hoveddokumentation
├── SETUP_GUIDE.md              # Setup instruktioner
├── WORKFLOWS.md                # Workflow eksempler
├── DEPLOYMENT.md               # Deployment guide
├── requirements.txt            # Python dependencies
├── .env.example               # Eksempel miljøvariabler
├── .gitignore                 # Git ignore fil
├── mcp_server.py              # Hovedfil - MCP server
├── test_mcp_tools.py          # Test script
├── src/
│   ├── config/
│   │   └── settings.py        # Konfiguration
│   ├── api/
│   │   └── wordpress_client.py # WordPress API client
│   ├── services/
│   │   ├── post_service.py    # Post management
│   │   └── content_generator.py # AI content generation
│   ├── models/
│   │   └── post.py            # Data models
│   └── utils/
│       └── validators.py      # Validering
└── tests/
    └── test_wordpress_client.py
```

## MCP Tools (12 total)

### Post Management (5)
1. `list_posts` - Liste indlæg med filtrering
2. `get_post` - Hent specifikt indlæg
3. `create_post` - Opret nyt indlæg
4. `update_post` - Opdater indlæg
5. `delete_post` - Slet indlæg

### AI Content (3)
6. `generate_blog_post` - Generer komplet blog post
7. `improve_post_content` - Forbedre eksisterende indhold
8. `optimize_post_seo` - SEO-optimer post

### Utility (3)
9. `get_categories` - Hent kategorier
10. `get_tags` - Hent tags
11. `search_posts` - Søg i posts

## Sikkerhed

- **Application Passwords**: Bruger WordPress Application Passwords (ikke hovedpassword)
- **Environment Variables**: Alle credentials i .env fil
- **Git Security**: .env er git-ignored
- **Input Validation**: Pydantic models validerer alle inputs
- **Error Handling**: Robust fejlhåndtering på alle API calls

## Kom i Gang

### Quick Start

1. **Clone repository**
   ```bash
   git clone https://github.com/InboundCPH/wordpress-content-mcp.git
   cd wordpress-content-mcp
   ```

2. **Installer dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Konfigurer .env**
   ```bash
   cp .env.example .env
   # Rediger .env med dine credentials
   ```

4. **Start server**
   ```bash
   python3 mcp_server.py
   ```

5. **Tilføj til Manus**
   - Åbn Manus settings
   - Tilføj MCP server med sti til mcp_server.py

### Detaljeret Setup

Se **SETUP_GUIDE.md** for trin-for-trin instruktioner.

## Brug Eksempler

### Generer Blog Post
```
Generer et blog indlæg om "AI i digital marketing" på dansk,
med keywords "AI, marketing, automation". Gem som draft.
```

### Forbedre Indhold
```
Forbedre WordPress post ID 123 for bedre SEO og læsbarhed.
Vis forslagene først.
```

### Søg i Posts
```
Søg efter alle posts om "marketing automation"
```

Se **WORKFLOWS.md** for flere eksempler.

## Integration med AI-seo-tools

Denne MCP-server kan kombineres med InboundCPH's AI-seo-tools for:

1. **Keyword Research** → Content Generation
2. **Competitor Analysis** → Content Strategy
3. **SEO Analysis** → Content Optimization
4. **Performance Tracking** → Content Updates

## Deployment

### Lokalt (Development)
```bash
python3 mcp_server.py
```

### Railway (Production)
- Auto-deploy fra GitHub
- Miljøvariabler i Railway dashboard
- HTTPS automatisk

### Docker
```bash
docker build -t wordpress-mcp .
docker run -p 8000:8000 --env-file .env wordpress-mcp
```

Se **DEPLOYMENT.md** for detaljerede instruktioner.

## Testing

### Test MCP Tools
```bash
python3 test_mcp_tools.py
```

### Test WordPress Connection
```bash
python3 -c "from src.api.wordpress_client import WordPressClient; print(WordPressClient().get_posts(per_page=1))"
```

## Dokumentation

- **README.md** - Hoveddokumentation og API reference
- **SETUP_GUIDE.md** - Trin-for-trin setup guide
- **WORKFLOWS.md** - Praktiske workflow eksempler
- **DEPLOYMENT.md** - Deployment guide til forskellige miljøer
- **PROJECT_SUMMARY.md** - Dette dokument

## Fremtidige Forbedringer

### Potentielle Features

1. **Custom Post Types**
   - Support for pages
   - Support for custom post types
   - WooCommerce products

2. **Media Management**
   - Upload billeder
   - Generer featured images med AI
   - Optimér billeder

3. **Advanced ACF**
   - Auto-detect ACF field groups
   - Intelligent field population
   - Repeater field support

4. **Bulk Operations**
   - Batch post creation
   - Bulk content updates
   - Mass SEO optimization

5. **Analytics Integration**
   - Google Analytics data
   - Performance tracking
   - Content recommendations

6. **Scheduling**
   - Schedule post publication
   - Content calendar integration
   - Automated posting

## Support og Bidrag

### Rapporter Issues
- Brug GitHub Issues
- Inkluder fejlmeddelelser
- Beskriv forventet vs. faktisk adfærd

### Bidrag
1. Fork repository
2. Opret feature branch
3. Commit ændringer
4. Push til branch
5. Opret Pull Request

## Licens

Proprietary - InboundCPH A/S

## Credits

Udviklet til InboundCPH's content management workflow.

**Teknologier:**
- FastMCP - https://github.com/jlowin/fastmcp
- OpenAI GPT-4 - https://openai.com
- WordPress REST API - https://developer.wordpress.org/rest-api/

---

**Version:** 1.0.0  
**Sidste opdatering:** Oktober 2025  
**Status:** Production Ready ✅
