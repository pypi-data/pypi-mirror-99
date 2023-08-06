from steam_nb_api.sing.ParametersCOSIM import ParametersCOSIM
from steam_nb_api.utils.misc import makeCopyFile
import datetime
import csv
import os
from pathlib import Path
import numpy as np
import yaml
import shutil
from steam_nb_api.ledet.ParameterSweep import *

def _read_yaml(type_str, elem_name):
    """
    Reads yaml file and returns it as dictionary
    :param type_str: type of file, e.g.: quench, coil, wire
    :param elem_name: file name, e.g. ColSol.1
    :return: dictionary for file named: type.name.yam
    """
    fullfileName = os.path.join(os.getcwd(), f"{type_str}.{elem_name}.yaml")
    with open(fullfileName, 'r') as stream:
        data = yaml.safe_load(stream)
    return data

class MP3_setup:
    def __init__(self, family, circuit, ParameterFile):
        # Folder and Executables
        self.path_PSPICELib = ''
        self.path_NotebookLib = ''
        self.PspiceExecutable = ''
        self.LedetExecutable = ''
        self.CosimExecutable = ''
        self.ModelFolder = ''
        self.ResultFolder = ''
        self.EOS_stub_C = ''

        self.ParameterFile = ParameterFile

        self.circuit = circuit
        self.transient = ''

        return

    def load_config(self, file):
        config_dict = _read_yaml('config', file)
        self.path_PSPICELib = config_dict['LibraryFolder']
        self.path_NotebookLib = config_dict['NotebookFolder']
        self.PspiceExecutable = config_dict['PSpiceExecutable']
        self.LedetExecutable = config_dict['LEDETExecutable']
        self.CosimExecutable = config_dict['COSIMExecutable']
        self.ModelFolder = config_dict['ModelFolder']
        self.ResultFolder = config_dict['ResultFolder']
        self.EOS_stub_C = config_dict['EOS_SynchronizationFolder']
        EOS_stub_EOS = os.environ['SWAN_HOME']
        self.ModelFolder_EOS = self.ModelFolder.replace(self.EOS_stub_C, EOS_stub_EOS)
        self.ModelFolder_EOS = self.ModelFolder_EOS.replace('\\','//')
        return

    def _loadParameterFile(self):
        with open(self.ParameterFile, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row_parameter = []
            values = []
            parameter_dict = {}

            line_count = 0
            for row in csv_reader:
                if line_count == 0: row_parameter = row
                if row[0] == self.circuit: values = row
                line_count = line_count + 1
            for i in range(1,len(row_parameter)):
                try:
                    parameter_dict[row_parameter[i]] = float(values[i])
                except:
                    parameter_dict[row_parameter[i]] = values[i]

        return parameter_dict

    def SetUpSimulation(self, transient, I00):
        self.transient = transient
        parameter_dict = self._loadParameterFile()
        parameter_dict['I00'] = I00

        Sim_Flag = parameter_dict['flag_COSIM']

        if Sim_Flag:
            COSIMfolder = self._setUp_COSIM()
        else:
            COSIMfolder = self._setUp_LEDETonly(parameter_dict)
            newModelCosim = ParametersCOSIM('')
            newModelCosim.writeCOSIMBatch(COSIMfolder, self.CosimExecutable, Destination=os.path.join(self.ModelFolder_EOS, os.pardir), LEDET_exe=self.LedetExecutable)

    def _setUp_COSIM(self):
        # 1. Obtain existing cir file
        # 2. Obtain parameter to change
        # 3. link parameter to parameter list
        # 4. Change .cir file
        # 5. include EE&options& chain of magnets etc.
        # 6. Generate Stimuli file
        # 7. Generate Input/Output etc.
        # ....
        return

    def __generateStimuliLEDET(self, parameter_dict):
        if self.transient == 'FPA':
            current_level = parameter_dict['I00']
            t_PC = parameter_dict['t_PC']
            t_Start = parameter_dict['t_Start']

            I_LUT = [current_level, current_level, 0]
            t_LUT = [t_Start, t_PC, t_PC+0.01]

            parameter_dict["I_PC_LUT"] = I_LUT
            parameter_dict["t_PC_LUT"] = t_LUT
        else:
            print(self.transient+' is not supported yet. Abort!')
        return parameter_dict

    def _setUp_LEDETonly(self, parameter_dict):
        current_level = parameter_dict['I00']
        MagnetName = parameter_dict['MagnetName']

        ModelFolder_EOS = os.path.join(self.ModelFolder_EOS, 'LEDET_model_' + self.circuit + "_" + self.transient + "_" +
                                            str(current_level) + "A")

        ModelFolder_C = self.ModelFolder + 'LEDET_model_' + self.circuit + "_" + self.transient + "_" + str(current_level) + "A"
        COSIMfolder = str(MagnetName) + '_L_' + ModelFolder_C
        newModelCosim = ParametersCOSIM(ModelFolder_EOS, nameMagnet=MagnetName, nameCircuit=self.circuit)
        newModelCosim.makeAllFolders(N_LEDET=1, LEDET_only=1)
        LEDETfiles = newModelCosim.copyCOSIMfiles('0', '0', MagnetName, N_LEDET=1, LEDET_only=1)
        nameFileLEDET = os.path.join(ModelFolder_EOS, "LEDET", "LEDET", MagnetName, "Input", MagnetName + "_0.xlsx")

        parameter_dict = self.__generateStimuliLEDET(parameter_dict)
        if not "flag_saveMatFile" in parameter_dict.keys():
            parameter_dict["flag_saveMatFile"] = 1
        if not "flag_generateReport" in parameter_dict.keys():
            parameter_dict["flag_generateReport"] = 1
        self._manipulateLEDETExcel(nameFileLEDET, parameter_dict)

        # Display time stamp and end run
        currentDT = datetime.datetime.now()
        print(' ')
        print(self.circuit + ' LEDET magnet model generated.')
        print('Time stamp: ' + str(currentDT))
        return COSIMfolder

    def __generateImitate(self, PL, classvalue, value):
        if type(classvalue) == np.ndarray and len(classvalue) > 1:
            v = deepcopy(classvalue)
            v = np.where(PL.Inputs.polarities_inGroup != 0, value, v)
        elif type(classvalue) == np.ndarray:
            v = np.array([value])
        else:
            v = value
        return v

    def _manipulateLEDETExcel(self, file, parameter_dict):
        PL = ParametersLEDET()
        PL.readLEDETExcel(file)
        nHalfTurnsDefined = len(PL.getAttribute("Inputs", "HalfTurnToInductanceBlock"))

        for key in parameter_dict.keys():
            if key in PL.Inputs.__annotations__:
                if not isinstance(parameter_dict[key], list):
                    values = self.__generateImitate(PL, PL.getAttribute(getattr(PL, 'Inputs'), key), parameter_dict[key])
                elif len(parameter_dict[key])==1:
                    values = self.__generateImitate(PL, PL.getAttribute(getattr(PL, 'Inputs'), key), parameter_dict[key])
                else: values = parameter_dict[key]
                PL.setAttribute('Inputs', key, values)
            if key in PL.Options.__annotations__:
                PL.setAttribute("Options", key, parameter_dict[key])

        if parameter_dict['Quench']:
            i_qT = int(parameter_dict['i_qT'])
            t_Q = parameter_dict['t_Q']
            tStartQuench = [9999] * nHalfTurnsDefined
            tStartQuench[i_qT - 1] = t_Q
        else:
            tStartQuench = [9999] * nHalfTurnsDefined
        PL.setAttribute("Inputs", "tStartQuench", tStartQuench)

        PL.writeFileLEDET(file)
