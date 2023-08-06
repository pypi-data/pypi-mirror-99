# progress_bar.py
# %%

from corelibs import log, tools

# /!\ ATTENTION /!\
#     Jupyter Notebook n'étant pas un terminal, il ne se passera rien... =}
# Instanciations
sb = log.StatusBars()
cl = log.TermColorLog(output_2_log_file=False)


# %%
# Progress bar sur un fichier
fichier = r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8_head_preview.csv"

total_iteration = tools.get_total_lines_in_file(fichier) - 1  # dernière ligne à blanc comme dans tous fichiers plats
pb_1 = sb.init_progress_bar(total=total_iteration - 1, color="magenta")  # initialisation barre de progression

with open(fichier) as f_in:
    for i, f in enumerate(f_in):
        cl.info(f"N° : {i} - Valeur lue : {f}")  # ou process quelconque...
        duree_etape = sb.update_progress_bar(
            pb_1,
            status_text=f"{i + 1: >{3}}/{total_iteration - 1} - Reste {(total_iteration - i - 2): >{3}}"
        )

duree_totale = sb.terminate()
cl.info(duree_totale)
