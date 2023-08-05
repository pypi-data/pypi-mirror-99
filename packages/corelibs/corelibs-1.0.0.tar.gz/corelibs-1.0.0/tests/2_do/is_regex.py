import re


def _is_validated_renamed_file_name(replace):
    print(replace)
    forbidden_char = r"[\\\/:*?\"<>\|]"
    rec = re.compile(forbidden_char)

    if rec.search(replace):
        print("KO")
        return False

    return True


print(_is_validated_renamed_file_name(
    r"D:\OneDrive\Documents\_TEST_\_TEST_RENOMMAGE_\nouveau\\\/:*?\"<>|_cars.sas7bdat"
))