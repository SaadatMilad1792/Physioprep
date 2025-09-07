########################################################################################################################
## -- libraries and packages -- ########################################################################################
########################################################################################################################
import re
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
    with resources.open_binary("physioprep.data", "patient_signals.pkl") as file:
      patients_list_csv = pd.read_pickle(file)

    self.args_preset = {
      "dat_cache_dir": pooch.os_cache('wfdb'),
      "physionet_url": "https://physionet.org/files/",
      "physionet_dir": "mimic3wdb-matched/1.0/",
      "patients_list": patients_list_csv,
    }

  ## -- get the list of patients from preset .csv or from physionet -- ##
  def get_patients(self, load_preset: bool = True) -> list[str]:
    if load_preset:
      patients_list = self.args_preset["patients_list"]
      patients_list = patients_list.apply(lambda r: f"{r['patient_group']}/{r['patient_id']}/", axis = 1).tolist()
      patients_list = set(patients_list)
    
    else:
      patients_url = self.args_preset["physionet_url"] + self.args_preset["physionet_dir"] + "RECORDS"
      patients_list = requests.get(patients_url).text.strip().split("\n")

    return list(patients_list)
  
  ## -- get the group and id for a single patient entry of form "pXX/pXXXXXX/" -- ##
  def get_patient_group_id(self, patient_group_id: str) -> tuple[str, str]:
    group, pid = re.match("([^/]+)/([^/]+)/", patient_group_id).groups()
    return group, pid

  ## -- get all the available signals -- ##
  def get_available_signals(self) -> list[str]:
    forbidden = ['???']
    unique_signals = self.args_preset["patients_list"]["patient_signals"].explode().dropna().unique()
    return [s for s in unique_signals if s not in forbidden]

  ## -- get patients that have the listed signals available -- ##
  def get_patient_with_signal(self, patients: list[str] | None = None, 
                               signal_filter: list | None = None) -> pd.DataFrame:
    
    df = self.args_preset["patients_list"].copy()
    patients = patients if patients is not None else list(df["patient_id"])
    df = df[df["patient_id"].isin(patients)]
    if signal_filter is not None:
      df = df[df["patient_signals"].apply(lambda sig: set(signal_filter).issubset(sig))]
    return df

  ## -- get patient record as a dataset -- ##
  def get_patient_record(self, group: str, pid: str, record: str, sampfrom: int | None  = 0, 
                         sampto: int | None  = None, channels: list[int] | None = None) -> wfdb.Record:
    pn_dir = self.args_preset["physionet_dir"] + group + "/" + pid
    rec = wfdb.rdrecord(record, pn_dir = pn_dir, sampfrom = sampfrom, sampto = sampto, channels = channels)
    return rec