########################################################################################################################
## -- libraries and packages -- ########################################################################################
########################################################################################################################
import wfdb
import pooch
import requests
import pandas as pd
from importlib import resources

########################################################################################################################
## -- mimic iii waveform database data handler module -- ###############################################################
########################################################################################################################
class M3WaveFormMasterClass():
  def __init__(self) -> None:
    super(M3WaveFormMasterClass, self).__init__()
    with resources.open_text("physioprep.data", "patient_signals.csv") as file:
      patients_list_csv = pd.read_csv(file)

    self.args_preset = {
      "dat_cache_dir": pooch.os_cache('wfdb'),
      "physionet_url": "https://physionet.org/files/",
      "physionet_dir": "mimic3wdb-matched/1.0/",
      "patients_list": patients_list_csv,
    }

  ## -- get the list of patients from preset .csv or from physionet -- ##
  def get_patients(self, load_preset = True):
    if load_preset:
      patients_list = self.args_preset["patients_list"]
      patients_list = patients_list.apply(lambda r: f"{r['patient_group']}/{r['patient_id']}/", axis = 1).tolist()
      patients_list = set(patients_list)
    
    else:
      patients_url = self.args_preset["physionet_url"] + self.args_preset["physionet_dir"] + "RECORDS"
      patients_list = requests.get(patients_url).text.strip().split("\n")

    return list(patients_list)