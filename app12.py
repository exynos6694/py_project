from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
import requests
from bs4 import BeautifulSoup
import os
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")



posts = []  # 글을 저장할 리스트





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

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    chart = get_melon_chart()
    return templates.TemplateResponse("index.html", {"request": request, "chart": chart})

@app.get("/write", response_class=HTMLResponse)
async def write_form(request: Request):
    return templates.TemplateResponse("write.html", {"request": request})

@app.post("/submit", response_class=RedirectResponse)
async def submit_post(request: Request, title: str = Form(...), content: str = Form(...)):
    post = {"title": title, "content": content}
    posts.append(post)
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
