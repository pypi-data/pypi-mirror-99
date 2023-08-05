#                     GNU GENERAL PUBLIC LICENSE
#                        Version 3, 29 June 2007
#
#  Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
#  Everyone is permitted to copy and distribute verbatim copies
#  of this license document, but changing it is not allowed.
#
#                             Preamble
#
#   The GNU General Public License is a free, copyleft license for
# software and other kinds of works.
#
#   The licenses for most software and other practical works are designed
# to take away your freedom to share and change the works.  By contrast,
# the GNU General Public License is intended to guarantee your freedom to
# share and change all versions of a program--to make sure it remains free
# software for all its users.  We, the Free Software Foundation, use the
# GNU General Public License for most of our software; it applies also to
# any other work released this way by its authors.  You can apply it to
# your programs, too.
#
#   When we speak of free software, we are referring to freedom, not
# price.  Our General Public Licenses are designed to make sure that you
# have the freedom to distribute copies of free software (and charge for
# them if you wish), that you receive source code or can get it if you
# want it, that you can change the software or use pieces of it in new
# free programs, and that you know you can do these things.
#
#   To protect your rights, we need to prevent others from denying you
# these rights or asking you to surrender the rights.  Therefore, you have
# certain responsibilities if you distribute copies of the software, or if
# you modify it: responsibilities to respect the freedom of others.
#
#   For example, if you distribute copies of such a program, whether
# gratis or for a fee, you must pass on to the recipients the same
# freedoms that you received.  You must make sure that they, too, receive
# or can get the source code.  And you must show them these terms so they
# know their rights.
#
#   Developers that use the GNU GPL protect your rights with two steps:
# (1) assert copyright on the software, and (2) offer you this License
# giving you legal permission to copy, distribute and/or modify it.
#
#   For the developers' and authors' protection, the GPL clearly explains
# that there is no warranty for this free software.  For both users' and
# authors' sake, the GPL requires that modified versions be marked as
# changed, so that their problems will not be attributed erroneously to
# authors of previous versions.
#
#   Some devices are designed to deny users access to install or run
# modified versions of the software inside them, although the manufacturer
# can do so.  This is fundamentally incompatible with the aim of
# protecting users' freedom to change the software.  The systematic
# pattern of such abuse occurs in the area of products for individuals to
# use, which is precisely where it is most unacceptable.  Therefore, we
# have designed this version of the GPL to prohibit the practice for those
# products.  If such problems arise substantially in other domains, we
# stand ready to extend this provision to those domains in future versions
# of the GPL, as needed to protect the freedom of users.
#
#   Finally, every program is threatened constantly by software patents.
# States should not allow patents to restrict development and use of
# software on general-purpose computers, but in those that do, we wish to
# avoid the special danger that patents applied to a free program could
# make it effectively proprietary.  To prevent this, the GPL assures that
# patents cannot be used to render the program non-free.

# Open Generation and Transmission Operation and Expansion Planning Model with RES and ESS (openTEPES) - Version 2.1.0 - March 13, 2021
# simplicity and transparency in power systems planning

# Developed by

#    Andres Ramos, Erik Alvarez, Sara Lumbreras
#    Instituto de Investigacion Tecnologica
#    Escuela Tecnica Superior de Ingenieria - ICAI
#    UNIVERSIDAD PONTIFICIA COMILLAS
#    Alberto Aguilera 23
#    28015 Madrid, Spain
#    Andres.Ramos@comillas.edu
#    Erik.Alvarez@comillas.edu
#    Sara.Lumbreras@comillas.edu
#    https://pascua.iit.comillas.edu/aramos/Ramos_CV.htm

#    with the very valuable collaboration from David Dominguez (david.dominguez@comillas.edu) and Alejandro Rodriguez (argallego@comillas.edu), our local Python gurus

#%% libraries

import time
import os
import setuptools

from   pyomo.environ import ConcreteModel, Set

from openTEPES.openTEPES_InputData        import InputData
from openTEPES.openTEPES_ModelFormulation import InvestmentModelFormulation, GenerationOperationModelFormulation, NetworkOperationModelFormulation
from openTEPES.openTEPES_ProblemSolving   import ProblemSolving
from openTEPES.openTEPES_OutputResults    import *


def openTEPES_run(DirName, CaseName, SolverName):

    InitialTime = time.time()
    _path = os.path.join(DirName, CaseName)

    #%% model declaration
    mTEPES = ConcreteModel('Open Generation and Transmission Operation and Expansion Planning Model with RES and ESS (openTEPES) - Version 2.1.0 - March 13, 2021')

    InputData(DirName, CaseName, mTEPES)

    # investment model objective function
    InvestmentModelFormulation(mTEPES)

    # iterative model formulation for each stage of a year
    for sc,p,st in mTEPES.sc*mTEPES.p*range(1,int(sum(mTEPES.pDuration.values())/mTEPES.pStageDuration+1)):
        # activate only scenario to formulate
        mTEPES.del_component(mTEPES.sc)
        mTEPES.sc = Set(initialize=mTEPES.scc, ordered=True, doc='scenarios'  , filter=lambda mTEPES,scc: scc in mTEPES.scc and sc == scc and mTEPES.pScenProb[scc] > 0.0)
        # activate only period to formulate
        mTEPES.del_component(mTEPES.p )
        mTEPES.p  = Set(initialize=mTEPES.pp , ordered=True, doc='periods'    , filter=lambda mTEPES,pp : pp  in p  == pp                                 )
        # activate only load levels of this stage
        mTEPES.del_component(mTEPES.n )
        mTEPES.del_component(mTEPES.n2)
        mTEPES.n  = Set(initialize=mTEPES.nn , ordered=True, doc='load levels', filter=lambda mTEPES,nn : nn  in list(mTEPES.pDuration) and mTEPES.nn.ord(nn) > (st-1)*mTEPES.pStageDuration and mTEPES.nn.ord(nn) <= st*mTEPES.pStageDuration)
        mTEPES.n2 = Set(initialize=mTEPES.nn , ordered=True, doc='load levels', filter=lambda mTEPES,nn : nn  in list(mTEPES.pDuration) and mTEPES.nn.ord(nn) > (st-1)*mTEPES.pStageDuration and mTEPES.nn.ord(nn) <= st*mTEPES.pStageDuration)

        # operation model objective function and constraints by stage
        GenerationOperationModelFormulation(mTEPES, st)
        NetworkOperationModelFormulation   (mTEPES, st)

    StartTime = time.time()
    mTEPES.write(_path+'/openTEPES_'+CaseName+'.lp', io_options={'symbolic_solver_labels': True})  # create lp-format file
    WritingLPFileTime = time.time() - StartTime
    StartTime         = time.time()
    print('Writing LP file                       ... ', round(WritingLPFileTime), 's')

    ProblemSolving(DirName, CaseName, SolverName, mTEPES)

    mTEPES.del_component(mTEPES.sc)
    mTEPES.del_component(mTEPES.p )
    mTEPES.del_component(mTEPES.n )
    mTEPES.sc = Set(initialize=mTEPES.scc, ordered=True, doc='scenarios'  , filter=lambda mTEPES,scc: scc in mTEPES.scc and mTEPES.pScenProb[scc] > 0.0)
    mTEPES.p  = Set(initialize=mTEPES.pp , ordered=True, doc='periods'                                                                                 )
    mTEPES.n  = Set(initialize=mTEPES.nn , ordered=True, doc='load levels', filter=lambda mTEPES,nn : nn  in list(mTEPES.pDuration)                    )

    InvestmentResults(DirName, CaseName, mTEPES)
    GenerationOperationResults(DirName, CaseName, mTEPES)
    ESSOperationResults(DirName, CaseName, mTEPES)
    FlexibilityResults(DirName, CaseName, mTEPES)
    NetworkOperationResults(DirName, CaseName, mTEPES)
    MarginalResults(DirName, CaseName, mTEPES)
    EconomicResults(DirName, CaseName, mTEPES)
    NetworkMapResults(DirName, CaseName, mTEPES)

    TotalTime = time.time() - InitialTime
    print('Total time                            ... ', round(TotalTime), 's')
