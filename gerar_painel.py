"""Gera o painel SVG do perfil. Python 3.9+, sem dependências externas."""
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent

def idade(agora):
    nascimento = datetime(1990, 3, 16, tzinfo=agora.tzinfo)
    anos = agora.year - nascimento.year
    aniversario = nascimento.replace(year=agora.year)
    if agora < aniversario:
        anos -= 1
        aniversario = aniversario.replace(year=agora.year - 1)
    restante = agora - aniversario
    return anos, restante.days, restante.seconds // 3600

def gerar():
    agora = datetime.now(ZoneInfo('America/Sao_Paulo'))
    anos, dias, horas = idade(agora)
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="680" viewBox="0 0 1200 680" role="img" aria-labelledby="title desc">',
        '<title id="title">Robson Isidoro — profile</title>',
        '<desc id="desc">Octopus terminal art, age, Anthropic courses and projects.</desc>',
        '<rect width="1200" height="680" rx="18" fill="#101820"/>',
        '<path d="M0 55H1200" stroke="#304451"/>']
    def text(x,y,s,color='#cbd5df',size=17):
        parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="monospace" font-size="{size}" xml:space="preserve">{escape(s)}</text>')
    for x,c in [(27,'#ed6a5e'),(49,'#f4bf4f'),(71,'#61c554')]:
        parts.append(f'<circle cx="{x}" cy="28" r="6" fill="{c}"/>')
    text(99,34,'eusouisidoro1 / README', '#90a7b6',14)
    # The octopus consists exclusively of individual text glyphs.
    # Sample curved arms onto a character grid; no filled shapes or outlines.
    curves = [
        [(193,338),(140,380),(110,302),(73,354),(37,409),(120,424),(113,467),(109,496),(58,487),(58,456)],
        [(210,362),(167,403),(204,458),(153,490),(116,514),(94,544),(128,557)],
        [(231,375),(203,429),(259,474),(218,522),(197,550),(180,560),(195,577)],
        [(249,375),(237,430),(295,449),(274,504),(258,546),(279,565),(303,543)],
        [(268,373),(301,410),(295,460),(334,485),(369,510),(366,551),(337,552)],
        [(282,358),(335,372),(349,415),(386,424),(428,434),(449,407),(433,387)],
        [(292,342),(346,327),(357,294),(399,317),(427,332),(432,366),(409,372)],
        [(180,324),(128,333),(121,276),(85,286),(45,296),(42,334),(65,343)],
    ]
    samples = []
    for curve in curves:
        points = []
        for i in range(0,len(curve)-1,3):
            a,b,c,d = curve[i:i+4]
            for step in range(61):
                t = step/60
                points.append(tuple((1-t)**3*a[k]+3*(1-t)**2*t*b[k]+3*(1-t)*t*t*c[k]+t**3*d[k] for k in (0,1)))
        for i,(x,y) in enumerate(points):
            samples.append((x,y,14-8*i/len(points)))
    for row in range(47):
        y = 123+row*10
        for col in range(69):
            x = 36+col*6
            head = ((x-237)/83)**2+((y-251)/119)**2
            depth = max((1-((x-px)**2+(y-py)**2)**.5/r for px,py,r in samples),default=-1)
            eye = any(((x-ex)/18)**2+((y-286)/23)**2 < 1 for ex in (205,270))
            if eye:
                char = '0' if any(((x-ex)/6)**2+((y-288)/11)**2 < 1 for ex in (208,273)) else ' '
            elif head < 1:
                char = '0' if head < .82 else (':' if head > .96 else 'o')
                if head < .82 and (row+col)%7 == 0:
                    char = '@'
            elif depth > 0:
                char = '0' if depth > .28 else ('.' if depth < .10 else 'o')
            else:
                char = ' '
            if char != ' ':
                text(x,y,char,'#acd4e5',10)
    text(112,620,'$ hello, world.', '#83c9f4',16)
    text(500,105,'@eusouisidoro1', '#e3edf5',25)
    text(500,134,'─────────────────────────────────────────','#405b6b',16)
    def field(y,label,value):
        text(500,y,label,'#f0b477',16)
        text(671,y,value,'#a9d9f8',16)
    field(170,'Name', 'Robson Isidoro')
    field(201,'Age', f'{anos} years, {dias} days, {horas} hours')
    field(232,'Born','March 16, 1990')
    field(263,'GitHub','@eusouisidoro1')
    text(500,309,'Learning ─────────────────────────────','#e3edf5',17)
    field(344,'Anthropic','22 completed courses')
    field(375,'Topics','Claude, API, MCP & agents')
    field(406,'Applications','AI fluency, cloud & business')
    text(500,452,'Projects ────────────────────────────────','#e3edf5',17)
    field(487,'Conexão Viva','Connection monitoring')
    field(518,'Pereira','School website')
    text(500,596,'Timezone: America/Sao_Paulo','#90a7b6',12)
    text(500,622,agora.strftime('Updated %Y-%m-%d at %H:%M'),'#90a7b6',12)
    parts.append('</svg>')
    (ROOT/'painel.svg').write_text('\n'.join(parts),encoding='utf-8')

if __name__ == '__main__':
    gerar()
