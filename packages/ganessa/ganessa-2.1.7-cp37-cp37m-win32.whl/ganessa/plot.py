# -*- coding: utf-8 -*-
'''
Created on 13 juin 2018

@author: Jarrige_Pi
'''
from __future__ import (unicode_literals, print_function, absolute_import)
from os.path import splitext
from sys import modules
from math import sqrt, floor
from numbers import Number
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter
from ganessa.util import strf3, unistr, ws, tsadd, scaladjust, is_wq

#****g* ganessa.plot/functions_plot
#****

#****f* functions_plot/layout
# PURPOSE
#   Determines the number of pages, lines and columns of a figure
# SYNTAX
#   npages, nlines, ncols = layout(nbplots [, nlmax=6 ] [, ncmax= 4] [, orient= 'h'])
# ARGUMENT
#   * int nbplots: number of graph to plot
#   * int nlmax (optional, default 6): max nb of graphs per column
#   * int ncmax (optional, default 4): max nb of graphs per line
#   * char orient (optional, default 'h'): orientation of the layout (h or v)
# RESULT
#   * int npages:  number of pages to plot
#   * int nlines:  number of lines per page
#   * int ncols:   number of columns per page
# EXAMPLE
#   - nf, nl, nc = layout(len(mes))
#   - for i in range(nf):
#   -     plotmes(graphs[i*nl*nc:(i+1)*nl*nc] , ...)
#****
def layout(nbplots, nlmax=6, ncmax=4, orient=''):
    'Calcul du nb de pages, lignes et de colonnes du plot'
    if nbplots < 2:
        return 1, 1, 1
    nf = (nbplots + nlmax*ncmax - 1) // (nlmax*ncmax)
    nbplots = (nbplots + nf - 1) // nf
    if not orient:
        orient = 'v' if  nlmax > ncmax + 1 else 'h'
    if orient[0].lower() in ('l', 'h'):
        nl = min(nlmax, int(floor(0.5 + sqrt(nbplots))))
        nc = (nbplots + nl -1) // nl
    else:
        nc = min(ncmax, int(floor(sqrt(nbplots))))
        nl = (nbplots + nc -1) // nc
    return nf, nl, nc

#****f* functions_plot/plotmes, plotmesx, pageplot, pageplotx
# PURPOSE
#   * plotmes plots one or more time series of the same kind in a single page.
#   * plotmesx plots one or more time series of the same kind on one or more figures.
#     it makes use of layout in order to determine the number of pages.
#   * pageplot plots a table of time series.
#   * plot_close allows to clean up matplotlib scraps and should be called
#     before the script ends.
# SYNTAX
#   * plotmes(mes, attr  [, nl=3 ]  [, nc=2 ] [, cmt='' ] [, fgname=''] [, inter=True]  [, orient= 'h'])
#   * plotmesx(mes, attr [, nlx=6 ] [, ncx=4 ] [, cmt='' ] [, fgname=''] [, inter=True]  [, orient= 'h'])
#   * pageplot(tsl, title [, nl=3 ] [, nc=2 ] fgname=''] [, inter=True] [, lang='FR']  [, orient= 'h'])
#   * pageplotx(tsl, title [, nlx=3 ] [, ncx=2 ] fgname=''] [, inter=True] [, lang='FR']  [, orient= 'h'])
#   * plot_close()
# ARGUMENT
#   * list mes: either a list of element ids, for which the result time series
#     will be retrieved from the result file. If a measurement is associated
#     with an id, it will also be displayed on the same id graph.
#   * or a list of (id, ftime, fval), in which case the additional
#     time serie (ftime, fval) will be plotted on the id graph.
#   * list tsl: list of (id, tvec, vvec [,vvec2]) to be plotted, one per graph.
#   * string attr: attribute to be plotted
#    (or attr:DA for residual or attr:DR for relative residual)
#   * string title: title for pageplot(x). If tsl contains 2 data series, title can
#     be given as a tuple (title, legend1, legend2).
#   * nl, nc: number of lines and columns of plots in the page (plotmes and pageplot only)
#   * nlx, ncx: maximum number of lines and columns of plots in the page (plotmesx and pageplotx only)
#   * cmt: optional comment appended to the title
#   * string fgname: output file name - if not nul, the plot will be saved
#     into a filename with extension '.png'.
#   * bool inter: if False, no plot is displayed
#   * char orient (optional, default 'h'): orientation of the layout (h or v)
# REMARK
#   Type of data and units are displayed (in french) in the figure title
# HISTORY
#   - 170426: improvement of x axis labels when time horizon > 24h
#   - 170618 (1.7.6): added pageplot
#   - 171120 (1.8.5): added plot_close
#   - 180924 (2.0.1): added orient kw
#   - 181105 (2.0.3): added pageplotx
#   - 200103 (2.0.8): plot reference before simulation
#   - 200315 (2.1.1): plot chlorine
#   - 200603 (2.1.3): single (static) measurement plotted as an horizontal line
#   - 200915 (2.1.5): pageplot(x) allows multiple ts per graph.
#   - 210111 (2.1.6): fix an overflow error plotting long TS (> 248 days)
#   - 210301 (2.1.7): optionnally plot bottom & top tank levels ('*' marker)
#****
PLOT_BOUNDS_MARKERS = '*#&='
def plotmesx(mes, symbattr, nlx=6, ncx=4, cmt='', fgname=None, inter=True, orient=''):
    '''Multiple plots on one or more pages'''
    if fgname:
        fnam, fext = splitext(fgname)
        fnam += '_' + symbattr.strip(PLOT_BOUNDS_MARKERS).strip()
        fgni = fnam + fext
    else:
        fgni = None
    nf, nl, nc = layout(len(mes), nlx, ncx, orient)
    if nf == 1:
        plotmes(mes, symbattr, nl, nc, cmt, fgni, inter, orient)
        return
    for i in range(nf):
        si = '_' + str(i+1)
        if fgname:
            fgni = fnam + si + fext
        plotmes(mes[i*nl*nc:(i+1)*nl*nc], symbattr, nl, nc, cmt=cmt + si,
                fgname=fgni, inter=inter, orient=orient)

def plot_close():
    '''Ends up matplotlib'''
    # close matplotlib in order to avoid the error:
    # Fatal Python error: PyEval_RestoreThread: NULL tstate
    if 'matplotlib.pyplot' in modules:
        print('Closing matplotlib...')
        plt.close('all')

def plotmes(mes, symbattr, nl=3, nc=2, cmt='', fgname=None, inter=True, orient='h'):
    ''' Trace de series de resultats Piccolo
        mes: liste des points e tracer, chacun se presentant:
            soit sous forme d'un identifiant 'id'
                -> l'attribut symb sera trace
            soit sous forme d'un tuple ('id', vecteur dates, vecteur valeurs de reference)
                -> l'attribut symb sera trace ainsi que le vecteur de reference
            si une mesure est presente en ce point, elle sera tracee
        symb: symbole Piccolo du type de variable tracee ('Q', 'V', 'CH', 'P', 'NC' etc.)
            si le symbole contient '*' ont trace RD et TP si reservoir
        nl, nc: disposition du graphe en nl lignes par nc colonnes
        cmt: texte ajoute dans le titre
        fgname: nom du fichier resultat pour sauvegarde en plt
        inter: permet de ne pas afficher la courbe
    '''
    if 'ganessa.sim' not in modules:
        print('*** plotmes(x) must be used with "ganessa.sim".')
        return
    else:
        gans = modules['ganessa.sim']

    typmes = {'Q': gans.LINK, 'V': gans.LINK,
              'P': gans.NODE, 'CH': gans.NODE, 'C1': gans.NODE,
              'VC':gans.TANK, 'NC':gans.TANK, 'V%':gans.TANK, 'H':gans.TANK}
    libmes = {'Q': 'Debit', 'V': 'Vitesse',
              'P': 'Pression', 'CH': 'Charge', 'C1': 'Chlore',
              'VC':'Volume', 'NC':'Niveau', 'V%':'% remplissage', 'H':'Hauteur'}

    plot_bounds = set(PLOT_BOUNDS_MARKERS) & set(symbattr)
    symbattr = symbattr.strip(PLOT_BOUNDS_MARKERS)
    diff = symbattr.upper().split(':')
    symb = diff[0]
    bresidu = len(diff) > 1

    if is_wq(symb):
        nbts, tmax = gans.wqtslen(gans.NODE)
        tmin = 0
    else:
        nbts = gans.tslen()
        tmin, tmax, nbts = gans.tsinterv()
    if nbts == 0:
        print('*** plotmes(x): no EPS results available - quitting.')
        return

    nbh = 0.01*int(0.5 + (tmax-tmin)/36.)
    if nbh < 100:
        xscale, xunit = 3600., 'h'
        xstep = 6 if nbh < 40 else (12 if nbh < 80 else 24)
    else:
        xscale, xunit = 86400., 'jours'
        xstep = 1 if nbh < 1+24*9 else int(nbh/144)
    def xvals(t):
        'Conversion de seconde en heures/jour avec arrondi'
        return 0.01*int(0.5 + 100*(t/xscale))
    nbmes = len(mes)
    if inter:
        print(' plotting {:d} time serie(s) of {:d} steps on [{:.3s}, {:.3s}] {}'.format(
              nbmes, nbts, strf3(xvals(tmin)), strf3(xvals(tmax)),
              'hours' if xunit == 'h' else 'days'))
    if nbmes == 0:
        return

    strattr = gans.nodeattrs
    try:
        if typmes[symb] == gans.LINK:
            strattr = gans.linkattrs
    except KeyError:
        print('*** plotmes: unknown symbol:', symb)
        return
    # ajustement ponctuel du nb de graphes
    if not orient:
        orient = 'v' if  nl > nc + 1 else 'h'
    if nbmes > nc*nl:
        nl += 1
        if nbmes > nc*nl:
            nc += 1
    if orient[0].lower() in ('l', 'h'):
        fx, fy, ftop, fbottom, fleft, fright = 16, 9, 0.9, 0.1, 0.075, 0.95
        if nc == 1:
            fx, fleft, fright = 6, 0.125, 0.9
        elif nc == 2:
            fx, fleft, fright = 11, 0.1, 0.925
        if nl == 1:
            fy, ftop, fbottom = 3, 0.8, 0.2
        elif nl == 2:
            fy, ftop, fbottom = 6, 0.85, 0.15
    else:
        fx, fy, ftop, fbottom, fleft, fright = 9, 16, 0.9, 0.1, 0.075, 0.95
        if nc == 1:
            fx, fleft, fright = 6, 0.125, 0.9
        if nl == 1:
            fy, ftop, fbottom = 4, 0.8, 0.2
        elif nl == 2:
            fy, ftop, fbottom = 8, 0.85, 0.15
        elif nl == 3:
            fy, ftop, fbottom = 12, 0.875, 0.125
    fig = plt.gcf()
    if nc > 1 or nl > 2 or not fig:  #  or inter:
        if fig:
            plt.close(fig)
        fig = plt.figure(figsize=(fx, fy))
    else:
        fig.clf()
        fig.figsize = (fx, fy)
    y_formatter = ScalarFormatter(useOffset=False)
    if bresidu and diff[1] == 'DR':
        unit = ''
    else:
        unit = gans.getunitname(symb)
        if unit[0:2] == 'm3':
            unit = '$m^3' + unit[2:] +'$'
    title_plt = libmes[symb] + ' (' + unit + ')'
    if cmt:
        title_plt += ' ' + cmt
    plt.suptitle(title_plt, fontsize=18.)
    i = 0
    for item in mes[0:nl*nc]:
        if isinstance(item, tuple):
            eid, tr, r = item
        else:
            eid = item
        nom = strattr(eid, 'NO')
        nom = unistr(nom)
        id_titre = eid
        if nom and nom != eid:
            if len(nom) + len(eid) < 100 / nc:
                id_titre = eid + ' (' + nom + ')'
            else:
                id_titre = '(' + nom + ')'
        i += 1
        if i > nl*nc:
            if inter:
                print('*** Cannot plot: ', id_titre, ' - increase nc and/or nl')
            continue
        else:
            if inter:
                print(' plotting: ', eid, ws(nom))
        nbm = gans.mslen(typmes[symb], eid, symb)
        if nbm == 0 and bresidu:
            continue
        ax = plt.subplot(nl, nc, i)
        plt.rcParams['legend.loc'] = 'best'
        # Nota available in mpl 1.2
        # plt.rcParams['axes.formatter.useoffset'] = False
        # print ('    ... Found {:d} MS for id: {:s}'.format(nbm,eid))
        # if symb == 'C1':
        #     tv, v, nv = gans.tsval(typmes[symb], eid, symb, 60) # every min
        # else:
        tv, v, nv = gans.tsval(typmes[symb], eid, symb) # int(0.5+(tmax - tmin)/step)+1, step)
        ymin, ymax = 1, -1
        if isinstance(item, tuple):
            ax.plot(tr/xscale, r, 'g-', label='Reference')
            ymin, ymax = min(r), max(r)
        if not bresidu:
            ax.plot(tv/xscale, v, 'b-', label='Simulation')
            if ymin > ymax:
                ymin, ymax = min(v), max(v)
            else:
                ymin, ymax = min(ymin, min(v)), max(ymax, max(v))
        if nbm > 0:
            tm, m, nm = gans.ms(typmes[symb], eid, symb, nbm)
            if nm == 1:
                tm = np.array([tmin, tmax])
                m = np.hstack((m, m))
                nm = 2
            ymin, ymax = min(ymin, min(m)), max(ymax, max(m))
            if bresidu:
                tm, r, nm = tsadd(tm, -m, nm, tv, v, nv)
                mmax = max(abs(m)) * 0.0001
                if diff[1] == 'DA':
                    ax.plot(tm/xscale, r, 'g-', label='Simulation - Mesure')
                else:
                    tm, s, nm = tsadd(tm, abs(m), nm, tv, abs(v), nv)
                    s = r/(s+mmax)
                    ax2 = ax.twinx()
                    ax2.plot(tm/xscale, s, 'g-', label='Difference relative (S-M)')
                    dy2grid = 0.25*(max(s) - min(s))
                    if dy2grid == 0.0:
                        dy2grid = 1.0
                    ax2.yaxis.set_major_locator(MultipleLocator(scaladjust(dy2grid)))
                    ax2.yaxis.set_major_formatter(y_formatter)
                    for t2 in ax2.get_yticklabels():
                        t2.set_color('g')
            else:
                ax.plot(tm/xscale, m, 'r.' if nm > 2 else 'r-', label='Mesure')
        plt.xlim(xvals(tmin), xvals(tmax))
        plt.legend(fontsize=6.)
        if i > min(nc*nl, nbmes)-nc:
            plt.xlabel('temps (' + xunit + ')')
        # plt.ylabel(ylab)
        plt.title(id_titre, fontsize=2.*fx/nc * min(1., 42./(len(id_titre)+1)))
        if plot_bounds:
            if typmes[symb] == gans.TANK:
                if symb == 'V%':
                    vlow, vhigh = 0, 100
                elif symb == 'VC':
                    vlow, vhigh = 0, gans.tankattr(eid, 'VO')
                else: # if symb in ('NC', 'H'):
                    vlow, vhigh = gans.tankattr(eid, 'RD'), gans.tankattr(eid, 'TP')
                    if symb == 'H':
                        vlow, vhigh = 0, vhigh - vlow
                ymin, ymax = min(ymin, vlow), max(ymax, vhigh)
                tb = [xvals(tmin), xvals(tmax)]
                ax.plot(tb, [vlow]*2, '--c', tb, [vhigh]*2, '--c')
            else:
                ax.plot([tmin], [0], '--c')
                ymin, ymax = min(ymin, 0), max(ymax, 0)
        dygrid = 0.25*(ymax - ymin)

        if dygrid == 0.0:
            dygrid = 1.0
        ax.xaxis.set_major_locator(MultipleLocator(xstep))
        ax.yaxis.set_major_locator(MultipleLocator(scaladjust(dygrid)))
        ax.yaxis.set_major_formatter(y_formatter)
        plt.grid(True)
    plt.subplots_adjust(hspace=0.5, wspace=0.25,
                top=ftop, bottom=fbottom, left=fleft, right=fright)

    if fgname:
        plt.savefig(splitext(fgname)[0] + '.png')
    if inter:
        plt.ion()
        plt.show()
        # plt.close(fig)
    else:
        plt.clf()
        # plt.close(fig)
    del tv, v

def pageplot(mes, cmt, nl=3, nc=2, fgname=None, inter=True, lang='FR', orient=''):
    ''' Trace de series de donnees
        mes: liste des points e tracer, chacun se presentant:
            sous forme d'un tuple ('id', vecteur dates, vecteur(s) valeurs)
            -> si plusieurs vecteurs valeurs sont présents, ils ont le meme vecteur date
        cmt: titre du trace ou tuple (titre, legend1, legend2 ...) si plusieurs vecteurs
        nl, nc: disposition du graphe en nl lignes par nc colonnes
        fgname: nom du fichier resultat pour sauvegarde en plt
        inter: permet de ne pas afficher la courbe
    '''
    nbmes = len(mes)
    if nbmes == 0:
        return
    t = mes[0][1]
    tmin, tmax = min(t), max(t)
    for other_ts in mes[1:]:
        t = other_ts[1]
        tmin, tmax = min(tmin, min(t)), max(tmax, max(t))
    if isinstance(cmt, (tuple, list)):
        cmt, labels = cmt[0], cmt[1:]
    else:
        labels = []
    nbh = 0.01*int(0.5 + (tmax-tmin)/36.)
    if nbh < 100:
        xscale, xunit = 3600., 'h'
        xstep = 6 if nbh < 40 else (12 if nbh < 80 else 24)
    else:
        xscale, xunit = 86400., 'jours' if lang.upper() == 'FR' else 'days'
        xstep = 1 if nbh < 1+24*9 else int(nbh/144)
    def xvals(t):
        'Conversion de seconde en heures/jour avec arrondi'
        return 0.01*int(0.5 + 100*(t/xscale))
    if inter:
        print(' plotting {:d} time serie(s) on [{:.3s}, {:.3s}] {}'.format(
                 nbmes, strf3(xvals(tmin)), strf3(xvals(tmax)),
                 'hours' if xunit == 'h' else 'days'))

    if not orient:
        orient = 'v' if  nl > nc + 1 else 'h'
    # ajustement ponctuel du nb de graphes
    if nbmes > nc*nl:
        nl += 1
        if nbmes > nc*nl:
            nc += 1
    if orient[0].lower() in ('l', 'h'):
        fx, fy, ftop, fbottom, fleft, fright = 16, 9, 0.9, 0.1, 0.075, 0.95
        if nc == 1:
            fx, fleft, fright = 6, 0.125, 0.9
        elif nc == 2:
            fx, fleft, fright = 11, 0.1, 0.925
        if nl == 1:
            fy, ftop, fbottom = 3, 0.8, 0.2
        elif nl == 2:
            fy, ftop, fbottom = 6, 0.85, 0.15
    else:
        fx, fy, ftop, fbottom, fleft, fright = 9, 16, 0.9, 0.1, 0.075, 0.95
        if nc == 1:
            fx, fleft, fright = 6, 0.125, 0.9
        if nl == 1:
            fy, ftop, fbottom = 4, 0.8, 0.2
        elif nl == 2:
            fy, ftop, fbottom = 8, 0.85, 0.15
        elif nl == 3:
            fy, ftop, fbottom = 12, 0.875, 0.125
    fig = plt.gcf()
    if nc > 1 or nl > 2 or not fig:  #  or inter:
        if fig:
            plt.close(fig)
        fig = plt.figure(figsize=(fx, fy))
    else:
        fig.clf()
        fig.figsize = (fx, fy)
    y_formatter = ScalarFormatter(useOffset=False)
    plt.suptitle(cmt, fontsize=18.)
    i = 0
    time_legend = 'temps' if lang.upper() == 'FR' else 'time'
    label1 = dict(label=labels[0]) if labels else {}
    label2 = dict(label=labels[1]) if len(labels) > 1 else {}
    for single_ts in mes[0:nl*nc]:
        eid, tr, r = single_ts[0:3]
        id_titre = eid
        i += 1
        if i > nl*nc:
            if inter:
                print('*** Cannot plot: ', id_titre, ' - increase nc and/or nl')
            continue
        if inter:
            print(' plotting: ', eid)
        ax = plt.subplot(nl, nc, i)
        # plt.rcParams['legend.loc'] = 'best'
        ymin, ymax = min(r), max(r)
        ax.plot(tr/xscale, r, 'g-', **label1)
        if len(single_ts) > 3:
            s = single_ts[3]
            if isinstance(s, Number):
                ax.plot([xvals(tmin), xvals(tmax)], [s]*2, 'b-', **label2)
                ymin, ymax = min(ymin, s), max(ymax, s)
            else:
                ax.plot(tr/xscale, s, 'b-', **label2)
                ymin, ymax = min(ymin, min(s)), max(ymax, max(s))
        plt.xlim(xvals(tmin), xvals(tmax))
        if i > min(nc*nl, nbmes)-nc:
            plt.xlabel(time_legend + ' (' + xunit + ')')
        # plt.ylabel(ylab)
        if labels:
            plt.legend(fontsize=6.)
        plt.title(id_titre, fontsize=2.*fx/nc * min(1., 42./(len(id_titre)+1)))
        dygrid = 0.25*(ymax - ymin)
        if dygrid == 0.0:
            dygrid = 1.0
        ax.xaxis.set_major_locator(MultipleLocator(xstep))
        ax.yaxis.set_major_locator(MultipleLocator(scaladjust(dygrid)))
        ax.yaxis.set_major_formatter(y_formatter)
        plt.grid(True)
    if nbmes > 1:
        plt.subplots_adjust(hspace=0.5, wspace=0.25,
                top=ftop, bottom=fbottom, left=fleft, right=fright)

    if fgname:
        plt.savefig(splitext(fgname)[0] + '.png')
    if inter:
        plt.ion()
        plt.show()
        # plt.close(fig)
    else:
        plt.clf()
        # plt.close(fig)

def pageplotx(mes, cmt, nlx=6, ncx=4, fgname=None, inter=True, lang='FR', orient=''):
    '''Multipage plot'''
    if fgname:
        fnam, fext = splitext(fgname)
        fgni = fnam + fext
    else:
        fgni = None
    nf, nl, nc = layout(len(mes), nlx, ncx, orient)
    if nf == 1:
        pageplot(mes, cmt, nl, nc, fgname, inter, lang, orient)
        return
    for i in range(nf):
        si = '_' + str(i+1)
        if fgname:
            fgni = fnam + si + fext
        pageplot(mes[i*nl*nc:(i+1)*nl*nc], cmt + si, nl, nc,
                fgname=fgni, inter=inter, lang='FR', orient=orient)
