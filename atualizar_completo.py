
# atualizar_completo.py — Adiciona visão completa de despesas com filtros

with open("dashboard.html", "r", encoding="utf-8") as f:
    html = f.read()
print(f"Lido: {len(html)} bytes")

# ══════════════════════════════════════════════════════════════════════════════
# 1. Atualizar aviso da Seção 1 (Resumo Executivo)
# ══════════════════════════════════════════════════════════════════════════════
OLD_AVISO = '''          <p class="text-amber-300 text-sm font-semibold">Análise com dados comparáveis</p>
            <p class="text-amber-200/70 text-xs mt-0.5 leading-relaxed">
              Apenas categorias com dados nos <strong>4 meses</strong> (Jan/25, Fev/25, Jan/26, Fev/26) foram incluídas.
              Excluídos por política: Juros de Cartão, Laboratórios, Materiais Odontológicos, Porcentagens (comissões), Taxas e Despesas Diversas, Marketing, Manutenção de Equipamentos e Infraestrutura.
            </p>'''
NEW_AVISO = '''          <p class="text-amber-300 text-sm font-semibold">Metodologia da análise de precificação</p>
            <p class="text-amber-200/70 text-xs mt-0.5 leading-relaxed">
              Para o cálculo do reajuste, foram usadas <strong>9 categorias fixas comparáveis</strong> (Jan+Fev 2025×2026).
              Custos variáveis (Laboratórios, Materiais, Porcentagens) são excluídos da precificação por variarem com o volume de procedimentos.
              Veja os dados completos de todas as 27 categorias na seção <a href="#excluidos" class="text-amber-300 underline hover:text-white">Despesas Completas</a>.
            </p>'''

if OLD_AVISO in html:
    html = html.replace(OLD_AVISO, NEW_AVISO)
    print("1. Aviso Seção 1 atualizado")
else:
    print("1. AVISO: texto não encontrado exatamente")

# ══════════════════════════════════════════════════════════════════════════════
# 2. Atualizar cabeçalho da Seção 3 (Detalhamento)
# ══════════════════════════════════════════════════════════════════════════════
OLD_DET = '            <p class="text-white font-semibold text-sm">9 categorias com dados em todos os 4 meses analisados</p>'
NEW_DET = '            <p class="text-white font-semibold text-sm">9 categorias fixas comparáveis — base da análise de precificação</p>'
if OLD_DET in html:
    html = html.replace(OLD_DET, NEW_DET)
    print("2. Cabeçalho Seção 3 atualizado")
else:
    print("2. AVISO: cabeçalho não encontrado")

# ══════════════════════════════════════════════════════════════════════════════
# 3. Substituir Seção 4 (Excluídos → Despesas Completas)
# ══════════════════════════════════════════════════════════════════════════════
S4_START = '      <!-- ============================================================\n           SE\u00c7\u00c3O 4 \u2013 EXCLU\u00cdDOS\n      ============================================================ -->'
S4_END   = '\n\n      <!-- ============================================================\n           SE\u00c7\u00c3O 5 \u2013 METODOLOGIA'

idx_s4 = html.find(S4_START)
idx_s5 = html.find(S4_END, idx_s4 if idx_s4 >= 0 else 0)
print(f"  Seção 4: start={idx_s4}, end={idx_s5}")

NEW_S4 = '''      <!-- ============================================================
           SEÇÃO 4 – DESPESAS COMPLETAS JAN-MAR 2025/2026
      ============================================================ -->
      <section id="excluidos">
        <h2 class="text-slate-300 text-xs font-bold uppercase tracking-widest mb-4">Despesas Completas — Jan-Mar 2025/2026 (27 categorias)</h2>

        <!-- KPI totais -->
        <div class="grid grid-cols-3 gap-4 mb-5">
          <div class="bg-slate-800/50 rounded-xl p-4 border border-slate-700/40">
            <p class="text-slate-400 text-xs mb-1">Total Despesas Q1 2025</p>
            <p class="text-red-300 text-2xl font-black">R$&nbsp;71.092</p>
            <p class="text-slate-500 text-[10px] mt-1">Jan+Fev+Mar 2025</p>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 border border-red-500/30">
            <p class="text-slate-400 text-xs mb-1">Total Despesas Q1 2026</p>
            <p class="text-red-400 text-2xl font-black">R$&nbsp;76.270</p>
            <p class="text-red-400 text-[10px] mt-1">+7,3% vs Q1 2025</p>
          </div>
          <div class="bg-amber-500/10 rounded-xl p-4 border border-amber-500/20">
            <p class="text-slate-400 text-xs mb-1">Aumento das Despesas</p>
            <p class="text-amber-400 text-2xl font-black">+R$&nbsp;5.178</p>
            <p class="text-slate-500 text-[10px] mt-1">Acima do IPCA 2025 (4,83%)</p>
          </div>
        </div>

        <!-- Filtros -->
        <div class="flex gap-2 mb-4 flex-wrap" id="filtrosDespesas">
          <button onclick="filtrarDespesas('todas')"
            class="btn-desp active-desp px-3 py-1.5 text-xs font-semibold rounded-full bg-[#0EA5E9] text-white">
            Todas (27)
          </button>
          <button onclick="filtrarDespesas('Fixo')"
            class="btn-desp px-3 py-1.5 text-xs font-semibold rounded-full bg-slate-700 text-slate-300 hover:bg-slate-600">
            Fixas
          </button>
          <button onclick="filtrarDespesas('Pessoal')"
            class="btn-desp px-3 py-1.5 text-xs font-semibold rounded-full bg-slate-700 text-slate-300 hover:bg-slate-600">
            Pessoal
          </button>
          <button onclick="filtrarDespesas('Operacional')"
            class="btn-desp px-3 py-1.5 text-xs font-semibold rounded-full bg-slate-700 text-slate-300 hover:bg-slate-600">
            Operacional
          </button>
          <button onclick="filtrarDespesas('Variável')"
            class="btn-desp px-3 py-1.5 text-xs font-semibold rounded-full bg-slate-700 text-slate-300 hover:bg-slate-600">
            Variáveis
          </button>
          <button onclick="filtrarDespesas('precif')"
            class="btn-desp px-3 py-1.5 text-xs font-semibold rounded-full bg-slate-700 text-slate-300 hover:bg-slate-600">
            &#128274; Precificação (9)
          </button>
        </div>

        <!-- Tabela completa -->
        <div class="bg-slate-800/50 rounded-2xl border border-slate-700/40 overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-xs">
              <thead>
                <tr class="bg-slate-900/70 text-slate-400 font-semibold uppercase tracking-wider text-[10px]">
                  <th class="text-left px-4 py-3">Categoria</th>
                  <th class="text-center px-2 py-3">Tipo</th>
                  <th class="text-right px-3 py-3 bg-slate-800/40">Jan/25</th>
                  <th class="text-right px-3 py-3 bg-slate-800/40">Fev/25</th>
                  <th class="text-right px-3 py-3 bg-slate-800/40">Mar/25</th>
                  <th class="text-right px-3 py-3 bg-sky-900/20" style="color:#0EA5E9">Q1 2025</th>
                  <th class="text-right px-3 py-3">Jan/26</th>
                  <th class="text-right px-3 py-3">Fev/26</th>
                  <th class="text-right px-3 py-3">Mar/26</th>
                  <th class="text-right px-3 py-3 bg-sky-900/30" style="color:#38bdf8">Q1 2026</th>
                  <th class="text-right px-3 py-3">Var%</th>
                </tr>
              </thead>
              <tbody id="tabelaCompleta"></tbody>
              <tfoot>
                <tr class="bg-slate-900 font-bold text-white border-t-2 border-slate-600 text-[11px]" id="footerCompleta">
                  <td class="px-4 py-3">TOTAL GERAL</td>
                  <td></td>
                  <td class="text-right px-3 py-3 bg-slate-800/40" id="ft-j25">—</td>
                  <td class="text-right px-3 py-3 bg-slate-800/40" id="ft-f25">—</td>
                  <td class="text-right px-3 py-3 bg-slate-800/40" id="ft-m25">—</td>
                  <td class="text-right px-3 py-3 bg-sky-900/20 text-[#0EA5E9]" id="ft-t25">—</td>
                  <td class="text-right px-3 py-3" id="ft-j26">—</td>
                  <td class="text-right px-3 py-3" id="ft-f26">—</td>
                  <td class="text-right px-3 py-3" id="ft-m26">—</td>
                  <td class="text-right px-3 py-3 bg-sky-900/30 text-[#38bdf8]" id="ft-t26">—</td>
                  <td class="text-right px-3 py-3" id="ft-var">—</td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
        <p class="text-slate-500 text-[10px] mt-2">
          &#128274; Categorias marcadas "Precificação" são as 9 usadas na análise de reajuste. Mar/2025 e Mar/2026 são dados parciais (~25/03 de cada ano).
        </p>
      </section>

      <!-- ============================================================
           SEÇÃO 5 – METODOLOGIA'''

if idx_s4 >= 0 and idx_s5 >= 0:
    html = html[:idx_s4] + NEW_S4 + html[idx_s5 + len(S4_END):]
    print(f"3. Seção 4 substituída. Novo tamanho: {len(html)}")
else:
    print("3. ERRO: seção 4 não encontrada")

# ══════════════════════════════════════════════════════════════════════════════
# 4. CSS para btn-desp
# ══════════════════════════════════════════════════════════════════════════════
OLD_CSS_END = '    .col-sim     { background: rgba(245,158,11,0.08); }'
NEW_CSS_END = '''    .col-sim     { background: rgba(245,158,11,0.08); }
    /* Filtros de despesas completas */
    .btn-desp { transition: all 0.15s; }
    .btn-desp.active-desp { background: #0EA5E9 !important; color: white !important; }
    .tipo-fixo       { background: rgba(14,165,233,0.15); color: #38bdf8; }
    .tipo-pessoal    { background: rgba(168,85,247,0.15); color: #c084fc; }
    .tipo-operac     { background: rgba(34,197,94,0.15);  color: #4ade80; }
    .tipo-variavel   { background: rgba(239,68,68,0.15);  color: #f87171; }
    .tipo-outros     { background: rgba(148,163,184,0.1); color: #94a3b8; }
    .precif-badge    { background: rgba(14,165,233,0.2);  color: #0EA5E9; font-size:10px; padding:1px 5px; border-radius:4px; }'''

if OLD_CSS_END in html:
    html = html.replace(OLD_CSS_END, NEW_CSS_END)
    print("4. CSS adicionado")
else:
    print("4. AVISO: marcador CSS não encontrado")

# ══════════════════════════════════════════════════════════════════════════════
# 5. JS: dados DADOS_COMPLETOS e funções
# ══════════════════════════════════════════════════════════════════════════════
JS_INSERT_BEFORE = '  // ============================================================\n  // TABELA DE PREÇOS\n  // ============================================================'

JS_NEW = '''  // ============================================================
  // DADOS COMPLETOS — 27 CATEGORIAS (3 meses cada ano)
  // ============================================================
  const PRECIF_CATS = new Set([
    "Aluguel","Contabilidade","Empréstimo Jurídico","Telefone",
    "Codental","CHB Ambiental","Imposto Jurídico","Desp. Funcionárias","Mat. Conserv./Limpeza"
  ]);

  const DADOS_COMPLETOS = [
    { cat: "Aluguel",                    tipo: "Fixo",        j25:3050.68, f25:3006.00, m25:3006.00, j26:3007.72, f26:2969.58, m26:2069.58 },
    { cat: "Água",                       tipo: "Operacional", j25:  88.96, f25:   0.00, m25: 241.78, j26: 135.68, f26: 136.51, m26: 136.73 },
    { cat: "CHB Ambiental",              tipo: "Fixo",        j25:  95.65, f25:  93.75, m25:  93.75, j26: 101.17, f26: 101.27, m26: 101.27 },
    { cat: "Codental",                   tipo: "Fixo",        j25: 160.90, f25: 114.90, m25: 114.90, j26: 128.90, f26: 128.90, m26: 128.90 },
    { cat: "Contabilidade",              tipo: "Fixo",        j25:1214.40, f25:1214.00, m25:   0.00, j26:1214.40, f26:1296.86, m26:   0.00 },
    { cat: "CRO",                        tipo: "Fixo",        j25:   0.00, f25:   0.00, m25:   0.00, j26: 238.67, f26: 242.92, m26:   0.00 },
    { cat: "Cartões de Crédito",         tipo: "Variável",    j25:   0.00, f25:   0.00, m25:   0.00, j26:   0.00, f26:   0.00, m26: 688.21 },
    { cat: "Desp. Funcionárias",         tipo: "Pessoal",     j25:5440.59, f25:5616.92, m25:5148.56, j26:6250.16, f26:5869.27, m26:5753.27 },
    { cat: "Empréstimo Jurídico",        tipo: "Fixo",        j25:1854.00, f25:1854.00, m25:1854.00, j26:1766.00, f26:1766.00, m26:   0.00 },
    { cat: "Energia Elétrica",           tipo: "Operacional", j25:   0.00, f25:1237.84, m25: 234.05, j26:1343.16, f26:1032.64, m26:   0.00 },
    { cat: "Escritório/Papelaria",       tipo: "Operacional", j25:   0.00, f25:  46.48, m25:  80.00, j26:  40.00, f26:   0.00, m26:   0.00 },
    { cat: "Imposto Fiscal",             tipo: "Fixo",        j25:   0.00, f25:   0.00, m25:   0.00, j26: 189.94, f26:   0.00, m26:   0.00 },
    { cat: "Imposto Jurídico",           tipo: "Pessoal",     j25: 583.49, f25: 708.05, m25: 888.67, j26:1249.95, f26:1119.07, m26: 608.52 },
    { cat: "Infraestrutura",             tipo: "Variável",    j25:   0.00, f25: 194.00, m25: 336.90, j26: 120.00, f26:   0.00, m26:   0.00 },
    { cat: "Internet",                   tipo: "Fixo",        j25: 168.00, f25: 139.28, m25: 306.46, j26:   0.00, f26: 296.75, m26: 290.00 },
    { cat: "ISS",                        tipo: "Fixo",        j25: 168.79, f25: 168.79, m25:   0.00, j26:   0.00, f26: 191.04, m26:   0.00 },
    { cat: "Juros dos Cartões",          tipo: "Variável",    j25: 800.27, f25:2823.61, m25: 331.14, j26: 825.60, f26:1210.51, m26:   0.00 },
    { cat: "Laboratórios",               tipo: "Variável",    j25:1300.00, f25:2940.00, m25: 500.00, j26:1500.00, f26:3150.00, m26:2402.00 },
    { cat: "Manutenção Equipamentos",    tipo: "Variável",    j25:   0.00, f25:   0.00, m25: 430.00, j26: 380.00, f26: 390.00, m26: 220.00 },
    { cat: "Marketing/Publicidade",      tipo: "Variável",    j25:   0.00, f25:   0.00, m25:   0.00, j26: 750.00, f26:   0.00, m26: 400.00 },
    { cat: "Mat. Conserv./Limpeza",      tipo: "Operacional", j25:  37.15, f25:  96.30, m25:   0.00, j26: 239.58, f26: 101.07, m26:  82.62 },
    { cat: "Materiais Odontológicos",    tipo: "Variável",    j25:1407.13, f25:2007.63, m25: 951.74, j26:1715.56, f26:2737.48, m26:1546.15 },
    { cat: "NF Prefeitura",              tipo: "Fixo",        j25:   0.00, f25:   0.00, m25:   0.00, j26:  40.87, f26:  79.80, m26:  79.80 },
    { cat: "Porcentagem",                tipo: "Pessoal",     j25:4812.76, f25:6694.24, m25:3361.95, j26:4427.00, f26:5242.00, m26:7306.09 },
    { cat: "SSI / SESI",                 tipo: "Fixo",        j25: 286.51, f25:   0.00, m25:   0.00, j26:   0.00, f26:   0.00, m26:   0.00 },
    { cat: "Taxas e Desp. Diversas",     tipo: "Variável",    j25:1932.35, f25: 420.18, m25:   0.00, j26:   0.00, f26: 238.67, m26: 138.67 },
    { cat: "Telefone",                   tipo: "Fixo",        j25: 182.09, f25: 211.74, m25:  40.84, j26: 296.45, f26:  57.50, m26:   0.00 },
  ];

  // Cores por tipo
  const COR_TIPO = {
    'Fixo':        { bg: 'tipo-fixo',     label: 'Fixo' },
    'Pessoal':     { bg: 'tipo-pessoal',  label: 'Pessoal' },
    'Operacional': { bg: 'tipo-operac',   label: 'Operac.' },
    'Variável':    { bg: 'tipo-variavel', label: 'Variável' },
  };

  let filtroDespAtivo = 'todas';

  function filtrarDespesas(filtro) {
    filtroDespAtivo = filtro;
    document.querySelectorAll('.btn-desp').forEach(b => {
      b.classList.remove('active-desp', 'bg-[#0EA5E9]', 'text-white');
      b.classList.add('bg-slate-700', 'text-slate-300');
    });
    event.target.classList.add('active-desp');
    event.target.classList.remove('bg-slate-700', 'text-slate-300');
    renderTabelaCompleta(filtro);
  }

  function renderTabelaCompleta(filtro) {
    const tb = document.getElementById('tabelaCompleta');
    if (!tb) return;
    tb.innerHTML = '';

    const lista = filtro === 'todas'  ? DADOS_COMPLETOS
                : filtro === 'precif' ? DADOS_COMPLETOS.filter(d => PRECIF_CATS.has(d.cat))
                : DADOS_COMPLETOS.filter(d => d.tipo === filtro);

    let sj25=0, sf25=0, sm25=0, sj26=0, sf26=0, sm26=0;

    lista.forEach((d, i) => {
      const t25 = d.j25 + d.f25 + d.m25;
      const t26 = d.j26 + d.f26 + d.m26;
      const varPct = t25 > 0 ? (t26/t25 - 1) * 100 : null;
      const isPrecif = PRECIF_CATS.has(d.cat);
      const corTipo = COR_TIPO[d.tipo] || { bg: 'tipo-outros', label: d.tipo };
      const isPos = varPct !== null && varPct > 0;
      const rowBg = i % 2 === 0 ? 'bg-slate-800/20' : 'bg-transparent';

      sj25+=d.j25; sf25+=d.f25; sm25+=d.m25;
      sj26+=d.j26; sf26+=d.f26; sm26+=d.m26;

      const varStr = varPct === null ? '—'
                   : (isPos ? '<span class="text-red-400 font-semibold">+' + varPct.toFixed(1) + '%</span>'
                             : '<span class="text-emerald-400 font-semibold">' + varPct.toFixed(1) + '%</span>');

      tb.innerHTML += `<tr class="${rowBg} hover:bg-slate-700/20 border-b border-slate-700/20 text-xs">
        <td class="px-4 py-2 text-slate-200 font-medium whitespace-nowrap">
          ${d.cat}${isPrecif ? ' <span class="precif-badge">&#128274;</span>' : ''}
        </td>
        <td class="text-center px-2 py-2"><span class="${corTipo.bg} text-[10px] font-semibold px-1.5 py-0.5 rounded">${corTipo.label}</span></td>
        <td class="text-right px-3 py-2 bg-slate-800/30 text-slate-400">${d.j25 ? brl(d.j25) : '<span class="text-slate-600">—</span>'}</td>
        <td class="text-right px-3 py-2 bg-slate-800/30 text-slate-400">${d.f25 ? brl(d.f25) : '<span class="text-slate-600">—</span>'}</td>
        <td class="text-right px-3 py-2 bg-slate-800/30 text-slate-400">${d.m25 ? brl(d.m25) : '<span class="text-slate-600">—</span>'}</td>
        <td class="text-right px-3 py-2 bg-sky-900/20 text-[#0EA5E9] font-bold">${brl(t25)}</td>
        <td class="text-right px-3 py-2 text-slate-300">${d.j26 ? brl(d.j26) : '<span class="text-slate-600">—</span>'}</td>
        <td class="text-right px-3 py-2 text-slate-300">${d.f26 ? brl(d.f26) : '<span class="text-slate-600">—</span>'}</td>
        <td class="text-right px-3 py-2 text-slate-300">${d.m26 ? brl(d.m26) : '<span class="text-slate-600">—</span>'}</td>
        <td class="text-right px-3 py-2 bg-sky-900/30 text-[#38bdf8] font-bold">${brl(t26)}</td>
        <td class="text-right px-3 py-2">${varStr}</td>
      </tr>`;
    });

    // Totais no footer
    const st25 = sj25+sf25+sm25, st26 = sj26+sf26+sm26;
    const svPct = st25 > 0 ? (st26/st25-1)*100 : 0;
    const svStr = svPct > 0 ? `<span class="text-red-400">+${svPct.toFixed(1)}%</span>`
                             : `<span class="text-emerald-400">${svPct.toFixed(1)}%</span>`;
    const set = (id, v) => { const el = document.getElementById(id); if(el) el.innerHTML = v; };
    set('ft-j25', brl(sj25)); set('ft-f25', brl(sf25)); set('ft-m25', brl(sm25));
    set('ft-t25', brl(st25));
    set('ft-j26', brl(sj26)); set('ft-f26', brl(sf26)); set('ft-m26', brl(sm26));
    set('ft-t26', brl(st26));
    set('ft-var', svStr);
  }

  renderTabelaCompleta('todas');

  // ============================================================
  // TABELA DE PREÇOS
  // ============================================================'''

if JS_INSERT_BEFORE in html:
    html = html.replace(JS_INSERT_BEFORE, JS_NEW)
    print("5. Dados e funções JS inseridos")
else:
    print("5. ERRO: marcador JS não encontrado")

# ══════════════════════════════════════════════════════════════════════════════
# 6. Sidebar: adicionar link para "Despesas Completas"
# ══════════════════════════════════════════════════════════════════════════════
OLD_EXCL_LINK = '      <a href="#excluidos" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>&#128683;</span> Excluídos\n      </a>'
NEW_EXCL_LINK = '      <a href="#excluidos" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>&#128202;</span> Desp. Completas\n      </a>'

# Try with the actual HTML emoji characters
if OLD_EXCL_LINK in html:
    html = html.replace(OLD_EXCL_LINK, NEW_EXCL_LINK)
    print("6. Link sidebar atualizado")
else:
    # Try finding the excluidos link more broadly
    old2 = 'href="#excluidos"'
    idx = html.find(old2)
    if idx >= 0:
        # Find the entire <a> tag
        start_a = html.rfind('<a ', 0, idx)
        end_a = html.find('</a>', idx) + 4
        old_block = html[start_a:end_a]
        # Check what span text it has
        new_block = old_block.replace('🚫', '📊').replace('Excluídos', 'Desp. Completas')
        html = html[:start_a] + new_block + html[end_a:]
        print(f"6. Link sidebar atualizado (método alternativo)")
    else:
        print("6. AVISO: link excluidos não encontrado")

# ══════════════════════════════════════════════════════════════════════════════
# 7. Gravar
# ══════════════════════════════════════════════════════════════════════════════
with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"\ndashboard.html salvo: {len(html)} bytes")
