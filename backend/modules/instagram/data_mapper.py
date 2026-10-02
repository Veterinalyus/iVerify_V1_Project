# =====================================================
# iVerify V2 - Data Mapper
# Sosyal Medya Veri Analiz Motoru
# =====================================================


from datetime import datetime



class DataMapper:


    def __init__(self):

        self.mapped_users = []



    # -------------------------------------------------
    # Tarih formatlama
    # -------------------------------------------------

    def format_date(self, timestamp):


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
    # Kullanıcı standartlaştırma
    # -------------------------------------------------

    def map_user(
            self,
            user,
            source
    ):


        return {


            "username":
            user.get("username"),


            "link":
            user.get("link"),


            "source":
            source,


            "timestamp":
            user.get("timestamp"),


            "date":
            self.format_date(
                user.get("timestamp")
            ),


            "relations":{

                "follower": False,

                "following": False,

                "blocked": False,

                "restricted": False

            },


            "categories": [],


            "analysis":{

                "reason": None,

                "confidence": None,

                "evidence": [],

                "risk": None

            }

        }



    # -------------------------------------------------
    # Liste dönüşümü
    # -------------------------------------------------

    def map_users(
            self,
            users,
            source
    ):


        result = []


        for user in users:


            mapped = self.map_user(
                user,
                source
            )


            if mapped["username"]:

                result.append(
                    mapped
                )



        self.mapped_users.extend(
            result
        )


        return result



    # -------------------------------------------------
    # İlişki ekleme
    # -------------------------------------------------

    def add_relation(
            self,
            user,
            relation
    ):


        if relation in user["relations"]:

            user["relations"][relation] = True



    # -------------------------------------------------
    # Kategori ekleme
    # -------------------------------------------------

    def add_category(
            self,
            user,
            category
    ):


        if category not in user["categories"]:

            user["categories"].append(
                category
            )



    # -------------------------------------------------
    # Sonuç
    # -------------------------------------------------

    def get_result(self):

        return self.mapped_users