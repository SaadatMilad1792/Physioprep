## Getting Started

To ensure a clean and reproducible setup, it is strongly recommended to create a dedicated Python environment before installing Physioprep. Using an isolated environment helps prevent conflicts with existing packages and makes your workflow more robust. You can create a new environment using Conda as follows:

```bash
# Create a new Conda environment named <env-name> with Python 3.10
conda create --name <env-name> python=3.10

# Activate the newly created environment
conda activate <env-name>
```

Once your environment is active, Physioprep can be installed easily via `pip`:
```bash 
pip install physioprep
```

After the installation completes, your environment is ready to use Physioprep. You can start by importing the package in a Python session to verify that it is installed correctly:
```python
import physioprep
print(physioprep.__version__)
```

## Navigation Panel
<div style="display: flex; justify-content: space-between; width: 100%;">
  <a href="/README.md" style="text-decoration: none;">&#x2B9C; Back (Introduction)</a>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="/" style="text-decoration: none; padding: 4px 8px;">&#x2BAC; Return to repository &#x2BAF;</a>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="/docs/markdowns/mimic_iii_tk.md" style="text-decoration: none; padding: 4px 8px;">Next (Getting Started) &#x2B9E;</a>
</div>