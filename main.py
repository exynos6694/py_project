from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient

app = FastAPI()

# Jinja2 템플릿 디렉토리를 설정합니다.
templates = Jinja2Templates(directory="templates")

# 정적 파일을 제공하기 위한 디렉토리를 설정합니다.
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # HTML 템플릿에 데이터를 전달하여 렌더링합니다.
    return templates.TemplateResponse("base.html", {"request": request, "name": "World"})


# uvicorn main:app --reload 명령어로 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
