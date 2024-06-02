import requests
from bs4 import BeautifulSoup

def get_gga():
    url = "http://www.di.hs.kr/?act=lunch.main2&month=2024.05.3&code=121610"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        print("HTTP 요청 성공")  # 디버깅 출력
    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 중 오류 발생: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    gga = []
    ggaadd = soup.select('div.menuName span')
    print(f"파싱된 요소 개수: {len(ggaadd)}")  # 디버깅 출력

    for rank, gga_item in enumerate(ggaadd, start=1):
        gga.append({
            'rank': rank,
            'nani': gga_item.text
        })
        print(gga_item.text, "나니")
    
    return gga

if __name__ == "__main__":
    lunch_menu = get_gga()
    
    
