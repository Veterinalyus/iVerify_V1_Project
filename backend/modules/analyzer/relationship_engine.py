# =====================================================
# iVerify V2 - Relationship Analysis Engine V2
# Sosyal Medya Veri Analiz Motoru
# =====================================================


from backend.modules.analyzer.reason_engine import (
    ReasonEngine
)



class RelationshipEngine:


    def __init__(self):

        self.results = []

        self.reason_engine = ReasonEngine()



    # -------------------------------------------------
    # Kullanıcı normalize
    # -------------------------------------------------

    def normalize_users(
            self,
            users
    ):


        normalized = set()


        for user in users:


            if isinstance(user, dict):

                username = user.get(
                    "username"
                )

            else:

                username = user



            if username:

                normalized.add(
                    username.lower()
                )



        return normalized



    # -------------------------------------------------
    # Ortak takip
    # -------------------------------------------------

    def analyze_mutual_followers(
            self,
            followers,
            following
    ):


        followers_set = self.normalize_users(
            followers
        )


        following_set = self.normalize_users(
            following
        )


        mutual = followers_set.intersection(
            following_set
        )


        result = []


        for username in mutual:


            result.append(

                self.reason_engine.create_reason(
                    username,
                    "ortak_takip"
                )

            )


        return result



    # -------------------------------------------------
    # Geri takip yok
    # -------------------------------------------------

    def analyze_not_following_back(
            self,
            followers,
            following
    ):


        followers_set = self.normalize_users(
            followers
        )


        following_set = self.normalize_users(
            following
        )


        result = []



        for username in following_set:


            if username not in followers_set:


                result.append(

                    self.reason_engine.create_reason(
                        username,
                        "geri_takip_yok"
                    )

                )



        return result



    # -------------------------------------------------
    # Sadece takip edenler
    # -------------------------------------------------

    def analyze_followers_only(
            self,
            followers,
            following
    ):


        followers_set = self.normalize_users(
            followers
        )


        following_set = self.normalize_users(
            following
        )


        result = []



        for username in followers_set:


            if username not in following_set:


                result.append(

                    self.reason_engine.create_reason(
                        username,
                        "sadece_takip_edenler"
                    )

                )



        return result



    # -------------------------------------------------
    # Genel analiz
    # -------------------------------------------------

    def analyze(
            self,
            followers,
            following
    ):


        return {


            "mutual_followers":

            self.analyze_mutual_followers(
                followers,
                following
            ),



            "not_following_back":

            self.analyze_not_following_back(
                followers,
                following
            ),



            "followers_only":

            self.analyze_followers_only(
                followers,
                following
            )

        }