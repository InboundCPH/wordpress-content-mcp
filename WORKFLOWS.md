# WordPress MCP Server - Workflow Eksempler

Dette dokument viser praktiske workflows for at bruge WordPress MCP-serveren sammen med AI-assistenter som Manus.

## Basic Workflows

### 1. Liste og Gennemse Indlæg

**Scenarie:** Du vil se de seneste blog posts på dit site.

**Manus kommando:**
```
Hent de 10 seneste publicerede blog posts fra WordPress
```

**Hvad sker der:**
- MCP-serveren kalder `list_posts(per_page=10, status="publish")`
- Returnerer liste med titel, ID, dato og link

**Opfølgning:**
```
Vis mig det fulde indhold af post ID 123
```

### 2. Søg i Eksisterende Indlæg

**Scenarie:** Du vil finde alle posts om et specifikt emne.

**Manus kommando:**
```
Søg efter alle WordPress posts der handler om "AI" eller "kunstig intelligens"
```

**Hvad sker der:**
- MCP-serveren kalder `search_posts(query="AI kunstig intelligens")`
- Returnerer matching posts med uddrag

### 3. Opret Simpelt Indlæg

**Scenarie:** Du har allerede skrevet indhold og vil uploade det.

**Manus kommando:**
```
Opret et nyt WordPress indlæg med følgende:
Titel: "Sådan bruger du AI i din marketing"
Indhold: <p>AI revolutionerer digital marketing...</p>
Status: draft
Kategorier: 1,5
```

**Hvad sker der:**
- MCP-serveren kalder `create_post()` med de angivne parametre
- Returnerer post ID og link

## AI Content Generation Workflows

### 4. Generer Komplet Blog Post

**Scenarie:** Du vil have AI til at skrive et helt blog indlæg.

**Manus kommando:**
```
Generer et professionelt blog indlæg på dansk om "AI i e-commerce" 
med følgende keywords: "AI, e-handel, automation, personalisering".
Gør det medium længde og gem som draft.
```

**Hvad sker der:**
1. MCP-serveren kalder `generate_blog_post()`
2. AI genererer titel, indhold og excerpt
3. Indlægget gemmes som draft i WordPress
4. Du får post ID og link tilbage

**Resultat:**
- Komplet blog post med struktureret HTML
- SEO-optimeret titel
- Engagerende excerpt
- Klar til review og publicering

### 5. Generer Serie af Blog Posts

**Scenarie:** Du vil oprette flere relaterede blog posts.

**Manus kommando:**
```
Generer 3 blog posts om følgende emner:
1. "Introduktion til AI i marketing"
2. "AI-værktøjer til content marketing"
3. "Fremtiden for AI i marketing"

Alle på dansk, professionel tone, medium længde, gem som drafts.
```

**Hvad sker der:**
- MCP-serveren genererer 3 separate posts
- Hver post får sin egen titel, indhold og excerpt
- Alle gemmes som drafts

## Content Improvement Workflows

### 6. Forbedre Eksisterende Indlæg

**Scenarie:** Du har et gammelt indlæg der skal opdateres.

**Manus kommando:**
```
Forbedre WordPress post ID 123 for bedre SEO og læsbarhed.
Vis mig forslagene først, gem dem ikke automatisk.
```

**Hvad sker der:**
1. MCP-serveren henter det eksisterende indlæg
2. AI analyserer og forbedrer indholdet
3. Du får både original og forbedret version
4. Du kan vælge at gemme ændringerne

**Opfølgning:**
```
Det ser godt ud, gem de forbedrede ændringer
```

### 7. SEO-Optimer Post

**Scenarie:** Du vil optimere et indlæg for specifikke keywords.

**Manus kommando:**
```
Optimer WordPress post ID 456 for SEO med target keywords: 
"digital marketing strategi", "online marketing", "marketing automation".
Vis forslag til forbedret titel og meta description.
```

**Hvad sker der:**
1. MCP-serveren analyserer det eksisterende indlæg
2. AI genererer SEO-optimeret titel og meta description
3. Du får forslag til content forbedringer
4. Du kan vælge at gemme ændringerne

### 8. Bulk Content Improvement

**Scenarie:** Du vil forbedre flere indlæg på én gang.

**Manus kommando:**
```
Find alle WordPress posts fra 2023 og forbedre dem for bedre læsbarhed.
Start med de 5 ældste posts.
```

**Hvad sker der:**
1. MCP-serveren søger efter posts fra 2023
2. Sorterer efter dato
3. Forbedrer de 5 ældste posts
4. Viser resultaterne

## Advanced Workflows

### 9. Content Workflow med SEO-Analyse

**Scenarie:** Du vil oprette SEO-optimeret indhold baseret på konkurrent-analyse.

**Manus kommando:**
```
1. Analyser Google SERP for "AI marketing tools" (brug AI-seo-tools)
2. Generer et blog indlæg der dækker de emner konkurrenterne mangler
3. Optimer indlægget for target keywords
4. Gem som draft i WordPress
```

**Hvad sker der:**
1. AI-seo-tools analyserer konkurrenterne
2. Identificerer content gaps
3. WordPress MCP genererer indhold der udfylder gaps
4. Indlægget SEO-optimeres
5. Gemmes som draft

### 10. Content Calendar Automation

**Scenarie:** Du vil planlægge en måned med blog posts.

**Manus kommando:**
```
Opret en content calendar for november med 8 blog posts om:
- AI trends (2 posts)
- Marketing automation (3 posts)  
- SEO strategi (3 posts)

Generer alle posts som drafts med passende keywords.
```

**Hvad sker der:**
1. MCP-serveren genererer 8 blog posts
2. Hver post får relevant titel og indhold
3. Keywords fordeles strategisk
4. Alle gemmes som drafts
5. Du får en oversigt med post IDs og titler

### 11. Content Refresh Workflow

**Scenarie:** Du vil opdatere gamle posts med ny information.

**Manus kommando:**
```
Find alle WordPress posts om "SEO" fra før 2024.
For hver post:
1. Tjek om informationen er forældet
2. Tilføj ny information om AI-SEO
3. Opdater meta description
4. Gem ændringerne
```

**Hvad sker der:**
1. Søger efter gamle SEO posts
2. AI analyserer hver post
3. Tilføjer opdateret information
4. Opdaterer SEO metadata
5. Gemmer ændringerne

## Integration med AI-seo-tools

### 12. Komplet SEO Content Workflow

**Scenarie:** Fra keyword research til publicering.

**Workflow:**

**Step 1: Keyword Research**
```
Brug AI-seo-tools til at generere en query strategi for:
- Business area: Digital marketing bureau
- Target audience: B2B virksomheder
- Buying job: Finde det bedste marketing bureau
```

**Step 2: Competitor Analysis**
```
Analyser Google SERP for de top 5 queries fra strategien
```

**Step 3: Content Generation**
```
Baseret på analysen, generer blog posts der:
- Dækker de identificerede emner
- Bruger de anbefalede keywords
- Adresserer content gaps
```

**Step 4: SEO Optimization**
```
Optimer hver post for:
- Target keywords
- Meta descriptions
- Heading struktur
```

**Step 5: Quality Check**
```
Gennemgå alle posts og publicer de bedste
```

## Tips til Effektive Workflows

### 1. Start med Drafts
Gem altid AI-genereret indhold som drafts først, så du kan gennemgå det.

### 2. Brug Specifik Tone
Angiv altid tone (professional, casual, friendly) for konsistent brand voice.

### 3. Inkluder Keywords
Giv altid relevante keywords for bedre SEO.

### 4. Review AI Content
AI-genereret indhold er godt, men skal altid gennemgås af en person.

### 5. Batch Operations
Når du arbejder med mange posts, brug batch operations for effektivitet.

### 6. Kombiner Tools
Brug WordPress MCP sammen med AI-seo-tools for bedste resultater.

### 7. Dokumenter Workflows
Gem dine mest brugte workflows for gentagelse.

## Eksempel på Daglig Workflow

### Morgen: Content Review
```
1. Hent alle draft posts fra WordPress
2. Gennemgå AI-genereret indhold
3. Foretag nødvendige rettelser
4. Publicer godkendte posts
```

### Middag: Content Creation
```
1. Generer 2-3 nye blog posts baseret på content calendar
2. Gem som drafts
3. Schedule til review næste dag
```

### Eftermiddag: Content Optimization
```
1. Find gamle posts der skal opdateres
2. Forbedre for SEO og læsbarhed
3. Opdater publicerede posts
```

## Fejlfinding i Workflows

### Problem: AI-genereret indhold er for generisk

**Løsning:**
- Giv mere specifikke instruktioner
- Inkluder flere keywords
- Angiv target audience tydeligt
- Giv eksempler på ønsket stil

### Problem: SEO-optimering ændrer for meget

**Løsning:**
- Brug `save_changes=false` først for at se forslag
- Gennemgå forslag før gemning
- Angiv hvilke dele der skal optimeres

### Problem: Bulk operations tager for lang tid

**Løsning:**
- Arbejd med mindre batches (5-10 posts ad gangen)
- Brug mere specifikke filtre
- Overvej at køre operationer om natten

---

**Disse workflows er udgangspunkter - tilpas dem til dine specifikke behov! 🚀**

