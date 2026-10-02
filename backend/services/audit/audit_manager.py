# =====================================================
# iVerify V2 - Audit Manager
# Sosyal Medya Veri Analiz Motoru
# =====================================================


from datetime import datetime
import uuid



class AuditManager:


    def __init__(self):

        self.logs = []



    # -------------------------------------------------
    # Yeni analiz kaydı oluştur
    # -------------------------------------------------

    def create_analysis_record(
            self,
            filename=None
    ):


        record = {


            "analysis_id":

            str(uuid.uuid4()),



            "filename":

            filename,



            "created_at":

            datetime.now().strftime(
                "%d.%m.%Y %H:%M:%S"
            ),



            "status":

            "started",



            "total_users":

            0



        }



        self.logs.append(
            record
        )


        return record




    # -------------------------------------------------
    # Kullanıcı sayısını güncelle
    # -------------------------------------------------

    def update_user_count(
            self,
            record,
            count
    ):


        record["total_users"] = count


        return record




    # -------------------------------------------------
    # Analiz tamamlandı
    # -------------------------------------------------

    def complete_analysis(
            self,
            record
    ):


        record["status"] = "completed"


        record["completed_at"] = datetime.now().strftime(
            "%d.%m.%Y %H:%M:%S"
        )


        return record




    # -------------------------------------------------
    # Hata kaydı
    # -------------------------------------------------

    def fail_analysis(
            self,
            record,
            error
    ):


        record["status"] = "failed"


        record["error"] = str(error)


        return record




    # -------------------------------------------------
    # Tüm kayıtları getir
    # -------------------------------------------------

    def get_logs(self):


        return self.logs