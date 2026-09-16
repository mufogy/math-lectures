const slides = [...document.querySelectorAll('.slide')];
const stage  = document.getElementById('stage');
const bar    = document.getElementById('bar');
let cur = 0;

/* KaTeX 가 수식을 MathML+HTML 로 이중 삽입하므로,
   하단바에 쓸 제목은 렌더링 '전에' 미리 뽑아 둔다. */
const titles = slides.map(s => {
  const h = s.querySelector('h1, h2');
  if (!h) return '';
  const c = h.cloneNode(true);
  c.querySelector('.pg')?.remove();      // 쪽수 배지는 제목에서 뺀다
  return c.textContent
          .replace(/\$([^$]*)\$/g, '$1') // KaTeX 구분자 $…$ 는 벗겨 낸다
          .replace(/\s+/g, ' ').trim();
});

/* 무대를 화면 크기에 맞춰 축소 */
function fit(){
  const pad = 40;
  const s = Math.min((innerWidth - pad) / 1600, (innerHeight - pad) / 900);
  stage.style.transform = `scale(${s})`;
}
addEventListener('resize', fit);

/* 슬라이드 이동 */
function show(i){
  cur = Math.max(0, Math.min(slides.length - 1, i));
  slides.forEach((s, k) => {
    const on = k === cur;
    s.classList.toggle('on', on);
    const v = s.querySelector('video');
    if (v){
      if (on){
        if (!v.src && v.dataset.src) v.src = v.dataset.src;   // 보일 때 로드
      } else if (!v.paused) v.pause();
    }
  });
  const s = slides[cur];
  document.getElementById('c-sec').textContent   = s.dataset.sec || '';
  document.getElementById('c-title').textContent = titles[cur];
  document.getElementById('c-num').textContent   = `${cur + 1} / ${slides.length}`;
  document.getElementById('n-body').textContent  = s.dataset.notes || '(노트 없음)';
  bar.style.width = ((cur + 1) / slides.length * 100) + '%';
  document.querySelectorAll('.ov').forEach((o, k) => o.classList.toggle('cur', k === cur));
  location.hash = cur + 1;
}
const next = () => show(cur + 1);
const prev = () => show(cur - 1);

/* 전체 보기 */
const ov = document.getElementById('overview');
slides.forEach((s, i) => {
  const d = document.createElement('div');
  d.className = 'ov';
  d.innerHTML = `<div class="ov-t">${titles[i] || '슬라이드'}</div>
                 <div class="ov-n">${i + 1}</div>`;
  d.onclick = () => { ov.classList.remove('on'); show(i); };
  ov.appendChild(d);
});

/* 키보드 */
addEventListener('keydown', e => {
  if (e.target.tagName === 'INPUT') return;
  switch(e.key){
    case 'ArrowRight': case 'PageDown': case ' ': e.preventDefault(); next(); break;
    case 'ArrowLeft':  case 'PageUp':            e.preventDefault(); prev(); break;
    case 'Home': show(0); break;
    case 'End':  show(slides.length - 1); break;
    case 'n': case 'N': case 'ㅜ':
      document.getElementById('notes').classList.toggle('on'); break;
    case 'o': case 'O': case 'ㅐ':
      ov.classList.toggle('on'); break;
    case 'f': case 'F': case 'ㄹ':
      document.fullscreenElement ? document.exitFullscreen()
                                 : document.documentElement.requestFullscreen(); break;
    case 'b': case 'B': case 'ㅠ':
      document.body.style.visibility =
        document.body.style.visibility === 'hidden' ? 'visible' : 'hidden'; break;
    case '?': case '/':
      document.getElementById('help').classList.toggle('on'); break;
    case 'Escape':
      ov.classList.remove('on');
      document.getElementById('help').classList.remove('on'); break;
  }
});

/* 클릭 이동 — 영상·컨트롤 위에서는 무시 */
stage.addEventListener('click', e => {
  if (e.target.closest('video')) return;
  (e.clientX > innerWidth / 2 ? next : prev)();
});

/* 영상이 없을 때 안내로 대체 */
addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.video-wrap video').forEach(v => {
    v.addEventListener('error', () => {
      const w = v.closest('.video-wrap');
      w.innerHTML = `<div class="video-missing">
        manim 영상이 아직 렌더링되지 않았습니다.<br>
        <code>build_manim.ps1 -SceneFile ...\\05_자료\\manim\\k01_scenes.py</code><br>
        <span style="font-size:20px">기대 경로: ${v.dataset.src}</span></div>`;
    });
  });

  renderMathInElement(document.body, {
    delimiters: [
      {left:'$$', right:'$$', display:true},
      {left:'$',  right:'$',  display:false}
    ],
    throwOnError: false
  });

  fit();
  const h = parseInt(location.hash.slice(1), 10);
  show(Number.isInteger(h) && h > 0 ? h - 1 : 0);
  setTimeout(() => document.getElementById('hint').style.display = 'none', 6000);
});
