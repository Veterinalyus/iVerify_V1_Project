# =====================================================
# iVerify V2 - Instagram Parser
# Sosyal Medya Veri Analiz Motoru
# =====================================================

import json
from pathlib import Path



class InstagramParser:


    def __init__(self):

        self.data = {}

        self.users = []



    # -------------------------------------------------
    # JSON dosyası okuma
    # -------------------------------------------------

    def load_json(self, file_path):

        file_path = Path(file_path)


        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)


        except Exception:

            return None



    # -------------------------------------------------
    # Dosya türünü tahmin etme
    # -------------------------------------------------

    def detect_type(self, file_name):

        name = file_name.lower()



        if "followers" in name:

            return "followers"



        if "following" in name:

            return "following"



        if "blocked" in name:

            return "blocked"



        if "restricted" in name:

            return "restricted"



        if "close" in name and "friend" in name:

            return "close_friends"



        if "request" in name:

            return "requests"



        if "contact" in name:

            return "contacts"



        return "unknown"




    # -------------------------------------------------
    # Kullanıcı çıkarma
    # -------------------------------------------------

    def extract_users(self, data):


        users = []



        if isinstance(data, list):


            for item in data:


                user = self.parse_user(item)


                if user:

                    users.append(user)



        elif isinstance(data, dict):


            for key, value in data.items():


                if isinstance(value, list):


                    for item in value:


                        user = self.parse_user(item)


                        if user:

                            users.append(user)



        return users




    # -------------------------------------------------
    # Tek kullanıcı çözümleme
    # -------------------------------------------------

    def parse_user(self, item):


        if not isinstance(item, dict):

            return None



        username = None

        link = None

        timestamp = None



        # Meta yeni format

        if "string_list_data" in item:


            data = item.get(
                "string_list_data"
            )


            if data and isinstance(data, list):


                first = data[0]


                username = first.get(
                    "value"
                )


                link = first.get(
                    "href"
                )


                timestamp = first.get(
                    "timestamp"
                )



        # Basit format

        if not username:


            username = item.get(
                "value"
            )



        if not username:


            username = item.get(
                "username"
            )



        return {


            "username":

            username,


            "link":

            link,


            "timestamp":

            timestamp

        }




    # -------------------------------------------------
    # Instagram klasörü analiz etme
    # -------------------------------------------------

    def parse_folder(self, folder_path):


        folder_path = Path(folder_path)


        results = {}



        for file in folder_path.rglob("*.json"):


            file_type = self.detect_type(
                file.name
            )


            json_data = self.load_json(
                file
            )


            if json_data:


                users = self.extract_users(
                    json_data
                )


                results[file_type] = users



        self.data = results


        return results