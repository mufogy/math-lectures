# -*- coding: utf-8 -*-
"""
AI Studio(Gemini)로 강의 슬라이드 HTML 의 CSS 를 다시 디자인한다.

사용 예)
  python ai_redesign.py "..\\01_지수와_로그\\02_강의안\\01_지수와로그_강의슬라이드.html"
  python ai_redesign.py <html> --brief "더 차분하고 절제된 느낌으로"
  python ai_redesign.py <html> --dry-run      # 적용하지 않고 결과만 저장

동작
  1. HTML 의 <style> 블록을 통째로 뽑아 Gemini 에 보낸다
  2. 레이아웃을 건드리지 말라는 제약을 걸어 CSS 만 다시 받는다
  3. 선택자가 하나라도 사라졌으면 적용을 거부한다
  4. 통과하면 원본을 .bak 으로 백업하고 교체한다

주의
  - API 키는 D:\\test1234\\.env 의 GEMINI_API_KEY 에서 읽는다
  - 슬라이드 팔레트를 바꾸면 manim 장면 파일(k01_scenes.py 등)의
    INK/ACCENT/... 상수도 같이 바꿔야 영상과 톤이 맞는다
"""
import argparse
import json
import pathlib
import re
import shutil
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(r"D:\test1234")
MODEL = "gemini-3.5-flash"     # 무료 티어에서 쓸 수 있는 모델
ENDPOINT = ("https://generativelanguage.googleapis.com/v1beta/models/"
            f"{MODEL}:generateContent")

DEFAULT_BRIEF = """현재 디자인이 "딱딱하다"는 평을 받았습니다.
각진 모서리, 뚜렷한 1px 회색 테두리, 차가운 청회색(slate) 계열,
높은 대비의 원색 강조가 원인입니다. 부드러운(soft) 디자인으로 다시 써 주세요.

- 차가운 slate 대신 따뜻한 중성색(warm gray / 미색 기운)으로
- 채도 높은 원색 대신 한 단계 가라앉은 톤으로
- 테두리선 대신 아주 옅은 배경색 + 부드러운 그림자로 면을 구분
- 모서리 반경을 넉넉하게(18~28px), 여백도 조금 더 후하게
- 그림자는 검정 대신 바탕색 계열의 저채도 그림자로
- 애니메이션 이징을 조금 더 부드럽게"""

CONSTRAINTS = """# 반드시 지킬 것 (어기면 슬라이드가 깨집니다)
1. 모든 선택자(selector)와 클래스명을 그대로 유지하세요. 추가는 되지만 삭제·개명은 금지.
2. 레이아웃 역학을 건드리지 마세요:
   - #stage 의 width/height 는 var(--stage-w)/var(--stage-h) 유지
   - .slide{position:absolute; inset:0}, .slide.on{display:flex} 유지
   - .body, .cols, .roadmap 의 flex/grid 구조와 flex:1, min-height:0 유지
   - .video-wrap{flex:1} 와 video{object-fit:contain} 유지
   - #overview, #notes, #help 의 display:none / .on 토글 구조 유지
   - @media print 블록의 규칙 유지
3. 교실 프로젝터에서 읽혀야 합니다. 본문과 배경 대비는 WCAG AA(4.5:1) 이상 유지.
   부드럽게 만든다고 본문 글자를 연회색으로 만들지 마세요.
4. 폰트 패밀리는 그대로 두세요(한글 폰트 문제). 크기도 크게 바꾸지 마세요.

# 출력 형식
설명이나 마크다운 없이, 완성된 CSS 전문만 출력하세요.
<style> 태그는 포함하지 마세요. 주석은 한국어로 달아도 좋습니다."""


def api_key() -> str:
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit(".env 에서 GEMINI_API_KEY 를 찾지 못했습니다.")


def selectors(css: str) -> set:
    """CSS 에서 선택자만 뽑아낸다 (@규칙 제외)."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = set()
    for m in re.finditer(r"([^{}]+)\{", css):
        head = m.group(1).strip()
        if head.startswith("@") or not head:
            continue
        for part in head.split(","):
            part = part.strip()
            if part:
                out.add(part)
    return out


def ask_gemini(css: str, brief: str) -> str:
    prompt = (
        "당신은 교육용 프레젠테이션을 디자인하는 시니어 UI 디자이너입니다.\n\n"
        "아래는 고등학교 수학 수업용 HTML 슬라이드(1600×900, 밝은 테마)의 CSS 전문입니다.\n\n"
        + brief + "\n\n" + CONSTRAINTS + "\n\n--- 현재 CSS ---\n" + css
    )
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 32768},
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key()},
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            res = json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"API 오류 {e.code}: {e.read().decode('utf-8', 'replace')[:400]}")

    cand = res["candidates"][0]
    if cand.get("finishReason") not in (None, "STOP"):
        print("  경고: finishReason =", cand.get("finishReason"))
    text = "".join(p.get("text", "") for p in cand["content"]["parts"])
    usage = res.get("usageMetadata", {})
    print(f"  토큰 입력 {usage.get('promptTokenCount')} / 출력 {usage.get('candidatesTokenCount')}")
    return re.sub(r"^```(?:css)?\n|\n```$", "", text.strip())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html", help="강의 슬라이드 HTML 경로")
    ap.add_argument("--brief", default=DEFAULT_BRIEF, help="원하는 디자인 방향")
    ap.add_argument("--dry-run", action="store_true", help="적용하지 않고 .new.css 로만 저장")
    args = ap.parse_args()

    p = pathlib.Path(args.html)
    html = p.read_text(encoding="utf-8")
    m = re.search(r"<style>(.*?)</style>", html, re.S)
    if not m:
        raise SystemExit("<style> 블록을 찾지 못했습니다.")
    old = m.group(1)

    print(f"{p.name} · 기존 CSS {len(old)}자")
    print("Gemini 에 재디자인 요청 중...")
    new = ask_gemini(old, args.brief)
    print(f"  받은 CSS {len(new)}자 / {new.count(chr(10)) + 1}줄")

    missing = sorted(selectors(old) - selectors(new))
    if missing:
        side = p.with_suffix(".rejected.css")
        side.write_text(new, encoding="utf-8")
        print(f"\n적용 거부: 선택자 {len(missing)}개가 사라졌습니다.")
        for s in missing[:20]:
            print("   ", s)
        print(f"받은 CSS 는 {side.name} 에 남겨 두었습니다.")
        return 1
    print("  선택자 검증 통과")

    if args.dry_run:
        side = p.with_suffix(".new.css")
        side.write_text(new, encoding="utf-8")
        print(f"dry-run · {side.name} 에 저장했습니다.")
        return 0

    shutil.copy(p, str(p) + ".bak")
    out = re.sub(r"(<style>).*?(</style>)",
                 lambda mm: mm.group(1) + "\n" + new + "\n" + mm.group(2),
                 html, count=1, flags=re.S)
    p.write_text(out, encoding="utf-8")
    print(f"적용 완료 · 백업: {p.name}.bak")
    print("잊지 말 것: manim 장면 파일의 색 상수도 새 팔레트로 맞추세요.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
