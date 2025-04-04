# Viam Calibration Updater

This tool solves a specific pain-point: manually updating calibration values in a particular Viam machine configuration. Instead of tedious copy-pasting and potential errors, this script automates the process by reading calibration data from a CSV file and applying it to your JSON configuration.


## Installation

```bash
# Clone the repository
git clone https://github.com/hunter-volkman/calibration-updater.git
cd viam-calibration-updater
```

## Usage

The simplest way to run the tool:

```bash
python3 calibration_updater.py
```

This assumes default file names:
- `config.json` - Your existing configuration
- `calibration.csv` - Your new calibration values
- `output.json` - Where to save the updated configuration

### Advanced Options

```bash
python3 calibration_updater.py \
  --config path/to/your/config.json \
  --calibration path/to/your/calibration.csv \
  --output path/to/save/updated-config.json \
  --calibration-fields full_fill_percent empty_fill_percent brightness_threshold \
  --pretty
```

| Option | Description |
|--------|-------------|
| `--config` | Path to input configuration file |
| `--calibration` | Path to calibration CSV file |
| `--output` | Path where updated configuration will be saved |
| `--calibration-fields` | Space-separated list of fields to update |
| `--pretty` | Format output JSON with indentation |

## CSV Format

Your calibration CSV should be structured like this:

```
,A-1,A-2,A-3,B-1,B-2,...
full_fill_percent,55,60,52,58,61,...
empty_fill_percent,26,30,28,32,25,...
brightness_threshold,150,155,150,145,160,...
```

Where:
- The first row contains region names (A-1, A-2, etc.)
- The first column contains calibration parameter names
- The remaining cells contain the new values

## Example

Given:
- A config.json file with regions A-1, A-2, etc., each containing calibration parameters
- A calibration.csv file with updated values for these parameters

Running:
```bash
python3 calibration_updater.py --pretty
```

Results in:
- An output.json file with the updated configuration
- Terminal output showing which values were updated

## Requirements

- Python 3.6 or higher
- No external dependencies
