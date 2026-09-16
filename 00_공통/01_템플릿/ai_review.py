# -*- coding: utf-8 -*-
r"""
강의자료를 Antigravity(Gemini Interactions API)에 보내 검수받는다.

    python ai_review.py            # 전체 6강 검수
    python ai_review.py --lesson 03
    python ai_review.py --focus math    # math | code | teaching | all

결과는 00_공통/04_공식_개념요약/검수보고서_<날짜>.md 로 저장된다.

주의: Antigravity 는 generateContent 가 아니라 /v1beta/interactions 를 쓴다.
      요청 본문은 {"model": ..., "input": ...} 이고, 응답은 steps[] 안에 들어 있다.
"""
import argparse
import datetime
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(r"D:\test1234")
MATH1 = ROOT / "02_수학1"
OUTDIR = ROOT / "00_공통" / "04_공식_개념요약"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
MODEL = "models/antigravity-preview-09-2026"

FOCUS = {
    "math": """**수학적 정확성**에만 집중하세요.
- 공식·정의·조건이 틀린 곳
- 조건 누락 (예: a>0, a≠1, 진수>0, r≠1, n≥2)
- 그림/애니메이션이 설명하는 명제와 어긋나는 곳
- 반례가 있는 서술""",
    "teaching": """**교육적 타당성**에 집중하세요. 대상은 고2 학생입니다.
- 개념의 제시 순서가 논리적으로 앞뒤가 맞는지
- 학생이 이 설명만으로 이해할 수 있는지 (비약이 있는지)
- 발표자 노트의 발문·힌트가 실제로 도움이 되는지
- 빠진 필수 개념이 있는지""",
    "code": """**코드 품질**에 집중하세요.
- manim 장면에서 화면 밖으로 나가거나 겹칠 위험이 있는 배치
- 하드코딩된 좌표 중 값이 바뀌면 깨질 것
- HTML/CSS 의 접근성·가독성 문제""",
    "all": """다음 세 가지를 모두 보되, **수학적 오류를 최우선**으로 보고하세요.
1. 수학적 정확성 — 공식·조건 누락, 그림과 명제의 불일치, 반례
2. 교육적 타당성 — 고2 대상 설명의 논리 순서와 비약
3. 코드 품질 — manim 배치 위험, 하드코딩""",
}

PROMPT = """당신은 고등학교 수학 교재를 검수하는 베테랑 수학 교사이자 수학 전공자입니다.

아래는 고2 대상 EBS 수능특강 수학Ⅰ 강의자료입니다.
각 강은 (1) HTML 슬라이드의 텍스트와 (2) 영상을 만드는 manim 파이썬 코드로 이루어져 있습니다.
슬라이드에는 발표자 노트(data-notes)가 들어 있는데, 이것은 교사가 수업 중에 말할 내용입니다.

{focus}

# 보고 형식
발견한 문제만 아래 형식으로 나열하세요. 문제가 없으면 "문제 없음"이라고만 쓰세요.
칭찬이나 요약은 쓰지 마세요. **오직 고쳐야 할 것만** 쓰세요.

각 항목:
```
### [심각도] 강NN · 위치
**무엇이 틀렸나:** (한 문장)
**근거:** (왜 틀렸는지. 수학 오류면 반례나 정확한 서술을 제시)
**고칠 내용:** (구체적으로)
```
심각도는 `치명` (수학적으로 틀림) / `중요` (오해를 부름) / `경미` (다듬으면 좋음) 중 하나.

심각도 `치명` 이 있으면 반드시 맨 위에 두세요.
확신이 없으면 그렇게 밝히세요. 억지로 문제를 만들어 내지 마세요.

---

{payload}
"""


def api_key() -> str:
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit(".env 에서 GEMINI_API_KEY 를 찾지 못했습니다.")


def slide_text(html: str) -> str:
    """슬라이드 HTML 에서 검수에 필요한 내용만 뽑는다 (CSS/JS/보일러플레이트 제외)."""
    out = []
    for s in re.findall(r'<section class="slide[^"]*"[^>]*>.*?</section>', html, re.S):
        sec = re.search(r'data-sec="([^"]*)"', s)
        notes = re.search(r'data-notes="([^"]*)"', s, re.S)
        body = re.sub(r'data-notes="[^"]*"', "", s, flags=re.S)
        body = re.sub(r"<[^>]+>", " ", body)
        body = re.sub(r"[ \t]+", " ", body).strip()
        out.append(f"--- 슬라이드 [{sec.group(1) if sec else ''}] ---\n{body}")
        if notes:
            out.append(f"[발표자 노트] {notes.group(1).strip()}")
    return "\n".join(out)


def build_payload(only: str = "") -> str:
    parts = []
    for d in sorted(MATH1.glob("*/*")):
        if not d.is_dir():
            continue
        num = d.name[:2]
        if only and num != only:
            continue
        html = next((d / "02_강의안").glob("*.html"), None)
        py = next((d / "05_자료" / "manim").glob("*_scenes.py"), None)
        if not html:
            continue
        parts.append(f"\n\n{'='*70}\n# 강 {num} — {d.name}\n{'='*70}\n")
        parts.append("## 슬라이드\n" + slide_text(html.read_text(encoding="utf-8")))
        if py:
            parts.append("\n## manim 장면 코드\n```python\n"
                         + py.read_text(encoding="utf-8") + "\n```")
    return "".join(parts)


def ask(prompt: str) -> tuple:
    body = {"model": MODEL, "input": prompt}
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key()},
    )
    try:
        with urllib.request.urlopen(req, timeout=1800) as r:
            res = json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"API 오류 {e.code}: {e.read().decode('utf-8', 'replace')[:500]}")

    if res.get("status") != "completed":
        print("  경고: status =", res.get("status"))
    text = "\n".join(
        c.get("text", "")
        for step in res.get("steps", [])
        if step.get("type") == "model_output"
        for c in step.get("content", [])
        if c.get("type") == "text"
    )
    return text, res.get("usage", {})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", default="", help="특정 강만 (예: 03)")
    ap.add_argument("--focus", default="all", choices=list(FOCUS))
    args = ap.parse_args()

    payload = build_payload(args.lesson)
    if not payload:
        raise SystemExit("검수할 강의자료를 찾지 못했습니다.")
    prompt = PROMPT.format(focus=FOCUS[args.focus], payload=payload)
    print(f"검수 대상 {len(payload):,}자 · 초점 {args.focus}"
          + (f" · 강{args.lesson}" if args.lesson else " · 전체"))
    print("Antigravity 에 요청 중... (수 분 걸릴 수 있습니다)")

    text, usage = ask(prompt)
    print(f"  입력 {usage.get('total_input_tokens'):,} 토큰 / "
          f"사고 {usage.get('total_thought_tokens', 0):,} / "
          f"출력 {usage.get('total_output_tokens'):,}")

    OUTDIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.date.today().isoformat()
    tag = f"_강{args.lesson}" if args.lesson else ""
    path = OUTDIR / f"검수보고서_{stamp}{tag}_{args.focus}.md"
    path.write_text(
        f"# 강의자료 검수 보고서\n\n"
        f"- 검수: Antigravity (`{MODEL}`)\n"
        f"- 날짜: {stamp}\n"
        f"- 대상: {'강 ' + args.lesson if args.lesson else '수학Ⅰ 전 6강'}\n"
        f"- 초점: {args.focus}\n"
        f"- 토큰: 입력 {usage.get('total_input_tokens'):,} · "
        f"출력 {usage.get('total_output_tokens'):,}\n\n---\n\n{text}\n",
        encoding="utf-8")
    print(f"\n저장: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
