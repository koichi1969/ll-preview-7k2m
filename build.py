# -*- coding: utf-8 -*-
"""
LOUVRELINE デモサイト ビルドスクリプト
  python build.py  を実行すると、index.html / products.html / cases.html /
  company.html / contact.html と cases/*.html を生成します。
  （共通ヘッダー・フッターをひとつの場所で管理するための補助スクリプトです）
"""
import os, io

ROOT = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------
# 共通データ
# ------------------------------------------------------------------
SITE = "ルーバーライン｜可動ルーバー自動制御システム"
TEL = "000-000-0000"          # 仮
POSTAL = "〒000-0000"          # 仮
ADDRESS = "○○県○○市○○町0-0-0"  # 仮
EMAIL = "info@louverline.jp"

CASES = [
    dict(slug="karumai", name="軽米文化センター", pref="岩手県", year="2023年3月", cat="public", catname="公共・文化施設",
         product="可動ルーバー タテライン 電動式 Aerofoil 330", control="電動式（タテライン）", n=8, thumb=1,
         tagline="木目調のタテラインルーバーが、文化施設の顔をつくる。",
         body=["ガラスファサードの前面に、木目調のタテライン（縦型）可動ルーバーを連続して設置。日中はルーバーの角度で直射日光をやわらげ、ホワイエに穏やかな光を届けます。",
               "連続する縦のラインが建物全体に統一感をもたらし、地域の文化拠点にふさわしい外観を実現しました。ルーバーテック株式会社のパンフレット表紙にも採用された物件です。"]),
    dict(slug="chiba-dc", name="千葉DC我孫子研究所", pref="千葉県", year="2020年", cat="office", catname="事務所・研究施設",
         product="Airfoil 210 @200 ヨコライン / 電動式 / 木目調転写塗装 / 自動制御システム（タイマー式）", control="自動制御システム（タイマー式）", n=8, thumb=1,
         tagline="木目調のヨコラインルーバーを、365日タイマーで自動制御。",
         body=["研究所の執務エリア外周に、木目調転写塗装のヨコライン（横型）可動ルーバーを設置。365日タイマー式の自動制御システムにより、季節と時刻に応じた最適な角度で日射を遮蔽します。",
               "室内からは、ルーバーのすき間越しに周囲の景色が見え、閉塞感のない明るい執務空間を実現。西日対策と空調負荷の低減を同時に叶えた事例です。"]),
    dict(slug="sansho", name="自動車用品会社 新社屋", pref="静岡県", year="2017年", cat="office", catname="事務所・研究施設",
         product="Airfoil 210 ヨコライン 電動式可動ルーバー 自動制御システム", control="自動制御システム", n=5, thumb=1,
         tagline="新社屋の窓面全体を、自動制御ルーバーで包む。",
         body=["新築社屋の各階窓面に、ヨコラインの電動式可動ルーバーを連続配置。自動制御システムにより、従業員が操作することなく日射と眩しさをコントロールします。",
               "全閉時にはシャッターのように窓面を覆い、防犯面にも配慮。日射計を屋上に設置し、天候に応じた制御を行っています。"]),
    dict(slug="m-clinic", name="M医院", pref="奈良県", year="2017年", cat="medical", catname="医療施設",
         product="Aerofoil 330 縦ライン電動式可動ルーバー 自動制御システム（タイマー式）", control="自動制御システム（タイマー式）", n=5, thumb=1,
         tagline="白いタテラインルーバーで、待合室に心地よい光を。",
         body=["医院の2階待合・診療エリアの外周に、白色のタテライン可動ルーバー（Aerofoil 330）を設置。タイマー式の自動制御により、患者さまの滞在時間帯に合わせて光と視線をコントロールします。",
               "外部からの視線を遮りプライバシーを守りながら、ルーバーの間から自然光と風を取り込む設計。医療施設に求められる快適性と清潔感を両立しました。"]),
    dict(slug="ikari", name="いかりスーパー", pref="兵庫県", year="2015年", cat="commercial", catname="商業施設",
         product="Airfoil 210 ヨコライン 電動式可動ルーバー", control="電動式（ヨコライン）", n=4, thumb=1,
         tagline="店舗の高窓に、電動ヨコラインルーバー。",
         body=["スーパーマーケットの売場上部に設けられた高窓に、ヨコラインの電動式可動ルーバーを設置。商品の日焼けを防ぎながら、売場に自然光を取り込みます。",
               "営業時間や天候に合わせてルーバー角度を調整でき、照明・空調のエネルギー削減にも貢献しています。"]),
]
CASE_BY_SLUG = {c["slug"]: c for c in CASES}

# ------------------------------------------------------------------
# アイコン（インラインSVG）
# ------------------------------------------------------------------
ICON = {
 "sun": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
 "shade": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 6h18M3 10h18M3 14h18M3 18h18"/><path d="M12 2v2"/></svg>',
 "rain": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M7 15a4 4 0 0 1-.5-8 5.5 5.5 0 0 1 10.6 1.5A3.5 3.5 0 0 1 17 15H7z"/><path d="M8 18l-1 2M12 18l-1 2M16 18l-1 2"/></svg>',
 "eye": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="3"/><path d="M4 4l16 16"/></svg>',
 "cloud": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M7 17a4 4 0 0 1-.5-8 5.5 5.5 0 0 1 10.6 1.5A3.5 3.5 0 0 1 17 17H7z"/><circle cx="18" cy="5" r="2.5"/></svg>',
 "lock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>',
 "thermo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M10 14.5V5a2 2 0 1 1 4 0v9.5a3.5 3.5 0 1 1-4 0z"/></svg>',
 "chip": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/></svg>',
 "touch": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 22h8M12 18v4"/></svg>',
 "gauge": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 18a8 8 0 1 1 16 0"/><path d="M12 18l4-6"/></svg>',
 "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 20c0-9 6-15 16-16-1 10-7 16-16 16z"/><path d="M4 20c4-5 8-8 12-10"/></svg>',
 "wind": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 8h11a3 3 0 1 0-3-3M3 12h15a3 3 0 1 1-3 3M3 16h8a2 2 0 1 1-2 2"/></svg>',
 "design": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 20l12-12 4 4L8 24H4v-4z"/><path d="M14 6l4 4"/></svg>',
 "factory": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 21V9l6 4V9l6 4V9l6 4v8H3z"/><path d="M7 21v-4h4v4"/></svg>',
 "school": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 21V10l9-5 9 5v11"/><path d="M9 21v-6h6v6"/><path d="M12 10v2"/></svg>',
 "shop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 9l1-5h14l1 5"/><path d="M4 9a2.5 2.5 0 0 0 5 0 2.5 2.5 0 0 0 5 0 2.5 2.5 0 0 0 5 0"/><path d="M5 11v10h14V11"/><path d="M10 21v-6h4v6"/></svg>',
 "office": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="4" y="3" width="16" height="18"/><path d="M8 7h3M13 7h3M8 11h3M13 11h3M8 15h3M13 15h3M10 21v-3h4v3"/></svg>',
 "hospital": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="4" y="4" width="16" height="17"/><path d="M12 8v6M9 11h6M10 21v-4h4v4"/></svg>',
 "house": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/></svg>',
 "warehouse": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 20V8l9-4 9 4v12"/><path d="M7 20v-7h10v7M7 16h10"/></svg>',
}

# ------------------------------------------------------------------
# 共通テンプレート
# ------------------------------------------------------------------
def head(title, base, desc="可動ルーバーの開発・製造メーカー ルーバーライン。365日カレンダー×気象条件で可動ルーバーを自動制御する「可動ルーバー自動制御システム」のご紹介。"):
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Outfit:wght@300;400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/css/style.css">
<link rel="icon" href="{base}assets/img/logo.png">
</head>
<body>
<header class="site-header">
  <div class="inner">
    <a class="brand" href="{base}index.html"><img src="{base}assets/img/logo.png" alt="LOUVRELINE ルーバーライン"></a>
    <button class="nav-toggle" aria-label="メニュー"><span></span><span></span><span></span></button>
    <nav class="gnav">
      <a href="{base}index.html" data-page="index.html">TOP</a>
      <a href="{base}products.html" data-page="products.html">製品紹介</a>
      <a href="{base}cases.html" data-page="cases.html">導入事例</a>
      <a href="{base}company.html" data-page="company.html">会社案内</a>
      <a href="{base}contact.html" class="btn-contact">お問い合わせ</a>
    </nav>
  </div>
</header>
<main>
"""

def cta(base):
    return f"""
<section class="cta">
  <div class="container">
    <a class="card" href="{base}contact.html">
      <div>
        <span class="en">Contact</span><span class="ja">お問い合わせ</span>
        <p>製品のご質問、設計・お見積りのご相談、既設ルーバーの自動制御化など、<br>お気軽にご相談ください。</p>
      </div>
      <span class="arrow">→</span>
    </a>
  </div>
</section>
"""

def foot(base):
    return f"""
</main>
<footer class="site-footer">
  <div class="container">
    <div class="grid">
      <div>
        <a class="logo" href="{base}index.html"><img src="{base}assets/img/logo-white.png" alt="LOUVRELINE"></a>
        <div class="corp">ルーバーライン</div>
        <div class="tel">TEL: {TEL}</div>
        <div class="hours">受付時間 9:00-17:00（土・日・祝日を除く）</div>
        <address>{POSTAL}<br>{ADDRESS}<br>E-MAIL: {EMAIL}</address>
      </div>
      <ul class="links">
        <li><a href="{base}index.html">TOP</a></li>
        <li><a href="{base}company.html">会社案内</a></li>
        <li><a href="#">プライバシーポリシー</a></li>
        <li><a href="{base}products.html">製品紹介</a></li>
        <li><a href="{base}contact.html">お問い合わせ</a></li>
        <li><a href="#">サイトマップ</a></li>
        <li><a href="{base}cases.html">導入事例</a></li>
      </ul>
    </div>
    <div class="copy">©2026 LOUVRELINE</div>
    <div class="demo-note">※ 本サイトはデモ用です。住所・電話番号・一部画像は仮のものです。</div>
  </div>
</footer>
<script src="{base}assets/js/main.js"></script>
</body>
</html>
"""

def case_card(c, base):
    return f"""
      <a class="case-card reveal" href="{base}cases/{c['slug']}.html" data-cat="{c['cat']}">
        <div class="thumb"><img src="{base}assets/img/cases/{c['slug']}/{c['thumb']:02d}.jpg" alt="{c['name']}"></div>
        <div class="meta"><span class="cat">{c['catname']}</span>{c['pref']}</div>
        <div class="name">{c['name']}（{c['control']}）</div>
        <div class="spec">{c['year']}納入</div>
      </a>"""

# ------------------------------------------------------------------
# トップページ
# ------------------------------------------------------------------
def page_index():
    b = ""
    cards = "".join(case_card(CASE_BY_SLUG[s], b) for s in ["karumai", "chiba-dc", "m-clinic"])
    return head(SITE, b) + f"""
<section class="hero">
  <img class="bg" src="assets/img/hero.jpg" alt="可動ルーバーを設置した建物">
  <div class="inner">
    <div class="tag">Movable Louver Planning &amp; Design</div>
    <h1>光と風を、365日 自動でコントロール。<br>可動ルーバー自動制御システム</h1>
    <p>日本古来の伝統技術を継承した可動ルーバーに、カレンダーと気象条件で動く自動制御を搭載。<br>リモコン操作いらずで、一年中快適な室内環境と省エネルギーを実現します。</p>
    <p>ルーバーラインは、可動ルーバーと駆動装置・制御システムを自社で開発・製造するメーカーです。</p>
    <div class="badges"><span>365日カレンダー × 気象条件</span><span>業界初 自動コントロールタイプ</span><span>ZEB対応・カーボンニュートラル</span></div>
  </div>
  <div class="scroll">SCROLL</div>
</section>

<section class="concept">
  <div class="container">
    <div class="grid">
      <div class="reveal">
        <div class="sec-head"><span class="en">Concept</span><span class="ja">ルーバーラインとは</span></div>
        <h2 class="ttl">可動ルーバーの開発・製造から、<br>自動制御システムまで一貫して。</h2>
        <p class="lead">ルーバーラインは、アルミ押出成形による可動ルーバーと、それを動かす駆動装置・制御システムを自社で企画・開発・製造する可動ルーバー専門メーカーです。可動ルーバー「ルーバーテック」のOEM供給元として、大型施設から戸建て住宅まで数多くの建物に製品をお届けしてきました。</p>
        <p class="lead" style="margin-top:12px">2025年、PLC（シーケンサ）と独自センサーによる「可動ルーバー自動制御システム」を発表。目隠し・採光・通風・日よけの4つの機能はそのままに、365日の自動運転で建物の省エネ化を支えます。</p>
      </div>
      <div class="reveal"><img src="assets/img/cases/karumai/08.jpg" alt="タテライン可動ルーバー" style="box-shadow:var(--shadow)"></div>
    </div>
    <div class="stats reveal">
      <div class="stat"><div class="num">4<small>機能</small></div><div class="lbl">目隠し・採光・通風・日よけ</div></div>
      <div class="stat"><div class="num">365<small>日</small></div><div class="lbl">カレンダー × 気象条件で自動制御</div></div>
      <div class="stat"><div class="num">3<small>倍</small></div><div class="lbl">ブラインド比 熱量遮蔽性能</div></div>
      <div class="stat"><div class="num">2020</div><div class="lbl">グッドデザイン賞受賞（共同開発製品）</div></div>
    </div>
  </div>
</section>

<section class="band-teal">
  <div class="container">
    <div class="grid">
      <div class="reveal">
        <div class="sec-head on-dark"><span class="en">Products</span><span class="ja">製品紹介</span></div>
        <h3>365日カレンダー × 気象条件。<br>可動ルーバー自動制御システム</h3>
        <p>制御盤内のPLCが日出没時刻表と設置場所の緯度・経度から太陽の位置を算出し、ルーバーを最適な角度へ。日射計・温度計などのセンサーを加えることで、曇りの日や室温の上昇にも自動で対応します。</p>
        <p>タッチパネルで自動・手動の切り替えもワンタッチ。従業員の操作負担をなくし、確実な運用を実現します。</p>
        <ul class="feature-list"><li>目隠し</li><li>採光</li><li>通風</li><li>日よけ</li></ul>
        <a class="btn btn-white" href="products.html">製品紹介</a>
      </div>
      <div class="visual reveal">
        <img src="assets/img/cases/chiba-dc/04.jpg" alt="木目調ヨコライン可動ルーバー">
        <div class="cap">千葉DC我孫子研究所｜自動制御システム（タイマー式）</div>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="container">
    <div class="sec-head inline reveal">
      <div><span class="en">Cases</span><span class="ja">導入事例</span></div>
      <p class="lead">可動ルーバー・自動制御システムは、<br>文化施設、研究所、医療施設、商業施設など、規模・種別を問わずさまざまな建物に導入いただいています。</p>
      <a class="btn" href="cases.html" style="margin-left:auto">導入事例一覧</a>
    </div>
    <div class="case-grid">{cards}
    </div>
  </div>
</section>

<div class="strip"><img src="assets/img/cases/karumai/05.jpg" alt="軽米文化センター"></div>

<section class="band-light">
  <div class="container">
    <div class="grid">
      <div class="reveal">
        <div class="sec-head"><span class="en">Company</span><span class="ja">会社案内</span></div>
        <p>可動ルーバーの企画・設計から製造まで。<br>光と風をデザインする可動ルーバー専門メーカー、ルーバーライン。<br>設計者・施工会社の皆さまのパートナーとして、自由設計・受注生産で建物のニーズにお応えします。</p>
        <a class="btn" href="company.html">会社案内</a>
      </div>
      <div class="visual reveal"><img src="assets/img/company-building.svg" alt="ルーバーライン 本社・工場（仮画像）"></div>
    </div>
  </div>
</section>
""" + cta(b) + foot(b)

# ------------------------------------------------------------------
# 製品紹介
# ------------------------------------------------------------------
def fn_card(icon, title, text):
    return f'<div class="fn reveal"><div class="ic">{ICON[icon]}</div><h4>{title}</h4><p>{text}</p></div>'

def page_products():
    b = ""
    fns = "".join([
        fn_card("sun", "光の調整", "室内の明るさ・温度を自由自在に調節できます。西日対策のほか、商品の日焼け防止に効果的です。"),
        fn_card("shade", "直射日光の遮断", "地域や季節による日照角度を考慮し、可動式ルーバーで最適な角度を設定。一年中、快適な室内空間を維持できます。"),
        fn_card("rain", "雨の防止", "雨から洗濯物・草花・ペットを守ります。窓の外に設置してあるのでシャッターの役目も果たします。"),
        fn_card("eye", "プライバシー", "屋外からの視線を遮りプライバシーを保護し、コミュニケーションスペースを確保します。"),
        fn_card("cloud", "天候に合わせた調整", "降雨時には雨の浸入を防ぎ、日差しの強い晴天時には直射日光を遮って温度上昇を防止します。"),
        fn_card("lock", "防犯性アップ", "可動式ルーバーは視線を遮りながら窓を閉じ、防犯対策への対応力を強化します。自由に調節できるルーバーが安全と安心をサポートします。"),
    ])
    feats = "".join([
        fn_card("design", "高いデザイン性", "アルミニウム押出成形型の美しいフォルムと、連続性のある直線形状により高いデザイン性を発揮。カラーリングも自由に施せます。"),
        fn_card("lock", "防犯性能", "ルーバーは外部から取り外しできないように設計。全閉時にはシャッターのように全面を覆って窓ガラスを護ります。"),
        fn_card("factory", "受注生産と自由設計", "お客様のニーズに対応可能な製品ラインナップをご用意。受注生産により、建物にマッチした製品をご提供します。"),
        fn_card("gauge", "調整性能", "施設内の明るさと温度を自由自在に調整。直射日光の遮断、雨風からの保護、外からの視線の遮断でプライバシーを守ります。"),
        fn_card("thermo", "優れた省エネ性", "窓の外で日射を遮蔽するため夏季には高い断熱性能を発揮。屋内への熱量遮蔽性能はブラインドの3倍。冬季は日射を採り入れ暖房費を削減します。"),
        fn_card("leaf", "環境負荷の低減", "ほとんどの部材にアルミニウムを使用してリサイクル性を確保し、環境負荷を低減します。"),
    ])
    return head("製品紹介｜" + SITE, b) + f"""
<section class="page-hero">
  <img src="assets/img/cases/karumai/06.jpg" alt="">
  <div class="inner"><span class="en">Products</span><span class="ja">製品紹介</span></div>
</section>
<div class="container breadcrumb"><a href="index.html">TOP</a><span>製品紹介</span></div>

<section class="sec" style="padding-top:70px">
  <div class="container">
    <div class="intro-block reveal">
      <span class="label-teal">ZEB化・カーボンニュートラルを検討されている建築関係の方へ</span>
      <h2>日本古来の伝統技術を継承した採光や通風を、<br>自動でコントロール。可動ルーバーは進化します。</h2>
      <p class="lead">可動ルーバーは、日本古来の伝統技術を活かして採光や通風をコントロールする建材です。ルーバーを開けて自然の光や風、景色をとり込み、ルーバーを閉じて紫外線や雨、風、視線を防ぎます。カーボンニュートラルの達成に向けて建物の省エネ化が求められる中、当社の製品は大型施設から一般的な戸建て住宅に至るまで幅広く採用されています。2020年には、3社の共同開発による製品がグッドデザイン賞を受賞しました。</p>
    </div>
  </div>
</section>

<section class="bg-light sec">
  <div class="container">
    <h2 class="ttl reveal">365日カレンダー × 気象条件で動く、新しい可動ルーバー。</h2>
    <div class="sec-head reveal"><span class="en">Latest product</span><span class="ja">最新製品</span></div>
    <div class="kv-product reveal">
      <img src="assets/img/hero.jpg" alt="可動ルーバー自動制御システム 設置例">
      <div class="ov"><strong>ルーバーライン 可動ルーバー自動制御システム</strong><span>ルーバーに新しい風。年中無休の制御が始まる。</span></div>
    </div>
    <div class="mt-60">
      <div class="reveal" style="max-width:860px">
        <div class="pill-row"><span class="pill outline">365日 カレンダー</span><span class="x-mark">×</span><span class="pill outline">気象条件</span></div>
        <h2 class="ttl" style="font-size:32px">自動コントロールタイプ 誕生 <span style="display:inline-block;background:var(--wood);color:#fff;font-size:15.5px;padding:4px 12px;border-radius:30px;vertical-align:middle;margin-left:8px">業界初</span></h2>
        <p class="lead">気象状況に応じてリモコンでの開閉が不要な365日自動制御に、独自センサーを加えた、理想を実現した新しいルーバーです。</p>
        <div class="pill-row"><span class="pill">目隠し</span><span class="pill">採光</span><span class="pill">通風</span><span class="pill">日よけ</span></div>
        <p class="lead">の4つの機能は据え置き。可動ルーバーの良さはそのままに、自動制御で<strong>快適さと省エネを両立</strong>します。</p>
      </div>
      <div class="reveal mt-60">
        <span class="label-teal">新機能搭載｜センサーによる制御ロジック</span>
        <table class="logic-table">
          <thead><tr><th>条件</th><th>外部・室内の状態</th><th></th><th>ルーバー</th><th>室内</th></tr></thead>
          <tbody>
            <tr><th rowspan="2">太陽光による変化<small>日射計</small></th><td>外が明るい</td><td class="arrow">→</td><td class="res close">閉</td><td>トーンダウン</td></tr>
            <tr><td>外が暗い</td><td class="arrow">→</td><td class="res">開</td><td>トーンアップ</td></tr>
            <tr><th rowspan="2">温度による変化<small>サーモセンサー</small></th><td>室内温度 上昇</td><td class="arrow">→</td><td class="res close">閉</td><td>温度上昇を抑制</td></tr>
            <tr><td>室内温度 下降</td><td class="arrow">→</td><td class="res">開</td><td>日射を採り入れる</td></tr>
            <tr><th rowspan="2">室内照度<small>照度計</small></th><td>明るい</td><td class="arrow">→</td><td class="res close">閉</td><td>眩しさを低減</td></tr>
            <tr><td>暗い</td><td class="arrow">→</td><td class="res">開</td><td>採光を確保</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</section>

<section class="adv">
  <div class="container">
    <div class="sec-head reveal"><span class="en" style="font-size:36px">Advantages</span><span class="ja">自動制御システムの特長</span></div>

    <div class="adv-item">
      <div class="reveal">
        <div class="num">01</div>
        <h3>太陽の位置・天候に合わせて<br>ルーバーの開閉を自動制御</h3>
        <p>制御盤内に取り付けられたPLC（プログラマブル・ロジック・コントローラ／三菱電機製シーケンサ）が、日出没時刻表を基本動作として、設定された緯度・経度と現在の日時から太陽の位置を算出。ルーバーが太陽光と直角になるように稼働し、季節や時間によって変化する日射を365日自動で遮蔽します。暗い日は日射計が感知して採光する「照度補正」機能付きです。</p>
        <ul class="icon-tags"><li>{ICON['chip']}PLCによるシーケンス制御</li><li>{ICON['sun']}日出没時刻表・太陽位置を算出</li><li>{ICON['gauge']}照度補正で採光を確保</li></ul>
      </div>
      <div class="reveal"><img src="assets/img/panel-auto.svg" alt="自動運転画面（イメージ）"><div class="cap">タッチパネル 自動運転画面（イメージ）</div></div>
    </div>

    <div class="adv-item">
      <div class="reveal">
        <div class="num">02</div>
        <h3>エンコーダーによる高精度な角度制御と、<br>センサーによる拡張性</h3>
        <p>ただ開閉するだけではなく、モーターを細かく制御してルーバーの角度を調整するためにエンコーダーを使用。正確かつ細かな角度設定が可能です。「ピラノメーター（日射計）」や「サーモセンサー（温度計）」などの拡張性を持たせることで、採遮光条件をより細かく設定できます。</p>
        <ul class="icon-tags"><li>{ICON['gauge']}エンコーダーで角度を高精度制御</li><li>{ICON['sun']}ピラノメーター（日射計）</li><li>{ICON['thermo']}サーモセンサー（温度計）</li></ul>
      </div>
      <div class="reveal"><img src="assets/img/system-diagram.svg" alt="システム構成図"><div class="cap">システム構成イメージ</div></div>
    </div>

    <div class="adv-item">
      <div class="reveal">
        <div class="num">03</div>
        <h3>タッチパネルで、<br>自動・手動の切り替えもワンタッチ</h3>
        <p>新たに導入したタッチパネル（三菱電機製 5.7型TFTカラー液晶）により、自動運転と手動運転の切り替えが容易になりました。手動画面ではボタンを押している間だけルーバーが正転・逆転し、現在の角度を表示。設定画面では制御の開始・終了時間、照度の設定範囲、調整間隔、待機角度、最大角度などを建物ごとに細かく設定できます。</p>
        <ul class="icon-tags"><li>{ICON['touch']}5.7型 TFTカラー液晶タッチパネル</li><li>{ICON['chip']}制御時間・照度範囲・角度を設定</li></ul>
      </div>
      <div class="reveal"><img src="assets/img/panel-manual.svg" alt="手動運転画面（イメージ）"><div class="cap">タッチパネル 手動運転画面（イメージ）</div></div>
    </div>

    <div class="adv-item">
      <div class="reveal">
        <div class="num">04</div>
        <h3>屋内・屋外兼用の制御盤。<br>既設の電動ルーバーにも対応</h3>
        <p>制御盤は屋内・屋外兼用の鋼板製キャビネット。水切構造・防塵・防水パッキンを備え、屋外設置にも対応します。駆動装置は自社開発のため、新築はもちろん、既設の電動ルーバーへの自動制御システムの追加についてもご相談ください。</p>
        <table class="spec-table" style="margin-top:20px;font-size:15.5px">
          <tr><th>キャビネット寸法</th><td>W500 × H800 × D200（mm）</td></tr>
          <tr><th>材質</th><td>ボデー・ドア：鋼板 t1.6／基板：鋼板 t2.3</td></tr>
          <tr><th>色</th><td>クリーム（2.5Y9/1）</td></tr>
          <tr><th>構造</th><td>屋内・屋外兼用、水切構造、防塵・防水パッキン</td></tr>
          <tr><th>タッチパネル</th><td>三菱電機 TFTカラー液晶 5.7型（表示サイズ W115.2 × H86.4）</td></tr>
        </table>
      </div>
      <div class="reveal"><img src="assets/img/cabinet.svg" alt="制御盤（イメージ）" style="max-width:420px;margin:0 auto"><div class="cap center">制御盤キャビネットとタッチパネル（イメージ）</div></div>
    </div>
  </div>
</section>

<section class="bg-light sec">
  <div class="container">
    <h2 class="ttl reveal">PLCを活用した、ルーバー自動開閉システムの構成</h2>
    <p class="lead reveal" style="max-width:820px;margin-bottom:40px">システム構成は、制御盤内のPLCに日出没時刻表を基本動作設定とし、「ピラノメーター」や「サーモセンサー」などの拡張性を持たせることで採遮光条件をより細かく設定することができ、「エンコーダー」を使用することで高精度な制御を実現するシステムです。</p>
    <div class="step-flow reveal">
      <div class="step"><h4>可動ルーバー</h4><p>電動機によりルーバーを可動させます。新たに導入したタッチパネルにより自手動の切り替えが容易となります。</p></div>
      <div class="step"><h4>ピラノメーター（日射計）</h4><p>必要な照度を確保するためルーバーを細かく制御。曇りなどで採光が難しいときは通常よりも入光しやすい状態へと対応します。</p></div>
      <div class="step"><h4>サーモセンサー（温度計）</h4><p>日差しが強く室温が上昇する夏季には基本設定よりも遮光して温度上昇を抑制し、冬季は採光をすることで快適性を高めます。</p></div>
      <div class="step"><h4>エンコーダー</h4><p>モーターを細かく制御しルーバーを調整するためにエンコーダーを使用。正確かつ細かな設定が可能となります。</p></div>
    </div>

    <div class="two-col mt-80">
      <div class="reveal">
        <h3 class="sub">ご要望に応じた機能追加（オプション）</h3>
        <p class="lead" style="font-size:17px;margin-bottom:16px">以下のような機能追加は、ご要望に応じて検討・対応が可能です。</p>
        <ul class="option-list"><li>日射計</li><li>温度計</li><li>風速計</li><li>雨センサー</li><li>湿度計</li><li>エアコンとの連動</li><li>外気冷房との連動</li><li>その他ご相談</li></ul>
      </div>
      <div class="reveal">
        <h3 class="sub">自動化による主なメリット</h3>
        <ul class="merit" style="grid-template-columns:1fr;gap:12px">
          <li><strong>従業員の操作負担を軽減</strong><span>日々の開閉操作が不要になり、本来の業務に集中できます。</span></li>
          <li><strong>人的判断に伴うリスクを低減</strong><span>責任の所在や判断のばらつきをなくします。</span></li>
          <li><strong>確実な運用</strong><span>開閉管理を自動化することで、確実な運用が可能になります。</span></li>
        </ul>
        <div class="callout mt-40"><strong>ランニングコストの目安</strong><br>電気代は1台あたり約100円/日程度。手動への切り替えも可能です。</div>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="container">
    <div class="sec-head reveal"><span class="en" style="font-size:36px">Functions</span><span class="ja">可動ルーバーの優れた機能</span></div>
    <p class="lead reveal" style="max-width:860px;margin-bottom:44px">自由に開度を調節でき、眺望からプライベート空間まで、多彩なシーンに対応する可動ルーバー。視線と日射しをコントロールし、防犯にも貢献。採光や防風・防雨機能も備え、家庭から商業施設、医療・教育施設までの環境改善に寄与します。"目隠し"、"採光"、"通風"、"日よけ"の4つの機能を一つに結集した製品が、ルーバーラインの可動ルーバーです。その多機能性と信頼性が、幅広いシーンで可動ルーバーが選ばれ続けている理由です。</p>
    <div class="fn-grid">{fns}</div>
  </div>
</section>

<section class="bg-light2 sec">
  <div class="container">
    <div class="sec-head reveal"><span class="en" style="font-size:36px">Features</span><span class="ja">知っておきたいルーバーの特徴</span></div>
    <div class="fn-grid">{feats}</div>
  </div>
</section>

<section class="sec">
  <div class="container">
    <div class="two-col">
      <div class="reveal">
        <h3 class="sub">対象の建物</h3>
        <p class="lead" style="font-size:17px">規模・種別を問わず開発・設置が可能です。教育・研究機関や展示館などの大型施設から、一般の戸建て住宅まで幅広くご利用いただいています。</p>
      </div>
      <div class="target-grid reveal">
        <div class="target"><div class="ic">{ICON['school']}</div>教育・文化施設</div>
        <div class="target"><div class="ic">{ICON['shop']}</div>商業施設</div>
        <div class="target"><div class="ic">{ICON['office']}</div>事務所・研究所</div>
        <div class="target"><div class="ic">{ICON['hospital']}</div>医療施設</div>
        <div class="target"><div class="ic">{ICON['warehouse']}</div>工場・倉庫</div>
        <div class="target"><div class="ic">{ICON['house']}</div>一般住宅</div>
      </div>
    </div>

    <div class="mt-80 reveal">
      <h3 class="sub">製品ラインナップ</h3>
      <table class="spec-table">
        <tr><th>Airfoil 210 ヨコライン</th><td>翼型断面の横型可動ルーバー。事務所・研究施設・商業施設の窓面に。木目調転写塗装などのカラーリングに対応。</td></tr>
        <tr><th>Aerofoil 330 タテライン</th><td>大判の縦型可動ルーバー。文化施設・医療施設など、連続する縦のラインで建物の顔をつくります。</td></tr>
        <tr><th>可動ルーバー自動制御システム</th><td>PLC・エンコーダー・タッチパネルで構成する自動制御盤。365日タイマー式を基本に、日射計・温度計などのセンサーを追加可能。</td></tr>
        <tr><th>駆動装置</th><td>軽量なルーバーから重量のあるルーバーまで対応する自社開発の駆動装置。既設ルーバーの電動化・自動制御化もご相談ください。</td></tr>
      </table>
      <p class="note mt-40">※ 製品は受注生産です。仕様・寸法・カラーは建物に合わせて設計いたします。詳しくはお問い合わせください。</p>
    </div>
  </div>
</section>
""" + cta(b) + foot(b)

# ------------------------------------------------------------------
# 導入事例 一覧・詳細
# ------------------------------------------------------------------
def page_cases():
    b = ""
    cards = "".join(case_card(c, b) for c in CASES)
    return head("導入事例｜" + SITE, b) + f"""
<section class="page-hero plain">
  <div class="inner"><span class="en">Cases</span><span class="ja">導入事例</span></div>
</section>
<div class="container breadcrumb"><a href="index.html">TOP</a><span>導入事例</span></div>
<section class="sec" style="padding-top:20px">
  <div class="container">
    <div class="filter">
      <button class="is-active" data-cat="all">すべて</button>
      <button data-cat="public">公共・文化施設</button>
      <button data-cat="office">事務所・研究施設</button>
      <button data-cat="medical">医療施設</button>
      <button data-cat="commercial">商業施設</button>
    </div>
    <div class="case-grid two">{cards}
    </div>
  </div>
</section>
""" + cta(b) + foot(b)

def page_case(c, prev, nxt):
    b = "../"
    imgs = [f"{b}assets/img/cases/{c['slug']}/{i:02d}.jpg" for i in range(1, c["n"] + 1)]
    main = imgs[0]
    side = imgs[1:3]
    more = imgs[3:]
    side_html = "".join(f'<div><img src="{s}" data-zoom="{s}" alt="{c["name"]}"></div>' for s in side)
    more_html = ("".join(f'<img src="{s}" data-zoom="{s}" alt="{c["name"]}">' for s in more)) if more else ""
    body = "".join(f"<p>{p}</p>" for p in c["body"])
    return head(f"{c['name']}｜導入事例｜{SITE}", b) + f"""
<section class="page-hero plain">
  <div class="inner"><span class="en">Cases</span><span class="ja">導入事例</span></div>
</section>
<div class="container breadcrumb"><a href="../index.html">TOP</a><span><a href="../cases.html">導入事例</a></span><span>{c['name']}</span></div>
<section class="sec case-detail" style="padding-top:20px">
  <div class="container">
    <div class="gallery">
      <div class="main"><img src="{main}" data-zoom="{main}" alt="{c['name']}"></div>
      {side_html}
    </div>
    {('<div class="more">' + more_html + '</div>') if more_html else ''}
    <div class="info">
      <div>
        <div class="case-card" style="pointer-events:none"><div class="meta"><span class="cat">{c['catname']}</span>{c['pref']}</div></div>
        <h1>{c['name']}</h1>
        <div class="tagline">{c['tagline']}</div>
        <div class="body">{body}</div>
      </div>
      <div>
        <table class="spec-table">
          <tr><th>納入年</th><td>{c['year']}</td></tr>
          <tr><th>都道府県</th><td>{c['pref']}</td></tr>
          <tr><th>用途</th><td>{c['catname']}</td></tr>
          <tr><th>製品</th><td>{c['product']}</td></tr>
          <tr><th>制御方式</th><td>{c['control']}</td></tr>
        </table>
      </div>
    </div>
    <div class="pager">
      <a href="{prev['slug']}.html">← {prev['name']}</a>
      <a href="../cases.html">一覧へ戻る</a>
      <a href="{nxt['slug']}.html">{nxt['name']} →</a>
    </div>
  </div>
</section>
<div class="lightbox"><img src="" alt=""></div>
""" + cta(b) + foot(b)

# ------------------------------------------------------------------
# 会社案内
# ------------------------------------------------------------------
def page_company():
    b = ""
    return head("会社案内｜" + SITE, b) + f"""
<section class="page-hero">
  <img src="assets/img/cases/chiba-dc/02.jpg" alt="">
  <div class="inner"><span class="en">Company</span><span class="ja">会社案内</span></div>
</section>
<div class="container breadcrumb"><a href="index.html">TOP</a><span>会社案内</span></div>

<section class="sec" style="padding-top:70px">
  <div class="container">
    <div class="message">
      <div class="reveal">
        <span class="label-teal">Movable Louver Planning &amp; Design</span>
        <h2>可動ルーバーを、<br>企画・設計から製造まで。</h2>
        <p>ルーバーラインは、可動ルーバーと、それを動かす駆動装置・制御システムを自社で企画・開発・製造する可動ルーバー専門メーカーです。</p>
        <p>日本古来の伝統技術である「ルーバー」を、アルミ押出成形の美しいフォルムと確かな機構で現代の建築に。可動ルーバー「ルーバーテック」のOEM供給元として、教育・研究機関や展示館などの大型施設から一般の戸建て住宅まで、数多くの建物に製品をお届けしてきました。</p>
        <p>そして2025年、PLCとセンサーによる「可動ルーバー自動制御システム」を発表。光と風を365日自動でコントロールし、建物の省エネ化とカーボンニュートラルの実現に貢献します。</p>
      </div>
      <div class="reveal"><img src="assets/img/company-building.svg" alt="本社・工場（仮画像）"></div>
    </div>
  </div>
</section>

<section class="bg-light sec">
  <div class="container">
    <div class="sec-head reveal"><span class="en" style="font-size:36px">Business</span><span class="ja">事業内容</span></div>
    <div class="biz-grid">
      <div class="biz reveal"><div class="num">01</div><h4>可動ルーバーの開発・製造</h4><p>アルミ押出成形型の可動ルーバー（タテライン・ヨコライン）および固定ルーバーの企画・設計・製造。受注生産・自由設計で建物に合わせた製品をご提供します。</p></div>
      <div class="biz reveal"><div class="num">02</div><h4>駆動装置・自動制御システムの開発</h4><p>ルーバーを動かすオリジナル駆動装置、金型、樹脂ギヤ、そしてPLCを活用した可動ルーバー自動制御システムの開発・設計・製造。</p></div>
      <div class="biz reveal"><div class="num">03</div><h4>OEM供給・技術支援</h4><p>ルーバーテック株式会社をはじめとする販売パートナーへの製品供給と、設計・施工に関する技術支援。</p></div>
    </div>
    <div class="oem mt-60 reveal">
      <div class="flow">
        <div class="box">ルーバーライン<small>開発・製造（メーカー）</small></div>
        <span class="arr">→</span>
        <div class="box">ルーバーテック株式会社<small>OEM販売・設計・施工</small></div>
        <span class="arr">→</span>
        <div class="box">建物オーナー・設計者<small>施設・住宅</small></div>
      </div>
      <p>ルーバーラインで開発・製造した可動ルーバーと自動制御システムは、ルーバーテック株式会社よりOEM商品「ルーバーテック」として販売されています。メーカーであるルーバーラインへ直接ご相談いただくことも可能です。</p>
    </div>
  </div>
</section>

<section class="sec">
  <div class="container">
    <div class="sec-head reveal"><span class="en" style="font-size:36px">Profile</span><span class="ja">会社概要</span></div>
    <div class="two-col" style="align-items:start">
      <table class="spec-table reveal">
        <tr><th>商号</th><td>ルーバーライン（LOUVRELINE）</td></tr>
        <tr><th>所在地</th><td>{POSTAL}<br>{ADDRESS}<span class="note">（仮）</span></td></tr>
        <tr><th>電話番号</th><td>{TEL}<span class="note">（仮）</span></td></tr>
        <tr><th>E-MAIL</th><td>{EMAIL}</td></tr>
        <tr><th>URL</th><td>https://louverline.jp/</td></tr>
        <tr><th>事業内容</th><td>可動式ルーバーの企画・開発・製造<br>駆動装置・自動制御システムの開発・設計<br>金型の設計・制作</td></tr>
        <tr><th>主要取引先</th><td>ルーバーテック株式会社</td></tr>
        <tr><th>受付時間</th><td>9:00-17:00（土・日・祝日を除く）</td></tr>
      </table>
      <div class="reveal">
        <div class="map-ph">地図（仮）：所在地確定後にGoogleマップを埋め込みます</div>
        <p class="note mt-40">※ 所在地・電話番号・設立・資本金等は確認中のため仮表示です。正式な情報をいただき次第、差し替えます。</p>
      </div>
    </div>
  </div>
</section>
""" + cta(b) + foot(b)

# ------------------------------------------------------------------
# お問い合わせ
# ------------------------------------------------------------------
def page_contact():
    b = ""
    return head("お問い合わせ｜" + SITE, b) + f"""
<section class="page-hero plain">
  <div class="inner"><span class="en">Contact</span><span class="ja">お問い合わせ</span></div>
</section>
<div class="container breadcrumb"><a href="index.html">TOP</a><span>お問い合わせ</span></div>

<section class="sec" style="padding-top:20px">
  <div class="container">
    <div class="contact-grid">
      <div class="contact-side reveal">
        <p class="lead" style="margin-bottom:24px">製品のご質問、設計・お見積りのご相談、既設ルーバーの自動制御化、CADデータ・カタログのご請求など、お気軽にお問い合わせください。通常1営業日以内にご返信いたします。</p>
        <div class="box">
          <h4>お電話でのお問い合わせ</h4>
          <div class="tel">{TEL}</div>
          <p>受付時間 9:00-17:00（土・日・祝日を除く）<span class="note">　※番号は仮</span></p>
        </div>
        <div class="box">
          <h4>メールでのお問い合わせ</h4>
          <p style="font-family:var(--font-en);font-size:21.5px">{EMAIL}</p>
        </div>
        <div class="box">
          <h4>よくあるご相談</h4>
          <p>・設置費の概算を知りたい<br>・タイマー式と日射計付の違いは？<br>・手動への切り替えはできる？<br>・既設の電動ルーバーに後付けできる？<br>・事例を見学したい</p>
        </div>
      </div>
      <div class="reveal">
        <form class="form" action="#" method="post">
          <div class="row"><label>お名前<span class="req">必須</span></label><input type="text" name="name" required placeholder="例）山田 太郎"></div>
          <div class="row"><label>会社名<span class="opt">任意</span></label><input type="text" name="company" placeholder="例）株式会社○○建築設計"></div>
          <div class="row"><label>電話番号<span class="opt">任意</span></label><input type="tel" name="tel" placeholder="例）053-000-0000"></div>
          <div class="row"><label>Email<span class="req">必須</span></label><input type="email" name="email" required placeholder="例）info@example.com"></div>
          <div class="row"><label>住所<span class="opt">任意</span></label><input type="text" name="address" placeholder="例）静岡県浜松市○○区○○町1-2-3"></div>
          <div class="row"><label>お問い合わせ種別<span class="req">必須</span></label>
            <select name="type" required>
              <option value="">選択してください</option>
              <option>製品についての質問</option>
              <option>設計・お見積りの相談</option>
              <option>既設ルーバーの自動制御化</option>
              <option>CADデータ・カタログ請求</option>
              <option>事例見学の希望</option>
              <option>その他</option>
            </select></div>
          <div class="row"><label>メッセージ<span class="req">必須</span></label><textarea name="message" required placeholder="建物の用途、開口部の大きさ（W×H）、縦型／横型、電動／自動制御のご希望などをご記入いただくとスムーズです。"></textarea></div>
          <div class="row"><label>当社を知ったきっかけ<span class="opt">任意</span></label>
            <div class="checks">
              <label><input type="checkbox" name="src" value="検索"> 検索</label>
              <label><input type="checkbox" name="src" value="ルーバーテック"> ルーバーテック</label>
              <label><input type="checkbox" name="src" value="建材ナビ"> 建材ナビ</label>
              <label><input type="checkbox" name="src" value="展示会"> 展示会</label>
              <label><input type="checkbox" name="src" value="雑誌"> 雑誌・記事</label>
              <label><input type="checkbox" name="src" value="紹介"> 紹介</label>
            </div></div>
          <div class="agree"><input type="checkbox" required id="agree"><label for="agree" style="margin:0;font-weight:400">プライバシーポリシーに同意する</label></div>
          <div class="submit"><button type="submit" class="btn btn-teal">送信する</button></div>
          <p class="privacy">※ デモサイトのため、送信してもメールは送られません。本番では送信先メールアドレスを設定します。</p>
        </form>
        <div class="form-done">
          <h3>お問い合わせを受け付けました</h3>
          <p>ご入力ありがとうございます。担当者より1営業日以内にご連絡いたします。<br><span class="note">（デモ表示です）</span></p>
        </div>
      </div>
    </div>
  </div>
</section>
""" + foot(b)

# ------------------------------------------------------------------
# 出力
# ------------------------------------------------------------------
def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with io.open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("wrote", path)

if __name__ == "__main__":
    write("index.html", page_index())
    write("products.html", page_products())
    write("cases.html", page_cases())
    write("company.html", page_company())
    write("contact.html", page_contact())
    for i, c in enumerate(CASES):
        prev = CASES[i - 1]
        nxt = CASES[(i + 1) % len(CASES)]
        write(f"cases/{c['slug']}.html", page_case(c, prev, nxt))
