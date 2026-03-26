# -*- coding: utf-8 -*-
"""
Substitui localStorage por Supabase (banco de dados online compartilhado).
O percentual confirmado no index.html fica disponível para qualquer
dispositivo que abra tabela.html — secretaria, celular, outro computador.

Fallback automático: se Supabase não estiver configurado ou offline,
usa localStorage como cache local.
"""

SUPABASE_CDN = '  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>'

SUPABASE_BLOCK = """\
  // ══════════════════════════════════════════════════════════════
  // SUPABASE — banco de dados compartilhado
  // Preencha com as credenciais do seu projeto em supabase.com
  // ══════════════════════════════════════════════════════════════
  const SUPABASE_URL = 'https://SEU_PROJETO.supabase.co';  // ← edite
  const SUPABASE_KEY = 'SUA_ANON_KEY_AQUI';                // ← edite
  const _sb = (typeof supabase !== 'undefined' &&
               !SUPABASE_URL.includes('SEU_PROJETO'))
    ? supabase.createClient(SUPABASE_URL, SUPABASE_KEY)
    : null;

"""

# ============================================================
# 1. TABELA.HTML
# ============================================================
with open('tabela.html', encoding='utf-8') as f:
    t = f.read()
print(f"tabela.html lido: {len(t)} bytes")

# 1a. Adiciona CDN do Supabase no <head>
old_cdn_t = '  <script src="https://cdn.tailwindcss.com"></script>\n  <link'
new_cdn_t = (
    '  <script src="https://cdn.tailwindcss.com"></script>\n'
    + SUPABASE_CDN + '\n'
    + '  <link'
)
if old_cdn_t in t:
    t = t.replace(old_cdn_t, new_cdn_t)
    print("1a. CDN Supabase adicionado ao tabela.html")
else:
    print("ERRO: ancora CDN tabela.html nao encontrada!")

# 1b. Remove initState() e injeta constantes Supabase
#     (o estado inicial agora vem do Supabase no INIT async abaixo)
old_init_state = """    let filtroAtivo  = 'todos';

    (function initState() {
      try {
        const saved = localStorage.getItem('cpReajuste');
        if (saved) {
          const obj   = JSON.parse(saved);
          reajustePct  = (typeof obj.pct === 'number') ? obj.pct : 5;
          reajusteData = obj.data ? new Date(obj.data) : null;
        }
      } catch (e) { /* usa padrão 5% */ }
    })();"""

new_init_state = (
    "    let filtroAtivo  = 'todos';\n\n"
    + "    // ── Supabase client ──────────────────────────────────────\n"
    + "    const SUPABASE_URL = 'https://SEU_PROJETO.supabase.co'; // ← edite\n"
    + "    const SUPABASE_KEY = 'SUA_ANON_KEY_AQUI';               // ← edite\n"
    + "    const _sb = (typeof supabase !== 'undefined' &&\n"
    + "                 !SUPABASE_URL.includes('SEU_PROJETO'))\n"
    + "      ? supabase.createClient(SUPABASE_URL, SUPABASE_KEY)\n"
    + "      : null;"
)

if old_init_state in t:
    t = t.replace(old_init_state, new_init_state)
    print("1b. initState() substituido por cliente Supabase")
else:
    print("ERRO: initState block nao encontrado!")

# 1c. Substitui INIT (updateDisplay) por IIFE async com Supabase
old_init_t = """    // INIT
    // ============================================================
    updateDisplay();"""

new_init_t = """\
    // ── INIT — carrega do Supabase (ou localStorage como fallback) ──
    (async function () {
      // 1. Mostra imediatamente o cache local (sem latência)
      try {
        const cache = localStorage.getItem('cpReajuste');
        if (cache) {
          const obj = JSON.parse(cache);
          if (typeof obj.pct === 'number') {
            reajustePct  = obj.pct;
            reajusteData = obj.data ? new Date(obj.data) : null;
          }
        }
      } catch (_) {}
      updateDisplay(); // exibe enquanto busca no servidor

      // 2. Busca a versão mais recente no Supabase (fonte de verdade)
      if (_sb) {
        const sync = document.getElementById('syncStatus');
        if (sync) sync.classList.remove('hidden');
        try {
          const { data, error } = await _sb
            .from('config')
            .select('value')
            .eq('key', 'reajuste')
            .maybeSingle();
          if (!error && data?.value?.pct != null) {
            reajustePct  = data.value.pct;
            reajusteData = data.value.saved_at
              ? new Date(data.value.saved_at)
              : null;
            // Atualiza cache local
            localStorage.setItem('cpReajuste', JSON.stringify({
              pct: reajustePct,
              data: data.value.saved_at
            }));
            updateDisplay(); // atualiza com dados do servidor
          }
        } catch (e) { /* mantém cache local */ }
        if (sync) sync.classList.add('hidden');
      }
    })();"""

if old_init_t in t:
    t = t.replace(old_init_t, new_init_t)
    print("1c. INIT substituido por carregamento async do Supabase")
else:
    print("ERRO: bloco INIT tabela.html nao encontrado!")

# 1d. Adiciona indicador de sincronização no badge do header
old_badge_wrap = ('      <div class="flex items-center gap-1.5 bg-emerald-950/60 border border-emerald-700/40\n'
                  '                  rounded-lg px-3 py-1.5 shrink-0">')
new_badge_wrap = ('      <div class="flex items-center gap-1.5 bg-emerald-950/60 border border-emerald-700/40\n'
                  '                  rounded-lg px-3 py-1.5 shrink-0">\n'
                  '        <span id="syncStatus" class="hidden text-yellow-400 text-xs animate-pulse">⟳</span>')

if old_badge_wrap in t:
    t = t.replace(old_badge_wrap, new_badge_wrap)
    print("1d. Indicador de sincronizacao adicionado ao header")
else:
    print("AVISO: badge wrap nao encontrado (nao critico)")

with open('tabela.html', 'w', encoding='utf-8') as f:
    f.write(t)
print(f"tabela.html salvo: {len(t)} bytes")


# ============================================================
# 2. INDEX.HTML
# ============================================================
with open('index.html', encoding='utf-8') as f:
    h = f.read()
print(f"\nindex.html lido: {len(h)} bytes")

# 2a. Adiciona CDN Supabase (após chart.js)
old_chartjs = '  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>'
new_chartjs = (
    '  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>\n'
    + SUPABASE_CDN
)
if old_chartjs in h:
    h = h.replace(old_chartjs, new_chartjs)
    print("2a. CDN Supabase adicionado ao index.html")
else:
    print("ERRO: ancora chart.js nao encontrada!")

# 2b. Injeta constantes Supabase + cliente no início do <script>
old_script_open = '<script>\n  // ============================================================\n  // DADOS REAIS'
new_script_open = ('<script>\n'
                   + SUPABASE_BLOCK
                   + '  // ============================================================\n'
                   + '  // DADOS REAIS')
if old_script_open in h:
    h = h.replace(old_script_open, new_script_open)
    print("2b. Constantes Supabase injetadas no inicio do script")
else:
    print("ERRO: abertura do script nao encontrada!")

# 2c. Substitui salvarReajuste() + updateSavedBadge() por versões async
old_save_block = """function salvarReajuste() {
    const obj = { pct: simPct, data: new Date().toISOString() };
    localStorage.setItem('cpReajuste', JSON.stringify(obj));
    updateSavedBadge();
    const msg = document.getElementById('savedMsg');
    if (msg) {
      msg.classList.remove('hidden');
      setTimeout(() => msg.classList.add('hidden'), 3500);
    }
  }

  function updateSavedBadge() {
    const badge = document.getElementById('savedPctBadge');
    if (!badge) return;
    try {
      const saved = localStorage.getItem('cpReajuste');
      if (saved) {
        const obj = JSON.parse(saved);
        const d   = new Date(obj.data);
        badge.textContent = 'Salvo: ' + obj.pct.toFixed(1).replace('.', ',') +
          '% em ' + d.toLocaleDateString('pt-BR');
      } else {
        badge.textContent = 'Nenhum salvo ainda';
      }
    } catch (e) {}
  }"""

new_save_block = """\
async function salvarReajuste() {
    const now = new Date().toISOString();
    const payload = { pct: simPct, saved_at: now };
    let sbOk = false;

    // Salva no Supabase (banco compartilhado)
    if (_sb) {
      try {
        const { error } = await _sb.from('config').upsert({
          key: 'reajuste',
          value: payload,
          updated_at: now
        });
        if (!error) sbOk = true;
      } catch (e) { /* fallback local */ }
    }

    // Sempre atualiza o cache local
    localStorage.setItem('cpReajuste', JSON.stringify({ pct: simPct, data: now }));
    updateSavedBadge();

    const msg = document.getElementById('savedMsg');
    if (msg) {
      msg.textContent = sbOk
        ? '✓ Salvo no banco! A secretaria já pode consultar a tabela.'
        : (_sb
           ? '⚠ Erro ao salvar no banco. Verifique a conexão.'
           : '✓ Salvo localmente. Configure o Supabase para compartilhar.');
      msg.classList.remove('hidden');
      setTimeout(() => msg.classList.add('hidden'), 4500);
    }
  }

  function updateSavedBadge() {
    const badge = document.getElementById('savedPctBadge');
    if (!badge) return;
    try {
      const saved = localStorage.getItem('cpReajuste');
      if (saved) {
        const obj   = JSON.parse(saved);
        const d     = new Date(obj.data);
        const fonte = _sb ? ' ☁' : ' (local)';
        badge.textContent = 'Salvo: ' + obj.pct.toFixed(1).replace('.', ',') +
          '% em ' + d.toLocaleDateString('pt-BR') + fonte;
      } else {
        badge.textContent = _sb ? 'Nenhum salvo no banco' : 'Nenhum salvo ainda';
      }
    } catch (e) {}
  }"""

if old_save_block in h:
    h = h.replace(old_save_block, new_save_block)
    print("2c. salvarReajuste() e updateSavedBadge() atualizados para Supabase")
else:
    print("ERRO: bloco salvarReajuste nao encontrado!")

# 2d. Substitui init IIFE por versão async com Supabase
old_init_h = """// Inicializar simulador — restaura último percentual salvo (localStorage)
  (function () {
    let initPct = 5;
    try {
      const saved = localStorage.getItem('cpReajuste');
      if (saved) {
        const obj = JSON.parse(saved);
        if (typeof obj.pct === 'number') initPct = obj.pct;
      }
    } catch (e) { /* usa padrão 5% */ }
    const slider = document.getElementById('sliderSim');
    const input  = document.getElementById('inputSimNum');
    if (slider) slider.value = Math.min(initPct, 30);
    if (input)  input.value  = initPct;
    atualizarSimulador(initPct);
  })();"""

new_init_h = """\
// Inicializar simulador — busca percentual do Supabase ou localStorage
  (async function () {
    let initPct = 5;

    // 1. Tenta buscar do Supabase (fonte de verdade compartilhada)
    if (_sb) {
      try {
        const { data, error } = await _sb
          .from('config')
          .select('value')
          .eq('key', 'reajuste')
          .maybeSingle();
        if (!error && data?.value?.pct != null) {
          initPct = data.value.pct;
          // Sincroniza cache local
          localStorage.setItem('cpReajuste', JSON.stringify({
            pct: initPct,
            data: data.value.saved_at || new Date().toISOString()
          }));
        }
      } catch (e) { /* fallback abaixo */ }
    }

    // 2. Fallback: cache localStorage
    if (initPct === 5) {
      try {
        const saved = localStorage.getItem('cpReajuste');
        if (saved) {
          const obj = JSON.parse(saved);
          if (typeof obj.pct === 'number') initPct = obj.pct;
        }
      } catch (e) {}
    }

    const slider = document.getElementById('sliderSim');
    const input  = document.getElementById('inputSimNum');
    if (slider) slider.value = Math.min(initPct, 30);
    if (input)  input.value  = initPct;
    atualizarSimulador(initPct);
    updateSavedBadge();
  })();"""

if old_init_h in h:
    h = h.replace(old_init_h, new_init_h)
    print("2d. Init do simulador atualizado para buscar do Supabase")
else:
    print("ERRO: init IIFE nao encontrado!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print(f"index.html salvo: {len(h)} bytes")


# ============================================================
# INSTRUÇÕES DE CONFIGURAÇÃO DO SUPABASE
# ============================================================
print("""
══════════════════════════════════════════════════════════════
CONFIGURAÇÃO SUPABASE — execute os passos abaixo
══════════════════════════════════════════════════════════════

1. Acesse https://supabase.com e crie uma conta gratuita
2. Crie um novo projeto (ex: "clinica-pelegrino")
3. Vá em SQL Editor e execute o SQL abaixo:

───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.config (
  key        TEXT PRIMARY KEY,
  value      JSONB NOT NULL DEFAULT '{}',
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.config ENABLE ROW LEVEL SECURITY;

CREATE POLICY "leitura_publica" ON public.config
  FOR SELECT USING (true);

CREATE POLICY "escrita_interna" ON public.config
  FOR ALL USING (true) WITH CHECK (true);

INSERT INTO public.config (key, value)
  VALUES ('reajuste', '{"pct": 5.0, "saved_at": null}')
  ON CONFLICT (key) DO NOTHING;
───────────────────────────────────────────

4. Vá em Project Settings > API e copie:
   - Project URL (https://xxxx.supabase.co)
   - anon public key (eyJhbGci...)

5. Edite os dois arquivos:
   - index.html:   procure SUPABASE_URL e SUPABASE_KEY perto do topo do <script>
   - tabela.html:  procure SUPABASE_URL e SUPABASE_KEY no bloco // Supabase client

6. Substitua os placeholders pelas suas credenciais reais.

Pronto! O percentual confirmado em index.html ficara disponivel
para qualquer dispositivo que abra tabela.html.
══════════════════════════════════════════════════════════════
""")
