# =====================================================
# iVerify V2 - Real Instagram ZIP Test
# =====================================================


from pathlib import Path

from backend.services.pipeline.analysis_pipeline import (
    AnalysisPipeline
)



def run_test():


    print(
        "iVerify Gerçek Instagram ZIP Test Başladı..."
    )


    zip_file = Path(
        "instagram-username-2026.zip"
    )



    if not zip_file.exists():

        print(
            "ZIP dosyası bulunamadı!"
        )

        return



    pipeline = AnalysisPipeline()



    result = pipeline.run(
        zip_file
    )



    print(
        "\n===== ANALİZ SONUCU =====\n"
    )


    print(result)



    print(
        "\n===== TEST TAMAMLANDI ====="
    )




if __name__ == "__main__":

    run_test()