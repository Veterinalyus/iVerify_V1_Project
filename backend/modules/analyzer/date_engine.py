# =====================================================
# iVerify V2 - Date Analysis Engine
# Sosyal Medya Veri Analiz Motoru
# =====================================================

from datetime import datetime



class DateEngine:


    def __init__(self):

        self.supported_fields = [

            "timestamp",
            "created_at",
            "updated_at",
            "date",
            "time"

        ]



    # -------------------------------------------------
    # Timestamp dönüştürme
    # -------------------------------------------------

    def convert_timestamp(self, timestamp):

        if not timestamp:

            return None


        try:

            return datetime.fromtimestamp(
                int(timestamp)
            ).strftime(
                "%d.%m.%Y %H:%M"
            )


        except Exception:

            return None



    # -------------------------------------------------
    # Tarih alanı arama
    # -------------------------------------------------

    def find_date(self, data):


        if not isinstance(data, dict):

            return {

                "date": None,

                "source": None,

                "status":
                "Meta verisi bulunamadı"

            }



        # Önce timestamp kontrolü

        if "timestamp" in data:


            converted = self.convert_timestamp(
                data["timestamp"]
            )


            if converted:


                return {

                    "date":
                    converted,

                    "source":
                    "timestamp",

                    "status":
                    "bulundu"

                }



        # Diğer tarih alanları

        for field in self.supported_fields:


            if field in data:


                value = data[field]


                if value:


                    return {

                        "date":
                        str(value),

                        "source":
                        field,

                        "status":
                        "bulundu"

                    }



        return {

            "date":
            None,

            "source":
            None,

            "status":
            "Meta verisinde tarih bulunamadı"

        }




    # -------------------------------------------------
    # Kullanıcı tarih analizi
    # -------------------------------------------------

    def analyze_user_date(self, user):


        result = self.find_date(
            user
        )


        return {


            "username":
            user.get(
                "username"
            ),


            "date":
            result["date"],


            "date_source":
            result["source"],


            "date_status":
            result["status"]

        }




    # -------------------------------------------------
    # Tarih karşılaştırma
    # -------------------------------------------------

    def compare_dates(
            self,
            old_date,
            new_date
    ):


        return {


            "old":

            old_date,


            "new":

            new_date,


            "changed":

            old_date != new_date

        }