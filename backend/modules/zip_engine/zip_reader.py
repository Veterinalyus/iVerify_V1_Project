# =====================================================
# iVerify V2 - ZIP Reader
# Sosyal Medya Veri Analiz Motoru
# =====================================================

import zipfile
from pathlib import Path



def check_zip_file(zip_path):

    """
    ZIP dosyası geçerli mi kontrol eder.
    """

    zip_path = Path(zip_path)

    if not zip_path.exists():
        return False


    if zip_path.suffix.lower() != ".zip":
        return False


    return True




def extract_zip(zip_path, output_folder):

    """
    ZIP dosyasını belirtilen klasöre çıkarır.
    """

    zip_path = Path(zip_path)
    output_folder = Path(output_folder)


    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )


    with zipfile.ZipFile(
        zip_path,
        "r"
    ) as archive:

        archive.extractall(
            output_folder
        )


    return output_folder




def find_json_files(folder):

    """
    Çıkarılan klasör içinde JSON dosyalarını bulur.
    """

    folder = Path(folder)

    json_files = list(
        folder.rglob("*.json")
    )


    return json_files