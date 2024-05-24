import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

# 환경 변수 로드
load_dotenv()

app = FastAPI()

# 정적 파일 경로 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# MongoDB 클라이언트 설정
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["mydatabase"]
posts_collection = db["posts"]

# 멜론 차트 데이터 가져오기
def get_melon_chart():
    url = "https://www.melon.com/chart/index.htm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    chart = []
    songs = soup.select('div.ellipsis.rank01 span a')
    artists = soup.select('div.ellipsis.rank02 span')

    for rank, (song, artist) in enumerate(zip(songs, artists), start=1):
        chart.append({
            'rank': rank,
            'title': song.text,
            'artist': artist.text
        })
    return chart

# 루트 경로 처리
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    chart = get_melon_chart()
    posts = await posts_collection.find().to_list(length=100)
    return templates.TemplateResponse("index.html", {"request": request, "chart": chart, "posts": posts})

# 로그인 폼 페이지
@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# 글쓰기 폼 페이지
@app.get("/write", response_class=HTMLResponse)
async def write_form(request: Request):
    return templates.TemplateResponse("write.html", {"request": request})

# 글쓰기 제출 처리
@app.post("/submit", response_class=RedirectResponse)
async def submit_post(request: Request, title: str = Form(...), content: str = Form(...), author: str = Form(...) ) :
    post = {"title": title,"author":author, "content": content}
    await posts_collection.insert_one(post)
    return RedirectResponse(url="/", status_code=303)

@app.get("/posts", response_class=HTMLResponse)
async def read_posts(request: Request):
    posts = await posts_collection.find().to_list(length=100)
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
