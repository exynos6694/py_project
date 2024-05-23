from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import requests
from bs4 import BeautifulSoup

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

# 정적 파일을 제공하기 위해 "static" 디렉토리를 "/static" 경로로 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 멜론 차트 데이터를 가져오는 함수
def get_melon_chart():
    # 멜론 차트 페이지 URL
    url = "https://www.melon.com/chart/index.htm"
    
    # HTTP 요청 헤더 설정 (봇 차단 회피를 위해 User-Agent 설정)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # 멜론 차트 페이지로부터 데이터 가져오기
    response = requests.get(url, headers=headers)
    
    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 차트 데이터를 저장할 리스트
    chart = []
    
    # 곡 제목과 아티스트를 선택하는 CSS 선택자
    songs = soup.select('div.ellipsis.rank01 span a')
    artists = soup.select('div.ellipsis.rank02 span')

    # 각 곡에 대해 순위를 매기고 제목과 아티스트를 리스트에 추가
    for rank, (song, artist) in enumerate(zip(songs, artists), start=1):
        chart.append({
            'rank': rank,
            'title': song.text,
            'artist': artist.text
        })

    # 차트 데이터를 반환
    return chart

# 루트 경로("/")에 대한 GET 요청 핸들러
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # 멜론 차트 데이터를 가져옴
    chart = get_melon_chart()
    
    # 템플릿을 사용하여 HTML 응답 생성
    return templates.TemplateResponse("base3.html", {"request": request, "chart": chart})

# 애플리케이션을 직접 실행하는 경우
if __name__ == "__main__":
    import uvicorn
    # uvicorn을 사용하여 애플리케이션 실행
    uvicorn.run(app, host="0.0.0.0", port=8000)
