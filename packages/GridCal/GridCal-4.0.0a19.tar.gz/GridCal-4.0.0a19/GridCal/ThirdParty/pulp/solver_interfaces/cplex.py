# PuLP : Python LP Modeler
# Version 1.4.2

# Copyright (c) 2002-2005, Jean-Sebastien Roy (js@jeannot.org)
# Modifications Copyright (c) 2007- Stuart Anthony Mitchell (s.mitchell@auckland.ac.nz)
# $Id:solvers.py 1791 2008-04-23 22:54:34Z smit023 $

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

from GridCal.ThirdParty.pulp.solvers import *


class CPLEX_CMD(LpSolver_CMD):
    """The CPLEX LP solver"""

    def __init__(self, path = None, keepFiles = 0, mip = 1,
            msg = 0, options = [], timelimit = None):
        LpSolver_CMD.__init__(self, path, keepFiles, mip, msg, options)
        self.timelimit = timelimit

    def defaultPath(self):
        return self.executableExtension("cplex")

    def available(self):
        """True if the solver is available"""
        return self.executable(self.path)

    def actualSolve(self, lp):
        """Solve a well formulated lp problem"""
        if not self.executable(self.path):
            raise PulpSolverError("PuLP: cannot execute "+self.path)
        if not self.keepFiles:
            uuid = uuid4().hex
            tmpLp = os.path.join(self.tmpDir, "%s-pulp.lp" % uuid)
            tmpSol = os.path.join(self.tmpDir, "%s-pulp.sol" % uuid)
        else:
            tmpLp = lp.name+"-pulp.lp"
            tmpSol = lp.name+"-pulp.sol"
        lp.writeLP(tmpLp, writeSOS = 1)
        try: os.remove(tmpSol)
        except: pass
        if not self.msg:
            cplex = subprocess.Popen(self.path, stdin = subprocess.PIPE,
                stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        else:
            cplex = subprocess.Popen(self.path, stdin = subprocess.PIPE)
        cplex_cmds = "read "+tmpLp+"\n"
        if self.timelimit is not None:
            cplex_cmds += "set timelimit " + str(self.timelimit) + "\n"
        for option in self.options:
            cplex_cmds += option+"\n"
        if lp.isMIP():
            if self.mip:
                cplex_cmds += "mipopt\n"
                cplex_cmds += "change problem fixed\n"
            else:
                cplex_cmds += "change problem lp\n"

        cplex_cmds += "optimize\n"
        cplex_cmds += "write "+tmpSol+"\n"
        cplex_cmds += "quit\n"
        cplex_cmds = cplex_cmds.encode('UTF-8')
        cplex.communicate(cplex_cmds)
        if cplex.returncode != 0:
            raise PulpSolverError("PuLP: Error while trying to execute "+self.path)
        if not self.keepFiles:
            try: os.remove(tmpLp)
            except: pass
        if not os.path.exists(tmpSol):
            status = LpStatusInfeasible
        else:
            status, values, reducedCosts, shadowPrices, slacks = self.readsol(tmpSol)
        if not self.keepFiles:
            try: os.remove(tmpSol)
            except: pass
            try: os.remove("cplex.log")
            except: pass
        if status != LpStatusInfeasible:
            lp.assignVarsVals(values)
            lp.assignVarsDj(reducedCosts)
            lp.assignConsPi(shadowPrices)
            lp.assignConsSlack(slacks)
        lp.status = status
        return status

    def readsol(self,filename):
        """Read a CPLEX solution file"""
        try:
            import xml.etree.ElementTree as et
        except ImportError:
            import elementtree.ElementTree as et
        solutionXML = et.parse(filename).getroot()
        solutionheader = solutionXML.find("header")
        statusString = solutionheader.get("solutionStatusString")
        cplexStatus = {
            "optimal":LpStatusOptimal,
            }
        if statusString not in cplexStatus:
            raise PulpSolverError("Unknown status returned by CPLEX: "+statusString)
        status = cplexStatus[statusString]

        shadowPrices = {}
        slacks = {}
        shadowPrices = {}
        slacks = {}
        constraints = solutionXML.find("linearConstraints")
        for constraint in constraints:
                name = constraint.get("name")
                shadowPrice = constraint.get("dual")
                slack = constraint.get("slack")
                shadowPrices[name] = float(shadowPrice)
                slacks[name] = float(slack)

        values = {}
        reducedCosts = {}
        for variable in solutionXML.find("variables"):
                name = variable.get("name")
                value = variable.get("value")
                reducedCost = variable.get("reducedCost")
                values[name] = float(value)
                reducedCosts[name] = float(reducedCost)

        return status, values, reducedCosts, shadowPrices, slacks

def CPLEX_DLL_load_dll(path):
    """
    function that loads the DLL useful for debugging installation problems
    """
    import ctypes
    if os.name in ['nt','dos']:
        lib = ctypes.windll.LoadLibrary(str(path))
    else:
        lib = ctypes.cdll.LoadLibrary(str(path))
    return lib

try:

    import ctypes


    class CPLEX_DLL(LpSolver):
        """
        The CPLEX LP/MIP solver (via a Dynamic library DLL - windows or SO - Linux)

        This solver wraps the c library api of cplex.
        It has been tested against cplex 11.
        For api functions that have not been wrapped in this solver please use
        the ctypes library interface to the cplex api in CPLEX_DLL.lib
        """
        lib = CPLEX_DLL_load_dll(cplex_dll_path)
        # parameters manually found in solver manual
        CPX_PARAM_EPGAP = 2009
        CPX_PARAM_MEMORYEMPHASIS = 1082 # from Cplex 11.0 manual
        CPX_PARAM_TILIM = 1039
        CPX_PARAM_LPMETHOD = 1062
        # argtypes for CPLEX functions
        lib.CPXsetintparam.argtypes = [ctypes.c_void_p,
                         ctypes.c_int, ctypes.c_int]
        lib.CPXsetdblparam.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                                ctypes.c_double]
        lib.CPXfopen.argtypes = [ctypes.c_char_p,
                                      ctypes.c_char_p]
        lib.CPXfopen.restype = ctypes.c_void_p
        lib.CPXsetlogfile.argtypes = [ctypes.c_void_p,
                                      ctypes.c_void_p]

        def __init__(self, mip=True, msg=True, timeLimit=None, epgap=None, logfilename=None, emphasizeMemory=False):
            """
            Initializes the CPLEX_DLL solver.

            @param mip: if False the solver will solve a MIP as an LP
            @param msg: displays information from the solver to stdout
            @param epgap: sets the integer bound gap
            @param logfilename: sets the filename of the cplex logfile
            @param emphasizeMemory: makes the solver emphasize Memory over
              solution time
            """
            LpSolver.__init__(self, mip, msg)

            self.timeLimit = timeLimit

            self.grabLicence()

            self.setMemoryEmphasis(emphasizeMemory)

            self.logfilep = None

            if epgap is not None:
                self.changeEpgap(epgap)
            if timeLimit is not None:
                self.setTimeLimit(timeLimit)
            if logfilename is not None:
                self.setlogfile(logfilename)
            else:
                self.logfile = None

        def setlogfile(self, filename):
            """
            sets the logfile for cplex output
            """
            self.logfilep = CPLEX_DLL.lib.CPXfopen(filename, "w")
            CPLEX_DLL.lib.CPXsetlogfile(self.env, self.logfilep)

        def changeEpgap(self, epgap=1e-4):
            """
            Change cplex solver integer bound gap tolerence
            """
            CPLEX_DLL.lib.CPXsetdblparam(self.env, CPLEX_DLL.CPX_PARAM_EPGAP, epgap)

        def setLpAlgorithm(self, algo):
            """
            Select the LP algorithm to use.

            See your CPLEX manual for valid values of algo.  For CPLEX
            12.1 these are 0 for "automatic", 1 primal, 2 dual, 3 network, 4
            barrier, 5 sifting and 6 concurrent.  Currently the default setting
            0 always choooses dual simplex.
            """
            CPLEX_DLL.lib.CPXsetintparam(self.env, CPLEX_DLL.CPX_PARAM_LPMETHOD, algo)

        def setTimeLimit(self, timeLimit=0.0):
            """
            Make cplex limit the time it takes --added CBM 8/28/09
            """
            CPLEX_DLL.lib.CPXsetdblparam(self.env, CPLEX_DLL.CPX_PARAM_TILIM, float(timeLimit))

        def setMemoryEmphasis(self, yesOrNo = False):
            """
            Make cplex try to conserve memory at the expense of
            performance.
            """
            CPLEX_DLL.lib.CPXsetintparam(self.env, CPLEX_DLL.CPX_PARAM_MEMORYEMPHASIS, yesOrNo)

        def findSolutionValues(self, lp, numcols, numrows):
            """

            :param lp:
            :param numcols:
            :param numrows:
            :return:
            """
            byref = ctypes.byref
            solutionStatus = ctypes.c_int()
            objectiveValue = ctypes.c_double()
            x = (ctypes.c_double * numcols)()
            pi = (ctypes.c_double * numrows)()
            slack = (ctypes.c_double * numrows)()
            dj = (ctypes.c_double * numcols)()

            status= CPLEX_DLL.lib.CPXsolwrite(self.env, self.hprob, "CplexTest.sol")

            if lp.isMIP():

                solutionStatus.value = CPLEX_DLL.lib.CPXgetstat(self.env, self.hprob)

                status = CPLEX_DLL.lib.CPXgetobjval(self.env, self.hprob, byref(objectiveValue))

                if status != 0 and status != 1217:  # no solution exists
                    raise PulpSolverError("Error in CPXgetobjval status=" + str(status))

                status = CPLEX_DLL.lib.CPXgetx(self.env, self.hprob, byref(x), 0, numcols - 1)

                if status != 0 and status != 1217:
                    raise PulpSolverError("Error in CPXgetx status=" + str(status))
            else:
                status = CPLEX_DLL.lib.CPXsolution(self.env, self.hprob,
                                                   byref(solutionStatus),
                                                   byref(objectiveValue),
                                                   byref(x), byref(pi),
                                                   byref(slack), byref(dj))
            # 102 is the cplex return status for
            # integer optimal within tolerance
            # and is useful for breaking symmetry.
            CplexLpStatus = {1: LpStatusOptimal,
                             3: LpStatusInfeasible,
                             2: LpStatusUnbounded,
                             0: LpStatusNotSolved,
                             101: LpStatusOptimal,
                             102: LpStatusOptimal,
                             103: LpStatusInfeasible}

            # populate pulp solution values
            variablevalues = {}
            variabledjvalues = {}
            constraintpivalues = {}
            constraintslackvalues = {}
            for i in range(numcols):
                variablevalues[self.n2v[i].name] = x[i]
                variabledjvalues[self.n2v[i].name] = dj[i]

            lp.assignVarsVals(variablevalues)
            lp.assignVarsDj(variabledjvalues)

            # put pi and slack variables against the constraints
            for i in range(numrows):
                constraintpivalues[self.n2c[i]] = pi[i]
                constraintslackvalues[self.n2c[i]] = slack[i]
            lp.assignConsPi(constraintpivalues)
            lp.assignConsSlack(constraintslackvalues)

            # TODO: clear up the name of self.n2c
            if self.msg:
                print("Cplex status=", solutionStatus.value)

            lp.resolveOK = True
            for var in lp.variables():
                var.isModified = False

            lp.status = CplexLpStatus.get(solutionStatus.value, LpStatusUndefined)

            return lp.status

        def __del__(self):
            # LpSolver.__del__(self)
            self.releaseLicence()

        def available(self):
            """True if the solver is available"""
            return True

        def grabLicence(self):
            """
            Returns True if a CPLEX licence can be obtained.
            The licence is kept until releaseLicence() is called.
            """
            status = ctypes.c_int()
            # If the config file allows to do so (non null params), try to
            # grab a runtime license.
            if ilm_cplex_license and ilm_cplex_license_signature:
                runtime_status = CPLEX_DLL.lib.CPXsetstaringsol(
                        ilm_cplex_license,
                        ilm_cplex_license_signature)
                # if runtime_status is not zero, running with a runtime
                # license will fail. However, no error is thrown (yet)
                # because the second call might still succeed if the user
                # has another license. Let us forgive bad user
                # configuration:
                if not (runtime_status == 0) and self.msg:
                    print("CPLEX library failed to load the runtime license" +
                          "the call returned status=%s" % str(runtime_status) +
                          "Please check the pulp config file.")

            self.env = CPLEX_DLL.lib.CPXopenCPLEX(ctypes.byref(status))

            self.hprob = None

            if not(status.value == 0):
                raise PulpSolverError("CPLEX library failed on CPXopenCPLEX status=" + str(status))

        def releaseLicence(self):
            """Release a previously obtained CPLEX licence"""
            if getattr(self,"env",False):
                status=CPLEX_DLL.lib.CPXcloseCPLEX(self.env)
                self.env = self.hprob = None
            else:
                raise PulpSolverError("No CPLEX enviroment to close")

        def callSolver(self, isMIP):
            """Solves the problem with cplex
            """
            #solve the problem
            self.cplexTime = -clock()
            if isMIP and self.mip:
                status= CPLEX_DLL.lib.CPXmipopt(self.env, self.hprob)
                if status != 0:
                    raise PulpSolverError("Error in CPXmipopt status="
                                        + str(status))
            else:
                status = CPLEX_DLL.lib.CPXlpopt(self.env, self.hprob)
                if status != 0:
                    raise PulpSolverError("Error in CPXlpopt status="
                                            + str(status))
            self.cplexTime += clock()

        def actualSolve(self, lp):
            """Solve a well formulated lp problem"""
            #TODO alter so that msg parameter is handled correctly
            status = ctypes.c_int()
            byref = ctypes.byref   #shortcut to function
            if self.hprob is not None:
                CPLEX_DLL.lib.CPXfreeprob(self.env, self.hprob)
            self.hprob = CPLEX_DLL.lib.CPXcreateprob(self.env,
                                                    byref(status), lp.name)
            if status.value != 0:
                raise PulpSolverError("Error in CPXcreateprob status="
                                    + str(status))
            (numcols, numrows, numels, rangeCount,
                objSense, obj, objconst,
                rhs, rangeValues, rowSense, matbeg, matcnt, matind,
                matval, lb, ub, initValues, colname,
                rowname, xctype, n2v, n2c )= self.getCplexStyleArrays(lp)
            status.value = CPLEX_DLL.lib.CPXcopylpwnames (self.env, self.hprob,
                                 numcols, numrows,
                                 objSense, obj, rhs, rowSense, matbeg, matcnt,
                                 matind, matval, lb, ub, None, colname, rowname)
            if status.value != 0:
                raise PulpSolverError("Error in CPXcopylpwnames status=" +
                                        str(status))
            if lp.isMIP() and self.mip:
                status.value = CPLEX_DLL.lib.CPXcopyctype(self.env,
                                                          self.hprob,
                                                          xctype)
            if status.value != 0:
                raise PulpSolverError("Error in CPXcopyctype status=" +
                                        str(status))
            #set the initial solution
            self.callSolver(lp.isMIP())
            #get the solution information
            solutionStatus = self.findSolutionValues(lp, numcols, numrows)
            for var in lp.variables():
                var.modified = False
            return solutionStatus


        def actualResolve(self,lp):
            """looks at which variables have been modified and changes them
            """
            #TODO: Add changing variables not just adding them
            #TODO: look at constraints
            modifiedVars = [var for var in lp.variables() if var.modified]
            #assumes that all variables flagged as modified
            #need to be added to the problem
            newVars = modifiedVars
            #print newVars
            self.v2n.update([(var, i+self.addedVars)
                                for i,var in enumerate(newVars)])
            self.n2v.update([(i+self.addedVars, var)
                                for i,var in enumerate(newVars)])
            self.vname2n.update([(var.name, i+self.addedVars)
                                for i,var in enumerate(newVars)])
            oldVars = self.addedVars
            self.addedVars += len(newVars)
            (ccnt,nzcnt,obj,cmatbeg,
            cmatlen, cmatind,cmatval,
            lb,ub, initvals,
            colname, coltype) = self.getSparseCols(newVars, lp, oldVars,
                                defBound = 1e20)
            CPXaddcolsStatus = CPLEX_DLL.lib.CPXaddcols(self.env, self.hprob,
                                          ccnt, nzcnt,
                                          obj,cmatbeg,
                                          cmatind,cmatval,
                                          lb,ub,colname)
            #add the column types
            if lp.isMIP() and self.mip:
                indices = (ctypes.c_int * len(newVars))()
                for i,var in enumerate(newVars):
                    indices[i] = oldVars +i
                CPXchgctypeStatus = CPLEX_DLL.lib.CPXchgctype (self.env,
                                                 self.hprob,
                                                 ccnt, indices, coltype);
            #solve the problem
            self.callSolver(lp.isMIP())
            #get the solution information
            solutionStatus = self.findSolutionValues(lp, self.addedVars,
                                                     self.addedRows)
            for var in modifiedVars:
                var.modified = False
            return solutionStatus

        def getSparseCols(self, vars, lp, offset = 0, defBound = 1e20):
            """
            outputs the variables in var as a sparse matrix,
            suitable for cplex and Coin

            Copyright (c) Stuart Mitchell 2007
            """
            numVars = len(vars)
            obj = (ctypes.c_double * numVars)()
            cmatbeg = (ctypes.c_int * numVars)()
            mycmatind = []
            mycmatval = []
            rangeCount = 0
            #values for variables
            colNames =  (ctypes.c_char_p * numVars)()
            lowerBounds =  (ctypes.c_double * numVars)()
            upperBounds =  (ctypes.c_double * numVars)()
            initValues =  (ctypes.c_double * numVars)()
            i=0
            for v in vars:
                colNames[i] = str(v.name)
                initValues[i] = v.init
                if v.lowBound != None:
                    lowerBounds[i] = v.lowBound
                else:
                    lowerBounds[i] = -defBound
                if v.upBound != None:
                    upperBounds[i] = v.upBound
                else:
                    upperBounds[i] = defBound
                i+= 1
                #create the new variables
            #values for constraints
            #return the coefficient matrix as a series of vectors
            myobjectCoeffs = {}
            numRows = len(lp.constraints)
            sparseMatrix = sparse.Matrix(list(range(numRows)), list(range(numVars)))
            for var in vars:
                for row,coeff in var.expression.items():
                   if row.name == lp.objective.name:
                        myobjectCoeffs[var] = coeff
                   else:
                        sparseMatrix.add(self.c2n[row.name], self.v2n[var] - offset, coeff)
            #objective values
            objectCoeffs = (ctypes.c_double * numVars)()
            for var in vars:
                objectCoeffs[self.v2n[var]-offset] = myobjectCoeffs[var]
            (numels, mystartsBase, mylenBase, myindBase,
             myelemBase) = sparseMatrix.col_based_arrays()
            elemBase = ctypesArrayFill(myelemBase, ctypes.c_double)
            indBase = ctypesArrayFill(myindBase, ctypes.c_int)
            startsBase = ctypesArrayFill(mystartsBase, ctypes.c_int)
            lenBase = ctypesArrayFill(mylenBase, ctypes.c_int)
            #MIP Variables
            NumVarCharArray = ctypes.c_char * numVars
            columnType = NumVarCharArray()
            if lp.isMIP():
                CplexLpCategories = {LpContinuous: "C",
                                    LpInteger: "I"}
                for v in vars:
                    columnType[self.v2n[v] - offset] = CplexLpCategories[v.cat]
            return  numVars, numels,  objectCoeffs, \
                startsBase, lenBase, indBase, \
                elemBase, lowerBounds, upperBounds, initValues, colNames, \
                columnType

        def objSa(self, vars = None):
            """Objective coefficient sensitivity analysis.

            Called after a problem has been solved, this function
            returns a dict mapping variables to pairs (lo, hi) indicating
            that the objective coefficient of the variable can vary
            between lo and hi without changing the optimal basis
            (if other coefficients remain constant).  If an iterable
            vars is given, results are returned only for variables in vars.
            """
            if vars is None:
                v2n = self.v2n
            else:
                v2n = dict((v, self.v2n[v]) for v in vars)
            ifirst = min(v2n.values())
            ilast = max(v2n.values())

            row_t = ctypes.c_double * (ilast - ifirst + 1)
            lo = row_t()
            hi = row_t()
            status = ctypes.c_int()
            status.value = CPLEX_DLL.lib.CPXobjsa(self.env, self.hprob,
                                                  ifirst, ilast, lo, hi)
            if status.value != 0:
                raise PulpSolverError("Error in CPXobjsa, status="
                                        + str(status))
            return dict((v, (lo[i - ifirst], hi[i - ifirst]))
                        for v, i in v2n.items())


    CPLEX = CPLEX_DLL

except (ImportError, OSError):

    class CPLEX_DLL(LpSolver):
        """
        The CPLEX LP/MIP solver PHANTOM Something went wrong!!!!
        """
        def available(self):
            """
            True if the solver is available
            """
            return False

        def actualSolve(self, lp):
            """
            Solve a well formulated lp problem
            """
            raise PulpSolverError("CPLEX_DLL: Not Available")

    CPLEX = CPLEX_CMD


try:
    import cplex

except ImportError:

    class CPLEX_PY(LpSolver):

        """
        The CPLEX LP/MIP solver from python PHANTOM Something went wrong!!!!
        """
        def available(self):
            """
            True if the solver is available
            """
            return False

        def actualSolve(self, lp):
            """
            Solve a well formulated lp problem
            """
            raise PulpSolverError("CPLEX_PY: Not Available")
else:
    class CPLEX_PY(LpSolver):
        """
        The CPLEX LP/MIP solver (via a Python Binding)

        This solver wraps the python api of cplex.
        It has been tested against cplex 12.3.
        For api functions that have not been wrapped in this solver please use
        the base cplex classes
        """

        def __init__(self, mip=True, msg=True, timeLimit=None, epgap=None, logfilename=None):
            """
            Initializes the CPLEX_PY solver.

            @param mip: if False the solver will solve a MIP as an LP
            @param msg: displays information from the solver to stdout
            @param epgap: sets the integer bound gap
            @param logfilename: sets the filename of the cplex logfile
            """
            LpSolver.__init__(self, mip, msg)
            self.timeLimit = timeLimit
            self.epgap = epgap
            self.logfilename = logfilename

        def available(self):
            """True if the solver is available"""
            return True

        def actualSolve(self, lp, callback = None):
            """
            Solve a well formulated lp problem

            creates a cplex model, variables and constraints and attaches
            them to the lp model which it then solves
            """
            self.buildSolverModel(lp)

            # set the initial solution
            log.debug("Solve the Model using cplex")
            self.callSolver(lp)

            # get the solution information
            solution_status = self.findSolutionValues(lp)

            for var in lp.variables():
                var.modified = False

            for constraint in lp.constraints.values():
                constraint.modified = False

            return solution_status

        def buildSolverModel(self, lp):
            """
            Takes the pulp lp model and translates it into a cplex model
            """
            self.n2v = dict((var.name, var) for var in lp.variables())
            if len(self.n2v) != len(lp.variables()):
                raise PulpSolverError(
                        'Variables must have unique names for cplex solver')
            log.debug("create the cplex model")
            self.solverModel = lp.solverModel = cplex.Cplex()
            log.debug("set the name of the problem")
            if not self.mip:
                self.solverModel.set_problem_name(lp.name)
            log.debug("set the sense of the problem")
            if lp.sense == LpMaximize:
                lp.solverModel.objective.set_sense(
                                    lp.solverModel.objective.sense.maximize)
            obj = [float(lp.objective.get(var, 0.0)) for var in lp.variables()]
            def cplex_var_lb(var):
                if var.lowBound is not None:
                    return float(var.lowBound)
                else:
                    return -cplex.infinity
            lb = [cplex_var_lb(var) for var in lp.variables()]
            def cplex_var_ub(var):
                if var.upBound is not None:
                    return float(var.upBound)
                else:
                    return cplex.infinity
            ub = [cplex_var_ub(var) for var in lp.variables()]
            colnames = [var.name for var in lp.variables()]
            def cplex_var_types(var):
                if var.cat == LpInteger:
                    return 'I'
                else:
                    return 'C'
            ctype = [cplex_var_types(var) for var in lp.variables()]
            ctype = "".join(ctype)
            lp.solverModel.variables.add(obj=obj, lb=lb, ub=ub, types=ctype,
                       names=colnames)
            rows = []
            senses = []
            rhs = []
            rownames = []
            for name,constraint in lp.constraints.items():
                #build the expression
                expr = [(var.name, float(coeff)) for var, coeff in constraint.items()]
                if not expr:
                    #if the constraint is empty
                    rows.append(([],[]))
                else:
                    rows.append(list(zip(*expr)))
                if constraint.sense == LpConstraintLE:
                    senses.append('L')
                elif constraint.sense == LpConstraintGE:
                    senses.append('G')
                elif constraint.sense == LpConstraintEQ:
                    senses.append('E')
                else:
                    raise PulpSolverError('Detected an invalid constraint type')
                rownames.append(name)
                rhs.append(float(-constraint.constant))
            lp.solverModel.linear_constraints.add(lin_expr=rows, senses=senses,
                                rhs=rhs, names=rownames)
            log.debug("set the type of the problem")
            if not self.mip:
                self.solverModel.set_problem_type(cplex.Cplex.problem_type.LP)
            log.debug("set the logging")
            if not self.msg:
                self.solverModel.set_error_stream(None)
                self.solverModel.set_log_stream(None)
                self.solverModel.set_warning_stream(None)
                self.solverModel.set_results_stream(None)
            if self.logfilename is not None:
                self.setlogfile(self.logfilename)
            if self.epgap is not None:
                self.changeEpgap(self.epgap)
            if self.timeLimit is not None:
                self.setTimeLimit(self.timeLimit)

        def setlogfile(self, filename):
            """
            sets the logfile for cplex output
            """
            self.solverModel.set_log_stream(filename)

        def changeEpgap(self, epgap = 10**-4):
            """
            Change cplex solver integer bound gap tolerence
            """
            self.solverModel.parameters.mip.tolerances.mipgap.set(epgap)

        def setTimeLimit(self, timeLimit = 0.0):
            """
            Make cplex limit the time it takes --added CBM 8/28/09
            """
            self.solverModel.parameters.timelimit.set(timeLimit)

        def callSolver(self, isMIP):
            """Solves the problem with cplex
            """
            #solve the problem
            self.solveTime = -clock()
            self.solverModel.solve()
            self.solveTime += clock()

        def findSolutionValues(self, lp):
            CplexLpStatus = {lp.solverModel.solution.status.MIP_optimal: LpStatusOptimal,
                             lp.solverModel.solution.status.optimal: LpStatusOptimal,
                             lp.solverModel.solution.status.optimal_tolerance: LpStatusOptimal,
                             lp.solverModel.solution.status.infeasible: LpStatusInfeasible,
                             lp.solverModel.solution.status.infeasible_or_unbounded:  LpStatusInfeasible,
                             lp.solverModel.solution.status.MIP_infeasible: LpStatusInfeasible,
                             lp.solverModel.solution.status.MIP_infeasible_or_unbounded:  LpStatusInfeasible,
                             lp.solverModel.solution.status.unbounded: LpStatusUnbounded,
                             lp.solverModel.solution.status.MIP_unbounded: LpStatusUnbounded,
                             lp.solverModel.solution.status.abort_dual_obj_limit: LpStatusNotSolved,
                             lp.solverModel.solution.status.abort_iteration_limit: LpStatusNotSolved,
                             lp.solverModel.solution.status.abort_obj_limit: LpStatusNotSolved,
                             lp.solverModel.solution.status.abort_relaxed: LpStatusNotSolved,
                             lp.solverModel.solution.status.abort_time_limit: LpStatusNotSolved,
                             lp.solverModel.solution.status.abort_user: LpStatusNotSolved}
            lp.cplex_status = lp.solverModel.solution.get_status()
            lp.status = CplexLpStatus.get(lp.cplex_status, LpStatusUndefined)
            var_names = [var.name for var in lp.variables()]
            con_names = [con for con in lp.constraints]
            try:
                objectiveValue = lp.solverModel.solution.get_objective_value()
                variablevalues = dict(zip(var_names, lp.solverModel.solution.get_values(var_names)))
                lp.assignVarsVals(variablevalues)
                constraintslackvalues = dict(zip(con_names, lp.solverModel.solution.get_linear_slacks(con_names)))
                lp.assignConsSlack(constraintslackvalues)
                if lp.solverModel.get_problem_type == cplex.Cplex.problem_type.LP:
                    variabledjvalues = dict(zip(var_names, lp.solverModel.solution.get_reduced_costs(var_names)))
                    lp.assignVarsDj(variabledjvalues)
                    constraintpivalues = dict(zip(con_names, lp.solverModel.solution.get_dual_values(con_names)))
                    lp.assignConsPi(constraintpivalues)
            except cplex.exceptions.CplexSolverError:
                #raises this error when there is no solution
                pass
            #put pi and slack variables against the constraints
            #TODO: clear up the name of self.n2c
            if self.msg:
                print("Cplex status=", lp.cplex_status)
            lp.resolveOK = True
            for var in lp.variables():
                var.isModified = False
            return lp.status

        def actualResolve(self,lp):
            """
            looks at which variables have been modified and changes them
            """
            raise NotImplementedError("Resolves in CPLEX_PY not yet implemented")

    CPLEX = CPLEX_PY

