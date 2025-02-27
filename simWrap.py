# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA.
# 

'''
*******************************************************************
 * File:            simWrap.py
 * Description:     Base class for simulator interfaces for findSim
 * Author:          Upinder S. Bhalla
 * E-mail:          bhalla@ncbs.res.in
 ********************************************************************/
 '''
import json
#from simError import SimError
import numpy as np

if __package__ is None or __package__ == '':
    from simError import SimError

else:
    from FindSim.simError import SimError



class SimWrap():
    def __init__( self, *args, **kwargs ):
        self.ignoreMissingObj = kwargs["ignoreMissingObj"]
        self.silent = kwargs["silent"]
        self.exptFile = kwargs["exptFile"]
        self.modelLookup = {}
        self.runtime = 0.0
        self.loadtime = 0.0
        self.paramAccessTime = 0.0
        if "mapFile" in kwargs and len( kwargs["mapFile"] ) > 5:
            with open( kwargs["mapFile"] ) as fd:
                self.objMap = json.load( fd )
        self.modelId = ""
        self.plots = {} # Keys: Readout objects. Values: 2d numpy arrays
        self.upperLimit = {} # Key: field name . Value: upper limit
        self.lowerLimit = {} # Key: field name. Values: lower limit
                
        return

    def diagnostics( self, sim, expt, exptType ):
        if not expt:
            ex = []
            ey = []
        else:
            edata = np.array( expt )
            ex = edata[:,0]
            ey = edata[:,1]
        return { "runtime": self.runtime, 
                "loadtime": self.loadtime, 
                "paramAccessTime": self.paramAccessTime, 
                "exptType": exptType, 
                "sim": np.array( sim ),
                "exptX": ex,
                "exptY": ey
            }

    def lookup( self, key ):
        ret = self.modelLookup.get( key )
        if ret:
            return ret
        elif self.ignoreMissingObj:
            return []
        raise SimError( "SimWrap: failed modelLookup[{}]".format( key ) )

    def _scaleParams( self, params ):
        if len(params) == 0:
            return
        if (len(params) % 3) != 0:
            raise SimError( "scaleParam: expecting triplets of [obj, field, scale], got: '{}'".format( params ) )
        for i in range( 0, len(params), 3):
            self._scaleOneParam( params[i:i+3] )
            # _scaleOneParam is a derived function

    def getParamVec( self, params ):
        # Params is a list of strings of form obj.field
        # If param not found we put in a -1.
        ret = []
        for p in params:
            [ obj, field ] = p.split( '.' )
            ret.append( self.getObjParam( obj, field, isSilent=False ) )
        return ret

    def _scaleOneParam( self, params ): # place holder, to be overridden
        return

    def deleteItems( self, itemsToDelete ): # to be overridden
        return

    def subsetItems( self, modelSubset ): # to be overridden
        return

    def pruneDanglingObj( self, erSPlist ): # to be overridden
        return

    def loadModelFile( self, fname, modifyFunc, scaleParam, dumpFname, paramFname ): # to be overridden
        self.turnOffElec = True
        return

    def changeParams( self, params ):
        return

    def buildSolver( self, solver, useVclamp = False, minInterval = 1 ):
        return

    def buildVclamp( self, stim ):
        return

    def setHsolveState(self, state, pauseHsolve):
        return

    def makeReadoutPlots( self, readouts ):
        return

    def fillPlots( self ): # takes plots from sim and puts the numpy arrays of the plot values from sim into the return. Also returns dt as a float and numMainPlots
        return [], [1.0], 0
    
    def deliverStim( self, qe ):
        return

    def getCurrentTime( self ):
        return 0.0

    def advanceSimulation( self, advanceTime, doPlot = True, doSettle = False ):
        return

    def reinitSimulation( self ):
        return

    def sumFields( self, entityList, field ):
        return 0.0

    def getObjParam( self, entity, field ):
        return 0.0

    def steadyStateStims(self, stimList, responseList, isSeries = False, settleTime = 300 ):
        '''
        Computes steady_state output for specified stimulus combinatations.
        stimList is 2-D list of 
            (stimEntity, field, value, scale) tuples. 
        The first dimension is the combined stimulus for each data point
        The second dimension is the series of data points.
        responseList is list of 
            (respEntityList, field, refEntityList, field) 
        tuples for the readout. The respEntityList/refEntityList specify
        multiple entities whose values should be summed for the response.
        In some cases we have a special global reference stimulus. This
        is just another entry in the stimList.
        isSeries is true if the entries are successive, like a dose-response
        This function is used for a doser by having just the same
        stimulus entity throughout, for a series of doses.
        Returns the list of responses, and the list of matching references.
        '''
        return [], []
        
    def deleteSimulation( self ):
        return

    def presettle( self ):
        return {}

    def assignPresettle( settledict ):
        return

