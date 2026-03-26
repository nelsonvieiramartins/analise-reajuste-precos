# -*- coding: utf-8 -*-
"""
Atualiza index.html para incluir dados de março em todas as seções:
  - DADOS array (9 cat comparáveis): adiciona mar25/mar26, corrige j26 Funcionárias
  - forEach: recomputa avg25/avg26 com meses disponíveis
  - Tabela detalhamento Seção 3: adiciona colunas Mar/25 e Mar/26*
  - KPI cards Seção 1: atualiza valores (média mensal Q1)
  - Chart 1: usa avg25/avg26, subtítulo Q1
  - Chart 3: adiciona barras Mar/25* e Mar/26*
"""

with open('index.html', encoding='utf-8') as f:
    html = f.read()

original_size = len(html)
print(f"Lido: {original_size} bytes")

# ============================================================
# 1. SUBSTITUIR DADOS ARRAY (9 categorias comparáveis)
# ============================================================
old_dados = """  const DADOS = [
    { cat: "Aluguel",                    j25: 3050.68, f25: 3006.00, j26: 3007.72, f26: 2969.58 },
    { cat: "Contabilidade",              j25: 1214.40, f25: 1214.00, j26: 1214.40, f26: 1296.86 },
    { cat: "Empr\u00e9stimo Jur\u00eddico",        j25: 1854.00, f25: 1854.00, j26: 1766.00, f26: 1766.00 },
    { cat: "Telefone",                   j25:  182.09, f25:  211.74, j26:  296.45, f26:   57.50 },
    { cat: "Codental (Sistema)",         j25:  160.90, f25:  114.90, j26:  128.90, f26:  128.90 },
    { cat: "CHB Ambiental",              j25:   95.65, f25:   93.75, j26:  101.17, f26:  101.27 },
    { cat: "Imposto Jur\u00eddico",           j25:  583.49, f25:  708.05, j26: 1249.95, f26: 1119.07 },
    { cat: "Desp. Funcion\u00e1rias",         j25: 5440.59, f25: 5616.92, j26: 4050.16, f26: 5869.27 },
    { cat: "Material Conserv./Limpeza",  j25:   37.15, f25:   96.30, j26:  239.58, f26:  101.07 },
  ];"""

new_dados = """  // DADOS: 9 categorias comparáveis — inclui Jan+Fev+Mar (Mar* = parcial, mês não fechado)
  const DADOS = [
    { cat: "Aluguel",                    j25: 3050.68, f25: 3006.00, mar25: 3006.00, j26: 3007.72, f26: 2969.58, mar26: 2069.58 },
    { cat: "Contabilidade",              j25: 1214.40, f25: 1214.00, mar25:    0.00, j26: 1214.40, f26: 1296.86, mar26:    0.00 },
    { cat: "Empr\u00e9stimo Jur\u00eddico",        j25: 1854.00, f25: 1854.00, mar25: 1854.00, j26: 1766.00, f26: 1766.00, mar26:    0.00 },
    { cat: "Telefone",                   j25:  182.09, f25:  211.74, mar25:   40.84, j26:  296.45, f26:   57.50, mar26:    0.00 },
    { cat: "Codental (Sistema)",         j25:  160.90, f25:  114.90, mar25:  114.90, j26:  128.90, f26:  128.90, mar26:  128.90 },
    { cat: "CHB Ambiental",              j25:   95.65, f25:   93.75, mar25:   93.75, j26:  101.17, f26:  101.27, mar26:  101.27 },
    { cat: "Imposto Jur\u00eddico",           j25:  583.49, f25:  708.05, mar25:  888.67, j26: 1249.95, f26: 1119.07, mar26:  608.52 },
    { cat: "Desp. Funcion\u00e1rias",         j25: 5440.59, f25: 5616.92, mar25: 5148.56, j26: 6250.16, f26: 5869.27, mar26: 5753.27 },
    { cat: "Material Conserv./Limpeza",  j25:   37.15, f25:   96.30, mar25:    0.00, j26:  239.58, f26:  101.07, mar26:   82.62 },
  ];"""

if old_dados in html:
    html = html.replace(old_dados, new_dados)
    print("1. DADOS array atualizado (mar25/mar26 adicionados, Funcionárias j26 corrigido)")
else:
    print("ERRO: DADOS array não encontrado!")

# ============================================================
# 2. SUBSTITUIR forEach (m25/m26 → avg25/avg26 + meses disponíveis)
# ============================================================
old_foreach = """  // Calcular m\u00e9dias e varia\u00e7\u00f5es
  DADOS.forEach(d => {
    d.m25 = (d.j25 + d.f25) / 2;
    d.m26 = (d.j26 + d.f26) / 2;
    d.varR = d.m26 - d.m25;
    d.varP = (d.m26 / d.m25 - 1) * 100;
  });"""

new_foreach = """  // Calcular médias Q1 (apenas meses com valor > 0) e totais trimestrais
  DADOS.forEach(d => {
    const vs25 = [d.j25, d.f25, d.mar25].filter(v => v > 0);
    const vs26 = [d.j26, d.f26, d.mar26].filter(v => v > 0);
    d.avg25 = vs25.length ? vs25.reduce((a,b)=>a+b,0)/vs25.length : 0;
    d.avg26 = vs26.length ? vs26.reduce((a,b)=>a+b,0)/vs26.length : 0;
    d.q125  = d.j25 + d.f25 + d.mar25;
    d.q126  = d.j26 + d.f26 + d.mar26;
    d.varR  = d.avg26 - d.avg25;
    d.varP  = d.avg25 > 0 ? (d.avg26 / d.avg25 - 1) * 100 : 0;
  });"""

if old_foreach in html:
    html = html.replace(old_foreach, new_foreach)
    print("2. forEach atualizado (avg25/avg26 + Q1)")
else:
    print("ERRO: forEach não encontrado!")

# ============================================================
# 3. ATUALIZAR TABELA DE DETALHAMENTO — cabeçalho (thead)
# ============================================================
old_thead = """                <tr class="bg-slate-900/50 text-slate-400 text-xs font-semibold uppercase tracking-wider">
                  <th class="text-left px-5 py-3">Categoria</th>
                  <th class="text-right px-4 py-3">Jan/25</th>
                  <th class="text-right px-4 py-3">Fev/25</th>
                  <th class="text-right px-4 py-3 bg-blue-900/20">M\u00e9dia/25</th>
                  <th class="text-right px-4 py-3">Jan/26</th>
                  <th class="text-right px-4 py-3">Fev/26</th>
                  <th class="text-right px-4 py-3 bg-sky-900/20">M\u00e9dia/26</th>
                  <th class="text-right px-4 py-3">Var. R$</th>
                  <th class="text-right px-4 py-3">Var. %</th>
                </tr>"""

new_thead = """                <tr class="bg-slate-900/50 text-slate-400 text-xs font-semibold uppercase tracking-wider">
                  <th class="text-left px-5 py-3">Categoria</th>
                  <th class="text-right px-4 py-3">Jan/25</th>
                  <th class="text-right px-4 py-3">Fev/25</th>
                  <th class="text-right px-4 py-3 text-slate-500">Mar/25</th>
                  <th class="text-right px-4 py-3 bg-blue-900/20">Méd/25</th>
                  <th class="text-right px-4 py-3">Jan/26</th>
                  <th class="text-right px-4 py-3">Fev/26</th>
                  <th class="text-right px-4 py-3 text-amber-400/80">Mar/26*</th>
                  <th class="text-right px-4 py-3 bg-sky-900/20">Méd/26</th>
                  <th class="text-right px-4 py-3">Var. R$</th>
                  <th class="text-right px-4 py-3">Var. %</th>
                </tr>"""

if old_thead in html:
    html = html.replace(old_thead, new_thead)
    print("3. Thead tabela detalhamento atualizado")
else:
    print("ERRO: thead não encontrado!")

# ============================================================
# 4. ATUALIZAR TABELA DE DETALHAMENTO — tfoot (totais)
# ============================================================
old_tfoot = """                <tr class="bg-slate-900 font-bold text-white border-t-2 border-slate-600">
                  <td class="px-5 py-3.5">TOTAL GERAL</td>
                  <td class="text-right px-4 py-3.5">R$ 12.619</td>
                  <td class="text-right px-4 py-3.5">R$ 12.916</td>
                  <td class="text-right px-4 py-3.5 bg-blue-900/20">R$ 12.767</td>
                  <td class="text-right px-4 py-3.5">R$ 12.054</td>
                  <td class="text-right px-4 py-3.5">R$ 13.410</td>
                  <td class="text-right px-4 py-3.5 bg-sky-900/20">R$ 12.732</td>
                  <td class="text-right px-4 py-3.5 text-emerald-400">-R$ 35</td>
                  <td class="text-right px-4 py-3.5">
                    <span class="tag-flat text-xs font-bold px-2 py-0.5 rounded">-0,28%</span>
                  </td>
                </tr>"""

new_tfoot = """                <tr class="bg-slate-900 font-bold text-white border-t-2 border-slate-600">
                  <td class="px-5 py-3.5">TOTAL GERAL</td>
                  <td class="text-right px-4 py-3.5">R$ 12.619</td>
                  <td class="text-right px-4 py-3.5">R$ 12.916</td>
                  <td class="text-right px-4 py-3.5 text-slate-400 font-normal">R$ 11.147</td>
                  <td class="text-right px-4 py-3.5 bg-blue-900/20">R$ 12.654</td>
                  <td class="text-right px-4 py-3.5">R$ 14.254</td>
                  <td class="text-right px-4 py-3.5">R$ 13.410</td>
                  <td class="text-right px-4 py-3.5 text-amber-400/80 font-normal">R$ 8.744*</td>
                  <td class="text-right px-4 py-3.5 bg-sky-900/20">R$ 13.202</td>
                  <td class="text-right px-4 py-3.5 text-red-400">+R$ 548</td>
                  <td class="text-right px-4 py-3.5">
                    <span class="tag-high text-xs font-bold px-2 py-0.5 rounded">+4,33%</span>
                  </td>
                </tr>"""

if old_tfoot in html:
    html = html.replace(old_tfoot, new_tfoot)
    print("4. Tfoot tabela detalhamento atualizado")
else:
    print("ERRO: tfoot não encontrado!")

# ============================================================
# 5. ATUALIZAR RENDERIZAÇÃO JS DA TABELA (tbDetalhes forEach)
#    Adiciona Mar/25 e Mar/26*, troca d.m25→d.avg25, d.m26→d.avg26
# ============================================================
old_tb_render = """    tbDetalhes.innerHTML += `
      <tr class="${rowBg} hover:bg-slate-700/30 transition-colors border-b border-slate-700/20">
        <td class="px-5 py-3 font-medium text-slate-200">${d.cat}</td>
        <td class="text-right px-4 py-3 text-slate-300">${brl(d.j25)}</td>
        <td class="text-right px-4 py-3 text-slate-300">${brl(d.f25)}</td>
        <td class="text-right px-4 py-3 bg-blue-900/10 font-semibold text-white">${brl(d.m25)}</td>
        <td class="text-right px-4 py-3 text-slate-300">${brl(d.j26)}</td>
        <td class="text-right px-4 py-3 text-slate-300">${brl(d.f26)}</td>
        <td class="text-right px-4 py-3 bg-sky-900/10 font-semibold text-white">${brl(d.m26)}</td>
        <td class="text-right px-4 py-3 ${varColor} font-medium">${sinal}${brl(d.varR)}</td>
        <td class="text-right px-4 py-3">
          <span class="${tagClass} text-xs font-bold px-2 py-0.5 rounded">${sinal}${d.varP.toFixed(1)}%</span>
        </td>
      </tr>`;"""

new_tb_render = """    tbDetalhes.innerHTML += `
      <tr class="${rowBg} hover:bg-slate-700/30 transition-colors border-b border-slate-700/20">
        <td class="px-5 py-3 font-medium text-slate-200">${d.cat}</td>
        <td class="text-right px-4 py-3 text-slate-300">${brl(d.j25)}</td>
        <td class="text-right px-4 py-3 text-slate-300">${brl(d.f25)}</td>
        <td class="text-right px-4 py-3 text-slate-500 text-[11px]">${d.mar25 > 0 ? brl(d.mar25) : '—'}</td>
        <td class="text-right px-4 py-3 bg-blue-900/10 font-semibold text-white">${brl(d.avg25)}</td>
        <td class="text-right px-4 py-3 text-slate-300">${brl(d.j26)}</td>
        <td class="text-right px-4 py-3 text-slate-300">${brl(d.f26)}</td>
        <td class="text-right px-4 py-3 text-amber-400/80 text-[11px]">${d.mar26 > 0 ? brl(d.mar26)+'*' : '—'}</td>
        <td class="text-right px-4 py-3 bg-sky-900/10 font-semibold text-white">${brl(d.avg26)}</td>
        <td class="text-right px-4 py-3 ${varColor} font-medium">${sinal}${brl(d.varR)}</td>
        <td class="text-right px-4 py-3">
          <span class="${tagClass} text-xs font-bold px-2 py-0.5 rounded">${sinal}${d.varP.toFixed(1)}%</span>
        </td>
      </tr>`;"""

if old_tb_render in html:
    html = html.replace(old_tb_render, new_tb_render)
    print("5. Renderização tbDetalhes atualizada (Mar/25 e Mar/26*)")
else:
    print("ERRO: tbDetalhes innerHTML não encontrado!")

# ============================================================
# 6. ATUALIZAR KPI CARDS — SEÇÃO 1
# ============================================================

# Card 1: Total Comparável 2025
old_kpi1 = """          <div class="card-hover bg-gradient-to-br from-[#1B3A6B] to-[#0c2040] rounded-2xl p-5 border border-blue-800/40">
            <p class="text-slate-400 text-xs font-medium mb-1">Total Compar\u00e1vel 2025</p>
            <p class="text-white text-2xl font-bold">R$ 25.534</p>
            <p class="text-slate-400 text-xs mt-1">Bimestral Jan+Fev</p>
            <p class="text-[#0EA5E9] text-xs font-semibold mt-2">\u2248 R$ 12.767/m\u00eas</p>
          </div>"""
new_kpi1 = """          <div class="card-hover bg-gradient-to-br from-[#1B3A6B] to-[#0c2040] rounded-2xl p-5 border border-blue-800/40">
            <p class="text-slate-400 text-xs font-medium mb-1">Média Mensal Comparável 2025</p>
            <p class="text-white text-2xl font-bold">R$ 12.654</p>
            <p class="text-slate-400 text-xs mt-1">Q1 Jan+Fev+Mar — 9 categorias</p>
            <p class="text-[#0EA5E9] text-xs font-semibold mt-2">Total Q1: R$ 36.681</p>
          </div>"""

if old_kpi1 in html:
    html = html.replace(old_kpi1, new_kpi1)
    print("6a. KPI card 2025 atualizado")
else:
    print("ERRO: KPI card 2025 não encontrado!")

# Card 2: Total Comparável 2026
old_kpi2 = """          <div class="card-hover bg-gradient-to-br from-[#1B3A6B] to-[#0c2040] rounded-2xl p-5 border border-blue-800/40">
            <p class="text-slate-400 text-xs font-medium mb-1">Total Compar\u00e1vel 2026</p>
            <p class="text-white text-2xl font-bold">R$ 25.464</p>
            <p class="text-slate-400 text-xs mt-1">Bimestral Jan+Fev</p>
            <p class="text-[#0EA5E9] text-xs font-semibold mt-2">\u2248 R$ 12.732/m\u00eas</p>
          </div>"""
new_kpi2 = """          <div class="card-hover bg-gradient-to-br from-[#1B3A6B] to-[#0c2040] rounded-2xl p-5 border border-blue-800/40">
            <p class="text-slate-400 text-xs font-medium mb-1">Média Mensal Comparável 2026</p>
            <p class="text-white text-2xl font-bold">R$ 13.202<span class="text-amber-400 text-sm ml-1">*</span></p>
            <p class="text-slate-400 text-xs mt-1">Q1 Jan+Fev+Mar* — Mar/26 parcial</p>
            <p class="text-[#0EA5E9] text-xs font-semibold mt-2">Total Q1: R$ 36.408*</p>
          </div>"""

if old_kpi2 in html:
    html = html.replace(old_kpi2, new_kpi2)
    print("6b. KPI card 2026 atualizado")
else:
    print("ERRO: KPI card 2026 não encontrado!")

# Card 3: Variação Real
old_kpi3 = """          <div class="card-hover bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-5 border border-slate-700/40">
            <p class="text-slate-400 text-xs font-medium mb-1">Varia\u00e7\u00e3o Real (compar\u00e1vel)</p>
            <p class="text-emerald-400 text-2xl font-bold">-0,28%</p>
            <p class="text-slate-400 text-xs mt-1">Despesas praticamente est\u00e1veis</p>
            <div class="mt-2 inline-flex items-center gap-1 bg-emerald-500/10 rounded px-2 py-0.5">
              <span class="text-emerald-400 text-xs font-semibold">\u2713 Abaixo do IPCA</span>
            </div>
          </div>"""
new_kpi3 = """          <div class="card-hover bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-5 border border-slate-700/40">
            <p class="text-slate-400 text-xs font-medium mb-1">Variação Real (comparável)</p>
            <p class="text-red-400 text-2xl font-bold">+4,33%</p>
            <p class="text-slate-400 text-xs mt-1">Média mensal Q1 2025 → 2026</p>
            <div class="mt-2 inline-flex items-center gap-1 bg-emerald-500/10 rounded px-2 py-0.5">
              <span class="text-emerald-400 text-xs font-semibold">✓ Abaixo do IPCA (4,83%)</span>
            </div>
          </div>"""

if old_kpi3 in html:
    html = html.replace(old_kpi3, new_kpi3)
    print("6c. KPI variação atualizado (+4,33%)")
else:
    print("ERRO: KPI variação não encontrado!")

# Context cards (3 menores cards abaixo)
old_ctx = """        <div class="grid grid-cols-3 gap-4 mt-4">
          <div class="bg-slate-800/50 rounded-xl p-4 border border-slate-700/40">
            <p class="text-slate-400 text-xs mb-1">Maior alta \u2014 Imposto Jur\u00eddico</p>
            <p class="text-red-400 text-xl font-bold">+83,4%</p>
            <p class="text-slate-500 text-xs mt-1">R$ 646/m\u00eas \u2192 R$ 1.185/m\u00eas</p>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 border border-slate-700/40">
            <p class="text-slate-400 text-xs mb-1">Maior queda \u2014 Funcion\u00e1rias</p>
            <p class="text-emerald-400 text-xl font-bold">-10,3%</p>
            <p class="text-slate-500 text-xs mt-1">R$ 5.529/m\u00eas \u2192 R$ 4.960/m\u00eas</p>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 border border-slate-700/40">
            <p class="text-slate-400 text-xs mb-1">IPCA acumulado 2025</p>
            <p class="text-[#0EA5E9] text-xl font-bold">4,83%</p>
            <p class="text-slate-500 text-xs mt-1">Fonte: IBGE \u2014 infla\u00e7\u00e3o oficial</p>
          </div>
        </div>"""
new_ctx = """        <div class="grid grid-cols-3 gap-4 mt-4">
          <div class="bg-slate-800/50 rounded-xl p-4 border border-slate-700/40">
            <p class="text-slate-400 text-xs mb-1">Maior alta — Mat. Conserv./Limpeza</p>
            <p class="text-red-400 text-xl font-bold">+111,4%</p>
            <p class="text-slate-500 text-xs mt-1">R$ 67/mês → R$ 141/mês</p>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 border border-slate-700/40">
            <p class="text-slate-400 text-xs mb-1">2ª maior alta — Imposto Jurídico</p>
            <p class="text-red-400 text-xl font-bold">+36,6%</p>
            <p class="text-slate-500 text-xs mt-1">R$ 727/mês → R$ 993/mês</p>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 border border-slate-700/40">
            <p class="text-slate-400 text-xs mb-1">IPCA acumulado 2025</p>
            <p class="text-[#0EA5E9] text-xl font-bold">4,83%</p>
            <p class="text-slate-500 text-xs mt-1">Fonte: IBGE — inflação oficial</p>
          </div>
        </div>"""

if old_ctx in html:
    html = html.replace(old_ctx, new_ctx)
    print("6d. Context cards atualizados")
else:
    print("ERRO: context cards não encontrados!")

# ============================================================
# 7. ATUALIZAR AVISO METODOLÓGICO (Seção 1)
# ============================================================
old_aviso = """              Para o c\u00e1lculo do reajuste, foram usadas <strong>9 categorias fixas compar\u00e1veis</strong> (Jan+Fev 2025\u00d72026)."""
new_aviso = """              Para o c\u00e1lculo do reajuste, foram usadas <strong>9 categorias fixas comparáveis</strong> (Jan+Fev+Mar* 2025×2026 — Mar/26 parcial)."""
if old_aviso in html:
    html = html.replace(old_aviso, new_aviso)
    print("7. Aviso metodológico atualizado")
else:
    print("ERRO: aviso metodológico não encontrado!")

# ============================================================
# 8. ATUALIZAR CHART 1 — subtítulo e dados (m25/m26 → avg25/avg26)
# ============================================================
old_chart1_sub = """                <p class="text-slate-400 text-xs mt-0.5">M\u00e9dia de Jan+Fev \u2014 2025 \u00d7 2026 (R$)</p>"""
new_chart1_sub = """                <p class="text-slate-400 text-xs mt-0.5">Média Mensal Q1 Jan+Fev+Mar* — 2025 × 2026 (R$)</p>"""
if old_chart1_sub in html:
    html = html.replace(old_chart1_sub, new_chart1_sub)
    print("8a. Chart 1 subtítulo atualizado")
else:
    print("ERRO: chart 1 subtítulo não encontrado!")

# Chart 1: dados (d.m25 → d.avg25, d.m26 → d.avg26)
old_chart1_d1 = "          label: '2025 (M\u00e9dia)',\n          data: DADOS.map(d => Math.round(d.m25)),"
new_chart1_d1 = "          label: '2025 (Méd. Q1)',\n          data: DADOS.map(d => Math.round(d.avg25)),"
if old_chart1_d1 in html:
    html = html.replace(old_chart1_d1, new_chart1_d1)
    print("8b. Chart 1 dataset 2025 -> avg25")
else:
    print("ERRO: chart 1 dataset 2025 nao encontrado!")

old_chart1_d2 = "          label: '2026 (M\u00e9dia)',\n          data: DADOS.map(d => Math.round(d.m26)),"
new_chart1_d2 = "          label: '2026 (Méd. Q1)',\n          data: DADOS.map(d => Math.round(d.avg26)),"
if old_chart1_d2 in html:
    html = html.replace(old_chart1_d2, new_chart1_d2)
    print("8c. Chart 1 dataset 2026 -> avg26")
else:
    print("ERRO: chart 1 dataset 2026 não encontrado!")

# ============================================================
# 9. ATUALIZAR CHART 3 — subtítulo + adiciona Mar/25* e Mar/26*
# ============================================================
old_chart3_sub = """              <p class="text-slate-400 text-xs mt-0.5">Evolu\u00e7\u00e3o m\u00eas a m\u00eas \u2014 Jan/25, Fev/25, Jan/26, Fev/26</p>"""
new_chart3_sub = """              <p class="text-slate-400 text-xs mt-0.5">Evolução mês a mês — Jan/25, Fev/25, Mar/25, Jan/26, Fev/26, Mar/26* <span class="text-amber-400">* mês parcial</span></p>"""
if old_chart3_sub in html:
    html = html.replace(old_chart3_sub, new_chart3_sub)
    print("9a. Chart 3 subtítulo atualizado")
else:
    print("ERRO: chart 3 subtítulo não encontrado!")

old_totais = """  const totaisMensais = {
    'Jan/25': DADOS.reduce((s, d) => s + d.j25, 0),
    'Fev/25': DADOS.reduce((s, d) => s + d.f25, 0),
    'Jan/26': DADOS.reduce((s, d) => s + d.j26, 0),
    'Fev/26': DADOS.reduce((s, d) => s + d.f26, 0),
  };"""
new_totais = """  const totaisMensais = {
    'Jan/25':   DADOS.reduce((s, d) => s + d.j25,   0),
    'Fev/25':   DADOS.reduce((s, d) => s + d.f25,   0),
    'Mar/25':   DADOS.reduce((s, d) => s + d.mar25,  0),
    'Jan/26':   DADOS.reduce((s, d) => s + d.j26,   0),
    'Fev/26':   DADOS.reduce((s, d) => s + d.f26,   0),
    'Mar/26 *': DADOS.reduce((s, d) => s + d.mar26,  0),
  };"""
if old_totais in html:
    html = html.replace(old_totais, new_totais)
    print("9b. totaisMensais expandido para 6 meses")
else:
    print("ERRO: totaisMensais não encontrado!")

old_colors = "        backgroundColor: ['#1B3A6B', '#1B3A6B', '#0EA5E9', '#0EA5E9'],"
new_colors = "        backgroundColor: ['#1B3A6B', '#1B3A6B', '#1B3A6B80', '#0EA5E9', '#0EA5E9', '#f59e0b80'],"
if old_colors in html:
    html = html.replace(old_colors, new_colors)
    print("9c. Chart 3 cores atualizadas (6 barras)")
else:
    print("ERRO: chart 3 cores não encontradas!")

# Remove min: 10000 do eixo Y do chart 3 (Mar/26 é R$8.744)
old_ymin = "          min: 10000,"
new_ymin = "          min: 0,"
if old_ymin in html:
    html = html.replace(old_ymin, new_ymin)
    print("9d. Chart 3 min eixo Y ajustado para 0")
else:
    print("AVISO: min:10000 não encontrado (pode já estar ok)")

# ============================================================
# 10. ATUALIZAR SEÇÃO 3 HEADER
# ============================================================
old_s3h = """            <p class="text-white font-semibold text-sm">9 categorias fixas compar\u00e1veis \u2014 base da an\u00e1lise de precifica\u00e7\u00e3o</p>"""
new_s3h = """            <p class="text-white font-semibold text-sm">9 categorias fixas comparáveis — Jan+Fev+Mar* 2025 × 2026 <span class="text-amber-400 font-normal text-xs">(Mar/26 parcial)</span></p>"""
if old_s3h in html:
    html = html.replace(old_s3h, new_s3h)
    print("10. Header seção 3 atualizado")
else:
    print("ERRO: header seção 3 não encontrado!")

# ============================================================
# SALVAR
# ============================================================
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

new_size = len(html)
print(f"\nindex.html salvo: {new_size} bytes (delta: +{new_size - original_size})")
