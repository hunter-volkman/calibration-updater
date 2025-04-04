#!/usr/bin/env python3
"""
Calibration Updater for Viam Machine JSON Config

This script updates the Viam machine configuration by applying new calibration values
from a CSV file to the existing configuration, producing an updated JSON configuration file.
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, Any, List


def parse_arguments() -> argparse.Namespace:
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(
        description='Update Viam machine configuration with new calibration values.'
    )
    parser.add_argument(
        '--config', 
        type=str, 
        default='config.json',
        help='Path to the existing configuration JSON file (default: config.json)'
    )
    parser.add_argument(
        '--calibration', 
        type=str, 
        default='calibration.csv',
        help='Path to the calibration CSV file (default: calibration.csv)'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        default='output.json',
        help='Path for the updated configuration file (default: output.json)'
    )
    parser.add_argument(
        '--calibration-fields', 
        type=str, 
        nargs='+',
        default=['full_fill_percent', 'empty_fill_percent', 'brightness_threshold'],
        help='Calibration fields to update (default: full_fill_percent empty_fill_percent brightness_threshold)'
    )
    parser.add_argument(
        '--pretty', 
        action='store_true',
        help='Pretty-print the JSON output'
    )
    
    args = parser.parse_args()
    
    # Validate that files exist
    if not Path(args.config).exists():
        parser.error(f"Configuration file not found: {args.config}")
    if not Path(args.calibration).exists():
        parser.error(f"Calibration file not found: {args.calibration}")
        
    return args


def load_json_config(config_path: str) -> Dict[str, Any]:
    """Load and parse the JSON configuration file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON configuration: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading configuration file: {e}", file=sys.stderr)
        sys.exit(1)


def load_calibration_data(calibration_path: str) -> Dict[str, Dict[str, float]]:
    """
    Load and parse the calibration CSV file.
    
    Returns a dictionary mapping region names to calibration values.
    """
    calibration_data = {}
    
    try:
        with open(calibration_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            
            # Process each row in the CSV
            for row in reader:
                # The first column might be empty or contain row labels
                row_label = row.get('', '')
                
                # Extract calibration values for each region
                region_data = {}
                for region, value in row.items():
                    # Skip empty column headers
                    if region and region != '':
                        try:
                            # Convert value to float if it's a number
                            if value and value.strip():
                                region_data[region] = float(value)
                        except ValueError:
                            # Skip non-numeric values
                            pass
                
                # Store with row label for identification (like "full_fill_percent")
                if row_label:
                    calibration_data[row_label] = region_data
    
    except Exception as e:
        print(f"Error reading calibration file: {e}", file=sys.stderr)
        sys.exit(1)
    
    return calibration_data


def update_config_with_calibration(
    config: Dict[str, Any], 
    calibration_data: Dict[str, Dict[str, float]],
    calibration_fields: List[str]
) -> Dict[str, Any]:
    """Update configuration with new calibration values."""
    # Create a deep copy of the config to avoid modifying the original
    updated_config = json.loads(json.dumps(config))
    
    # Check if regions exist in the config
    if 'regions' not in updated_config:
        print("Warning: No 'regions' section found in configuration", file=sys.stderr)
        return updated_config
    
    # Process each region in the config
    for region_name, region_config in updated_config['regions'].items():
        # Update each calibration field if it exists in both config and calibration data
        for field in calibration_fields:
            # Check if we have calibration data for this field
            if field in calibration_data:
                # Check if we have a value for this region
                if region_name in calibration_data[field]:
                    # Update the value in the config
                    if field in region_config:
                        new_value = calibration_data[field][region_name]
                        old_value = region_config[field]
                        region_config[field] = new_value
                        print(f"Updated {region_name}.{field}: {old_value} -> {new_value}")
                    else:
                        print(f"Warning: Field '{field}' not found in region '{region_name}'", file=sys.stderr)
    
    return updated_config


def save_config(config: Dict[str, Any], output_path: str, pretty: bool = False) -> None:
    """Save the updated configuration to a file."""
    try:
        with open(output_path, 'w') as f:
            if pretty:
                json.dump(config, f, indent=2)
            else:
                json.dump(config, f)
        print(f"Successfully wrote updated configuration to {output_path}")
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main function to run the calibration update process."""
    # Parse command-line arguments
    args = parse_arguments()
    
    # Load existing configuration
    config = load_json_config(args.config)
    
    # Load calibration data
    calibration_data = load_calibration_data(args.calibration)
    
    # Update configuration with calibration data
    updated_config = update_config_with_calibration(
        config, 
        calibration_data,
        args.calibration_fields
    )
    
    # Save updated configuration
    save_config(updated_config, args.output, args.pretty)


if __name__ == "__main__":
    main()