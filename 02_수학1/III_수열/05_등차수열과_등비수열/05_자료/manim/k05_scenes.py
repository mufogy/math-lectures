# -*- coding: utf-8 -*-
"""
2027 EBS 수능특강 수학Ⅰ — 강05 「등차수열과 등비수열」 시각화

  S1ArithTerm   1차시 · 등차수열의 일반항과 등차중항
  S2ArithSum    2차시 · 등차수열의 합 — 거꾸로 더하기
  S3SnAn        3차시 · Sn 과 an 의 관계
  S4GeoTerm     4차시 · 등비수열의 일반항과 등비중항
  S5GeoSum      5차시 · 등비수열의 합 — r 배 하고 빼기

렌더: 00_공통/01_템플릿/build_manim.ps1
"""
import sys

sys.path.insert(0, r"D:\test1234\00_공통\01_템플릿")
from slide_theme import *   # noqa: F403,F401


# ──────────────────────────────────────────────────────────────
# 1차시 · 등차수열 — 같은 간격을 (n-1)번 건너뛴다
# ──────────────────────────────────────────────────────────────
class S1ArithTerm(Scene):
    def construct(self):
        hd = head("등차수열 — 같은 간격을 (n-1) 번 건너뛴다")
        self.add(hd)

        a, d = 3, 4
        n = 6
        nl = NumberLine(x_range=[0, 26, 2], length=11.4,
                        color=FAINT, stroke_width=3).move_to(UP * 0.55)
        self.play(Create(nl), run_time=0.9)

        dots, labels = VGroup(), VGroup()
        for i in range(n):
            v = a + i * d
            dt = Dot(nl.n2p(v), color=ACCENT, radius=0.1)
            lb = MathTex(f"a_{{{i+1}}}", font_size=30, color=ACCENT)
            lb.next_to(dt, UP, buff=0.28)
            vl = MathTex(str(v), font_size=28, color=INK)
            vl.next_to(dt, DOWN, buff=0.28)
            dots.add(dt)
            labels.add(VGroup(lb, vl))

        self.play(FadeIn(dots[0], scale=0.4), FadeIn(labels[0]))
        for i in range(1, n):
            arr = Arrow(nl.n2p(a + (i - 1) * d), nl.n2p(a + i * d),
                        color=WARM, stroke_width=4, buff=0.08,
                        max_tip_length_to_length_ratio=0.22)
            dl = MathTex("+d", font_size=26, color=WARM)
            dl.next_to(arr, UP, buff=0.05)
            self.play(GrowArrow(arr), FadeIn(dl), run_time=0.35)
            self.play(FadeIn(dots[i], scale=0.4), FadeIn(labels[i]), run_time=0.3)

        self.wait(0.7)
        count = kr("첫째항에서 d 를 (n-1) 번 더한다", 30, INK, BOLD)
        count.move_to(DOWN * 1.6)
        self.play(FadeIn(count, shift=UP * 0.2))

        gen = MathTex(r"a_{n}=a+(n-1)d", font_size=52, color=GOOD)
        gen.move_to(DOWN * 2.6)
        self.play(Write(gen), run_time=1.2)
        self.play(Create(box(gen, GOOD)))
        self.wait(1.6)

        wipe(self, hd)

        # 등차중항
        self.play(FadeIn(kr("등차중항 — 가운데 항은 양옆의 평균", 34, INK, BOLD)
                         .move_to(UP * 2.2)))
        three = VGroup(
            MathTex("a", font_size=48, color=ACCENT),
            MathTex("b", font_size=48, color=BAD),
            MathTex("c", font_size=48, color=ACCENT),
        ).arrange(RIGHT, buff=2.4).move_to(UP * 0.7)
        self.play(FadeIn(three, shift=UP * 0.2))

        g1 = MathTex("b-a", font_size=30, color=WARM).move_to(
            (three[0].get_center() + three[1].get_center()) / 2 + DOWN * 0.75)
        g2 = MathTex("c-b", font_size=30, color=WARM).move_to(
            (three[1].get_center() + three[2].get_center()) / 2 + DOWN * 0.75)
        eqg = MathTex("=", font_size=36, color=WARM).move_to(
            three[1].get_center() + DOWN * 0.75)
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(eqg))
        self.wait(0.7)

        res = MathTex(r"2b=a+c\qquad b=\frac{a+c}{2}",
                      font_size=46, color=GOOD).move_to(DOWN * 2.1)
        self.play(Write(res), run_time=1.3)
        self.play(Create(box(res, GOOD)))
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 2차시 · 등차수열의 합 — 거꾸로 써서 더하면 전부 같아진다
# ──────────────────────────────────────────────────────────────
class S2ArithSum(Scene):
    def construct(self):
        hd = head("등차수열의 합 — 거꾸로 써서 더한다")
        self.add(hd)

        terms = ["a", "a+d", "a+2d", r"\cdots", "l-d", "l"]
        rev = ["l", "l-d", r"\cdots", "a+2d", "a+d", "a"]

        row1 = VGroup(*[MathTex(t, font_size=36, color=ACCENT) for t in terms])
        row2 = VGroup(*[MathTex(t, font_size=36, color=WARM) for t in rev])
        for r in (row1, row2):
            r.arrange(RIGHT, buff=0.72)
        row1.move_to(UP * 1.7)
        row2.move_to(UP * 0.55)

        s1 = MathTex("S_{n}=", font_size=36, color=INK).next_to(row1, LEFT, buff=0.35)
        s2 = MathTex("S_{n}=", font_size=36, color=INK).next_to(row2, LEFT, buff=0.35)

        self.play(FadeIn(s1), Write(row1), run_time=1.4)
        self.wait(0.5)
        note = kr("같은 합을 거꾸로 한 번 더 쓴다", 26, MUTED).move_to(RIGHT * 4.6 + UP * 1.1)
        self.play(FadeIn(note, shift=LEFT * 0.2))
        self.play(FadeIn(s2), TransformFromCopy(row1, row2), run_time=1.6)
        self.wait(0.6)

        line = Line(LEFT * 6.3, RIGHT * 6.3, color=MUTED, stroke_width=2.5)
        line.move_to(DOWN * 0.15)
        plus = MathTex("+", font_size=40, color=MUTED).move_to(LEFT * 6.0 + UP * 0.2)
        self.play(Create(line), FadeIn(plus))

        # 세로로 더하면 모두 (a+l)
        pairs = VGroup()
        for i in range(6):
            x = row1[i].get_center()[0]
            p = MathTex("a+l", font_size=32, color=GOOD).move_to(
                np.array([x, -0.85, 0]))
            pairs.add(p)
        s3 = MathTex("2S_{n}=", font_size=36, color=INK).next_to(pairs, LEFT, buff=0.35)
        self.play(FadeIn(s3), LaggedStartMap(FadeIn, pairs, shift=DOWN * 0.2,
                                             lag_ratio=0.15), run_time=1.6)
        brace = Brace(pairs, DOWN, color=MUTED)
        bl = kr("n 개", 26, MUTED).next_to(brace, DOWN, buff=0.12)
        self.play(GrowFromCenter(brace), FadeIn(bl))
        self.wait(0.8)

        res = VGroup(
            MathTex(r"2S_{n}=n(a+l)", font_size=44, color=INK),
            MathTex(r"S_{n}=\frac{n(a+l)}{2}=\frac{n\{2a+(n-1)d\}}{2}",
                    font_size=46, color=GOOD),
        ).arrange(DOWN, buff=0.4).move_to(DOWN * 2.6)
        self.play(Write(res[0]), run_time=0.9)
        self.play(Write(res[1]), run_time=1.5)
        self.play(Create(box(res[1], GOOD, buff=0.25)))
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 3차시 · Sn 과 an — 겹치는 부분을 빼면 한 항만 남는다
# ──────────────────────────────────────────────────────────────
class S3SnAn(Scene):
    def construct(self):
        hd = head("Sₙ 과 aₙ — 겹치는 부분을 빼면 한 항만 남는다")
        self.add(hd)

        w, h, gap = 0.95, 0.62, 0.1
        base = LEFT * 4.6 + UP * 1.3

        def bar(i, color, opacity=1.0):
            r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5,
                          fill_color=color, fill_opacity=opacity)
            r.move_to(base + RIGHT * i * (w + gap))
            t = MathTex(f"a_{{{i+1}}}" if i < 4 else "a_n",
                        font_size=24, color="#ffffff").move_to(r.get_center())
            return VGroup(r, t)

        # Sn : a1 .. an
        Sn = VGroup(*[bar(i, ACCENT) for i in range(6)])
        Sn[4][1].become(MathTex(r"a_{n-1}", font_size=20, color="#ffffff")
                        .move_to(Sn[4][0].get_center()))
        Sn[5][1].become(MathTex("a_{n}", font_size=22, color="#ffffff")
                        .move_to(Sn[5][0].get_center()))
        lblS = MathTex("S_{n}=", font_size=34, color=INK).next_to(Sn, LEFT, buff=0.3)
        self.play(FadeIn(lblS), LaggedStartMap(FadeIn, Sn, shift=UP * 0.15,
                                               lag_ratio=0.12), run_time=1.4)

        # Sn-1 : a1 .. a(n-1)
        Sm = VGroup(*[bar(i, WARM) for i in range(5)])
        Sm.shift(DOWN * 1.35)
        Sm[4][1].become(MathTex(r"a_{n-1}", font_size=20, color="#ffffff")
                        .move_to(Sm[4][0].get_center()))
        lblM = MathTex("S_{n-1}=", font_size=34, color=INK).next_to(Sm, LEFT, buff=0.3)
        self.play(FadeIn(lblM), LaggedStartMap(FadeIn, Sm, shift=UP * 0.15,
                                               lag_ratio=0.12), run_time=1.2)
        self.wait(0.6)

        # 겹치는 부분이 상쇄된다
        cross = VGroup(*[
            Cross(Sn[i][0], stroke_color=BAD, stroke_width=4).scale(0.9)
            for i in range(5)
        ])
        cross2 = VGroup(*[
            Cross(Sm[i][0], stroke_color=BAD, stroke_width=4).scale(0.9)
            for i in range(5)
        ])
        self.play(Create(cross), Create(cross2), run_time=1.2)
        self.play(Indicate(Sn[5], color=GOOD, scale_factor=1.2))
        self.wait(0.8)

        res = VGroup(
            MathTex(r"a_{n}=S_{n}-S_{n-1}\quad(n\ge 2)", font_size=46, color=GOOD),
            MathTex(r"a_{1}=S_{1}", font_size=40, color=ACCENT),
        ).arrange(DOWN, buff=0.4).move_to(DOWN * 2.3)
        self.play(Write(res[0]), run_time=1.3)
        self.play(Write(res[1]), run_time=0.9)
        self.wait(0.8)

        warn = kr("n=1 은 따로 확인해야 한다 — Sₙ₋₁ 이 없기 때문", 27, BAD, BOLD)
        warn.move_to(DOWN * 3.35)
        self.play(FadeIn(warn, shift=UP * 0.2))
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 4차시 · 등비수열 — 같은 수를 (n-1)번 곱한다
# ──────────────────────────────────────────────────────────────
class S4GeoTerm(Scene):
    def construct(self):
        hd = head("등비수열 — 같은 수를 (n-1) 번 곱한다")
        self.add(hd)

        a, r = 1.0, 2.0
        ax = Axes(
            x_range=[0, 7, 1], y_range=[0, 36, 8],
            x_length=9.0, y_length=4.2,
            axis_config={"color": FAINT, "stroke_width": 2,
                         "tip_width": 0.14, "tip_height": 0.14},
        ).move_to(DOWN * 0.7)
        self.play(Create(ax), run_time=0.9)

        bars, labs = VGroup(), VGroup()
        for i in range(6):
            v = a * r ** i
            bar = Rectangle(width=0.62, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1],
                            stroke_color=ACCENT, stroke_width=2,
                            fill_color=ACCENT, fill_opacity=0.75)
            bar.move_to(ax.c2p(i + 1, v / 2))
            lb = MathTex(f"{int(v)}", font_size=26, color=INK).next_to(bar, UP, buff=0.12)
            bars.add(bar)
            labs.add(lb)

        self.play(FadeIn(bars[0], shift=UP * 0.2), FadeIn(labs[0]))
        for i in range(1, 6):
            arr = MathTex(r"\times r", font_size=26, color=WARM)
            arr.move_to((bars[i - 1].get_top() + bars[i].get_top()) / 2 + UP * 0.45)
            self.play(FadeIn(arr), FadeIn(bars[i], shift=UP * 0.2),
                      FadeIn(labs[i]), run_time=0.45)

        self.wait(0.7)
        gen = MathTex(r"a_{n}=ar^{\,n-1}", font_size=52, color=GOOD)
        gen.move_to(RIGHT * 4.3 + UP * 2.0)
        self.play(Write(gen), run_time=1.2)
        self.play(Create(box(gen, GOOD)))
        self.wait(1.4)

        wipe(self, hd)

        # 등비중항 — 비로 식을 세우므로 세 수가 모두 0 이 아니어야 한다
        self.play(FadeIn(kr("등비중항 — 가운데 항의 제곱이 양옆의 곱", 34, INK, BOLD)
                         .move_to(UP * 2.45)))
        cond = kr("단, a, b, c 는 모두 0 이 아니다", 24, MUTED).move_to(UP * 1.75)
        self.play(FadeIn(cond))
        three = VGroup(
            MathTex("a", font_size=48, color=ACCENT),
            MathTex("b", font_size=48, color=BAD),
            MathTex("c", font_size=48, color=ACCENT),
        ).arrange(RIGHT, buff=2.4).move_to(UP * 0.7)
        self.play(FadeIn(three, shift=UP * 0.2))

        g1 = MathTex(r"\frac{b}{a}", font_size=34, color=WARM).move_to(
            (three[0].get_center() + three[1].get_center()) / 2 + DOWN * 0.85)
        g2 = MathTex(r"\frac{c}{b}", font_size=34, color=WARM).move_to(
            (three[1].get_center() + three[2].get_center()) / 2 + DOWN * 0.85)
        eqg = MathTex("=", font_size=36, color=WARM).move_to(
            three[1].get_center() + DOWN * 0.85)
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(eqg))
        self.wait(0.7)

        res = MathTex(r"b^{2}=ac", font_size=52, color=GOOD).move_to(DOWN * 2.2)
        self.play(Write(res), run_time=1.0)
        self.play(Create(box(res, GOOD)))
        warn = kr("부호가 두 개 나오므로 답을 고를 때 조건을 확인할 것", 26, BAD)
        warn.move_to(DOWN * 3.3)
        self.play(FadeIn(warn, shift=UP * 0.2))
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 5차시 · 등비수열의 합 — r 배 해서 빼면 가운데가 다 사라진다
# ──────────────────────────────────────────────────────────────
class S5GeoSum(Scene):
    def construct(self):
        hd = head("등비수열의 합 — r 배 해서 빼면 가운데가 사라진다")
        self.add(hd)

        t1 = ["a", "ar", "ar^{2}", r"\cdots", "ar^{\,n-1}"]
        t2 = ["ar", "ar^{2}", r"\cdots", "ar^{\,n-1}", "ar^{\,n}"]

        row1 = VGroup(*[MathTex(t, font_size=38, color=ACCENT) for t in t1])
        row1.arrange(RIGHT, buff=0.9).move_to(UP * 1.75)
        row2 = VGroup(*[MathTex(t, font_size=38, color=WARM) for t in t2])
        row2.arrange(RIGHT, buff=0.9).move_to(UP * 0.5)
        # 한 칸 밀어 같은 항끼리 세로로 맞춘다
        row2.shift(RIGHT * (row1[1].get_center()[0] - row2[0].get_center()[0]))

        l1 = MathTex("S_{n}=", font_size=38, color=INK).next_to(row1, LEFT, buff=0.35)
        l2 = MathTex("rS_{n}=", font_size=38, color=INK).move_to(
            np.array([l1.get_center()[0], row2.get_center()[1], 0]))

        self.play(FadeIn(l1), Write(row1), run_time=1.5)
        self.wait(0.4)
        # 오른쪽 끝을 넘지 않도록 수식 줄 위쪽에 둔다
        note = kr("양변에 r 을 곱해 한 칸 민다", 26, MUTED).move_to(RIGHT * 3.0 + UP * 2.6)
        self.play(FadeIn(note, shift=LEFT * 0.2))
        self.play(FadeIn(l2), TransformFromCopy(row1, row2), run_time=1.7)
        self.wait(0.6)

        line = Line(LEFT * 6.3, RIGHT * 6.3, color=MUTED, stroke_width=2.5)
        line.move_to(DOWN * 0.25)
        minus = MathTex("-", font_size=44, color=MUTED).move_to(LEFT * 6.0 + UP * 0.1)
        self.play(Create(line), FadeIn(minus))

        # 겹치는 항이 전부 상쇄
        strike = VGroup()
        for i in range(1, 5):
            strike.add(Cross(row1[i], stroke_color=BAD, stroke_width=4).scale(0.75))
        for i in range(0, 4):
            strike.add(Cross(row2[i], stroke_color=BAD, stroke_width=4).scale(0.75))
        self.play(Create(strike), run_time=1.4)
        self.play(Indicate(row1[0], color=GOOD, scale_factor=1.3),
                  Indicate(row2[4], color=GOOD, scale_factor=1.3))
        self.wait(0.8)

        res = VGroup(
            MathTex(r"(1-r)S_{n}=a-ar^{\,n}=a(1-r^{\,n})",
                    font_size=42, color=INK),
            MathTex(r"S_{n}=\frac{a(1-r^{\,n})}{1-r}=\frac{a(r^{\,n}-1)}{r-1}"
                    r"\quad(r\neq 1)", font_size=44, color=GOOD),
            MathTex(r"S_{n}=na\quad(r=1)", font_size=38, color=BAD),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 2.35)
        self.play(Write(res[0]), run_time=1.2)
        self.play(Write(res[1]), run_time=1.6)
        self.play(Create(box(res[1], GOOD, buff=0.22)))
        self.wait(0.6)
        self.play(FadeIn(res[2], shift=UP * 0.2))
        self.wait(2.2)
