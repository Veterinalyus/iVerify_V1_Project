# =====================================================
# iVerify V2 - Main Application
# =====================================================


from flask import (
    Flask,
    render_template,
    request
)

from pathlib import Path


from config import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    UPLOAD_DIR
)


from backend.services.database.database import (
    initialize_database
)


from backend.services.pipeline.analysis_pipeline import (
    AnalysisPipeline
)



# -----------------------------------------------------
# Database başlat
# -----------------------------------------------------

initialize_database()



# -----------------------------------------------------
# Flask
# -----------------------------------------------------

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)



# -----------------------------------------------------
# Ana sayfa
# -----------------------------------------------------

@app.route("/")
def home():

    return render_template(
        "upload.html"
    )



# -----------------------------------------------------
# Analiz
# -----------------------------------------------------

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():


    file = request.files.get(
        "zip_file"
    )


    if not file:

        return "ZIP dosyası bulunamadı."



    zip_path = (
        UPLOAD_DIR /
        file.filename
    )


    file.save(
        zip_path
    )



    pipeline = AnalysisPipeline()



    result = pipeline.run(
        zip_path
    )



    return render_template(
        "result.html",
        result=result
    )



# -----------------------------------------------------
# Çalıştır
# -----------------------------------------------------

if __name__ == "__main__":


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )