import moose
import rdesigneur as rd
def load( scaleParam, chemFile ):
    rdes = rd.rdesigneur(
        turnOffElec = True,
        elecDt = 5e-5,
        chanProto = [['make_GABA()', 'gabaR']],
        chanDistrib = [
            ['gabaR', 'soma', 'Gbar', '1' ]],
        stimList = [['soma', '1','gabaR', 'periodicsyn', '50 * (t > 0.1)']],
    )
    return rdes

def build( rdes ):
    rdes.buildModel()
    #moose.le( '/model/elec/soma/gabaR/sh/synapse/synInput_rs' )
