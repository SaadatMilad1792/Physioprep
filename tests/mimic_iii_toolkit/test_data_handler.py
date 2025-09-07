########################################################################################################################
## -- libraries and packages -- ########################################################################################
########################################################################################################################
import physioprep

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