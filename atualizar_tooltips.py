# -*- coding: utf-8 -*-
"""
Adiciona tooltips explicativos nos 4 KPI cards da Seção 1.
"""

with open('index.html', encoding='utf-8') as f:
    html = f.read()

print(f"Lido: {len(html)} bytes")

# ============================================================
# 1. ADICIONAR CSS DE TOOLTIP
# ============================================================
old_css_end = "    .precif-badge    { background: rgba(14,165,233,0.2);  color: #0EA5E9; font-size:10px; padding:1px 5px; border-radius:4px; }\n  </style>"
new_css_end = """    .precif-badge    { background: rgba(14,165,233,0.2);  color: #0EA5E9; font-size:10px; padding:1px 5px; border-radius:4px; }
    /* Tooltips */
    .tip-wrap { position: relative; display: inline-flex; align-items: center; }
    .tip-icon { color: #475569; font-size: 12px; cursor: help; line-height: 1; transition: color 0.15s; }
    .tip-icon:hover { color: #94a3b8; }
    .tip-box {
      display: none;
      position: absolute;
      bottom: calc(100% + 8px);
      left: 50%;
      transform: translateX(-50%);
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 10px;
      padding: 10px 12px;
      width: 230px;
      font-size: 11px;
      color: #cbd5e1;
      line-height: 1.6;
      z-index: 200;
      pointer-events: none;
      box-shadow: 0 8px 30px rgba(0,0,0,0.5);
      white-space: normal;
    }
    .tip-box::after {
      content: '';
      position: absolute;
      top: 100%;
      left: 50%;
      transform: translateX(-50%);
      border: 6px solid transparent;
      border-top-color: #334155;
    }
    .tip-wrap:hover .tip-box { display: block; }
  </style>"""

if old_css_end in html:
    html = html.replace(old_css_end, new_css_end)
    print("1. CSS tooltip adicionado")
else:
    print("ERRO: fim do bloco <style> nao encontrado!")

# ============================================================
# 2. KPI CARD 1 — Média Mensal 2025
# ============================================================
old_kpi1_title = '            <p class="text-slate-400 text-xs font-medium mb-1">M\u00e9dia Mensal Compar\u00e1vel 2025</p>'
new_kpi1_title = '''            <div class="flex items-center gap-1.5 mb-1">
              <p class="text-slate-400 text-xs font-medium">Média Mensal Comparável 2025</p>
              <div class="tip-wrap">
                <span class="tip-icon">ⓘ</span>
                <div class="tip-box">Média das despesas mensais das <strong>9 categorias fixas comparáveis</strong> no Q1 2025 (Jan, Fev, Mar). Calculado apenas com os meses que têm lançamentos registrados.</div>
              </div>
            </div>'''

if old_kpi1_title in html:
    html = html.replace(old_kpi1_title, new_kpi1_title)
    print("2. Tooltip KPI 2025 adicionado")
else:
    print("ERRO: titulo KPI 2025 nao encontrado!")

# ============================================================
# 3. KPI CARD 2 — Média Mensal 2026
# ============================================================
old_kpi2_title = '            <p class="text-slate-400 text-xs font-medium mb-1">M\u00e9dia Mensal Compar\u00e1vel 2026</p>'
new_kpi2_title = '''            <div class="flex items-center gap-1.5 mb-1">
              <p class="text-slate-400 text-xs font-medium">Média Mensal Comparável 2026</p>
              <div class="tip-wrap">
                <span class="tip-icon">ⓘ</span>
                <div class="tip-box">Média das despesas mensais das <strong>9 categorias fixas comparáveis</strong> no Q1 2026. <span class="text-amber-400 font-semibold">Mar/26 ainda não fechou</span> — o valor de março é parcial e pode crescer até o fechamento do mês.</div>
              </div>
            </div>'''

if old_kpi2_title in html:
    html = html.replace(old_kpi2_title, new_kpi2_title)
    print("3. Tooltip KPI 2026 adicionado")
else:
    print("ERRO: titulo KPI 2026 nao encontrado!")

# ============================================================
# 4. KPI CARD 3 — Variação Real
# ============================================================
old_kpi3_title = '            <p class="text-slate-400 text-xs font-medium mb-1">Varia\u00e7\u00e3o Real (compar\u00e1vel)</p>'
new_kpi3_title = '''            <div class="flex items-center gap-1.5 mb-1">
              <p class="text-slate-400 text-xs font-medium">Variação Real (comparável)</p>
              <div class="tip-wrap">
                <span class="tip-icon">ⓘ</span>
                <div class="tip-box">Variação percentual da <strong>média mensal</strong> das 9 categorias fixas entre 2025 e 2026. É a base para definir o reajuste necessário: se as despesas subiram menos que o IPCA, o índice oficial é o critério de reajuste.</div>
              </div>
            </div>'''

if old_kpi3_title in html:
    html = html.replace(old_kpi3_title, new_kpi3_title)
    print("4. Tooltip Variacao adicionado")
else:
    print("ERRO: titulo Variacao nao encontrado!")

# ============================================================
# 5. KPI CARD 4 — Reajuste Recomendado
# ============================================================
old_kpi4_title = '            <p class="text-slate-400 text-xs font-medium mb-1">Reajuste Recomendado</p>'
new_kpi4_title = '''            <div class="flex items-center gap-1.5 mb-1">
              <p class="text-slate-400 text-xs font-medium">Reajuste Recomendado</p>
              <div class="tip-wrap">
                <span class="tip-icon">ⓘ</span>
                <div class="tip-box">Reajuste sugerido para a <strong>tabela de preços</strong> da clínica. Como a variação real das despesas (+4,33%) ficou abaixo do IPCA 2025 (4,83%), recomendamos aplicar o índice oficial. Use o simulador para testar outros percentuais.</div>
              </div>
            </div>'''

if old_kpi4_title in html:
    html = html.replace(old_kpi4_title, new_kpi4_title)
    print("5. Tooltip Reajuste adicionado")
else:
    print("ERRO: titulo Reajuste nao encontrado!")

# ============================================================
# SALVAR
# ============================================================
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nindex.html salvo: {len(html)} bytes")
