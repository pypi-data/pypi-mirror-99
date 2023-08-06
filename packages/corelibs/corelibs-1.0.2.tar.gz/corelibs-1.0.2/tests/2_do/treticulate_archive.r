# install.packages("reticulate")  # si n'existe pas...
library("reticulate")

reticulate::use_condaenv(condaenv="test_conda", required=TRUE)
lazy <- reticulate::import("corelibs.lazy", delay_load=TRUE)
tools <- reticulate::import("corelibs.tools", delay_load=TRUE)

lazy$mkdir("D:\\OneDrive\\Desktop\\_test_\\folder_from_r")  # création répertoires avec scaffolding par défaut

archive <- tools$Archive()  # instanciation Archive()
zip_file <- gsub(  # nom fichier dynamique avec un timestamp
  " ",
  "",
  paste("D:\\OneDrive\\Desktop\\_test_\\folder_from_r\\MON_ARCHIVE_", lazy$get_timestamp())
)
src_file <- "D:\\OneDrive\\Desktop\\StockEtablissement_utf8\\StockEtablissement_utf8_h65k.csv"

exit_code <- archive$zip(  # zip
    archive_name=zip_file,
    files_2_zip=src_file
)

if (exit_code == 0) {
  print("L'archivage s'est terminé avec succès et le fichier source a été supprimé")
  lazy$delete_files(src_file)  # suppression fichier source
}

yaml_file <- gsub(  # dézip en passant par le fichier yaml auto généré lors du zip...
  " ",
  "",
  paste(zip_file, ".yaml")
)
exit_code <- archive$unzip(yaml_file=yaml_file)

if (exit_code == 0) {
  print(
    paste(
      "Le désarchivage s'est terminé correctement, vous le trouverez à son emplacement originel...",
      gsub("\\\\", "/", src_file)
    )
  )
} else {
  print(
    paste(
      "Le désarchivage s'est terminé avec le code erreur:",
      exit_code
    )
  )
}