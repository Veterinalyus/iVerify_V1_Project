# =====================================================
# iVerify V2 - Data Validator
# Sosyal Medya Veri Analiz Motoru
# =====================================================

from pathlib import Path
import json



class DataValidator:


    def __init__(self):

        self.errors = []

        self.warnings = []

        self.valid_files = []



    # -------------------------------------------------
    # Dosya var mı kontrolü
    # -------------------------------------------------

    def check_file_exists(self, file_path):

        file_path = Path(file_path)


        if not file_path.exists():

            self.errors.append(
                f"Dosya bulunamadı: {file_path}"
            )

            return False


        return True



    # -------------------------------------------------
    # JSON okunabilir mi?
    # -------------------------------------------------

    def validate_json(self, file_path):

        file_path = Path(file_path)


        if not self.check_file_exists(file_path):

            return False


        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)



            if data is None:

                self.warnings.append(
                    f"Boş veri: {file_path.name}"
                )

                return False



            self.valid_files.append(
                file_path.name
            )


            return True



        except json.JSONDecodeError:


            self.errors.append(
                f"Bozuk JSON dosyası: {file_path.name}"
            )


            return False



        except Exception as error:


            self.errors.append(
                str(error)
            )


            return False




    # -------------------------------------------------
    # Liste içindeki tekrarları kontrol eder
    # -------------------------------------------------

    def remove_duplicates(self, items):


        if not isinstance(items, list):

            return items



        cleaned = []

        seen = set()


        for item in items:


            item_text = str(item)


            if item_text not in seen:

                seen.add(item_text)

                cleaned.append(item)



        return cleaned




    # -------------------------------------------------
    # Sonuç raporu
    # -------------------------------------------------

    def get_report(self):


        return {


            "valid_files":
            self.valid_files,


            "errors":
            self.errors,


            "warnings":
            self.warnings,


            "status":
            "ready"
            if not self.errors
            else "failed"


        }