# =====================================================
# iVerify V2 - Analyzer Test
# Sosyal Medya Veri Analiz Motoru
# =====================================================


from backend.modules.analyzer.analyzer import AnalyzerEngine



def run_test():


    print(
        "iVerify V2 Analyzer Test Başladı..."
    )


    analyzer = AnalyzerEngine()



    # ---------------------------------------------
    # Sahte Meta verisi
    # ---------------------------------------------


    fake_followers = [

        {
            "username": "ahmet",
            "timestamp": 1750000000
        },

        {
            "username": "mehmet",
            "timestamp": 1750000000
        },

        {
            "username": "veli",
            "timestamp": 1750000000
        }

    ]



    fake_following = [

        {
            "username": "ahmet",
            "timestamp": 1750000000
        },

        {
            "username": "mehmet",
            "timestamp": 1750000000
        },

        {
            "username": "ali",
            "timestamp": 1750000000
        }

    ]



    # ---------------------------------------------
    # İlişki analizi
    # ---------------------------------------------


    result = analyzer.analyze_relationships(

        fake_followers,

        fake_following

    )



    print("\n===== ANALİZ SONUCU =====\n")


    print(result)



    print("\n===== TEST TAMAMLANDI =====")




if __name__ == "__main__":

    run_test()