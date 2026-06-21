// Servidor mínimo (sem dependências) para o site da Facilita Veículos.
//  /          -> landing page (pública)
//  /login     -> tela de login estilizada (pública)
//  /dashboard -> painel de gestão (protegido por sessão via cookie assinado)
//  /logout    -> encerra a sessão
// Variáveis de ambiente (Railway): DASH_USER, DASH_PASS, DASH_SLUG, SESSION_SECRET (PORT é injetado).

const http = require("http");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const PORT = process.env.PORT || 3000;
const SLUG = process.env.DASH_SLUG || "/dashboard";
const SESSAO_HORAS = 12; // validade do login

// ---------- usuários ----------
// Vários usuários: DASH_USERS="usuario1:senha1,usuario2:senha2,maria:senha3"
// (também aceita DASH_USER + DASH_PASS para 1 usuário, por compatibilidade)
function carregarUsuarios() {
  const map = {};
  if (process.env.DASH_USER) map[process.env.DASH_USER] = process.env.DASH_PASS || "";
  (process.env.DASH_USERS || "").split(",").forEach((par) => {
    const i = par.indexOf(":");
    if (i > 0) {
      const u = par.slice(0, i).trim();
      const s = par.slice(i + 1).trim();
      if (u) map[u] = s;
    }
  });
  if (Object.keys(map).length === 0) map["facilita"] = "troque-esta-senha"; // padrão
  return map;
}
const USERS = carregarUsuarios();
const SECRET =
  process.env.SESSION_SECRET ||
  "facilita-secret-2026:" + Object.keys(USERS).sort().join(",");

// arquivos públicos liberados (allowlist)
const PUBLICOS = {
  "/": { file: "landing.html", type: "text/html; charset=utf-8" },
  "/login": { file: "login.html", type: "text/html; charset=utf-8" },
  "/favicon.svg": { file: "favicon.svg", type: "image/svg+xml" },
};

// ---------- helpers ----------
function send(res, code, body, type) {
  res.writeHead(code, { "Content-Type": type || "text/plain; charset=utf-8" });
  res.end(body);
}
function serveFile(res, file, type) {
  fs.readFile(path.join(__dirname, file), (err, data) => {
    if (err) return send(res, 404, "Não encontrado");
    send(res, 200, data, type);
  });
}
function redirect(res, location, cookie) {
  const h = { Location: location };
  if (cookie) h["Set-Cookie"] = cookie;
  res.writeHead(302, h);
  res.end();
}
function parseCookies(req) {
  const out = {};
  (req.headers.cookie || "").split(";").forEach((c) => {
    const i = c.indexOf("=");
    if (i > -1) out[c.slice(0, i).trim()] = decodeURIComponent(c.slice(i + 1).trim());
  });
  return out;
}

// ---------- token de sessão assinado (HMAC-SHA256) ----------
function assinar(payload) {
  const data = Buffer.from(JSON.stringify(payload)).toString("base64url");
  const sig = crypto.createHmac("sha256", SECRET).update(data).digest("base64url");
  return `${data}.${sig}`;
}
function valido(token) {
  if (!token) return false;
  const [data, sig] = token.split(".");
  if (!data || !sig) return false;
  const esperado = crypto.createHmac("sha256", SECRET).update(data).digest("base64url");
  const a = Buffer.from(sig), b = Buffer.from(esperado);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return false;
  try {
    const p = JSON.parse(Buffer.from(data, "base64url").toString());
    return !(p.exp && Date.now() > p.exp);
  } catch {
    return false;
  }
}
function autenticado(req) {
  return valido(parseCookies(req)["fv_session"]);
}

// ---------- servidor ----------
http
  .createServer((req, res) => {
    const url = req.url.split("?")[0];
    const https = (req.headers["x-forwarded-proto"] || "").includes("https");

    // POST /login  -> valida credenciais
    if (req.method === "POST" && url === "/login") {
      let body = "";
      req.on("data", (c) => { body += c; if (body.length > 1e4) req.destroy(); });
      req.on("end", () => {
        const p = new URLSearchParams(body);
        const u = p.get("usuario"), s = p.get("senha");
        if (u && Object.prototype.hasOwnProperty.call(USERS, u) && USERS[u] === s) {
          const token = assinar({ u, exp: Date.now() + SESSAO_HORAS * 3600e3 });
          const cookie =
            `fv_session=${token}; HttpOnly; Path=/; SameSite=Lax; Max-Age=${SESSAO_HORAS * 3600}` +
            (https ? "; Secure" : "");
          return redirect(res, SLUG, cookie);
        }
        return redirect(res, "/login?erro=1");
      });
      return;
    }

    // logout
    if (url === "/logout") {
      return redirect(res, "/login", "fv_session=; HttpOnly; Path=/; Max-Age=0");
    }

    // painel protegido
    if (url === SLUG || url === SLUG + "/") {
      if (!autenticado(req)) return redirect(res, "/login");
      return serveFile(res, "dashboard.html", "text/html; charset=utf-8");
    }

    // se já logado e acessar /login, manda pro painel
    if (url === "/login" && autenticado(req)) return redirect(res, SLUG);

    // arquivos públicos
    if (PUBLICOS[url]) return serveFile(res, PUBLICOS[url].file, PUBLICOS[url].type);

    send(res, 404, "Não encontrado");
  })
  .listen(PORT, () => console.log(`Facilita no ar na porta ${PORT} | painel em ${SLUG}`));
