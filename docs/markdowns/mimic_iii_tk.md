
## MIMIC-III Toolkit
This section is specifically dedicated to providing a comprehensive and detailed documentation of the MIMIC-III Toolkit, which serves as a set of utilities and methods designed for working with the MIMIC-III Waveform Database Matched Subset. In addition to describing the functionalities and features of the toolkit, this section thoroughly explains the underlying methodologies, the rationale behind each implemented function, and the recommended usage patterns. The goal is to equip researchers, data scientists, and practitioners with clear guidance, practical examples, and contextual information that facilitates the effective and efficient use of the toolkit for tasks such as physiological time-series analysis, preprocessing, and integration with generative modeling workflows. By covering both high-level conceptual overviews and low-level implementation details, this section aims to provide a complete resource for understanding, navigating, and applying the MIMIC-III Toolkit in a variety of research and analytical scenarios.

<!-- get_patients -->
### Methods &#x279C; get_patients
```python
get_patients(self, load_preset: bool = True) -> list[str]
```
**Description:** This method extracts, and returns a list of patients.

**Parameters:**
- load_preset: fetches RECORDS from physionet if set to `False`, and loads from preset csv file if set to `True`.

**Returns:** a list of strings, where each string is a `patient_id`.

<!-- get_patient_group_id -->
### Methods &#x279C; get_patient_group_id
```python
get_patient_group_id(self, patient_group_id: str) -> tuple[str, str]
```
**Description:** for a single patient entry from RECORDS returns group and pid.

**Parameters:**
- patient_group_id: patients group and id in the following string format `group/id/` (e.g. `p00/p000020/`).

**Returns:** a tuple with the following format (`group`, `id`).

<!-- get_available_signals -->
### Methods &#x279C; get_available_signals
```python
get_available_signals(self) -> list[str]
```
**Description:** gets all available signals in the entire [MIMIC-III Waveform Database Matched Subset](https://physionet.org/content/mimic3wdb-matched/1.0/).

**Returns:** list of all available signals in the entire [MIMIC-III Waveform Database Matched Subset](https://physionet.org/content/mimic3wdb-matched/1.0/).

<!-- get_patient_with_signal -->
### Methods &#x279C; get_patient_with_signal
```python
get_patient_with_signal(self, patients: list[str] | None = None, 
                              signal_filter: list[str] | None = None) -> pd.DataFrame
```
**Description:** gets all the entries in the patients dataframe which have certain signals.

**Parameters:**
- patients: can limit the search to certain patients.
- signal_filter: which signals must be included in the entries (e.g. `['ABP', 'II']`).

**Returns:** a dataframe of patients and records that are guaranteed to have all the signals included in `signal_filter`.

<!-- get_patient_record -->
### Methods &#x279C; get_patient_record
```python
get_patient_record(self, group: str, pid: str, record: str, sampfrom: int = 0, 
                         sampto: int | None  = None, channels: list[int] | None = None) -> wfdb.Record
```
**Description:** given a patients information, fetches the corresponding record data files.

**Parameters:**
- group: patients group indicator (e.g. `p00`).
- pid: patients id indicator (e.g. `p000020`).
- record: patients record name (e.g. `p000020-2183-04-28-17-47`).
- sampfrom: starting point of the loaded files, initially set to `0`.
- sampto: ending point of the loaded files, if set to `None`, will load the entire file.
- channels: specific channels to be included in the record file (e.g. `['ABP', 'PLETH']`).

**Returns:** returns the corresponding `wfdb.Record` for a given patient (just the data).

<!-- get_patient_header -->
### Methods &#x279C; get_patient_header
```python
get_patient_header(self, group: str, pid: str, record: str) -> wfdb.Record
```
**Description:** given a patients information, fetches the corresponding header files.

**Parameters:**
- group: patients group indicator (e.g. `p00`).
- pid: patients id indicator (e.g. `p000020`).
- record: patients record name (e.g. `p000020-2183-04-28-17-47`).

**Returns:** returns the corresponding `wfdb.Record` for a given patient (just the header).

<!-- get_patient_header -->
### Methods &#x279C; get_patient_header
```python
get_subject_split(self, df: pd.DataFrame, frac1: float = 0.8, frac2: float = 0.1, frac3: float = 0.1, 
                  seed: int | None = None, channels: list[str] | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
```
**Description:** splits a dataframe, to patient-based isolated training, testing, and validation sets.

**Parameters:**
- df: the initial dataframe.
- frac1: training portion of the dataframe, default value is `0.8`.
- frac2: validation portion of the dataframe, default value is `0.1`.
- frac3: test portion of the dataframe, default value is `0.1`.
- seed: random_state for reproducibility.
- channels: filters patients with the given data types only, the then splits (e.g. `['ABP', 'II']`)

**Returns:** returns a tuple of three dataframes of patient info for train, test, and validation.

<!-- get_data_batch -->
### Methods &#x279C; get_data_batch
```python
get_data_batch(self, df: pd.DataFrame, batch_size: int, signal_len: int, 
                     channels: list[str] | None = None, timeout: int = 100) -> np.array
```
**Description:** generates a batch of data with a certain length from a given dataframe.

**Parameters:**
- df: the initial dataframe.
- batch_size: training portion of the dataframe, default value is `0.8`.
- signal_len: length of the chosen segment for each batch element.
- channels: signals to be included in the batch (e.g. `['ABP', 'II']`).
  - **Note:** Only use `None` if you have already filtered the signals during splitting.
- timeout: maximum failure rounds allowed before returning the premature batch.
  - **Note:** MIMIC is not guaranteed to have all signals in all timestamps, therefore we 
              will hault the process after not being able to find the required batch size 
              after this many steps, default is `100`.

**Returns:** returns a np.array of shape `(smaller or equal to batch_size, len(channels), signal_len)`

## Navigation Panel
- [Back (Getting Started)](/docs/markdowns/getting_started.md)
- [Return to repository](/)
<!-- - [Next (TBD)](/docs/markdowns/getting_started.md) -->