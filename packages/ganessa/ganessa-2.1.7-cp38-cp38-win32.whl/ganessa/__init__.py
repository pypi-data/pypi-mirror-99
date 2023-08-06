# -*- coding: utf-8 -*-
'''ganessa integration package for PicWin32/Ganessa_SIM/Ganessa_TH - see pyGanessa.html'''
from __future__ import unicode_literals
# Version of the package
__version__ = '2.1.7'

#****g* ganessa.sim&th/About
# PURPOSE
#   The module ganessa.sim (resp. ganessa.th) provides a Python interface
#   to Picwin32.dll and Ganessa_SIM.dll (resp. Ganessa_TH.dll) kernel API.
#   Starting with version 2, it is compatible with 32 and 64 bits versions
#   of python 3.6/3.7.
#   Starting with version 2.1, it is compatible with python 3.7.6 and 3.8.
#
#   The module name ganessa.sim&th is used for items availble both
#   in .sim and .th environments
# INSTALLATION
#   pip install ganessa
#
#   The package expects the simulation kernel .dll to be found either
#   in the folders given by %GANESSA_DIR environment variable (for Ganessa_xx.dll)
#   or %PICCOLO_DIR (for Picwin32.dll),
#   or in the %PATH environment variable (either name),
#   or in one of the sub folders of Program Files folder (x86 under Windows 7):
#   * "Safege/Ganessa_<lang>/Ganessa_xx" (xx = SIM or TH) or
#   * "Gfi Progiciels/Piccolo6_<lang>[_ck | _cl]/Picwin32.dll" or
#   * "Gfi Progiciels/Picalor6_<lang>[_ck | _cl]/Picwin32.dll" or
#   * "Adelior/Piccolo5_<lang>/Picwin32.dll"
#   in either drive D: or C:
# USE
#   Syntax:
#   * import ganessa.sim as pic   (or ganessa.th for Picalor)
#   * pic.cmdfile('my file.dat')
#   Or:
#   * from ganessa.sim import *
#   * cmdfile('my file.dat')
#
#   the import will perform the following initialisation tasks:
#   * locate Ganessa_xx.dll or Picwin32.dll kernel
#   * initialise it
#   * locate result.bin in a working subdirectory
#   * bind termination to ctrl+Z
# CONTENT
#   The package provides the following content:
#   * constants for calling API functions
#   * iterators for browsing objects and selections
#   * functions for loading .bin file
#   * functions for executing command files / command strings / running simulations
#   * functions for catching simulation errors and retrieving unstable items
#   * functions for retrieving individual objects attributes
#   * functions for retrieving table entries and object count
#   * functions for retrieving result or measurements time series
#   * functions for retrieving min / max / avg values for all objects
#
# REMARKS
#   * Most of the functions are getter. A few direct setter functions are provided
#     (setlinkattr, setdensity, defcalind, *SHL functions). The general purpose
#     gencmd(w), addcmd(w), cmd, execute and cmdfile can be used to build / commit
#     any other settings with command language (see the Piccolo Reference Manual).
#   * Commands (passed to cmd, execute, cmdfile) should be built in the language
#     (idiom) of the current version. getkeyword, modulekeyword, attrkeyword allow
#     to retrieve a given keyword in the current idiom; gencmd(w) allow to build a
#     command line in the current idiom.
#   * A command file may be written in any of English, French or Spanish, the current
#     command language interpreter will switch to the xxx language from _LANG_ xxx
#     command until the end of the file, then switch back to the current language.
#   * Any suggestion for extending / improving can be mailed to: piccolo@safege.fr
#
# HISTORY
#   The history of the package is:
#   * 1.0.3: plotmesx png takes care of measurement type
#   * 1.0.4: added demand getter for a demand code or for all
#   * 1.0.5: added Windows 7 paths 'program files (x86)';
#            added option to get TS by measurement step 'tsvalbymts';
#            added 'refdate' : retireval of REFDATE
#   * 1.0.6: correction to the grid adjustment in plotmes (util)
#   * 1.0.7: getMinMax can be called with a selection name
#   * 1.0.8: save function
#   * 1.0.9: SimulationError exception catching + save(identical to MMI);
#            requires numpy 1.8.1
#   * 1.1.0: same as 1.0.9 but requires only numpy 1.7.1
#   * 1.1.1: minor change to codewinfile=winstr
#   * 1.1.2: added 'execute' for multiple commands as strings (\n managed as a separator)
#   * 1.1.3: (141104) disable useoffset for Y axes in 'util.plotmes'
#   * 1.1.4: (141118) handling Picwin32.dll provided by GFI after 18-11-2014 (best 03-12-2014)
#   * 1.1.5: (141205) handling ts < ms in tsvalbymts
#   * 1.1.6: (150127) nodexyz added + bugfix in attrs documentation
#   * 1.1.7: (150309) minor grammatical changes
#   * 1.2.0: (150507) change in folder search order (ws7 priority) + language - OK with Picwin32 151203
#   * 1.2.1: (150527) Picalor enabled  as ganessa.th + density and SHL management;
#            (150603) added 'meanattr';
#            (150610) added 'addSHLtype'
#   * 1.2.2: (150709) bug fix calls select* from Selected
#   * 1.2.3: (150812) bug fix: return value of browseWQ; getall
#   * 1.2.4: (150910) constants added (WQ, Inverse Pb) + demandcodes
#   * 1.2.5: (150922) utils: tuning of plotmes subtitle fontsize for large titles
#                      + constants (MOD, NOD ...) + 'areas' function
#   * 1.2.6: (151128) added tsdemand and tsdemandlen, tsdevice and tsdevicelen;
#                     added tables (material, area etc.) access;
#                     utils: added list2file
#   * 1.3.0: (151202) added support for compatibility with Picwin32 12/2014, 12/2015 and Ganessa;
#            (151206) addl constants (BRA, DYN, RSV);
#            (151218) reviewed compatibility with Picwin32 (2015+ -> Piccolo6), (2014 -> Piccolo5)
#   * 1.3.1: (160108) header, footer and suffix optional args for utils.list2file;
#            (160113) added memory allocation error exception (inverse module)
#   * 1.3.2: (160118) added retrieval of problematic devices;
#            (160126) added 'H' tank attribute in util.plotmes(x)
#   * 1.3.3: (160226) added getindex, tankattrs, linkattr and linkattrs
#   * 1.3.4: (160301) added constants for inverse pb;
#            (160309) added inverse simulation summary;
#            (160318) added added nxxxxattr and nxxxxatrs function for getting attributes by index;
#            (160325) added file quote as needed in save function;
#            (160329) corrected doc (selectlen/select);
#            (160405) corrected doc, added linkXYZV;
#            (160408) utils: strloc, strf3loc
#   * 1.3.5: (160410) added init(folder)
#   * 1.3.6: (160511) added 'symmetric_node' (Ganessa_TH);
#            (160531) reviewed compatibility with dll versions since 2014.
#   * 1.3.7: (160622) added OpenFileMMI classes: SelectModel, SelectFile, ExecStatus;
#            (160706) added 'dist2link'; added 'util.dist_to_poly' as pure python backup;
#                     OpenFileMMI uses simulation interface from caller, or None;
#                     changed all classes to new style;
#                     added 'len' method to 'Selected' and 'Elements'; added 'Graph'
#   * 1.4.0: (160715) setup changed to build whl from source files;
#            (160719) minor bug fix in util.plotmes - reuse same fig in non interactive mode
#   * 1.4.1: (160820) OpenFileMMI SelectFile with null extension; load error handling
#   * 1.4.2: (160830) added AUTO and QUAL storestep constants; minor fix in gencmd;
#                     added include_depth optional attribute to 'linkxyzv';
#            (160915) added version_2016b in the Picwin32 lookup table;
#            (160919) added SelectFolder in OpenFileMMI;
#            (160922) added setlinkattr as a synonym of setbranchattr;
#            (160927) intermediate API for Piccolo6 2016 B (dec-2016)
#   * 1.5.0: (161010) added 'getkeyword';
#            (161019) minor change in util.plotmes: 160719 patch reviewed for better output;
#            (161124) added 'stat_quantiles', 'stat_duration', and 'Dynamic_Stats'
#   * 1.5.1  (161212) bug fix on ts* functions without result file;
#                     added 'retry' optional argument to full_solveH
#   * 1.5.2  (170105) added folder=option in util.list2file
#            (170110) build with numpy 1.11.0 - compatible with
#   * 1.7.0  (170119) build with BIND(C) instead of DEC$ATTRIBUTE C, REFERENCE;
#                     required with ganessa_SIM > 170117 (renamed API functions);
#            (170125) added fixed_interval to tsdevice, now return float values
#   * 1.7.1  (170221) minor changes in util.Inifile (default encoding utf-8);
#                     switch to unicode_literals in sim&th, util and prot;
#            (170223) added compiled util.dist, util.dist_p_seg, util.dist_to_poly
#   * 1.7.2  (170228) added OpenFileMMI.setlanguage function (FR/US or UK);
#            (170304) fix getMinMax/getallminmax break in 1.7.0
#   * 1.7.3  (170313) added WQ, MOD and LNK constants; added DICT.END;
#                     added modulekeyword and attrkeyword;
#            (170331) added shearstr; match Piccolo 2017 --> NO !
#   * 1.7.4  (170407) added silent option to init;
#            (170424) added default '@safege.com' domain to util.envoi_msg
#   * 1.7.5  (170426) improved util.plotmes(x) for horizon > 24h;
#            (170512) added module 'multithread';
#            (170515) fix parent.inidir error in OpenFileMMI; added solveH
#   * 1.7.6  (170613) added constants (STATIC, QUA.VISUSTEP) and util.group;
#                     minor bug fix in Selected, GetMinMax and Dynamic_Stats;
#            (170618) added title to OpenFileMMI.SelectFile and SelectFolder;
#                     added util.pageplot;
#            (170620) replaced litteral symbols with attrkeyword();
#            (170627) match Piccolo 2017 (apr 2017);
#   * 1.7.7  (170705) added cwfold;
#            (170707) optional arg for sim&th.close(arg) and prot.close(arg);
#                     added C1 in util.plotmes for chlorine plots;
#   * 1.7.8pr1 (170808) doc update; upload to pypi
#   * 1.7.8  (170817) replaced IniFile with json/xml version
#   * 1.7.9pr1 (170824) prepared for Piccolo 2017b;
#              (170830) added getunitcoef
#   * 1.8.0 (170907) sim.py split into core, core_sim, core_th; changed/fixed path lookup;
#           (170918) added resfile, raw_getcmdw, raw_stat_duration, raw_stat_quantiles
#   * 1.8.1 (171004) added util.update_package
#   * 1.8.2 (171016) added util.str2uni (tries utf8 the cp1252 - reverse from unistr);
#           (171018) minor bug fix for util.update_package;
#           (171103) added sort.HeapSort class and Graph.dtree
#   * 1.8.3 (171109) added error msg when OpenFileMMI is imported before sim or th;
#           (171110) fix _pyganutl import broken in 1.8.0 (util.dist, util.dist_to_poly);
#           (171114) added multithread.MultiProc class
#   * 1.8.4 (171120) bug fix / changed multithread.MultiProc.run return values as 3 lists
#   * 1.8.5 (171120) added util.plot_close to avoid Fatal Python error at exit;
#           (171128) added linkbbox and util.gbool
#   * 1.8.6 (171201) added progress keyword to parallel.Multiproc; full_version;
#                    added util.send_report
#   * 1.8.7 (171208) fix update_package not succeeding in update 'ganessa'
#   * 1.8.8 (171212) improved update_package proxy configuration using .json files;
#                    added Picwin32.dll lookup into PICCOLO_DIR environment variable
#                    and '_ck' optional folder suffix
#   * 1.8.9 (171220) updated full_version; added UPN lookup in send_report;
#           (180126) added importEpanet and exportEpanet
#   * 1.9.0 (180227) added con2uni for converting console output to unicode (cp850)
#           (180305) fixes related to 2to3: _getdll: environ; util: winstr and utf,
#                    Inifile encoding, cmp_version, added version_as_tuple
#           (180328) send_report timeout to 2 seconds, added util.is_text;
#                    2 and 3 compatibility changes for unistr, str2uni, utf2uni, ascii.
#   * 1.9.1 (180418) added a reduce function to parallel.MultiProc; fix seq run
#           (180502) update_package looks for package in current folder
#   * 1.9.2 (180514) fix python3 issue in parallel submodule; minor OpenFileMMI fixes
#           (180518) fix update_package compatibility with parallel
#   * 1.9.3 (180525) added epanet2 API and dll (py27 only); fix epanet.getlinknodes
#           (180530) added util.ws
#   * 1.9.4 (180531) fix utf-8 decoding for Inifile1L
#           (180604) fix getindex; added exists
#   * 1.9.5 (180607) added epanet2 API and dll (compiled from epanettools 0.4.2)
#           (180608) added an example in README
#           (180613) plot funcs moved from ganessa.util to ganessa.plot
#   * 1.9.6 (180615) fix sim.init handling non-ascii chars in folder name (uploaded 180621)
#   * 1.9.7 (180705) fix util.IniFile handling non-ascii chars in file name
#           (180718) fix OpenFileMMI issue with inidir
#           (180813) added support for Piccolo 2018 (released 2018-07-25) and uploaded
#   * 1.9.8 (180814) 64-bits version for Ganessa_SIM (python 3.6)
#                    minor OpenFileMMI changes (clear_exe, bt_exe_state)
#           (180815) upload wheels for python 3.7 (32 and 64 bits).
#   * 2.0.0 (180816) util.group fix (python 3.7); added verbose param in util.update_package
#           (180820) added 'wqtracevectsize' for returning the max size of WQ
#                    concentration vector usable for tracing origin of water
#           (180823) added geojsonfile for writing to geojson; fix minor midfile issue
#           (180829) added C:/Program Files lookup in x64 env; geojson reader
#           (180831) release and upload
#   * 2.0.1 (180910) util.list2file minor fix; doc fix; minor Elements changes
#           (180919) fix ganessa.th break in 2.0.0
#           (180924) added orient keyword in ganessa.plot functions; slight behavior change
#   * 2.0.2 (181003) added util.strf2loc; doc update
#           (181011) minor change in sim.seleclen; added util.call_until_false
#           (181025) minor fix in ganessa.prot
#           (181030) release and upload
#   * 2.0.3 (181105) added plot.pageplotx; (13) added '.' at head of prot lookup folders
#           (181119) changed geojson and midfile to conform to shapefile 2.0
#           (181203) added '_cl' suffix option to the Piccolo lookup folder;
#                    len for Selected, Elements and derived iterators
#           (181207) fix util.Inifile1L.save with python 3.x
#           (181209) doc updated; release and upload
#   * 2.0.4 (181218) debug mode for unicode control; util.Inifile.get returns ustr
#           (181220) OpenFileMMI.ExecStatus.clear: remove 'all' kwarg;
#                    added len to GetMinMax and DynamicStats iterators
#   * 2.0.5 (181229) added util.perfs
#           (190107) handle OpenFileMMI.SelectModel(usedef=False)
#           (190109) changes in update_package permission lookup
#           (190131) release and (190211) upload
#   * 2.0.6 (190411) minor fix in parallel.required_cpu
#           (190416) minor evolution to parallel.Multiproc: alternate erfun call on Exception
#           (190423) release and upload
#   * 2.0.7 (190617) added 'extra_data' keyword to sim.savemodel
#           (190715) added DYNSTOP SimulationError; minor doc fix
#           (190819) improved simulation error check in full_solveH, solveH, solveTH
#           (190821) added util.get_python_exe
#           (191007) minor fix in OpenFileMMI.SelectFile
#           (191008) release and upload
#   * 2.0.8 (191015) fix README.rst
#           (200106) added upstream and downstream methods to sim.Graph
#           (200204) fix new python 3.8 dll directory search
#                    release and upload (2.7-32 / 3.7 / 3.8 only)
#   * 2.0.9 (200205) fix prot with python 3.8 dll directory search + minor changes;
#                    release and upload (2.7-32 / 3.7 / 3.8 only)
#   * 2.1.0 (200214) fix urllib3 requiring proxy scheme in get_proxy
#           (200220) Piccolo versions 2017+ required for python 3.x+;
#                    fix to dll directory search, related to FlexLM; fix Example.py;
#                    release and upload (2.7-32 / 3.7 / 3.8 only)
#   * 2.1.1 (200306) new sim.WQsources() iterator
#           (200313) fix util.scaladjust for range below 1;
#                    fix chlorine (C1) plot.plotmes(x)
#           (200314) add added util.is_wq and sim.wqtslen; fix sim.tsval for WQ TS
#           (200323) doc fixes; add module constant KW (MOD kw, QUA, INV)
#                    add optional return_type=True kw to sim.Selected
#           (200324) fix workdir & result file in virtualstore;
#                    release and upload (2.7-32 / 3.7 / 3.8 only)
#   * 2.1.2 (200506) add util.IniFile.remove
#           (200511) release and upload (2.7-32 / 3.7 / 3.8 only)
#   * 2.1.3 (200603) plot.plotmes: single (static) measurement plotted as an horizontal line
#           (200604) OpenFileMMI.SelectModel: chdir to model folder to allow relative inner read
#           (200619) added en2emu sim-like minimal compatibility module
#           (200622) added nbvertices() and fake get_labels()
#           (200629) release and upload (2.7-32 / 3.7 / 3.8 only)
#   * 2.1.4 (200708) dll lookup in '.'
#           (200819) minor fix on plot.pageplot
#                    release and upload (2.7-32 / 3.7 / 3.8 only)
#   * 2.1.5 (200824) replace util.ascii with util.myascii
#           (200915) plot.pageplot(x) allows multiple ts per graph; fix cmdfile;
#           (200922) added demand profile query by zone and code/zone (tsdemand);
#           (201109) added util.read_as_idpic;
#           (201119) release and upload  (2.7-32 / 3.7 / 3.8 only)
#   * 2.1.6 (201221) fix prot error with null path chunks
#           (201222) fix Ganessa_TH integration not working properly
#           (210126) added util.split_poly_at; release and upload
#   * 2.1.7 (210301) plot.plotmes(x) plot tank bottom and top water level when prefixed with '=';
#           (210307) addl single value plot as horizontal line in plot.pageplot
#           (210310) add util.utf8_bom_encoding(file)
#           (210324) fix util.split_poly_at ValueError: not enough values to unpack (expected 3, got 2)
#
#           postponed: <<add epanet 2.2.0 API as _epanet22 - same interface as _epanet2>>.
#****
