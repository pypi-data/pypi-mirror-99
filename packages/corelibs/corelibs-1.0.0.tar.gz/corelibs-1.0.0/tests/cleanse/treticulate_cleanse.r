# treticulate_clease.r
# exemple appel des fonctions du package corelibs depuis R...

# install.packages("reticulate")  # si n'existe pas...
# install.packages("readr")

library("reticulate")
library(readr)

reticulate::use_condaenv(condaenv="test_conda", required=TRUE)
cleanse <- reticulate::import("corelibs.cleanse", delay_load=TRUE)

file_2_cleanse <- read_file(file="D:\\OneDrive\\Desktop\\Alex_L_LD.txt")

data <- cleanse$is_str(file_2_cleanse, chars_2_replace="Ã©", replaced_chars="é")
data <- cleanse$is_str(file_2_cleanse, chars_2_replace="Ã´", replaced_chars="ô")
data <- cleanse$is_str(file_2_cleanse, chars_2_replace="Ã§", replaced_chars="ç")
data <- cleanse$is_str(file_2_cleanse, chars_2_replace="Ã‡", replaced_chars="C")

data <- cleanse$replace(
  data,
  search="((([-\\w',çéô Ç]* )*(<[-\\w.@]*>)|([\\w .@]*)))(;)",
  replace="\\1\\n"
)

data <- cleanse$replace(data, "(^[ ]+)?(.*)", "\\2")

f <- py_run_string("
def name_2_upper(m):
    return m.groups()[1] + \" \" + m.groups()[0].upper()[:-1] + \" \" + m.groups()[2]
")
data <- cleanse$replace(
  data,
  "'(.*),? (.*)' (.*)",
  f$name_2_upper
)

f <- py_run_string("
def mail_2_name(m):
    return m.groups()[0].title() + \" \" + m.groups()[1].upper() + \" <\" + m.groups()[0].lower() + \".\" + m.groups()[1].lower() + m.groups()[2].lower() + \">\"
")
data <- cleanse$replace(
  data,
  "^(?!(?:DOCUMENTATION).*$)(\\w*).(\\w*)(@[\\w.]*)",
  f$mail_2_name
)

data <- cleanse$replace(
  data,
  "(([A-Z][-,a-zéèôç. ']+[ ]*)+) (([-A-Z ]+) ?)+ <(.*)>",
  "\\1;\\3;\\5"
)

data <- cleanse$replace(
  data,
  "^(?!(.*;){2}(.*))([\\w\\- ]+) <?([\\w.@]*)>?",
  "\\3;;\\4;VALIDATION MANUELLE"
)

f_out <- file("D:\\OneDrive\\Desktop\\Alex_L_LD_FORMATED_BY_R.txt")
writeLines(data, f_out)
close(f_out)
