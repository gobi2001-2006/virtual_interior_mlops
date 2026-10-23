"""
Script to generate architectural SVG illustrations for the complete furniture catalogue (54 items).
Outputs to backend/app/static/furniture, frontend/public/furniture, and frontend/public/static/furniture.
"""

import os

SVG_ITEMS = {
    # ----------------- Existing 18 Items -----------------
    "sofa_nordic_3seater.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_sofa1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F5F7F5" />
      <stop offset="100%" stop-color="#E4EAE4" />
    </linearGradient>
    <filter id="shadow_sofa1" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_sofa1)" rx="16" />
  <ellipse cx="200" cy="245" rx="140" ry="16" fill="rgba(0,0,0,0.07)" />
  <g filter="url(#shadow_sofa1)">
    <polygon points="90,210 98,245 106,245 98,210" fill="#8B5A2B" />
    <polygon points="120,210 124,242 130,242 126,210" fill="#654321" />
    <polygon points="302,210 294,245 286,245 294,210" fill="#8B5A2B" />
    <polygon points="274,210 270,242 264,242 268,210" fill="#654321" />
    <rect x="75" y="90" width="250" height="95" rx="18" fill="#586A5B" />
    <rect x="85" y="95" width="72" height="75" rx="12" fill="#6B7C6E" />
    <rect x="164" y="95" width="72" height="75" rx="12" fill="#6B7C6E" />
    <rect x="243" y="95" width="72" height="75" rx="12" fill="#6B7C6E" />
    <rect x="70" y="165" width="260" height="52" rx="14" fill="#637466" />
    <line x1="156" y1="168" x2="156" y2="214" stroke="#4D5C50" stroke-width="2.5" />
    <line x1="244" y1="168" x2="244" y2="214" stroke="#4D5C50" stroke-width="2.5" />
    <rect x="62" y="135" width="24" height="75" rx="10" fill="#546557" />
    <rect x="314" y="135" width="24" height="75" rx="10" fill="#546557" />
    <rect x="86" y="150" width="34" height="34" rx="6" transform="rotate(-8 103 167)" fill="#D8CFBC" />
    <rect x="280" y="150" width="34" height="34" rx="6" transform="rotate(8 297 167)" fill="#C5BAA8" />
  </g>
</svg>""",

    "sofa_minimalist_loveseat.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_love" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FBFBF9" />
      <stop offset="100%" stop-color="#EFEFEA" />
    </linearGradient>
    <filter id="shadow_love" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_love)" rx="16" />
  <ellipse cx="200" cy="240" rx="110" ry="14" fill="rgba(0,0,0,0.06)" />
  <g filter="url(#shadow_love)">
    <rect x="110" y="210" width="6" height="32" rx="3" fill="#2E342F" />
    <rect x="284" y="210" width="6" height="32" rx="3" fill="#2E342F" />
    <rect x="95" y="105" width="210" height="90" rx="16" fill="#7D8D79" />
    <rect x="90" y="170" width="220" height="46" rx="12" fill="#8A9A86" />
    <line x1="200" y1="172" x2="200" y2="214" stroke="#687764" stroke-width="2" />
    <rect x="85" y="145" width="22" height="66" rx="9" fill="#758571" />
    <rect x="293" y="145" width="22" height="66" rx="9" fill="#758571" />
    <rect x="180" y="155" width="40" height="20" rx="10" fill="#EAE5DC" />
  </g>
</svg>""",

    "armchair_lounge_accent.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_arm" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FAF7F2" />
      <stop offset="100%" stop-color="#EFE8DE" />
    </linearGradient>
    <filter id="shadow_arm" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_arm)" rx="16" />
  <ellipse cx="200" cy="245" rx="80" ry="14" fill="rgba(0,0,0,0.08)" />
  <g filter="url(#shadow_arm)">
    <polygon points="140,215 130,248 136,248 144,215" fill="#D4AF37" />
    <polygon points="260,215 270,248 264,248 256,215" fill="#D4AF37" />
    <rect x="135" y="80" width="130" height="110" rx="28" fill="#B88E75" />
    <rect x="125" y="165" width="150" height="52" rx="16" fill="#C99F86" />
    <rect x="115" y="130" width="26" height="75" rx="12" fill="#AA826A" />
    <rect x="259" y="130" width="26" height="75" rx="12" fill="#AA826A" />
  </g>
</svg>""",

    "bed_platform_queen.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_bedq" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8F7F4" />
      <stop offset="100%" stop-color="#EDE9DF" />
    </linearGradient>
    <filter id="shadow_bedq" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_bedq)" rx="16" />
  <ellipse cx="200" cy="250" rx="145" ry="16" fill="rgba(0,0,0,0.08)" />
  <g filter="url(#shadow_bedq)">
    <rect x="80" y="65" width="240" height="100" rx="12" fill="#C5BAA8" />
    <line x1="160" y1="70" x2="160" y2="155" stroke="#A89E8D" stroke-width="2" stroke-dasharray="4 4" />
    <line x1="240" y1="70" x2="240" y2="155" stroke="#A89E8D" stroke-width="2" stroke-dasharray="4 4" />
    <rect x="70" y="195" width="260" height="42" rx="8" fill="#8B5A2B" />
    <rect x="85" y="145" width="230" height="60" rx="10" fill="#FFFFFF" stroke="#E2DCD2" stroke-width="2" />
    <rect x="100" y="115" width="85" height="45" rx="8" fill="#F4EFE6" stroke="#D3CBC0" stroke-width="1.5" />
    <rect x="215" y="115" width="85" height="45" rx="8" fill="#F4EFE6" stroke="#D3CBC0" stroke-width="1.5" />
    <rect x="85" y="165" width="230" height="48" rx="8" fill="#D8CFBC" />
    <rect x="85" y="195" width="230" height="22" rx="4" fill="#6B7C6E" opacity="0.85" />
  </g>
</svg>""",

    "bed_scandinavian_king.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_bedk" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FAF9F6" />
      <stop offset="100%" stop-color="#EAE6DC" />
    </linearGradient>
    <filter id="shadow_bedk" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_bedk)" rx="16" />
  <ellipse cx="200" cy="252" rx="150" ry="16" fill="rgba(0,0,0,0.08)" />
  <g filter="url(#shadow_bedk)">
    <rect x="70" y="60" width="260" height="15" rx="4" fill="#A89178" />
    <rect x="80" y="75" width="12" height="90" fill="#A89178" />
    <rect x="110" y="75" width="12" height="90" fill="#A89178" />
    <rect x="140" y="75" width="12" height="90" fill="#A89178" />
    <rect x="170" y="75" width="12" height="90" fill="#A89178" />
    <rect x="200" y="75" width="12" height="90" fill="#A89178" />
    <rect x="230" y="75" width="12" height="90" fill="#A89178" />
    <rect x="260" y="75" width="12" height="90" fill="#A89178" />
    <rect x="290" y="75" width="12" height="90" fill="#A89178" />
    <rect x="310" y="75" width="12" height="90" fill="#A89178" />
    <rect x="65" y="200" width="270" height="38" rx="6" fill="#BFA993" />
    <rect x="75" y="145" width="250" height="65" rx="8" fill="#F8F8F8" stroke="#DDD6C9" stroke-width="1.5" />
    <rect x="90" y="120" width="95" height="42" rx="6" fill="#FFFFFF" stroke="#DDD" stroke-width="1" />
    <rect x="215" y="120" width="95" height="42" rx="6" fill="#FFFFFF" stroke="#DDD" stroke-width="1" />
    <rect x="75" y="165" width="250" height="52" rx="6" fill="#C5BAA8" />
  </g>
</svg>""",

    "table_solid_wood_dining.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_tbl_din" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FBF9F5" />
      <stop offset="100%" stop-color="#EFE7DA" />
    </linearGradient>
    <filter id="shadow_tbl_din" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_tbl_din)" rx="16" />
  <ellipse cx="200" cy="250" rx="130" ry="14" fill="rgba(0,0,0,0.07)" />
  <g filter="url(#shadow_tbl_din)">
    <rect x="110" y="90" width="36" height="50" rx="4" fill="#A5836A" opacity="0.6" />
    <rect x="182" y="90" width="36" height="50" rx="4" fill="#A5836A" opacity="0.6" />
    <rect x="254" y="90" width="36" height="50" rx="4" fill="#A5836A" opacity="0.6" />
    <polygon points="95,150 90,248 100,248 105,150" fill="#5A3E2A" />
    <polygon points="120,150 115,242 123,242 128,150" fill="#422C1D" />
    <polygon points="305,150 310,248 300,248 295,150" fill="#5A3E2A" />
    <polygon points="280,150 285,242 277,242 272,150" fill="#422C1D" />
    <rect x="70" y="135" width="260" height="22" rx="6" fill="#7A583E" />
    <rect x="75" y="137" width="250" height="5" fill="#8C6649" opacity="0.6" />
    <rect x="160" y="134" width="80" height="4" fill="#DDD5C7" />
    <circle cx="200" cy="125" r="8" fill="#43A047" />
    <rect x="198" y="128" width="4" height="6" fill="#A1887F" />
  </g>
</svg>""",

    "table_round_glass_coffee.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_coff" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FAFA" />
      <stop offset="100%" stop-color="#E8ECEC" />
    </linearGradient>
    <filter id="shadow_coff" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_coff)" rx="16" />
  <ellipse cx="200" cy="242" rx="100" ry="14" fill="rgba(0,0,0,0.07)" />
  <g filter="url(#shadow_coff)">
    <line x1="200" y1="160" x2="140" y2="240" stroke="#2E3630" stroke-width="7" stroke-linecap="round" />
    <line x1="200" y1="160" x2="260" y2="240" stroke="#2E3630" stroke-width="7" stroke-linecap="round" />
    <line x1="200" y1="160" x2="200" y2="244" stroke="#1E2320" stroke-width="7" stroke-linecap="round" />
    <ellipse cx="200" cy="160" rx="115" ry="32" fill="rgba(190, 220, 230, 0.45)" stroke="#78909C" stroke-width="3" />
    <ellipse cx="195" cy="158" rx="90" ry="22" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.6" />
    <rect x="175" y="148" width="35" height="8" rx="2" fill="#D8CFBC" />
    <rect x="178" y="144" width="30" height="5" rx="1.5" fill="#6B7C6E" />
    <circle cx="225" cy="155" r="9" fill="#B88E75" />
  </g>
</svg>""",

    "table_minimalist_nightstand.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_nt" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FAF9F7" />
      <stop offset="100%" stop-color="#ECE7DD" />
    </linearGradient>
    <filter id="shadow_nt" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_nt)" rx="16" />
  <ellipse cx="200" cy="245" rx="75" ry="12" fill="rgba(0,0,0,0.06)" />
  <g filter="url(#shadow_nt)">
    <polygon points="145,185 138,245 144,245 150,185" fill="#A88B74" />
    <polygon points="255,185 262,245 256,245 250,185" fill="#A88B74" />
    <rect x="135" y="105" width="130" height="85" rx="8" fill="#DDD5C7" />
    <rect x="142" y="112" width="116" height="36" rx="4" fill="#EDE7DD" stroke="#C8BFB0" stroke-width="1.5" />
    <circle cx="200" cy="130" r="3.5" fill="#555" />
    <rect x="142" y="154" width="116" height="28" rx="4" fill="#C5BCAE" />
    <rect x="195" y="94" width="10" height="11" rx="2" fill="#FFFFFF" />
    <circle cx="200" cy="88" r="7" fill="#43A047" />
  </g>
</svg>""",

    "desk_executive_standing.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_desk1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F7F8F7" />
      <stop offset="100%" stop-color="#E5E8E5" />
    </linearGradient>
    <filter id="shadow_desk1" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_desk1)" rx="16" />
  <ellipse cx="200" cy="248" rx="125" ry="14" fill="rgba(0,0,0,0.07)" />
  <g filter="url(#shadow_desk1)">
    <rect x="110" y="145" width="10" height="95" fill="#434B45" />
    <rect x="95" y="238" width="40" height="7" rx="3" fill="#303732" />
    <rect x="280" y="145" width="10" height="95" fill="#434B45" />
    <rect x="265" y="238" width="40" height="7" rx="3" fill="#303732" />
    <rect x="120" y="180" width="160" height="6" fill="#383F3A" />
    <rect x="75" y="130" width="250" height="18" rx="5" fill="#7A583E" />
    <rect x="175" y="105" width="50" height="24" rx="3" fill="#CFD8DC" stroke="#90A4AE" stroke-width="1.5" />
    <polygon points="170,129 230,129 225,131 175,131" fill="#78909C" />
  </g>
</svg>""",

    "chair_ergonomic_task.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_chair1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8F8F8" />
      <stop offset="100%" stop-color="#E8E8E8" />
    </linearGradient>
    <filter id="shadow_chair1" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_chair1)" rx="16" />
  <ellipse cx="200" cy="250" rx="60" ry="12" fill="rgba(0,0,0,0.08)" />
  <g filter="url(#shadow_chair1)">
    <rect x="196" y="205" width="8" height="35" fill="#252B26" />
    <line x1="200" y1="238" x2="160" y2="248" stroke="#252B26" stroke-width="5" stroke-linecap="round" />
    <line x1="200" y1="238" x2="240" y2="248" stroke="#252B26" stroke-width="5" stroke-linecap="round" />
    <line x1="200" y1="238" x2="180" y2="252" stroke="#252B26" stroke-width="5" stroke-linecap="round" />
    <line x1="200" y1="238" x2="220" y2="252" stroke="#252B26" stroke-width="5" stroke-linecap="round" />
    <rect x="155" y="165" width="90" height="25" rx="8" fill="#303732" />
    <path d="M150,165 L150,145 L165,145" fill="none" stroke="#252B26" stroke-width="5" stroke-linecap="round" />
    <path d="M250,165 L250,145 L235,145" fill="none" stroke="#252B26" stroke-width="5" stroke-linecap="round" />
    <rect x="162" y="75" width="76" height="90" rx="16" fill="#252B26" />
    <rect x="167" y="80" width="66" height="80" rx="12" fill="#3B443D" stroke="#525E55" stroke-width="1.5" />
    <rect x="175" y="55" width="50" height="18" rx="6" fill="#252B26" />
  </g>
</svg>""",

    "storage_sliding_wardrobe.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_ward" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FAF9F6" />
      <stop offset="100%" stop-color="#EBE7DE" />
    </linearGradient>
    <filter id="shadow_ward" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_ward)" rx="16" />
  <ellipse cx="200" cy="252" rx="100" ry="14" fill="rgba(0,0,0,0.08)" />
  <g filter="url(#shadow_ward)">
    <rect x="120" y="50" width="160" height="195" rx="6" fill="#EDE8DE" stroke="#C5BCAE" stroke-width="2" />
    <rect x="126" y="56" width="72" height="183" rx="4" fill="#F8F6F0" />
    <rect x="192" y="130" width="4" height="35" rx="2" fill="#A89E8D" />
    <rect x="202" y="56" width="72" height="183" rx="4" fill="#DFE6E8" stroke="#C5CED1" stroke-width="1.5" />
    <line x1="215" y1="70" x2="260" y2="190" stroke="#FFFFFF" stroke-width="3" opacity="0.4" />
    <rect x="204" y="130" width="4" height="35" rx="2" fill="#78888D" />
  </g>
</svg>""",

    "storage_media_console_tv.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_tv" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FAF8F5" />
      <stop offset="100%" stop-color="#EAE3D5" />
    </linearGradient>
    <filter id="shadow_tv" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_tv)" rx="16" />
  <ellipse cx="200" cy="245" rx="135" ry="14" fill="rgba(0,0,0,0.07)" />
  <g filter="url(#shadow_tv)">
    <polygon points="100,205 92,242 100,242 108,205" fill="#5C4033" />
    <polygon points="300,205 308,242 300,242 292,205" fill="#5C4033" />
    <rect x="80" y="145" width="240" height="62" rx="8" fill="#9E8B75" />
    <rect x="86" y="151" width="70" height="50" rx="4" fill="#B3A28D" />
    <line x1="98" y1="151" x2="98" y2="201" stroke="#8A7761" stroke-width="2" />
    <line x1="110" y1="151" x2="110" y2="201" stroke="#8A7761" stroke-width="2" />
    <line x1="122" y1="151" x2="122" y2="201" stroke="#8A7761" stroke-width="2" />
    <line x1="134" y1="151" x2="134" y2="201" stroke="#8A7761" stroke-width="2" />
    <line x1="146" y1="151" x2="146" y2="201" stroke="#8A7761" stroke-width="2" />
    <rect x="162" y="151" width="76" height="50" rx="4" fill="#524334" />
    <rect x="166" y="180" width="68" height="15" rx="2" fill="#2E241B" />
    <rect x="244" y="151" width="70" height="50" rx="4" fill="#B3A28D" />
    <line x1="256" y1="151" x2="256" y2="201" stroke="#8A7761" stroke-width="2" />
    <line x1="268" y1="151" x2="268" y2="201" stroke="#8A7761" stroke-width="2" />
    <line x1="280" y1="151" x2="280" y2="201" stroke="#8A7761" stroke-width="2" />
    <line x1="292" y1="151" x2="292" y2="201" stroke="#8A7761" stroke-width="2" />
    <line x1="304" y1="151" x2="304" y2="201" stroke="#8A7761" stroke-width="2" />
    <rect x="125" y="70" width="150" height="70" rx="4" fill="#212121" stroke="#424242" stroke-width="2" />
    <rect x="195" y="140" width="10" height="6" fill="#424242" />
  </g>
</svg>""",

    "storage_architectural_bookshelf.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_book" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F9F9F8" />
      <stop offset="100%" stop-color="#EAE9E5" />
    </linearGradient>
    <filter id="shadow_book" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_book)" rx="16" />
  <ellipse cx="200" cy="252" rx="90" ry="12" fill="rgba(0,0,0,0.07)" />
  <g filter="url(#shadow_book)">
    <rect x="135" y="45" width="6" height="200" fill="#383E3A" />
    <rect x="259" y="45" width="6" height="200" fill="#383E3A" />
    <rect x="130" y="55" width="140" height="8" rx="2" fill="#BFA993" />
    <rect x="130" y="98" width="140" height="8" rx="2" fill="#BFA993" />
    <rect x="130" y="141" width="140" height="8" rx="2" fill="#BFA993" />
    <rect x="130" y="184" width="140" height="8" rx="2" fill="#BFA993" />
    <rect x="130" y="227" width="140" height="8" rx="2" fill="#BFA993" />
    <rect x="145" y="70" width="8" height="28" fill="#6B7C6E" />
    <rect x="154" y="65" width="10" height="33" fill="#B88E75" />
    <rect x="165" y="68" width="7" height="30" fill="#3E6B48" />
    <circle cx="190" cy="126" r="12" fill="#D8CFBC" />
    <ellipse cx="220" cy="128" rx="8" ry="12" fill="#A89E8D" />
    <rect x="215" y="156" width="10" height="28" fill="#586A5B" />
    <rect x="226" y="152" width="12" height="32" fill="#A08068" />
    <rect x="239" y="158" width="8" height="26" fill="#DDD5C7" />
  </g>
</svg>""",

    "lamp_arc_brass_floor.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_lamp" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FBFBF9" />
      <stop offset="100%" stop-color="#EFEFE8" />
    </linearGradient>
    <filter id="shadow_lamp" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12" />
    </filter>
    <radialGradient id="lampGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFE082" stop-opacity="0.4" />
      <stop offset="100%" stop-color="#FFE082" stop-opacity="0" />
    </radialGradient>
  </defs>
  <rect width="400" height="300" fill="url(#bg_lamp)" rx="16" />
  <ellipse cx="230" cy="245" rx="50" ry="10" fill="rgba(0,0,0,0.06)" />
  <circle cx="150" cy="165" r="55" fill="url(#lampGlow)" />
  <g filter="url(#shadow_lamp)">
    <ellipse cx="240" cy="240" rx="36" ry="10" fill="#D4AF37" stroke="#AA8C2C" stroke-width="1.5" />
    <path d="M240,238 C240,110 230,55 150,65" fill="none" stroke="#D4AF37" stroke-width="5" stroke-linecap="round" />
    <line x1="150" y1="65" x2="150" y2="95" stroke="#D4AF37" stroke-width="2.5" />
    <path d="M125,120 C125,95 175,95 175,120 Z" fill="#FDFBF7" stroke="#D4AF37" stroke-width="2" />
  </g>
</svg>""",

    "plant_fiddle_leaf_fig.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_plant" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FAF8" />
      <stop offset="100%" stop-color="#E7EFE7" />
    </linearGradient>
    <filter id="shadow_plant" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_plant)" rx="16" />
  <ellipse cx="200" cy="248" rx="45" ry="10" fill="rgba(0,0,0,0.07)" />
  <g filter="url(#shadow_plant)">
    <polygon points="175,185 225,185 218,242 182,242" fill="#FFFFFF" stroke="#E0E0E0" stroke-width="2" />
    <ellipse cx="200" cy="186" rx="24" ry="5" fill="#4E342E" />
    <path d="M200,186 Q195,120 185,60" fill="none" stroke="#5D4037" stroke-width="5" stroke-linecap="round" />
    <path d="M198,150 Q215,110 220,75" fill="none" stroke="#5D4037" stroke-width="4" stroke-linecap="round" />
    <ellipse cx="170" cy="70" rx="28" ry="16" transform="rotate(-25 170 70)" fill="#2E7D32" />
    <ellipse cx="225" cy="80" rx="26" ry="15" transform="rotate(25 225 80)" fill="#388E3C" />
    <ellipse cx="165" cy="115" rx="30" ry="18" transform="rotate(-30 165 115)" fill="#388E3C" />
    <ellipse cx="230" cy="120" rx="28" ry="16" transform="rotate(30 230 120)" fill="#43A047" />
    <ellipse cx="175" cy="155" rx="26" ry="16" transform="rotate(-20 175 155)" fill="#4CAF50" />
    <ellipse cx="220" cy="158" rx="25" ry="15" transform="rotate(20 220 158)" fill="#2E7D32" />
  </g>
</svg>""",

    "rug_wool_geometric.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_rug" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FBFBF9" />
      <stop offset="100%" stop-color="#ECEBE3" />
    </linearGradient>
    <filter id="shadow_rug" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="8" stdDeviation="6" flood-opacity="0.08" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_rug)" rx="16" />
  <g filter="url(#shadow_rug)">
    <polygon points="200,60 350,150 200,240 50,150" fill="#E3DCCF" stroke="#FFFFFF" stroke-width="3" />
    <line x1="50" y1="150" x2="200" y2="60" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="3 3" />
    <line x1="200" y1="240" x2="350" y2="150" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="3 3" />
    <polygon points="200,95 295,150 200,205 105,150" fill="#D6CEBF" />
    <line x1="105" y1="150" x2="295" y2="150" stroke="#B88E75" stroke-width="2.5" />
    <line x1="200" y1="95" x2="200" y2="205" stroke="#6B7C6E" stroke-width="2.5" />
    <circle cx="200" cy="150" r="18" fill="none" stroke="#586A5B" stroke-width="2" />
  </g>
</svg>""",

    "vanity_floating_bathroom.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_van1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F5F9FA" />
      <stop offset="100%" stop-color="#E2EDF0" />
    </linearGradient>
    <filter id="shadow_van1" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_van1)" rx="16" />
  <ellipse cx="200" cy="245" rx="90" ry="12" fill="rgba(0,0,0,0.06)" />
  <g filter="url(#shadow_van1)">
    <rect x="150" y="45" width="100" height="75" rx="50" fill="#E8F4F8" stroke="#B0BEC5" stroke-width="2.5" />
    <line x1="165" y1="58" x2="185" y2="82" stroke="#FFFFFF" stroke-width="2.5" opacity="0.6" />
    <ellipse cx="200" cy="148" rx="42" ry="16" fill="#FFFFFF" stroke="#CFD8DC" stroke-width="2" />
    <path d="M200,140 L200,118 Q200,110 192,112 L185,115" fill="none" stroke="#78909C" stroke-width="3.5" stroke-linecap="round" />
    <rect x="100" y="155" width="200" height="58" rx="8" fill="#8D6E63" />
    <line x1="200" y1="158" x2="200" y2="210" stroke="#6D4C41" stroke-width="2" />
    <rect x="130" y="180" width="40" height="4" rx="2" fill="#4E342E" />
    <rect x="230" y="180" width="40" height="4" rx="2" fill="#4E342E" />
  </g>
</svg>""",

    "island_kitchen_prep_cart.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_kcart" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FAFBFB" />
      <stop offset="100%" stop-color="#E8ECEE" />
    </linearGradient>
    <filter id="shadow_kcart" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12" />
    </filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_kcart)" rx="16" />
  <ellipse cx="200" cy="250" rx="110" ry="14" fill="rgba(0,0,0,0.07)" />
  <g filter="url(#shadow_kcart)">
    <rect x="105" y="125" width="8" height="110" fill="#90A4AE" />
    <rect x="287" y="125" width="8" height="110" fill="#90A4AE" />
    <circle cx="109" cy="242" r="6" fill="#37474F" />
    <circle cx="291" cy="242" r="6" fill="#37474F" />
    <rect x="100" y="195" width="200" height="8" rx="2" fill="#B0BEC5" />
    <rect x="85" y="112" width="230" height="22" rx="5" fill="#D7CCC8" stroke="#A1887F" stroke-width="1.5" />
    <rect x="100" y="134" width="200" height="32" rx="4" fill="#CFD8DC" />
    <rect x="110" y="140" width="85" height="20" rx="3" fill="#ECEFF1" />
    <rect x="205" y="140" width="85" height="20" rx="3" fill="#ECEFF1" />
    <rect x="140" y="148" width="25" height="3" rx="1.5" fill="#78909C" />
    <rect x="235" y="148" width="25" height="3" rx="1.5" fill="#78909C" />
    <rect x="75" y="120" width="10" height="2" fill="#78909C" />
    <rect x="73" y="120" width="4" height="25" rx="2" fill="#78909C" />
  </g>
</svg>""",

    # ----------------- New 36 Items (Expanded Catalogue) -----------------
    # Bedroom
    "bed_single_platform.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_sbed" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F9F8F6"/><stop offset="100%" stop-color="#ECE7DD"/></linearGradient>
    <filter id="sh_sbed"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_sbed)" rx="16"/>
  <ellipse cx="200" cy="245" rx="110" ry="12" fill="rgba(0,0,0,0.08)"/>
  <g filter="url(#sh_sbed)">
    <rect x="120" y="80" width="160" height="85" rx="8" fill="#B39274"/>
    <rect x="110" y="185" width="180" height="45" rx="6" fill="#8C6D52"/>
    <rect x="125" y="195" width="70" height="26" rx="4" fill="#A48366"/>
    <rect x="205" y="195" width="70" height="26" rx="4" fill="#A48366"/>
    <rect x="120" y="135" width="160" height="60" rx="8" fill="#FFFFFF" stroke="#DDD" stroke-width="1.5"/>
    <rect x="140" y="110" width="120" height="40" rx="6" fill="#F4EFE6"/>
    <rect x="120" y="155" width="160" height="45" rx="6" fill="#7B8B7B"/>
  </g>
</svg>""",

    "bedroom_chest_drawers.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_chest" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FAF9F6"/><stop offset="100%" stop-color="#ECE5D8"/></linearGradient>
    <filter id="sh_chest"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_chest)" rx="16"/>
  <ellipse cx="200" cy="252" rx="90" ry="12" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_chest)">
    <polygon points="125,225 120,248 128,248 132,225" fill="#5C4033"/>
    <polygon points="275,225 280,248 272,248 268,225" fill="#5C4033"/>
    <rect x="115" y="70" width="170" height="160" rx="6" fill="#A88B74"/>
    <rect x="123" y="78" width="154" height="40" rx="4" fill="#C5A88F"/>
    <rect x="123" y="126" width="154" height="40" rx="4" fill="#C5A88F"/>
    <rect x="123" y="174" width="154" height="40" rx="4" fill="#C5A88F"/>
    <line x1="200" y1="78" x2="200" y2="214" stroke="#8A6E58" stroke-width="2"/>
    <rect x="150" y="94" width="20" height="4" rx="2" fill="#2E241B"/>
    <rect x="230" y="94" width="20" height="4" rx="2" fill="#2E241B"/>
    <rect x="150" y="142" width="20" height="4" rx="2" fill="#2E241B"/>
    <rect x="230" y="142" width="20" height="4" rx="2" fill="#2E241B"/>
    <rect x="150" y="190" width="20" height="4" rx="2" fill="#2E241B"/>
    <rect x="230" y="190" width="20" height="4" rx="2" fill="#2E241B"/>
  </g>
</svg>""",

    "bedroom_dressing_table.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_dress" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FBF9F8"/><stop offset="100%" stop-color="#EFE8E2"/></linearGradient>
    <filter id="sh_dress"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_dress)" rx="16"/>
  <ellipse cx="200" cy="250" rx="100" ry="12" fill="rgba(0,0,0,0.06)"/>
  <g filter="url(#sh_dress)">
    <circle cx="200" cy="100" r="45" fill="#E8F4F8" stroke="#D4AF37" stroke-width="3"/>
    <line x1="175" y1="80" x2="195" y2="110" stroke="#FFF" stroke-width="2" opacity="0.6"/>
    <rect x="110" y="150" width="180" height="20" rx="4" fill="#B38B6D"/>
    <rect x="120" y="170" width="160" height="25" rx="3" fill="#9C7356"/>
    <line x1="125" y1="195" x2="120" y2="245" stroke="#5C4033" stroke-width="5" stroke-linecap="round"/>
    <line x1="275" y1="195" x2="280" y2="245" stroke="#5C4033" stroke-width="5" stroke-linecap="round"/>
    <rect x="175" y="210" width="50" height="35" rx="4" fill="#C5A88F"/>
    <rect x="170" y="205" width="60" height="10" rx="3" fill="#D8CFBC"/>
  </g>
</svg>""",

    "bedroom_end_bench.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_ben" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FAF9F7"/><stop offset="100%" stop-color="#EAE5DC"/></linearGradient>
    <filter id="sh_ben"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_ben)" rx="16"/>
  <ellipse cx="200" cy="245" rx="115" ry="12" fill="rgba(0,0,0,0.06)"/>
  <g filter="url(#sh_ben)">
    <polygon points="105,190 98,242 106,242 112,190" fill="#6B4E3D"/>
    <polygon points="295,190 302,242 294,242 288,190" fill="#6B4E3D"/>
    <rect x="90" y="175" width="220" height="20" rx="4" fill="#8B6B55"/>
    <rect x="85" y="145" width="230" height="35" rx="10" fill="#C8B89E"/>
    <line x1="140" y1="145" x2="140" y2="180" stroke="#B09F85" stroke-width="1.5" stroke-dasharray="3 3"/>
    <line x1="200" y1="145" x2="200" y2="180" stroke="#B09F85" stroke-width="1.5" stroke-dasharray="3 3"/>
    <line x1="260" y1="145" x2="260" y2="180" stroke="#B09F85" stroke-width="1.5" stroke-dasharray="3 3"/>
  </g>
</svg>""",

    "bedroom_bedside_lamp.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_blamp" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FBFBF9"/><stop offset="100%" stop-color="#EFEFE8"/></linearGradient>
    <filter id="sh_blamp"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
    <radialGradient id="glow_blamp" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FFE082" stop-opacity="0.45"/><stop offset="100%" stop-color="#FFE082" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="400" height="300" fill="url(#bg_blamp)" rx="16"/>
  <circle cx="200" cy="140" r="70" fill="url(#glow_blamp)"/>
  <ellipse cx="200" cy="242" rx="45" ry="8" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_blamp)">
    <ellipse cx="200" cy="235" rx="30" ry="7" fill="#8D6E63"/>
    <rect x="197" y="150" width="6" height="85" fill="#D4AF37"/>
    <polygon points="170,150 230,150 245,100 155,100" fill="#FBF9F5" stroke="#E0D7C6" stroke-width="2"/>
    <circle cx="200" cy="98" r="4" fill="#D4AF37"/>
  </g>
</svg>""",

    # Living Room
    "sofa_sectional_lshape.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_sec" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F7F8F7"/><stop offset="100%" stop-color="#E6ECE6"/></linearGradient>
    <filter id="sh_sec"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_sec)" rx="16"/>
  <ellipse cx="200" cy="245" rx="145" ry="16" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_sec)">
    <rect x="70" y="100" width="260" height="80" rx="14" fill="#4A584D"/>
    <rect x="70" y="160" width="180" height="50" rx="10" fill="#5D6E60"/>
    <rect x="230" y="150" width="100" height="75" rx="12" fill="#5D6E60"/>
    <rect x="58" y="140" width="20" height="70" rx="8" fill="#3E4A40"/>
    <rect x="322" y="140" width="20" height="85" rx="8" fill="#3E4A40"/>
    <rect x="85" y="155" width="30" height="30" rx="6" transform="rotate(-10 100 170)" fill="#D8CFBC"/>
    <rect x="260" y="160" width="30" height="30" rx="6" transform="rotate(8 275 175)" fill="#B88E75"/>
  </g>
</svg>""",

    "living_side_table_ceramic.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_cside" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F9F9F8"/><stop offset="100%" stop-color="#EBEAE6"/></linearGradient>
    <filter id="sh_cside"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_cside)" rx="16"/>
  <ellipse cx="200" cy="242" rx="65" ry="10" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_cside)">
    <path d="M150,140 Q180,185 160,230 L240,230 Q220,185 250,140 Z" fill="#D3CBC0"/>
    <ellipse cx="200" cy="140" rx="55" ry="16" fill="#EDE7DD" stroke="#C5BCAE" stroke-width="2"/>
    <ellipse cx="200" cy="138" rx="20" ry="6" fill="#9E8B75" opacity="0.6"/>
  </g>
</svg>""",

    "living_media_credenza.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_cred" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FAF8F5"/><stop offset="100%" stop-color="#EAE3D5"/></linearGradient>
    <filter id="sh_cred"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_cred)" rx="16"/>
  <ellipse cx="200" cy="245" rx="130" ry="12" fill="rgba(0,0,0,0.06)"/>
  <g filter="url(#sh_cred)">
    <rect x="95" y="210" width="8" height="30" fill="#2E241B"/>
    <rect x="297" y="210" width="8" height="30" fill="#2E241B"/>
    <rect x="80" y="110" width="240" height="105" rx="8" fill="#7A583E"/>
    <rect x="86" y="116" width="70" height="93" rx="4" fill="#9C7356"/>
    <rect x="165" y="116" width="70" height="93" rx="4" fill="#9C7356"/>
    <rect x="244" y="116" width="70" height="93" rx="4" fill="#9C7356"/>
    <circle cx="150" cy="162" r="3" fill="#DDD"/>
    <circle cx="172" cy="162" r="3" fill="#DDD"/>
    <circle cx="308" cy="162" r="3" fill="#DDD"/>
  </g>
</svg>""",

    # Kitchen
    "kitchen_base_cabinet.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_kbase" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F8FAFA"/><stop offset="100%" stop-color="#E7ECEE"/></linearGradient>
    <filter id="sh_kbase"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_kbase)" rx="16"/>
  <ellipse cx="200" cy="250" rx="95" ry="12" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_kbase)">
    <rect x="110" y="80" width="180" height="18" rx="3" fill="#FAFAFA" stroke="#CFD8DC" stroke-width="2"/>
    <rect x="115" y="98" width="170" height="135" rx="4" fill="#455A64"/>
    <rect x="122" y="105" width="74" height="120" rx="3" fill="#546E7A"/>
    <rect x="204" y="105" width="74" height="120" rx="3" fill="#546E7A"/>
    <rect x="185" y="150" width="4" height="30" rx="2" fill="#ECEFF1"/>
    <rect x="211" y="150" width="4" height="30" rx="2" fill="#ECEFF1"/>
    <rect x="115" y="233" width="170" height="12" fill="#263238"/>
  </g>
</svg>""",

    "kitchen_wall_cabinet.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_kwall" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FAFBFB"/><stop offset="100%" stop-color="#ECEFF1"/></linearGradient>
    <filter id="sh_kwall"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_kwall)" rx="16"/>
  <g filter="url(#sh_kwall)">
    <rect x="110" y="60" width="180" height="160" rx="6" fill="#37474F"/>
    <rect x="118" y="68" width="78" height="144" rx="4" fill="#546E7A"/>
    <rect x="204" y="68" width="78" height="144" rx="4" fill="#546E7A"/>
    <rect x="124" y="74" width="66" height="132" rx="3" fill="#B0BEC5" opacity="0.4"/>
    <rect x="210" y="74" width="66" height="132" rx="3" fill="#B0BEC5" opacity="0.4"/>
    <rect x="186" y="125" width="4" height="30" rx="2" fill="#ECEFF1"/>
    <rect x="210" y="125" width="4" height="30" rx="2" fill="#ECEFF1"/>
  </g>
</svg>""",

    "kitchen_island_butcherblock.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_kisl" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FBF9F6"/><stop offset="100%" stop-color="#EBE3D5"/></linearGradient>
    <filter id="sh_kisl"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_kisl)" rx="16"/>
  <ellipse cx="200" cy="250" rx="125" ry="14" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_kisl)">
    <rect x="80" y="90" width="240" height="26" rx="6" fill="#C5A07A" stroke="#A88159" stroke-width="1.5"/>
    <line x1="120" y1="90" x2="120" y2="116" stroke="#A88159" stroke-width="1.5"/>
    <line x1="160" y1="90" x2="160" y2="116" stroke="#A88159" stroke-width="1.5"/>
    <line x1="200" y1="90" x2="200" y2="116" stroke="#A88159" stroke-width="1.5"/>
    <line x1="240" y1="90" x2="240" y2="116" stroke="#A88159" stroke-width="1.5"/>
    <line x1="280" y1="90" x2="280" y2="116" stroke="#A88159" stroke-width="1.5"/>
    <rect x="95" y="116" width="210" height="115" rx="4" fill="#2E3D34"/>
    <rect x="105" y="125" width="90" height="95" rx="3" fill="#3D4F44"/>
    <rect x="205" y="125" width="90" height="95" rx="3" fill="#3D4F44"/>
    <rect x="180" y="160" width="4" height="25" rx="2" fill="#D4AF37"/>
    <rect x="216" y="160" width="4" height="25" rx="2" fill="#D4AF37"/>
    <rect x="95" y="231" width="210" height="10" fill="#1C2620"/>
  </g>
</svg>""",

    "kitchen_prep_counter.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_kprep" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F8FAFA"/><stop offset="100%" stop-color="#E8ECEC"/></linearGradient>
    <filter id="sh_kprep"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_kprep)" rx="16"/>
  <ellipse cx="200" cy="248" rx="115" ry="12" fill="rgba(0,0,0,0.06)"/>
  <g filter="url(#sh_kprep)">
    <rect x="90" y="100" width="220" height="20" rx="4" fill="#37474F" stroke="#263238" stroke-width="1.5"/>
    <rect x="100" y="120" width="200" height="110" rx="4" fill="#ECEFF1"/>
    <rect x="110" y="130" width="85" height="40" rx="3" fill="#FFFFFF" stroke="#CFD8DC" stroke-width="1.5"/>
    <rect x="205" y="130" width="85" height="40" rx="3" fill="#FFFFFF" stroke="#CFD8DC" stroke-width="1.5"/>
    <rect x="110" y="180" width="180" height="40" rx="3" fill="#FFFFFF" stroke="#CFD8DC" stroke-width="1.5"/>
    <rect x="140" y="148" width="25" height="4" rx="2" fill="#78909C"/>
    <rect x="235" y="148" width="25" height="4" rx="2" fill="#78909C"/>
    <rect x="185" y="198" width="30" height="4" rx="2" fill="#78909C"/>
  </g>
</svg>""",

    "kitchen_bar_stool.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_bstool" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FAF9F7"/><stop offset="100%" stop-color="#ECE6DC"/></linearGradient>
    <filter id="sh_bstool"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_bstool)" rx="16"/>
  <ellipse cx="200" cy="250" rx="55" ry="10" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_bstool)">
    <polygon points="175,170 160,248 168,248 180,170" fill="#2E241B"/>
    <polygon points="225,170 240,248 232,248 220,170" fill="#2E241B"/>
    <ellipse cx="200" cy="220" rx="28" ry="6" fill="none" stroke="#2E241B" stroke-width="3"/>
    <ellipse cx="200" cy="165" rx="42" ry="14" fill="#C5A07A"/>
    <path d="M165,165 Q160,110 200,110 Q240,110 235,165" fill="none" stroke="#A88159" stroke-width="8" stroke-linecap="round"/>
  </g>
</svg>""",

    "kitchen_bar_table.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_btbl" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FBFBF9"/><stop offset="100%" stop-color="#EDECE8"/></linearGradient>
    <filter id="sh_btbl"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_btbl)" rx="16"/>
  <ellipse cx="200" cy="252" rx="115" ry="12" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_btbl)">
    <line x1="120" y1="120" x2="110" y2="248" stroke="#212121" stroke-width="6" stroke-linecap="round"/>
    <line x1="280" y1="120" x2="290" y2="248" stroke="#212121" stroke-width="6" stroke-linecap="round"/>
    <line x1="115" y1="190" x2="285" y2="190" stroke="#212121" stroke-width="4"/>
    <rect x="90" y="105" width="220" height="18" rx="4" fill="#7A583E" stroke="#5C4033" stroke-width="1.5"/>
  </g>
</svg>""",

    "kitchen_pantry_cabinet.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_pant" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F8FAF8"/><stop offset="100%" stop-color="#E5ECE5"/></linearGradient>
    <filter id="sh_pant"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_pant)" rx="16"/>
  <ellipse cx="200" cy="254" rx="80" ry="12" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_pant)">
    <rect x="130" y="45" width="140" height="200" rx="6" fill="#F5F5F0" stroke="#D1D5DB" stroke-width="2"/>
    <rect x="136" y="52" width="60" height="95" rx="3" fill="#E5E7EB"/>
    <rect x="204" y="52" width="60" height="95" rx="3" fill="#E5E7EB"/>
    <rect x="136" y="152" width="128" height="25" rx="3" fill="#E5E7EB"/>
    <rect x="136" y="182" width="60" height="55" rx="3" fill="#E5E7EB"/>
    <rect x="204" y="182" width="60" height="55" rx="3" fill="#E5E7EB"/>
    <rect x="188" y="90" width="3" height="20" rx="1.5" fill="#374151"/>
    <rect x="208" y="90" width="3" height="20" rx="1.5" fill="#374151"/>
    <rect x="190" y="162" width="20" height="3" rx="1.5" fill="#374151"/>
  </g>
</svg>""",

    "kitchen_bakers_rack.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_brack" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FAFBFB"/><stop offset="100%" stop-color="#E8ECEE"/></linearGradient>
    <filter id="sh_brack"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_brack)" rx="16"/>
  <ellipse cx="200" cy="252" rx="90" ry="10" fill="rgba(0,0,0,0.06)"/>
  <g filter="url(#sh_brack)">
    <rect x="125" y="45" width="6" height="200" fill="#2E342F"/>
    <rect x="269" y="45" width="6" height="200" fill="#2E342F"/>
    <rect x="120" y="60" width="160" height="8" rx="2" fill="#D7CCC8"/>
    <rect x="120" y="100" width="160" height="8" rx="2" fill="#D7CCC8"/>
    <rect x="115" y="145" width="170" height="14" rx="3" fill="#8D6E63"/>
    <rect x="120" y="190" width="160" height="8" rx="2" fill="#CFD8DC"/>
    <rect x="120" y="225" width="160" height="8" rx="2" fill="#CFD8DC"/>
  </g>
</svg>""",

    # Dining Room
    "dining_table_2seater.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_dt2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FBF9F7"/><stop offset="100%" stop-color="#EFE8DE"/></linearGradient>
    <filter id="sh_dt2"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_dt2)" rx="16"/>
  <ellipse cx="200" cy="248" rx="75" ry="12" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_dt2)">
    <ellipse cx="200" cy="242" rx="40" ry="8" fill="#3E2723"/>
    <rect x="196" y="150" width="8" height="92" fill="#3E2723"/>
    <rect x="125" y="135" width="150" height="16" rx="4" fill="#8D6E63"/>
    <circle cx="200" cy="125" r="7" fill="#43A047"/>
  </g>
</svg>""",

    "dining_table_4seater.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_dt4" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FAF9F6"/><stop offset="100%" stop-color="#ECE5D8"/></linearGradient>
    <filter id="sh_dt4"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_dt4)" rx="16"/>
  <ellipse cx="200" cy="250" rx="110" ry="14" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_dt4)">
    <line x1="150" y1="160" x2="135" y2="245" stroke="#8D6E63" stroke-width="7" stroke-linecap="round"/>
    <line x1="250" y1="160" x2="265" y2="245" stroke="#8D6E63" stroke-width="7" stroke-linecap="round"/>
    <ellipse cx="200" cy="155" rx="110" ry="25" fill="#D7CCC8" stroke="#BCAAA4" stroke-width="2"/>
    <ellipse cx="200" cy="153" rx="90" ry="18" fill="none" stroke="#FFFFFF" stroke-width="1.5" opacity="0.6"/>
  </g>
</svg>""",

    "dining_table_8seater.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_dt8" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F8F6F0"/><stop offset="100%" stop-color="#E5DEC9"/></linearGradient>
    <filter id="sh_dt8"><feDropShadow dx="0" dy="14" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_dt8)" rx="16"/>
  <ellipse cx="200" cy="252" rx="145" ry="16" fill="rgba(0,0,0,0.08)"/>
  <g filter="url(#sh_dt8)">
    <polygon points="120,150 110,248 122,248 132,150" fill="#4E342E"/>
    <polygon points="280,150 268,248 280,248 290,150" fill="#4E342E"/>
    <line x1="120" y1="210" x2="280" y2="210" stroke="#3E2723" stroke-width="6"/>
    <rect x="60" y="135" width="280" height="24" rx="6" fill="#5D4037"/>
  </g>
</svg>""",

    "dining_chair_wood.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_dchr" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FBF9F7"/><stop offset="100%" stop-color="#EDE6DC"/></linearGradient>
    <filter id="sh_dchr"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_dchr)" rx="16"/>
  <ellipse cx="200" cy="248" rx="60" ry="10" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_dchr)">
    <line x1="160" y1="180" x2="150" y2="246" stroke="#5D4037" stroke-width="5" stroke-linecap="round"/>
    <line x1="240" y1="180" x2="250" y2="246" stroke="#5D4037" stroke-width="5" stroke-linecap="round"/>
    <rect x="150" y="170" width="100" height="16" rx="4" fill="#C5A880"/>
    <path d="M160,170 L160,85 Q200,75 240,85 L240,170" fill="none" stroke="#5D4037" stroke-width="5"/>
    <line x1="180" y1="80" x2="180" y2="170" stroke="#8D6E63" stroke-width="3"/>
    <line x1="200" y1="78" x2="200" y2="170" stroke="#8D6E63" stroke-width="3"/>
    <line x1="220" y1="80" x2="220" y2="170" stroke="#8D6E63" stroke-width="3"/>
  </g>
</svg>""",

    "dining_bench_upholstered.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_dben" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FAF9F6"/><stop offset="100%" stop-color="#E8E2D5"/></linearGradient>
    <filter id="sh_dben"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_dben)" rx="16"/>
  <ellipse cx="200" cy="246" rx="120" ry="12" fill="rgba(0,0,0,0.06)"/>
  <g filter="url(#sh_dben)">
    <line x1="105" y1="180" x2="98" y2="244" stroke="#4E342E" stroke-width="6" stroke-linecap="round"/>
    <line x1="295" y1="180" x2="302" y2="244" stroke="#4E342E" stroke-width="6" stroke-linecap="round"/>
    <rect x="90" y="170" width="220" height="15" rx="3" fill="#6D4C41"/>
    <rect x="80" y="145" width="240" height="30" rx="8" fill="#B0BEC5"/>
  </g>
</svg>""",

    "dining_sideboard_credenza.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_dside" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FAF8F5"/><stop offset="100%" stop-color="#ECE4D6"/></linearGradient>
    <filter id="sh_dside"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_dside)" rx="16"/>
  <ellipse cx="200" cy="246" rx="130" ry="12" fill="rgba(0,0,0,0.06)"/>
  <g filter="url(#sh_dside)">
    <polygon points="105,210 98,245 106,245 112,210" fill="#4E342E"/>
    <polygon points="295,210 302,245 294,245 288,210" fill="#4E342E"/>
    <rect x="80" y="105" width="240" height="110" rx="8" fill="#A1887F"/>
    <rect x="86" y="112" width="70" height="96" rx="4" fill="#BCAAA4"/>
    <rect x="165" y="112" width="70" height="96" rx="4" fill="#BCAAA4"/>
    <rect x="244" y="112" width="70" height="96" rx="4" fill="#BCAAA4"/>
    <rect x="145" y="155" width="4" height="20" rx="2" fill="#3E2723"/>
    <rect x="175" y="155" width="4" height="20" rx="2" fill="#3E2723"/>
    <rect x="255" y="155" width="4" height="20" rx="2" fill="#3E2723"/>
  </g>
</svg>""",

    "dining_display_cabinet.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_ddisp" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F9F9F8"/><stop offset="100%" stop-color="#E7E5DE"/></linearGradient>
    <filter id="sh_ddisp"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_ddisp)" rx="16"/>
  <ellipse cx="200" cy="254" rx="90" ry="12" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_ddisp)">
    <rect x="125" y="45" width="150" height="200" rx="6" fill="#3E2723"/>
    <rect x="133" y="53" width="63" height="184" rx="3" fill="#B0BEC5" opacity="0.35" stroke="#5D4037" stroke-width="2"/>
    <rect x="204" y="53" width="63" height="184" rx="3" fill="#B0BEC5" opacity="0.35" stroke="#5D4037" stroke-width="2"/>
    <line x1="133" y1="110" x2="267" y2="110" stroke="#8D6E63" stroke-width="3"/>
    <line x1="133" y1="165" x2="267" y2="165" stroke="#8D6E63" stroke-width="3"/>
    <circle cx="190" cy="140" r="3" fill="#D4AF37"/>
    <circle cx="210" cy="140" r="3" fill="#D4AF37"/>
  </g>
</svg>""",

    "dining_serving_cart.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_dcart" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FBFBF9"/><stop offset="100%" stop-color="#ECEBE3"/></linearGradient>
    <filter id="sh_dcart"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_dcart)" rx="16"/>
  <ellipse cx="200" cy="250" rx="80" ry="10" fill="rgba(0,0,0,0.06)"/>
  <g filter="url(#sh_dcart)">
    <rect x="130" y="100" width="140" height="12" rx="3" fill="#D4AF37"/>
    <rect x="130" y="180" width="140" height="12" rx="3" fill="#D4AF37"/>
    <line x1="140" y1="80" x2="140" y2="235" stroke="#AA8C2C" stroke-width="5"/>
    <line x1="260" y1="100" x2="260" y2="235" stroke="#AA8C2C" stroke-width="5"/>
    <circle cx="140" cy="242" r="8" fill="#37474F"/>
    <circle cx="260" cy="242" r="8" fill="#37474F"/>
    <path d="M125,80 L140,80" stroke="#AA8C2C" stroke-width="5" stroke-linecap="round"/>
  </g>
</svg>""",

    # Bathroom
    "bathroom_double_vanity.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_bvan2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F5F9FA"/><stop offset="100%" stop-color="#DFECEF"/></linearGradient>
    <filter id="sh_bvan2"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_bvan2)" rx="16"/>
  <ellipse cx="200" cy="248" rx="120" ry="12" fill="rgba(0,0,0,0.06)"/>
  <g filter="url(#sh_bvan2)">
    <rect x="110" y="45" width="70" height="70" rx="35" fill="#E8F4F8" stroke="#78909C" stroke-width="2"/>
    <rect x="220" y="45" width="70" height="70" rx="35" fill="#E8F4F8" stroke="#78909C" stroke-width="2"/>
    <ellipse cx="145" cy="145" rx="30" ry="12" fill="#FFF" stroke="#B0BEC5" stroke-width="1.5"/>
    <ellipse cx="255" cy="145" rx="30" ry="12" fill="#FFF" stroke="#B0BEC5" stroke-width="1.5"/>
    <rect x="80" y="150" width="240" height="65" rx="6" fill="#37474F"/>
    <line x1="200" y1="150" x2="200" y2="215" stroke="#263238" stroke-width="2"/>
    <rect x="130" y="180" width="30" height="4" rx="2" fill="#ECEFF1"/>
    <rect x="240" y="180" width="30" height="4" rx="2" fill="#ECEFF1"/>
  </g>
</svg>""",

    "bathroom_wall_washbasin.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_bwb" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F6F9FA"/><stop offset="100%" stop-color="#E2ECEE"/></linearGradient>
    <filter id="sh_bwb"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_bwb)" rx="16"/>
  <ellipse cx="200" cy="242" rx="60" ry="10" fill="rgba(0,0,0,0.06)"/>
  <g filter="url(#sh_bwb)">
    <ellipse cx="200" cy="155" rx="65" ry="24" fill="#FFFFFF" stroke="#B0BEC5" stroke-width="2"/>
    <path d="M200,145 L200,125 Q200,118 194,120 L190,122" fill="none" stroke="#37474F" stroke-width="3.5" stroke-linecap="round"/>
    <rect x="150" y="175" width="100" height="12" rx="2" fill="#CFD8DC"/>
  </g>
</svg>""",

    "bathroom_mirror_cabinet.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_bmir" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F5F8F9"/><stop offset="100%" stop-color="#E0EBF0"/></linearGradient>
    <filter id="sh_bmir"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_bmir)" rx="16"/>
  <g filter="url(#sh_bmir)">
    <rect x="120" y="60" width="160" height="180" rx="8" fill="#ECEFF1" stroke="#90A4AE" stroke-width="2"/>
    <rect x="126" y="66" width="71" height="168" rx="4" fill="#E1F5FE" stroke="#B3E5FC" stroke-width="1.5"/>
    <rect x="203" y="66" width="71" height="168" rx="4" fill="#E1F5FE" stroke="#B3E5FC" stroke-width="1.5"/>
    <line x1="140" y1="80" x2="185" y2="160" stroke="#FFF" stroke-width="2.5" opacity="0.6"/>
  </g>
</svg>""",

    "bathroom_linen_tower.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_btow" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F7FAF9"/><stop offset="100%" stop-color="#E5ECE9"/></linearGradient>
    <filter id="sh_btow"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_btow)" rx="16"/>
  <ellipse cx="200" cy="254" rx="65" ry="10" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_btow)">
    <rect x="150" y="45" width="100" height="200" rx="6" fill="#FFFFFF" stroke="#CFD8DC" stroke-width="2"/>
    <rect x="156" y="55" width="88" height="60" rx="3" fill="#E0F2F1"/>
    <rect x="156" y="125" width="88" height="50" rx="3" fill="#F5F5F5"/>
    <rect x="156" y="185" width="88" height="52" rx="3" fill="#F5F5F5"/>
    <circle cx="235" cy="150" r="3" fill="#37474F"/>
    <circle cx="235" cy="210" r="3" fill="#37474F"/>
  </g>
</svg>""",

    "bathroom_towel_shelf.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_bts" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FAF9F6"/><stop offset="100%" stop-color="#ECE5D8"/></linearGradient>
    <filter id="sh_bts"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_bts)" rx="16"/>
  <ellipse cx="200" cy="250" rx="70" ry="10" fill="rgba(0,0,0,0.06)"/>
  <g filter="url(#sh_bts)">
    <rect x="145" y="70" width="5" height="175" fill="#C5A07A"/>
    <rect x="250" y="70" width="5" height="175" fill="#C5A07A"/>
    <rect x="140" y="90" width="120" height="8" rx="2" fill="#D7CCC8"/>
    <rect x="140" y="140" width="120" height="8" rx="2" fill="#D7CCC8"/>
    <rect x="140" y="190" width="120" height="8" rx="2" fill="#D7CCC8"/>
    <rect x="160" y="125" width="35" height="15" rx="3" fill="#80CBC4"/>
    <rect x="205" y="125" width="35" height="15" rx="3" fill="#FFF"/>
  </g>
</svg>""",

    "bathroom_teak_stool.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_bstl" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FBF9F7"/><stop offset="100%" stop-color="#EFE6DC"/></linearGradient>
    <filter id="sh_bstl"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_bstl)" rx="16"/>
  <ellipse cx="200" cy="245" rx="60" ry="10" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_bstl)">
    <polygon points="150,170 142,242 150,242 158,170" fill="#6D4C41"/>
    <polygon points="250,170 258,242 250,242 242,170" fill="#6D4C41"/>
    <rect x="135" y="150" width="130" height="20" rx="6" fill="#8D6E63"/>
    <line x1="175" y1="150" x2="175" y2="170" stroke="#5D4037" stroke-width="2"/>
    <line x1="225" y1="150" x2="225" y2="170" stroke="#5D4037" stroke-width="2"/>
  </g>
</svg>""",

    "bathroom_laundry_hamper.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_bhmp" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FBFBF9"/><stop offset="100%" stop-color="#EDECE8"/></linearGradient>
    <filter id="sh_bhmp"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_bhmp)" rx="16"/>
  <ellipse cx="200" cy="246" rx="55" ry="10" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_bhmp)">
    <polygon points="150,120 160,240 240,240 250,120" fill="#B0BEC5"/>
    <rect x="145" y="110" width="110" height="15" rx="5" fill="#8D6E63"/>
  </g>
</svg>""",

    "bathroom_overtoilet_rack.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_botr" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FAFBFB"/><stop offset="100%" stop-color="#E8ECEE"/></linearGradient>
    <filter id="sh_botr"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_botr)" rx="16"/>
  <ellipse cx="200" cy="252" rx="80" ry="10" fill="rgba(0,0,0,0.06)"/>
  <g filter="url(#sh_botr)">
    <rect x="135" y="50" width="5" height="195" fill="#37474F"/>
    <rect x="260" y="50" width="5" height="195" fill="#37474F"/>
    <rect x="130" y="65" width="140" height="6" rx="2" fill="#78909C"/>
    <rect x="130" y="105" width="140" height="6" rx="2" fill="#78909C"/>
    <rect x="130" y="145" width="140" height="6" rx="2" fill="#78909C"/>
    <line x1="135" y1="180" x2="265" y2="180" stroke="#90A4AE" stroke-width="3" stroke-dasharray="4 4"/>
  </g>
</svg>""",

    # Home Office
    "office_compact_study_desk.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_ostd" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FAF9F6"/><stop offset="100%" stop-color="#ECE5D8"/></linearGradient>
    <filter id="sh_ostd"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_ostd)" rx="16"/>
  <ellipse cx="200" cy="248" rx="100" ry="12" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_ostd)">
    <line x1="120" y1="140" x2="110" y2="245" stroke="#3E2723" stroke-width="6" stroke-linecap="round"/>
    <line x1="280" y1="140" x2="290" y2="245" stroke="#3E2723" stroke-width="6" stroke-linecap="round"/>
    <rect x="95" y="125" width="210" height="16" rx="4" fill="#C5A07A"/>
    <rect x="110" y="95" width="180" height="30" rx="3" fill="#EFEBE9"/>
    <rect x="130" y="105" width="8" height="20" fill="#5D4037"/>
    <rect x="140" y="102" width="10" height="23" fill="#8D6E63"/>
  </g>
</svg>""",

    "office_electric_sitstand_desk.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_oess" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F8FAFA"/><stop offset="100%" stop-color="#E5E8E8"/></linearGradient>
    <filter id="sh_oess"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_oess)" rx="16"/>
  <ellipse cx="200" cy="248" rx="125" ry="14" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_oess)">
    <rect x="110" y="130" width="12" height="110" fill="#212121"/>
    <rect x="95" y="238" width="45" height="7" rx="3" fill="#000"/>
    <rect x="278" y="130" width="12" height="110" fill="#212121"/>
    <rect x="260" y="238" width="45" height="7" rx="3" fill="#000"/>
    <rect x="75" y="115" width="250" height="18" rx="4" fill="#FFFFFF" stroke="#CFD8DC" stroke-width="2"/>
    <rect x="270" y="133" width="16" height="8" rx="2" fill="#455A64"/>
  </g>
</svg>""",

    "office_executive_leather_chair.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_oexc" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F9F9F8"/><stop offset="100%" stop-color="#E9E8E4"/></linearGradient>
    <filter id="sh_oexc"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_oexc)" rx="16"/>
  <ellipse cx="200" cy="250" rx="65" ry="12" fill="rgba(0,0,0,0.08)"/>
  <g filter="url(#sh_oexc)">
    <rect x="196" y="200" width="8" height="40" fill="#B0BEC5"/>
    <line x1="200" y1="240" x2="160" y2="248" stroke="#78909C" stroke-width="6" stroke-linecap="round"/>
    <line x1="200" y1="240" x2="240" y2="248" stroke="#78909C" stroke-width="6" stroke-linecap="round"/>
    <rect x="150" y="160" width="100" height="28" rx="8" fill="#3E2723"/>
    <rect x="155" y="70" width="90" height="95" rx="14" fill="#3E2723"/>
    <path d="M142,150 L142,130 L155,130" stroke="#78909C" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M258,150 L258,130 L245,130" stroke="#78909C" stroke-width="5" fill="none" stroke-linecap="round"/>
  </g>
</svg>""",

    "office_mobile_pedestal.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_oped" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F8FAFA"/><stop offset="100%" stop-color="#E8ECEC"/></linearGradient>
    <filter id="sh_oped"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_oped)" rx="16"/>
  <ellipse cx="200" cy="248" rx="65" ry="10" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_oped)">
    <circle cx="155" cy="238" r="6" fill="#37474F"/>
    <circle cx="245" cy="238" r="6" fill="#37474F"/>
    <rect x="145" y="100" width="110" height="130" rx="6" fill="#FFFFFF" stroke="#CFD8DC" stroke-width="2"/>
    <rect x="152" y="108" width="96" height="32" rx="3" fill="#ECEFF1"/>
    <rect x="152" y="146" width="96" height="32" rx="3" fill="#ECEFF1"/>
    <rect x="152" y="184" width="96" height="38" rx="3" fill="#ECEFF1"/>
    <rect x="190" y="122" width="20" height="4" rx="2" fill="#78909C"/>
    <rect x="190" y="160" width="20" height="4" rx="2" fill="#78909C"/>
    <rect x="190" y="200" width="20" height="4" rx="2" fill="#78909C"/>
  </g>
</svg>""",

    "office_dual_monitor_stand.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_oms" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FAF9F6"/><stop offset="100%" stop-color="#ECE5D8"/></linearGradient>
    <filter id="sh_oms"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_oms)" rx="16"/>
  <ellipse cx="200" cy="245" rx="120" ry="12" fill="rgba(0,0,0,0.06)"/>
  <g filter="url(#sh_oms)">
    <rect x="90" y="170" width="14" height="45" fill="#3E2723"/>
    <rect x="296" y="170" width="14" height="45" fill="#3E2723"/>
    <rect x="80" y="155" width="240" height="18" rx="4" fill="#8D6E63"/>
    <rect x="110" y="100" width="80" height="50" rx="3" fill="#212121"/>
    <rect x="210" y="100" width="80" height="50" rx="3" fill="#212121"/>
  </g>
</svg>""",

    "office_file_cabinet.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_ofc" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F8FAFA"/><stop offset="100%" stop-color="#E8ECEC"/></linearGradient>
    <filter id="sh_ofc"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_ofc)" rx="16"/>
  <ellipse cx="200" cy="250" rx="100" ry="12" fill="rgba(0,0,0,0.07)"/>
  <g filter="url(#sh_ofc)">
    <rect x="110" y="90" width="180" height="150" rx="6" fill="#37474F"/>
    <rect x="118" y="98" width="164" height="66" rx="4" fill="#455A64"/>
    <rect x="118" y="168" width="164" height="66" rx="4" fill="#455A64"/>
    <rect x="180" y="128" width="40" height="6" rx="3" fill="#CFD8DC"/>
    <rect x="180" y="198" width="40" height="6" rx="3" fill="#CFD8DC"/>
  </g>
</svg>""",

    "office_storage_credenza.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg_ocred" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FAF8F5"/><stop offset="100%" stop-color="#EAE3D5"/></linearGradient>
    <filter id="sh_ocred"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-opacity="0.12"/></filter>
  </defs>
  <rect width="400" height="300" fill="url(#bg_ocred)" rx="16"/>
  <ellipse cx="200" cy="245" rx="125" ry="12" fill="rgba(0,0,0,0.06)"/>
  <g filter="url(#sh_ocred)">
    <polygon points="100,210 94,242 102,242 108,210" fill="#2E241B"/>
    <polygon points="300,210 306,242 298,242 292,210" fill="#2E241B"/>
    <rect x="85" y="115" width="230" height="98" rx="6" fill="#5D4037"/>
    <rect x="92" y="122" width="105" height="84" rx="4" fill="#8D6E63"/>
    <rect x="203" y="122" width="105" height="84" rx="4" fill="#8D6E63"/>
    <rect x="182" y="158" width="5" height="20" rx="2.5" fill="#D7CCC8"/>
    <rect x="213" y="158" width="5" height="20" rx="2.5" fill="#D7CCC8"/>
  </g>
</svg>"""
}

def main():
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "app", "static", "furniture"))
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "furniture"))
    frontend_static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "static", "furniture"))

    os.makedirs(backend_dir, exist_ok=True)
    os.makedirs(frontend_dir, exist_ok=True)
    os.makedirs(frontend_static_dir, exist_ok=True)

    print(f"Generating {len(SVG_ITEMS)} architectural SVG furniture assets...")
    for filename, content in SVG_ITEMS.items():
        backend_path = os.path.join(backend_dir, filename)
        frontend_path = os.path.join(frontend_dir, filename)
        frontend_static_path = os.path.join(frontend_static_dir, filename)

        with open(backend_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        with open(frontend_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        with open(frontend_static_path, "w", encoding="utf-8") as f:
            f.write(content.strip())

    print(f"Successfully generated all {len(SVG_ITEMS)} furniture assets across all static directories.")

if __name__ == "__main__":
    main()
