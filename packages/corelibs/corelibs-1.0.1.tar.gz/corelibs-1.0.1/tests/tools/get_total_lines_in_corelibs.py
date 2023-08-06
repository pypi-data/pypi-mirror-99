# get_total_lines_in_folder.py
from corelibs import tools as to


# exclusions finales
wcl = to.get_total_lines_in_folder(
    dir_2_scan=r"D:\OneDrive\Documents\[PYTHON_PROJECTS]\corelibs",
    files_pattern="*.py",
    to_exclude=(r"*build*", r"*egg-info*", r"*dist*", r"*docs*")
)
print(wcl)
