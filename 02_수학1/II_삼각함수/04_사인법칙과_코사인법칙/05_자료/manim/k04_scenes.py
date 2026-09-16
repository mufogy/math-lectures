# -*- coding: utf-8 -*-
"""
2027 EBS 수능특강 수학Ⅰ — 강04 「사인법칙과 코사인법칙」 시각화

  S1SineLaw       1차시 · 사인법칙과 외접원
  S2CosineLaw     2차시 · 코사인법칙 — 피타고라스의 확장
  S3TriangleShape 3차시 · 삼각형의 모양 판정
  S4TriangleArea  4차시 · 삼각형의 넓이

렌더: 00_공통/01_템플릿/build_manim.ps1
"""
import sys

import numpy as np

sys.path.insert(0, r"D:\test1234\00_공통\01_템플릿")
from slide_theme import *   # noqa: F403,F401


def triangle(A, B, C, color=ACCENT, w=4):
    return VGroup(
        Line(A, B, color=color, stroke_width=w),
        Line(B, C, color=color, stroke_width=w),
        Line(C, A, color=color, stroke_width=w),
    )


# ──────────────────────────────────────────────────────────────
# 1차시 · 사인법칙 — 세 비가 모두 외접원 지름과 같다
# ──────────────────────────────────────────────────────────────
class S1SineLaw(Scene):
    def construct(self):
        self.add(head("사인법칙 — 세 비가 모두 외접원의 지름"))

        R = 2.2
        O = LEFT * 3.4 + DOWN * 0.7
        circ = Circle(radius=R, color=FAINT, stroke_width=3).move_to(O)
        self.play(Create(circ), run_time=0.9)

        ang = [2.3, 3.9, 5.6]      # 원 위의 세 점
        P = [O + R * np.array([np.cos(t), np.sin(t), 0]) for t in ang]
        tri = triangle(*P, color=ACCENT)
        dots = VGroup(*[Dot(p, color=ACCENT, radius=0.08) for p in P])
        names = VGroup(
            MathTex("A", font_size=32, color=INK).next_to(P[0], UL, buff=0.12),
            MathTex("B", font_size=32, color=INK).next_to(P[1], DL, buff=0.12),
            MathTex("C", font_size=32, color=INK).next_to(P[2], DR, buff=0.12),
        )
        self.play(Create(tri), FadeIn(dots), FadeIn(names), run_time=1.4)

        Od = Dot(O, color=WARM, radius=0.08)
        Rl = Line(O, P[0], color=WARM, stroke_width=3)
        Rt = MathTex("R", font_size=30, color=WARM).next_to(
            (O + P[0]) / 2, LEFT, buff=0.15)
        self.play(FadeIn(Od), Create(Rl), FadeIn(Rt))
        self.play(FadeIn(kr("외접원의 반지름", 24, WARM).next_to(circ, DOWN, buff=0.25)))
        self.wait(0.6)

        law = MathTex(r"\frac{a}{\sin A}=\frac{b}{\sin B}"
                      r"=\frac{c}{\sin C}=2R",
                      font_size=50, color=ACCENT).move_to(RIGHT * 3.3 + UP * 1.4)
        self.play(Write(law), run_time=1.6)
        self.wait(0.8)

        use = VGroup(
            kr("두 각 + 한 변  →  나머지 변", 27, INK),
            kr("두 변 + 한 대각  →  나머지 각", 27, INK),
            kr("변의 비 = sin 의 비", 27, GOOD, BOLD),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 3.3 + DOWN * 1.2)
        self.play(LaggedStartMap(FadeIn, use, shift=UP * 0.2, lag_ratio=0.3),
                  run_time=1.6)

        ratio = MathTex(r"\sin A:\sin B:\sin C=a:b:c",
                        font_size=36, color=GOOD)
        ratio.move_to(RIGHT * 3.3 + DOWN * 2.6)
        self.play(Write(ratio), run_time=1.2)
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 2차시 · 코사인법칙 — 피타고라스에 보정항이 붙은 것
# ──────────────────────────────────────────────────────────────
class S2CosineLaw(Scene):
    def construct(self):
        self.add(head("코사인법칙 — 피타고라스에 보정항이 붙은 것"))

        law = MathTex(r"a^{2}=b^{2}+c^{2}", r"-2bc\cos A",
                      font_size=56, color=INK).move_to(UP * 1.9)
        law[1].set_color(BAD)
        self.play(Write(law[0]), run_time=1.0)
        self.play(FadeIn(law[1], shift=LEFT * 0.3), run_time=0.8)
        tag = kr("이 항이 직각에서 벗어난 만큼을 보정한다", 26, MUTED)
        tag.next_to(law, DOWN, buff=0.3)
        self.play(FadeIn(tag))
        self.wait(1.0)
        self.play(FadeOut(tag))

        # A 를 움직이며 보정항을 관찰
        Ang = ValueTracker(np.pi / 3)
        Ov = LEFT * 3.2 + DOWN * 1.5
        b_len, c_len = 2.0, 2.6

        def pts():
            A = Ov
            B = Ov + RIGHT * c_len
            t = Ang.get_value()
            C = Ov + b_len * np.array([np.cos(t), np.sin(t), 0])
            return A, B, C

        tri = always_redraw(lambda: triangle(*pts(), color=ACCENT))
        marks = always_redraw(lambda: VGroup(
            MathTex("A", font_size=30, color=INK).next_to(pts()[0], DL, buff=0.12),
            MathTex("B", font_size=30, color=INK).next_to(pts()[1], DR, buff=0.12),
            MathTex("C", font_size=30, color=INK).next_to(pts()[2], UP, buff=0.12),
        ))
        arc = always_redraw(lambda: Arc(
            radius=0.55, start_angle=0, angle=Ang.get_value(),
            color=BAD, stroke_width=3).move_arc_center_to(Ov))

        self.play(Create(tri), FadeIn(marks), Create(arc), run_time=1.2)

        panel = always_redraw(lambda: VGroup(
            VGroup(MathTex(r"A=", font_size=34, color=BAD),
                   DecimalNumber(np.degrees(Ang.get_value()),
                                 num_decimal_places=0, font_size=34, color=BAD),
                   MathTex(r"^{\circ}", font_size=34, color=BAD),
                   ).arrange(RIGHT, buff=0.08),
            VGroup(MathTex(r"-2bc\cos A=", font_size=32, color=WARM),
                   DecimalNumber(-2 * b_len * c_len * np.cos(Ang.get_value()),
                                 num_decimal_places=2, font_size=32, color=WARM),
                   ).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, buff=0.4).move_to(RIGHT * 3.6 + DOWN * 0.6))
        self.play(FadeIn(panel))
        self.wait(0.5)

        note = kr("A = 90° 이면 보정항이 0 → 피타고라스 정리", 27, GOOD, BOLD)
        note.move_to(RIGHT * 3.6 + DOWN * 2.3)

        self.play(Ang.animate.set_value(np.pi / 2), run_time=2.0)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.play(Flash(Ov, color=GOOD, line_length=0.3))
        self.wait(1.2)
        self.play(FadeOut(note))
        self.play(Ang.animate.set_value(2.3), run_time=1.8)
        self.wait(1.0)

        self.play(FadeOut(VGroup(tri, marks, arc, panel, law)), run_time=0.8)

        var = VGroup(
            kr("각을 구할 때는 뒤집어 쓴다", 30, INK, BOLD),
            MathTex(r"\cos A=\frac{b^{2}+c^{2}-a^{2}}{2bc}",
                    font_size=50, color=GOOD),
            kr("세 변을 알면 세 각이 전부 나온다", 27, MUTED),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.3)
        self.play(FadeIn(var[0], shift=UP * 0.2), run_time=0.7)
        self.play(Write(var[1]), run_time=1.4)
        self.play(Create(box(var[1], GOOD)))
        self.play(FadeIn(var[2], shift=UP * 0.2))
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 3차시 · 삼각형의 모양 — 각 조건을 변 조건으로 갈아끼운다
# ──────────────────────────────────────────────────────────────
class S3TriangleShape(Scene):
    def construct(self):
        self.add(head("삼각형의 모양 — 각 조건을 변 조건으로 바꾼다"))

        idea = VGroup(
            kr("각에 대한 식은 그대로는 판정할 수 없다", 28, MUTED),
            kr("사인법칙·코사인법칙으로 변만 남기면 인수분해가 된다", 30, INK, BOLD),
        ).arrange(DOWN, buff=0.3).move_to(UP * 2.2)
        self.play(FadeIn(idea[0]), run_time=0.7)
        self.play(FadeIn(idea[1], shift=UP * 0.2), run_time=0.8)
        self.wait(0.8)

        tools = VGroup(
            MathTex(r"\sin A=\frac{a}{2R}", font_size=36, color=ACCENT),
            MathTex(r"\cos A=\frac{b^{2}+c^{2}-a^{2}}{2bc}",
                    font_size=36, color=ACCENT),
        ).arrange(RIGHT, buff=1.6).move_to(UP * 0.9)
        self.play(LaggedStartMap(FadeIn, tools, shift=UP * 0.2, lag_ratio=0.3),
                  run_time=1.2)
        self.wait(0.8)

        rows = [
            (r"a\cos A=b\cos B", "주어진 조건"),
            (r"a\cdot\frac{b^{2}+c^{2}-a^{2}}{2bc}"
             r"=b\cdot\frac{c^{2}+a^{2}-b^{2}}{2ca}", "코사인법칙 대입"),
            (r"a^{2}(b^{2}+c^{2}-a^{2})=b^{2}(c^{2}+a^{2}-b^{2})", "정리"),
            (r"(a+b)(a-b)(a^{2}+b^{2}-c^{2})=0", "인수분해"),
        ]
        shown = VGroup()
        for i, (tex, desc) in enumerate(rows):
            y = -0.35 - i * 0.92
            m = MathTex(tex, font_size=32, color=INK).move_to(LEFT * 2.1 + UP * y)
            d = kr(desc, 21, MUTED).move_to(RIGHT * 4.4 + UP * y)
            self.play(Write(m), run_time=0.9)
            self.play(FadeIn(d, shift=LEFT * 0.15), run_time=0.4)
            shown.add(m, d)

        self.wait(0.6)
        concl = kr("a = b 인 이등변삼각형  또는  C = 90° 인 직각삼각형",
                   29, GOOD, BOLD).move_to(DOWN * 3.15)
        self.play(FadeIn(concl, shift=UP * 0.2), run_time=0.9)
        self.play(Create(box(concl, GOOD, buff=0.25)))
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 4차시 · 삼각형의 넓이 — 높이를 sin 으로 바꾼다
# ──────────────────────────────────────────────────────────────
class S4TriangleArea(Scene):
    def construct(self):
        self.add(head("삼각형의 넓이 — 높이를 sin 으로 갈아끼운다"))

        # 오른쪽 수식 열과 겹치지 않도록 삼각형을 왼쪽으로 몰아 둔다
        A = LEFT * 5.0 + DOWN * 1.9
        B = A + RIGHT * 4.4
        t = 1.02
        b_len = 3.0
        C = A + b_len * np.array([np.cos(t), np.sin(t), 0])
        H = np.array([C[0], A[1], 0])

        tri = triangle(A, B, C, color=ACCENT)
        names = VGroup(
            MathTex("A", font_size=32, color=INK).next_to(A, DL, buff=0.12),
            MathTex("B", font_size=32, color=INK).next_to(B, DR, buff=0.12),
            MathTex("C", font_size=32, color=INK).next_to(C, UP, buff=0.12),
        )
        self.play(Create(tri), FadeIn(names), run_time=1.3)

        sc = MathTex("c", font_size=30, color=MUTED).next_to((A + B) / 2, DOWN, buff=0.18)
        sb = MathTex("b", font_size=30, color=MUTED).next_to((A + C) / 2, UL, buff=0.1)
        self.play(FadeIn(sc), FadeIn(sb))

        h = DashedLine(C, H, color=WARM, stroke_width=3, dash_length=0.1)
        h_lbl = MathTex("h", font_size=30, color=WARM).next_to((C + H) / 2, RIGHT, buff=0.15)
        arc = Arc(radius=0.5, start_angle=0, angle=t, color=BAD,
                  stroke_width=3).move_arc_center_to(A)
        a_lbl = MathTex("A", font_size=26, color=BAD).move_to(
            A + 0.8 * np.array([np.cos(t / 2), np.sin(t / 2), 0]))
        self.play(Create(h), FadeIn(h_lbl), Create(arc), FadeIn(a_lbl), run_time=1.0)
        self.wait(0.5)

        steps = VGroup(
            MathTex(r"S=\tfrac{1}{2}\times c\times h", font_size=38, color=INK),
            MathTex(r"h=b\sin A", font_size=38, color=WARM),
            MathTex(r"S=\tfrac{1}{2}bc\sin A", font_size=46, color=GOOD),
        ).arrange(DOWN, buff=0.55).move_to(RIGHT * 3.6 + UP * 0.9)

        self.play(Write(steps[0]), run_time=1.0)
        self.play(Write(steps[1]), run_time=0.9)
        self.play(Indicate(h_lbl, color=WARM, scale_factor=1.4))
        self.play(Write(steps[2]), run_time=1.2)
        self.play(Create(box(steps[2], GOOD)))
        self.wait(1.4)

        sym = MathTex(r"S=\tfrac{1}{2}bc\sin A=\tfrac{1}{2}ca\sin B"
                      r"=\tfrac{1}{2}ab\sin C",
                      font_size=36, color=INK).move_to(DOWN * 3.15)
        cap = kr("두 변과 끼인각이면 넓이가 나온다", 24, MUTED)
        cap.move_to(RIGHT * 4.0 + DOWN * 1.5)
        self.play(FadeIn(cap, shift=UP * 0.2))
        self.play(Write(sym), run_time=1.5)
        self.wait(2.2)
