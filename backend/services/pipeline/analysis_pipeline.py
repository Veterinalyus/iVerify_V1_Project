# =====================================================
# iVerify V2 - Analysis Pipeline Core V5
# Sosyal Medya Veri Analiz Motoru
# =====================================================


from pathlib import Path


from backend.modules.instagram.meta_detector import (
    MetaDetector
)

from backend.modules.instagram.instagram_parser import (
    InstagramParser
)

from backend.modules.instagram.data_mapper import (
    DataMapper
)

from backend.modules.analyzer.relationship_engine import (
    RelationshipEngine
)

from backend.modules.analyzer.reason_engine import (
    ReasonEngine
)

from backend.modules.zip_engine.zip_reader import (
    check_zip_file,
    extract_zip
)

from backend.services.audit.audit_manager import (
    AuditManager
)

from backend.services.database.database import (
    get_connection
)



class AnalysisPipeline:


    def __init__(self):


        self.detector = MetaDetector()

        self.parser = InstagramParser()

        self.mapper = DataMapper()

        self.relationship = RelationshipEngine()

        self.reason = ReasonEngine()

        self.audit = AuditManager()



    # =================================================
    # ZIP / KLASÖR HAZIRLAMA
    # =================================================


    def prepare_input(
            self,
            input_path
    ):


        path = Path(
            input_path
        )



        if path.is_file() and path.suffix.lower() == ".zip":


            if not check_zip_file(path):

                raise Exception(
                    "Geçersiz ZIP dosyası."
                )



            output_folder = (
                path.parent /
                "extracted_analysis"
            )



            return extract_zip(
                path,
                output_folder
            )



        if path.is_dir():

            return path



        raise Exception(
            "Geçerli ZIP veya klasör bulunamadı."
        )



    # =================================================
    # DATABASE KAYIT
    # =================================================


    def save_to_database(
            self,
            result,
            audit_record
    ):


        connection = get_connection()

        cursor = connection.cursor()



        cursor.execute(
            """
            INSERT INTO analyses
            (
                analysis_id,
                filename,
                created_at,
                total_users,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                audit_record["analysis_id"],
                audit_record["filename"],
                audit_record["created_at"],
                audit_record["total_users"],
                audit_record["status"]
            )
        )



        for category, users in result["users"].items():


            for user in users:


                cursor.execute(
                    """
                    INSERT INTO users
                    (
                        username,
                        category,
                        source,
                        discovered_at,
                        reason
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        user.get("username"),
                        category,
                        user.get("source"),
                        user.get("date"),
                        user.get("analysis", {}).get("reason")
                    )
                )



        cursor.execute(
            """
            INSERT INTO audit_logs
            (
                action,
                created_at,
                details
            )
            VALUES (?, ?, ?)
            """,
            (
                "analysis_completed",
                audit_record["created_at"],
                str(audit_record)
            )
        )



        connection.commit()

        connection.close()
    # =================================================
    # Reason sonuçlarını kullanıcı kayıtlarına bağlama
    # =================================================


    def attach_reason_analysis(
            self,
            mapped_data,
            relationship_result
    ):


        reason_items = []



        reason_items.extend(
            relationship_result.get(
                "not_following_back",
                []
            )
        )



        reason_items.extend(
            relationship_result.get(
                "followers_only",
                []
            )
        )



        reason_items.extend(
            relationship_result.get(
                "mutual_followers",
                []
            )
        )



        for category_users in mapped_data.values():


            for user in category_users:


                username = user.get(
                    "username"
                )



                for reason in reason_items:


                    if reason.get(
                        "username"
                    ) == username:


                        user["analysis"] = {


                            "reason":

                            reason.get(
                                "reason"
                            ),



                            "confidence":

                            reason.get(
                                "confidence"
                            ),



                            "evidence":

                            reason.get(
                                "evidence",
                                []
                            ),



                            "risk":

                            reason.get(
                                "risk"
                            )

                        }



        return mapped_data





    # =================================================
    # ANA ANALİZ AKIŞI
    # =================================================


    def run(
            self,
            input_path
    ):


        audit_record = self.audit.create_analysis_record(
            str(input_path)
        )



        try:


            folder = self.prepare_input(
                input_path
            )



            print(
                "iVerify analiz başladı..."
            )



            # -----------------------------------------
            # Meta kontrol
            # -----------------------------------------


            meta_report = self.detector.scan_folder(
                folder
            )



            if not meta_report["is_instagram_export"]:


                self.audit.fail_analysis(
                    audit_record,
                    "Instagram export bulunamadı."
                )



                return {


                    "status":

                    "failed",



                    "reason":

                    "Geçerli Meta arşivi yok."

                }




            # -----------------------------------------
            # JSON okuma
            # -----------------------------------------


            instagram_data = self.parser.parse_folder(
                folder
            )



            mapped_data = {}

            total_users = 0



            for category, users in instagram_data.items():


                mapped_users = self.mapper.map_users(
                    users,
                    category
                )



                mapped_data[category] = mapped_users



                total_users += len(
                    mapped_users
                )



            self.audit.update_user_count(
                audit_record,
                total_users
            )



            # -----------------------------------------
            # İlişki analizi
            # -----------------------------------------


            followers = mapped_data.get(
                "followers",
                []
            )



            following = mapped_data.get(
                "following",
                []
            )



            relationship_result = self.relationship.analyze(
                followers,
                following
            )



            mapped_data = self.attach_reason_analysis(
                mapped_data,
                relationship_result
            )



            # -----------------------------------------
            # Sonuç
            # -----------------------------------------


            result = {


                "status":

                "completed",



                "meta":

                meta_report,



                "users":

                mapped_data,



                "relationships":

                relationship_result,



                "audit":

                audit_record

            }



            self.audit.complete_analysis(
                audit_record
            )



            self.save_to_database(
                result,
                audit_record
            )



            return result



        except Exception as error:


            self.audit.fail_analysis(
                audit_record,
                error
            )



            return {


                "status":

                "error",



                "error":

                str(error),



                "audit":

                audit_record

            }