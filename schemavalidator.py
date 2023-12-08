import json
import jsonschema
from jsonschema import validate
import argparse
import os
from simError import SimError

def main():
    """ This program handles loading a kinetic model, and running it
 with the specified stimuli. The output is then compared with expected output to generate a model score.
    """
    parser = argparse.ArgumentParser( description = 'FindSim argument parser\n'
    'This program loads a kinetic model, and runs it with the \n'
    'specified stimuli. The output is then compared with expected output \n'
    'specified in the same file, to generate a model score.\n'
    )

    parser.add_argument( 'schema', type = str, help='Required: schema of experiment spec, in json format.')
    parser.add_argument( 'script', type = str, help='Required: filename of experiment spec, in json format.')
    
    args = parser.parse_args()
    jsonschemaValidator( args.schema,args.script)

def jsonschemaValidator( fschema,fname):
    '''
        1 Need to check TS,DR 'data' should be present and not ["paramdata","bardata"]
        2 Need to check BC 'bardata' should be present and not ["paramdata","data"]
        3 Need to check DP 'paramdata' should be present and not ["data","bardata"]
            
         A. TS can be presetTime,start,end,each,min,max 
         B. "DR" can be dose
         C. "BC" can be start,end,each,min,max 
         D. "DP" doesn't/can't have any default Readout's field nor normalization files, only paramdata 
     
    '''
    with open( fname ) as fd:
        findsim = json.load( fd )
        filename = fname
        if findsim["Experiment"]['design'] in ["TimeSeries","DoseResponse"]:
            if "data" not in findsim["Readouts"]:
                raise SimError("For TimeSeries and DoseResponse should have Readout->data")
            if "normalization" in findsim["Readouts"]:
                    if findsim["Experiment"]['design'] == "TimeSeries":
                        if findsim["Readouts"]["normalization"]["sampling"] not in ["presetTime","start","end","max","min","each"]:
                            raise SimError("TimeSeries->sampling should be one of these [\"presetTime\",\"start\",\"end\",\"max\",\"min\",\"each\"]")
                            
                    elif findsim["Experiment"]['design'] == "DoseResponse":
                        if findsim["Readouts"]["normalization"]["sampling"] not in ["dose"]:
                            raise SimError("DoseResponse->sampling should be one of these [\"dose\"]")
        elif findsim["Experiment"]['design'] in ["BarChart"]:
            if "bardata" not in findsim["Readouts"]:
                raise SimError("For BarChart should have Readout->bardata")
            if "normalization" in findsim["Readouts"]:
                if findsim["Readouts"]["normalization"]["sampling"] not in ["start","end","max","min","each"]:
                    raise SimError("TimeSeries->sampling should be one of these [\"start\",\"end\",\"max\",\"min\",\"each\"]")
        elif findsim["Experiment"]['design'] in ["DirectParameter"]:
            if "paramdata" not in findsim["Readouts"]:
                raise SimError("For DirectParameter should have Readout->paramdata")
            if "normalization" in findsim["Readouts"] or "timeUnits" in findsim["Readouts"] or "quantityUnits" in findsim["Readouts"] or "entities" in findsim["Readouts"] or "field" in findsim["Readouts"]:
                raise SimError("DirectParameter contains extra field")

    
        with open( fschema ) as _schema:
            schema = json.load( _schema )
            
            try:
                jsonschema.validate( findsim, schema )
                print(filename,"JSON data is valid.")
            except jsonschema.exceptions.ValidationError as e:
                print( "Failed to validate findSim file {}".format( fname ) )
                print(e.message)
                raise
if __name__ == '__main__':
    main()
