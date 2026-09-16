# -*- coding: utf-8 -*-
"""
2027 EBS 수능특강 수학Ⅰ — 강03 「삼각함수」 시각화

  S1Radian        1차시 · 일반각과 호도법
  S2UnitCircle    2차시 · 단위원으로 정의하는 삼각함수
  S3TrigGraph     3차시 · 삼각함수의 그래프와 주기
  S4TrigIdentity  4차시 · 삼각함수의 성질
  S5TrigSolve     5차시 · 삼각방정식과 삼각부등식

렌더: 00_공통/01_템플릿/build_manim.ps1
"""
import sys

import numpy as np

sys.path.insert(0, r"D:\test1234\00_공통\01_템플릿")
from slide_theme import *   # noqa: F403,F401


# ──────────────────────────────────────────────────────────────
# 1차시 · 호도법 — 반지름을 자로 삼아 각을 잰다
# ──────────────────────────────────────────────────────────────
class S1Radian(Scene):
    def construct(self):
        self.add(head("호도법 — 반지름을 자로 삼아 각을 잰다"))

        R = 2.0
        O = LEFT * 3.4 + DOWN * 0.6
        circ = Circle(radius=R, color=FAINT, stroke_width=3).move_to(O)
        self.play(Create(circ), run_time=1.0)

        th = ValueTracker(0.001)

        def radius_line(angle, color=MUTED, w=3):
            return Line(O, O + R * np.array([np.cos(angle), np.sin(angle), 0]),
                        color=color, stroke_width=w)

        r0 = radius_line(0, INK, 4)
        r0_lbl = MathTex("r", font_size=32, color=INK).next_to(
            O + RIGHT * R / 2, DOWN, buff=0.2)
        self.play(Create(r0), FadeIn(r0_lbl))

        arm = always_redraw(lambda: radius_line(th.get_value(), ACCENT, 4))
        arc = always_redraw(lambda: Arc(
            radius=R, start_angle=0, angle=th.get_value(),
            color=WARM, stroke_width=7).move_arc_center_to(O))
        self.play(Create(arm), Create(arc))

        # 호의 길이가 반지름과 같아지는 순간이 1라디안
        one = kr("호의 길이가 반지름과 같아지는 각  =  1 라디안", 27, WARM, BOLD)
        one.move_to(RIGHT * 2.6 + UP * 1.5)
        val = always_redraw(lambda: VGroup(
            MathTex(r"\theta=", font_size=36, color=ACCENT),
            DecimalNumber(th.get_value(), num_decimal_places=2,
                          font_size=36, color=ACCENT),
            kr("라디안", 26, ACCENT),
        ).arrange(RIGHT, buff=0.14).move_to(RIGHT * 2.6 + UP * 0.45))
        self.play(FadeIn(val))
        self.play(th.animate.set_value(1.0), run_time=2.4)
        self.play(FadeIn(one, shift=UP * 0.2))
        self.play(Flash(O + R * np.array([np.cos(1.0), np.sin(1.0), 0]),
                        color=WARM, line_length=0.3))
        self.wait(1.2)

        conv = MathTex(r"\pi\ \text{rad}=180^{\circ}", font_size=44, color=GOOD)
        conv.move_to(RIGHT * 2.6 + DOWN * 0.9)
        self.play(Write(conv))
        self.play(th.animate.set_value(np.pi), run_time=2.0)
        self.wait(1.0)

        self.play(FadeOut(VGroup(circ, r0, r0_lbl, arm, arc, one, val, conv)),
                  run_time=0.8)

        # 부채꼴 공식
        f = VGroup(
            MathTex(r"l=r\theta", font_size=52, color=ACCENT),
            MathTex(r"S=\tfrac{1}{2}r^{2}\theta=\tfrac{1}{2}rl",
                    font_size=52, color=GOOD),
        ).arrange(RIGHT, buff=2.0).move_to(UP * 0.7)
        cap = kr("호도법을 쓰면 부채꼴 공식에서 π 가 사라진다", 28, MUTED)
        cap.next_to(f, DOWN, buff=0.7)
        self.play(Write(f[0]), run_time=1.0)
        self.play(Write(f[1]), run_time=1.2)
        self.play(FadeIn(cap, shift=UP * 0.2))
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 2차시 · 단위원 — sin, cos 은 좌표 그 자체
# ──────────────────────────────────────────────────────────────
class S2UnitCircle(Scene):
    def construct(self):
        self.add(head("단위원 — sin θ, cos θ 는 점의 좌표 그 자체"))

        R = 2.3
        O = LEFT * 3.3 + DOWN * 0.7
        ax = VGroup(
            Line(O + LEFT * (R + 0.6), O + RIGHT * (R + 0.6),
                 color=FAINT, stroke_width=2),
            Line(O + DOWN * (R + 0.6), O + UP * (R + 0.6),
                 color=FAINT, stroke_width=2),
        )
        circ = Circle(radius=R, color=MUTED, stroke_width=3).move_to(O)
        self.play(Create(ax), Create(circ), run_time=1.1)

        th = ValueTracker(0.6)

        def P():
            t = th.get_value()
            return O + R * np.array([np.cos(t), np.sin(t), 0])

        arm = always_redraw(lambda: Line(O, P(), color=ACCENT, stroke_width=4))
        dot = always_redraw(lambda: Dot(P(), color=BAD, radius=0.1))
        xleg = always_redraw(lambda: Line(
            O, O + RIGHT * (P()[0] - O[0]), color=WARM, stroke_width=6))
        yleg = always_redraw(lambda: Line(
            O + RIGHT * (P()[0] - O[0]), P(), color=GOOD, stroke_width=6))
        arc = always_redraw(lambda: Arc(
            radius=0.5, start_angle=0, angle=th.get_value(),
            color=ACCENT, stroke_width=3).move_arc_center_to(O))

        self.play(Create(arm), FadeIn(dot), Create(arc))
        self.play(Create(xleg), Create(yleg))

        lblx = always_redraw(lambda: MathTex(r"\cos\theta", font_size=30, color=WARM)
                             .next_to(O + RIGHT * (P()[0] - O[0]) / 2, DOWN, buff=0.22))
        lbly = always_redraw(lambda: MathTex(r"\sin\theta", font_size=30, color=GOOD)
                             .next_to((O + RIGHT * (P()[0] - O[0]) + P()) / 2,
                                      RIGHT, buff=0.18))
        self.play(FadeIn(lblx), FadeIn(lbly))
        self.wait(0.5)

        defn = VGroup(
            MathTex(r"P(\cos\theta,\ \sin\theta)", font_size=42, color=INK),
            MathTex(r"\tan\theta=\dfrac{\sin\theta}{\cos\theta}",
                    font_size=40, color=ACCENT),
        ).arrange(DOWN, buff=0.6).move_to(RIGHT * 3.4 + UP * 1.5)
        self.play(Write(defn[0]), run_time=1.0)
        self.play(Write(defn[1]), run_time=1.0)

        self.play(th.animate.set_value(2.4), run_time=2.2)
        self.wait(0.3)
        self.play(th.animate.set_value(4.1), run_time=1.8)
        self.wait(0.3)
        self.play(th.animate.set_value(0.6), run_time=1.8)

        # 피타고라스 항등식
        iden = MathTex(r"\sin^{2}\theta+\cos^{2}\theta=1",
                       font_size=48, color=GOOD).move_to(RIGHT * 3.4 + DOWN * 1.4)
        why = kr("반지름이 1 인 원 위의 점이므로", 24, MUTED)
        why.next_to(iden, UP, buff=0.3)
        self.play(FadeIn(why), Write(iden), run_time=1.4)
        self.play(Create(box(iden, GOOD)))
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 3차시 · 그래프 — 단위원을 굴려서 그린다
# ──────────────────────────────────────────────────────────────
class S3TrigGraph(Scene):
    def construct(self):
        self.add(head("사인 곡선 — 단위원을 굴려서 그린다"))

        R = 1.5
        O = LEFT * 5.0 + DOWN * 0.5
        circ = Circle(radius=R, color=MUTED, stroke_width=3).move_to(O)

        ax = Axes(
            x_range=[0, 2 * np.pi + 0.3, np.pi / 2],
            y_range=[-1.5, 1.5, 1],
            x_length=8.2, y_length=3.0,
            axis_config={"color": FAINT, "stroke_width": 2,
                         "tip_width": 0.14, "tip_height": 0.14},
        ).move_to(RIGHT * 1.6 + DOWN * 0.5)
        self.play(Create(circ), Create(ax), run_time=1.1)

        th = ValueTracker(0.001)

        def P():
            t = th.get_value()
            return O + R * np.array([np.cos(t), np.sin(t), 0])

        arm = always_redraw(lambda: Line(O, P(), color=ACCENT, stroke_width=4))
        dot = always_redraw(lambda: Dot(P(), color=BAD, radius=0.09))
        graph = always_redraw(lambda: ax.plot(
            np.sin, x_range=[0, max(0.001, th.get_value())],
            color=GOOD, stroke_width=5))
        tip = always_redraw(lambda: Dot(
            ax.c2p(th.get_value(), np.sin(th.get_value())),
            color=BAD, radius=0.09))
        link = always_redraw(lambda: DashedLine(
            P(), ax.c2p(th.get_value(), np.sin(th.get_value())),
            color=FAINT, stroke_width=2, dash_length=0.1))

        self.play(Create(arm), FadeIn(dot))
        self.add(graph, tip, link)
        self.play(th.animate.set_value(2 * np.pi), run_time=5.0, rate_func=linear)
        self.wait(0.8)

        self.play(FadeOut(VGroup(circ, arm, dot, link, tip)), run_time=0.7)
        self.play(VGroup(ax, graph).animate.move_to(DOWN * 0.4).scale(1.05),
                  run_time=0.9)

        facts = VGroup(
            kr("주기 2π · 치역 [-1, 1] · 원점 대칭 (기함수)", 28, INK),
            # b=0 이면 분모가 0 이 되므로 조건을 함께 띄운다
            MathTex(r"y=a\sin(bx)\ \ (a\neq0,\ b\neq0)\ \Longrightarrow\ "
                    r"\text{max}=|a|,\ \ \text{period}=\tfrac{2\pi}{|b|}",
                    font_size=32, color=ACCENT),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 2.6)
        self.play(FadeIn(facts[0], shift=UP * 0.2), run_time=0.8)
        self.play(Write(facts[1]), run_time=1.3)
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 4차시 · 삼각함수의 성질 — 단위원 위의 대칭 한 번이면 끝
# ──────────────────────────────────────────────────────────────
class S4TrigIdentity(Scene):
    def construct(self):
        self.add(head("삼각함수의 성질 — 외우지 말고 단위원에서 접어라"))

        R = 2.1
        O = LEFT * 3.5 + DOWN * 0.6
        circ = Circle(radius=R, color=MUTED, stroke_width=3).move_to(O)
        ax = VGroup(
            Line(O + LEFT * (R + 0.5), O + RIGHT * (R + 0.5),
                 color=FAINT, stroke_width=2),
            Line(O + DOWN * (R + 0.5), O + UP * (R + 0.5),
                 color=FAINT, stroke_width=2),
        )
        self.play(Create(ax), Create(circ), run_time=1.0)

        t0 = 0.85
        Pp = O + R * np.array([np.cos(t0), np.sin(t0), 0])
        armP = Line(O, Pp, color=ACCENT, stroke_width=4)
        dotP = Dot(Pp, color=ACCENT, radius=0.1)
        lblP = MathTex(r"\theta", font_size=32, color=ACCENT).move_to(
            O + 0.75 * np.array([np.cos(t0 / 2), np.sin(t0 / 2), 0]))
        self.play(Create(armP), FadeIn(dotP), FadeIn(lblP))
        self.wait(0.4)

        cases = [
            (-t0, r"-\theta", "x축 대칭",
             r"\sin(-\theta)=-\sin\theta,\ \ \cos(-\theta)=\cos\theta", BAD),
            (np.pi - t0, r"\pi-\theta", "y축 대칭",
             r"\sin(\pi-\theta)=\sin\theta,\ \ \cos(\pi-\theta)=-\cos\theta", WARM),
            (np.pi + t0, r"\pi+\theta", "원점 대칭",
             r"\sin(\pi+\theta)=-\sin\theta,\ \ \cos(\pi+\theta)=-\cos\theta", GOOD),
        ]
        shown = VGroup()
        for i, (t, tex, how, res, col) in enumerate(cases):
            Q = O + R * np.array([np.cos(t), np.sin(t), 0])
            arm = Line(O, Q, color=col, stroke_width=4)
            d = Dot(Q, color=col, radius=0.1)
            lb = MathTex(tex, font_size=30, color=col).next_to(d, RIGHT if np.cos(t) > 0
                                                               else LEFT, buff=0.18)
            title = kr(how, 26, col, BOLD).move_to(RIGHT * 3.3 + UP * 2.1)
            eq = MathTex(res, font_size=34, color=INK).move_to(RIGHT * 3.3 + UP * 1.35)

            self.play(Create(arm), FadeIn(d), FadeIn(lb), run_time=0.8)
            self.play(FadeIn(title), Write(eq), run_time=1.2)
            self.wait(1.3)
            self.play(FadeOut(VGroup(arm, d, lb, title, eq)), run_time=0.5)

        # π/2 ± θ 는 sin ↔ cos 이 바뀐다
        self.play(FadeOut(VGroup(circ, ax, armP, dotP, lblP)), run_time=0.7)
        rule = VGroup(
            kr("π 를 더하거나 빼면 — 함수는 그대로, 부호만 확인", 29, INK),
            kr("π/2 를 더하거나 빼면 — sin ↔ cos 으로 바뀐다", 29, BAD, BOLD),
        ).arrange(DOWN, buff=0.4).move_to(UP * 1.4)
        ex = MathTex(r"\sin\!\left(\tfrac{\pi}{2}+\theta\right)=\cos\theta,"
                     r"\qquad \cos\!\left(\tfrac{\pi}{2}+\theta\right)=-\sin\theta",
                     font_size=40, color=GOOD).move_to(DOWN * 0.6)
        self.play(FadeIn(rule[0], shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(rule[1], shift=UP * 0.2), run_time=0.8)
        self.play(Write(ex), run_time=1.5)
        self.play(Create(box(ex, GOOD)))
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 5차시 · 삼각방정식 — 그래프와 직선의 교점
# ──────────────────────────────────────────────────────────────
class S5TrigSolve(Scene):
    def construct(self):
        self.add(head("삼각방정식 — 곡선과 직선의 교점을 읽는다"))

        ax = Axes(
            x_range=[0, 2 * np.pi + 0.2, np.pi / 2],
            y_range=[-1.4, 1.4, 1],
            x_length=10.4, y_length=4.0,
            axis_config={"color": FAINT, "stroke_width": 2,
                         "tip_width": 0.14, "tip_height": 0.14},
        ).move_to(DOWN * 0.6)
        curve = ax.plot(np.sin, x_range=[0, 2 * np.pi], color=ACCENT, stroke_width=5)
        c_lbl = MathTex(r"y=\sin x", font_size=34, color=ACCENT)
        c_lbl.next_to(ax.c2p(1.2, 1.0), UP, buff=0.1)
        self.play(Create(ax), Create(curve), FadeIn(c_lbl), run_time=1.6)

        # x축 눈금 π/2 단위
        ticks = VGroup()
        for v, tex in ((np.pi / 2, r"\tfrac{\pi}{2}"), (np.pi, r"\pi"),
                       (3 * np.pi / 2, r"\tfrac{3\pi}{2}"), (2 * np.pi, r"2\pi")):
            ticks.add(MathTex(tex, font_size=26, color=MUTED)
                      .next_to(ax.c2p(v, 0), DOWN, buff=0.22))
        self.play(FadeIn(ticks), run_time=0.6)

        eq = MathTex(r"\sin x=\tfrac{1}{2}", font_size=46, color=INK)
        eq.move_to(LEFT * 4.6 + UP * 2.2)
        self.play(Write(eq))

        line = ax.plot(lambda x: 0.5, x_range=[0, 2 * np.pi],
                       color=WARM, stroke_width=4)
        l_lbl = MathTex(r"y=\tfrac{1}{2}", font_size=30, color=WARM)
        l_lbl.next_to(ax.c2p(2 * np.pi, 0.5), RIGHT, buff=0.12)
        self.play(Create(line), FadeIn(l_lbl), run_time=1.0)

        sols = [np.pi / 6, 5 * np.pi / 6]
        dots = VGroup(*[Dot(ax.c2p(s, 0.5), color=BAD, radius=0.1) for s in sols])
        drops = VGroup(*[DashedLine(ax.c2p(s, 0.5), ax.c2p(s, 0),
                                    color=BAD, stroke_width=2.5, dash_length=0.1)
                         for s in sols])
        labs = VGroup(
            MathTex(r"\tfrac{\pi}{6}", font_size=30, color=BAD)
            .next_to(ax.c2p(sols[0], 0), DOWN, buff=0.22),
            MathTex(r"\tfrac{5\pi}{6}", font_size=30, color=BAD)
            .next_to(ax.c2p(sols[1], 0), DOWN, buff=0.22),
        )
        self.play(FadeIn(dots, scale=0.4), run_time=0.7)
        self.play(Create(drops), FadeIn(labs), run_time=1.0)
        self.wait(1.0)

        ans = MathTex(r"x=\tfrac{\pi}{6}\ \ \text{or}\ \ x=\tfrac{5\pi}{6}",
                      font_size=40, color=GOOD).move_to(RIGHT * 4.2 + UP * 2.2)
        self.play(Write(ans), run_time=1.1)
        self.wait(1.2)

        # 부등식 — 직선보다 아래쪽
        ineq = MathTex(r"\sin x<\tfrac{1}{2}", font_size=46, color=INK)
        ineq.move_to(LEFT * 4.6 + UP * 2.2)
        self.play(ReplacementTransform(eq, ineq), FadeOut(ans), run_time=0.9)

        band1 = ax.plot(np.sin, x_range=[0, sols[0]], color=GOOD, stroke_width=8)
        band2 = ax.plot(np.sin, x_range=[sols[1], 2 * np.pi],
                        color=GOOD, stroke_width=8)
        self.play(Create(band1), Create(band2), run_time=1.4)

        ans2 = MathTex(r"0\le x<\tfrac{\pi}{6}\ \ \text{or}\ \ "
                       r"\tfrac{5\pi}{6}<x<2\pi",
                       font_size=36, color=GOOD).move_to(RIGHT * 3.6 + UP * 2.2)
        self.play(Write(ans2), run_time=1.3)
        tip = kr("직선보다 아래에 있는 구간을 읽으면 된다", 26, MUTED)
        tip.move_to(DOWN * 3.2)
        self.play(FadeIn(tip, shift=UP * 0.2))
        self.wait(2.2)
