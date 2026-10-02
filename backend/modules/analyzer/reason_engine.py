# =====================================================
# iVerify V2 - Advanced Reason Engine
# Sosyal Medya Veri Analiz Motoru
# =====================================================


class ReasonEngine:


    def __init__(self):

        self.version = "2.0"



    # =================================================
    # Güven puanı
    # =================================================

    def confidence(
            self,
            score=100
    ):


        if score >= 90:

            level = "high"

        elif score >= 70:

            level = "medium"

        else:

            level = "low"



        return {

            "score": score,

            "level": level

        }



    # =================================================
    # Geri takip yok
    # =================================================

    def generate_not_following_back_reason(
            self,
            username
    ):


        return {


            "username": username,


            "category":
            "geri_takip_yok",



            "reason":

            f"{username} hesabı sizin tarafınızdan takip ediliyor ancak sizi takip etmiyor.",



            "evidence":[

                "following listesinde mevcut",

                "followers listesinde bulunamadı"

            ],



            "confidence":

            self.confidence(98),



            "risk":

            "medium"



        }



    # =================================================
    # Sadece takip eden
    # =================================================

    def generate_followers_only_reason(
            self,
            username
    ):


        return {


            "username": username,


            "category":
            "sadece_takip_edenler",



            "reason":

            f"{username} hesabı sizi takip ediyor ancak sizin takip listenizde bulunmuyor.",



            "evidence":[

                "followers listesinde mevcut",

                "following listesinde bulunamadı"

            ],



            "confidence":

            self.confidence(98),



            "risk":

            "low"



        }



    # =================================================
    # Ortak takip
    # =================================================

    def generate_mutual_reason(
            self,
            username
    ):


        return {


            "username": username,


            "category":
            "ortak_takip",



            "reason":

            f"{username} hesabı ile karşılıklı takip ilişkisi mevcut.",



            "evidence":[

                "followers listesinde mevcut",

                "following listesinde mevcut"

            ],



            "confidence":

            self.confidence(100),



            "risk":

            "low"



        }



    # =================================================
    # Genel üretici
    # =================================================

    def create_reason(
            self,
            username,
            category
    ):


        handlers = {


            "geri_takip_yok":
            self.generate_not_following_back_reason,


            "sadece_takip_edenler":
            self.generate_followers_only_reason,


            "ortak_takip":
            self.generate_mutual_reason

        }



        if category in handlers:


            return handlers[category](
                username
            )



        return {


            "username":

            username,


            "category":

            category,


            "reason":

            "Bu kategori için detaylı analiz açıklaması bulunamadı.",



            "confidence":

            self.confidence(50),



            "risk":

            "unknown"

        }