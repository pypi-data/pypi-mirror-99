import subprocess
from subprocess import check_output, Popen, PIPE
import pip
import os

#  envs = subprocess.check_output('conda env list', shell=True, encoding='utf-8').splitlines()
#  active_env = list(filter(lambda s: '*' in str(s), envs))[0]
#  print(active_env)
#  env_name = str(active_env).split()[0]
#  print(env_name)

# subprocess.run('conda activate tins_corelibs', shell=True)

#  output = subprocess.check_output("conda env list", shell=True, encoding='utf-8')
#  print(output)

# subprocess.Popen("conda activate tins_corelibs",
#                  shell=True,
#                  stdout=open(r"D:\OneDrive\Documents\TMP\test_requirement.txt", "w"))


# print(pip.main(['list']))
# print([p.project_name + "==" + p.version for p in pip._vendor.pkg_resources.working_set])  # p.location, p.egg_name

# subprocess.run([
#     r"%windir%\System32\cmd.exe",
#     "/K",
#     r"C:\ProgramData\Anaconda3\Scripts\activate.bat",
#     r"C:\ProgramData\Anaconda3"
# ], shell=True)

# subprocess.run(r"C:\ProgramData\Anaconda3\Scripts\conda list -n corelibs -e > C:\Users\miki\corelibs_vp_requirements.txt", shell=True)  # ça marche!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# subprocess.run(r"C:\ProgramData\Anaconda3\Scripts\conda activate tins_corelibs", shell=True)
# subprocess.run(r"C:\ProgramData\Anaconda3\Scripts\conda env list", shell=True)

# Ajouter "C:\ProgramData\Anaconda3\Scripts" dans ENV PATH


# https://stackoverflow.com/questions/11712629/opening-a-python-thread-in-a-new-console-window
# command = r"where /R C: Anaconda"
# subprocess.run(["cmd.exe", "/c", "start", f"{command}"])

# https://datatofish.com/command-prompt-python/
# command = "dir"
# subprocess.run(["cmd.exe", "/c", "start", f"{command}"], timeout=15)

# import os
# os.system('cmd /k "color a & date"')


# out = check_output([r"C:\ProgramData\Anaconda3\Scripts\conda", "env", "list"])
# print(out)

pipe = Popen(r"C:\ProgramData\Anaconda3\Scripts\conda env list", stdout=PIPE, encoding="utf-8")
text = pipe.communicate()[0]
print(text)

# cmd = r"C:\ProgramData\Anaconda3\Scripts\conda list -n tins_corelibs"
# pipe = Popen(cmd, stdout=PIPE, encoding="utf-8")
# text = pipe.communicate()[0]
# for i, t in enumerate(text.splitlines()):
#     if i == 2:
#         header = [h for h in t.split(" ") if h]
#         print(header[0].rjust(5), header[1].ljust(47), header[2].rjust(23), header[3].rjust(23), header[4].rjust(23))
#     elif i > 2:
#         body = [b for b in t.split(" ") if b]
#         print(str(i - 2).rjust(5), body[0].ljust(47), body[1].rjust(23), body[2].rjust(23), (body[3].rjust(23) if len(body) == 4 else ""))


# pip freeze
# pip list --format=freeze --path "C:\ProgramData\Anaconda3\envs\corelibs\Lib\site-packages" > corelibs_requirements.txt

# conda list -n corelibs -e > corelibs_conda_requirements.txt
