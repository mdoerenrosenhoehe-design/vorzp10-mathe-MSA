import json, pathlib, re, sys
BASE=pathlib.Path(__file__).resolve().parents[1]/'data'
def load(name):
    s=(BASE/name).read_text(encoding='utf-8')
    return json.loads(s.split('=',1)[1].strip().rstrip(';'))
tasks=load('tasks.js'); challenges=load('challenges.js'); cards=load('flashcards.js'); exams=load('exams.js'); topics=load('topics.js')
errors=[]
def check_unique(items,label):
    ids=[x.get('id') for x in items]
    dup={x for x in ids if ids.count(x)>1}
    if dup: errors.append(f'{label}: doppelte IDs: {sorted(dup)[:5]}')
check_unique(tasks,'tasks'); check_unique(challenges,'challenges'); check_unique(cards,'cards'); check_unique(exams,'exams')
for t in topics:
    n=sum(x['topic']==t['id'] for x in tasks)
    if n<100: errors.append(f"{t['id']}: nur {n} Aufgaben")
    c=sum(x['topic']==t['id'] for x in challenges)
    if c<5: errors.append(f"{t['id']}: nur {c} Challenges")
for x in tasks+challenges:
    for key in ['id','topic','subtopic','competency','difficulty','type','prompt','answer','solution']:
        if key not in x: errors.append(f"{x.get('id','?')}: Feld {key} fehlt")
    a=x.get('answer',{})
    if a.get('kind')=='choice':
        opts=x.get('options',[]); idx=a.get('index',-1)
        if not (0<=idx<len(opts)): errors.append(f"{x['id']}: ungültiger Choice-Index")
        if len(set(map(str,opts)))!=len(opts): errors.append(f"{x['id']}: doppelte Choice-Option")
    if a.get('kind')=='number' and not isinstance(a.get('value'),(int,float)): errors.append(f"{x['id']}: Zahlantwort fehlt")
if len(exams)!=20: errors.append(f'Prüfungsvarianten: {len(exams)} statt 20')
for e in exams:
    if len(e['part1'])!=6: errors.append(f"{e['id']}: Teil 1 hat {len(e['part1'])} Aufgaben")
    if sum(q['points'] for q in e['part1'])!=18: errors.append(f"{e['id']}: Teil 1 nicht 18 Punkte")
    if len(e['part2'])!=3: errors.append(f"{e['id']}: Teil 2 hat {len(e['part2'])} Kontexte")
    pts=sum(p['points'] for c in e['part2'] for p in c['parts'])
    if pts!=54: errors.append(f"{e['id']}: Teil 2 hat {pts} statt 54 Punkte")
    for q in e['part1']:
        if q['topic']=='koerper': errors.append(f"{e['id']}: Körperformel in Teil 1 unerwünscht")
print(f"{len(tasks)} Aufgaben, {len(challenges)} Challenges, {len(cards)} Karteikarten, {len(exams)} Prüfungsvarianten")
if errors:
    print('FEHLER:')
    for e in errors[:100]: print('-',e)
    sys.exit(1)
print('Validierung erfolgreich.')
