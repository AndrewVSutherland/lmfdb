
import ast
import re
from io import BytesIO
import time

from flask import render_template, request, url_for, make_response, redirect, send_file
from sage.all import QQ, PolynomialRing, PowerSeriesRing, conway_polynomial, prime_range, latex

from lmfdb import db
from lmfdb.utils import web_latex, parse_ints, search_wrap, flash_error, redirect_no_cache
from lmfdb.modlmf import modlmf_page
from lmfdb.modlmf.modlmf_stats import get_stats

modlmf_credit = 'Samuele Anni, Anna Medvedovsky, Bartosz Naskrecki, David Roberts'

# utilitary functions for displays


def print_q_expansion(lst):
    lst = [str(c) for c in lst]
    Qb = PolynomialRing(QQ, 'b')
    Qq = PowerSeriesRing(Qb['a'], 'q')
    return web_latex(Qq(lst).add_bigoh(len(lst)))


def my_latex(s):
    # This code was copy pasted and should be refactored
    ss = ""
    ss += re.sub(r'x\d', 'x', s)
    ss = re.sub(r"\^(\d+)", r"^{\1}", ss)
    ss = re.sub(r'\*', '', ss)
    ss = re.sub(r'zeta(\d+)', r'zeta_{\1}', ss)
    ss = re.sub('zeta', r'\zeta', ss)
    ss += ""
    return ss

# breadcrumbs and links for data quality entries

def get_bread(breads=[]):
    bc = [("mod &#x2113; modular forms", url_for(".index"))]
    bc.extend(b for b in breads)
    return bc

def learnmore_list():
    return [('Completeness of the data', url_for(".completeness_page")),
            ('Source of the data', url_for(".how_computed_page")),
            ('Labels', url_for(".labels_page"))]

# Return the learnmore list with the matchstring entry removed
def learnmore_list_remove(matchstring):
    return [t for t in learnmore_list() if t[0].find(matchstring) < 0]


# webpages: main, random and search results
@modlmf_page.route("/")
def modlmf_render_webpage():
    args = request.args
    if len(args) == 0:
        counts = get_stats().counts()
        characteristic_list = [2,3,5,7,11]
        max_lvl = min(counts['max_level'],150)
        level_list_endpoints = list(range(1, max_lvl + 1, 10))
        level_list = ["%s-%s" % (start, end - 1) for start, end in zip(level_list_endpoints[:-1], level_list_endpoints[1:])]
        max_wt = min(counts['max_weight'], 10)
        weight_list = list(range(1, max_wt + 1))
        label_list = ["3.1.0.1.1","13.1.0.1.1"]
        info = {'characteristic_list': characteristic_list, 'level_list': level_list,'weight_list': weight_list, 'label_list': label_list}
        credit = modlmf_credit
        t = 'Mod &#x2113; modular forms'
        bread = [('Modular forms', "/ModularForm"),('mod &#x2113;', url_for(".modlmf_render_webpage"))]
        info['counts'] = get_stats().counts()
        return render_template("modlmf-index.html", info=info, credit=credit, title=t, learnmore=learnmore_list_remove('Completeness'), bread=bread)
    else:
        return modlmf_search(args)


# Random modlmf
@modlmf_page.route("/random")
@redirect_no_cache
def random_modlmf():
    label = db.modlmf_forms.random()
    return url_for(".render_modlmf_webpage", label=label)

modlmf_label_regex = re.compile(r'(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d*)')

def split_modlmf_label(lab):
    return modlmf_label_regex.match(lab).groups()

def modlmf_by_label(lab):
    if db.modlmf_forms.exists({'label': lab}):
        return render_modlmf_webpage(label=lab)
    if modlmf_label_regex.match(lab):
        flash_error("The mod &#x2113; modular form %s is not recorded in the database or the label is invalid", lab)
    else:
        flash_error("No mod &#x2113; modular form in the database has label %s", lab)
    return redirect(url_for(".modlmf_render_webpage"))

#download
download_comment_prefix = {'magma':'//','sage':'#','gp':'\\\\'}
download_assignment_start = {'magma':'data := ','sage':'data = ','gp':'data = '}
download_assignment_end = {'magma':';','sage':'','gp':''}
download_file_suffix = {'magma':'.m','sage':'.sage','gp':'.gp'}


def download_search(info):
    lang = info["Submit"]
    filename = 'mod_l_modular_forms' + download_file_suffix[lang]
    mydate = time.strftime("%d %B %Y")
    # reissue saved query here

    proj = ['characteristic', 'deg', 'level', 'min_weight', 'conductor']
    res = list(db.modlmf_forms.search(ast.literal_eval(info["query"]), proj))

    c = download_comment_prefix[lang]
    s = '\n'
    s += c + ' Mod l modular forms downloaded from the LMFDB on %s. Found %s mod l modular forms.\n\n' % (mydate, len(res))
    s += ' Each entry is given in the following format: field characteristic, field degree, level, minimal weight, conductor.\n\n'
    list_start = '[*' if lang == 'magma' else '['
    list_end = '*]' if lang == 'magma' else ']'
    s += download_assignment_start[lang] + list_start + '\\\n'
    for r in res:
        for m in proj:
            s += ",\\\n".join(str(r[m]))
    s += list_end
    s += download_assignment_end[lang]
    s += '\n'
    strIO = BytesIO()
    strIO.write(s.encode('utf-8'))
    strIO.seek(0)
    return send_file(strIO, download_name=filename, as_attachment=True)

@search_wrap(template="modlmf-search.html",
             table=db.modlmf_forms,
             title='Mod &#x2113; modular forms search results',
             err_title='Mod &#x2113; modular forms search error',
             shortcuts={'download':download_search,
                        'label':lambda info:modlmf_by_label(info.get('label'))},
             projection=['label','characteristic','deg','level','weight_grading'],
             bread=lambda:[('Modular forms', "/ModularForm"),('mod &#x2113;', url_for(".modlmf_render_webpage")),('Search results', ' ')],
             learnmore=learnmore_list,
             properties=lambda:[])
def modlmf_search(info, query):
    for field, name in (('characteristic','Field characteristic'),('deg','Field degree'),
                        ('level', 'Level'),('conductor','Conductor'),
                        ('weight_grading', 'Weight grading')):
        parse_ints(info, query, field, name)
    # missing search by character, search up to twists and gamma0, gamma1

@modlmf_page.route('/<label>')
def render_modlmf_webpage(**args):
    data = None
    if 'label' in args:
        lab = args.get('label')
        data = db.modlmf_forms.lookup(lab)
    if data is None:
        t = "Mod &#x2113; modular form search error"
        bread = [('mod &#x2113; modular forms', url_for(".modlmf_render_webpage"))]
        flash_error("%s is not a valid label for a mod &#x2113; modular form in the database.", lab)
        return render_template("modlmf-error.html", title=t, properties=[], bread=bread, learnmore=learnmore_list())
    info = {}
    info.update(data)

    info['friends'] = []

    bread = [('Modular forms', "/ModularForm"),('mod &#x2113;', url_for(".modlmf_render_webpage")), ('%s' % data['label'], ' ')]
    credit = modlmf_credit

    for m in ['characteristic','deg','level','weight_grading', 'n_coeffs', 'min_theta_weight', 'ordinary']:
        info[m] = int(data[m])
    info['atkinlehner'] = data['atkinlehner']
    info['dirchar'] = str(data['dirchar'])
    info['label'] = str(data['label'])
    if data['reducible']:
        info['reducible'] = data['reducible']
    info['cuspidal_lift'] = data['cuspidal_lift']
    info['cuspidal_lift_weight'] = int(data['cuspidal_lift'][0])
    info['cuspidal_lift_orbit'] = str(data['cuspidal_lift'][1])

    if data['cuspidal_lift'][2] == 'x':
        info['cuspidal_hecke_field'] = 1
    else:
        info['cuspidal_hecke_field'] = latex(data['cuspidal_lift'][2])

    info['cuspidal_lift_gen'] = data['cuspidal_lift'][3]

    if data['theta_cycle']:
        info['theta_cycle'] = data['theta_cycle']

    info['coeffs'] = [str(s).replace('x','a').replace('*','') for s in data['coeffs']]

    if data['deg'] != 1:
        try:
            pol = str(conway_polynomial(data['characteristic'], data['deg'])).replace('x','a').replace('*','')
            info['field'] = pol
        except Exception:
            info['field'] = ""

    ncoeff = int(round(20/data['deg']))
    av_coeffs = min(data['n_coeffs'],100)
    info['av_coeffs'] = int(av_coeffs)
    if data['coeffs'] != "":
        coeff = [info['coeffs'][i] for i in range(ncoeff+1)]
        info['q_exp'] = my_latex(print_q_expansion(coeff))
        info['q_exp_display'] = url_for(".q_exp_display", label=data['label'], number="")
        p_range = prime_range(av_coeffs)
        info['table_list'] = [[p_range[i], info['coeffs'][p_range[i]]] for i in range(len(p_range))]
        info['download_q_exp'] = [
            (i, url_for(".render_modlmf_webpage_download", label=info['label'], lang=i)) for i in ['gp', 'magma','sage']]

        t = "Mod "+str(info['characteristic'])+" modular form "+info['label']
    info['properties'] = [
        ('Label', '%s' % info['label']),
        ('Field characteristic', '%s' % info['characteristic']),
        ('Field degree', '%s' % info['deg']),
        ('Level', '%s' % info['level']),
        ('Weight grading', '%s' % info['weight_grading'])]
    return render_template("modlmf-single.html", info=info, credit=credit, title=t, bread=bread, properties=info['properties'], learnmore=learnmore_list(), KNOWL_ID='modlmf.%s' % info['label'])


#auxiliary function for displaying more coefficients of the theta series
@modlmf_page.route('/q_exp_display/<label>/<number>')
def q_exp_display(label, number):
    try:
        number = int(number)
    except Exception:
        number = 20
    number = max(number, 20)
    number = min(number, 150)
    coeffs = db.modlmf_forms.lookup(label, projection='coeffs')[:number+1]
    return print_q_expansion(coeffs)


#data quality pages
@modlmf_page.route("/Completeness")
def completeness_page():
    t = 'Completeness of mod &#8467; modular form data'
    bread = [('Modular forms', "/ModularForm"),('mod &#x2113;', url_for(".modlmf_render_webpage")),('Completeness', '')]
    credit = modlmf_credit
    return render_template("single.html", kid='dq.modlmf.extent',
                           credit=credit, title=t, bread=bread, learnmore=learnmore_list_remove('Completeness'))

@modlmf_page.route("/Source")
def how_computed_page():
    t = 'Source of mod &#8467; modular form data'
    bread = [('Modular forms', "/ModularForm"),('mod &#x2113;', url_for(".modlmf_render_webpage")),('Source', '')]
    credit = modlmf_credit
    return render_template("single.html", kid='dq.modlmf.source',
                           credit=credit, title=t, bread=bread, learnmore=learnmore_list_remove('Source'))

@modlmf_page.route("/Labels")
def labels_page():
    t = 'Label of a mod &#x2113; modular forms'

    bread = [('Modular forms', "/ModularForm"),('mod &#x2113;', url_for(".modlmf_render_webpage")), ('Labels', '')]
    credit = modlmf_credit
    return render_template("single.html", kid='modlmf.label',
                           credit=credit, title=t, bread=bread, learnmore=learnmore_list_remove('Labels'))

@modlmf_page.route('/<label>/download/<lang>/')
def render_modlmf_webpage_download(**args):
    response = make_response(download_modlmf_full_lists(**args))
    response.headers['Content-type'] = 'text/plain'
    return response


def download_modlmf_full_lists(**args):
    label = str(args['label'])
    res = db.modlmf_forms.lookup(label, projection=['characteristic', 'deg', 'coeffs'])
    mydate = time.strftime("%d %B %Y")
    if res is None:
        return "No such modlmf"
    lang = args['lang']
    c = download_comment_prefix[lang]
    outstr = c + ' List of q-expansion coefficients downloaded from the LMFDB on %s. \n\n' % (mydate)
    if lang == 'magma':
        outstr += 'F<x>:=FiniteField(%s,%s); \n' % (res['characteristic'], res['deg'])

    elif lang == 'sage':
        outstr += 'F.<x>=GF({0}^({1}), conway_polynomial({0},{1})) \n'.format(res['characteristic'], res['deg'])

    outstr += '\\\n'
    outstr += download_assignment_start[lang] + '\\\n'
    outstr += str(res['coeffs']).replace("'", "").replace("u", "")
    outstr += download_assignment_end[lang]
    outstr += '\n'
    return outstr
