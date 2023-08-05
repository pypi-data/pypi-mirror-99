import codecs


BLOCKSIZE = 1048576  # or some other, desired size in bytes

with codecs.open(r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8_tail_preview.tsv",
                 "r",
                 "utf-8") as sourceFile:
    with codecs.open(r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8_tail_preview_latin.tsv",
                     "w",
                     "iso-8859-1",
                     errors="ignore") as targetFile:
        while True:
            contents = sourceFile.read(BLOCKSIZE)
            if not contents:
                break
            targetFile.write(contents)


# %%
print("-\x8F-")  # latin-1 supp char
