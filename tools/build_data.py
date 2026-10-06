import json, math, random, os
from statistics import mean, median

OUT = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(OUT, exist_ok=True)
rng = random.Random(27032027)

def r1(x): return round(float(x)+1e-12,1)
def r2(x): return round(float(x)+1e-12,2)
def fmt(x):
    if isinstance(x, int): return str(x)
    if abs(x-round(x))<1e-10: return str(int(round(x)))
    return (f"{x:.3f}").rstrip('0').rstrip('.')

def answer_num(v, tol=0.01, unit=None, accepted=None):
    d={"kind":"number","value":float(v),"tolerance":tol}
    if unit: d["unit"]=unit
    if accepted: d["acceptedUnits"]=accepted
    return d

def answer_text(vals):
    if isinstance(vals,str): vals=[vals]
    return {"kind":"text","accepted":[str(v).lower() for v in vals]}

def answer_keywords(any_words=None, all_words=None):
    return {"kind":"keywords","any":[w.lower() for w in (any_words or [])],"all":[w.lower() for w in (all_words or [])]}

def mc(correct, distractors):
    opts=[]
    for x in [correct]+list(distractors):
        s=str(x)
        if s not in opts: opts.append(s)
    filler=0
    while len(opts)<4:
        cand=str(filler)
        filler+=1
        if cand not in opts: opts.append(cand)
    opts=opts[:4]
    rng.shuffle(opts)
    return opts, {"kind":"choice","index":opts.index(str(correct))}

def q(id_, topic, sub, comp, diff, typ, prompt, ans, solution, hint1, hint2, options=None, visual=None, points=None, exam=True, source=None):
    o={
        "id":id_,"topic":topic,"subtopic":sub,"competency":comp,"difficulty":diff,"type":typ,
        "prompt":prompt,"answer":ans,"solution":solution,"hint1":hint1,"hint2":hint2,
        "points": points or max(1,diff), "examEligible":bool(exam)
    }
    if options is not None:o["options"]=options
    if visual is not None:o["visual"]=visual
    if source:o["source"]=source
    return o

TOPICS=[
 {"id":"zahlen","title":"Zahlen, Potenzen & Wurzeln","icon":"123","desc":"Zahlvorstellungen, Brüche, Potenzen, Wurzeln, Einheiten und Überschlag"},
 {"id":"algebra","title":"Terme, Gleichungen & LGS","icon":"x=","desc":"Terme umformen, Gleichungen lösen, lineare Gleichungssysteme, Tabellenkalkulation"},
 {"id":"prozent","title":"Prozent- & Zinsrechnung","icon":"%","desc":"Prozentwert, Grundwert, Prozentsatz, Zinsen und mehrstufige Änderungen"},
 {"id":"linear","title":"Lineare Funktionen & Zuordnungen","icon":"↗","desc":"Geraden, Steigung, Achsenabschnitt, Schnittpunkte und Modelle"},
 {"id":"quadratisch","title":"Quadratische Funktionen","icon":"∩","desc":"Parabeln, Scheitelpunkte, Nullstellen und quadratische Gleichungen"},
 {"id":"wachstum","title":"Exponentielles Wachstum","icon":"×q","desc":"Wachstumsfaktor, Abnahme, Vergleich von Modellen und Interpretation"},
 {"id":"geometrie","title":"Ebene Geometrie & Trigonometrie","icon":"△","desc":"Flächen, Kreise, Ähnlichkeit, Pythagoras und Trigonometrie"},
 {"id":"koerper","title":"Körper & räumliche Geometrie","icon":"◉","desc":"Volumen, Oberfläche, zusammengesetzte Körper, Dichte und Modellierung"},
 {"id":"statistik","title":"Daten & Statistik","icon":"▥","desc":"Häufigkeiten, Mittelwerte, Quartile, Boxplots und Dateninterpretation"},
 {"id":"wahrscheinlichkeit","title":"Wahrscheinlichkeit","icon":"🎲","desc":"Laplace, Baumdiagramme, Pfadregeln, Gegenereignis und Simulation"}
]

tasks=[]

def add_family(topic, fam, n, maker):
    for i in range(n):
        tasks.append(maker(i, f"{topic}-{fam}-{i+1:02d}"))

# --- Zahlen ---
contexts=['Schulweg','Gaming-PC','Fahrradtour','Konzert','Sportfest','Klassenfahrt','Streaming','Schulkiosk','Werkstatt']

def zn_order(i,id_):
    vals=[round(rng.uniform(-2,2),2) for _ in range(4)]
    vals=sorted(set(vals))
    while len(vals)<4: vals=sorted(set(vals+[round(rng.uniform(-2,2),2)]))
    vals=vals[:4]; correct=' < '.join(fmt(x) for x in sorted(vals))
    opts,ans=mc(correct,[ ' < '.join(fmt(x) for x in order) for order in [list(reversed(vals)), [vals[1],vals[0],vals[2],vals[3]],[vals[0],vals[2],vals[1],vals[3]]] ])
    return q(id_,'zahlen','Zahlen ordnen','Darstellen',1,'choice',f"Ordne die Zahlen aufsteigend: {', '.join(fmt(x) for x in vals)}",ans,correct,'Vergleiche zuerst die Vorzeichen.','Bei negativen Zahlen ist die Zahl mit dem größeren Betrag kleiner.',opts)
add_family('zahlen','ordnen',9,zn_order)

def zn_power(i,id_):
    b=rng.choice([2,3,4,5,10]); e=rng.choice([2,3,4]); val=b**e
    opts,ans=mc(val,[b*e,b**(e-1),val+b])
    return q(id_,'zahlen','Potenzen','Operieren',1,'choice',f"Berechne {b}^{e}.",ans,f"{b}^{e} = {val}",'Eine Potenz ist eine wiederholte Multiplikation.','Multipliziere die Basis so oft mit sich selbst, wie der Exponent angibt.',opts)
add_family('zahlen','potenz',9,zn_power)

def zn_root(i,id_):
    a=rng.choice([4,9,16,25,36,49,64,81,100,121,144]); val=int(math.sqrt(a))
    opts,ans=mc(val,[val-1,val+1,a//2])
    return q(id_,'zahlen','Wurzeln','Operieren',1,'choice',f"Bestimme √{a}.",ans,f"√{a} = {val}, denn {val}² = {a}.",'Suche eine Zahl, deren Quadrat die Zahl unter der Wurzel ergibt.','Teste benachbarte Quadratzahlen.',opts)
add_family('zahlen','wurzel',9,zn_root)

def zn_scientific(i,id_):
    m=rng.choice([1.2,2.5,3.4,4.8,6.2,7.5,8.1,9.3]); e=rng.choice([-4,-3,-2,2,3,4]); val=m*(10**e)
    return q(id_,'zahlen','Zehnerpotenzen','Darstellen',2,'number',f"Schreibe {m} · 10^{e} als Dezimalzahl.",answer_num(val,1e-8),f"Das Komma wird um {abs(e)} Stellen {'nach rechts' if e>0 else 'nach links'} verschoben: {fmt(val)}.",'Beachte das Vorzeichen des Exponenten.','Positiver Exponent: Komma nach rechts; negativer: nach links.')
add_family('zahlen','zehnerpotenz',9,zn_scientific)

def zn_fraction(i,id_):
    den=rng.choice([4,5,8,10,20,25]); num=rng.randint(1,den-1); pct=num/den*100
    opts,ans=mc(f"{fmt(pct)} %",[f"{fmt(num/den)} %",f"{fmt((den-num)/den*100)} %",f"{fmt(pct+10)} %"])
    return q(id_,'zahlen','Bruch–Dezimal–Prozent','Darstellen',2,'choice',f"Welcher Prozentsatz entspricht dem Bruch {num}/{den}?",ans,f"{num}/{den} = {fmt(num/den)} = {fmt(pct)} %.",'Berechne Zähler ÷ Nenner.','Multipliziere die Dezimalzahl anschließend mit 100 %.',opts)
add_family('zahlen','bruchprozent',9,zn_fraction)

def zn_unit(i,id_):
    typ=i%5
    if typ==0:
        v=rng.choice([1.2,2.5,3.75,6.4]); ans=v*1000; p=f"{v} km = ? m"; sol=f"{v} · 1000 = {fmt(ans)} m"; unit='m'
    elif typ==1:
        v=rng.choice([250,430,780,1250]); ans=v/1000; p=f"{v} g = ? kg"; sol=f"{v} : 1000 = {fmt(ans)} kg"; unit='kg'
    elif typ==2:
        v=rng.choice([1.5,2.25,3.5]); ans=v*60; p=f"{v} h = ? min"; sol=f"{v} · 60 = {fmt(ans)} min"; unit='min'
    elif typ==3:
        v=rng.choice([2,3.5,4.2]); ans=v*10000; p=f"{v} m² = ? cm²"; sol=f"1 m² = 10 000 cm², also {v} · 10 000 = {fmt(ans)} cm²"; unit='cm²'
    else:
        v=rng.choice([1.2,2.8,3.6]); ans=v*1000; p=f"{v} ℓ = ? ml"; sol=f"1 ℓ = 1000 ml, also {v} · 1000 = {fmt(ans)} ml"; unit='ml'
    return q(id_,'zahlen','Einheiten','Operieren',1,'number',p,answer_num(ans,0.01,unit),sol,'Prüfe, ob du in eine kleinere oder größere Einheit umrechnest.','Nutze den passenden Umrechnungsfaktor.')
add_family('zahlen','einheiten',9,zn_unit)

def zn_signed(i,id_):
    a=rng.randint(-18,18); b=rng.randint(-15,15); op=rng.choice(['+','-'])
    val=a+b if op=='+' else a-b
    return q(id_,'zahlen','Rationale Zahlen','Operieren',1,'number',f"Berechne: {a} {op} ({b})",answer_num(val,0),f"{a} {op} ({b}) = {val}",'Achte auf das Vorzeichen in der Klammer.','Beim Subtrahieren einer negativen Zahl wird addiert.')
add_family('zahlen','vorzeichen',9,zn_signed)

def zn_estimate(i,id_):
    a=rng.choice([198,247,399,612,805]); b=rng.choice([19,31,48,52]); exact=a*b
    estimates=[round(exact,-2),round(exact,-3),round(exact*0.5,-2),round(exact*1.5,-2)]
    correct=min(estimates,key=lambda x:abs(x-exact))
    opts,ans=mc(correct,[x for x in estimates if x!=correct])
    return q(id_,'zahlen','Überschlag','Problemlösen',2,'choice',f"Welcher Wert ist ein sinnvoller Überschlag für {a} · {b}?",ans,f"Zum Beispiel {a} ≈ {round(a,-2)} und {b} ≈ {round(b,-1)}. Das Produkt liegt ungefähr bei {correct}.",'Runde beide Faktoren auf gut rechenbare Zahlen.','Vergleiche Größenordnungen, nicht die letzten Ziffern.',opts)
add_family('zahlen','ueberschlag',9,zn_estimate)

def zn_ratio(i,id_):
    k=rng.choice([2,3,4,5]); a=rng.choice([6,8,10,12]); b=a*k; x=rng.choice([7,9,11,13]); val=x*k
    return q(id_,'zahlen','Verhältnisse','Modellieren',2,'number',f"{a} gleiche Artikel kosten {b} €. Wie viel kosten {x} Artikel bei gleichem Stückpreis?",answer_num(val,0.01,'€'),f"Stückpreis: {b} : {a} = {k} €. Für {x} Stück: {x} · {k} = {val} €.",'Bestimme zuerst den Preis für ein Stück.','Nutze dann die proportionale Zuordnung.')
add_family('zahlen','verhaeltnis',9,zn_ratio)

def zn_scale(i,id_):
    scale=rng.choice([50,100,200,500,1000]); cm=rng.choice([2.5,4,6.5,8]); real_m=cm*scale/100
    return q(id_,'zahlen','Maßstab','Modellieren',2,'number',f"Auf einem Plan im Maßstab 1:{scale} ist eine Strecke {cm} cm lang. Wie lang ist sie in Wirklichkeit in Metern?",answer_num(real_m,0.01,'m'),f"{cm} cm · {scale} = {fmt(cm*scale)} cm = {fmt(real_m)} m.",'Multipliziere die Planlänge mit dem Maßstabsfaktor.','Wandle anschließend Zentimeter in Meter um.')
add_family('zahlen','massstab',9,zn_scale)

def zn_fractionop(i,id_):
    d=rng.choice([4,5,6,8,10]); a=rng.randint(1,d-1); b=rng.randint(1,d-1); val=(a+b)/d
    return q(id_,'zahlen','Bruchrechnung','Operieren',2,'number',f"Berechne als Dezimalzahl: {a}/{d} + {b}/{d}",answer_num(val,0.001),f"Gleicher Nenner: ({a}+{b})/{d} = {a+b}/{d} = {fmt(val)}.",'Bei gleichem Nenner werden die Zähler addiert.','Wandle den Ergebnisbruch durch Division in eine Dezimalzahl um.')
add_family('zahlen','bruchrechnung',9,zn_fractionop)

def zn_round(i,id_):
    x=round(rng.uniform(10,500),3); dec=rng.choice([0,1,2]); val=round(x,dec)
    return q(id_,'zahlen','Runden','Darstellen',1,'number',f"Runde {x} auf {dec} Nachkommastelle{'n' if dec!=1 else ''}.",answer_num(val,10**(-dec)/100 if dec else 0),f"Gerundet ergibt sich {fmt(val)}.",'Betrachte die Ziffer rechts von der Rundungsstelle.','0–4 abrunden, 5–9 aufrunden.')
add_family('zahlen','runden',9,zn_round)

# --- Algebra ---
def alg_simplify(i,id_):
    a=rng.randint(2,9); b=rng.randint(1,8); c=rng.randint(1,6); coef=a+b-c
    opts,ans=mc(f"{coef}x",[f"{a+b+c}x",f"{coef}",f"{a+b}x-{c}"])
    return q(id_,'algebra','Terme zusammenfassen','Operieren',1,'choice',f"Vereinfache: {a}x + {b}x − {c}x",ans,f"Gleichartige Terme zusammenfassen: ({a}+{b}−{c})x = {coef}x.",'Nur gleichartige Terme dürfen zusammengefasst werden.','Addiere bzw. subtrahiere die Koeffizienten.',opts)
add_family('algebra','vereinfachen',9,alg_simplify)

def alg_eval(i,id_):
    a=rng.randint(2,6); b=rng.randint(-8,8); x=rng.randint(-4,7); val=a*x+b
    return q(id_,'algebra','Termwerte','Operieren',1,'number',f"Für T(x) = {a}x {'+' if b>=0 else '−'} {abs(b)} gilt x = {x}. Berechne T(x).",answer_num(val,0),f"T({x}) = {a}·({x}) {'+' if b>=0 else '−'} {abs(b)} = {val}.",'Setze den Wert anstelle von x ein.','Achte bei negativen x-Werten auf Klammern.')
add_family('algebra','termwert',9,alg_eval)

def alg_linear_eq(i,id_):
    x=rng.randint(-8,12); a=rng.randint(2,9); b=rng.randint(-15,15); c=a*x+b
    return q(id_,'algebra','Lineare Gleichungen','Operieren',2,'number',f"Löse: {a}x {'+' if b>=0 else '−'} {abs(b)} = {c}",answer_num(x,0),f"Zuerst {('− '+str(b)) if b>=0 else '+ '+str(abs(b))}, dann durch {a} teilen. Es folgt x = {x}.",'Mache zuerst die Addition/Subtraktion rückgängig.','Teile anschließend beide Seiten durch den Faktor vor x.')
add_family('algebra','lineargleichung',9,alg_linear_eq)

def alg_lgs(i,id_):
    x=rng.randint(-4,6); y=rng.randint(-4,6); a,b,c,d=2,1,1,-1
    e=a*x+b*y; f=c*x+d*y
    typ='text'; ans=answer_text([f"{x};{y}",f"({x}|{y})",f"x={x},y={y}",f"{x},{y}"])
    return q(id_,'algebra','Lineare Gleichungssysteme','Operieren',3,typ,f"Löse das LGS und gib x;y an: I: 2x + y = {e}; II: x − y = {f}",ans,f"Aus II folgt y=x−{f}. Einsetzen in I: 2x+x−{f}={e}. Damit x={x} und y={y}.",'Nutze Einsetzen oder Addieren.','Aus II kannst du y direkt in Abhängigkeit von x ausdrücken.')
add_family('algebra','lgs',9,alg_lgs)

def alg_binom(i,id_):
    a=rng.randint(2,9); opts,ans=mc(f"x² + {2*a}x + {a*a}",[f"x² + {a}x + {a*a}",f"x² + {2*a}x + {2*a*a}",f"x² − {2*a}x + {a*a}"])
    return q(id_,'algebra','Binomische Formeln','Operieren',2,'choice',f"Welche Entwicklung ist richtig? (x + {a})²",ans,f"(x+{a})² = x² + 2·{a}·x + {a}² = x² + {2*a}x + {a*a}.",'Nutze (a+b)²=a²+2ab+b².','Der mittlere Term enthält den Faktor 2.',opts)
add_family('algebra','binomisch',9,alg_binom)

def alg_zero_product(i,id_):
    rA=rng.randint(-8,7); rB=rng.randint(rA+1,9)
    ans=answer_text([f"{rA};{rB}",f"{rB};{rA}",f"x={rA},x={rB}"])
    return q(id_,'algebra','Quadratische Gleichungen','Operieren',3,'text',f"Löse: (x − ({rA})) · (x − ({rB})) = 0. Gib beide Lösungen mit Semikolon an.",ans,f"Ein Produkt ist 0, wenn mindestens ein Faktor 0 ist. Daher x={rA} oder x={rB}.",'Nutze den Satz vom Nullprodukt.','Setze jeden Faktor einzeln gleich 0.')
add_family('algebra','nullprodukt',9,alg_zero_product)

def alg_pq(i,id_):
    r1v=rng.randint(-5,2); r2v=rng.randint(3,8); p=-(r1v+r2v); qqv=r1v*r2v
    ans=answer_text([f"{r1v};{r2v}",f"{r2v};{r1v}",f"x={r1v},x={r2v}"])
    sign='+' if qqv>=0 else '−'
    return q(id_,'algebra','p-q-Formel','Operieren',4,'text',f"Löse x² {'+' if p>=0 else '−'} {abs(p)}x {sign} {abs(qqv)} = 0. Gib beide Lösungen mit Semikolon an.",ans,f"Mit der p-q-Formel erhält man x={r1v} und x={r2v}.",'Bringe die Gleichung in die Normalform x²+px+q=0.','Setze p und q sorgfältig mit Vorzeichen in die p-q-Formel ein.')
add_family('algebra','pq',9,alg_pq)

def alg_formula(i,id_):
    w=rng.choice([48,72,96,120]); p=rng.choice([0.2,0.25,0.4]); G=w/p
    return q(id_,'algebra','Formeln umstellen','Operieren',2,'number',f"Es gilt W = G · p. Stelle nach G um und berechne G für W={w} und p={fmt(p)}.",answer_num(G,0.01),f"G = W/p = {w}/{fmt(p)} = {fmt(G)}.",'Teile beide Seiten durch p.','Setze die Werte erst nach dem Umstellen ein.')
add_family('algebra','umstellen',9,alg_formula)

def alg_spreadsheet(i,id_):
    row=i+2; opts,ans=mc(f"=B{row}*C{row}/100",[f"=B{row}+C{row}/100",f"=B{row}/C{row}*100",f"=B2*C2/100"])
    return q(id_,'algebra','Tabellenkalkulation','Werkzeuge',2,'choice',f"In Zeile {row} steht in B{row} der Grundwert und in C{row} der Prozentsatz. Welche Formel berechnet in D{row} den Prozentwert?",ans,f"Prozentwert = Grundwert · Prozentsatz / 100, also =B{row}*C{row}/100.",'Übertrage die Prozentformel W=G·p/100 auf Zellbezüge.','Achte darauf, dass die Zellnummern zur gleichen Zeile gehören.',opts)
add_family('algebra','tabellenkalkulation',9,alg_spreadsheet)

def alg_word(i,id_):
    price=rng.randint(4,12); fixed=rng.randint(10,30); total=rng.choice([70,82,94,106]); n=(total-fixed)/price
    while abs(n-round(n))>1e-9 or n<=0:
        total+=1; n=(total-fixed)/price
    n=int(n)
    return q(id_,'algebra','Sachgleichungen','Modellieren',3,'number',f"Für eine Veranstaltung fallen {fixed} € Grundkosten und {price} € pro Person an. Insgesamt werden {total} € bezahlt. Wie viele Personen sind es?",answer_num(n,0),f"Gleichung: {fixed}+{price}x={total}. Daraus {price}x={total-fixed} und x={n}.",'Formuliere die Gesamtkosten als Grundkosten + Preis pro Person · Anzahl.','Löse die entstehende lineare Gleichung nach x.')
add_family('algebra','sachgleichung',9,alg_word)

def alg_factor(i,id_):
    a=rng.randint(2,9); b=rng.randint(2,9); g=math.gcd(a,b); opts,ans=mc(f"{g}({a//g}x + {b//g})",[f"{a}(x+{b})",f"{g}({a}x+{b})",f"x({a}+{b})"])
    return q(id_,'algebra','Ausklammern','Operieren',2,'choice',f"Klammere den größten gemeinsamen Faktor aus: {a}x + {b}",ans,f"ggT({a},{b})={g}. Daher {a}x+{b} = {g}({a//g}x+{b//g}).",'Bestimme den größten gemeinsamen Teiler der Koeffizienten.','Teile jeden Summanden durch den ausgeklammerten Faktor.',opts)
add_family('algebra','ausklammern',9,alg_factor)

def alg_check(i,id_):
    x=rng.randint(-3,6); a=rng.randint(2,5); b=rng.randint(-4,7); c=a*x+b; cand=x+rng.choice([-2,-1,0,1,2]); truth=(cand==x); opts,ans=mc('ja' if truth else 'nein',['nein' if truth else 'ja','nur für x=0','nicht entscheidbar'])
    return q(id_,'algebra','Probe','Argumentieren',1,'choice',f"Ist x={cand} eine Lösung von {a}x {'+' if b>=0 else '−'} {abs(b)} = {c}?",ans,f"Einsetzen: linke Seite = {a*cand+b}. Das ist {'gleich' if truth else 'nicht gleich'} {c}. Also {'ja' if truth else 'nein'}.",'Setze den vorgeschlagenen Wert in die linke Seite ein.','Vergleiche anschließend beide Seiten.',opts)
add_family('algebra','probe',9,alg_check)

# --- Prozent ---
def pr_value(i,id_):
    G=rng.choice([80,120,150,200,240,300,450]); p=rng.choice([5,10,12,15,20,25,30]); W=G*p/100
    return q(id_,'prozent','Prozentwert','Operieren',1,'number',f"Berechne {p} % von {G}.",answer_num(W,0.01),f"W = {G}·{p}/100 = {fmt(W)}.",'Prozentwert = Grundwert · Prozentsatz / 100.','Rechne zunächst 1 % oder nutze direkt die Formel.')
add_family('prozent','wert',9,pr_value)

def pr_base(i,id_):
    p=rng.choice([10,20,25,40,50]); G=rng.choice([100,160,200,240,300]); W=G*p/100
    return q(id_,'prozent','Grundwert','Operieren',2,'number',f"{fmt(W)} entsprechen {p} %. Bestimme den Grundwert.",answer_num(G,0.01),f"G = W / ({p}/100) = {fmt(W)}/{fmt(p/100)} = {G}.",'Wenn der Prozentwert gegeben ist, teile durch den Prozentsatz als Dezimalzahl.','{p} % entsprechen p/100 des Grundwerts.'.replace('{p}',str(p)))
add_family('prozent','grundwert',9,pr_base)

def pr_rate(i,id_):
    G=rng.choice([80,120,160,200,250]); p=rng.choice([12.5,20,25,30,40]); W=G*p/100
    return q(id_,'prozent','Prozentsatz','Operieren',2,'number',f"Von {G} sind {fmt(W)} markiert. Wie viel Prozent sind das?",answer_num(p,0.01,'%'),f"p = {fmt(W)}/{G}·100 = {fmt(p)} %.",'Bilde Anteil ÷ Ganzes.','Multipliziere das Verhältnis mit 100 %.')
add_family('prozent','prozentsatz',9,pr_rate)

def pr_discount(i,id_):
    price=rng.choice([49,59,79,99,129,159]); p=rng.choice([10,15,20,25,30]); new=price*(1-p/100)
    return q(id_,'prozent','Rabatt','Modellieren',2,'number',f"Ein Artikel kostet {price} €. Im Sale gibt es {p} % Rabatt. Berechne den neuen Preis.",answer_num(new,0.02,'€'),f"Neuer Preis = {price}·(1−{p}/100) = {fmt(new)} €.",'Berechne entweder den Rabatt und ziehe ihn ab oder nutze den Restfaktor.','Nach {p} % Rabatt bleiben {r} %.'.replace('{p}',str(p)).replace('{r}',str(100-p)))
add_family('prozent','rabatt',9,pr_discount)

def pr_change(i,id_):
    old=rng.choice([40,50,80,100,120,200]); p=rng.choice([5,10,15,20,25]); new=old*(1+p/100)
    return q(id_,'prozent','Prozentuale Änderung','Modellieren',2,'number',f"Ein Wert steigt von {old} um {p} %. Wie groß ist der neue Wert?",answer_num(new,0.01),f"{old}·(1+{p}/100) = {fmt(new)}.",'Nutze den Wachstumsfaktor 1+p/100.','Eine Zunahme wird nicht durch p/100 allein, sondern durch 1+p/100 beschrieben.')
add_family('prozent','aenderung',9,pr_change)

def pr_reverse(i,id_):
    original=rng.choice([80,100,120,160,200]); p=rng.choice([10,20,25]); sale=original*(1-p/100)
    return q(id_,'prozent','Rückwärtsrechnen','Problemlösen',3,'number',f"Nach {p} % Rabatt kostet ein Produkt {fmt(sale)} €. Wie hoch war der ursprüngliche Preis?",answer_num(original,0.02,'€'),f"{fmt(sale)} entspricht {100-p} %. Grundwert = {fmt(sale)}/{fmt((100-p)/100)} = {original} €.",'Der reduzierte Preis ist nicht 100 %, sondern nur der Restprozentsatz.','Teile den neuen Preis durch den Restfaktor.')
add_family('prozent','rueckwaerts',9,pr_reverse)

def pr_interest(i,id_):
    K=rng.choice([500,800,1200,1500,2000]); p=rng.choice([1.5,2,2.5,3,4]); Z=K*p/100
    return q(id_,'prozent','Jahreszinsen','Modellieren',2,'number',f"Ein Kapital von {K} € wird ein Jahr lang mit {p} % verzinst. Berechne die Zinsen.",answer_num(Z,0.02,'€'),f"Z = K·p/100 = {K}·{p}/100 = {fmt(Z)} €.",'Jahreszinsen funktionieren wie ein Prozentwert.','Setze Kapital und Zinssatz in Z=K·p/100 ein.')
add_family('prozent','zins',9,pr_interest)

def pr_month_interest(i,id_):
    K=rng.choice([1200,1800,2400,3600]); p=rng.choice([2,3,4,5]); m=rng.choice([2,3,4,6,9]); Z=K*p/100*m/12
    return q(id_,'prozent','Monatszinsen','Modellieren',3,'number',f"{K} € werden {m} Monate lang mit {p} % p.a. verzinst. Berechne die Zinsen (kaufmännisch vereinfacht).",answer_num(Z,0.02,'€'),f"Jahreszins: {fmt(K*p/100)} €. Für {m}/12 Jahr: {fmt(K*p/100)}·{m}/12 = {fmt(Z)} €.",'Berechne erst den Jahreszins.','Nimm davon den Anteil m/12.')
add_family('prozent','monatszins',9,pr_month_interest)

def pr_compound(i,id_):
    K=rng.choice([1000,1500,2000,2500]); p=rng.choice([2,3,4,5]); n=rng.choice([2,3,4]); val=K*((1+p/100)**n)
    return q(id_,'prozent','Zinseszins','Modellieren',3,'number',f"{K} € werden {n} Jahre lang mit {p} % pro Jahr verzinst. Wie hoch ist das Kapital danach? Runde auf Cent.",answer_num(r2(val),0.02,'€'),f"K_n = {K}·(1+{p}/100)^{n} = {r2(val)} €.",'Jedes Jahr wird auch der bisherige Zins mitverzinst.','Nutze den Faktor q=1+p/100 und K_n=K_0·q^n.')
add_family('prozent','zinseszins',9,pr_compound)

def pr_multistep(i,id_):
    price=rng.choice([80,100,120,160]); p1=rng.choice([10,20]); p2=rng.choice([5,10]); val=price*(1-p1/100)*(1+p2/100)
    return q(id_,'prozent','Mehrstufige Änderungen','Problemlösen',4,'number',f"Ein Preis von {price} € wird zuerst um {p1} % gesenkt und danach um {p2} % erhöht. Wie hoch ist der Endpreis?",answer_num(r2(val),0.02,'€'),f"{price}·{fmt(1-p1/100)}·{fmt(1+p2/100)} = {r2(val)} €. Prozentänderungen werden nacheinander mit Faktoren verrechnet.",'Die beiden Prozentsätze dürfen nicht einfach addiert oder subtrahiert werden.','Verwende zuerst den Rabattfaktor und danach den Erhöhungsfaktor.')
add_family('prozent','mehrstufig',9,pr_multistep)

def pr_compare(i,id_):
    a=rng.choice([39,49,59,79]); disc=rng.choice([15,20,25]); b=rng.choice([32,42,52,62]); aval=a*(1-disc/100); cheaper='A' if aval<b else 'B'; opts,ans=mc(cheaper,['B' if cheaper=='A' else 'A','gleich teuer','nicht bestimmbar'])
    return q(id_,'prozent','Preisvergleich','Modellieren',3,'choice',f"Shop A: {a} € mit {disc} % Rabatt. Shop B: {b} € ohne Rabatt. Welches Angebot ist günstiger?",ans,f"Shop A kostet {fmt(aval)} €. Shop B kostet {b} €. Daher ist {cheaper} günstiger.",'Berechne den tatsächlichen Preis in Shop A.','Vergleiche anschließend die beiden Endpreise.',opts)
add_family('prozent','vergleich',9,pr_compare)

def pr_point(i,id_):
    total=rng.choice([200,250,320,400]); part=rng.choice([40,50,64,80,100]); p=part/total*100
    return q(id_,'prozent','Anteile','Argumentieren',2,'number',f"Bei einer Umfrage wählen {part} von {total} Personen Option A. Bestimme den Anteil in Prozent.",answer_num(p,0.01,'%'),f"{part}/{total}·100 = {fmt(p)} %.",'Relative Häufigkeit = Anteil / Gesamtzahl.','Multipliziere mit 100, um Prozent zu erhalten.')
add_family('prozent','anteil',9,pr_point)

# --- Linear ---
def li_slope(i,id_):
    m=rng.choice([-3,-2,-1,0.5,1,2,3]); x1=rng.randint(-3,2); x2=x1+rng.choice([2,3,4]); y1=rng.randint(-5,5); y2=y1+m*(x2-x1)
    return q(id_,'linear','Steigung','Operieren',2,'number',f"Eine Gerade geht durch A({x1}|{fmt(y1)}) und B({x2}|{fmt(y2)}). Bestimme die Steigung m.",answer_num(m,0.001),f"m=(y₂−y₁)/(x₂−x₁)=({fmt(y2)}−{fmt(y1)})/({x2}−{x1})={fmt(m)}.",'Steigung = Änderung in y geteilt durch Änderung in x.','Achte auf dieselbe Reihenfolge im Zähler und Nenner.')
add_family('linear','steigung',9,li_slope)

def li_equation(i,id_):
    m=rng.choice([-2,-1,0.5,1,2,3]); b=rng.randint(-5,6); opts,ans=mc(f"y={fmt(m)}x{('+'+str(b)) if b>=0 else str(b)}",[f"y={fmt(b)}x+{fmt(m)}",f"y={fmt(m)}x{('+'+str(-b)) if -b>=0 else str(-b)}",f"y={fmt(m+b)}x"])
    return q(id_,'linear','Geradengleichung','Darstellen',2,'choice',f"Eine Gerade hat die Steigung m={fmt(m)} und den y-Achsenabschnitt b={b}. Welche Gleichung passt?",ans,f"Allgemein y=mx+b, also y={fmt(m)}x{('+'+str(b)) if b>=0 else str(b)}.",'Nutze y=mx+b.','Setze m und b mit Vorzeichen ein.',opts)
add_family('linear','gleichung',9,li_equation)

def li_point(i,id_):
    m=rng.choice([-2,-1,1,2,3]); b=rng.randint(-6,6); x=rng.randint(-4,6); y=m*x+b
    return q(id_,'linear','Punktprobe','Argumentieren',2,'number',f"Für f(x)={m}x {'+' if b>=0 else '−'} {abs(b)}: Welchen y-Wert hat der Graph bei x={x}?",answer_num(y,0),f"f({x})={m}·({x}) {'+' if b>=0 else '−'} {abs(b)}={y}.",'Setze x in die Funktionsgleichung ein.','Der berechnete Funktionswert ist die y-Koordinate.')
add_family('linear','punktprobe',9,li_point)

def li_intersection(i,id_):
    x=rng.randint(-3,6); m1=rng.choice([1,2,3]); m2=rng.choice([-2,-1,0.5]); b1=rng.randint(-4,5); y=m1*x+b1; b2=y-m2*x
    return q(id_,'linear','Schnittpunkt','Problemlösen',3,'number',f"Bestimme die x-Koordinate des Schnittpunkts von f(x)={fmt(m1)}x{('+'+str(b1)) if b1>=0 else str(b1)} und g(x)={fmt(m2)}x{('+'+fmt(b2)) if b2>=0 else fmt(b2)}.",answer_num(x,0.001),f"Setze f(x)=g(x). Die Gleichung liefert x={x}.",'Am Schnittpunkt sind die y-Werte gleich.','Setze die beiden Funktionsterme gleich und löse nach x.')
add_family('linear','schnittpunkt',9,li_intersection)

def li_context(i,id_):
    base=rng.choice([3,5,8,10]); per=rng.choice([1.5,2,2.5,3]); h=rng.choice([2,4,6,8]); cost=base+per*h
    return q(id_,'linear','Kostenmodelle','Modellieren',2,'number',f"Ein Verleih verlangt {base} € Grundgebühr und {per} € pro Stunde. Wie viel kosten {h} Stunden?",answer_num(cost,0.01,'€'),f"K(h)={base}+{per}·h. Für h={h}: K={fmt(cost)} €.",'Die Grundgebühr ist der y-Achsenabschnitt.','Addiere Grundgebühr und variable Kosten.')
add_family('linear','kosten',9,li_context)

def li_table(i,id_):
    m=rng.choice([2,3,4,5]); b=rng.choice([-2,0,1,3]); x=rng.choice([4,5,6,7]); y=m*x+b
    prompt=f"Eine Wertetabelle folgt der linearen Zuordnung y={m}x {'+' if b>=0 else '−'} {abs(b)}. Bestimme y für x={x}."
    return q(id_,'linear','Wertetabellen','Darstellen',1,'number',prompt,answer_num(y,0),f"y={m}·{x}{('+'+str(b)) if b>=0 else str(b)}={y}.",'Setze den x-Wert in die Zuordnung ein.','Rechne Multiplikation vor Addition/Subtraktion.')
add_family('linear','wertetabelle',9,li_table)

def li_model(i,id_):
    scenarios=[('Taxifahrt','Strecke in km','Kosten in €'),('Wassertank','Zeit in min','Wasserhöhe in cm'),('Sparplan','Monate','Guthaben in €')]
    name,xlab,ylab=scenarios[i%3]; m=rng.choice([2,3,5]); b=rng.choice([0,5,10]); opts,ans=mc(f"Startwert {b}, Zuwachs {m} pro Einheit",[f"Startwert {m}, Zuwachs {b} pro Einheit",f"Startwert 0, Zuwachs {b+m}","nicht linear"])
    return q(id_,'linear','Interpretation','Argumentieren',2,'choice',f"Das Modell lautet y={m}x+{b} ({name}). Welche Interpretation ist richtig?",ans,f"b={b} ist der Startwert bei x=0; m={m} ist die Änderung pro x-Einheit.",'Bei y=mx+b hat b eine andere Rolle als m.','Setze x=0, um die Bedeutung von b zu sehen.',opts)
add_family('linear','interpretation',9,li_model)

def li_proportional(i,id_):
    b=rng.choice([0,3,5]); opts,ans=mc('proportional' if b==0 else 'linear, aber nicht proportional',[ 'linear, aber nicht proportional' if b==0 else 'proportional','quadratisch','exponentiell'])
    return q(id_,'linear','Proportionalität','Argumentieren',2,'choice',f"Ordne y=4x{('+'+str(b)) if b else ''} ein.",ans,("Die Gerade geht durch den Ursprung, also proportional." if b==0 else "Die Zuordnung ist linear, hat aber einen von 0 verschiedenen Achsenabschnitt und ist daher nicht proportional."),'Proportional bedeutet: Gerade durch den Ursprung.','Prüfe den Wert bei x=0.',opts)
add_family('linear','proportional',9,li_proportional)

def li_rate(i,id_):
    d=rng.choice([60,90,120,150]); t=rng.choice([1.5,2,2.5,3]); v=d/t
    return q(id_,'linear','Durchschnittsgeschwindigkeit','Modellieren',2,'number',f"Eine Strecke von {d} km wird in {t} h zurückgelegt. Bestimme die durchschnittliche Geschwindigkeit.",answer_num(v,0.01,'km/h'),f"v=s/t={d}/{t}={fmt(v)} km/h.",'Geschwindigkeit = Strecke / Zeit.','Achte auf passende Einheiten.')
add_family('linear','geschwindigkeit',9,li_rate)

def li_zero(i,id_):
    m=rng.choice([-4,-3,-2,2,3,4]); x0=rng.randint(-4,6); b=-m*x0
    return q(id_,'linear','Nullstelle','Operieren',2,'number',f"Bestimme die Nullstelle von f(x)={m}x {'+' if b>=0 else '−'} {abs(b)}.",answer_num(x0,0.001),f"0={m}x{('+'+str(b)) if b>=0 else str(b)} ⇒ x={x0}.",'An der Nullstelle gilt f(x)=0.','Setze y=0 und löse die lineare Gleichung.')
add_family('linear','nullstelle',9,li_zero)

def li_compare(i,id_):
    b1=rng.choice([5,10,15]); m1=rng.choice([1,2,3]); b2=b1+rng.choice([5,10]); m2=max(0.5,m1-rng.choice([0.5,1])); x=(b2-b1)/(m1-m2)
    return q(id_,'linear','Tarifvergleich','Modellieren',4,'number',f"Tarif A: {b1} € Grundpreis + {m1} €/Einheit. Tarif B: {b2} € Grundpreis + {fmt(m2)} €/Einheit. Ab wie vielen Einheiten sind beide gleich teuer?",answer_num(x,0.01),f"{b1}+{m1}x={b2}+{fmt(m2)}x ⇒ x={fmt(x)}.",'Setze die beiden Kostenfunktionen gleich.','Bringe alle x-Terme auf eine Seite und Konstanten auf die andere.')
add_family('linear','tarifvergleich',9,li_compare)

def li_graph(i,id_):
    m=rng.choice([-2,-1,1,2]); b=rng.choice([-3,0,2,4]); visual={"kind":"line","m":m,"b":b,"xmin":-5,"xmax":5,"ymin":-8,"ymax":8}
    opts,ans=mc(f"y={m}x{('+'+str(b)) if b>=0 else str(b)}",[f"y={-m}x{('+'+str(b)) if b>=0 else str(b)}",f"y={m}x{('+'+str(-b)) if -b>=0 else str(-b)}",f"y={b}x+{m}"])
    return q(id_,'linear','Graphen','Darstellen',2,'choice','Welche Gleichung gehört zum dargestellten Graphen?',ans,f"Die Steigung ist {m}, der y-Achsenabschnitt ist {b}. Daher y={m}x{('+'+str(b)) if b>=0 else str(b)}.",'Lies zuerst den Schnittpunkt mit der y-Achse ab.','Bestimme anschließend die Steigung mit einem Steigungsdreieck.',opts,visual)
add_family('linear','graph',9,li_graph)

# --- Quadratisch ---
def qu_eval(i,id_):
    a=rng.choice([-2,-1,1,2]); b=rng.randint(-3,3); c=rng.randint(-5,5); x=rng.randint(-3,4); y=a*x*x+b*x+c
    return q(id_,'quadratisch','Funktionswerte','Operieren',2,'number',f"Berechne f({x}) für f(x)={a}x² {'+' if b>=0 else '−'} {abs(b)}x {'+' if c>=0 else '−'} {abs(c)}.",answer_num(y,0),f"Einsetzen ergibt f({x})={y}.",'Setze x überall in die Funktion ein.','Beachte: x² wird vor Multiplikation und Addition berechnet.')
add_family('quadratisch','wert',9,qu_eval)

def qu_vertex(i,id_):
    a=rng.choice([-2,-1,1,2]); d=rng.randint(-4,4); e=rng.randint(-3,8); opts,ans=mc(f"S({d}|{e})",[f"S({-d}|{e})",f"S({d}|{-e})",f"S({e}|{d})"])
    return q(id_,'quadratisch','Scheitelpunktform','Darstellen',2,'choice',f"Bestimme den Scheitelpunkt von f(x)={a}(x−({d}))²+({e}).",ans,f"In der Scheitelpunktform a(x−d)²+e liegt der Scheitel bei S(d|e), also S({d}|{e}).",'Vergleiche mit a(x−d)²+e.','Das Vorzeichen innerhalb der Klammer gehört zu x−d.',opts)
add_family('quadratisch','scheitel',9,qu_vertex)

def qu_roots(i,id_):
    rA=rng.randint(-5,1); rB=rng.randint(2,7); p=-(rA+rB); qqv=rA*rB
    ans=answer_text([f"{rA};{rB}",f"{rB};{rA}",f"x={rA},x={rB}"])
    return q(id_,'quadratisch','Nullstellen','Operieren',3,'text',f"Bestimme die Nullstellen von f(x)=x² {'+' if p>=0 else '−'} {abs(p)}x {'+' if qqv>=0 else '−'} {abs(qqv)}. Gib sie mit Semikolon an.",ans,f"Die Funktion faktorisiert zu (x−({rA}))(x−({rB})); Nullstellen: {rA} und {rB}.",'Setze f(x)=0.','Nutze Faktorisieren oder die p-q-Formel.')
add_family('quadratisch','nullstellen',9,qu_roots)

def qu_opening(i,id_):
    a=rng.choice([-3,-1,-0.5,0.5,1,3]); correct='nach oben' if a>0 else 'nach unten'; opts,ans=mc(correct,['nach unten' if a>0 else 'nach oben','linear','nicht bestimmbar'])
    return q(id_,'quadratisch','Parabeleigenschaften','Argumentieren',1,'choice',f"Wie ist die Parabel f(x)={a}x² geöffnet?",ans,f"a={a}. Bei a>0 ist die Parabel nach oben, bei a<0 nach unten geöffnet.",'Entscheidend ist das Vorzeichen vor x².','Positiv → oben, negativ → unten.',opts)
add_family('quadratisch','oeffnung',9,qu_opening)

def qu_stretch(i,id_):
    a=rng.choice([0.25,0.5,1.5,2,3]); correct='gestreckt' if abs(a)>1 else 'gestaucht'; opts,ans=mc(correct,['gestaucht' if correct=='gestreckt' else 'gestreckt','linear','verschoben'])
    return q(id_,'quadratisch','Streckfaktor','Argumentieren',2,'choice',f"Verglichen mit y=x² ist y={a}x² …",ans,f"|a|={a}. {'|a|>1, daher gestreckt.' if a>1 else '0<|a|<1, daher gestaucht.'}",'Vergleiche |a| mit 1.','|a|>1 bedeutet schmaler/gestreckt, 0<|a|<1 breiter/gestaucht.',opts)
add_family('quadratisch','streckung',9,qu_stretch)

def qu_axis(i,id_):
    d=rng.randint(-5,5); e=rng.randint(-3,7); a=rng.choice([-2,-1,1,2]); return q(id_,'quadratisch','Symmetrieachse','Darstellen',2,'number',f"Welche x-Koordinate hat die Symmetrieachse von f(x)={a}(x−({d}))²+{e}?",answer_num(d,0),f"Die Symmetrieachse verläuft durch den Scheitelpunkt, also x={d}.",'Die Symmetrieachse geht durch den Scheitelpunkt.','Lies d aus der Scheitelpunktform ab.')
add_family('quadratisch','achse',9,qu_axis)

def qu_context(i,id_):
    h=rng.choice([4,5,6,8]); a=rng.choice([0.25,0.5,1]); x=rng.choice([1,2]); y=-a*x*x+h
    return q(id_,'quadratisch','Sachkontext Parabel','Modellieren',3,'number',f"Ein Bogen wird durch h(x)=−{a}x²+{h} modelliert. Wie hoch ist der Bogen bei x={x} m?",answer_num(y,0.01,'m'),f"h({x})=−{a}·{x}²+{h}={fmt(y)} m.",'Setze die horizontale Entfernung in die Funktion ein.','Die Funktion liefert direkt die Höhe.')
add_family('quadratisch','bogen',9,qu_context)

def qu_width(i,id_):
    a=rng.choice([0.25,0.5,1]); h=rng.choice([4,9,16]); root=math.sqrt(h/a); width=2*root
    return q(id_,'quadratisch','Nullstellen im Kontext','Modellieren',4,'number',f"Ein symmetrischer Torbogen wird durch y=−{a}x²+{h} beschrieben. Wie breit ist der Bogen am Boden (y=0)?",answer_num(width,0.02,'m'),f"0=−{a}x²+{h} ⇒ x²={fmt(h/a)} ⇒ x=±{fmt(root)}. Breite={fmt(2*root)} m.",'Bestimme zuerst die beiden Nullstellen.','Die Breite ist der Abstand zwischen negativer und positiver Nullstelle.')
add_family('quadratisch','breite',9,qu_width)

def qu_interpret(i,id_):
    d=rng.randint(-3,3); e=rng.randint(2,9); a=-rng.choice([0.5,1,2]); opts,ans=mc(f"Maximum {e} bei x={d}",[f"Minimum {e} bei x={d}",f"Nullstelle bei x={d}",f"y-Achsenabschnitt {d}"])
    return q(id_,'quadratisch','Interpretation Scheitel','Argumentieren',3,'choice',f"f(x)={a}(x−({d}))²+{e}. Welche Aussage ist richtig?",ans,f"Da a<0, ist der Scheitel ein Maximum. Der Scheitel liegt bei ({d}|{e}).",'Bestimme Scheitelpunkt und Öffnungsrichtung.','a<0 bedeutet nach unten geöffnet.',opts)
add_family('quadratisch','interpretation',9,qu_interpret)

def qu_graph(i,id_):
    a=rng.choice([-1,-0.5,0.5,1]); d=rng.randint(-2,2); e=rng.randint(-2,4); visual={"kind":"quadratic","a":a,"d":d,"e":e,"xmin":-5,"xmax":5,"ymin":-6,"ymax":8}
    opts,ans=mc(f"{a}(x−({d}))²+{e}",[f"{-a}(x−({d}))²+{e}",f"{a}(x−({-d}))²+{e}",f"{a}(x−({d}))²−{e}"])
    return q(id_,'quadratisch','Graphen','Darstellen',3,'choice','Welche Scheitelpunktform passt zum Graphen?',ans,f"Der Scheitel liegt bei ({d}|{e}) und die Öffnung entspricht a={a}.",'Lies zuerst den Scheitelpunkt ab.','Prüfe danach Öffnungsrichtung und Breite.',opts,visual)
add_family('quadratisch','graph',9,qu_graph)

def qu_equiv(i,id_):
    d=rng.choice([2,3,4]); e=rng.choice([1,2,5]); # (x-d)^2+e = x2-2dx+d2+e
    corr=f"x² − {2*d}x + {d*d+e}"; opts,ans=mc(corr,[f"x² − {d}x + {d*d+e}",f"x² + {2*d}x + {d*d+e}",f"x² − {2*d}x + {e}"])
    return q(id_,'quadratisch','Formwechsel','Operieren',3,'choice',f"Welche Normalform gehört zu (x−{d})²+{e}?",ans,f"(x−{d})²=x²−{2*d}x+{d*d}; plus {e} ergibt {corr}.",'Nutze die binomische Formel.','Vergiss den konstanten Summanden +e nicht.',opts)
add_family('quadratisch','formwechsel',9,qu_equiv)

def qu_area(i,id_):
    total=rng.choice([10,12,14,16]); x=rng.choice([2,3,4]); area=x*(total-2*x)
    return q(id_,'quadratisch','Flächenmodell','Modellieren',4,'number',f"Ein Rechteck liegt an einer Mauer. Für die drei freien Seiten stehen {total} m Zaun zur Verfügung. Wenn die beiden kurzen Seiten je {x} m lang sind, wie groß ist die Fläche?",answer_num(area,0.01,'m²'),f"Lange Seite = {total}−2·{x}={total-2*x} m. Fläche={x}·{total-2*x}={area} m².",'Drücke zuerst die lange Seite durch x aus.','A=x·({total}−2x).'.replace('{total}',str(total)))
add_family('quadratisch','flaeche',9,qu_area)

# --- Wachstum ---
def wa_factor(i,id_):
    p=rng.choice([3,5,8,10,12,15,20]); qv=1+p/100
    return q(id_,'wachstum','Wachstumsfaktor','Operieren',1,'number',f"Bestimme den Wachstumsfaktor bei einer Zunahme um {p} %.",answer_num(qv,0.001),f"q=1+{p}/100={fmt(qv)}.",'Bei Wachstum beginnt der Faktor mit 1.','Addiere den Prozentsatz als Dezimalzahl zu 1.')
add_family('wachstum','faktor',9,wa_factor)

def wa_decay(i,id_):
    p=rng.choice([5,10,15,20,25]); qv=1-p/100
    return q(id_,'wachstum','Abnahmefaktor','Operieren',1,'number',f"Bestimme den Faktor bei einer Abnahme um {p} %.",answer_num(qv,0.001),f"q=1−{p}/100={fmt(qv)}.",'Bei Abnahme wird der Prozentsatz von 1 abgezogen.','Der Faktor muss zwischen 0 und 1 liegen.')
add_family('wachstum','abnahmefaktor',9,wa_decay)

def wa_future(i,id_):
    a=rng.choice([50,80,100,200,500]); p=rng.choice([5,10,20,25]); n=rng.choice([2,3,4,5]); val=a*((1+p/100)**n)
    return q(id_,'wachstum','Exponentielles Modell','Modellieren',2,'number',f"Ein Bestand von {a} wächst pro Zeiteinheit um {p} %. Wie groß ist er nach {n} Zeiteinheiten? Runde auf eine Dezimalstelle.",answer_num(r1(val),0.11),f"N={a}·{fmt(1+p/100)}^{n}={r1(val)}.",'Nutze Anfangswert · Wachstumsfaktor^Zeit.','Der Wachstumsfaktor ist 1+p/100.')
add_family('wachstum','zukunft',9,wa_future)

def wa_decrease(i,id_):
    a=rng.choice([100,200,500,1000]); p=rng.choice([5,10,20]); n=rng.choice([2,3,4]); val=a*((1-p/100)**n)
    return q(id_,'wachstum','Exponentielle Abnahme','Modellieren',2,'number',f"Ein Wert von {a} sinkt je Periode um {p} %. Wie groß ist er nach {n} Perioden? Runde auf eine Dezimalstelle.",answer_num(r1(val),0.11),f"N={a}·{fmt(1-p/100)}^{n}={r1(val)}.",'Nutze einen Faktor kleiner als 1.','q=1−p/100.')
add_family('wachstum','abnahme',9,wa_decrease)

def wa_find_n(i,id_):
    a=rng.choice([20,50,100]); p=rng.choice([20,25,50]); threshold=rng.choice([200,300,500,800]); n=0
    while a*((1+p/100)**n)<=threshold: n+=1
    return q(id_,'wachstum','Schwellenwert','Problemlösen',4,'number',f"Ein Bestand startet bei {a} und wächst pro Schritt um {p} %. Nach wie vielen Schritten ist er erstmals größer als {threshold}?",answer_num(n,0),f"Systematisch prüfen: N(n)={a}·{fmt(1+p/100)}^n. Erstmals größer als {threshold} ist der Wert bei n={n}.",'Du musst keine Logarithmen verwenden.','Berechne nacheinander die Werte für n=1,2,3,… bis die Schwelle überschritten ist.')
add_family('wachstum','schwelle',9,wa_find_n)

def wa_compare(i,id_):
    a1=rng.choice([50,100]); q1=rng.choice([1.1,1.2]); a2=rng.choice([80,120]); q2=rng.choice([1.05,1.1]); n=rng.choice([3,4,5]); v1=a1*q1**n; v2=a2*q2**n; cor='Modell A' if v1>v2 else 'Modell B'; opts,ans=mc(cor,['Modell B' if cor=='Modell A' else 'Modell A','gleich groß','nicht bestimmbar'])
    return q(id_,'wachstum','Modelle vergleichen','Argumentieren',3,'choice',f"Nach {n} Perioden: Modell A startet mit {a1}, Faktor {q1}; Modell B startet mit {a2}, Faktor {q2}. Welches ist dann größer?",ans,f"A≈{r1(v1)}, B≈{r1(v2)}. Damit ist {cor} größer.",'Berechne beide Werte mit a·q^n.','Vergleiche erst nach derselben Anzahl an Perioden.',opts)
add_family('wachstum','vergleich',9,wa_compare)

def wa_linear_exp(i,id_):
    a=rng.choice([100,200]); add=rng.choice([20,30,50]); p=rng.choice([10,20,25]); n=rng.choice([3,4]); lin=a+add*n; exp=a*(1+p/100)**n; cor='linear' if lin>exp else 'exponentiell'; opts,ans=mc(cor,['exponentiell' if cor=='linear' else 'linear','gleich','nicht vergleichbar'])
    return q(id_,'wachstum','Linear vs. exponentiell','Argumentieren',3,'choice',f"Startwert {a}. Modell L wächst je Schritt um {add}; Modell E wächst je Schritt um {p} %. Welches Modell liefert nach {n} Schritten den größeren Wert?",ans,f"L={lin}; E≈{r1(exp)}. Daher ist {cor} größer.",'Lineares Wachstum addiert immer denselben Betrag.','Exponentielles Wachstum multipliziert immer mit demselben Faktor.',opts)
add_family('wachstum','linearvergleich',9,wa_linear_exp)

def wa_percent_from_factor(i,id_):
    qv=rng.choice([0.75,0.8,0.9,1.05,1.1,1.25]); p=(qv-1)*100
    return q(id_,'wachstum','Faktor interpretieren','Argumentieren',2,'number',f"Ein exponentielles Modell hat den Faktor q={qv}. Bestimme die prozentuale Änderung pro Schritt (Abnahme negativ).",answer_num(p,0.01,'%'),f"p=(q−1)·100=({qv}−1)·100={fmt(p)} %.",'Vergleiche q mit 1.','p=(q−1)·100 %.')
add_family('wachstum','faktorinterpret',9,wa_percent_from_factor)

def wa_graph(i,id_):
    a=rng.choice([1,2,3]); qv=rng.choice([0.5,0.8,1.2,1.5,2]); visual={"kind":"exponential","a":a,"q":qv,"xmin":0,"xmax":6,"ymin":0,"ymax":max(8,a*qv**6+1)}
    cor='wachsend' if qv>1 else 'fallend'; opts,ans=mc(cor,['fallend' if cor=='wachsend' else 'wachsend','linear','konstant'])
    return q(id_,'wachstum','Graphen','Darstellen',2,'choice','Wie verhält sich der dargestellte Exponentialgraph?',ans,f"Der Faktor q={qv}. {'q>1 → wachsend.' if qv>1 else '0<q<1 → fallend.'}",'Betrachte die Veränderung von links nach rechts.','Bei Exponentialfunktionen entscheidet q über Wachstum oder Abnahme.',opts,visual)
add_family('wachstum','graph',9,wa_graph)

def wa_context(i,id_):
    a=rng.choice([500,800,1200]); p=rng.choice([5,8,10]); n=rng.choice([2,3,4]); val=a*(1-p/100)**n
    return q(id_,'wachstum','Alltagsmodell','Modellieren',3,'number',f"Ein Akku hat rechnerisch {a} Ladezyklen Kapazitätswert. Pro Jahr sinkt dieser Modellwert um {p} %. Wie groß ist er nach {n} Jahren? Runde auf ganze Einheiten.",answer_num(round(val),1),f"{a}·{fmt(1-p/100)}^{n}≈{round(val)}.",'Es handelt sich um wiederholte prozentuale Abnahme.','Nutze den Abnahmefaktor q=1−p/100.')
add_family('wachstum','kontext',9,wa_context)

def wa_reverse(i,id_):
    a=rng.choice([100,200,500]); qv=rng.choice([1.1,1.2,1.25]); n=rng.choice([2,3]); end=a*qv**n
    return q(id_,'wachstum','Anfangswert','Problemlösen',3,'number',f"Nach {n} Perioden beträgt ein Bestand {r1(end)}. Der Wachstumsfaktor ist {qv}. Wie groß war der Anfangswert?",answer_num(a,0.2),f"a = Endwert / q^n = {r1(end)}/{qv}^{n} = {a}.",'Stelle N=a·q^n nach a um.','Teile den Endwert durch q^n.')
add_family('wachstum','rueckwaerts',9,wa_reverse)

def wa_absolute(i,id_):
    a=rng.choice([100,200]); p=rng.choice([10,20,25]); qv=1+p/100; n=rng.choice([2,3]); before=a*qv**(n-1); after=a*qv**n; diff=after-before
    return q(id_,'wachstum','Absolute Zunahme','Argumentieren',3,'number',f"N(n)={a}·{fmt(qv)}^n. Wie groß ist die absolute Zunahme vom Schritt {n-1} zum Schritt {n}?",answer_num(diff,0.05),f"N({n})−N({n-1})={fmt(after)}−{fmt(before)}={fmt(diff)}.",'Berechne zwei aufeinanderfolgende Funktionswerte.','Absolute Zunahme = späterer Wert − früherer Wert.')
add_family('wachstum','absolute',9,wa_absolute)

# --- Geometrie ---
def ge_rect(i,id_):
    a=rng.choice([4,5,6,8,10]); b=rng.choice([3,4,7,9]); A=a*b
    return q(id_,'geometrie','Flächeninhalt','Operieren',1,'number',f"Ein Rechteck ist {a} cm lang und {b} cm breit. Bestimme den Flächeninhalt.",answer_num(A,0,'cm²'),f"A=a·b={a}·{b}={A} cm².",'Flächeninhalt eines Rechtecks: Länge · Breite.','Achte auf die Einheit cm².')
add_family('geometrie','rechteck',9,ge_rect)

def ge_triangle(i,id_):
    g=rng.choice([6,8,10,12]); h=rng.choice([3,5,7,9]); A=g*h/2
    return q(id_,'geometrie','Dreiecksfläche','Operieren',1,'number',f"Ein Dreieck hat Grundseite g={g} cm und zugehörige Höhe h={h} cm. Bestimme die Fläche.",answer_num(A,0.01,'cm²'),f"A=g·h/2={g}·{h}/2={fmt(A)} cm².",'Dreiecksfläche ist die Hälfte von Grundseite · Höhe.','Nutze die zur Grundseite gehörende Höhe.')
add_family('geometrie','dreieck',9,ge_triangle)

def ge_circle(i,id_):
    r=rng.choice([2,3,4,5,6]); A=math.pi*r*r
    return q(id_,'geometrie','Kreis','Operieren',2,'number',f"Ein Kreis hat Radius {r} cm. Bestimme den Flächeninhalt. Runde auf eine Dezimalstelle.",answer_num(r1(A),0.11,'cm²'),f"A=πr²=π·{r}²≈{r1(A)} cm².",'Nutze A=πr².','Quadriere zuerst den Radius.')
add_family('geometrie','kreis',9,ge_circle)

def ge_sector(i,id_):
    r=rng.choice([4,6,8,10]); alpha=rng.choice([45,60,90,120,180]); A=math.pi*r*r*alpha/360
    return q(id_,'geometrie','Kreissektor','Operieren',3,'number',f"Ein Kreissektor hat r={r} cm und α={alpha}°. Bestimme seine Fläche. Runde auf eine Dezimalstelle.",answer_num(r1(A),0.11,'cm²'),f"A=α/360·πr²={alpha}/360·π·{r}²≈{r1(A)} cm².",'Der Sektor ist der Anteil α/360 des ganzen Kreises.','Berechne zuerst die Kreisfläche und multipliziere mit α/360.')
add_family('geometrie','sektor',9,ge_sector)

def ge_pyth(i,id_):
    triples=[(3,4,5),(5,12,13),(6,8,10),(8,15,17),(7,24,25)]; a,b,c=rng.choice(triples)
    return q(id_,'geometrie','Satz des Pythagoras','Operieren',2,'number',f"Ein rechtwinkliges Dreieck hat Katheten {a} cm und {b} cm. Bestimme die Hypotenuse.",answer_num(c,0.01,'cm'),f"c=√({a}²+{b}²)=√{a*a+b*b}={c} cm.",'Die Hypotenuse liegt dem rechten Winkel gegenüber.','Nutze c²=a²+b².')
add_family('geometrie','pythagoras',9,ge_pyth)

def ge_trig_len(i,id_):
    alpha=rng.choice([30,35,40,45,50,60]); hyp=rng.choice([8,10,12,15]); opp=hyp*math.sin(math.radians(alpha))
    return q(id_,'geometrie','Trigonometrie Länge','Operieren',3,'number',f"In einem rechtwinkligen Dreieck ist die Hypotenuse {hyp} cm lang und α={alpha}°. Bestimme die Gegenkathete zu α. Runde auf eine Dezimalstelle.",answer_num(r1(opp),0.11,'cm'),f"sin(α)=Gegenkathete/Hypotenuse ⇒ g={hyp}·sin({alpha}°)≈{r1(opp)} cm.",'Welche trigonometrische Funktion verknüpft Gegenkathete und Hypotenuse?','sin(α)=Gegenkathete/Hypotenuse.')
add_family('geometrie','triglaenge',9,ge_trig_len)

def ge_trig_angle(i,id_):
    opp=rng.choice([3,4,5,6,8]); adj=rng.choice([4,5,7,8,10]); alpha=math.degrees(math.atan(opp/adj))
    return q(id_,'geometrie','Trigonometrie Winkel','Operieren',3,'number',f"Gegenkathete={opp} cm, Ankathete={adj} cm. Bestimme α. Runde auf ganze Grad.",answer_num(round(alpha),1,'°'),f"tan(α)={opp}/{adj}. Daher α=arctan({opp}/{adj})≈{round(alpha)}°.",'Für Gegenkathete und Ankathete eignet sich der Tangens.','Nutze die Umkehrfunktion tan⁻¹.')
add_family('geometrie','trigwinkel',9,ge_trig_angle)

def ge_similarity(i,id_):
    k=rng.choice([0.5,1.5,2,2.5,3]); old=rng.choice([4,6,8,10]); new=old*k
    return q(id_,'geometrie','Ähnlichkeit','Modellieren',2,'number',f"Bei einer zentrischen Streckung mit Faktor k={k} ist eine Originalstrecke {old} cm lang. Wie lang ist die Bildstrecke?",answer_num(new,0.01,'cm'),f"Bildlänge=k·Originallänge={k}·{old}={fmt(new)} cm.",'Alle Längen werden mit demselben Faktor multipliziert.','Nutze Bild = k · Original.')
add_family('geometrie','aehnlichkeit',9,ge_similarity)

def ge_ring(i,id_):
    R=rng.choice([5,6,8,10]); r=R-rng.choice([1,2,3]); A=math.pi*(R*R-r*r)
    return q(id_,'geometrie','Kreisring','Operieren',3,'number',f"Ein Kreisring hat Außenradius {R} cm und Innenradius {r} cm. Bestimme die Fläche. Runde auf eine Dezimalstelle.",answer_num(r1(A),0.11,'cm²'),f"A=π(R²−r²)=π({R}²−{r}²)≈{r1(A)} cm².",'Ziehe die Fläche des inneren Kreises von der äußeren ab.','A=πR²−πr².')
add_family('geometrie','kreisring',9,ge_ring)

def ge_compound(i,id_):
    a=rng.choice([8,10,12]); b=rng.choice([6,8]); cut=rng.choice([2,3,4]); A=a*b-cut*cut
    return q(id_,'geometrie','Zusammengesetzte Flächen','Modellieren',3,'number',f"Aus einem Rechteck {a} cm × {b} cm wird ein Quadrat {cut} cm × {cut} cm herausgeschnitten. Bestimme die verbleibende Fläche.",answer_num(A,0,'cm²'),f"A={a}·{b}−{cut}²={a*b}−{cut*cut}={A} cm².",'Berechne Gesamtfläche minus ausgeschnittene Fläche.','Beide Teilflächen sind Rechtecke/Quadrate.')
add_family('geometrie','zusammengesetzt',9,ge_compound)

def ge_scale(i,id_):
    k=rng.choice([1.5,2,3]); A=rng.choice([12,20,30,45]); new=A*k*k
    return q(id_,'geometrie','Flächen bei Streckung','Argumentieren',4,'number',f"Eine Figur mit Fläche {A} cm² wird mit Faktor k={k} gestreckt. Wie groß ist die neue Fläche?",answer_num(new,0.01,'cm²'),f"Flächen skalieren mit k²: {A}·{k}²={fmt(new)} cm².",'Bei Längen gilt k, bei Flächen nicht.','Flächenfaktor = k².')
add_family('geometrie','flaechenstreckung',9,ge_scale)

def ge_distance(i,id_):
    x1,y1=0,0; x2,y2=rng.choice([(3,4),(5,12),(6,8),(8,15)]); d=math.hypot(x2-x1,y2-y1)
    return q(id_,'geometrie','Koordinatengeometrie','Problemlösen',3,'number',f"Bestimme den Abstand zwischen A(0|0) und B({x2}|{y2}).",answer_num(d,0.01),f"Der Abstand ist die Hypotenuse: d=√({x2}²+{y2}²)={fmt(d)}.",'Zeichne gedanklich ein rechtwinkliges Dreieck.','Nutze den Satz des Pythagoras mit Δx und Δy.')
add_family('geometrie','abstand',9,ge_distance)

# --- Körper ---
def ko_quader(i,id_):
    a,b,c=rng.choice([(4,5,6),(5,6,8),(3,7,10),(8,9,12)]); V=a*b*c
    return q(id_,'koerper','Quader','Operieren',1,'number',f"Ein Quader ist {a} cm × {b} cm × {c} cm groß. Bestimme das Volumen.",answer_num(V,0,'cm³'),f"V=a·b·c={a}·{b}·{c}={V} cm³.",'Volumen eines Quaders = Länge · Breite · Höhe.','Achte auf cm³.')
add_family('koerper','quader',9,ko_quader)

def ko_cyl(i,id_):
    r=rng.choice([2,3,4,5]); h=rng.choice([5,8,10,12]); V=math.pi*r*r*h
    return q(id_,'koerper','Zylinder','Operieren',2,'number',f"Ein Zylinder hat r={r} cm und h={h} cm. Bestimme sein Volumen. Runde auf eine Dezimalstelle.",answer_num(r1(V),0.11,'cm³'),f"V=πr²h=π·{r}²·{h}≈{r1(V)} cm³.",'Grundfläche ist ein Kreis.','V=G·h mit G=πr².')
add_family('koerper','zylinder',9,ko_cyl)

def ko_pyr(i,id_):
    a=rng.choice([4,6,8,10]); h=rng.choice([6,9,12]); V=a*a*h/3
    return q(id_,'koerper','Pyramide','Operieren',2,'number',f"Eine quadratische Pyramide hat Grundkante {a} cm und Höhe {h} cm. Bestimme das Volumen.",answer_num(V,0.01,'cm³'),f"G={a}²={a*a}; V=1/3·G·h=1/3·{a*a}·{h}={fmt(V)} cm³.",'Volumen einer Pyramide ist ein Drittel von Grundfläche · Höhe.','Berechne zuerst die quadratische Grundfläche.')
add_family('koerper','pyramide',9,ko_pyr)

def ko_cone(i,id_):
    r=rng.choice([3,4,5]); h=rng.choice([6,9,12]); V=math.pi*r*r*h/3
    return q(id_,'koerper','Kegel','Operieren',2,'number',f"Ein Kegel hat r={r} cm und h={h} cm. Bestimme das Volumen. Runde auf eine Dezimalstelle.",answer_num(r1(V),0.11,'cm³'),f"V=1/3·πr²h≈{r1(V)} cm³.",'Kegelvolumen = ein Drittel des entsprechenden Zylinders.','V=1/3·πr²h.')
add_family('koerper','kegel',9,ko_cone)

def ko_sphere(i,id_):
    r=rng.choice([2,3,4,5]); V=4/3*math.pi*r**3
    return q(id_,'koerper','Kugel','Operieren',3,'number',f"Eine Kugel hat r={r} cm. Bestimme das Volumen. Runde auf eine Dezimalstelle.",answer_num(r1(V),0.11,'cm³'),f"V=4/3·π·r³=4/3·π·{r}³≈{r1(V)} cm³.",'Nutze die Kugelvolumenformel.','Der Radius wird hoch 3 genommen.')
add_family('koerper','kugel',9,ko_sphere)

def ko_surface_cyl(i,id_):
    r=rng.choice([2,3,4]); h=rng.choice([5,8,10]); O=2*math.pi*r*r+2*math.pi*r*h
    return q(id_,'koerper','Oberfläche Zylinder','Operieren',3,'number',f"Ein geschlossener Zylinder hat r={r} cm und h={h} cm. Bestimme die Oberfläche. Runde auf eine Dezimalstelle.",answer_num(r1(O),0.11,'cm²'),f"O=2πr²+2πrh≈{r1(O)} cm².",'Oberfläche = zwei Kreisflächen + Mantelfläche.','Mantel M=Umfang·Höhe=2πr·h.')
add_family('koerper','oberflaeche',9,ko_surface_cyl)

def ko_density(i,id_):
    V=rng.choice([0.4,0.6,0.8,1.2,1.5]); rho=rng.choice([0.8,1.2,2.7,7.8]); m=V*rho
    return q(id_,'koerper','Dichte & Masse','Modellieren',3,'number',f"Ein Körper hat Volumen {V} m³ und Dichte {rho} t/m³. Bestimme die Masse.",answer_num(m,0.01,'t'),f"m=ρ·V={rho}·{V}={fmt(m)} t.",'Dichte bedeutet Masse pro Volumen.','m=ρ·V.')
add_family('koerper','dichte',9,ko_density)

def ko_hollow(i,id_):
    R=rng.choice([5,6,8]); r=R-rng.choice([1,2]); V=4/3*math.pi*(R**3-r**3)
    return q(id_,'koerper','Hohlkörper','Modellieren',4,'number',f"Eine kugelförmige Hülle hat Außenradius {R} cm und Innenradius {r} cm. Bestimme das Materialvolumen. Runde auf eine Dezimalstelle.",answer_num(r1(V),0.11,'cm³'),f"V_Material=4/3·π·({R}³−{r}³)≈{r1(V)} cm³.",'Außenvolumen minus Innenvolumen.','Nutze zweimal die Kugelvolumenformel.')
add_family('koerper','hohlkugel',9,ko_hollow)

def ko_water(i,id_):
    G=rng.choice([200,250,300,400]); delta=rng.choice([2,3,4,5]); V=G*delta
    return q(id_,'koerper','Wasserverdrängung','Modellieren',3,'number',f"In einem Gefäß mit konstanter Grundfläche {G} cm² steigt der Wasserstand beim Eintauchen eines Körpers um {delta} cm. Bestimme das Körpervolumen.",answer_num(V,0,'cm³'),f"Verdrängtes Volumen=G·Δh={G}·{delta}={V} cm³.",'Das verdrängte Wasservolumen entspricht dem Körpervolumen.','V=Grundfläche·Höhenänderung.')
add_family('koerper','verdrängung',9,ko_water)

def ko_packing(i,id_):
    box=rng.choice([20000,30000,40000]); item=rng.choice([800,1000,1250]); ideal=box/item; realistic=math.floor(ideal*0.8)
    return q(id_,'koerper','Modellannahmen','Argumentieren',4,'number',f"Ein Karton hat {box} cm³ Volumen. Ein ungefähr kugelförmiger Gegenstand braucht rechnerisch {item} cm³. Schätze mit 80 % Packungsgrad die Anzahl ganzer Gegenstände.",answer_num(realistic,0),f"N≈{box}/{item}·0,8={fmt(ideal*0.8)}. Ganze Gegenstände: {realistic}.",'Das reine Volumenverhältnis überschätzt die Anzahl.','Berücksichtige den Packungsgrad und runde auf ganze Gegenstände ab.')
add_family('koerper','packen',9,ko_packing)

def ko_scale(i,id_):
    k=rng.choice([1.5,2,3]); V=rng.choice([50,100,200]); new=V*k**3
    return q(id_,'koerper','Volumen bei Streckung','Argumentieren',4,'number',f"Ein Körper mit Volumen {V} cm³ wird in allen Längen mit Faktor {k} vergrößert. Bestimme das neue Volumen.",answer_num(new,0.01,'cm³'),f"Volumen skaliert mit k³: {V}·{k}³={fmt(new)} cm³.",'Bei räumlichen Körpern wirkt der Streckfaktor dreifach.','Volumenfaktor = k³.')
add_family('koerper','streckung',9,ko_scale)

def ko_reverse(i,id_):
    r=rng.choice([2,3,4,5]); V=math.pi*r*r*rng.choice([5,8,10]); h=V/(math.pi*r*r)
    return q(id_,'koerper','Rückwärtsrechnen','Problemlösen',3,'number',f"Ein Zylinder hat Volumen {r1(V)} cm³ und Radius {r} cm. Bestimme die Höhe. Runde auf eine Dezimalstelle.",answer_num(r1(h),0.11,'cm'),f"h=V/(πr²)={r1(V)}/(π·{r}²)≈{r1(h)} cm.",'Stelle V=πr²h nach h um.','Teile das Volumen durch die Grundfläche.')
add_family('koerper','rueckwaerts',9,ko_reverse)

# --- Statistik ---
def st_mean(i,id_):
    vals=[rng.randint(2,20) for _ in range(5)]; m=sum(vals)/5
    return q(id_,'statistik','Arithmetisches Mittel','Operieren',1,'number',f"Bestimme den Mittelwert der Daten: {', '.join(map(str,vals))}.",answer_num(m,0.01),f"Summe={sum(vals)}, Anzahl=5, Mittelwert={fmt(m)}.",'Addiere alle Werte und teile durch ihre Anzahl.','Mittelwert = Summe / n.')
add_family('statistik','mittelwert',9,st_mean)

def st_median(i,id_):
    vals=[rng.randint(1,30) for _ in range(rng.choice([5,7]))]; med=median(vals)
    return q(id_,'statistik','Median','Operieren',1,'number',f"Bestimme den Median: {', '.join(map(str,vals))}.",answer_num(med,0.01),f"Sortiert: {', '.join(map(str,sorted(vals)))}. Der mittlere Wert ist {fmt(med)}.",'Sortiere die Daten zuerst.','Bei ungerader Anzahl ist der mittlere Wert der Median.')
add_family('statistik','median',9,st_median)

def st_range(i,id_):
    vals=[rng.randint(5,50) for _ in range(6)]; span=max(vals)-min(vals)
    return q(id_,'statistik','Spannweite','Operieren',1,'number',f"Bestimme die Spannweite: {', '.join(map(str,vals))}.",answer_num(span,0),f"Maximum={max(vals)}, Minimum={min(vals)}. Spannweite={max(vals)}−{min(vals)}={span}.",'Spannweite = größter Wert − kleinster Wert.','Suche Minimum und Maximum.')
add_family('statistik','spannweite',9,st_range)

def st_relative(i,id_):
    total=rng.choice([40,50,80,100,120]); count=rng.randint(5,total//2); rel=count/total
    return q(id_,'statistik','Relative Häufigkeit','Operieren',2,'number',f"{count} von {total} Beobachtungen haben Merkmal A. Bestimme die relative Häufigkeit als Dezimalzahl.",answer_num(rel,0.001),f"h_rel={count}/{total}={fmt(rel)}.",'Relative Häufigkeit = absolute Häufigkeit / Gesamtzahl.','Teile {count} durch {total}.'.replace('{count}',str(count)).replace('{total}',str(total)))
add_family('statistik','relativ',9,st_relative)

def st_quartile(i,id_):
    vals=sorted([rng.randint(1,30) for _ in range(8)]); lower=median(vals[:4]); upper=median(vals[4:]); ask='unteres' if i%2==0 else 'oberes'; val=lower if ask=='unteres' else upper
    return q(id_,'statistik','Quartile','Operieren',3,'number',f"Geordnete Daten: {', '.join(map(str,vals))}. Bestimme das {ask} Quartil.",answer_num(val,0.01),f"{ask.capitalize()} Quartil = Median der {'unteren' if ask=='unteres' else 'oberen'} Hälfte = {fmt(val)}.",'Teile die Rangliste in zwei Hälften.','Bestimme den Median der passenden Hälfte.')
add_family('statistik','quartil',9,st_quartile)

def st_effect(i,id_):
    vals=[10,12,13,15,16]; old=mean(vals); newval=rng.choice([20,25,30]); new=mean(vals+[newval]); change=new-old
    return q(id_,'statistik','Einfluss einzelner Werte','Argumentieren',3,'number',f"Die Werte {vals} haben einen Mittelwert von {fmt(old)}. Ein weiterer Wert {newval} kommt hinzu. Um wie viel verändert sich der Mittelwert?",answer_num(change,0.01),f"Neuer Mittelwert=({sum(vals)}+{newval})/6={fmt(new)}. Änderung={fmt(new)}−{fmt(old)}={fmt(change)}.",'Berechne den neuen Mittelwert vollständig.','Ziehe danach den alten Mittelwert ab.')
add_family('statistik','einfluss',9,st_effect)

def st_compare(i,id_):
    A=[5,5,5,15,20]; B=[9,9,10,10,12]; opts,ans=mc('B ist gleichmäßiger',[ 'A ist gleichmäßiger','beide gleich','nicht bestimmbar'])
    return q(id_,'statistik','Verteilungen vergleichen','Argumentieren',3,'choice',f"Datensatz A: {A}; Datensatz B: {B}. Welcher Datensatz streut weniger?",ans,f"Spannweite A={max(A)-min(A)}, B={max(B)-min(B)}. B streut deutlich weniger.",'Vergleiche zum Beispiel die Spannweiten.','Kleinere Spannweite bedeutet hier geringere Streuung.',opts)
add_family('statistik','vergleich',9,st_compare)

def st_weighted(i,id_):
    a=rng.choice([2,3,4]); b=rng.choice([4,5,6]); na=rng.choice([2,3]); nb=rng.choice([2,4]); m=(a*na+b*nb)/(na+nb)
    return q(id_,'statistik','Gewichteter Mittelwert','Problemlösen',3,'number',f"Ein Wert {a} tritt {na}-mal auf, ein Wert {b} tritt {nb}-mal auf. Bestimme den Mittelwert.",answer_num(m,0.01),f"Mittelwert=({a}·{na}+{b}·{nb})/({na}+{nb})={fmt(m)}.",'Berücksichtige, wie oft jeder Wert vorkommt.','Multipliziere Wert · Häufigkeit, addiere und teile durch Gesamtanzahl.')
add_family('statistik','gewichtet',9,st_weighted)

def st_chart(i,id_):
    vals=[rng.randint(5,25) for _ in range(4)]; labels=['A','B','C','D']; maxidx=max(range(4),key=lambda j:vals[j]); visual={"kind":"bars","labels":labels,"values":vals}; opts,ans=mc(labels[maxidx],[l for l in labels if l!=labels[maxidx]])
    return q(id_,'statistik','Diagramme lesen','Darstellen',2,'choice','Welche Kategorie hat im Diagramm den größten Wert?',ans,f"Der höchste Balken gehört zu {labels[maxidx]} ({vals[maxidx]}).",'Vergleiche die Balkenhöhen.','Der höchste Balken zeigt das Maximum.',opts,visual)
add_family('statistik','diagramm',9,st_chart)

def st_sample(i,id_):
    opts,ans=mc('Eine größere, zufällig ausgewählte Stichprobe ist meist aussagekräftiger',[ 'Je kleiner die Stichprobe, desto sicherer','Nur der Mittelwert entscheidet','Zufällige Auswahl ist unwichtig'])
    return q(id_,'statistik','Datenerhebung','Argumentieren',3,'choice','Welche Aussage zur Qualität einer Umfrage ist am sinnvollsten?',ans,'Größe und zufällige, passende Auswahl der Stichprobe beeinflussen die Aussagekraft.', 'Denke an Repräsentativität und Zufallsauswahl.','Eine verzerrte Auswahl kann auch bei vielen Personen irreführen.',opts)
add_family('statistik','stichprobe',9,st_sample)

def st_percent(i,id_):
    vals=[rng.randint(10,50) for _ in range(4)]; total=sum(vals); idx=i%4; p=vals[idx]/total*100
    return q(id_,'statistik','Anteile aus Daten','Modellieren',2,'number',f"Vier Kategorien haben Häufigkeiten {vals}. Welchen prozentualen Anteil hat die {idx+1}. Kategorie? Runde auf eine Dezimalstelle.",answer_num(r1(p),0.11,'%'),f"Anteil={vals[idx]}/{total}·100≈{r1(p)} %.",'Addiere zuerst alle Häufigkeiten.','Anteil / Gesamtzahl · 100.')
add_family('statistik','anteil',9,st_percent)

def st_box(i,id_):
    vals=sorted([rng.randint(1,40) for _ in range(9)]); med=median(vals); opts,ans=mc(str(med),[str(vals[0]),str(vals[-1]),str(max(vals)-min(vals))]); visual={"kind":"box","values":vals}
    return q(id_,'statistik','Boxplot','Darstellen',3,'choice','Welcher Wert ist der Median der dargestellten Daten?',ans,f"Die geordneten Daten sind {vals}; bei 9 Werten ist der 5. Wert der Median: {med}.",'Der Median teilt die Daten in zwei Hälften.','Bei neun Werten ist der fünfte Wert der Median.',opts,visual)
add_family('statistik','boxplot',9,st_box)

# --- Wahrscheinlichkeit ---
def wh_laplace(i,id_):
    sides=rng.choice([6,8,10,12]); fav=rng.randint(1,sides-1); p=fav/sides
    return q(id_,'wahrscheinlichkeit','Laplace','Operieren',1,'number',f"Bei einem Laplace-Experiment gibt es {sides} gleich wahrscheinliche Ergebnisse, davon {fav} günstig. Bestimme P(E) als Dezimalzahl.",answer_num(p,0.001),f"P(E)={fav}/{sides}={fmt(p)}.",'Günstige Ergebnisse durch alle möglichen Ergebnisse.','Bei Laplace sind alle Einzelergebnisse gleich wahrscheinlich.')
add_family('wahrscheinlichkeit','laplace',9,wh_laplace)

def wh_die(i,id_):
    threshold=rng.choice([3,4,5]); fav=6-threshold+1; p=fav/6
    return q(id_,'wahrscheinlichkeit','Würfel','Modellieren',1,'number',f"Ein fairer Würfel wird einmal geworfen. Bestimme P(Augenzahl ≥ {threshold}).",answer_num(p,0.001),f"Günstig sind {list(range(threshold,7))}: {fav} von 6. P={fav}/6={fmt(p)}.",'Liste die günstigen Augenzahlen auf.','Teile ihre Anzahl durch 6.')
add_family('wahrscheinlichkeit','wuerfel',9,wh_die)

def wh_complement(i,id_):
    p=rng.choice([0.1,0.2,0.25,0.3,0.4,0.6]); comp=1-p
    return q(id_,'wahrscheinlichkeit','Gegenereignis','Operieren',2,'number',f"P(E)={p}. Bestimme P(nicht E).",answer_num(comp,0.001),f"P(nicht E)=1−P(E)=1−{p}={fmt(comp)}.",'Ereignis und Gegenereignis ergeben zusammen 1.','Rechne 1−p.')
add_family('wahrscheinlichkeit','gegenereignis',9,wh_complement)

def wh_two(i,id_):
    p=rng.choice([0.2,0.25,0.4,0.5,0.6]); val=p*p
    return q(id_,'wahrscheinlichkeit','Pfadregel Produkt','Operieren',2,'number',f"Bei zwei unabhängigen Versuchen gilt jeweils P(E)={p}. Bestimme P(E tritt zweimal ein).",answer_num(val,0.001),f"1. Pfadregel: {p}·{p}={fmt(val)}.",'Entlang eines Pfades werden Wahrscheinlichkeiten multipliziert.','Unabhängige Wiederholung: p².')
add_family('wahrscheinlichkeit','produkt',9,wh_two)

def wh_atleast(i,id_):
    p=rng.choice([0.2,0.25,0.4,0.5]); none=(1-p)**2; val=1-none
    return q(id_,'wahrscheinlichkeit','Mindestens einmal','Problemlösen',3,'number',f"Bei zwei unabhängigen Versuchen gilt P(E)={p}. Bestimme P(E tritt mindestens einmal ein).",answer_num(val,0.001),f"Gegenereignis: kein E zweimal = (1−{p})²={fmt(none)}. Daher 1−{fmt(none)}={fmt(val)}.",'„Mindestens einmal“ ist oft leichter über das Gegenereignis.','Berechne 1−P(kein Treffer).')
add_family('wahrscheinlichkeit','mindestens',9,wh_atleast)

def wh_without(i,id_):
    total=10; red=rng.choice([3,4,5,6]); val=(red/total)*((red-1)/(total-1))
    return q(id_,'wahrscheinlichkeit','Ohne Zurücklegen','Modellieren',3,'number',f"In einer Box liegen {red} rote und {total-red} blaue Kugeln. Zweimal wird ohne Zurücklegen gezogen. Bestimme P(zweimal rot). Runde auf drei Dezimalstellen.",answer_num(round(val,3),0.0015),f"P=({red}/{total})·({red-1}/{total-1})≈{round(val,3)}.",'Beim zweiten Zug sind Gesamtzahl und Zahl roter Kugeln verändert.','Multipliziere die beiden Pfadwahrscheinlichkeiten.')
add_family('wahrscheinlichkeit','ohnezurueck',9,wh_without)

def wh_sumrule(i,id_):
    p1=rng.choice([0.1,0.2,0.25]); p2=rng.choice([0.15,0.3,0.4]); val=p1+p2
    return q(id_,'wahrscheinlichkeit','Pfadregel Summe','Operieren',2,'number',f"Zwei disjunkte Wege führen zum Ereignis E mit Wahrscheinlichkeiten {p1} und {p2}. Bestimme P(E).",answer_num(val,0.001),f"2. Pfadregel: {p1}+{p2}={fmt(val)}.",'Wenn mehrere disjunkte Pfade zum Ereignis gehören, werden ihre Wahrscheinlichkeiten addiert.','Addiere die Pfadwahrscheinlichkeiten.')
add_family('wahrscheinlichkeit','summe',9,wh_sumrule)

def wh_expected(i,id_):
    n=rng.choice([50,100,200,500]); p=rng.choice([0.1,0.2,0.25,0.4]); val=n*p
    return q(id_,'wahrscheinlichkeit','Erwartete Häufigkeit','Modellieren',2,'number',f"Ein Ereignis hat Wahrscheinlichkeit {p}. Wie oft erwartet man es ungefähr bei {n} Wiederholungen?",answer_num(val,0.01),f"Erwartete Häufigkeit≈n·p={n}·{p}={fmt(val)}.",'Wahrscheinlichkeit mal Anzahl der Versuche.','n·p liefert eine erwartete Häufigkeit, keinen sicheren Wert.')
add_family('wahrscheinlichkeit','erwartung',9,wh_expected)

def wh_empirical(i,id_):
    n=rng.choice([100,200,500]); k=rng.randint(20,n-20); val=k/n
    return q(id_,'wahrscheinlichkeit','Relative Häufigkeit','Interpretieren',2,'number',f"In {n} Versuchen tritt ein Ereignis {k}-mal ein. Bestimme die relative Häufigkeit.",answer_num(val,0.001),f"h_rel={k}/{n}={fmt(val)}.",'Teile die Trefferzahl durch die Versuchszahl.','Die relative Häufigkeit ist eine Dezimalzahl zwischen 0 und 1.')
add_family('wahrscheinlichkeit','relativ',9,wh_empirical)

def wh_fair(i,id_):
    winp=rng.choice([0.2,0.25,0.4,0.5]); prize=rng.choice([4,5,8,10]); cost=winp*prize; asked=r2(cost)
    return q(id_,'wahrscheinlichkeit','Faires Spiel','Modellieren',4,'number',f"Ein Spiel zahlt mit Wahrscheinlichkeit {winp} einen Gewinn von {prize} € aus, sonst 0 €. Welcher Einsatz macht den Erwartungswert 0?",answer_num(asked,0.02,'€'),f"Erwartete Auszahlung={winp}·{prize}={fmt(cost)} €. Ein fairer Einsatz entspricht diesem Wert.",'Berechne die mittlere Auszahlung.','Fair bedeutet: erwartete Auszahlung = Einsatz.')
add_family('wahrscheinlichkeit','fair',9,wh_fair)

def wh_tree_context(i,id_):
    p=rng.choice([0.3,0.4,0.6,0.7]); val=p*(1-p)+(1-p)*p
    return q(id_,'wahrscheinlichkeit','Baumdiagramm','Problemlösen',3,'number',f"Ein Versuch mit Trefferwahrscheinlichkeit {p} wird zweimal unabhängig wiederholt. Bestimme die Wahrscheinlichkeit für genau einen Treffer.",answer_num(val,0.001),f"Genau ein Treffer: T–N oder N–T. P={p}·{fmt(1-p)}+{fmt(1-p)}·{p}={fmt(val)}.",'Es gibt zwei passende Pfade.','Multipliziere entlang jedes Pfades und addiere beide Pfade.')
add_family('wahrscheinlichkeit','baum',9,wh_tree_context)

def wh_two_dice(i,id_):
    target=rng.choice([5,6,7,8,9]); fav=sum(1 for a in range(1,7) for b in range(1,7) if a+b==target); p=fav/36
    return q(id_,'wahrscheinlichkeit','Zwei Würfel','Problemlösen',3,'number',f"Zwei faire Würfel werden geworfen. Bestimme P(Augensumme={target}). Runde auf drei Dezimalstellen.",answer_num(round(p,3),0.0015),f"Es gibt 36 geordnete Ergebnisse, davon {fav} mit Summe {target}. P={fav}/36≈{round(p,3)}.",'Bei zwei Würfeln gibt es 6·6=36 gleich wahrscheinliche geordnete Ergebnisse.','Zähle die Zahlenpaare mit der gewünschten Summe.')
add_family('wahrscheinlichkeit','zweierwuerfel',9,wh_two_dice)

# A few tasks deliberately use current public facts found during the requested web research.
# They replace generated variants, so every topic still contains exactly 108 regular tasks.
_live = next(x for x in tasks if x['id']=='prozent-vergleich-09')
_live.update(q(_live['id'],'prozent','Preisvergleich','Modellieren',3,'number',
    'Das Deutschlandticket kostet seit Januar 2026 monatlich 63 €. Ein Arbeitgeber übernimmt hypothetisch 25 % des Preises. Wie viel zahlt die Person selbst pro Monat?',
    answer_num(47.25,0.02,'€'),'25 % von 63 € sind 15,75 €. Selbst zu zahlen: 63 € − 15,75 € = 47,25 €.',
    'Berechne zuerst den übernommenen Anteil.','Nach 25 % Zuschuss bleiben 75 % des Ticketpreises.',
    source={'label':'Bundesregierung – Deutschlandticket, Stand 01.05.2026','url':'https://www.bundesregierung.de/breg-de/bundesregierung/bundeskanzleramt/deutschlandticket-2134074'}))
_live = next(x for x in tasks if x['id']=='statistik-diagramm-09')
_live.update(q(_live['id'],'statistik','Daten interpretieren','Interpretieren',3,'number',
    'Der Anteil erneuerbarer Energien am deutschen Bruttostromverbrauch lag 2024 bei 54,4 % und 2025 bei 55,1 %. Um wie viele Prozentpunkte stieg der Anteil?',
    answer_num(0.7,0.01,'Prozentpunkte'),'55,1 − 54,4 = 0,7 Prozentpunkte.',
    'Bei Prozentpunkten werden die beiden Prozentwerte voneinander abgezogen.','Berechne 55,1 − 54,4.',
    source={'label':'Umweltbundesamt – Erneuerbare Energien in Deutschland 2025','url':'https://www.umweltbundesamt.de/themen/klima-energie/erneuerbare-energien/erneuerbare-energien-in-zahlen'}))

# --- Challenge tasks, 8 per topic, drawn as separate original multi-step contexts ---
challenge=[]
for ti,t in enumerate(TOPICS):
    for j in range(8):
        seed=1000+ti*50+j
        rr=random.Random(seed)
        if t['id']=='zahlen':
            km=rr.choice([12,18,24]); pace=rr.choice([15,20,30]); mins=km*pace/rr.choice([3,4,6]); prompt=f"Eine Radtour ist {km} km lang. Ein Plan teilt die Strecke im Verhältnis 1:{rr.choice([50000,100000])} ab. Für die reale Strecke werden im Mittel {pace} Minuten pro 5 km angesetzt. Schätze die Fahrzeit in Minuten für die gesamte Strecke."; val=km/5*pace
            sol=f"Pro 5 km {pace} min; {km}/5·{pace}={fmt(val)} min."
        elif t['id']=='algebra':
            adult=rr.randint(8,14); child=rr.randint(5,9); na=rr.randint(10,20); nc=rr.randint(10,25); total=adult*na+child*nc; prompt=f"Bei einer Schulveranstaltung kostet ein Erwachsenenticket {adult} €, ein Jugendticket {child} €. Insgesamt werden {na+nc} Tickets verkauft und {total} € eingenommen. Wie viele Erwachsenentickets wurden verkauft?"; val=na; sol=f"x+y={na+nc}, {adult}x+{child}y={total}. Lösen ergibt x={na}."
        elif t['id']=='prozent':
            price=rr.choice([120,160,200]); d=rr.choice([15,20]); vat=rr.choice([5,10]); val=price*(1-d/100)*(1+vat/100); prompt=f"Ein Preis von {price} € wird zuerst um {d} % reduziert. Anschließend steigt der reduzierte Preis um {vat} %. Bestimme den Endpreis."; sol=f"{price}·{1-d/100}·{1+vat/100}={r2(val)} €."
        elif t['id']=='linear':
            a0=rr.choice([5,8,10]); a1=rr.choice([2,3]); b0=rr.choice([15,20]); b1=rr.choice([0.5,1]); val=(b0-a0)/(a1-b1); prompt=f"Tarif A kostet {a0} € Grundpreis und {a1} €/Einheit, Tarif B {b0} € Grundpreis und {b1} €/Einheit. Bei welcher Nutzung sind beide gleich teuer?"; sol=f"{a0}+{a1}x={b0}+{b1}x ⇒ x={fmt(val)}."
        elif t['id']=='quadratisch':
            h=rr.choice([4,9,16]); a=rr.choice([0.25,0.5,1]); val=2*math.sqrt(h/a); prompt=f"Ein Torbogen wird durch y=−{a}x²+{h} beschrieben. Bestimme die Breite am Boden."; sol=f"Nullstellen: x=±√({h}/{a}); Breite={r2(val)}."
        elif t['id']=='wachstum':
            start=rr.choice([100,200,500]); p=rr.choice([10,20,25]); threshold=rr.choice([500,800,1000]); n=0
            while start*(1+p/100)**n<threshold:n+=1
            val=n; prompt=f"Ein Bestand startet bei {start} und wächst pro Periode um {p} %. Nach wie vielen Perioden erreicht oder überschreitet er erstmals {threshold}?"; sol=f"Mit N(n)={start}·{1+p/100}^n systematisch prüfen. Erstmals bei n={n}."
        elif t['id']=='geometrie':
            h=rr.choice([8,10,12]); dist=rr.choice([5,6,8]); val=math.degrees(math.atan(h/dist)); prompt=f"Eine {h} m hohe Wand wird von einem Punkt in {dist} m horizontalem Abstand betrachtet. Bestimme den Höhenwinkel auf ganze Grad."; sol=f"tan α={h}/{dist}; α≈{round(val)}°."; val=round(val)
        elif t['id']=='koerper':
            R=rr.choice([4,5,6]); r=R-1; rho=rr.choice([1.2,2.7,7.8]); val=4/3*math.pi*(R**3-r**3)*rho/1000; prompt=f"Eine kugelförmige Hülle hat Außenradius {R} cm, Innenradius {r} cm und Materialdichte {rho} g/cm³. Bestimme die Masse in kg."; sol=f"Materialvolumen=4/3π({R}³−{r}³); Masse=V·{rho}/1000≈{r2(val)} kg."; val=r2(val)
        elif t['id']=='statistik':
            vals=[rr.randint(10,30) for _ in range(6)]; new=rr.randint(30,50); val=mean(vals+[new]); prompt=f"Messwerte: {vals}. Ein weiterer Wert {new} kommt hinzu. Bestimme den neuen Mittelwert auf eine Dezimalstelle."; sol=f"({sum(vals)}+{new})/7={r1(val)}."; val=r1(val)
        else:
            p=rr.choice([0.2,0.25,0.4]); n=rr.choice([3,4]); val=1-(1-p)**n; prompt=f"Ein Treffer tritt pro Versuch unabhängig mit Wahrscheinlichkeit {p} ein. Bestimme die Wahrscheinlichkeit, bei {n} Versuchen mindestens einen Treffer zu erzielen."; sol=f"1−(1−{p})^{n}={r2(val)}."; val=r2(val)
        challenge.append(q(f"challenge-{t['id']}-{j+1:02d}",t['id'],'MSA-Challenge','Modellieren & Problemlösen',4,'number',prompt,answer_num(val,0.12),sol,'Zerlege den Kontext in bekannte Teilprobleme.','Notiere zuerst ein mathematisches Modell, bevor du rechnest.',points=4,exam=False))

# Flashcards
flashcards=[]
def fc(topic, pairs):
    for idx,(term,definition) in enumerate(pairs,1):
        flashcards.append({"id":f"fc-{topic}-{idx:02d}","topic":topic,"term":term,"definition":definition})
fc('zahlen',[
 ('Potenz','Kurzschreibweise für wiederholte Multiplikation derselben Basis.'),('Quadratwurzel','Die nichtnegative Zahl, deren Quadrat den Radikanden ergibt.'),('Betrag','Abstand einer Zahl von 0 auf der Zahlengeraden.'),('rationale Zahl','Zahl, die als Bruch ganzer Zahlen dargestellt werden kann.'),('Prozent','Hundertstel-Anteil; 1 % = 1/100.'),('Maßstab 1:n','1 Längeneinheit im Plan entspricht n Längeneinheiten in Wirklichkeit.'),('Überschlag','Näherungsrechnung mit sinnvoll gerundeten Zahlen.'),('wissenschaftliche Schreibweise','Darstellung a·10^n mit 1≤|a|<10.'),('Grundrechenart Vorrang','Potenzen vor Punktrechnung vor Strichrechnung.'),('Kubikzentimeter','Volumeneinheit; 1 cm³ = 1 ml.'),('Quadratmeter','Flächeneinheit; 1 m² = 10 000 cm².'),('Kehrwert','Zahl, die mit der Ausgangszahl multipliziert 1 ergibt.')])
fc('algebra',[
 ('Term','Mathematischer Ausdruck aus Zahlen, Variablen und Rechenzeichen.'),('Variable','Platzhalter für eine Zahl.'),('Koeffizient','Zahlfaktor vor einer Variablen.'),('Gleichung','Aussage, dass zwei Terme denselben Wert haben.'),('Äquivalenzumformung','Umformung einer Gleichung, die die Lösungsmenge nicht verändert.'),('Lineares Gleichungssystem','Mehrere lineare Gleichungen mit denselben Variablen.'),('Einsetzungsverfahren','Eine Variable ausdrücken und in die andere Gleichung einsetzen.'),('Additionsverfahren','Gleichungen so addieren/subtrahieren, dass eine Variable wegfällt.'),('Satz vom Nullprodukt','Ein Produkt ist 0, wenn mindestens ein Faktor 0 ist.'),('p-q-Formel','Verfahren zum Lösen von x²+px+q=0.'),('Zellbezug','Adresse einer Zelle in einer Tabellenkalkulation, z. B. B3.'),('binomische Formel','Regel zum Ausmultiplizieren bestimmter Quadrate und Produkte.')])
fc('prozent',[
 ('Grundwert G','Das Ganze, das 100 % entspricht.'),('Prozentwert W','Der Teil des Grundwerts, der zu einem Prozentsatz gehört.'),('Prozentsatz p %','Anteil in Hundertsteln.'),('Wachstumsfaktor','Bei +p %: q=1+p/100.'),('Abnahmefaktor','Bei −p %: q=1−p/100.'),('Rabatt','Prozentuale Preisermäßigung.'),('Jahreszins','Z=K·p/100 für ein Jahr.'),('Zinseszins','Zinsen werden in Folgeperioden mitverzinst.'),('Prozentuale Änderung','(neu−alt)/alt·100 %.'),('Restfaktor','Faktor, der nach einer prozentualen Abnahme übrig bleibt.'),('Kapital K','Geldbetrag, auf den Zinsen berechnet werden.'),('Zinssatz','Prozentsatz der Verzinsung pro Zeitraum.')])
fc('linear',[
 ('lineare Funktion','Funktion der Form y=mx+b.'),('Steigung m','Änderung von y pro Änderung von x.'),('y-Achsenabschnitt b','Funktionswert bei x=0.'),('Nullstelle','x-Wert mit f(x)=0.'),('Schnittpunkt','Punkt, der auf zwei Graphen liegt.'),('proportionale Zuordnung','Lineare Zuordnung mit b=0.'),('Steigungsdreieck','Grafische Bestimmung von Δy/Δx.'),('Definitionsbereich','Menge der zulässigen x-Werte.'),('Wertebereich','Menge der auftretenden y-Werte.'),('Funktionswert','y-Wert, der zu einem x-Wert gehört.'),('Geradengleichung','Gleichung, die alle Punkte einer Geraden beschreibt.'),('Punktprobe','Koordinaten in die Funktionsgleichung einsetzen und prüfen.')])
fc('quadratisch',[
 ('quadratische Funktion','Funktion mit höchster Potenz x².'),('Parabel','Graph einer quadratischen Funktion.'),('Scheitelpunkt','Höchster oder tiefster Punkt einer Parabel.'),('Scheitelpunktform','f(x)=a(x−d)²+e.'),('Normalform','f(x)=ax²+bx+c.'),('Nullstelle','x-Wert, an dem der Graph die x-Achse schneidet oder berührt.'),('Symmetrieachse','Vertikale Gerade durch den Scheitelpunkt.'),('Streckfaktor a','Bestimmt Öffnung und Breite der Parabel.'),('Normalparabel','Graph von y=x².'),('nach unten geöffnet','a<0.'),('gestreckt','|a|>1.'),('gestaucht','0<|a|<1.')])
fc('wachstum',[
 ('exponentielles Wachstum','In gleichen Schritten wird mit demselben Faktor multipliziert.'),('Anfangswert a','Wert bei x=0.'),('Wachstumsfaktor q','Faktor pro Zeiteinheit.'),('q>1','Exponentielles Wachstum.'),('0<q<1','Exponentielle Abnahme.'),('Modell a·q^x','Grundform eines exponentiellen Modells.'),('prozentuale Zunahme','q=1+p/100.'),('prozentuale Abnahme','q=1−p/100.'),('absolute Zunahme','Differenz zweier aufeinanderfolgender Werte.'),('linear vs exponentiell','Linear: gleicher Betrag; exponentiell: gleicher Faktor.'),('Schwellenwert','Grenzwert, der erstmals über- oder unterschritten wird.'),('Verdopplung','Sonderfall mit Faktor q=2 pro Schritt.')])
fc('geometrie',[
 ('Satz des Pythagoras','Im rechtwinkligen Dreieck gilt a²+b²=c².'),('Hypotenuse','Längste Seite; liegt dem rechten Winkel gegenüber.'),('Sinus','Gegenkathete/Hypotenuse.'),('Kosinus','Ankathete/Hypotenuse.'),('Tangens','Gegenkathete/Ankathete.'),('Ähnlichkeit','Gleiche Winkel; entsprechende Seiten sind proportional.'),('zentrische Streckung','Abbildung mit Zentrum und Streckfaktor k.'),('Kreissektor','Teil eines Kreises zwischen zwei Radien und einem Kreisbogen.'),('Kreisring','Fläche zwischen zwei konzentrischen Kreisen.'),('Flächenfaktor','Bei Streckung mit k ändern sich Flächen mit k².'),('Umfang','Länge des Randes einer Figur.'),('Flächeninhalt','Größe der von einer Figur bedeckten Fläche.')])
fc('koerper',[
 ('Volumen','Rauminhalt eines Körpers.'),('Oberfläche','Summe aller äußeren Flächen eines Körpers.'),('Mantelfläche','Seitenfläche eines Körpers ohne Grund-/Deckflächen.'),('Prisma','Körper mit zwei kongruenten parallelen Grundflächen.'),('Zylinder','Prisma-ähnlicher Körper mit Kreisgrundfläche.'),('Pyramide','Körper mit Grundfläche und Spitze; V=1/3·G·h.'),('Kegel','Körper mit Kreisgrundfläche und Spitze.'),('Kugelvolumen','V=4/3·πr³.'),('Kugeloberfläche','O=4πr².'),('Dichte','Masse pro Volumen.'),('Verdrängung','Eingetauchter Körper verdrängt sein Volumen an Flüssigkeit.'),('Volumenfaktor','Bei Streckung mit k ändern sich Volumina mit k³.')])
fc('statistik',[
 ('absolute Häufigkeit','Wie oft ein Wert/Ereignis auftritt.'),('relative Häufigkeit','Absolute Häufigkeit geteilt durch Anzahl aller Werte.'),('arithmetisches Mittel','Summe der Werte geteilt durch ihre Anzahl.'),('Median','Mittlerer Wert einer geordneten Datenreihe.'),('Spannweite','Maximum minus Minimum.'),('unteres Quartil','Median der unteren Hälfte einer Rangliste.'),('oberes Quartil','Median der oberen Hälfte einer Rangliste.'),('Boxplot','Darstellung von Minimum, Quartilen, Median und Maximum.'),('Urliste','Werte in Beobachtungsreihenfolge.'),('Rangliste','Werte der Größe nach geordnet.'),('Stichprobe','Untersuchte Teilmenge einer Grundgesamtheit.'),('Repräsentativität','Wie gut eine Stichprobe die Grundgesamtheit abbildet.')])
fc('wahrscheinlichkeit',[
 ('Laplace-Experiment','Alle Elementarereignisse sind gleich wahrscheinlich.'),('Ereignis','Menge von Ergebnissen eines Zufallsversuchs.'),('Gegenereignis','Alle Ergebnisse, die nicht zum Ereignis gehören.'),('Baumdiagramm','Darstellung mehrstufiger Zufallsversuche.'),('1. Pfadregel','Entlang eines Pfades Wahrscheinlichkeiten multiplizieren.'),('2. Pfadregel','Wahrscheinlichkeiten passender disjunkter Pfade addieren.'),('ohne Zurücklegen','Wahrscheinlichkeiten ändern sich von Zug zu Zug.'),('mit Zurücklegen','Zusammensetzung bleibt gleich; Wahrscheinlichkeiten bleiben konstant.'),('relative Häufigkeit','Beobachteter Anteil eines Ereignisses.'),('Erwartete Häufigkeit','n·p als langfristig erwartete Trefferzahl.'),('unabhängig','Das Ergebnis eines Versuchs verändert die Wahrscheinlichkeit des anderen nicht.'),('faires Spiel','Erwartungswert des Nettogewinns ist 0.')])

# Exam case builders

def part(prompt, answer, solution, topic, points=3, hint=''):
    return {"prompt":prompt,"answer":answer,"solution":solution,"topic":topic,"points":points,"hint":hint}

def case_solar(seed):
    rr=random.Random(seed); L=rr.choice([8,10,12]); W=rr.choice([5,6,7]); panel=rr.choice([1.6,1.8,2.0]); eff=rr.choice([0.85,0.9]); count=math.floor(L*W/panel); power=rr.choice([0.38,0.42,0.45]); peak=count*power; annual=peak*rr.choice([850,900,950]); price=rr.choice([0.28,0.30,0.32]); value=annual*price
    return {"title":"Solardach","intro":f"Eine Schule plant Solarmodule auf einem rechteckigen Dach von {L} m × {W} m. Ein Modul beansprucht einschließlich Abstand {panel} m². Pro Modul werden {power} kWp angesetzt.","parts":[
        part(f"Berechne die Dachfläche.",answer_num(L*W,0.01,'m²'),f"A={L}·{W}={L*W} m².",'geometrie'),
        part(f"Bestimme, wie viele ganze Module nach dem Flächenmodell höchstens Platz finden.",answer_num(count,0),f"{L*W}/{panel}={fmt(L*W/panel)} ⇒ höchstens {count} ganze Module.",'zahlen'),
        part("Berechne die installierte Spitzenleistung in kWp.",answer_num(peak,0.02,'kWp'),f"{count}·{power}={fmt(peak)} kWp.",'prozent'),
        part("Für eine grobe Jahresprognose werden 900 kWh pro kWp angesetzt. Berechne die Jahresenergie mit diesem Wert.",answer_num(peak*900,0.5,'kWh'),f"{fmt(peak)}·900={fmt(peak*900)} kWh.",'linear'),
        part(f"Bei einem Stromwert von {price} €/kWh: Bestimme den rechnerischen Jahreswert für die Prognose aus Teil d.",answer_num(peak*900*price,0.5,'€'),f"{fmt(peak*900)}·{price}={r2(peak*900*price)} €.",'prozent'),
        part("Begründe kurz, warum die Modulanzahl aus dem reinen Flächenquotienten eine Obergrenze ist.",answer_keywords(any_words=['rand','abstand','gang','hindernis','dachfenster','geometrie']),"In der Realität gehen Flächen durch Ränder, Abstände, Wartungswege oder Hindernisse verloren.",'geometrie')
    ]}

def case_ramp(seed):
    rr=random.Random(seed); run=rr.choice([120,150,180]); rise=rr.choice([40,50,60]); length=math.hypot(run,rise); angle=math.degrees(math.atan(rise/run)); m=rise/run; x=rr.choice([30,60,90]); y=m*x
    return {"title":"Miniaturrampe","intro":f"Eine Rampe steigt über eine waagerechte Länge von {run} cm um {rise} cm an.","parts":[
        part("Berechne die Länge der schrägen Rampenfläche im Seitenprofil. Runde auf eine Dezimalstelle.",answer_num(r1(length),0.11,'cm'),f"s=√({run}²+{rise}²)≈{r1(length)} cm.",'geometrie'),
        part("Bestimme den Steigungswinkel auf ganze Grad.",answer_num(round(angle),1,'°'),f"tan α={rise}/{run}; α≈{round(angle)}°.",'geometrie'),
        part("Modelliere die Oberkante als y=m·x. Bestimme m auf drei Dezimalstellen.",answer_num(round(m,3),0.0015),f"m={rise}/{run}≈{round(m,3)}.",'linear'),
        part(f"Bestimme die Höhe y bei x={x} cm.",answer_num(y,0.05,'cm'),f"y={fmt(m)}·{x}={fmt(y)} cm.",'linear'),
        part(f"Prüfe rechnerisch, ob P({run/2}|{rise/2}) auf der Modellgeraden liegt. Antworte ja/nein.",answer_text(['ja']),f"Bei x={run/2} gilt y={m*run/2}={rise/2}; also liegt P auf der Geraden.",'linear'),
        part("Warum ist ein lineares Modell für eine gerade Rampe sinnvoll?",answer_keywords(any_words=['konstante steigung','gerade','gleichmäßig','proportional']),"Die Höhe ändert sich bei einer geraden Rampe mit konstanter Steigung gleichmäßig zur waagerechten Strecke.",'linear')
    ]}

def case_sphere(seed):
    rr=random.Random(seed); d=rr.choice([3.0,3.6,4.0,4.5]); r=d/2; thick=rr.choice([0.04,0.05,0.06]); inner=r-thick; area=4*math.pi*r*r; shell=4/3*math.pi*(r**3-inner**3); density=rr.choice([1.1,1.2,2.7]); mass=shell*density; cans=math.ceil(area/rr.choice([6,8,10])); cover=rr.choice([6,8,10])
    return {"title":"Kunstkugel","intro":f"Eine hohle Kugelskulptur hat Außendurchmesser {d} m und Wandstärke {thick} m. Die Materialdichte beträgt {density} t/m³.","parts":[
        part("Bestimme den Außenradius.",answer_num(r,0.001,'m'),f"r=d/2={d}/2={r} m.",'koerper'),
        part("Berechne die Außenoberfläche. Runde auf eine Dezimalstelle.",answer_num(r1(area),0.11,'m²'),f"O=4πr²≈{r1(area)} m².",'koerper'),
        part("Bestimme den Innenradius.",answer_num(inner,0.001,'m'),f"r_i={r}−{thick}={fmt(inner)} m.",'koerper'),
        part("Berechne das Materialvolumen der Hülle. Runde auf zwei Dezimalstellen.",answer_num(r2(shell),0.02,'m³'),f"V_H=4/3π(r³−r_i³)≈{r2(shell)} m³.",'koerper'),
        part("Berechne die Masse der Hülle in Tonnen. Runde auf zwei Dezimalstellen.",answer_num(r2(mass),0.03,'t'),f"m=ρ·V={density}·{r2(shell)}≈{r2(mass)} t.",'koerper'),
        part(f"Ein Farbeimer reicht für {cover} m². Wie viele Eimer werden mindestens benötigt?",answer_num(math.ceil(area/cover),0),f"{r1(area)}/{cover}={fmt(area/cover)} ⇒ aufrunden auf {math.ceil(area/cover)} Eimer.",'prozent')
    ]}

def case_growth(seed):
    rr=random.Random(seed); a=rr.choice([80,100,120,200]); p=rr.choice([10,15,20,25]); qv=1+p/100; n=rr.choice([3,4,5]); val=a*qv**n; threshold=rr.choice([300,400,500,600]); k=0
    while a*qv**k<threshold:k+=1
    linadd=round(a*p/100)
    return {"title":"Community-Wachstum","intro":f"Eine schulische Online-Community startet mit {a} Mitgliedern. Ein Modell nimmt ein Wachstum von {p} % pro Woche an.","parts":[
        part("Bestimme den Wachstumsfaktor q.",answer_num(qv,0.001),f"q=1+{p}/100={qv}.",'wachstum'),
        part(f"Berechne die modellierte Mitgliederzahl nach {n} Wochen. Runde auf ganze Personen.",answer_num(round(val),1),f"N={a}·{qv}^{n}≈{round(val)}.",'wachstum'),
        part(f"Nach wie vielen Wochen wird erstmals {threshold} erreicht oder überschritten?",answer_num(k,0),f"Systematisches Prüfen von {a}·{qv}^n ergibt erstmals bei n={k} mindestens {threshold}.",'wachstum'),
        part(f"Ein lineares Vergleichsmodell addiert jede Woche {linadd} Mitglieder. Bestimme dessen Wert nach {n} Wochen.",answer_num(a+linadd*n,0),f"L={a}+{linadd}·{n}={a+linadd*n}.",'linear'),
        part(f"Welches Modell liefert nach {n} Wochen den größeren Wert? Antworte 'exponentiell' oder 'linear'.",answer_text(['exponentiell' if val>a+linadd*n else 'linear']),f"Exponentiell≈{round(val)}, linear={a+linadd*n}. Daher ist {'exponentiell' if val>a+linadd*n else 'linear'} größer.",'wachstum'),
        part("Nenne einen Grund, warum das exponentielle Modell langfristig unrealistisch werden kann.",answer_keywords(any_words=['begrenz','sättig','endlich','kapazität','nicht unbegrenzt']),"Reale Systeme haben meist begrenzte Zielgruppen/Ressourcen; dauerhaft konstantes prozentuales Wachstum ist daher unrealistisch.",'wachstum')
    ]}

def case_festival(seed):
    rr=random.Random(seed); pa=rr.choice([12,14,16]); py=rr.choice([7,8,9]); a=rr.randint(80,140); y=rr.randint(100,180); total=a+y; revenue=pa*a+py*y; avg=revenue/total; disc=rr.choice([10,15,20]); reduced=pa*(1-disc/100)
    return {"title":"Schulfestival","intro":f"Beim Schulfestival kosten Erwachsenentickets {pa} €, Jugendtickets {py} €. Insgesamt werden {total} Tickets verkauft und {revenue} € eingenommen.","parts":[
        part("Stelle das LGS gedanklich auf und bestimme die Zahl der Erwachsenentickets.",answer_num(a,0),f"x+y={total}; {pa}x+{py}y={revenue}. Lösung x={a}.",'algebra'),
        part("Bestimme die Zahl der Jugendtickets.",answer_num(y,0),f"y={total}−{a}={y}.",'algebra'),
        part("Berechne den durchschnittlichen Erlös pro Ticket. Runde auf Cent.",answer_num(r2(avg),0.02,'€'),f"{revenue}/{total}={r2(avg)} €.",'statistik'),
        part(f"Ein Erwachsenenticket wird für einen Vorverkauf um {disc} % reduziert. Bestimme den Vorverkaufspreis.",answer_num(r2(reduced),0.02,'€'),f"{pa}·{1-disc/100}={r2(reduced)} €.",'prozent'),
        part("Bestimme den Anteil der Jugendtickets in Prozent. Runde auf eine Dezimalstelle.",answer_num(r1(y/total*100),0.11,'%'),f"{y}/{total}·100≈{r1(y/total*100)} %.",'statistik'),
        part("Warum kann der Durchschnittserlös pro Ticket nicht einfach als Mittelwert der beiden Ticketpreise berechnet werden?",answer_keywords(any_words=['unterschiedlich viele','häufigkeit','gewicht','anzahl','nicht gleich']),"Die beiden Ticketarten wurden unterschiedlich häufig verkauft; deshalb braucht man einen gewichteten Mittelwert.",'statistik')
    ]}

def case_probability(seed):
    rr=random.Random(seed); red=rr.choice([3,4,5]); blue=10-red; p=red/10; p2=p*p; atleast=1-(1-p)**2; expected=50*p
    return {"title":"Gewinnbox","intro":f"In einer Box liegen {red} rote und {blue} blaue Chips. Für Teil a–d wird nach jedem Ziehen zurückgelegt.","parts":[
        part("Bestimme P(rot) bei einem Zug.",answer_num(p,0.001),f"P={red}/10={fmt(p)}.",'wahrscheinlichkeit'),
        part("Bestimme P(zweimal rot) bei zwei Zügen.",answer_num(p2,0.001),f"P={fmt(p)}²={fmt(p2)}.",'wahrscheinlichkeit'),
        part("Bestimme P(mindestens einmal rot) bei zwei Zügen.",answer_num(atleast,0.001),f"1−P(zweimal blau)=1−{fmt(1-p)}²={fmt(atleast)}.",'wahrscheinlichkeit'),
        part("Wie viele rote Ergebnisse erwartet man ungefähr bei 50 Einzelzügen?",answer_num(expected,0.01),f"50·{fmt(p)}={fmt(expected)}.",'wahrscheinlichkeit'),
        part("Nun wird zweimal ohne Zurücklegen gezogen. Bestimme P(zweimal rot). Runde auf drei Dezimalstellen.",answer_num(round((red/10)*((red-1)/9),3),0.0015),f"{red}/10·{red-1}/9≈{round((red/10)*((red-1)/9),3)}.",'wahrscheinlichkeit'),
        part("Warum ändert sich beim Ziehen ohne Zurücklegen die Wahrscheinlichkeit im zweiten Zug?",answer_keywords(any_words=['zusammensetzung','weniger','anzahl','verändert','nicht zurück']),"Nach dem ersten Zug befinden sich weniger Chips in der Box und ihre Zusammensetzung kann sich geändert haben.",'wahrscheinlichkeit')
    ]}

def case_tank(seed):
    rr=random.Random(seed); r=rr.choice([1.0,1.2,1.5]); h=rr.choice([2.0,2.5,3.0]); V=math.pi*r*r*h; fill=rr.choice([0.6,0.7,0.8]); water=V*fill; rate=rr.choice([0.08,0.1,0.12]); time=water/rate
    return {"title":"Wassertank","intro":f"Ein zylindrischer Tank hat Radius {r} m und Höhe {h} m. Er ist zu {int(fill*100)} % gefüllt. Eine Pumpe entnimmt {rate} m³ pro Minute.","parts":[
        part("Berechne das Gesamtvolumen des Tanks. Runde auf zwei Dezimalstellen.",answer_num(r2(V),0.03,'m³'),f"V=π·{r}²·{h}≈{r2(V)} m³.",'koerper'),
        part("Berechne das aktuelle Wasservolumen. Runde auf zwei Dezimalstellen.",answer_num(r2(water),0.03,'m³'),f"{int(fill*100)} % von {r2(V)}≈{r2(water)} m³.",'prozent'),
        part("Bestimme die aktuelle Wasserhöhe.",answer_num(h*fill,0.02,'m'),f"Bei konstantem Querschnitt entspricht {int(fill*100)} % Volumen auch {int(fill*100)} % Höhe: {h}·{fill}={fmt(h*fill)} m.",'koerper'),
        part("Wie lange dauert das Leerpumpen rechnerisch? Runde auf eine Dezimalstelle.",answer_num(r1(time),0.11,'min'),f"t=V/rate={r2(water)}/{rate}≈{r1(time)} min.",'linear'),
        part("Nach 5 Minuten: Wie viel Wasser ist noch im Tank?",answer_num(r2(max(0,water-5*rate)),0.03,'m³'),f"V(5)={r2(water)}−5·{rate}={r2(max(0,water-5*rate))} m³.",'linear'),
        part("Warum ist für das Leerpumpen mit konstanter Pumpenleistung ein lineares Modell sinnvoll?",answer_keywords(any_words=['konstant','gleiche menge','pro minute','rate']),"Pro Minute wird dieselbe Wassermenge entnommen; das Volumen nimmt daher um einen konstanten Betrag ab.",'linear')
    ]}

def case_quadratic(seed):
    rr=random.Random(seed); a=rr.choice([0.25,0.5,1]); h=rr.choice([4,9,16]); x=rr.choice([1,2]); y=-a*x*x+h; root=math.sqrt(h/a); width=2*root
    return {"title":"Bogenkonstruktion","intro":f"Der Querschnitt eines Bogens wird durch f(x)=−{a}x²+{h} (Maße in m) modelliert.","parts":[
        part("Bestimme die maximale Höhe.",answer_num(h,0.01,'m'),f"Scheitel bei (0|{h}); maximale Höhe {h} m.",'quadratisch'),
        part(f"Bestimme die Höhe bei x={x} m.",answer_num(y,0.01,'m'),f"f({x})=−{a}·{x}²+{h}={fmt(y)} m.",'quadratisch'),
        part("Bestimme die positive Nullstelle. Runde auf zwei Dezimalstellen.",answer_num(r2(root),0.03,'m'),f"0=−{a}x²+{h} ⇒ x=√({h}/{a})≈{r2(root)} m.",'quadratisch'),
        part("Bestimme die gesamte Breite am Boden.",answer_num(r2(width),0.03,'m'),f"Symmetrisch: Breite=2·{r2(root)}≈{r2(width)} m.",'quadratisch'),
        part("Ist die Parabel nach oben oder nach unten geöffnet?",answer_text(['unten','nach unten']),"Der x²-Koeffizient ist negativ, daher nach unten geöffnet.",'quadratisch'),
        part("Warum ist das Modell nur in einem begrenzten Definitionsbereich sinnvoll?",answer_keywords(any_words=['zwischen','nullstellen','boden','negative höhe','physikalisch']),"Außerhalb der Nullstellen liefert die Funktion negative Höhen, die für den realen Bogen keinen Sinn ergeben.",'quadratisch')
    ]}

def case_data(seed):
    rr=random.Random(seed); vals=sorted([rr.randint(5,25) for _ in range(9)]); m=mean(vals); med=median(vals); span=max(vals)-min(vals); high=sum(1 for v in vals if v>=15); rel=high/len(vals)
    return {"title":"Sportdaten","intro":f"Neun Trainingswerte wurden erhoben: {vals}.","parts":[
        part("Bestimme den Median.",answer_num(med,0.01),f"Bei 9 geordneten Werten ist der 5. Wert der Median: {med}.",'statistik'),
        part("Bestimme die Spannweite.",answer_num(span,0),f"{max(vals)}−{min(vals)}={span}.",'statistik'),
        part("Berechne das arithmetische Mittel. Runde auf eine Dezimalstelle.",answer_num(r1(m),0.11),f"Summe={sum(vals)}; /9≈{r1(m)}.",'statistik'),
        part("Wie viele Werte sind mindestens 15?",answer_num(high,0),f"Es sind {high} Werte ≥15.",'statistik'),
        part("Bestimme den Anteil dieser Werte in Prozent. Runde auf eine Dezimalstelle.",answer_num(r1(rel*100),0.11,'%'),f"{high}/9·100≈{r1(rel*100)} %.",'statistik'),
        part("Nenne einen Grund, warum neun Werte allein keine sichere Aussage über alle Schülerinnen und Schüler erlauben.",answer_keywords(any_words=['klein','stichprobe','nicht repräsentativ','auswahl','zufall']),"Die Stichprobe ist klein und möglicherweise nicht repräsentativ für die gesamte Gruppe.",'statistik')
    ]}

case_builders=[case_solar,case_ramp,case_sphere,case_growth,case_festival,case_probability,case_tank,case_quadratic,case_data]

# Exam variants: PT1 uses only tasks that are reasonable without calculator/formula sheet;
# PT2 uses three contextual multi-part tasks.
exam_variants=[]
pt1_allowed_subtopics={
 'zahlen': None,
 'prozent': {'Prozentwert','Grundwert','Prozentsatz','Rabatt','Prozentuale Änderung','Anteile'},
 'algebra': {'Ausklammern','Binomische Formeln','Formeln umstellen','Lineare Gleichungen','Lineare Gleichungssysteme','Probe','Quadratische Gleichungen','Sachgleichungen','Tabellenkalkulation','Terme zusammenfassen','Termwerte'},
 'geometrie': {'Flächeninhalt','Dreiecksfläche','Koordinatengeometrie','Satz des Pythagoras','Ähnlichkeit'},
 'statistik': None,
 'wahrscheinlichkeit': {'Laplace','Gegenereignis','Würfel','Relative Häufigkeit','Erwartete Häufigkeit'},
 'linear': {'Geradengleichung','Graphen','Interpretation','Nullstelle','Proportionalität','Punktprobe','Steigung','Wertetabellen'},
 'quadratisch': {'Funktionswerte','Graphen','Nullstellen','Parabeleigenschaften','Scheitelpunktform','Streckfaktor','Symmetrieachse'},
 'wachstum': {'Abnahmefaktor','Alltagsmodell','Anfangswert','Faktor interpretieren','Graphen','Linear vs. exponentiell','Wachstumsfaktor'}
}
by_topic={}
for t in TOPICS:
    allowed=pt1_allowed_subtopics.get(t['id'])
    by_topic[t['id']]=[x for x in tasks if x['topic']==t['id'] and x['difficulty']<=3 and x['examEligible'] and (allowed is None or x['subtopic'] in allowed)]
for v in range(20):
    rr=random.Random(202700+v)
    pt1_topics=[['zahlen','prozent'],['algebra'],['geometrie'],['statistik','wahrscheinlichkeit'],['linear','quadratisch'],['wachstum','prozent']]
    pt1=[]
    for k,choices in enumerate(pt1_topics):
        topic=rr.choice(choices); cand=rr.choice(by_topic[topic]).copy(); cand['points']=3; cand['id']=f"exam{v+1:02d}-pt1-{k+1}"; pt1.append(cand)
    cases=[]
    for k in range(3):
        builder=case_builders[(v*3+k)%len(case_builders)]
        cases.append(builder(7000+v*10+k))
    exam_variants.append({"id":f"msa-{v+1:02d}","part1":pt1,"part2":cases})

meta={
 "title":"ZP10 Mathematik NRW – MSA Training",
 "version":"1.0.0",
 "targetYear":2027,
 "officialStructure":{
   "part1":"Basiskompetenzen in voneinander unabhängigen Teilaufgaben; ohne Taschenrechner und Formelsammlung.",
   "part2":"Komplexere Aufgaben mit mehreren Teilaufgaben in Kontexten; Prozess- und Inhaltsbereiche werden verknüpft.",
   "part1Tools":["Zirkel","Geodreieck"],
   "part2Tools":["Zirkel","Geodreieck","Formelsammlung MSA","Taschenrechner"],
   "baseMinutes":120,"recommendedPart1Minutes":30,"recommendedPart2Minutes":90,"bonusMinutes":10,"maxMinutes":130,
   "part1Points":18,"part2MathPoints":54,"crossTaskFormalPoints":9,"officialTotalPoints":81,
   "gradeThresholds":[{"min":70,"grade":"sehr gut"},{"min":59,"grade":"gut"},{"min":48,"grade":"befriedigend"},{"min":36,"grade":"ausreichend"},{"min":15,"grade":"mangelhaft"},{"min":0,"grade":"ungenügend"}]
 },
 "copyrightNote":"Alle Trainingsaufgaben dieses Projekts wurden neu erstellt. Alte ZP10-Aufgaben und Abbildungen werden nicht in die Website übernommen.",
 "aiHelpUrl":"https://tools.paddy.app/groups/join/9c4a49d6-6d3a-4d78-b9da-2ff915b0cb0a/secret/1ca663de-e047-45a7-94af-7392fc4468ca"
}

# Wrap as JS globals to also work from file:// without fetch.
def write_js(name,var,obj):
    with open(os.path.join(OUT,name),'w',encoding='utf-8') as f:
        f.write(f"window.{var} = ")
        json.dump(obj,f,ensure_ascii=False,separators=(',',':'))
        f.write(';\n')

write_js('meta.js','ZP_META',meta)
write_js('topics.js','ZP_TOPICS',TOPICS)
write_js('tasks.js','ZP_TASKS',tasks)
write_js('challenges.js','ZP_CHALLENGES',challenge)
write_js('flashcards.js','ZP_FLASHCARDS',flashcards)
write_js('exams.js','ZP_EXAMS',exam_variants)

# Human-readable QA summary
qa={"topicTaskCounts":{t['id']:sum(1 for x in tasks if x['topic']==t['id']) for t in TOPICS},"challengeCounts":{t['id']:sum(1 for x in challenge if x['topic']==t['id']) for t in TOPICS},"flashcardCounts":{t['id']:sum(1 for x in flashcards if x['topic']==t['id']) for t in TOPICS},"examVariants":len(exam_variants)}
with open(os.path.join(OUT,'qa-summary.json'),'w',encoding='utf-8') as f: json.dump(qa,f,ensure_ascii=False,indent=2)
print(json.dumps(qa,ensure_ascii=False,indent=2))
