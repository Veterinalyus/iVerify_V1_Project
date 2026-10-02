# =====================================================
# iVerify V2 - Main Analyzer Engine
# Sosyal Medya Veri Analiz Motoru
# =====================================================


from backend.modules.analyzer.validator import DataValidator
from backend.modules.analyzer.json_parser import JSONParser
from backend.modules.analyzer.relationship_engine import RelationshipEngine
from backend.modules.analyzer.date_engine import DateEngine
from backend.modules.analyzer.reason_engine import ReasonEngine



class AnalyzerEngine:


    def __init__(self):

        self.validator = DataValidator()

        self.parser = JSONParser()

        self.relationship = RelationshipEngine()

        self.date_engine = DateEngine()

        self.reason_engine = ReasonEngine()



        self.result = {


            "metadata": {},

            "users": [],

            "categories": {},

            "audit": {}

        }



    # -------------------------------------------------
    # Ana analiz başlangıcı
    # -------------------------------------------------

    def analyze_json_files(
            self,
            json_files
    ):


        parsed_data = []



        # 1 - Dosya kontrolü

        for file in json_files:


            valid = self.validator.validate_json(
                file
            )


            if valid:

                parsed_data.append(
                    file
                )



        self.result["metadata"][

            "validated_files"

        ] = len(parsed_data)




        # 2 - JSON verilerini oku

        all_users = []



        for file in parsed_data:


            data = self.parser.load_json(
                file
            )


            if data:


                users = self.parser.parse_users(
                    data
                )


                all_users.extend(
                    users
                )



        self.result["users"] = all_users




        return self.result




    # -------------------------------------------------
    # Takip analizi
    # -------------------------------------------------

    def analyze_relationships(
            self,
            followers,
            following
    ):


        relationship_result = self.relationship.analyze(

            followers,

            following

        )


        self.result["categories"] = relationship_result


        return relationship_result




    # -------------------------------------------------
    # Tarih ekleme
    # -------------------------------------------------

    def add_dates(
            self,
            users
    ):


        updated_users = []


        for user in users:


            date_info = self.date_engine.analyze_user_date(

                user

            )


            user.update(

                date_info

            )


            updated_users.append(
                user
            )


        self.result["users"] = updated_users


        return updated_users




    # -------------------------------------------------
    # Sonuç üret
    # -------------------------------------------------

    def finalize(self):


        self.result["audit"] = {


            "engine":

            "iVerify V2 Analyzer",


            "status":

            "completed"


        }


        return self.result