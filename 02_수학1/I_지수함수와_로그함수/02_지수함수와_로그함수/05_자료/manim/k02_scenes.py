# -*- coding: utf-8 -*-
"""
2027 EBS 수능특강 수학Ⅰ — 강02 「지수함수와 로그함수」 시각화

  S1ExpGraph      1차시 · 지수함수의 그래프와 성질
  S2ExpTransform  2차시 · 지수함수의 이동과 최대·최소
  S3LogGraph      3차시 · 로그함수 — 지수함수의 역함수
  S4LogTransform  4차시 · 로그함수의 이동과 진수 조건
  S5ExpLogSolve   5차시 · 지수·로그 방정식과 부등식

렌더: 00_공통/01_템플릿/build_manim.ps1
"""
import sys

sys.path.insert(0, r"D:\test1234\00_공통\01_템플릿")
from slide_theme import *   # noqa: F403,F401


# ──────────────────────────────────────────────────────────────
# 1차시 · 지수함수의 그래프 — 밑이 1을 넘느냐가 모든 것을 가른다
# ──────────────────────────────────────────────────────────────
class S1ExpGraph(Scene):
    def construct(self):
        hd = head("지수함수 y=aˣ — 밑 a 가 방향을 정한다")
        self.add(hd)

        ax = Axes(
            x_range=[-3.2, 3.2, 1], y_range=[-0.6, 4.4, 1],
            x_length=9.0, y_length=5.0,
            axis_config={"color": FAINT, "stroke_width": 2,
                         "tip_width": 0.16, "tip_height": 0.16},
        ).move_to(DOWN * 0.55)
        self.play(Create(ax), run_time=1.0)

        # 점근선 y = 0
        asym = DashedLine(ax.c2p(-3.2, 0), ax.c2p(3.2, 0),
                          color=BAD, stroke_width=3, dash_length=0.12)
        asym_lbl = kr("점근선  y = 0", 24, BAD).next_to(ax.c2p(2.4, 0), UP, buff=0.18)

        a = ValueTracker(2.0)

        def clipped(fn):
            """치역이 y_range 를 넘지 않는 x 구간만 그린다."""
            lo, hi = -3.1, 3.1
            xs = [lo + (hi - lo) * i / 400 for i in range(401)]
            xs = [x for x in xs if fn(x) <= 4.3]
            if not xs:
                xs = [0.0]
            return min(xs), max(xs)

        def curve():
            v = a.get_value()
            f = lambda x: v ** x
            lo, hi = clipped(f)
            return ax.plot(f, x_range=[lo, hi], color=ACCENT, stroke_width=5)

        g = always_redraw(curve)
        self.play(Create(g), run_time=1.3)
        self.play(Create(asym), FadeIn(asym_lbl), run_time=0.8)

        # 모든 지수함수가 지나는 점 (0, 1)
        p = Dot(ax.c2p(0, 1), color=WARM, radius=0.1)
        p_lbl = MathTex("(0,\\,1)", font_size=32, color=WARM)
        p_lbl.next_to(p, RIGHT, buff=0.2).shift(UP * 0.12)
        self.play(FadeIn(p, scale=0.4), FadeIn(p_lbl))
        self.play(Flash(p, color=WARM, line_length=0.25))
        self.wait(0.5)

        readout = always_redraw(lambda: VGroup(
            MathTex("a=", font_size=36, color=ACCENT),
            DecimalNumber(a.get_value(), num_decimal_places=2,
                          font_size=36, color=ACCENT),
        ).arrange(RIGHT, buff=0.1).move_to(RIGHT * 5.3 + UP * 1.9))
        self.play(FadeIn(readout))

        note = kr("a 를 1 쪽으로 밀어 보자", 28, MUTED).move_to(LEFT * 4.3 + UP * 1.95)
        self.play(FadeIn(note, shift=UP * 0.2))

        # a > 1 : 증가 → a 를 1 에 가깝게 → 0 < a < 1 : 감소
        self.play(a.animate.set_value(1.25), run_time=2.0, rate_func=linear)
        self.wait(0.4)
        self.play(a.animate.set_value(0.4), run_time=2.4, rate_func=linear)
        self.wait(0.8)

        wipe(self, hd, run_time=0.9)

        # 성질 정리
        left = VGroup(
            kr("a > 1", 34, ACCENT, BOLD),
            kr("x 가 커지면 y 도 커진다", 27, INK),
            kr("(증가함수)", 24, MUTED),
        ).arrange(DOWN, buff=0.22)
        right = VGroup(
            kr("0 < a < 1", 34, WARM, BOLD),
            kr("x 가 커지면 y 는 작아진다", 27, INK),
            kr("(감소함수)", 24, MUTED),
        ).arrange(DOWN, buff=0.22)
        cols = VGroup(left, right).arrange(RIGHT, buff=2.2).move_to(UP * 0.85)

        common = VGroup(
            kr("정의역 = 실수 전체 · 치역 = 양의 실수 전체", 27, INK),
            kr("항상 점 (0, 1) 을 지나고 점근선은 x 축", 27, INK),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 1.9)
        frame = box(common, GOOD, fill=GOOD_SOFT)

        self.play(FadeIn(left, shift=RIGHT * 0.3), run_time=0.7)
        self.play(FadeIn(right, shift=LEFT * 0.3), run_time=0.7)
        self.wait(0.6)
        self.play(FadeIn(frame), Write(common), run_time=1.3)
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 2차시 · 이동과 최대·최소 — 점근선이 따라 움직인다
# ──────────────────────────────────────────────────────────────
class S2ExpTransform(Scene):
    def construct(self):
        hd = head("평행이동 — 점근선이 같이 따라간다")
        self.add(hd)

        ax = Axes(
            x_range=[-2.6, 4.6, 1], y_range=[-1.4, 5.0, 1],
            x_length=8.6, y_length=5.0,
            axis_config={"color": FAINT, "stroke_width": 2,
                         "tip_width": 0.16, "tip_height": 0.16},
        ).move_to(DOWN * 0.6)
        self.play(Create(ax), run_time=0.9)

        base = ax.plot(lambda x: 2 ** x, x_range=[-2.5, 2.15],
                       color=FAINT, stroke_width=4)
        base_lbl = MathTex("y=2^{x}", font_size=34, color=MUTED)
        base_lbl.next_to(ax.c2p(2.15, 4.4), RIGHT, buff=0.1)
        self.play(Create(base), FadeIn(base_lbl), run_time=1.1)

        m = ValueTracker(0.0)   # x 방향
        n = ValueTracker(0.0)   # y 방향

        def moved():
            mm, nn = m.get_value(), n.get_value()
            f = lambda x: 2 ** (x - mm) + nn
            hi = mm + 2.15
            hi = min(hi, 4.5)
            return ax.plot(f, x_range=[-2.5, hi], color=ACCENT, stroke_width=5)

        def asym():
            nn = n.get_value()
            return DashedLine(ax.c2p(-2.6, nn), ax.c2p(4.6, nn),
                              color=BAD, stroke_width=3, dash_length=0.12)

        g = always_redraw(moved)
        asy = always_redraw(asym)
        self.play(Create(g), Create(asy), run_time=1.0)

        eq = always_redraw(lambda: MathTex(
            f"y=2^{{x-{m.get_value():.1f}}}+{n.get_value():.1f}",
            font_size=40, color=ACCENT).move_to(RIGHT * 4.2 + UP * 2.15))
        self.play(FadeIn(eq))
        self.wait(0.5)

        self.play(m.animate.set_value(2.0), run_time=1.8)
        self.wait(0.4)
        self.play(n.animate.set_value(1.0), run_time=1.6)
        self.wait(0.9)

        concl = VGroup(
            kr("x 축으로 m, y 축으로 n 만큼 옮기면", 27, INK),
            MathTex(r"y=a^{\,x-m}+n", font_size=42, color=GOOD),
            kr("점근선은 y = n, 지나는 점은 (m, n+1)", 27, INK),
        ).arrange(DOWN, buff=0.22)
        frame = box(concl, GOOD, fill=GOOD_SOFT)
        grp = VGroup(frame, concl)

        self.play(FadeOut(VGroup(ax, base, base_lbl, g, asy, eq)), run_time=0.8)
        self.play(FadeIn(frame), Write(concl), run_time=1.5)
        self.wait(1.4)
        self.play(FadeOut(grp), run_time=0.6)

        # 최대·최소는 양 끝에서만 난다
        self.play(FadeIn(kr("정의역이 닫힌 구간이면 — 최댓값·최솟값은 양 끝에서만",
                            32, INK, BOLD).move_to(UP * 2.3)))
        rows = VGroup(
            VGroup(kr("a > 1  (증가)", 28, ACCENT, BOLD),
                   MathTex(r"x=m\ \text{min}\ \ \ x=n\ \text{max}",
                           font_size=32, color=INK)).arrange(RIGHT, buff=0.9),
            VGroup(kr("0 < a < 1  (감소)", 28, WARM, BOLD),
                   MathTex(r"x=m\ \text{max}\ \ \ x=n\ \text{min}",
                           font_size=32, color=INK)).arrange(RIGHT, buff=0.9),
        ).arrange(DOWN, buff=0.75, aligned_edge=LEFT).move_to(UP * 0.4)
        for r in rows:
            self.play(FadeIn(r, shift=UP * 0.2), run_time=0.8)
        self.wait(0.6)

        warn = kr("정의역 안에 꼭짓점이 없으므로, 끝값 두 개만 비교하면 끝",
                  28, GOOD, BOLD).move_to(DOWN * 2.1)
        self.play(FadeIn(warn, shift=UP * 0.2))
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 3차시 · 로그함수 — 지수함수를 y=x 로 접은 것
# ──────────────────────────────────────────────────────────────
class S3LogGraph(Scene):
    def construct(self):
        hd = head("로그함수 — 지수함수를 y=x 에 대해 접은 것")
        self.add(hd)

        ax = Axes(
            x_range=[-3.4, 4.4, 1], y_range=[-3.4, 4.4, 1],
            x_length=6.4, y_length=6.4,
            axis_config={"color": FAINT, "stroke_width": 2,
                         "tip_width": 0.15, "tip_height": 0.15},
        ).move_to(DOWN * 0.5 + LEFT * 2.4)
        self.play(Create(ax), run_time=0.9)

        expo = ax.plot(lambda x: 2 ** x, x_range=[-3.3, 2.1],
                       color=ACCENT, stroke_width=5)
        e_lbl = MathTex("y=2^{x}", font_size=32, color=ACCENT)
        e_lbl.move_to(ax.c2p(-0.3, 4.0))   # 곡선과 겹치지 않도록 왼쪽 위에
        self.play(Create(expo), FadeIn(e_lbl), run_time=1.2)

        mirror = DashedLine(ax.c2p(-3.3, -3.3), ax.c2p(4.3, 4.3),
                            color=MUTED, stroke_width=2.5, dash_length=0.12)
        m_lbl = MathTex("y=x", font_size=30, color=MUTED).move_to(ax.c2p(3.7, 3.2))
        self.play(Create(mirror), FadeIn(m_lbl), run_time=0.9)
        self.wait(0.4)

        # y=x 에 대해 접기
        import numpy as np
        # log2(0.1) = -3.32 — y_range 하한(-3.4) 안에 들어오도록 시작점을 잡는다
        logc = ax.plot(lambda x: np.log2(x), x_range=[0.1, 4.3],
                       color=WARM, stroke_width=5)
        l_lbl = MathTex(r"y=\log_{2}x", font_size=32, color=WARM)
        l_lbl.move_to(ax.c2p(3.5, 1.3))

        fold = kr("y = x 에 대해 대칭", 26, MUTED).move_to(RIGHT * 2.9 + UP * 2.4)
        self.play(FadeIn(fold, shift=DOWN * 0.2))
        self.play(TransformFromCopy(expo, logc), run_time=1.8)
        self.play(FadeIn(l_lbl))
        self.wait(0.6)

        # 대응하는 점 한 쌍
        d1 = Dot(ax.c2p(1, 2), color=ACCENT, radius=0.09)
        d2 = Dot(ax.c2p(2, 1), color=WARM, radius=0.09)
        t1 = MathTex("(1,2)", font_size=28, color=ACCENT).next_to(d1, LEFT, buff=0.15)
        t2 = MathTex("(2,1)", font_size=28, color=WARM).next_to(d2, DOWN, buff=0.15)
        link = DashedLine(d1.get_center(), d2.get_center(),
                          color=FAINT, stroke_width=2, dash_length=0.08)
        self.play(FadeIn(d1, scale=0.4), FadeIn(t1))
        self.play(Create(link), FadeIn(d2, scale=0.4), FadeIn(t2))
        self.wait(0.8)

        # 성질 요약 (오른쪽)
        table = VGroup(
            VGroup(kr("정의역", 26, MUTED),
                   MathTex(r"x>0", font_size=32, color=INK)).arrange(RIGHT, buff=0.5),
            VGroup(kr("치역", 26, MUTED),
                   kr("실수 전체", 26, INK)).arrange(RIGHT, buff=0.5),
            VGroup(kr("지나는 점", 26, MUTED),
                   MathTex(r"(1,\,0)", font_size=32, color=INK)).arrange(RIGHT, buff=0.5),
            VGroup(kr("점근선", 26, MUTED),
                   MathTex(r"x=0\ (y\text{-axis})", font_size=30, color=BAD)
                   ).arrange(RIGHT, buff=0.5),
        ).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        table.move_to(RIGHT * 4.1 + DOWN * 0.9)
        self.play(LaggedStartMap(FadeIn, table, shift=LEFT * 0.25, lag_ratio=0.25),
                  run_time=1.6)
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 4차시 · 로그함수의 이동 — 점근선과 진수 조건이 함께 옮겨간다
# ──────────────────────────────────────────────────────────────
class S4LogTransform(Scene):
    def construct(self):
        hd = head("로그함수의 이동 — 진수 조건이 같이 옮겨간다")
        self.add(hd)

        import numpy as np
        ax = Axes(
            x_range=[-1.4, 6.6, 1], y_range=[-3.0, 3.0, 1],
            x_length=8.8, y_length=4.8,
            axis_config={"color": FAINT, "stroke_width": 2,
                         "tip_width": 0.16, "tip_height": 0.16},
        ).move_to(DOWN * 0.7)
        self.play(Create(ax), run_time=0.9)

        m = ValueTracker(0.0)
        n = ValueTracker(0.0)

        def moved():
            mm, nn = m.get_value(), n.get_value()
            lo = mm + 0.06
            return ax.plot(lambda x: np.log2(x - mm) + nn,
                           x_range=[lo, 6.5], color=ACCENT, stroke_width=5)

        def asym():
            mm = m.get_value()
            return DashedLine(ax.c2p(mm, -3.0), ax.c2p(mm, 3.0),
                              color=BAD, stroke_width=3, dash_length=0.12)

        g = always_redraw(moved)
        asy = always_redraw(asym)
        self.play(Create(g), Create(asy), run_time=1.2)

        eq = always_redraw(lambda: MathTex(
            f"y=\\log_{{2}}(x-{m.get_value():.1f})+{n.get_value():.1f}",
            font_size=38, color=ACCENT).move_to(RIGHT * 3.6 + UP * 2.15))
        cond = always_redraw(lambda: MathTex(
            f"x>{m.get_value():.1f}", font_size=36, color=BAD
        ).move_to(LEFT * 4.6 + UP * 2.15))
        c_lbl = kr("진수 조건", 24, BAD).next_to(cond, UP, buff=0.18)

        self.play(FadeIn(eq), FadeIn(cond), FadeIn(c_lbl))
        self.wait(0.6)

        self.play(m.animate.set_value(2.0), run_time=2.0)
        self.wait(0.5)
        self.play(n.animate.set_value(1.0), run_time=1.5)
        self.wait(0.9)

        concl = VGroup(
            MathTex(r"y=\log_{a}(x-m)+n", font_size=42, color=GOOD),
            kr("점근선  x = m  ·  지나는 점  (1+m, n)", 27, INK),
            kr("진수 조건도 x > m 으로 함께 옮겨간다", 27, BAD),
        ).arrange(DOWN, buff=0.24)
        frame = box(concl, GOOD, fill=GOOD_SOFT)

        self.play(FadeOut(VGroup(ax, g, asy, eq, cond, c_lbl)), run_time=0.8)
        self.play(FadeIn(frame), Write(concl), run_time=1.6)
        self.wait(2.4)


# ──────────────────────────────────────────────────────────────
# 5차시 · 지수·로그 방정식과 부등식 — 밑이 1보다 작으면 뒤집힌다
# ──────────────────────────────────────────────────────────────
class S5ExpLogSolve(Scene):
    def construct(self):
        hd = head("부등식 — 밑이 1보다 작으면 부등호가 뒤집힌다")
        self.add(hd)

        base = MathTex(r"a^{x_{1}}<a^{x_{2}}", font_size=52, color=INK)
        base.move_to(UP * 1.95)
        self.play(Write(base))
        self.wait(0.6)

        import numpy as np
        ax = Axes(
            x_range=[-2.4, 2.4, 1], y_range=[-0.4, 3.6, 1],
            x_length=5.0, y_length=3.4,
            axis_config={"color": FAINT, "stroke_width": 2,
                         "tip_width": 0.14, "tip_height": 0.14},
        )
        axL = ax.copy().move_to(LEFT * 3.4 + DOWN * 0.9)
        axR = ax.copy().move_to(RIGHT * 3.4 + DOWN * 0.9)

        cL = axL.plot(lambda x: 2 ** x, x_range=[-2.3, 1.8],
                      color=ACCENT, stroke_width=5)
        cR = axR.plot(lambda x: 0.5 ** x, x_range=[-1.8, 2.3],
                      color=WARM, stroke_width=5)
        tL = kr("a > 1  (증가)", 28, ACCENT, BOLD).next_to(axL, UP, buff=0.15)
        tR = kr("0 < a < 1  (감소)", 28, WARM, BOLD).next_to(axR, UP, buff=0.15)

        self.play(Create(axL), Create(axR), run_time=0.9)
        self.play(Create(cL), Create(cR), run_time=1.2)
        self.play(FadeIn(tL), FadeIn(tR))
        self.wait(0.5)

        # 전제는 a^x1 < a^x2 — 즉 x1 의 높이가 x2 보다 '낮아야' 한다.
        # 증가함수에서는 x1 이 왼쪽에, 감소함수에서는 x1 이 오른쪽에 와야
        # 그 전제가 성립한다. 이 배치 자체가 결론을 보여 준다.
        for axis, fn, x1, x2 in ((axL, lambda x: 2 ** x, -1, 1),
                                 (axR, lambda x: 0.5 ** x, 1, -1)):
            p1 = Dot(axis.c2p(x1, fn(x1)), color=BAD, radius=0.085)
            p2 = Dot(axis.c2p(x2, fn(x2)), color=GOOD, radius=0.085)
            l1 = MathTex("x_{1}", font_size=28, color=BAD).next_to(
                axis.c2p(x1, 0), DOWN, buff=0.16)
            l2 = MathTex("x_{2}", font_size=28, color=GOOD).next_to(
                axis.c2p(x2, 0), DOWN, buff=0.16)
            self.play(FadeIn(p1, scale=0.4), FadeIn(p2, scale=0.4),
                      FadeIn(l1), FadeIn(l2), run_time=0.7)

        self.wait(0.6)

        resL = MathTex(r"x_{1}<x_{2}", font_size=38, color=GOOD)
        resL.next_to(axL, DOWN, buff=0.35)
        resR = MathTex(r"x_{1}>x_{2}", font_size=38, color=BAD)
        resR.next_to(axR, DOWN, buff=0.35)
        self.play(Write(resL), run_time=0.8)
        self.play(Write(resR), run_time=0.8)
        self.play(Indicate(resR, color=BAD, scale_factor=1.2))
        self.wait(1.4)

        self.play(FadeOut(VGroup(base, axL, axR, cL, cR, tL, tR, resL, resR)),
                  run_time=0.9)
        self.clear()
        hd = head("부등식 — 밑이 1보다 작으면 부등호가 뒤집힌다")
        self.add(hd)

        # 로그부등식은 진수 조건을 먼저
        self.play(FadeIn(kr("로그부등식은 진수 조건을 먼저 챙긴다", 34, INK, BOLD)
                         .move_to(UP * 2.2)))
        steps = VGroup(
            MathTex(r"\log_{2}(2x-1)<\log_{2}(x+1)", font_size=40, color=INK),
            MathTex(r"2x-1>0,\quad x+1>0\ \Longrightarrow\ x>\tfrac{1}{2}",
                    font_size=36, color=BAD),
            MathTex(r"2x-1<x+1\ \Longrightarrow\ x<2", font_size=36, color=ACCENT),
            MathTex(r"\therefore\ \tfrac{1}{2}<x<2", font_size=44, color=GOOD),
        ).arrange(DOWN, buff=0.55).move_to(DOWN * 0.35)

        labels = [None, "진수 조건", "밑이 2 (>1) 이므로 부등호 그대로", None]
        for s, lab in zip(steps, labels):
            self.play(Write(s), run_time=1.1)
            if lab:
                d = kr(lab, 22, MUTED).next_to(s, RIGHT, buff=0.5)
                self.play(FadeIn(d, shift=LEFT * 0.15), run_time=0.45)
            self.wait(0.3)

        self.play(Create(box(steps[3], GOOD)))
        self.wait(2.2)
