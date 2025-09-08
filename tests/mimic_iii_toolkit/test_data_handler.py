########################################################################################################################
## -- libraries and packages -- ########################################################################################
########################################################################################################################
import numpy as np
import physioprep

########################################################################################################################
## -- tests for validation master class -- #############################################################################
########################################################################################################################
def val():
  return physioprep.M3ValidationMasterClass()

def test_is_item_not_nan():
  nan_arr = np.array([[1, np.nan, 2], [1, 4, 2]])
  flag = val().is_item_not_nan(nan_arr)
  assert not flag

  nan_arr = np.array([[1, 0, 2], [1, 4, 2]])
  flag = val().is_item_not_nan(nan_arr)
  assert flag

def test_is_length_valid():
  len_arr = np.array([1, 2, 3, 4, 5])
  flag = val().is_length_valid(len_arr, 5)
  assert flag

  len_arr = np.array([1, 2, 3, 4, 5, 3, 3, 1])
  flag = val().is_length_valid(len_arr, 5)
  assert not flag
  
def test_apply():
  nan_arr = np.array([[1, np.nan, 2], [1, 4, 2]])
  flag = val().apply(nan_arr, 2)
  assert not flag

  flag = val().apply(nan_arr, 3)
  assert not flag

  nan_arr = np.array([[1, 0, 2, 5], [1, 4, 2, 4]])
  flag = val().apply(nan_arr, 3)
  assert not flag

  nan_arr = np.array([[1, 0, 2], [1, 4, 2], [2, 8, 2]])
  flag = val().apply(nan_arr, 3)
  assert flag

########################################################################################################################
## -- tests for physioprep module [mimic iii toolkit] -- ###############################################################
########################################################################################################################
def ppm():
  return physioprep.M3WaveFormMasterClass()

def test_get_patients() -> None:
  patients_preset = ppm().get_patients(load_preset = True)
  patients_reqset = ppm().get_patients(load_preset = False)
  only_in_preset = set(patients_preset) - set(patients_reqset)
  assert not only_in_preset

def test_get_patient_group_id() -> None:
  group, pid = ppm().get_patient_group_id("p00/p000020/")
  assert group == "p00"
  assert pid == "p000020"

def test_get_available_signals():
  real_signals = ['L', 'II+', 'aVL', 'CO2', 'II', 'BAP', 'R', 'PLETH', 'PLETHl', 'UVP', 'RAP', 'I', 
                  'aVR', 'MCL1+', 'AVR', 'UAP', 'IC1', 'AVF+', 'ECG', 'ART', 'III+', 'V+', 'III', 'AVL', 
                  'I+', 'FAP', 'Ao', 'V3', 'V', 'V2', 'PAP', 'AOBP', 'V5', 'P4', 'IC2', 'ABP', 'P1', 
                  'CVP', 'MCL+', 'LAP', 'AVR+', 'AVF', 'aVF', 'PLETHr', 'MCL', 'RESP', 'ICP', 'V1', 'MCL1']

  available_signals = ppm().get_available_signals()
  mismatch = set(available_signals) - set(real_signals)
  assert not mismatch

def test_get_patient_with_signal():
  df = ppm().get_patient_with_signal(patients = None, signal_filter = None)
  assert len(df) == 22494

  df = ppm().get_patient_with_signal(patients = ["p000020"], signal_filter = None)
  assert len(df) == 1

  df = ppm().get_patient_with_signal(patients = None, signal_filter = ['ABP'])
  assert len(df) == 9643

  df = ppm().get_patient_with_signal(patients = ["p000020"], signal_filter = ['ABP'])
  assert len(df) == 1

def test_get_patient_record():
  df = ppm().args_preset["patients_list"].iloc[0]
  rec = ppm().get_patient_record(df["patient_group"], df["patient_id"], df["patient_record"], 
                                 sampfrom = 20000, sampto = 20500, channels = ['II', 'ABP'])
  
  sig_mismatch = set(rec.sig_name) - set(['II', 'ABP'])
  assert not sig_mismatch
  assert rec.p_signal.shape == (500, 2)

def test_get_patient_header():
  df = ppm().args_preset["patients_list"].iloc[0]
  header = ppm().get_patient_header(df["patient_group"], df["patient_id"], df["patient_record"])
  assert header.sig_len == 9862593

def test_get_subject_split():
  df = ppm().args_preset["patients_list"]
  a, b, c = ppm().get_subject_split(df, channels = ['ABP', 'II', 'PLETH'])
  assert len(a) == 4784 and len(b) == 598 and len(c) == 598

def test_get_data_batch():
  channels = ['ABP', 'II', 'PLETH']
  df = ppm().args_preset["patients_list"]
  tr_df, va_df, te_df = ppm().get_subject_split(df, channels = channels)
  batch = ppm().get_data_batch(tr_df, batch_size = 12, signal_len = 750, channels = channels)
  assert batch.shape[1:] == (3, 750)
  assert batch.shape[0] <= 12