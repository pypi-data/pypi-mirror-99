import os
import logging

from printStatus import printStatus

from gistPipeline.plotting import gistPlot_kin, gistPlot_lambdar, gistPlot_gas, gistPlot_sfh, gistPlot_ls



def generatePlots(config, module):

    outputPrefix = os.path.join(config['GENERAL']['OUTPUT'],config['GENERAL']['RUN_ID'])

    # - - - - - STELLAR KINEMATICS MODULE - - - - -
    if module == 'KIN':
        try:
            printStatus.running("Producing stellar kinematics maps")
            gistPlot_kin.plotMaps('KIN', config['GENERAL']['OUTPUT'])
            gistPlot_lambdar.plotMaps(config['GENERAL']['OUTPUT'])
            printStatus.updateDone("Producing stellar kinematics maps")
            logging.info("Produced stellar kinematics maps")
        except Exception as e:
            printStatus.updateFailed("Producing stellar kinematics maps")
            logging.error(e, exc_info=True)
            logging.error("Failed to produce stellar kinematics maps.")


    # - - - - - EMISSION LINES MODULE - - - - - 
    if module == 'GAS':
        try: 
            printStatus.running("Producing maps from the emission-line analysis")
            if os.path.isfile(outputPrefix+"_gas_BIN.fits") == True:
                gistPlot_gas.plotMaps(config['GENERAL']['OUTPUT'], 'BIN', True)
            if os.path.isfile(outputPrefix+"_gas_SPAXEL.fits") == True:
                gistPlot_gas.plotMaps(config['GENERAL']['OUTPUT'], 'SPAXEL', True)
            printStatus.updateDone("Producing maps from the emission-line analysis")
            logging.info("Producing maps from the emission-line analysis")
        except Exception as e:
            printStatus.updateFailed("Producing maps from the emission-line analysis")
            logging.error(e, exc_info=True)
            logging.error("Failed to produce maps from the emission-line analysis.")


    # - - - - - STAR FORMATION HISTORIES MODULE - - - - -
    if module == 'SFH':
        try:
            printStatus.running("Producing SFH maps")
            gistPlot_sfh.plotMaps('SFH', config['GENERAL']['OUTPUT'])
            printStatus.updateDone("Producing SFH maps")
            logging.info("Produced SFH maps")
        except Exception as e:
            printStatus.updateFailed("Producing SFH maps")
            logging.error(e, exc_info=True)
            logging.error("Failed to produce SFH maps.")


    # - - - - - LINE STRENGTHS MODULE - - - - -
    if module == 'LS':
        try:
            printStatus.running("Producing line strength maps")
            gistPlot_ls.plotMaps(config['GENERAL']['OUTPUT'], 'ORIGINAL')
            gistPlot_ls.plotMaps(config['GENERAL']['OUTPUT'], 'ADAPTED')
            if config['LS']['TYPE'] == 'SPP':
                gistPlot_sfh.plotMaps('LS', config['GENERAL']['OUTPUT'])
            printStatus.updateDone("Producing line strength maps")
            logging.info("Produced line strength maps")
        except Exception as e:
            printStatus.updateFailed("Producing line strength maps")
            logging.error(e, exc_info=True)
            logging.error("Failed to produce line strength maps.")


    # Return
    return(None)


