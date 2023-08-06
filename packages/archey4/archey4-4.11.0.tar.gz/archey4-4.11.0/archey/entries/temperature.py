"""Temperature detection class"""

import json
import logging
import os
import platform
import re

from glob import iglob
from subprocess import CalledProcessError, DEVNULL, PIPE, check_output, run
from typing import List

from archey.entry import Entry


class Temperature(Entry):
    """
    Tries to compute an average temperature from `sensors` (LM-Sensors).
    If not available, falls back on system thermal zones files (GNU/Linux)
      or `sysctl` output for BSD and derivatives systems.
    On Raspberry devices, retrieves temperature from the `vcgencmd` binary.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._temps = []

        # Tries `sensors` at first.
        self._run_sensors(self.options.get('sensors_chipsets', []))

        # On error (list still empty)...
        if not self._temps:
            if platform.system() == 'Linux':
                # ... checks for system thermal zones files on GNU/Linux.
                self._poll_thermal_zones()
            elif platform.system() == 'Darwin':
                self._run_istats_or_osxcputemp()
            else:
                # ... or tries `sysctl` calls (available on BSD and derivatives).
                self._run_sysctl_dev_cpu()

        # Tries `vcgencmd` for Raspberry devices.
        self._run_vcgencmd()

        # No value could be fetched, leave `self.value` to `None`.
        if not self._temps:
            return

        # Let's DRY some constants once.
        use_fahrenheit = self.options.get('use_fahrenheit')
        char_before_unit = self.options.get('char_before_unit', ' ')

        # Conversion to Fahrenheit if needed.
        if use_fahrenheit:
            self._temps = list(map(self._convert_to_fahrenheit, self._temps))

        # Final average and maximum computations.
        self.value = {
            'temperature': float(round(sum(self._temps) / len(self._temps), 1)),
            'max_temperature': float(round(max(self._temps), 1)),
            'char_before_unit': char_before_unit,
            'unit': ('F' if use_fahrenheit else 'C')
        }


    def _run_sensors(self, whitelisted_chips: List[str]):
        # Uses the `sensors` program (from lm-sensors) to interrogate thermal chip-sets.
        try:
            sensors_output = run(
                ['sensors', '-A', '-j'] + whitelisted_chips,
                universal_newlines=True,
                stdout=PIPE, stderr=PIPE,
                check=True
            )
        except FileNotFoundError:
            error_message = None
            return
        except CalledProcessError as called_process_error:
            error_message = called_process_error.stderr
            return
        else:
            error_message = sensors_output.stderr
        finally:
            # Log any `sensors` error messages at warning level.
            if error_message:
                logging.warning('[lm-sensors]: %s', error_message.rstrip())

        try:
            sensors_data = json.loads(sensors_output.stdout)
        except json.JSONDecodeError:
            return

        # Iterates over the chip-sets outputs to filter interesting values.
        for features in sensors_data.values():
            for subfeatures in features.values():
                for name, value in subfeatures.items():
                    # These conditions check whether this sub-feature value is a correct
                    #  temperature, as :
                    # * It might be an input fan speed (from a control chip) ;
                    # * Some chips/adapters might return null temperatures.
                    if value != 0.0 and re.match(r"temp\d_input", name):
                        self._temps.append(value)
                        # There is only one `temp*_input` field, let's stop the current iteration.
                        break

    def _poll_thermal_zones(self):
        # We just check for values within files present in the path below.
        for thermal_file in iglob(r'/sys/class/thermal/thermal_zone*/temp'):
            with open(thermal_file) as file:
                try:
                    temp = float(file.read())
                except OSError:
                    continue

                if temp != 0.0:
                    self._temps.append(temp / 1000)

    def _run_istats_or_osxcputemp(self):
        """
        For Darwin systems, let's rely on `iStats` or `OSX CPU Temp` third-party programs.
        System's `powermetrics` program is **very** slow to run
          and requires administrator privileges.
        """
        # Run iStats binary (<https://github.com/Chris911/iStats>).
        try:
            istats_output = check_output(
                ['istats', 'cpu', 'temperature', '--value-only'],
                universal_newlines=True
            )
        except FileNotFoundError:
            pass
        else:
            self._temps.append(float(istats_output))
            return

        # Run OSX CPU Temp binary (<https://github.com/lavoiesl/osx-cpu-temp>).
        try:
            osxcputemp_output = check_output('osx-cpu-temp', universal_newlines=True)
        except FileNotFoundError:
            pass
        else:
            # Parse output across  <= 1.1.0 and above.
            temp = float(re.search(r'\d+\.\d', osxcputemp_output).group(0))
            if temp != 0.0:  # (Apple) System Management Control read _may_ fail.
                self._temps.append(temp)

    def _run_sysctl_dev_cpu(self):
        # Tries to get temperatures from each CPU core sensor.
        try:
            sysctl_output = check_output(
                ['sysctl', '-n'] + \
                    [f'dev.cpu.{i}.temperature' for i in range(os.cpu_count())],
                stderr=PIPE, universal_newlines=True
            )
        except FileNotFoundError:
            # `sysctl` does not seem to be available on this system.
            return
        except CalledProcessError as error_message:
            logging.warning(
                '[sysctl]: Couldn\'t fetch temperature from CPU sensors (%s). '
                'Please be sure to load the corresponding kernel driver beforehand '
                '(`kldload coretemp` for Intel or `kldload amdtemp` for AMD`).',
                (error_message.stderr or 'unknown error').rstrip()
            )
            return

        for temp in sysctl_output.splitlines():
            # Strip any temperature unit from output (some drivers may add it).
            temp = float(temp.rstrip('C'))
            if temp != 0.0:
                self._temps.append(temp)

    def _run_vcgencmd(self):
        # Let's try to retrieve a value from the Broadcom chip on Raspberry.
        try:
            vcgencmd_output = check_output(
                ['/opt/vc/bin/vcgencmd', 'measure_temp'],
                stderr=DEVNULL, universal_newlines=True
            )
        except (FileNotFoundError, CalledProcessError):
            return

        self._temps.append(
            float(
                re.search(
                    r'\d+\.\d+',
                    vcgencmd_output
                ).group(0)
            )
        )

    @staticmethod
    def _convert_to_fahrenheit(temp: float) -> float:
        """Simple Celsius to Fahrenheit conversion method"""
        return temp * (9 / 5) + 32


    def output(self, output):
        """Adds the entry to `output` after pretty-formatting with units."""
        if not self.value:
            # Fall back on the default behavior if no temperatures were detected.
            super().output(output)
            return

        # DRY some constants
        char_before_unit = self.value['char_before_unit']
        unit = self.value['unit']

        entry_text = f"{self.value['temperature']}{char_before_unit}{unit}"
        # When there are multiple input sources, show the hottest value.
        if len(self._temps) > 1:
            entry_text += f" (Max. {self.value['max_temperature']}{char_before_unit}{unit})"

        output.append(self.name, entry_text)
