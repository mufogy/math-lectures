# -*- coding: utf-8 -*-
"""
manim 장면의 공통 테마.

모든 강의 장면 파일이 이 모듈을 불러 씁니다. 색을 여기서 한 번만 바꾸면
모든 영상의 톤이 함께 바뀝니다.

    import sys
    sys.path.insert(0, r"D:\\test1234\\00_공통\\01_템플릿")
    from slide_theme import *

색값은 슬라이드 공통 CSS(00_공통/02_서식_스타일/slide.css)의 :root 와 짝입니다.
한쪽만 바꾸면 영상과 슬라이드의 톤이 어긋납니다.

주의: MathTex 안에는 한글을 넣지 마세요. LaTeX 가 비 ASCII 를 만나면
로그 인코딩이 깨져 렌더가 실패합니다. 한글은 kr() 로 따로 얹으세요.
"""
from manim import *

config.background_color = "#fbf9f5"   # 슬라이드 #stage 와 같은 미색 바탕

KFONT = "Malgun Gothic"   # 한글 폰트 (Windows 기본)
INK = "#2b2621"           # 본문 — 따뜻한 진갈색
MUTED = "#706456"         # 보조 설명 — 토프 브라운
FAINT = "#b0a290"         # 눈금·보조선
ACCENT = "#385499"        # 강조 1 — 소프트 인디고
WARM = "#ad5100"          # 강조 2 — 테라코타
GOOD = "#227255"          # 결론 — 세이지 그린
BAD = "#bd3a3a"           # 불가 / 주의 — 벽돌색

ACCENT_SOFT = "#f0f4fc"
WARM_SOFT = "#fff6e5"
GOOD_SOFT = "#f0f7f4"
BAD_SOFT = "#faf0f0"


def kr(t, size=32, color=INK, weight=NORMAL):
    """한글 텍스트"""
    return Text(t, font=KFONT, font_size=size, color=color, weight=weight)


def head(t):
    """슬라이드 상단 제목 + 밑줄. 화면 맨 위에 붙는다."""
    g = VGroup(
        kr(t, 40, INK, BOLD),
        Line(LEFT * 3.2, RIGHT * 3.2, color=ACCENT, stroke_width=4),
    ).arrange(DOWN, buff=0.18)
    return g.to_edge(UP, buff=0.35)


def box(mobj, color=GOOD, fill=None, buff=0.32):
    """결론을 감싸는 둥근 상자"""
    return SurroundingRectangle(
        mobj, color=color, buff=buff, corner_radius=0.16, stroke_width=3,
        fill_color=fill or "#ffffff", fill_opacity=1 if fill else 0,
    )


def wipe(scene, keep=None, run_time=0.8):
    """
    장면 중간에서 화면을 비운다. `keep` 에 준 것만 남기고 나머지를 전부 걷어낸다.

    FadeOut(VGroup(a, b, c)) 처럼 손으로 나열하면 반복문 안에서 만든 화살표나
    Create(box(...)) 처럼 변수에 담지 않은 것이 화면에 남아 다음 장면을 덮는다.
    이 함수는 남길 것만 지정하므로 그런 잔상이 생기지 않는다.

        hd = head("제목")
        self.add(hd)
        ...
        wipe(self, hd)      # 제목만 남기고 싹 지운다
    """
    keeps = []
    if keep is not None:
        keeps = list(keep) if isinstance(keep, (list, tuple)) else [keep]
    doomed = [m for m in scene.mobjects if m not in keeps]
    if doomed:
        scene.play(FadeOut(Group(*doomed)), run_time=run_time)


def derive(scene, rows, x_left=-2.8, x_desc=3.4, y_top=1.2, dy=1.15, size=38):
    """
    유도 과정을 한 줄씩 쌓아 보여 준다.
    rows: [(latex, 한글설명), ...]
    반환: 화면에 남은 VGroup (나중에 FadeOut 하기 위해)
    """
    shown = VGroup()
    for i, (tex, desc) in enumerate(rows):
        y = y_top - i * dy
        m = MathTex(tex, font_size=size, color=INK).move_to(RIGHT * x_left + UP * y)
        scene.play(Write(m), run_time=1.0)
        shown.add(m)
        if desc:
            d = kr(desc, 22, MUTED).move_to(RIGHT * x_desc + UP * y)
            scene.play(FadeIn(d, shift=LEFT * 0.2), run_time=0.45)
            shown.add(d)
        scene.wait(0.35)
    return shown
