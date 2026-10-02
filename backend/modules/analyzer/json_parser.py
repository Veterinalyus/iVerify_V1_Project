# =====================================================
# iVerify V2 - JSON Parser Engine
# Sosyal Medya Veri Analiz Motoru
# =====================================================

from pathlib import Path
from datetime import datetime
import json



class JSONParser:


    def __init__(self):

        self.parsed_users = []

        self.errors = []



    # -------------------------------------------------
    # JSON dosyası oku
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


        except Exception as error:

            self.errors.append(
                str(error)
            )

            return None



    # -------------------------------------------------
    # Tarih dönüştürme
    # -------------------------------------------------

    def convert_timestamp(self, timestamp):


        if not timestamp:

            return None


        try:

            return datetime.fromtimestamp(
                timestamp
            ).strftime(
                "%d.%m.%Y %H:%M"
            )


        except Exception:

            return None




    # -------------------------------------------------
    # Tek kullanıcı verisi çıkarma
    # -------------------------------------------------

    def extract_user(self, item):


        username = None

        link = None

        timestamp = None



        # Meta yeni format

        if isinstance(item, dict):


            if "string_list_data" in item:


                data = item[
                    "string_list_data"
                ]


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



                link = item.get(
                    "href"
                )



                timestamp = item.get(
                    "timestamp"
                )



        return {


            "username": username,


            "link": link,


            "timestamp": timestamp,


            "date":
            self.convert_timestamp(
                timestamp
            )


        }




    # -------------------------------------------------
    # JSON içinden kullanıcıları çıkar
    # -------------------------------------------------

    def parse_users(self, data):


        users = []



        if isinstance(data, list):


            for item in data:


                user = self.extract_user(
                    item
                )


                if user["username"]:

                    users.append(
                        user
                    )



        elif isinstance(data, dict):


            for key, value in data.items():


                if isinstance(value, list):


                    for item in value:


                        user = self.extract_user(
                            item
                        )


                        if user["username"]:

                            users.append(
                                user
                            )



        self.parsed_users = users


        return users