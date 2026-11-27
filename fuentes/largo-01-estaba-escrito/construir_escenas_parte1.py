#!/usr/bin/env python3
"""Arma parte1/escenas.json (planos, capítulos, referencias y temblores) y verifica que cada ancla exista en words.json."""
import json, re, unicodedata, sys
W = json.load(open('../../insumos-voz/largo-01-parte1/words.json'))['words']
norm = lambda s: re.sub(r'[^a-z0-9ñ]', '', ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn'))
T = [norm(w['text']) for w in W]
def existe(fr, occ=1):
    ks = [norm(k) for k in fr.split()]; c = 0
    for i in range(len(T) - len(ks) + 1):
        if T[i:i + len(ks)] == ks:
            c += 1
            if c == occ: return W[i]['start']
    return None
CAM = {'in': [.5, .5, 1.05, .5, .5, 1.28], 'out': [.5, .5, 1.32, .5, .5, 1.06], 'izq': [.62, .5, 1.22, .4, .5, 1.22], 'der': [.38, .5, 1.22, .6, .5, 1.22],
       'arriba': [.5, .62, 1.22, .5, .4, 1.22], 'abajo': [.5, .4, 1.22, .5, .6, 1.22]}
def cam(c):
    if isinstance(c, str): return CAM[c]
    if len(c) == 2: return [.5, .5, 1.06, c[0], c[1], 1.5]
    if len(c) == 3: return [.5, .5, 1.06, c[0], c[1], c[2]]
    return c
P = []
def s(fr, img, c='in', fx=('polvo',), occ=1, **kw):
    d = {'img': f'img/{img}.png', 'en': [fr, occ, -0.15] if fr else 0, 'cam': cam(c), 'fx': list(fx)}; d.update(kw); P.append(d)
R = []; CAPS = []; SH = []
def r(desde, hasta, txt, o1=1, o2=1): R.append({'desde': [desde, o1, -0.1], 'hasta': [hasta, o2, -0.2], 'texto': txt})
def cap(fr, a, b, dur=3.6, occ=1): CAPS.append({'en': [fr, occ, 0], 'a': a, 'b': b, 'dur': dur})
def tem(fr, f=1.0, occ=1): SH.append({'en': [fr, occ, 0], 'fuerza': f})
LUZ = {'luz': [.6, -.05]}
# 0 · Gancho
s(None, 'cuchillo', [.5, .5, 1.02, .45, .42, 1.35], ('rayos', 'polvo'), luz=[.62, -.05])
s('una familia en la noche', 'puerta', 'in', ('oscuro', 'polvo'))
s('un hombre sangra', 'cruces', (.5, .4), ('rayos', 'polvo'), **LUZ)
s('tres escenas', 'biblia', 'in', ('vela', 'polvo'), luz=[.07, .22])
s('porque la biblia dice', 'sangre_tierra', [.5, .55, 1.05, .42, .78, 1.6], ('rayos', 'polvo'), luz=[.3, -.1])
s('hoy vamos a abrir', 'biblia', 'der', ('vela', 'polvo'), luz=[.07, .22])
cap('estaba escrito', 'ESTABA ESCRITO', 'Parte 1', 4.2)
# 1 · Génesis 3
cap('la primera profecia', 'GÉNESIS 3', 'La primera promesa')
s('la primera profecia', 'eden', 'in', ('rayos', 'polvo'), luz=[.55, -.1])
s('en un jardin', 'eden', 'izq', ('polvo',))
s('el dia en que entro', 'serpiente_arbol', [.5, .5, 1.05, .25, .72, 1.45], ('oscuro', 'polvo'))
s('adan y eva acababan', 'eden', [.6, .6, 1.25, .66, .6, 1.8], ('oscuro', 'polvo'))
s('la serpiente parecia', 'serpiente_arbol', (.55, .45, 1.5), ('oscuro', 'polvo'))
s('pero en medio del juicio', 'luz_juicio', 'in', ('rayos', 'polvo'), luz=[.64, -.05])
s('un descendiente de la mujer', 'talon', (.6, .68, 1.45), ('polvo',)); tem('aplastara', .8)
s('genesis tres quince', 'talon', 'out', ('polvo',))
s('y ese dia paso', 'eden', [.25, .7, 1.5, .15, .72, 1.75], ('oscuro', 'polvo'))
s('antes de sacarlos', 'pieles', 'in', ('rayos', 'polvo'), luz=[.42, -.05])
s('la biblia no dice de que animal', 'pieles', 'der', ('polvo',))
s('para cubrir al culpable', 'leon_cordero', (.64, .62, 1.7), ('rayos', 'polvo'), luz=[.55, -.1])
s('fue la primera sangre', 'sangre_tierra', (.42, .8, 1.7), ('polvo',))
s('desde ese dia la sangre', 'ofrendas', 'in', ('polvo', 'niebla'))
s('y cada uno senalaba', 'cruces', 'in', ('rayos', 'polvo'), **LUZ)
s('miles de anos despues pablo', 'pesebre', 'in', ('vela', 'polvo'), luz=[.35, .25])
s('y juan explica', 'biblia', (.45, .62, 1.4), ('vela', 'polvo'), luz=[.07, .22])
s('en la cruz jesus fue herido', 'cruces', (.5, .4, 1.55), ('rayos', 'polvo'), **LUZ)
s('pero la serpiente fue vencida', 'talon', (.62, .75, 1.6), ('polvo',)); tem('fue vencida', .6)
s('la promesa mas antigua', 'cruces', 'out', ('rayos', 'polvo'), **LUZ)
r('un descendiente de la mujer', 'y ese dia paso', 'Génesis 3:15'); r('hojas de higuera', 'antes de sacarlos', 'Génesis 3:7')
r('los vistio', 'para cubrir al culpable', 'Génesis 3:21'); r('pablo escribe', 'y juan explica', 'Gálatas 4:4'); r('y juan explica', 'en la cruz jesus fue herido', '1 Juan 3:8')
# 2 · Abel
cap('pero antes de que esa promesa', 'GÉNESIS 4', 'La sangre de Abel')
s('pero antes de que esa promesa', 'cain_campo', 'out', ('niebla', 'polvo'))
s('adan y eva tuvieron dos hijos', 'ofrendas', 'in', ('polvo',))
s('un dia los dos trajeron', 'ofrendas', 'der', ('polvo',))
s('y dios miro con agrado', 'ofrendas', (.3, .42, 1.55), ('rayos', 'polvo'), luz=[.3, -.1])
s('por que hebreos lo responde', 'biblia', 'in', ('vela', 'polvo'), luz=[.07, .22])
s('cain se enojo', 'cain_enojo', 'in', ('oscuro', 'polvo'))
s('si bien hicieres', 'cain_enojo', (.72, .45, 1.5), ('oscuro', 'polvo')); tem('si bien hicieres', .5)
s('en el campo lejos de todos', 'cain_campo', (.3, .52, 1.35), ('niebla', 'polvo'))
s('dios pregunta', 'luz_juicio', [.5, .6, 1.05, .62, .42, 1.28], ('rayos', 'polvo'), luz=[.64, -.05]); tem('donde esta abel', .5)
s('no se soy yo acaso', 'cain_campo', (.3, .42, 1.6), ('oscuro', 'polvo'))
s('que has hecho', 'sangre_tierra', (.42, .8, 1.6), ('polvo',)); tem('que has hecho', 1.0)
s('siglos mas tarde', 'biblia', 'izq', ('vela', 'polvo'), luz=[.07, .22])
s('la sangre de abel pedia', 'sangre_tierra', [.42, .8, 1.6, .42, .78, 1.9], ('polvo',))
s('la sangre de jesus habla', 'cruces', (.55, .42, 1.6), ('rayos', 'polvo'), **LUZ)
r('un dia los dos trajeron', 'por que hebreos lo responde', 'Génesis 4:3-5'); r('por la fe abel', 'cain se enojo', 'Hebreos 11:4')
r('si bien hicieres', 'en el campo lejos de todos', 'Génesis 4:7'); r('donde esta abel', 'siglos mas tarde', 'Génesis 4:8-10')
r('la sangre de jesus habla', 'un hijo le hizo', 'Hebreos 12:24')
# 3 · Moriah
cap('un hijo le hizo', 'GÉNESIS 22', 'Dios se proveerá de cordero')
s('un hijo le hizo', 'subida', 'in', ('polvo',))
s('abraham habia esperado', 'estrellas', 'in', ('polvo',))
s('y a los cien anos', 'tienda', 'in', ('vela', 'polvo'), luz=[.5, .4])
s('hasta que un dia dios', 'luz_juicio', 'out', ('rayos', 'polvo'), luz=[.64, -.05])
s('tres dias de camino', 'subida', 'izq', ('polvo',))
s('al tercer dia', 'subida', (.62, .3, 1.5), ('polvo', 'niebla'))
s('volveremos los dos', 'subida', (.38, .6, 1.55), ('polvo',))
s('hebreos dice que abraham', 'biblia', 'in', ('vela', 'polvo'), luz=[.07, .22])
s('entonces pone la lena', 'subida', (.35, .55, 1.6), ('polvo',))
s('y en el camino isaac pregunta', 'subida', (.42, .5, 1.75), ('polvo',))
s('abraham responde', 'cuchillo', [.6, .35, 1.3, .5, .45, 1.1], ('rayos', 'polvo'), luz=[.62, -.05])
s('llegan arriba', 'cuchillo', (.42, .6, 1.5), ('polvo',))
s('una voz desde el cielo', 'cuchillo', (.58, .2, 1.6), ('rayos', 'polvo'), luz=[.62, -.05]); tem('abraham abraham', .8)
s('abraham alza los ojos', 'carnero', 'in', ('rayos', 'polvo'), luz=[.8, -.05])
s('pero fijate', 'carnero', 'out', ('polvo',))
s('siglos despues en el monte', 'templo', 'in', ('polvo', 'niebla'))
s('y un dia junto al rio', 'jordan', (.3, .45, 1.45), ('polvo',))
s('he aqui el cordero', 'jordan', (.74, .5, 1.7), ('rayos', 'polvo'), luz=[.75, -.1])
s('a abraham dios le dijo', 'cuchillo', 'out', ('rayos', 'polvo'), luz=[.62, -.05])
s('y pablo escribe que dios', 'cruces', 'in', ('rayos', 'polvo'), **LUZ)
s('en moriah dios detuvo', 'cuchillo', (.45, .25, 1.6), ('rayos', 'polvo'), luz=[.62, -.05])
s('en la cruz no lo detuvo', 'cruces', [.5, .45, 1.1, .5, .38, 1.75], ('oscuro', 'polvo'))
s('abraham llamo a aquel lugar', 'carnero', (.8, .2, 1.4), ('rayos', 'polvo'), luz=[.8, -.05])
r('las estrellas del cielo', 'y a los cien anos', 'Génesis 15:5'); r('y a los cien anos', 'hasta que un dia dios', 'Génesis 21:5')
r('toma ahora', 'tres dias de camino', 'Génesis 22:2'); r('a sus siervos', 'hebreos dice que abraham', 'Génesis 22:5')
r('hebreos dice que abraham', 'entonces pone la lena', 'Hebreos 11:19'); r('entonces pone la lena', 'y en el camino isaac pregunta', 'Génesis 22:6')
r('padre aqui estan', 'llegan arriba', 'Génesis 22:7-8'); r('una voz desde el cielo', 'abraham alza los ojos', 'Génesis 22:11-12')
r('y ve un carnero', 'pero fijate', 'Génesis 22:13'); r('siglos despues en el monte', 'y un dia junto al rio', '2 Crónicas 3:1')
r('he aqui el cordero', 'a abraham dios le dijo', 'Juan 1:29'); r('no me rehusaste', 'y pablo escribe que dios', 'Génesis 22:12')
r('no escatimo', 'en moriah dios detuvo', 'Romanos 8:32'); r('abraham llamo a aquel lugar', 'isaac tuvo un hijo', 'Génesis 22:14')
# 4 · Judá
cap('isaac tuvo un hijo', 'GÉNESIS 49', 'El cetro de Judá')
s('isaac tuvo un hijo', 'jacob', 'in', ('vela', 'polvo'), luz=[.2, .15])
s('no sera quitado el cetro', 'jacob', (.35, .45, 1.55), ('vela', 'polvo'), luz=[.2, .15])
s('un cetro es la vara', 'david', 'in', ('vela', 'polvo'), luz=[.7, .55])
s('siglos despues hebreos afirma', 'biblia', 'in', ('vela', 'polvo'), luz=[.07, .22])
s('y el apocalipsis', 'leon_cordero', (.4, .45, 1.5), ('rayos', 'polvo'), luz=[.5, -.1])
s('pero cuando juan se da vuelta', 'leon_cordero', (.62, .6, 1.8), ('rayos', 'polvo'), luz=[.55, -.1])
r('no sera quitado el cetro', 'un cetro es la vara', 'Génesis 49:10'); r('siglos despues hebreos afirma', 'y el apocalipsis', 'Hebreos 7:14')
r('y el apocalipsis', 'pasaron mas de cuatrocientos', 'Apocalipsis 5:5-6')
# 5 · Pascua
cap('pasaron mas de cuatrocientos', 'ÉXODO 12', 'La sangre en la puerta')
s('pasaron mas de cuatrocientos', 'esclavos', 'in', ('polvo',))
s('dios envio plaga tras plaga', 'esclavos', 'der', ('polvo', 'oscuro'))
s('hasta que llego la ultima', 'medianoche', 'in', ('oscuro', 'niebla'))
s('pero dios dio una salida', 'familia_cordero', 'in', ('polvo',))
s('y poner su sangre', 'puerta', (.5, .3, 1.5), ('oscuro', 'polvo'))
s('y la sangre os sera', 'puerta', 'out', ('oscuro', 'polvo')); tem('y la sangre os sera', .6)
s('a medianoche se oyo', 'medianoche', (.4, .5, 1.45), ('oscuro', 'niebla')); tem('clamor', 1.0)
s('pero las casas con sangre', 'medianoche', (.78, .55, 1.6), ('oscuro', 'polvo'))
s('y dios agrego un detalle', 'familia_cordero', (.45, .45, 1.6), ('polvo',))
s('mas de mil anos despues jesus muere', 'cruces', 'out', ('oscuro', 'polvo'))
s('a los crucificados', 'cruces', (.4, .45, 1.5), ('oscuro', 'polvo'))
s('y juan escribe', 'biblia', (.45, .62, 1.4), ('vela', 'polvo'), luz=[.07, .22])
s('por eso pablo dice', 'puerta', (.5, .45, 1.35), ('oscuro', 'polvo'))
s('que es cristo', 'cruces', [.5, .5, 1.5, .5, .45, 1.1], ('rayos', 'polvo'), luz=[.6, -.05], tdur=2.6)
r('cada familia debia', 'y la sangre os sera', 'Éxodo 12:5-7'); r('y la sangre os sera', 'a medianoche se oyo', 'Éxodo 12:13')
r('a medianoche se oyo', 'y dios agrego un detalle', 'Éxodo 12:29'); r('ni quebrareis', 'mas de mil anos despues jesus muere', 'Éxodo 12:46')
r('a los crucificados', 'por eso pablo dice', 'Juan 19:32-36'); r('nuestra pascua', 'en el desierto dios le dio', '1 Corintios 5:7')
# 6 · Levítico
cap('en el desierto dios le dio', 'LEVÍTICO 16-17', 'La sangre y la remisión')
s('en el desierto dios le dio', 'tabernaculo', 'in', ('polvo', 'niebla'))
s('en su interior habia un velo', 'sacerdote', (.75, .42, 1.45), ('vela', 'polvo'), luz=[.6, .3])
s('solo una vez al ano', 'sacerdote', (.48, .5, 1.4), ('vela', 'polvo'), luz=[.6, .3])
s('por que tanta sangre', 'sacerdote', (.53, .48, 1.8), ('vela', 'polvo'), luz=[.55, .45])
s('porque la vida de la carne', 'tabernaculo', (.5, .3, 1.5), ('rayos', 'polvo'), luz=[.5, -.1]); tem('porque la vida de la carne', .5)
s('el pecado cuesta una vida', 'ofrendas', (.3, .45, 1.4), ('polvo', 'niebla'), occ=2)
s('por eso el nuevo testamento', 'sangre_tierra', (.42, .8, 1.6), ('polvo',))
s('remision significa perdon', 'biblia', 'in', ('vela', 'polvo'), luz=[.07, .22])
s('pero habia un problema', 'tabernaculo', 'out', ('polvo',))
s('mas de mil anos despues en un aposento', 'copa', [.55, .66, 1.3, .6, .5, 1.55], ('vela', 'polvo'), luz=[.62, .3])
s('bebed de ella', 'copa', [.6, .5, 1.5, .62, .33, 1.85], ('vela', 'polvo'), luz=[.62, .3])
s('remision la misma palabra', 'copa', [.62, .4, 1.8, .55, .6, 1.3], ('vela', 'polvo'), luz=[.62, .3])
s('hebreos lo dice asi', 'sacerdote', (.75, .4, 1.6), ('rayos', 'vela', 'polvo'), luz=[.75, .3])
r('solo una vez al ano', 'por que tanta sangre', 'Hebreos 9:7'); r('porque la vida de la carne', 'el pecado cuesta una vida', 'Levítico 17:11', o2=2)
r('por eso el nuevo testamento', 'remision significa perdon', 'Hebreos 9:22'); r('pero habia un problema', 'mas de mil anos despues en un aposento', 'Hebreos 10:4')
r('bebed de ella', 'remision la misma palabra', 'Mateo 26:27-28'); r('hebreos lo dice asi', 'pero en el desierto el pueblo', 'Hebreos 9:12')
# 7 · Números 21
cap('pero en el desierto el pueblo', 'NÚMEROS 21', 'La serpiente de bronce')
s('pero en el desierto el pueblo', 'serpientes', 'in', ('polvo',))
s('hemos pecado', 'serpientes', (.6, .65, 1.5), ('polvo', 'oscuro')); tem('hemos pecado', 1.0)
s('moises oro por el pueblo', 'serpiente_bronce', 'out', ('rayos', 'polvo'), luz=[.62, -.05])
s('hazte una serpiente', 'serpiente_bronce', (.62, .3, 1.55), ('rayos', 'polvo'), luz=[.62, -.05]); tem('hazte una serpiente', .5)
s('no tenian que hacer nada', 'serpiente_bronce', (.4, .75, 1.5), ('polvo',))
s('siglos despues de noche', 'nicodemo', 'in', ('vela', 'polvo'), luz=[.5, .65])
s('y como moises levanto', 'nicodemo', (.68, .5, 1.55), ('vela', 'polvo'), luz=[.5, .65])
s('la cura colgaba', 'cruces', 'in', ('rayos', 'polvo'), **LUZ)
r('y vinieron serpientes', 'moises oro por el pueblo', 'Números 21:6-7'); r('hazte una serpiente', 'no tenian que hacer nada', 'Números 21:8')
r('y como moises levanto', 'la cura colgaba', 'Juan 3:14-15')
# 8 · Deuteronomio 18
cap('antes de morir moises', 'DEUTERONOMIO 18', 'Un profeta como Moisés')
s('antes de morir moises', 'serpiente_bronce', (.45, .55, 1.65), ('rayos', 'polvo'), luz=[.62, -.05])
s('moises saco al pueblo', 'puerta', 'in', ('oscuro', 'polvo'))
s('siglos despues cuando jesus', 'jordan', 'out', ('polvo',))
s('y pedro lo confirmo', 'pentecostes', 'in', ('polvo',))
r('profeta de en medio de ti', 'moises saco al pueblo', 'Deuteronomio 18:15'); r('este verdaderamente', 'y pedro lo confirmo', 'Juan 6:14')
r('y pedro lo confirmo', 'en uno de los libros', 'Hechos 3:22')
# 9 · Job
cap('en uno de los libros', 'JOB 19', 'Yo sé que mi Redentor vive')
s('en uno de los libros', 'job', 'in', ('polvo', 'niebla'))
s('yo se que mi redentor', 'job', (.6, .25, 1.5), ('rayos', 'polvo'), luz=[.62, -.05])
s('job no sabia su nombre', 'job', 'out', ('rayos', 'polvo'), luz=[.62, -.05])
r('yo se que mi redentor', 'job no sabia su nombre', 'Job 19:25-26')
# 10 · Salmo 16
cap('siglos despues el rey david', 'SALMO 16', 'No verá corrupción')
s('siglos despues el rey david', 'david', 'in', ('vela', 'polvo'), luz=[.72, .55])
s('porque no dejaras', 'david', (.32, .5, 1.5), ('vela', 'polvo'), luz=[.72, .55])
s('david murio y su cuerpo', 'pentecostes', 'out', ('polvo',))
s('a este jesus resucito', 'tumba', 'in', ('rayos', 'polvo'), luz=[.4, -.05])
r('porque no dejaras', 'david murio y su cuerpo', 'Salmo 16:10'); r('david murio y fue sepultado', 'pero hay un salmo', 'Hechos 2:29-32')
# 11 · Suspenso y cierre
s('pero hay un salmo', 'biblia', 'in', ('vela', 'polvo'), luz=[.07, .22])
s('manos y pies traspasados', 'cruces', (.5, .4, 1.7), ('oscuro', 'polvo'))
s('ropa repartida', 'multitud', 'in', ('polvo', 'oscuro'))
s('y despues vienen los profetas', 'pesebre', 'in', ('vela', 'polvo'), luz=[.35, .25])
s('un pueblo pequeno llamado belen', 'belen', 'in', ('polvo',))
s('un rey que entraria', 'burro', 'in', ('polvo',))
s('treinta monedas de plata', 'multitud', (.6, .3, 1.5), ('oscuro', 'polvo'))
s('un hombre traspasado', 'cruces', 'in', ('rayos', 'polvo'), **LUZ)
s('y una tumba', 'tumba', (.45, .5, 1.5), ('rayos', 'polvo'), luz=[.4, -.05])
s('todo eso estaba escrito', 'biblia', 'out', ('vela', 'polvo'), luz=[.07, .22])
cap('en la parte 2', 'PRÓXIMAMENTE', 'Estaba escrito · Parte 2', 6.0)
# --- verificación de anclas ---
mal = []
for x in P:
    if x['en'] and existe(x['en'][0], x['en'][1]) is None: mal.append(('plano', x['en'][0]))
for x in R:
    for k in ('desde', 'hasta'):
        if existe(x[k][0], x[k][1]) is None: mal.append(('ref', x[k][0]))
for x in CAPS + SH:
    if existe(x['en'][0], x['en'][1]) is None: mal.append(('cap/tem', x['en'][0]))
t = [existe(x['en'][0], x['en'][1]) if x['en'] else 0 for x in P]
desorden = [(P[i]['en'][0]) for i in range(1, len(t)) if t[i] is not None and t[i - 1] is not None and t[i] <= t[i - 1]]
print('planos', len(P), 'refs', len(R), 'capítulos', len(CAPS), 'temblores', len(SH))
malr = [(x['texto'], x['desde'][0]) for x in R if (existe(x['desde'][0], x['desde'][1]) or 0) >= (existe(x['hasta'][0], x['hasta'][1]) or 0)]
print('referencias al revés:', malr)
print('anclas que no existen:', mal); print('planos fuera de orden:', desorden)
json.dump({'escenas': P, 'capitulos': CAPS, 'refs': R, 'temblores': SH}, open('parte1/escenas.json', 'w'), ensure_ascii=False, indent=1)
