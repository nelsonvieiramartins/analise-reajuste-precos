# -*- coding: utf-8 -*-
"""
Correções:
  tabela.html — remove soma total (não faz sentido para tabela de preços)
              — renomeia "Preço Atual" → "Preço Anterior"
  index.html  — simulador restaura o percentual salvo (localStorage permanente)
                ao abrir a página
"""

# ============================================================
# TABELA.HTML — 3 patches
# ============================================================
with open('tabela.html', encoding='utf-8') as f:
    t = f.read()
print(f"tabela.html lido: {len(t)} bytes")

# ── 1. Remove card "Total da tabela" do banner ──────────────
old_total_card = """          <div>
            <p class="text-slate-500 text-[10px] uppercase tracking-wider mb-0.5">Total da tabela</p>
            <p class="text-white font-bold text-3xl" id="infoTotal">—</p>
          </div>"""
new_total_card = ""   # remove completamente

if old_total_card in t:
    t = t.replace(old_total_card, new_total_card)
    print("1. Card 'Total da tabela' removido do banner")
else:
    print("ERRO: card Total da tabela nao encontrado!")

# ── 2. Remove tfoot + atualiza total no JS ──────────────────
old_tfoot = """      // Totais
      const diffTotal = somaNovo - somaAtual;
      tfoot.innerHTML =
        '<tr class="tfoot-row border-t border-slate-600 bg-slate-800/60 font-bold">' +
        '<td class="no-print px-4 py-3"></td>' +
        '<td class="px-4 py-3 text-slate-200 text-xs uppercase tracking-wider">Total (' + count + ' procedimentos)</td>' +
        '<td class="px-4 py-3 text-right font-mono text-slate-300">' + brl(somaAtual) + '</td>' +
        '<td class="px-4 py-3 text-right font-mono text-emerald-300 text-base novo-preco">' + brl(somaNovo) + '</td>' +
        '<td class="no-print px-4 py-3 text-right font-mono text-slate-400">+' + brl(diffTotal) + '</td>' +
        '</tr>';

      // Atualiza total no banner
      const elTotal = document.getElementById('infoTotal');
      if (elTotal) elTotal.textContent = brl(somaNovo);"""

new_tfoot = "      tfoot.innerHTML = '';"

if old_tfoot in t:
    t = t.replace(old_tfoot, new_tfoot)
    print("2. Tfoot e soma total removidos do JS")
else:
    print("ERRO: bloco tfoot nao encontrado!")

# ── 3. Renomeia coluna "Preço Atual" → "Preço Anterior" ─────
old_th = """            <th class="text-right text-slate-400 font-semibold text-[11px] uppercase
                       tracking-wider px-4 py-3 w-32">Preço Atual</th>"""
new_th = """            <th class="text-right text-slate-400 font-semibold text-[11px] uppercase
                       tracking-wider px-4 py-3 w-32">Preço Anterior</th>"""

if old_th in t:
    t = t.replace(old_th, new_th)
    print("3. 'Preco Atual' renomeado para 'Preco Anterior'")
else:
    print("ERRO: th Preco Atual nao encontrado!")

with open('tabela.html', 'w', encoding='utf-8') as f:
    f.write(t)
print(f"tabela.html salvo: {len(t)} bytes")


# ============================================================
# INDEX.HTML — restaura percentual do localStorage na inicialização
# ============================================================
with open('index.html', encoding='utf-8') as f:
    h = f.read()
print(f"\nindex.html lido: {len(h)} bytes")

# Substitui a chamada fixa atualizarSimulador(5) por uma que lê
# o localStorage (armazenamento permanente no navegador)
old_init = """  // Inicializar simulador
  atualizarSimulador(5);"""

new_init = """  // Inicializar simulador — restaura último percentual salvo (localStorage)
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

if old_init in h:
    h = h.replace(old_init, new_init)
    print("4. Simulador agora restaura percentual do localStorage na abertura")
else:
    print("ERRO: init atualizarSimulador(5) nao encontrado!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print(f"index.html salvo: {len(h)} bytes")
print("\nCONCLUIDA.")
