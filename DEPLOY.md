# Como publicar no Railway

O site tem estas rotas servidas pelo `server.js`:

- `/` → **landing page** (pública)
- `/login` → **tela de login estilizada** (pública)
- `/dashboard` → **painel de gestão** (protegido — exige login)
- `/logout` → encerra a sessão

O login usa **cookie de sessão assinado** (HMAC), válido por 12h.

## Antes de subir
Sempre que mudar os dados ou o template, rode:
```
python build.py
```
Isso regenera o `dashboard.html` com os dados embutidos.

## Opção A — Deploy pelo GitHub (recomendado, faz deploy automático)

1. Crie um repositório no GitHub e suba a pasta do projeto:
   ```
   git init
   git add .
   git commit -m "Site Facilita Veículos"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/facilita-veiculos.git
   git push -u origin main
   ```
2. Acesse https://railway.app → **New Project** → **Deploy from GitHub repo** → escolha o repositório.
3. O Railway detecta o Node automaticamente e roda `npm start`.
4. Em **Variables**, defina (importante!):
   - `DASH_USER` = usuário do painel (ex.: `facilita`)
   - `DASH_PASS` = uma senha forte
   - `DASH_SLUG` = `/dashboard` (opcional, pode trocar o endereço do painel)
   - `SESSION_SECRET` = um texto aleatório longo (assina os cookies de sessão)
5. Em **Settings → Networking → Generate Domain** para receber a URL pública.
   - Landing: `https://SEU-APP.up.railway.app/`
   - Painel: `https://SEU-APP.up.railway.app/dashboard`

## Opção B — Deploy pela CLI (rápido, sem GitHub)

```
npm i -g @railway/cli
railway login
railway init
railway up
railway variables set DASH_USER=facilita DASH_PASS=senhaforte
railway domain
```

## Domínio próprio (opcional)
Em **Settings → Networking → Custom Domain**, aponte o domínio da revenda
(ex.: `facilitaveiculos.com.br`) e configure o CNAME no provedor do domínio.

## Segurança
- A senha do painel vai nas **Variables** do Railway (nunca no código).
- O Railway serve em **HTTPS**, então a senha trafega criptografada.
- Troque `DASH_PASS` antes de divulgar a URL.
