
# atualizar_dashboard.py — Atualiza dashboard.html com dados completos Jan-Mar 2025/2026
import re

with open("dashboard.html", "r", encoding="utf-8") as f:
    html = f.read()

print(f"Lido: {len(html)} bytes")

# ─── 1. Sidebar rodapé ───────────────────────────────────────────────────────
html = html.replace(
    'Jan-Fev 2025 \u00d7 Jan-Fev 2026',
    'Jan-Mar 2025 \u00d7 Jan-Mar 2026'
)
print("1. Sidebar atualizada")

# ─── 2. Substituir Seção 6.5 ─────────────────────────────────────────────────
START = '      <!-- ============================================================\n           SE\u00c7\u00c3O 6.5 \u2013 SIMULADOR DE FATURAMENTO (NOVA)\n      ============================================================ -->'
# Encontrar fim: fechamento do </section> imediatamente seguido de dois comentários da seção 7
END_TAG = '      </section>\n\n      <!-- ============================================================\n           SE\u00c7\u00c3O 7 \u2013 TABELA DE PRE\u00c7OS'

idx_s = html.find(START)
idx_e = html.find(END_TAG, idx_s if idx_s >= 0 else 0)
print(f"  Secao 6.5: start={idx_s}, end={idx_e}")

NEW_SEC = '''      <!-- ============================================================
           SE\u00c7\u00c3O 6.5 \u2013 RECEITA \u00d7 DESPESAS \u00d7 PROJE\u00c7\u00c3O 2026
      ============================================================ -->
      <section id="faturamento">
        <h2 class="text-slate-300 text-xs font-bold uppercase tracking-widest mb-4">Receita \u00d7 Despesas \u2014 Jan-Mar 2025/2026 + Proje\u00e7\u00e3o Anual</h2>

        <!-- KPI Row -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-5">
          <div class="bg-slate-800/50 rounded-xl p-4 border border-emerald-500/20">
            <p class="text-slate-400 text-xs mb-1">Receita Q1 2025</p>
            <p class="text-emerald-300 text-xl font-black">R$&nbsp;91.862</p>
            <p class="text-slate-500 text-[10px] mt-1">Refer\u00eancia (Jan-Mar/2025)</p>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 border border-emerald-400/30">
            <p class="text-slate-400 text-xs mb-1">Receita Q1 2026</p>
            <p class="text-emerald-400 text-xl font-black">R$&nbsp;87.570</p>
            <p class="text-red-400 text-[10px] mt-1">\u25bc -4,7% vs 2025</p>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 border border-red-500/20">
            <p class="text-slate-400 text-xs mb-1">Despesas Q1 2026</p>
            <p class="text-red-400 text-xl font-black">R$&nbsp;76.270</p>
            <p class="text-red-400/70 text-[10px] mt-1">\u25b2 +7,3% vs 2025</p>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 border border-[#0EA5E9]/30">
            <p class="text-slate-400 text-xs mb-1">Saldo L\u00edquido Q1 2026</p>
            <p class="text-[#0EA5E9] text-xl font-black">R$&nbsp;11.300</p>
            <p class="text-red-400 text-[10px] mt-1">Margem 12,9% (era 22,6%)</p>
          </div>
        </div>

        <!-- Tabela comparativa 2025 x 2026 -->
        <div class="bg-slate-800/50 rounded-2xl p-5 border border-slate-700/40 mb-5">
          <p class="text-slate-300 text-xs font-bold uppercase tracking-widest mb-3">Comparativo Mensal \u2014 Receita, Despesas e Saldo</p>
          <div class="overflow-x-auto">
            <table class="w-full text-xs">
              <thead>
                <tr class="bg-slate-900/60 text-slate-500 uppercase tracking-wider text-[10px]">
                  <th class="text-left px-4 py-2">M\u00eas</th>
                  <th class="text-right px-3 py-2 text-emerald-300">Receita 2025</th>
                  <th class="text-right px-3 py-2 text-emerald-400">Receita 2026</th>
                  <th class="text-right px-2 py-2">Var%</th>
                  <th class="text-right px-3 py-2 text-red-300">Despesa 2025</th>
                  <th class="text-right px-3 py-2 text-red-400">Despesa 2026</th>
                  <th class="text-right px-2 py-2">Var%</th>
                  <th class="text-right px-3 py-2 text-slate-300">Saldo 2025</th>
                  <th class="text-right px-3 py-2 text-[#38bdf8]">Saldo 2026</th>
                </tr>
              </thead>
              <tbody>
                <tr class="border-b border-slate-700/30 hover:bg-slate-700/20">
                  <td class="px-4 py-2.5 font-semibold text-slate-300">Janeiro</td>
                  <td class="text-right px-3 py-2.5 text-emerald-300/80">R$&nbsp;26.551</td>
                  <td class="text-right px-3 py-2.5 text-emerald-400">R$&nbsp;26.396</td>
                  <td class="text-right px-2 py-2.5 text-slate-400">-0,6%</td>
                  <td class="text-right px-3 py-2.5 text-red-300/80">R$&nbsp;23.584</td>
                  <td class="text-right px-3 py-2.5 text-red-400">R$&nbsp;25.961</td>
                  <td class="text-right px-2 py-2.5 text-red-400">+10,1%</td>
                  <td class="text-right px-3 py-2.5 text-slate-400">R$&nbsp;2.967</td>
                  <td class="text-right px-3 py-2.5 text-amber-400 font-semibold">R$&nbsp;435</td>
                </tr>
                <tr class="border-b border-slate-700/30 bg-slate-800/20 hover:bg-slate-700/20">
                  <td class="px-4 py-2.5 font-semibold text-slate-300">Fevereiro</td>
                  <td class="text-right px-3 py-2.5 text-emerald-300/80">R$&nbsp;46.421</td>
                  <td class="text-right px-3 py-2.5 text-emerald-400">R$&nbsp;36.463</td>
                  <td class="text-right px-2 py-2.5 text-red-400">-21,5%</td>
                  <td class="text-right px-3 py-2.5 text-red-300/80">R$&nbsp;29.588</td>
                  <td class="text-right px-3 py-2.5 text-red-400">R$&nbsp;28.358</td>
                  <td class="text-right px-2 py-2.5 text-emerald-400">-4,2%</td>
                  <td class="text-right px-3 py-2.5 text-slate-400">R$&nbsp;16.833</td>
                  <td class="text-right px-3 py-2.5 text-[#38bdf8] font-semibold">R$&nbsp;8.105</td>
                </tr>
                <tr class="border-b border-slate-700/30 hover:bg-slate-700/20">
                  <td class="px-4 py-2.5 font-semibold text-slate-300">Mar\u00e7o <span class="text-amber-400 text-[9px] ml-1">*parcial</span></td>
                  <td class="text-right px-3 py-2.5 text-emerald-300/80">R$&nbsp;18.891</td>
                  <td class="text-right px-3 py-2.5 text-emerald-400">R$&nbsp;24.712</td>
                  <td class="text-right px-2 py-2.5 text-emerald-400">+30,8%</td>
                  <td class="text-right px-3 py-2.5 text-red-300/80">R$&nbsp;17.921</td>
                  <td class="text-right px-3 py-2.5 text-red-400">R$&nbsp;21.952</td>
                  <td class="text-right px-2 py-2.5 text-red-400">+22,5%</td>
                  <td class="text-right px-3 py-2.5 text-slate-400">R$&nbsp;970</td>
                  <td class="text-right px-3 py-2.5 text-[#38bdf8] font-semibold">R$&nbsp;2.760</td>
                </tr>
                <tr class="bg-slate-900/70 font-bold text-[11px]">
                  <td class="px-4 py-3 text-white">Q1 TOTAL</td>
                  <td class="text-right px-3 py-3 text-emerald-300">R$&nbsp;91.862</td>
                  <td class="text-right px-3 py-3 text-emerald-400">R$&nbsp;87.570</td>
                  <td class="text-right px-2 py-3 text-red-400">-4,7%</td>
                  <td class="text-right px-3 py-3 text-red-300">R$&nbsp;71.092</td>
                  <td class="text-right px-3 py-3 text-red-400">R$&nbsp;76.270</td>
                  <td class="text-right px-2 py-3 text-red-400">+7,3%</td>
                  <td class="text-right px-3 py-3 text-slate-200">R$&nbsp;20.770</td>
                  <td class="text-right px-3 py-3 text-[#0EA5E9]">R$&nbsp;11.300</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p class="text-slate-500 text-[10px] mt-2 pl-1">* Mar\u00e7o/2025 e Mar\u00e7o/2026: dados at\u00e9 ~25/03 de cada ano \u2014 per\u00edodos equivalentes.</p>
        </div>

        <!-- 3 cards: Simula\u00e7\u00e3o / M\u00e9dia / Proje\u00e7\u00e3o -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-5">
          <div class="bg-gradient-to-br from-emerald-950/50 to-slate-900/80 rounded-xl p-4 border border-emerald-500/20">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-emerald-400">&#128202;</span>
              <p class="text-emerald-400 text-xs font-bold uppercase tracking-wider">Simula\u00e7\u00e3o Q1 2026</p>
            </div>
            <p class="text-slate-500 text-[10px] mb-3">Com reajuste de <span id="txtFatSimPct" class="text-amber-400 font-bold">5,0%</span></p>
            <div class="space-y-2 text-xs">
              <div class="flex justify-between">
                <span class="text-slate-400">Receita real Q1</span>
                <span class="text-emerald-400 font-semibold">R$&nbsp;87.570</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-400">Com reajuste</span>
                <span class="text-amber-400 font-semibold" id="fatSimTotal">\u2014</span>
              </div>
              <div class="flex justify-between border-t border-slate-700/40 pt-2">
                <span class="text-slate-400">Ganho no trimestre</span>
                <span class="text-emerald-400 font-bold" id="valFatGanho">\u2014</span>
              </div>
            </div>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 border border-[#0EA5E9]/20">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-[#0EA5E9]">&#128197;</span>
              <p class="text-[#0EA5E9] text-xs font-bold uppercase tracking-wider">M\u00e9dia Mensal Q1</p>
            </div>
            <div class="space-y-2 text-xs">
              <div class="flex justify-between">
                <span class="text-slate-400">M\u00e9dia real (3 meses)</span>
                <span class="text-slate-300 font-semibold">R$&nbsp;29.190</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-400">M\u00e9dia c/ reajuste</span>
                <span class="text-amber-400 font-semibold" id="fatMediaSim">\u2014</span>
              </div>
              <div class="flex justify-between border-t border-slate-700/40 pt-2">
                <span class="text-slate-400">Ganho por m\u00eas</span>
                <span class="text-emerald-400 font-bold" id="valFatGanhoMes">\u2014</span>
              </div>
            </div>
          </div>
          <div class="bg-slate-800/50 rounded-xl p-4 border border-amber-500/20">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-amber-400">&#128302;</span>
              <p class="text-amber-400 text-xs font-bold uppercase tracking-wider">Proje\u00e7\u00e3o Anual 2026</p>
            </div>
            <div class="space-y-2 text-xs">
              <div class="flex justify-between">
                <span class="text-slate-400">Sem reajuste (12 meses)</span>
                <span class="text-slate-300 font-semibold">R$&nbsp;350.280</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-400">Com reajuste Abr\u2013Dez</span>
                <span class="text-amber-400 font-semibold" id="fatProjecaoAno">\u2014</span>
              </div>
              <div class="flex justify-between border-t border-slate-700/40 pt-2">
                <span class="text-slate-400">Ganho anual projetado</span>
                <span class="text-emerald-400 font-bold" id="valFatGanhoAno">\u2014</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Tabela mensal detalhada -->
        <div class="bg-slate-800/50 rounded-xl border border-slate-700/40 overflow-hidden mb-4">
          <div class="px-5 py-3 bg-slate-900/40 border-b border-slate-700/40 flex items-center justify-between">
            <p class="text-slate-300 text-xs font-bold uppercase tracking-wider">Detalhamento \u2014 Simula\u00e7\u00e3o de Receita por M\u00eas</p>
            <span class="text-amber-400 text-xs font-bold bg-amber-500/10 px-2 py-1 rounded-full" id="lblFatSimPct">Reajuste: 5,0%</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-slate-900/60 text-slate-400 text-[10px] font-semibold uppercase tracking-wider">
                  <th class="text-left px-4 py-2.5">M\u00eas (2026)</th>
                  <th class="text-center px-4 py-2.5">Procedimentos</th>
                  <th class="text-right px-4 py-2.5">Receita Real</th>
                  <th class="text-right px-4 py-2.5 text-amber-400 bg-amber-500/5">Com Reajuste</th>
                  <th class="text-right px-4 py-2.5 text-emerald-400 bg-emerald-500/5">Diferen\u00e7a</th>
                </tr>
              </thead>
              <tbody id="tbFaturamento"></tbody>
              <tfoot>
                <tr class="bg-slate-800/80 font-bold border-t border-slate-700">
                  <td class="px-4 py-3 text-white">TOTAL TRIMESTRE</td>
                  <td class="text-center px-4 py-3 text-white">253</td>
                  <td class="text-right px-4 py-3 text-white">R$&nbsp;87.570,50</td>
                  <td class="text-right px-4 py-3 text-amber-400 bg-amber-500/10" id="tbFatTotSim">\u2014</td>
                  <td class="text-right px-4 py-3 text-emerald-400 bg-emerald-500/10" id="tbFatTotDif">\u2014</td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>

        <!-- Alerta de margem -->
        <div class="flex gap-2 items-start bg-red-950/30 rounded-lg p-3 border border-red-500/20">
          <span class="text-red-400 text-base shrink-0">&#9888;</span>
          <p class="text-slate-400 text-xs leading-relaxed">
            <strong class="text-red-400">Aten\u00e7\u00e3o \u2014 Margem em Risco:</strong>
            O saldo l\u00edquido Q1/2026 (R$&nbsp;11.300, margem 12,9%) \u00e9
            <strong class="text-red-400">45,6% menor</strong> que Q1/2025 (R$&nbsp;20.770, margem 22,6%).
            A receita caiu 4,7% enquanto as despesas subiram 7,3%.
            Sem reajuste, a proje\u00e7\u00e3o anual 2026 \u00e9 R$&nbsp;350.280. Use o simulador
            para ver o impacto de cada ponto percentual de ajuste sobre a receita dos pr\u00f3ximos meses.
          </p>
        </div>
      </section>

      <!-- ============================================================
           SE\u00c7\u00c3O 7 \u2013 TABELA DE PRE\u00c7OS'''

if idx_s >= 0 and idx_e >= 0:
    html = html[:idx_s] + NEW_SEC + html[idx_e + len(END_TAG):]
    print(f"2. Secao 6.5 substituida. Novo tamanho: {len(html)}")
else:
    print("ERRO: nao foi possivel localizar secao 6.5")

# ─── 3. Atualizar dados FATURAMENTO_REAL ─────────────────────────────────────
old_real = "    { mes: 'Mar\u00e7o',    procs: 71,  real: 24411.66 }"
new_real = "    { mes: 'Mar\u00e7o *',  procs: 71,  real: 24711.66 }   // * parcial ate 25/03"
if old_real in html:
    html = html.replace(old_real, new_real)
    print("3. Valor de marco atualizado: 24411 -> 24711")
else:
    print("3. AVISO: valor de marco nao encontrado")

# Adicionar constantes de projecao apos FAT_TOTAL_REAL
old_const = "  const FAT_TOTAL_REAL = FATURAMENTO_REAL.reduce((s, m) => s + m.real, 0);"
new_const = """  const FAT_TOTAL_REAL = FATURAMENTO_REAL.reduce((s, m) => s + m.real, 0);
  const FAT_MEDIA_MES  = FAT_TOTAL_REAL / FATURAMENTO_REAL.length;        // ~29190
  const FAT_PROJ_SEM   = FAT_TOTAL_REAL + FAT_MEDIA_MES * 9;              // ~350280"""
if old_const in html:
    html = html.replace(old_const, new_const)
    print("3b. Constantes FAT_MEDIA_MES e FAT_PROJ_SEM adicionadas")
else:
    print("3b. AVISO: FAT_TOTAL_REAL nao encontrado")

# ─── 4. Substituir função atualizarFaturamento ────────────────────────────────
# Localizar pelo inicio e fim da função
func_start = "  function atualizarFaturamento(pct) {"
func_end_marker = "\n  }"
idx_fs = html.find(func_start)
if idx_fs >= 0:
    idx_fe = html.find(func_end_marker, idx_fs)
    if idx_fe >= 0:
        old_func_block = html[idx_fs:idx_fe + len(func_end_marker)]
        new_func_block = """  function atualizarFaturamento(pct) {
    const mult   = 1 + pct / 100;
    const pctStr = pct.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';
    // Labels
    document.getElementById('txtFatSimPct').textContent = pctStr;
    document.getElementById('lblFatSimPct').textContent = 'Reajuste: ' + pctStr;
    // Tabela mensal
    let totSim = 0;
    let htmlTb = '';
    FATURAMENTO_REAL.forEach((m, i) => {
      const sim = m.real * mult;
      const dif = sim - m.real;
      totSim += sim;
      const rowBg = i % 2 === 0 ? 'bg-slate-800/30' : 'bg-transparent';
      htmlTb += '<tr class="' + rowBg + ' border-b border-slate-700/30 hover:bg-slate-800/50">'
        + '<td class="px-4 py-3 text-slate-300 font-medium">' + m.mes + '</td>'
        + '<td class="text-center px-4 py-3 text-slate-400">' + m.procs + '</td>'
        + '<td class="text-right px-4 py-3 text-slate-300 font-medium">' + brl(m.real) + '</td>'
        + '<td class="text-right px-4 py-3 text-amber-400 font-bold bg-amber-500/5">' + brl(sim) + '</td>'
        + '<td class="text-right px-4 py-3 text-emerald-400 font-bold bg-emerald-500/5">+' + brl(dif) + '</td>'
        + '</tr>';
    });
    const totDif   = totSim - FAT_TOTAL_REAL;
    const ganhoMes = totDif / FATURAMENTO_REAL.length;
    const projAno  = FAT_TOTAL_REAL + FAT_MEDIA_MES * 9 * mult;
    const ganhoAno = projAno - FAT_PROJ_SEM;
    // DOM updates
    document.getElementById('tbFaturamento').innerHTML   = htmlTb;
    document.getElementById('tbFatTotSim').textContent   = brl(totSim);
    document.getElementById('tbFatTotDif').textContent   = '+' + brl(totDif);
    document.getElementById('fatSimTotal').textContent   = brl(totSim);
    document.getElementById('valFatGanho').textContent   = '+' + brl(totDif);
    document.getElementById('fatMediaSim').textContent   = brl(FAT_MEDIA_MES * mult);
    document.getElementById('valFatGanhoMes').textContent = brl(ganhoMes);
    document.getElementById('fatProjecaoAno').textContent = brl(projAno);
    document.getElementById('valFatGanhoAno').textContent = '+' + brl(ganhoAno);
  }"""
        html = html.replace(old_func_block, new_func_block)
        print("4. atualizarFaturamento substituida")
    else:
        print("4. ERRO: fim da funcao nao encontrado")
else:
    print("4. ERRO: inicio da funcao nao encontrado")

# ─── 5. Gravar ───────────────────────────────────────────────────────────────
with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"\ndashboard.html salvo: {len(html)} bytes")
