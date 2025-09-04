########################################################################################################################
## -- libraries and packages -- ########################################################################################
########################################################################################################################
import re
import gc
import wfdb
import pooch
import requests
import pandas as pd
from tqdm import tqdm

########################################################################################################################
## -- preprocessing master class -- ####################################################################################
########################################################################################################################
class M3WaveFormMasterClass():
  def __init__(self, args: dict = None) -> None:
    super(M3WaveFormMasterClass, self).__init__()
    self.args = {
      "patient_list_url": "https://physionet.org/files/mimic3wdb-matched/1.0/RECORDS",
      "data_cache_dir": pooch.os_cache('wfdb'),
      "physionet_url": "https://physionet.org/files/",
      "physionet_dir": "mimic3wdb-matched/1.0/",
    }
    self.update_new_arguments(args)

  def update_new_arguments(self, args: dict) -> None:
    if args is not None:
      for key, value in args.items():
        if key in self.args:
          self.args[key] = value
        else:
          print(f"[!] Parameter reassignment skipped. Key '{key}' does not exist in argument dictionary.")

  def get_argument_list(self) -> list:
    return list(self.args.keys())

  def get_patients(self) -> list:
    patients_list = requests.get(self.args["patient_list_url"]).text.strip().split("\n")
    return list(patients_list)

  def get_patient_group_id(self, patient_group_id: str) -> tuple[str, str]:
    group, pid = re.match("([^/]+)/([^/]+)/", patient_group_id).groups()
    return group, pid
  
  def get_record_list(self, record_url: str) -> list:
    pattern = r"^p\d{6}-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}$"
    content = requests.get(record_url).text.strip().split("\n")
    records = [line for line in content if re.match(pattern, line)]
    return list(records)

  def get_available_signals(self, pn_dir: str, record: str) -> list:
    header = requests.get(self.args["physionet_url"] + pn_dir + "/" + record + ".hea").text.strip().split("\n")
    layouts = [entry.split(" ")[0] for entry in header if "_layout" in entry]
    for layout in layouts:
      layout_file = requests.get(self.args["physionet_url"] + pn_dir + "/" + layout + ".hea").text.strip().split("\n")
      layout_file = [item.split(" ")[-1].strip() for item in layout_file if "~" in item]

    return layout_file

  def get_all_available_signals(self) -> pd.DataFrame:
    wave_form_type_df = []
    patients = self.get_patients()
    pbar = tqdm(patients, desc = "Loading patients")
    for i, patient_group_id in enumerate(pbar):
      pbar.set_description(f"{i+1} out of {len(patients)}")
      group, pid = self.get_patient_group_id(patient_group_id)
      pn_dir = self.args["physionet_dir"] + group + "/" + pid
      records = self.get_record_list(self.args["physionet_url"] + pn_dir + "/" + "RECORDS")
      for record in records:
        wave_form_type_df.append(pd.DataFrame({
          "patient_group": group,
          "patient_id": pid,
          "patient_record": record,
          "patient_signals": [self.get_available_signals(pn_dir, record)],
        }))
        
    return pd.concat(wave_form_type_df)

  def load_patient_record(self, patient_group_id: str, patient_filter: list[str] = None) -> list[object]:
    group, pid = self.get_patient_group_id(patient_group_id)
    pn_dir = self.args["physionet_dir"] + group + "/" + pid
    records = self.get_record_list(self.args["physionet_url"] + pn_dir + "/" + "RECORDS")

    records_list = []
    for record in records:
      if patient_filter is not None:
        signals = self.get_available_signals(pn_dir, record)
        if not set(patient_filter).issubset(signals):
          continue

      print(patient_group_id, record)
      rec = wfdb.rdrecord(record, pn_dir = pn_dir)
      records_list.append({"group": group, "pid": pid, "record": record, "record_data": rec})
      del rec
      gc.collect()

    return records_list
  
  def load_all_patient_record(self, patient_filter: list[str] = None) -> list[object]:
    patient_record = []
    patients = self.get_patients()
    for patient_group_id in patients:
      patient_record.extend(self.load_patient_record(patient_group_id, patient_filter))

    return patient_record