# -*- coding: utf-8 -*-
"""
2027 EBS 수능특강 수학Ⅰ — 강06 「수열의 합과 수학적 귀납법」 시각화

  S1Sigma        1차시 · 합의 기호 Σ 와 그 성질
  S2PowerSum     2차시 · 자연수의 거듭제곱의 합
  S3Telescoping  3차시 · 분수 꼴 수열의 합 (망원급수)
  S4Recursive    4차시 · 수열의 귀납적 정의
  S5RecurTypes   5차시 · 귀납적으로 정의된 여러 가지 수열
  S6Induction    6차시 · 수학적 귀납법

렌더: 00_공통/01_템플릿/build_manim.ps1
"""
import sys

sys.path.insert(0, r"D:\test1234\00_공통\01_템플릿")
from slide_theme import *   # noqa: F403,F401


# ──────────────────────────────────────────────────────────────
# 1차시 · Σ 는 '더하라'는 명령어일 뿐
# ──────────────────────────────────────────────────────────────
class S1Sigma(Scene):
    def construct(self):
        hd = head("합의 기호 Σ — 더하라는 명령어일 뿐")
        self.add(hd)

        sig = MathTex(r"\sum_{k=1}^{n}a_{k}", font_size=64, color=ACCENT)
        sig.move_to(LEFT * 3.8 + UP * 1.4)
        eq = MathTex("=", font_size=48, color=MUTED).move_to(LEFT * 1.6 + UP * 1.4)
        expand = MathTex(r"a_{1}+a_{2}+a_{3}+\cdots+a_{n}",
                         font_size=44, color=INK).move_to(RIGHT * 2.2 + UP * 1.4)
        self.play(Write(sig), run_time=1.0)
        self.play(FadeIn(eq), TransformFromCopy(sig, expand), run_time=1.4)
        self.wait(0.6)

        # k 가 1부터 n 까지 돈다는 것을 강조
        k_note = kr("k 는 1 부터 n 까지 도는 '세는 문자'", 26, MUTED)
        k_note.next_to(sig, DOWN, buff=0.5)
        self.play(FadeIn(k_note, shift=UP * 0.2))
        self.wait(1.0)
        free = MathTex(r"\sum_{k=1}^{n}a_{k}=\sum_{i=1}^{n}a_{i}=\sum_{j=1}^{n}a_{j}",
                       font_size=36, color=GOOD).move_to(DOWN * 0.15)
        self.play(Write(free), run_time=1.3)
        self.wait(1.2)

        self.play(FadeOut(VGroup(sig, eq, expand, k_note, free)), run_time=0.7)

        # 성질 — 되는 것과 안 되는 것
        ok_t = kr("되는 것", 30, GOOD, BOLD).move_to(LEFT * 3.6 + UP * 2.2)
        no_t = kr("안 되는 것", 30, BAD, BOLD).move_to(RIGHT * 3.6 + UP * 2.2)
        self.play(FadeIn(ok_t), FadeIn(no_t))

        ok = VGroup(
            MathTex(r"\sum(a_{k}+b_{k})=\sum a_{k}+\sum b_{k}",
                    font_size=32, color=INK),
            MathTex(r"\sum c\,a_{k}=c\sum a_{k}", font_size=32, color=INK),
            MathTex(r"\sum_{k=1}^{n}c=cn", font_size=32, color=INK),
        ).arrange(DOWN, buff=0.55).move_to(LEFT * 3.6 + DOWN * 0.3)

        no = VGroup(
            MathTex(r"\sum a_{k}b_{k}\neq\left(\sum a_{k}\right)"
                    r"\left(\sum b_{k}\right)", font_size=30, color=INK),
            MathTex(r"\sum\frac{a_{k}}{b_{k}}\neq"
                    r"\frac{\sum a_{k}}{\sum b_{k}}", font_size=30, color=INK),
        ).arrange(DOWN, buff=0.7).move_to(RIGHT * 3.6 + DOWN * 0.15)

        for m in ok:
            self.play(Write(m), run_time=0.8)
        self.wait(0.4)
        for m in no:
            self.play(Write(m), run_time=0.8)

        self.wait(0.6)
        tip = kr("Σ 는 덧셈에만 분배된다 — 곱셈·나눗셈에는 분배되지 않는다",
                 28, BAD, BOLD).move_to(DOWN * 3.2)
        self.play(FadeIn(tip, shift=UP * 0.2))
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 2차시 · 1부터 n까지의 합 — 두 벌을 붙이면 직사각형
# ──────────────────────────────────────────────────────────────
class S2PowerSum(Scene):
    def construct(self):
        hd = head("자연수의 합 — 두 벌을 붙이면 직사각형")
        self.add(hd)

        n = 6
        u = 0.42
        origin = LEFT * 4.6 + DOWN * 2.0

        def block(i, j, color, op=0.85):
            return Square(side_length=u, stroke_color="#ffffff", stroke_width=1.5,
                          fill_color=color, fill_opacity=op).move_to(
                origin + RIGHT * (i * u + u / 2) + UP * (j * u + u / 2))

        stair = VGroup(*[block(i, j, ACCENT)
                         for i in range(n) for j in range(i + 1)])
        self.play(LaggedStartMap(FadeIn, stair, scale=0.6, lag_ratio=0.02),
                  run_time=1.6)
        lbl = MathTex(r"1+2+3+\cdots+n", font_size=38, color=ACCENT)
        lbl.move_to(RIGHT * 3.3 + UP * 1.6)
        self.play(FadeIn(lbl))
        self.wait(0.6)

        # 같은 계단을 뒤집어 끼워 넣는다.
        # 회전 대신 '빈 자리'를 직접 채운다 — 열 i 는 (i+1)칸이 차 있으므로
        # 그 위 (n-i)칸을 채우면 모든 열이 정확히 (n+1)칸이 된다.
        flip = VGroup(*[block(i, j, WARM)
                        for i in range(n) for j in range(i + 1, n + 1)])
        self.play(FadeIn(flip, shift=LEFT * 0.4), run_time=1.4)
        self.wait(0.5)

        brace_b = Brace(VGroup(stair, flip), DOWN, color=MUTED)
        brace_r = Brace(VGroup(stair, flip), RIGHT, color=MUTED)
        bl = MathTex("n", font_size=32, color=MUTED).next_to(brace_b, DOWN, buff=0.1)
        br = MathTex("n+1", font_size=32, color=MUTED).next_to(brace_r, RIGHT, buff=0.1)
        self.play(GrowFromCenter(brace_b), GrowFromCenter(brace_r),
                  FadeIn(bl), FadeIn(br))
        self.wait(0.8)

        res = VGroup(
            MathTex(r"2\sum_{k=1}^{n}k=n(n+1)", font_size=40, color=INK),
            MathTex(r"\sum_{k=1}^{n}k=\frac{n(n+1)}{2}", font_size=46, color=GOOD),
        ).arrange(DOWN, buff=0.45).move_to(RIGHT * 3.3 + DOWN * 0.5)
        self.play(Write(res[0]), run_time=1.0)
        self.play(Write(res[1]), run_time=1.2)
        self.play(Create(box(res[1], GOOD)))
        self.wait(1.4)

        wipe(self, hd)

        rest = VGroup(
            MathTex(r"\sum_{k=1}^{n}k^{2}=\frac{n(n+1)(2n+1)}{6}",
                    font_size=46, color=ACCENT),
            MathTex(r"\sum_{k=1}^{n}k^{3}=\left\{\frac{n(n+1)}{2}\right\}^{2}",
                    font_size=46, color=WARM),
        ).arrange(DOWN, buff=0.9).move_to(UP * 0.4)
        self.play(Write(rest[0]), run_time=1.4)
        self.play(Write(rest[1]), run_time=1.4)
        self.wait(0.6)
        tip = kr("세제곱의 합은 '첫째항까지의 합'의 제곱 — 외우기 쉬운 짝",
                 28, MUTED).move_to(DOWN * 2.3)
        self.play(FadeIn(tip, shift=UP * 0.2))
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 3차시 · 망원급수 — 가운데가 전부 지워진다
# ──────────────────────────────────────────────────────────────
class S3Telescoping(Scene):
    def construct(self):
        hd = head("분수 꼴의 합 — 쪼개면 가운데가 전부 지워진다")
        self.add(hd)

        split = MathTex(r"\frac{1}{k(k+1)}", r"=",
                        r"\frac{1}{k}-\frac{1}{k+1}",
                        font_size=48, color=INK).move_to(UP * 2.15)
        split[2].set_color(GOOD)
        self.play(Write(split[0]), run_time=0.8)
        self.play(FadeIn(split[1]), TransformFromCopy(split[0], split[2]),
                  run_time=1.3)
        self.wait(0.8)

        terms = VGroup(
            MathTex(r"\left(\tfrac{1}{1}-\tfrac{1}{2}\right)", font_size=36),
            MathTex("+", font_size=32, color=MUTED),
            MathTex(r"\left(\tfrac{1}{2}-\tfrac{1}{3}\right)", font_size=36),
            MathTex("+", font_size=32, color=MUTED),
            MathTex(r"\left(\tfrac{1}{3}-\tfrac{1}{4}\right)", font_size=36),
            MathTex(r"+\cdots+", font_size=32, color=MUTED),
            MathTex(r"\left(\tfrac{1}{n}-\tfrac{1}{n+1}\right)", font_size=36),
        ).arrange(RIGHT, buff=0.28).move_to(UP * 0.5)
        terms.set_color(INK)
        self.play(Write(terms), run_time=2.0)
        self.wait(0.7)

        # 이웃한 항끼리 상쇄
        pairs = [(0, 2), (2, 4)]
        arcs = VGroup()
        for i, j in pairs:
            a = terms[i].get_bottom() + DOWN * 0.12
            b = terms[j].get_bottom() + DOWN * 0.12
            arcs.add(ArcBetweenPoints(a, b, angle=-1.1, color=BAD, stroke_width=3))
        self.play(Create(arcs), run_time=1.2)
        self.play(*[Indicate(t, color=BAD, scale_factor=1.1)
                    for t in (terms[0], terms[2], terms[4])], run_time=1.0)
        self.wait(0.6)

        survive = kr("맨 앞과 맨 뒤만 살아남는다", 30, GOOD, BOLD)
        survive.move_to(DOWN * 1.35)
        self.play(FadeIn(survive, shift=UP * 0.2))

        res = MathTex(r"\sum_{k=1}^{n}\frac{1}{k(k+1)}=1-\frac{1}{n+1}"
                      r"=\frac{n}{n+1}", font_size=46, color=GOOD)
        res.move_to(DOWN * 2.6)
        self.play(Write(res), run_time=1.6)
        self.play(Create(box(res, GOOD)))
        self.wait(1.6)

        self.play(FadeOut(VGroup(split, terms, arcs, survive, res)), run_time=0.8)
        rule = VGroup(
            kr("일반형 — 분모 차이로 나눈다", 30, INK, BOLD),
            MathTex(r"\frac{1}{AB}=\frac{1}{B-A}\left(\frac{1}{A}-\frac{1}{B}\right)"
                    r"\quad(A\neq B)", font_size=44, color=ACCENT),
            kr("분모가 무리식이면 유리화하면 같은 꼴이 된다", 27, MUTED),
            MathTex(r"\frac{1}{\sqrt{k+1}+\sqrt{k}}=\sqrt{k+1}-\sqrt{k}",
                    font_size=40, color=WARM),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.1)
        for m in rule:
            self.play(FadeIn(m, shift=UP * 0.2) if isinstance(m, Text)
                      else Write(m), run_time=1.0)
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 4차시 · 귀납적 정의 — 출발점 + 다음 항 만드는 법
# ──────────────────────────────────────────────────────────────
class S4Recursive(Scene):
    def construct(self):
        hd = head("귀납적 정의 — 출발점과 '다음 만드는 법'")
        self.add(hd)

        two = VGroup(
            VGroup(kr("첫째항", 26, MUTED),
                   MathTex("a_{1}=2", font_size=40, color=ACCENT)
                   ).arrange(DOWN, buff=0.18),
            VGroup(kr("다음 항 만드는 법", 26, MUTED),
                   MathTex("a_{n+1}=a_{n}+3", font_size=40, color=WARM)
                   ).arrange(DOWN, buff=0.18),
        ).arrange(RIGHT, buff=2.4).move_to(UP * 2.15)
        self.play(FadeIn(two[0], shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(two[1], shift=UP * 0.2), run_time=0.7)
        self.wait(0.6)

        # 실제로 굴려 보기
        vals = [2, 5, 8, 11, 14, 17]
        chain = VGroup()
        for i, v in enumerate(vals):
            c = VGroup(
                Circle(radius=0.46, color=ACCENT, stroke_width=3,
                       fill_color=ACCENT_SOFT, fill_opacity=1),
                MathTex(str(v), font_size=32, color=INK),
            )
            chain.add(c)
        chain.arrange(RIGHT, buff=1.05).move_to(UP * 0.15)

        self.play(FadeIn(chain[0], scale=0.5))
        for i in range(1, len(vals)):
            arr = Arrow(chain[i - 1].get_right(), chain[i].get_left(),
                        color=WARM, stroke_width=4, buff=0.08,
                        max_tip_length_to_length_ratio=0.3)
            lb = MathTex("+3", font_size=26, color=WARM).next_to(arr, UP, buff=0.06)
            self.play(GrowArrow(arr), FadeIn(lb), run_time=0.3)
            self.play(FadeIn(chain[i], scale=0.5), run_time=0.3)

        self.wait(0.8)
        see = kr("이웃한 항의 차가 일정 → 등차수열", 30, GOOD, BOLD)
        see.move_to(DOWN * 1.5)
        self.play(FadeIn(see, shift=UP * 0.2))

        gen = MathTex(r"a_{n}=2+(n-1)\cdot 3=3n-1",
                      font_size=44, color=GOOD).move_to(DOWN * 2.5)
        self.play(Write(gen), run_time=1.2)
        self.play(Create(box(gen, GOOD)))
        self.wait(1.4)

        wipe(self, hd, run_time=0.7)
        table = VGroup(
            VGroup(MathTex(r"a_{n+1}=a_{n}+d", font_size=36, color=ACCENT),
                   kr("등차수열", 28, INK)).arrange(RIGHT, buff=1.0),
            VGroup(MathTex(r"a_{n+1}=r\,a_{n}", font_size=36, color=ACCENT),
                   kr("등비수열", 28, INK)).arrange(RIGHT, buff=1.0),
            VGroup(MathTex(r"2a_{n+1}=a_{n}+a_{n+2}", font_size=36, color=WARM),
                   kr("등차수열 (등차중항)", 28, INK)).arrange(RIGHT, buff=1.0),
            VGroup(MathTex(r"a_{n+1}^{\,2}=a_{n}a_{n+2}", font_size=36, color=WARM),
                   kr("등비수열 (등비중항)", 28, INK)).arrange(RIGHT, buff=1.0),
        ).arrange(DOWN, buff=0.48, aligned_edge=LEFT).move_to(DOWN * 0.45)
        self.play(LaggedStartMap(FadeIn, table, shift=UP * 0.2, lag_ratio=0.25),
                  run_time=2.0)
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 5차시 · 여러 가지 수열 — 막히면 그냥 대입해 본다
# ──────────────────────────────────────────────────────────────
class S5RecurTypes(Scene):
    def construct(self):
        hd = head("귀납적 수열 — 막히면 직접 대입해 굴려 본다")
        self.add(hd)

        prob = VGroup(
            MathTex(r"a_{1}=12,\qquad a_{n+1}=\frac{a_{n}}{n+1}",
                    font_size=44, color=INK),
            kr("a₅ 의 값은?", 30, MUTED),
        ).arrange(DOWN, buff=0.35).move_to(UP * 2.1)
        self.play(Write(prob[0]), run_time=1.3)
        self.play(FadeIn(prob[1], shift=UP * 0.2))
        self.wait(0.7)

        steps = [
            (r"a_{2}=\frac{a_{1}}{2}=\frac{12}{2}=6", "n=1"),
            (r"a_{3}=\frac{a_{2}}{3}=\frac{6}{3}=2", "n=2"),
            (r"a_{4}=\frac{a_{3}}{4}=\frac{2}{4}=\frac{1}{2}", "n=3"),
            (r"a_{5}=\frac{a_{4}}{5}=\frac{1/2}{5}=\frac{1}{10}", "n=4"),
        ]
        shown = VGroup()
        for i, (tex, tag) in enumerate(steps):
            y = 0.75 - i * 1.0
            t = kr(tag, 24, WARM, BOLD).move_to(LEFT * 5.2 + UP * y)
            m = MathTex(tex, font_size=38, color=INK).move_to(LEFT * 1.0 + UP * y)
            self.play(FadeIn(t, shift=RIGHT * 0.2), run_time=0.35)
            self.play(Write(m), run_time=0.9)
            shown.add(t, m)

        self.wait(0.7)
        ans = MathTex(r"a_{5}=\frac{1}{10}", font_size=46, color=GOOD)
        ans.move_to(RIGHT * 4.3 + DOWN * 1.4)
        self.play(Write(ans), run_time=1.0)
        self.play(Create(box(ans, GOOD)))
        self.wait(0.8)

        tip = kr("일반항이 안 보이면 n = 1, 2, 3 … 을 넣어 규칙을 먼저 본다",
                 28, MUTED).move_to(DOWN * 3.3)
        self.play(FadeIn(tip, shift=UP * 0.2))
        self.wait(2.2)


# ──────────────────────────────────────────────────────────────
# 6차시 · 수학적 귀납법 — 도미노 두 개만 확인하면 된다
# ──────────────────────────────────────────────────────────────
class S6Induction(Scene):
    def construct(self):
        hd = head("수학적 귀납법 — 도미노 두 개만 확인한다")
        self.add(hd)

        # 도미노 줄
        n = 7
        tiles = VGroup()
        for i in range(n):
            r = Rectangle(width=0.34, height=1.15, stroke_color=ACCENT,
                          stroke_width=3, fill_color=ACCENT_SOFT, fill_opacity=1)
            tiles.add(r)
        tiles.arrange(RIGHT, buff=0.5).move_to(UP * 1.25)
        nums = VGroup(*[
            MathTex(f"{i+1}" if i < 4 else ("k" if i == 4 else
                                            ("k{+}1" if i == 5 else r"\cdots")),
                    font_size=24, color=MUTED).next_to(tiles[i], DOWN, buff=0.22)
            for i in range(n)
        ])
        self.play(LaggedStartMap(FadeIn, tiles, shift=UP * 0.2, lag_ratio=0.1),
                  FadeIn(nums), run_time=1.5)

        # 첫 번째를 넘어뜨린다
        c1 = kr("① n = 1 일 때 성립", 30, WARM, BOLD).move_to(LEFT * 3.8 + DOWN * 0.9)
        self.play(FadeIn(c1, shift=UP * 0.2))
        self.play(tiles[0].animate.rotate(-PI / 2.4, about_point=tiles[0].get_bottom())
                  .set_fill(WARM_SOFT).set_stroke(WARM), run_time=0.6)
        self.play(Flash(tiles[0].get_center(), color=WARM, line_length=0.2))
        self.wait(0.6)

        # 화면 오른쪽 끝을 넘지 않도록 짧게 (프레임 반폭 7.11)
        c2 = kr("② n = k 성립  →  n = k+1 성립", 28, GOOD, BOLD)
        c2.move_to(RIGHT * 3.2 + DOWN * 0.9)
        self.play(FadeIn(c2, shift=UP * 0.2))
        link = Arrow(tiles[4].get_top() + UP * 0.25, tiles[5].get_top() + UP * 0.25,
                     color=GOOD, stroke_width=4, buff=0.05,
                     max_tip_length_to_length_ratio=0.35)
        self.play(GrowArrow(link))
        self.wait(0.6)

        # 연쇄적으로 넘어간다 (화살표는 역할을 다했으므로 걷어낸다)
        self.play(FadeOut(link), run_time=0.3)
        for i in range(1, n):
            self.play(tiles[i].animate.rotate(
                -PI / 2.4, about_point=tiles[i].get_bottom())
                .set_fill(GOOD_SOFT).set_stroke(GOOD), run_time=0.16)

        self.wait(0.6)
        concl = kr("→ 모든 자연수 n 에 대하여 성립", 32, GOOD, BOLD)
        concl.move_to(DOWN * 2.15)
        self.play(FadeIn(concl, shift=UP * 0.2))
        self.play(Create(box(concl, GOOD, buff=0.25)))
        self.wait(1.6)

        wipe(self, hd)

        # 실제 증명의 뼈대
        frame_t = kr("증명의 뼈대", 32, INK, BOLD).move_to(UP * 2.4)
        self.play(FadeIn(frame_t))
        proof = VGroup(
            MathTex(r"1+3+5+\cdots+(2n-1)=n^{2}", font_size=42, color=ACCENT),
            MathTex(r"\text{(i)}\ n=1:\ 1=1^{2}\ \checkmark", font_size=36, color=INK),
            MathTex(r"\text{(ii)}\ n=k:\ 1+3+\cdots+(2k-1)=k^{2}",
                    font_size=34, color=MUTED),
            MathTex(r"+\,(2k+1):\quad k^{2}+(2k+1)=(k+1)^{2}\ \checkmark",
                    font_size=36, color=GOOD),
        ).arrange(DOWN, buff=0.52).move_to(DOWN * 0.3)
        for m in proof:
            self.play(Write(m), run_time=1.1)
            self.wait(0.25)
        self.play(Create(box(proof[3], GOOD, buff=0.22)))
        self.wait(2.2)
