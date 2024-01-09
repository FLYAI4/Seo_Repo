from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
from dotenv import load_dotenv
import os
import serpapi

# .env 파일 로드 및 환경 변수 사용
load_dotenv()
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload_image/")
async def upload_image(file: UploadFile = File(...)):
    """
    사용자가 이미지를 업로드할 수 있는 API 엔드포인트.
    :param file: 업로드할 이미지 파일.
    :return: 파일 저장 성공 메시지 및 파일 정보.
    """
    file_extension = Path(file.filename).suffix
    allowed_extensions = [".jpg", ".jpeg", ".png"]

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")

    file_location = f"uploads/{file.filename}"

    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())
        return {"message": "파일이 성공적으로 업로드되었습니다.", "filename": file.filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/google_lens_search/")
async def google_lens_search(image_url: str):
    """
    Google Lens를 사용하여 이미지 검색을 수행하는 API 엔드포인트.
    :param image_url: 검색할 이미지의 URL.
    :param api_key: SerpApi를 사용하기 위한 API 키.
    :return: 검색 결과의 지식 그래프.
    """
    params = {
        "engine": "google_lens",
        "url": image_url,   #https://cdn.veritas-a.com/news/photo/old/4/3_1165480082.jpg
        "api_key": serpapi_api_key
    }

    search = serpapi.search(params)
    results = search.as_dict()
    visual_matches = results["video_results"]

    sentence = ''
    count = 0

    for i in visual_matches:
        count += 1
        sentence += f"{str(count)}: + {i['title']}\n"

    return {"text": sentence}