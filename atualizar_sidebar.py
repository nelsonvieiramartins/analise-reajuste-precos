# -*- coding: utf-8 -*-
"""
Transforma o sidebar fixo em retrátil.
Expandido: w-56 (224px) com ícone + texto.
Recolhido: w-12 (48px) com apenas ícones centralizados.
"""

with open('index.html', encoding='utf-8') as f:
    html = f.read()

print(f"Lido: {len(html)} bytes")

# ============================================================
# 1. CSS — transições e estado recolhido
# ============================================================
old_css_end = "    .tip-wrap:hover .tip-box { display: block; }\n  </style>"
new_css_end = """    .tip-wrap:hover .tip-box { display: block; }

    /* ── Sidebar retrátil ── */
    #sidebar {
      transition: width 0.25s ease;
      overflow: hidden;
    }
    #sidebar.collapsed { width: 48px; }
    #mainContent { transition: margin-left 0.25s ease; }
    #mainContent.expanded { margin-left: 48px; }

    /* Esconde textos quando recolhido */
    #sidebar.collapsed .nav-label  { display: none; }
    #sidebar.collapsed .logo-text  { display: none; }
    #sidebar.collapsed .footer-text { display: none; }

    /* Links centralizados com ícones */
    #sidebar.collapsed .sidebar-link {
      justify-content: center;
      padding-left: 0;
      padding-right: 0;
      gap: 0;
    }
    #sidebar.collapsed .nav-section-label {
      overflow: hidden;
      height: 0;
      padding: 0;
      margin: 0;
    }

    /* Botão de toggle */
    #sidebarToggle {
      transition: transform 0.25s ease, background 0.15s;
    }
    #sidebar.collapsed #sidebarToggle { transform: rotate(180deg); }

    /* Tooltip de item no estado recolhido */
    .nav-item-wrap { position: relative; }
    #sidebar.collapsed .nav-item-tip {
      display: none;
      position: absolute;
      left: calc(100% + 8px);
      top: 50%;
      transform: translateY(-50%);
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 6px;
      padding: 4px 10px;
      font-size: 12px;
      color: #e2e8f0;
      white-space: nowrap;
      z-index: 300;
      pointer-events: none;
      box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    #sidebar.collapsed .nav-item-wrap:hover .nav-item-tip { display: block; }
  </style>"""

if old_css_end in html:
    html = html.replace(old_css_end, new_css_end)
    print("1. CSS sidebar retrátil adicionado")
else:
    print("ERRO: fim do <style> não encontrado!")

# ============================================================
# 2. Adiciona id="sidebar" ao <aside>
# ============================================================
old_aside = '  <aside class="no-print w-56 min-h-screen bg-[#0F172A] border-r border-slate-700/50 flex flex-col fixed top-0 left-0 z-40">'
new_aside = '  <aside id="sidebar" class="no-print w-56 min-h-screen bg-[#0F172A] border-r border-slate-700/50 flex flex-col fixed top-0 left-0 z-40">'

if old_aside in html:
    html = html.replace(old_aside, new_aside)
    print("2. id='sidebar' adicionado ao <aside>")
else:
    print("ERRO: <aside> não encontrado!")

# ============================================================
# 3. Logo area — adiciona botão toggle e classes logo-text
# ============================================================
old_logo = """    <!-- Logo -->
    <div class="p-5 border-b border-slate-700/50">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg bg-gradient-to-br from-[#0EA5E9] to-[#1B3A6B] flex items-center justify-center text-white font-bold text-sm">CP</div>
        <div>
          <p class="text-white font-bold text-sm leading-tight">Cl\u00ednica Pelegrino</p>
          <p class="text-slate-400 text-[10px] uppercase tracking-wider">Gest\u00e3o Financeira</p>
        </div>
      </div>
    </div>"""

new_logo = """    <!-- Logo + toggle -->
    <div class="p-4 border-b border-slate-700/50">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3 min-w-0">
          <div class="w-9 h-9 shrink-0 rounded-lg bg-gradient-to-br from-[#0EA5E9] to-[#1B3A6B] flex items-center justify-center text-white font-bold text-sm">CP</div>
          <div class="logo-text min-w-0">
            <p class="text-white font-bold text-sm leading-tight whitespace-nowrap">Clínica Pelegrino</p>
            <p class="text-slate-400 text-[10px] uppercase tracking-wider whitespace-nowrap">Gestão Financeira</p>
          </div>
        </div>
        <button id="sidebarToggle" onclick="toggleSidebar()"
          class="shrink-0 w-6 h-6 flex items-center justify-center rounded-md text-slate-400 hover:text-white hover:bg-slate-700/60 text-xs ml-1">
          &#8249;
        </button>
      </div>
    </div>"""

if old_logo in html:
    html = html.replace(old_logo, new_logo)
    print("3. Logo com botão toggle adicionado")
else:
    print("ERRO: logo não encontrado!")

# ============================================================
# 4. Section labels — adiciona classe nav-section-label
# ============================================================
old_sec1 = '      <p class="text-slate-500 text-[10px] font-semibold uppercase tracking-widest px-3 pt-3 pb-1">An\u00e1lise</p>'
new_sec1 = '      <p class="nav-section-label text-slate-500 text-[10px] font-semibold uppercase tracking-widest px-3 pt-3 pb-1">Análise</p>'
if old_sec1 in html:
    html = html.replace(old_sec1, new_sec1)
    print("4a. Label 'Análise' marcado")
else:
    print("ERRO: label Análise não encontrado!")

old_sec2 = '      <p class="text-slate-500 text-[10px] font-semibold uppercase tracking-widest px-3 pt-4 pb-1">Precifica\u00e7\u00e3o</p>'
new_sec2 = '      <p class="nav-section-label text-slate-500 text-[10px] font-semibold uppercase tracking-widest px-3 pt-4 pb-1">Precificação</p>'
if old_sec2 in html:
    html = html.replace(old_sec2, new_sec2)
    print("4b. Label 'Precificação' marcado")
else:
    print("ERRO: label Precificação não encontrado!")

# ============================================================
# 5. Nav links — envolve textos em <span class="nav-label">
#    e adiciona wrapper + tip para tooltip colapsado
# ============================================================
nav_links = [
    (
        '      <a href="#resumo" class="sidebar-link active flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-200">\n        <span class="text-[#0EA5E9]">\u2b1b</span> Resumo Executivo\n      </a>',
        '      <div class="nav-item-wrap">\n      <a href="#resumo" class="sidebar-link active flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-200">\n        <span class="text-[#0EA5E9]">⬛</span><span class="nav-label"> Resumo Executivo</span>\n      </a>\n      <div class="nav-item-tip">Resumo Executivo</div>\n      </div>'
    ),
    (
        '      <a href="#comparativo" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>\U0001f4ca</span> Comparativo\n      </a>',
        '      <div class="nav-item-wrap">\n      <a href="#comparativo" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>📊</span><span class="nav-label"> Comparativo</span>\n      </a>\n      <div class="nav-item-tip">Comparativo</div>\n      </div>'
    ),
    (
        '      <a href="#detalhes" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>\U0001f4cb</span> Detalhamento\n      </a>',
        '      <div class="nav-item-wrap">\n      <a href="#detalhes" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>📋</span><span class="nav-label"> Detalhamento</span>\n      </a>\n      <div class="nav-item-tip">Detalhamento</div>\n      </div>'
    ),
    (
        '      <a href="#excluidos" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>\U0001f4ca</span> Desp. Completas\n      </a>',
        '      <div class="nav-item-wrap">\n      <a href="#excluidos" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>📊</span><span class="nav-label"> Desp. Completas</span>\n      </a>\n      <div class="nav-item-tip">Desp. Completas</div>\n      </div>'
    ),
    (
        '      <a href="#metodologia" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>\U0001f9ee</span> Metodologia\n      </a>',
        '      <div class="nav-item-wrap">\n      <a href="#metodologia" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>🧮</span><span class="nav-label"> Metodologia</span>\n      </a>\n      <div class="nav-item-tip">Metodologia</div>\n      </div>'
    ),
    (
        '      <a href="#simulacao" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>\U0001f3ae</span> Simulador\n      </a>',
        '      <div class="nav-item-wrap">\n      <a href="#simulacao" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>🎮</span><span class="nav-label"> Simulador</span>\n      </a>\n      <div class="nav-item-tip">Simulador</div>\n      </div>'
    ),
    (
        '      <a href="#faturamento" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>\U0001f4c8</span> Faturamento Simulado\n      </a>',
        '      <div class="nav-item-wrap">\n      <a href="#faturamento" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>📈</span><span class="nav-label"> Faturamento Simulado</span>\n      </a>\n      <div class="nav-item-tip">Faturamento Simulado</div>\n      </div>'
    ),
    (
        '      <a href="#tabela" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>\U0001f4b0</span> Tabela de Pre\u00e7os\n      </a>',
        '      <div class="nav-item-wrap">\n      <a href="#tabela" class="sidebar-link flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-400">\n        <span>💰</span><span class="nav-label"> Tabela de Preços</span>\n      </a>\n      <div class="nav-item-tip">Tabela de Preços</div>\n      </div>'
    ),
]

ok_count = 0
for old, new in nav_links:
    if old in html:
        html = html.replace(old, new)
        ok_count += 1
    else:
        print(f"  AVISO: link nao encontrado: {old[:50]}")
print(f"5. {ok_count}/8 nav links atualizados com nav-label + tip")

# ============================================================
# 6. Footer — adiciona classe footer-text
# ============================================================
old_footer = '      <p class="text-slate-500 text-[10px] text-center">Jan-Mar 2025 \u00d7 Jan-Mar 2026</p>'
new_footer = '      <p class="footer-text text-slate-500 text-[10px] text-center">Jan-Mar 2025 × Jan-Mar 2026</p>'
if old_footer in html:
    html = html.replace(old_footer, new_footer)
    print("6. Footer marcado com footer-text")
else:
    print("ERRO: footer não encontrado!")

# ============================================================
# 7. Adiciona id="mainContent" ao <main>
# ============================================================
old_main = '  <main class="ml-56 flex-1 min-h-screen bg-[#0F172A]">'
new_main = '  <main id="mainContent" class="ml-56 flex-1 min-h-screen bg-[#0F172A]">'
if old_main in html:
    html = html.replace(old_main, new_main)
    print("7. id='mainContent' adicionado ao <main>")
else:
    print("ERRO: <main> não encontrado!")

# ============================================================
# 8. JS — função toggleSidebar()
# ============================================================
old_scroll_spy = "  // ============================================================\n  // SIDEBAR SCROLL SPY\n  // ============================================================"
new_scroll_spy = """  // ============================================================
  // SIDEBAR TOGGLE
  // ============================================================
  function toggleSidebar() {
    const sb = document.getElementById('sidebar');
    const mc = document.getElementById('mainContent');
    sb.classList.toggle('collapsed');
    mc.classList.toggle('expanded');
    // Persiste estado na sessão
    sessionStorage.setItem('sidebarCollapsed', sb.classList.contains('collapsed') ? '1' : '0');
  }
  // Restaura estado da sessão
  (function() {
    if (sessionStorage.getItem('sidebarCollapsed') === '1') {
      document.getElementById('sidebar').classList.add('collapsed');
      document.getElementById('mainContent').classList.add('expanded');
    }
  })();

  // ============================================================
  // SIDEBAR SCROLL SPY
  // ============================================================"""

if old_scroll_spy in html:
    html = html.replace(old_scroll_spy, new_scroll_spy)
    print("8. JS toggleSidebar() adicionado")
else:
    print("ERRO: scroll spy não encontrado!")

# ============================================================
# SALVAR
# ============================================================
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nindex.html salvo: {len(html)} bytes")
