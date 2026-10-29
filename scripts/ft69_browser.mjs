// Conferência da UI pelo Chrome DevTools Protocol, sem dependências npm extras.
import { spawn } from "node:child_process";
import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { tmpdir } from "node:os";
import { join } from "node:path";
import assert from "node:assert/strict";

const [url, output] = process.argv.slice(2);
const profile = await mkdtemp(join(tmpdir(), "feneme-ft69-chrome-"));
const chrome = spawn(process.env.CHROME_PATH || "C:/Program Files/Google/Chrome/Application/chrome.exe", [
  "--headless=new", "--remote-debugging-port=0", `--user-data-dir=${profile}`,
  "--disable-background-networking", "--no-first-run", "--no-default-browser-check", "about:blank",
], { windowsHide: true, stdio: ["ignore", "ignore", "pipe"] });
let ws;
const checks = [];
const started = new Date().toISOString();
try {
  const endpoint = await new Promise((resolve, reject) => {
    let stderr = "";
    const timeout = setTimeout(() => reject(new Error("Chrome não iniciou em 15 segundos.")), 15000);
    chrome.on("error", reject);
    chrome.on("exit", code => reject(new Error(`Chrome encerrou: ${code}`)));
    chrome.stderr.on("data", data => {
      stderr += data;
      const match = stderr.match(/DevTools listening on (ws:\/\/[^\s]+)/);
      if (match) { clearTimeout(timeout); resolve(match[1]); }
    });
  });
  ws = new WebSocket(endpoint);
  await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });
  let nextId = 0;
  const pending = new Map();
  ws.onmessage = event => {
    const message = JSON.parse(event.data);
    if (!pending.has(message.id)) return;
    const { resolve, reject, timeout } = pending.get(message.id);
    pending.delete(message.id);
    clearTimeout(timeout);
    if (message.error) reject(new Error(JSON.stringify(message.error)));
    else resolve(message.result);
  };
  const call = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
    const id = ++nextId;
    const timeout = setTimeout(() => { pending.delete(id); reject(new Error(`Timeout: ${method}`)); }, 15000);
    pending.set(id, { resolve, reject, timeout });
    ws.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));
  });
  const version = await call("Browser.getVersion");
  const { targetId } = await call("Target.createTarget", { url: "about:blank" });
  const { sessionId } = await call("Target.attachToTarget", { targetId, flatten: true });
  const pageCall = (method, params) => call(method, params, sessionId);
  const evaluate = async (fn, ...args) => {
    const response = await pageCall("Runtime.evaluate", {
      expression: `(${fn.toString()})(...${JSON.stringify(args)})`, awaitPromise: true, returnByValue: true,
    });
    if (response.exceptionDetails) throw new Error(JSON.stringify(response.exceptionDetails));
    return response.result.value;
  };
  const wait = async (fn, ...args) => {
    const until = Date.now() + 10000;
    while (Date.now() < until) {
      if (await evaluate(fn, ...args)) return;
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    throw new Error(`Condição não atendida: ${fn}`);
  };
  const fill = (selector, value) => evaluate((selector, value) => {
    const element = document.querySelector(selector);
    if (!element) throw new Error(`Campo ausente: ${selector}`);
    const prototype = element.tagName === "TEXTAREA" ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    Object.getOwnPropertyDescriptor(prototype, "value").set.call(element, value);
    element.dispatchEvent(new Event("input", { bubbles: true }));
  }, selector, value);
  const screenshot = async (ct, description) => {
    const filename = `${ct}.png`;
    const { data } = await pageCall("Page.captureScreenshot", { format: "png", captureBeyondViewport: true });
    await writeFile(join(output, filename), Buffer.from(data, "base64"));
    checks.push({ ct, resultado: "aprovado", verificacao: description, captura: filename });
    console.log(`${ct}: aprovado — ${description}`);
  };
  const login = async (username, password = "SenhaSomenteTesteFT69!") => {
    await fill('input[autocomplete="username"]', username);
    await fill('input[type="password"]', password);
    await evaluate(() => document.querySelector("form").requestSubmit());
  };
  await pageCall("Page.enable");
  await pageCall("Runtime.enable");
  await pageCall("Emulation.setDeviceMetricsOverride", { width: 1440, height: 1100, deviceScaleFactor: 1, mobile: false });
  await pageCall("Page.navigate", { url });
  await wait(() => !!document.querySelector('input[autocomplete="username"]'));
  for (const [ct, username] of [["CT-02", "gestor_ft69"], ["CT-14", "motorista_ft69"]]) {
    await login(username, "SenhaIncorreta!");
    await wait(() => document.querySelector('[role="alert"]')?.textContent.includes("Verifique usuário e senha")
      && document.querySelector('button[type="submit"]')?.disabled === false);
    assert.equal(await evaluate(() => sessionStorage.getItem("feneme-session")), null);
    await screenshot(ct, "Mensagem de credenciais inválidas e sessão não criada.");
  }
  await login("gestor_ft69");
  await wait(() => document.querySelector("h1")?.textContent === "Gerencie suas entregas");
  await wait(() => document.body.innerText.includes("Nenhuma entrega cadastrada"));
  await screenshot("CT-01", "Login do Gestor abre o painel de operações.");
  await screenshot("CT-16", "Gestor visualiza o estado vazio da lista.");
  await fill('input[placeholder="Ex.: Campina Grande - PB"]', "Campina Grande - PB");
  await evaluate(() => document.querySelector("form").requestSubmit());
  assert.equal(await evaluate(() => document.querySelector('input[placeholder="Ex.: João Pessoa - PB"]').validity.valueMissing), true);
  assert.equal(await evaluate(() => document.querySelectorAll(".delivery-card").length), 0);
  await screenshot("CT-04", "Campo Destino obrigatório impede cadastro incompleto na interface.");
  await fill('input[placeholder="Ex.: João Pessoa - PB"]', "João Pessoa - PB");
  await fill("textarea", "Alimentos refrigerados FT69");
  await evaluate(() => document.querySelector("form").requestSubmit());
  await wait(() => document.querySelectorAll(".delivery-card").length === 1);
  await screenshot("CT-03", "Cadastro válido exibe confirmação e entrega na lista.");
  await pageCall("Page.reload");
  await wait(() => document.querySelector(".delivery-card")?.textContent.includes("Alimentos refrigerados FT69"));
  await screenshot("CT-15", "Entrega permanece na consulta após recarregar a página.");
  assert.equal(await evaluate(() => [...document.querySelectorAll("select option")].some(o => o.textContent.includes("gestor_ft69"))), false);
  await screenshot("CT-17-interface", "Seletor disponibiliza somente Motoristas; rejeição HTTP 400 está evidenciada na suíte da API.");
  await evaluate(() => {
    const select = document.querySelector("select");
    const option = [...select.options].find(o => o.textContent.includes("motorista_ft69"));
    select.value = option.value;
    select.dispatchEvent(new Event("change", { bubbles: true }));
  });
  await evaluate(() => document.querySelector(".assign-form").requestSubmit());
  await wait(() => document.querySelector(".assigned-label")?.textContent.includes("motorista_ft69"));
  await pageCall("Page.reload");
  await wait(() => document.querySelector(".assigned-label")?.textContent.includes("motorista_ft69"));
  await screenshot("CT-05-gestor", "Motorista atribuído permanece após recarregar o painel do Gestor.");
  await evaluate(() => [...document.querySelectorAll("button")].find(b => b.textContent === "Sair").click());
  await wait(() => !!document.querySelector('input[autocomplete="username"]'));
  await login("motorista_ft69");
  await wait(() => document.querySelector("h1")?.textContent === "Olá, motorista_ft69");
  await wait(() => document.querySelector(".delivery-card")?.textContent.includes("Alimentos refrigerados FT69"));
  await screenshot("CT-13", "Login do Motorista abre sua área e consulta a entrega atribuída.");
  await screenshot("CT-05-motorista", "Entrega atribuída pelo Gestor está disponível ao Motorista responsável.");
  const hashes = {};
  for (const file of ["scripts/ft69_browser.mjs", "backend/verify_ft69_browser.py",
    "frontend/src/App.tsx", "frontend/src/api.ts", "frontend/src/components/MotoristaHome.tsx"]) {
    hashes[file] = createHash("sha256").update(await readFile(file)).digest("hex");
  }
  await writeFile(join(output, "FT69_browser_resultado.json"), JSON.stringify({
    inicio: started, fim: new Date().toISOString(), navegador: version.product,
    tipo: "conferência automatizada no Chrome headless; revisão humana manual pendente",
    verificacoes: checks, sha256_fontes: hashes,
  }, null, 2) + "\n");
  const lines = ["# FT-69 — conferência automatizada da interface", "",
    `Início (UTC): ${started}. Navegador: ${version.product}.`, "",
    "Servidor Django real, build React e PostgreSQL temporário. Contas e entrega são dados sintéticos de teste.", "",
    "| CT | Verificação aprovada | Captura |", "|---|---|---|"];
  for (const check of checks) {
    lines.push(`| ${check.ct} | ${check.verificacao} | [PNG](${check.captura}) |`);
  }
  lines.push("", "Onze verificações complementares; elas não representam onze CT novos. "
    + "O CT-17 tem rejeição da atribuição inválida comprovada na API; a interface impede a seleção do Gestor.", "",
    "[Log da interface](FT69_browser_resultado.txt), [dados e hashes](FT69_browser_resultado.json) "
    + "e [relatório principal dos dez CT e Q-01](FT69_relatorio.md).", "",
    "Revisão humana manual e aprovação do universo por PO/QA permanecem pendentes. "
    + "A automação não representa aceite formal.", "");
  await writeFile(join(output, "FT69_browser_relatorio.md"), lines.join("\n"));
  await call("Browser.close");
} catch (error) {
  console.error(error);
  process.exitCode = 1;
} finally {
  ws?.close();
  chrome.kill();
  // Perfil temporário isolado, fora do repositório; nunca usar o perfil pessoal.
}
