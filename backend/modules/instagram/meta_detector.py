# =====================================================
# iVerify V2 - Meta Export Detector
# Sosyal Medya Veri Analiz Motoru
# =====================================================

from pathlib import Path



class MetaDetector:


    def __init__(self):

        self.detected_files = []

        self.available_data = {

            "followers": False,

            "following": False,

            "blocked": False,

            "restricted": False,

            "close_friends": False,

            "requests": False,

            "contacts": False

        }



    # -------------------------------------------------
    # Klasör kontrolü
    # -------------------------------------------------

    def scan_folder(self, folder_path):


        folder_path = Path(folder_path)


        if not folder_path.exists():

            return {

                "status": "error",

                "message":
                "Klasör bulunamadı."

            }



        files = list(
            folder_path.rglob("*")
        )


        self.detected_files = files


        self.detect_files()


        return self.get_report()



    # -------------------------------------------------
    # Dosyaları tanıma
    # -------------------------------------------------

    def detect_files(self):


        for file in self.detected_files:


            if not file.is_file():

                continue



            name = file.name.lower()



            # Takipçiler

            if "followers" in name:

                self.available_data["followers"] = True



            # Takip edilenler

            if "following" in name:

                self.available_data["following"] = True



            # Engellenenler

            if "blocked" in name:

                self.available_data["blocked"] = True



            # Kısıtlananlar

            if "restricted" in name:

                self.available_data["restricted"] = True



            # Yakın arkadaşlar

            if "close" in name and "friend" in name:

                self.available_data["close_friends"] = True



            # İstekler

            if "request" in name:

                self.available_data["requests"] = True



            # Kişiler

            if "contact" in name:

                self.available_data["contacts"] = True




    # -------------------------------------------------
    # Instagram export kontrolü
    # -------------------------------------------------

    def is_instagram_export(self):


        found = 0


        for value in self.available_data.values():

            if value:

                found += 1



        return found > 0




    # -------------------------------------------------
    # Rapor oluşturma
    # -------------------------------------------------

    def get_report(self):


        return {


            "is_instagram_export":

            self.is_instagram_export(),



            "detected_file_count":

            len(self.detected_files),



            "available_data":

            self.available_data



        }