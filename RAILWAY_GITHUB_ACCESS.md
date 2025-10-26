# Giv Railway Adgang til GitHub Organisation

## Problem

Du kan ikke se `InboundCPH/wordpress-content-mcp` repository i Railway fordi Railway ikke har adgang til din GitHub organisation (InboundCPH).

## Løsning: Giv Railway Adgang til Organisation

### Metode 1: Via Railway (Anbefalet)

1. **Log ind på Railway**
   - Gå til https://railway.app
   - Log ind med GitHub

2. **Start ny deployment**
   - Klik "New Project"
   - Vælg "Deploy from GitHub repo"

3. **Klik "Configure GitHub App"**
   - Du skulle se en knap der siger "Configure GitHub App" eller lignende
   - Dette åbner GitHub's permission side

4. **Giv adgang til InboundCPH organisation**
   - På GitHub siden, find "Organization access"
   - Find "InboundCPH"
   - Klik "Grant" eller "Request" ved siden af InboundCPH
   - Hvis du er admin: Klik "Grant" for at give adgang med det samme
   - Hvis du ikke er admin: Klik "Request" og vent på godkendelse fra admin

5. **Vælg repository adgang**
   - Vælg enten:
     - "All repositories" (giver Railway adgang til alle repos)
     - "Only select repositories" → vælg `wordpress-content-mcp`

6. **Gem og gå tilbage til Railway**
   - Klik "Save"
   - Gå tilbage til Railway
   - Nu skulle du kunne se `InboundCPH/wordpress-content-mcp`

### Metode 2: Via GitHub Direkte

1. **Gå til GitHub Settings**
   - Gå til https://github.com/settings/installations

2. **Find Railway App**
   - Find "Railway" i listen over installed GitHub Apps
   - Klik "Configure"

3. **Repository Access**
   - Under "Repository access" sektion
   - Vælg "All repositories" eller "Select repositories"
   - Hvis "Select repositories": Tilføj `InboundCPH/wordpress-content-mcp`

4. **Organisation Access**
   - Scroll ned til "Organization access"
   - Find "InboundCPH"
   - Klik "Grant" (hvis du er admin) eller "Request" (hvis ikke admin)

5. **Gem ændringer**
   - Klik "Save"
   - Gå tilbage til Railway og refresh

### Metode 3: Deploy via GitHub Link (Hurtigste)

Hvis du stadig ikke kan se repository, kan du deploye direkte via link:

1. **Gå til Railway**
   - https://railway.app

2. **Brug denne direkte link**
   ```
   https://railway.app/new/github?template=https://github.com/InboundCPH/wordpress-content-mcp
   ```

3. **Eller klik "Deploy" knappen**
   - Jeg kan tilføje en "Deploy to Railway" knap i README

### Metode 4: Fork Repository til Din Personlige Account

Hvis du ikke har admin adgang til InboundCPH organisation:

1. **Fork repository**
   - Gå til https://github.com/InboundCPH/wordpress-content-mcp
   - Klik "Fork" i øverste højre hjørne
   - Fork til din personlige GitHub account

2. **Deploy fra din fork**
   - Gå til Railway
   - Vælg "Deploy from GitHub repo"
   - Vælg din fork: `dit-brugernavn/wordpress-content-mcp`

3. **Sync med original** (valgfrit)
   - Du kan senere synce ændringer fra original repository

## Verificer Adgang

Efter at have givet Railway adgang:

1. **Gå til Railway**
2. **Klik "New Project"**
3. **Vælg "Deploy from GitHub repo"**
4. **Søg efter "wordpress-content-mcp"**
5. **Du skulle nu kunne se det!**

## Hvis Du Er Organisation Admin

Hvis du er admin af InboundCPH organisation:

1. **Gå til Organisation Settings**
   - https://github.com/organizations/InboundCPH/settings/installations

2. **Find Railway**
   - Se om Railway er installeret
   - Hvis ikke: Installer Railway GitHub App

3. **Konfigurer Adgang**
   - Giv Railway adgang til `wordpress-content-mcp` repository
   - Eller giv adgang til alle repositories

## Hvis Du IKKE Er Organisation Admin

Hvis du ikke har admin rettigheder:

**Option A: Bed admin om at give Railway adgang**
1. Kontakt InboundCPH organisation admin
2. Bed dem følge guiden ovenfor
3. Vent på godkendelse

**Option B: Brug din personlige fork**
1. Fork repository til din personlige account
2. Deploy fra din fork
3. Du har fuld kontrol over din fork

## Troubleshooting

### "I can't see the Configure GitHub App button"

**Løsning:**
- Gå direkte til: https://github.com/settings/installations
- Find Railway og konfigurer der

### "I don't have permission to grant access"

**Løsning:**
- Du skal være organisation admin
- Alternativt: Fork repository til din personlige account

### "Railway still can't see my repo"

**Løsning:**
1. Log ud af Railway
2. Log ind igen
3. Prøv at refresh siden
4. Tjek at repository er public (det er det)

### "Deploy button doesn't work"

**Løsning:**
- Brug direkte link metoden (Metode 3)
- Eller fork repository (Metode 4)

## Hurtig Løsning: Deploy via Direct Link

Klik på dette link for at deploye direkte:

```
https://railway.app/new/github?template=https://github.com/InboundCPH/wordpress-content-mcp
```

Eller brug denne Railway Deploy knap (jeg kan tilføje til README):

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/github?template=https://github.com/InboundCPH/wordpress-content-mcp)

---

**Når du har fået adgang, følg RAILWAY_SETUP.md for at færdiggøre deployment! 🚀**

