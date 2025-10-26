"""AI-powered content generation service."""

import logging
from typing import List, Optional, Dict, Any
from openai import OpenAI
from ..config.settings import settings

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Service for generating and improving content using AI."""
    
    def __init__(self):
        """Initialize content generator with OpenAI client."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o"  # Using GPT-4o for best quality
    
    def generate_blog_post(
        self,
        topic: str,
        keywords: Optional[List[str]] = None,
        tone: str = "professional",
        length: str = "medium",
        language: str = "da"
    ) -> Dict[str, str]:
        """Generate a complete blog post."""
        
        # Determine word count based on length
        word_counts = {
            "short": "400-600",
            "medium": "800-1200",
            "long": "1500-2000"
        }
        word_count = word_counts.get(length, "800-1200")
        
        # Build prompt
        prompt = f"""Skriv et professionelt blog indlæg på {language} om følgende emne:

Emne: {topic}

Krav:
- Længde: {word_count} ord
- Tone: {tone}
- Sprog: {language}
- Struktureret med overskrifter (H2, H3)
- Inkluder en engagerende introduktion
- Brug korte, læsbare afsnit
- Afslut med en konklusion eller call-to-action
"""
        
        if keywords:
            prompt += f"\n- Inkluder naturligt disse keywords: {', '.join(keywords)}"
        
        prompt += """

Formater indholdet som HTML med:
- <h2> for hovedoverskrifter
- <h3> for underoverskrifter  
- <p> for afsnit
- <ul> og <li> for punktlister hvor relevant
- <strong> for fremhævning

Returner KUN HTML-indholdet uden ```html tags eller forklaringer."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Du er en ekspert content writer specialiseret i SEO-optimeret blog indhold. Du skriver engagerende, informativt og professionelt indhold."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            
            # Generate title
            title = self._generate_title(topic, keywords, language)
            
            # Generate excerpt
            excerpt = self._generate_excerpt(content, language)
            
            return {
                "title": title,
                "content": content,
                "excerpt": excerpt
            }
        
        except Exception as e:
            logger.error(f"Error generating blog post: {str(e)}")
            raise
    
    def _generate_title(
        self,
        topic: str,
        keywords: Optional[List[str]],
        language: str
    ) -> str:
        """Generate an engaging title for the post."""
        prompt = f"""Generer en engagerende og SEO-venlig titel på {language} for et blog indlæg om:

Emne: {topic}
"""
        if keywords:
            prompt += f"Keywords: {', '.join(keywords)}\n"
        
        prompt += """
Krav:
- Maksimalt 60 tegn
- Inkluder primært keyword hvis muligt
- Gør den engagerende og klikbar
- Returner KUN titlen, ingen forklaringer"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Du er en SEO-ekspert specialiseret i at skrive engagerende titler."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip().strip('"')
        
        except Exception as e:
            logger.error(f"Error generating title: {str(e)}")
            return topic  # Fallback to topic
    
    def _generate_excerpt(self, content: str, language: str) -> str:
        """Generate an excerpt from content."""
        prompt = f"""Baseret på følgende blog indhold, skriv et kort og engagerende uddrag (excerpt) på {language}:

{content[:1000]}...

Krav:
- Maksimalt 160 tegn
- Opsummer hovedbudskabet
- Gør det engagerende
- Returner KUN uddraget, ingen forklaringer"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Du er en ekspert i at skrive korte, engagerende beskrivelser."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip().strip('"')
        
        except Exception as e:
            logger.error(f"Error generating excerpt: {str(e)}")
            # Fallback: extract first sentence from content
            import re
            text = re.sub('<[^<]+?>', '', content)  # Strip HTML
            sentences = text.split('.')
            return sentences[0][:160] + "..." if sentences else ""
    
    def improve_content(
        self,
        content: str,
        improvements: List[str],
        language: str = "da"
    ) -> str:
        """Improve existing content based on specified improvements."""
        
        improvement_instructions = {
            "seo": "Optimer for SEO ved at forbedre keyword-brug, overskrifter og struktur",
            "readability": "Forbedre læsbarheden ved at forkorte sætninger og gøre sproget mere tilgængeligt",
            "structure": "Forbedre strukturen med bedre overskrifter, afsnit og flow",
            "grammar": "Ret grammatik, stavefejl og formulering"
        }
        
        instructions = [improvement_instructions.get(imp, imp) for imp in improvements]
        
        prompt = f"""Forbedre følgende blog indhold på {language}:

{content}

Forbedringer der skal laves:
{chr(10).join(f'- {inst}' for inst in instructions)}

Krav:
- Bevar HTML-formateringen
- Bevar den overordnede struktur
- Gør kun de nødvendige forbedringer
- Returner det forbedrede indhold som HTML uden forklaringer"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Du er en ekspert content editor specialiseret i at forbedre blog indhold."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"Error improving content: {str(e)}")
            raise
    
    def optimize_for_seo(
        self,
        title: str,
        content: str,
        target_keywords: Optional[List[str]] = None,
        language: str = "da"
    ) -> Dict[str, str]:
        """Optimize title and content for SEO."""
        
        prompt = f"""Optimer følgende blog indlæg for SEO på {language}:

Nuværende titel: {title}

Indhold:
{content[:1500]}...

"""
        if target_keywords:
            prompt += f"Target keywords: {', '.join(target_keywords)}\n"
        
        prompt += """
Generer:
1. En forbedret SEO-optimeret titel (max 60 tegn)
2. En meta description (max 160 tegn)
3. Forslag til forbedringer af indholdet

Format dit svar som JSON:
{
  "title": "forbedret titel",
  "meta_description": "meta beskrivelse",
  "content_suggestions": ["forslag 1", "forslag 2"]
}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Du er en SEO-ekspert. Returner altid valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            import json
            return json.loads(response.choices[0].message.content)
        
        except Exception as e:
            logger.error(f"Error optimizing for SEO: {str(e)}")
            raise

