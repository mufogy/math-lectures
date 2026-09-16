# -*- coding: utf-8 -*-
r"""
각 강의 `02_강의안/README.md` 를 슬라이드 HTML 과 manim 장면 파일에서 자동 생성한다.

    python make_readme.py

슬라이드를 고친 뒤 다시 돌리면 목차가 갱신된다. 손으로 고치지 말 것.
"""
import html as html_mod
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(r"D:\test1234\02_수학1")
BUILD = r"D:\test1234\00_공통\01_템플릿\build_manim.ps1"

TITLES = {
    "01_지수와_로그": ("01", "지수와 로그", "p.4 ~ 19"),
    "02_지수함수와_로그함수": ("02", "지수함수와 로그함수", "p.20 ~ 35"),
    "03_삼각함수": ("03", "삼각함수", "p.36 ~ 51"),
    "04_사인법칙과_코사인법칙": ("04", "사인법칙과 코사인법칙", "p.52 ~ 67"),
    "05_등차수열과_등비수열": ("05", "등차수열과 등비수열", "p.68 ~ 83"),
    "06_수열의_합과_수학적_귀납법": ("06", "수열의 합과 수학적 귀납법", "p.84 ~ 101"),
}

# 경로에 백슬래시가 많으므로 raw 문자열로 둔다.
TMPL = r"""# 강 {num} 「{title}」 강의 슬라이드

교재 {pages} · 슬라이드 {nslide}장 · manim 영상 {nvid}편

> 이 파일은 `00_공통/01_템플릿/make_readme.py` 가 자동 생성합니다. 손으로 고치지 마세요.

## 파일

| 파일 | 내용 |
|---|---|
| `{htmlname}` | 수업용 슬라이드 (PPT 형식) |
| `media/*.mp4` | 슬라이드에 삽입되는 manim 시각화 |
| `../05_자료/manim/{pyname}` | 그 영상의 원본 소스 |

디자인과 동작은 `00_공통/02_서식_스타일/slide.css`, `slide.js` 를 **모든 강이 공유**합니다.
한 곳을 고치면 6개 강에 모두 반영됩니다.

## 여는 법

HTML 파일을 더블클릭하면 브라우저에서 바로 열립니다. 설치할 것은 없습니다.
수업 전 <kbd>F</kbd> 로 전체 화면으로 두고 시작하세요.

| 키 | 동작 |
|---|---|
| <kbd>→</kbd> <kbd>Space</kbd> / <kbd>←</kbd> | 다음 / 이전 슬라이드 |
| <kbd>N</kbd> | **발표자 노트** — 판서 순서·발문·영상 멈춤 지점 |
| <kbd>O</kbd> | 전체 슬라이드 한눈에 보기 |
| <kbd>F</kbd> / <kbd>B</kbd> | 전체 화면 / 화면 끄기(판서용) |
| <kbd>Ctrl</kbd>+<kbd>P</kbd> | PDF 유인물로 저장 |

## 슬라이드 구성

{outline}

## 영상

{videos}

## 영상을 다시 뽑을 때

```powershell
& "{build}" -SceneFile "{scenefile}"

# 한 장면만 빠르게 확인
& "{build}" -SceneFile "{scenefile}" -Scenes {first} -Quality preview
```

렌더된 mp4 는 이 폴더의 `media\` 로 자동 복사되므로 HTML 은 손댈 필요가 없습니다.
색은 `00_공통/01_템플릿/slide_theme.py` 한 곳에서 관리되며, 슬라이드 CSS 의 `:root` 와 짝입니다.
"""


def slide_title(section: str) -> str:
    """<h1>/<h2> 에서 제목만 뽑는다. 쪽수 배지와 수식 구분자는 걷어낸다."""
    m = re.search(r"<h[12][^>]*>(.*?)</h[12]>", section, re.S)
    if not m:
        return ""
    inner = m.group(1)
    inner = re.sub(r'<span class="pg">.*?</span>', "", inner, flags=re.S)  # 쪽수 배지
    text = re.sub(r"<[^>]+>", "", inner)
    text = html_mod.unescape(text)                     # &amp; → &
    text = re.sub(r"\$([^$]*)\$", r"\1", text)         # KaTeX 구분자
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    made = 0
    for folder, (num, title, pages) in TITLES.items():
        d = next(ROOT.glob(f"*/{folder}"), None)
        if d is None:
            print("폴더 없음:", folder)
            continue
        gu = d / "02_강의안"
        html_path = next(gu.glob("*.html"), None)
        py_path = next((d / "05_자료" / "manim").glob("*_scenes.py"), None)
        if not html_path or not py_path:
            print("파일 없음:", folder)
            continue

        src = html_path.read_text(encoding="utf-8")
        secs = re.findall(r'<section class="slide[^"]*"[^>]*>.*?</section>', src, re.S)

        rows = []
        for i, s in enumerate(secs, 1):
            sec = re.search(r'data-sec="([^"]*)"', s)
            vid = re.search(r'data-src="media/(\w+)\.mp4"', s)
            rows.append((i, sec.group(1) if sec else "", slide_title(s),
                         vid.group(1) if vid else ""))

        outline = ("| # | 구분 | 제목 | 영상 |\n|---|---|---|---|\n"
                   + "\n".join(f"| {i} | {sc} | {t} | {('`' + v + '`') if v else ''} |"
                               for i, sc, t, v in rows))

        py_src = py_path.read_text(encoding="utf-8")
        scenes = re.findall(r"^class (\w+)\(Scene\):", py_src, re.M)
        docs = dict(re.findall(r"^  (\w+)\s+(\S*차시 · .+)$", py_src, re.M))
        videos = ("| 파일 | 내용 |\n|---|---|\n"
                  + "\n".join(f"| `{s}.mp4` | {docs.get(s, '')} |" for s in scenes))

        (gu / "README.md").write_text(TMPL.format(
            num=num, title=title, pages=pages,
            nslide=len(secs), nvid=len(scenes),
            htmlname=html_path.name, pyname=py_path.name,
            outline=outline, videos=videos,
            build=BUILD, scenefile=str(py_path),
            first=scenes[0] if scenes else "",
        ), encoding="utf-8")
        print(f"강{num}: 슬라이드 {len(secs)}장 · 영상 {len(scenes)}편")
        made += 1
    print(f"\nREADME {made}개 작성")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
