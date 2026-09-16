# -*- coding: utf-8 -*-
"""
2027 EBS 수능특강 수학Ⅰ — 강01 「지수와 로그」 공식 설명 시각화

차시별 장면 1개씩:
  S1NthRoot            1차시 · 거듭제곱근
  S2ExponentExtension  2차시 · 지수의 확장
  S3LogDefinition      3차시 · 로그의 정의와 성질
  S4BaseChange         4차시 · 로그의 밑의 변환
  S5CommonLog          5차시 · 상용로그

렌더: 00_공통/01_템플릿/build_manim.ps1
"""
import sys

sys.path.insert(0, r"D:\test1234\00_공통\01_템플릿")
from slide_theme import *   # noqa: F403,F401  (색·폰트·kr·head·box 는 공통 테마에서)


# ──────────────────────────────────────────────────────────────
# 1차시 · 거듭제곱근
#   xⁿ = a 의 실근 개수가 왜 n 의 홀짝에 달렸는지를 그래프로 보여 준다.
# ──────────────────────────────────────────────────────────────
class S1NthRoot(Scene):
    def construct(self):
        self.add(head("실수 a 의 n 제곱근"))

        eq = MathTex(r"x^{\,n}=a", font_size=56, color=INK).move_to(UP * 1.2)
        sub = kr("의 실근 = y=xⁿ 의 그래프와 직선 y=a 의 교점", 26, MUTED)
        sub.next_to(eq, DOWN, buff=0.25)
        self.play(Write(eq))
        self.play(FadeIn(sub, shift=UP * 0.2))
        self.wait(0.6)
        self.play(FadeOut(sub),
                  eq.animate.scale(0.6).move_to(LEFT * 5.9 + UP * 1.75))

        # y_range 를 벗어나면 곡선이 축 밖으로 삐져나가므로,
        # |y| <= YMAX 가 되는 x 범위까지만 그린다.
        YMAX = 2.5

        def panel(fn, n, pos):
            ax = Axes(
                x_range=[-1.6, 1.6, 1], y_range=[-YMAX, YMAX, 1],
                x_length=4.0, y_length=4.0,
                axis_config={"color": MUTED, "stroke_width": 2,
                             "tip_width": 0.16, "tip_height": 0.16},
            ).move_to(pos)
            xm = YMAX ** (1.0 / n)          # fn(xm) = YMAX
            curve = ax.plot(fn, x_range=[-xm, xm], color=ACCENT, stroke_width=5)
            lbl = MathTex(r"y=x^{%d}" % n, font_size=34, color=ACCENT)
            lbl.next_to(ax, UP, buff=0.14)
            return ax, curve, lbl

        axL, curveL, lblL = panel(lambda x: x ** 3, 3, LEFT * 3.3 + DOWN * 0.75)
        axR, curveR, lblR = panel(lambda x: x ** 4, 4, RIGHT * 3.3 + DOWN * 0.75)

        capL = kr("n 이 홀수", 30, INK, BOLD).next_to(axL, DOWN, buff=0.22)
        capR = kr("n 이 짝수", 30, INK, BOLD).next_to(axR, DOWN, buff=0.22)

        self.play(Create(axL), Create(axR), run_time=1.2)
        self.play(Create(curveL), Create(curveR), run_time=1.4)
        self.play(FadeIn(lblL), FadeIn(lblR), FadeIn(capL), FadeIn(capR))
        self.wait(0.4)

        # 직선 y = a 를 위에서 아래로 훑으며 교점 개수를 관찰한다
        a = ValueTracker(2.0)

        def roots_odd(v):
            return [np.cbrt(v)]

        def roots_even(v):
            if v > 1e-6:
                r = v ** 0.25
                return [-r, r]
            if v < -1e-6:
                return []
            return [0.0]

        def hline(ax):
            return always_redraw(lambda: ax.plot(
                lambda x: a.get_value(), x_range=[-1.7, 1.7],
                color=WARM, stroke_width=4))

        def dots(ax, roots_fn):
            return always_redraw(lambda: VGroup(*[
                Dot(ax.c2p(r, a.get_value()), color=BAD, radius=0.09)
                for r in roots_fn(a.get_value())
            ]))

        lineL, lineR = hline(axL), hline(axR)
        dotL, dotR = dots(axL, roots_odd), dots(axR, roots_even)

        aval = always_redraw(lambda: VGroup(
            MathTex("a=", font_size=34, color=WARM),
            DecimalNumber(a.get_value(), num_decimal_places=1,
                          font_size=34, color=WARM),
        ).arrange(RIGHT, buff=0.1).move_to(RIGHT * 5.9 + UP * 1.75))

        self.play(Create(lineL), Create(lineR), FadeIn(aval))
        self.add(dotL, dotR)
        self.wait(0.5)

        cntL = always_redraw(lambda: kr(
            "실근 %d개" % len(roots_odd(a.get_value())), 28, GOOD, BOLD
        ).next_to(capL, DOWN, buff=0.15))
        cntR = always_redraw(lambda: kr(
            "실근 %d개" % len(roots_even(a.get_value())), 28,
            GOOD if roots_even(a.get_value()) else BAD, BOLD
        ).next_to(capR, DOWN, buff=0.15))
        self.play(FadeIn(cntL), FadeIn(cntR))

        self.play(a.animate.set_value(0.0), run_time=2.2, rate_func=linear)
        self.wait(0.7)
        self.play(a.animate.set_value(-2.0), run_time=2.2, rate_func=linear)
        self.wait(1.0)

        # 결론
        concl = VGroup(
            kr("n 홀수 → a 의 부호와 무관하게 실근 1개", 27, INK),
            kr("n 짝수 → a ≥ 0 일 때만 실근이 존재", 27, INK),
        ).arrange(DOWN, buff=0.18)
        box = RoundedRectangle(
            width=concl.width + 1.2, height=concl.height + 0.8,
            corner_radius=0.18, stroke_color=GOOD, stroke_width=3,
            fill_color=GOOD_SOFT, fill_opacity=1)
        grp = VGroup(box, concl)
        concl.move_to(box.get_center())
        grp.move_to(ORIGIN + UP * 0.1)

        # 결론 박스가 그래프를 덮지 않도록, 그래프를 먼저 모두 걷어낸다.
        self.play(FadeOut(lineL, lineR, dotL, dotR, aval, cntL, cntR,
                          axL, axR, curveL, curveR, lblL, lblR,
                          capL, capR, eq),
                  run_time=1.0)
        self.play(FadeIn(box), run_time=0.6)
        self.play(Write(concl), run_time=1.4)
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 2차시 · 지수의 확장
#   지수법칙을 그대로 유지하려면 a⁰, a⁻ⁿ, a^(m/n) 의 정의는 하나뿐임을 보인다.
# ──────────────────────────────────────────────────────────────
class S2ExponentExtension(Scene):
    def construct(self):
        self.add(head("지수의 확장 — 법칙을 지키려면 정의는 하나뿐"))

        law = MathTex(r"a^{m}\cdot a^{n}=a^{m+n}", font_size=60, color=ACCENT)
        law.move_to(UP * 1.5)
        note = kr("자연수 지수에서 성립하던 이 법칙을 그대로 유지하자", 27, MUTED)
        note.next_to(law, DOWN, buff=0.3)
        self.play(Write(law))
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(1.2)
        self.play(FadeOut(note), law.animate.scale(0.62).to_edge(UP, buff=1.4))

        def step(cond_kr, chain, result, y):
            cond = kr(cond_kr, 26, WARM, BOLD)
            mid = MathTex(chain, font_size=38, color=INK)
            arrow = MathTex(r"\Longrightarrow", font_size=36, color=MUTED)
            res = MathTex(result, font_size=42, color=GOOD)
            g = VGroup(cond, mid, arrow, res).arrange(RIGHT, buff=0.4)
            g.scale_to_fit_width(min(12.2, g.width))
            g.move_to(UP * y)
            return g

        s1 = step("m = 0", r"a^{0}\cdot a^{n}=a^{0+n}=a^{n}", r"a^{0}=1", 0.55)
        s2 = step("m = -n", r"a^{-n}\cdot a^{n}=a^{0}=1",
                  r"a^{-n}=\frac{1}{a^{n}}", -0.85)
        s3 = step("유리수 m/n", r"\left(a^{\frac{m}{n}}\right)^{n}=a^{m}",
                  r"a^{\frac{m}{n}}=\sqrt[n]{a^{m}}", -2.45)

        rows = VGroup()
        for s in (s1, s2, s3):
            self.play(FadeIn(s[0], shift=RIGHT * 0.3), run_time=0.5)
            self.play(Write(s[1]), run_time=1.1)
            self.play(FadeIn(s[2]), Write(s[3]), run_time=0.9)
            self.play(Indicate(s[3], color=GOOD, scale_factor=1.15), run_time=0.7)
            self.wait(0.4)
            rows.add(s)

        self.wait(1.2)
        self.play(FadeOut(rows), FadeOut(law))

        # 무리수 지수 — 유리수 지수로 조여 들어간다
        title2 = kr("지수가 무리수이면? 유리수로 조여 들어간다", 32, INK, BOLD)
        title2.move_to(UP * 2.15)
        self.play(FadeIn(title2))

        # 값들이 한 점으로 몰리므로 수직선 위에 라벨을 붙이면 서로 겹친다.
        # 값 표는 왼쪽에 세로로 쌓고, 수직선에는 점만 찍는다.
        seq = [
            (1.4,    r"2^{1.4}",    r"2.6390"),
            (1.41,   r"2^{1.41}",   r"2.6574"),
            (1.414,  r"2^{1.414}",  r"2.6647"),
            (1.4142, r"2^{1.4142}", r"2.66511"),
        ]
        rows = VGroup(*[
            VGroup(
                MathTex(tex, font_size=34, color=WARM),
                MathTex("=", font_size=34, color=MUTED),
                MathTex(val, font_size=34, color=INK),
            ).arrange(RIGHT, buff=0.25)
            for _, tex, val in seq
        ]).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(LEFT * 4.0 + UP * 0.35)

        # include_numbers 는 눈금 값의 부동소수 오차 탓에 라벨이 누락되므로
        # 눈금 숫자는 직접 붙인다.
        nl = NumberLine(
            x_range=[2.63, 2.67, 0.01], length=5.6,
            color=MUTED).move_to(RIGHT * 3.6 + UP * 0.35)
        nl_labels = VGroup(*[
            MathTex(f"{t:.2f}", font_size=26, color=MUTED)
            .next_to(nl.n2p(t), DOWN, buff=0.22)
            for t in (2.63, 2.65, 2.67)
        ])
        self.play(Create(nl), FadeIn(nl_labels), run_time=0.9)

        for (e, _, _), row in zip(seq, rows):
            d = Dot(nl.n2p(2 ** e), color=WARM, radius=0.085)
            self.play(Write(row), run_time=0.6)
            self.play(FadeIn(d, scale=0.4), run_time=0.35)

        v = 2 ** (2 ** 0.5)
        dt = Dot(nl.n2p(v), color=GOOD, radius=0.11)
        lt = VGroup(
            MathTex(r"2^{\sqrt{2}}", font_size=40, color=GOOD),
            MathTex("=", font_size=40, color=MUTED),
            MathTex(r"2.665144\cdots", font_size=40, color=GOOD),
        ).arrange(RIGHT, buff=0.25).move_to(DOWN * 2.5)
        self.play(FadeIn(dt, scale=0.3), Write(lt), run_time=1.1)
        self.play(Flash(dt, color=GOOD, line_length=0.35))
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 3차시 · 로그의 정의와 성질
# ──────────────────────────────────────────────────────────────
class S3LogDefinition(Scene):
    def construct(self):
        self.add(head("로그의 정의 — 지수를 되묻는 기호"))

        left = MathTex(r"a^{x}=N", font_size=60, color=ACCENT)
        left.move_to(LEFT * 3.4 + UP * 1.4)
        arrow = MathTex(r"\Longleftrightarrow", font_size=50, color=MUTED)
        arrow.move_to(UP * 1.4)
        right = MathTex(r"x=\log_{a}N", font_size=60, color=WARM)
        right.move_to(RIGHT * 3.4 + UP * 1.4)

        self.play(Write(left))
        self.play(FadeIn(arrow), run_time=0.5)
        self.play(TransformFromCopy(left, right), run_time=1.4)
        self.wait(0.6)

        q = kr("a 를 몇 번 곱해야 N 이 되는가 — 그 답이 로그", 28, MUTED)
        q.move_to(UP * 0.2)
        self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(1.4)
        self.play(FadeOut(q))

        b_lbl = kr("밑", 30, ACCENT, BOLD).move_to(RIGHT * 2.9 + DOWN * 0.45)
        a_lbl = kr("진수", 30, GOOD, BOLD).move_to(RIGHT * 4.6 + DOWN * 0.45)
        b_arr = Arrow(b_lbl.get_top(), right.get_bottom() + LEFT * 0.35,
                      buff=0.12, color=ACCENT, stroke_width=3,
                      max_tip_length_to_length_ratio=0.3)
        a_arr = Arrow(a_lbl.get_top(), right.get_bottom() + RIGHT * 0.7,
                      buff=0.12, color=GOOD, stroke_width=3,
                      max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(b_arr), FadeIn(b_lbl),
                  GrowArrow(a_arr), FadeIn(a_lbl))
        self.wait(0.8)

        cond = VGroup(
            MathTex(r"a>0,\quad a\neq 1,\quad N>0", font_size=40, color=BAD),
            kr("정의되기 위한 조건 — 유제와 기출에서 매번 물어본다", 24, MUTED),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 2.4)
        self.play(FadeIn(cond, shift=UP * 0.2))
        self.wait(1.8)

        self.play(FadeOut(VGroup(left, arrow, right, b_lbl, a_lbl,
                                 b_arr, a_arr, cond)))

        # 로그의 성질은 지수법칙을 뒤집은 것
        t2 = kr("로그의 성질은 지수법칙을 뒤집은 것", 34, INK, BOLD).move_to(UP * 2.3)
        self.play(FadeIn(t2))
        setup = MathTex(
            r"\log_{a}M=m,\ \log_{a}N=n \;\Longrightarrow\; a^{m}=M,\ a^{n}=N",
            font_size=36, color=MUTED).move_to(UP * 1.35)
        self.play(Write(setup), run_time=1.6)
        self.wait(0.5)

        props = [
            (r"MN=a^{m}a^{n}=a^{m+n}",
             r"\log_{a}MN=\log_{a}M+\log_{a}N"),
            (r"\frac{M}{N}=a^{m}\div a^{n}=a^{m-n}",
             r"\log_{a}\frac{M}{N}=\log_{a}M-\log_{a}N"),
            (r"M^{r}=(a^{m})^{r}=a^{mr}",
             r"\log_{a}M^{r}=r\log_{a}M"),
        ]
        for i, (lhs, rhs) in enumerate(props):
            y = -0.1 - i * 1.3
            L = MathTex(lhs, font_size=32, color=INK).move_to(LEFT * 3.6 + UP * y)
            A = MathTex(r"\Longrightarrow", font_size=28, color=MUTED).move_to(UP * y)
            R = MathTex(rhs, font_size=32, color=GOOD).move_to(RIGHT * 3.6 + UP * y)
            self.play(Write(L), run_time=0.8)
            self.play(FadeIn(A), TransformFromCopy(L, R), run_time=1.0)
            self.wait(0.35)
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 4차시 · 로그의 밑의 변환
# ──────────────────────────────────────────────────────────────
class S4BaseChange(Scene):
    def construct(self):
        self.add(head("로그의 밑의 변환 — 밑을 통일하는 열쇠"))

        goal = MathTex(r"\log_{a}b=\frac{\log_{c}b}{\log_{c}a}",
                       font_size=58, color=ACCENT).move_to(UP * 1.9)
        self.play(Write(goal))
        self.wait(0.8)
        why = kr("밑이 제각각이면 계산이 안 된다 → 하나의 밑 c 로 갈아끼운다", 26, MUTED)
        why.next_to(goal, DOWN, buff=0.35)
        self.play(FadeIn(why, shift=UP * 0.2))
        self.wait(1.4)
        self.play(FadeOut(why),
                  goal.animate.scale(0.5).to_corner(UR).shift(DOWN * 0.95))

        steps = [
            (r"\log_{a}b=x,\quad \log_{c}a=y", "두 로그를 문자로 놓는다"),
            (r"a^{x}=b,\qquad c^{\,y}=a", "로그의 정의로 지수식으로 되돌린다"),
            (r"b=a^{x}=\left(c^{\,y}\right)^{x}=c^{\,xy}", "a 를 대입해 밑을 c 로 통일"),
            (r"\log_{c}b=xy=\log_{a}b\cdot\log_{c}a", "다시 로그로 — 핵심 관계식"),
        ]
        shown = VGroup()
        for i, (tex, desc) in enumerate(steps):
            y = 1.2 - i * 1.15
            m = MathTex(tex, font_size=38, color=INK).move_to(LEFT * 2.6 + UP * y)
            d = kr(desc, 22, MUTED).move_to(RIGHT * 3.3 + UP * y)
            self.play(Write(m), run_time=1.0)
            self.play(FadeIn(d, shift=LEFT * 0.2), run_time=0.5)
            shown.add(m, d)
            self.wait(0.45)

        self.wait(0.8)
        div = kr("a ≠ 1 이므로 밑변환의 분모는 0 이 아니다 → 양변을 나눌 수 있다",
                 26, WARM, BOLD).move_to(DOWN * 2.75)
        self.play(FadeIn(div, shift=UP * 0.2))
        self.wait(1.2)

        final = MathTex(r"\log_{a}b=\frac{\log_{c}b}{\log_{c}a}",
                        font_size=62, color=GOOD).move_to(UP * 0.55)
        box = SurroundingRectangle(final, color=GOOD, buff=0.35,
                                   corner_radius=0.15, stroke_width=3)
        self.play(FadeOut(shown), FadeOut(div), run_time=0.8)
        self.play(Write(final), run_time=1.2)
        self.play(Create(box))
        self.wait(1.0)

        uses = VGroup(
            MathTex(r"\log_{a}b=\frac{1}{\log_{b}a}", font_size=32, color=INK),
            MathTex(r"\log_{a}b\cdot\log_{b}c=\log_{a}c", font_size=32, color=INK),
            MathTex(r"\log_{a^{m}}b^{\,n}=\frac{n}{m}\log_{a}b", font_size=32, color=INK),
            MathTex(r"a^{\log_{b}c}=c^{\log_{b}a}", font_size=32, color=INK),
        ).arrange(RIGHT, buff=0.65).move_to(DOWN * 2.3)
        uses.scale_to_fit_width(min(12.6, uses.width))
        self.play(LaggedStartMap(FadeIn, uses, shift=UP * 0.25, lag_ratio=0.25),
                  run_time=1.8)
        self.wait(2.4)


# ──────────────────────────────────────────────────────────────
# 5차시 · 상용로그 — 지표와 가수, 그리고 자릿수
# ──────────────────────────────────────────────────────────────
class S5CommonLog(Scene):
    def construct(self):
        self.add(head("상용로그 — 큰 수를 a × 10ⁿ 으로 쪼갠다"))

        d = MathTex(r"\log N=\log_{10}N", font_size=50, color=ACCENT).move_to(UP * 2.0)
        self.play(Write(d))
        self.wait(0.6)

        # MathTex 안에는 한글을 넣지 않는다.
        # (LaTeX 가 비 ASCII 를 만나면 로그 인코딩이 깨져 렌더가 실패한다)
        form = MathTex(r"N=a\times 10^{n}\quad(1\le a<10)",
                       font_size=42, color=INK).move_to(UP * 0.9)
        form_note = kr("n 은 정수", 26, MUTED).next_to(form, RIGHT, buff=0.45)
        self.play(Write(form), run_time=1.2)
        self.play(FadeIn(form_note), run_time=0.4)
        self.wait(0.5)

        expand = MathTex(r"\log N", r"=", r"n", r"+", r"\log a",
                         font_size=50, color=INK).move_to(DOWN * 0.35)
        expand[2].set_color(WARM)
        expand[4].set_color(GOOD)
        self.play(TransformFromCopy(form, expand), run_time=1.5)
        self.wait(0.4)

        # 교재(p.12)는 '지표·가수'라는 용어를 쓰지 않는다. 이 교육과정에서
        # 빠진 용어이므로 '정수 부분 / 소수 부분'으로만 부른다.
        t1 = kr("정수 부분", 28, WARM, BOLD)
        t1.move_to(expand[2].get_center() + DOWN * 1.25 + LEFT * 0.7)
        t2 = kr("소수 부분 — 표에서 읽는 값", 28, GOOD, BOLD)
        t2.move_to(expand[4].get_center() + DOWN * 1.25 + RIGHT * 1.3)
        a1 = Arrow(t1.get_top(), expand[2].get_bottom(), buff=0.12,
                   color=WARM, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        a2 = Arrow(t2.get_top(), expand[4].get_bottom(), buff=0.12,
                   color=GOOD, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(a1), FadeIn(t1), GrowArrow(a2), FadeIn(t2))
        self.wait(1.6)

        rule = MathTex(r"1\le a<10\ \Longrightarrow\ 0\le\log a<1",
                       font_size=40, color=INK).move_to(DOWN * 2.85)
        self.play(Write(rule), run_time=1.1)
        self.wait(1.6)

        self.play(FadeOut(VGroup(d, form, form_note, expand, t1, t2, a1, a2, rule)))

        # 예시 — 교재 p.12 ⑶ '상용로그의 활용' : 2³⁰ 의 어림한 값
        ex_t = kr("예)  2³⁰ 은 대략 얼마인가?", 36, INK, BOLD).move_to(UP * 2.5)
        self.play(FadeIn(ex_t))

        e1 = MathTex(r"\log 2^{30}=30\log 2=30\times 0.3010=9.03",
                     font_size=40, color=INK).move_to(UP * 1.35)
        e2 = MathTex(r"9.03", r"=", r"9", r"+", r"0.03",
                     font_size=44, color=INK).move_to(UP * 0.25)
        e2[2].set_color(WARM)
        e2[4].set_color(GOOD)
        self.play(Write(e1), run_time=1.4)
        self.wait(0.4)
        self.play(Write(e2), run_time=1.1)

        # 9 와 0.03 이 가까이 붙어 있어 라벨을 그대로 두면 겹친다. 좌우로 벌린다.
        l1 = kr("정수 부분", 24, WARM, BOLD).next_to(e2[2], DOWN, buff=0.42)
        l1.shift(LEFT * 0.95)
        l2 = kr("소수 부분", 24, GOOD, BOLD).next_to(e2[4], DOWN, buff=0.42)
        l2.shift(RIGHT * 0.95)
        self.play(FadeIn(l1, shift=UP * 0.15), FadeIn(l2, shift=UP * 0.15))
        self.wait(0.7)

        # 표를 거꾸로 되짚어 0.03 에 해당하는 수를 찾는다
        back = kr("표에서 되짚으면  log 1.07 ≈ 0.03", 28, GOOD)
        back.move_to(DOWN * 1.35)
        self.play(FadeIn(back, shift=UP * 0.2), run_time=0.8)

        e3 = MathTex(r"9+\log 1.07=\log\!\left(1.07\times 10^{9}\right)",
                     font_size=40, color=INK).move_to(DOWN * 2.25)
        self.play(Write(e3), run_time=1.3)

        tail = MathTex(r"\therefore\ 2^{30}\approx 1.07\times 10^{9}",
                       font_size=44, color=GOOD).move_to(DOWN * 3.2)
        self.play(Write(tail), run_time=1.0)
        self.play(Create(box(tail, GOOD, buff=0.25)))
        self.wait(2.4)
