"""Hardware model information detection class"""

import os
import platform
import re

from subprocess import CalledProcessError, DEVNULL, check_output
from typing import Optional

from archey.entry import Entry


class Model(Entry):
    """Uses multiple methods to retrieve some information about the host hardware"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.value = \
            self._fetch_virtual_env_info() \
            or self._fetch_product_info() \
            or self._fetch_sysctl_hw() \
            or self._fetch_raspberry_pi_revision() \
            or self._fetch_android_device_model()

    def _fetch_virtual_env_info(self) -> Optional[str]:
        """
        Relying on some system tools, tries to gather some details about hypervisor.
        When available, relies on systemd.
        When run as root, `virt-what` and/or `dmidecode` may be called.
        """
        environment, product_name = None, None

        try:
            environment = check_output(
                'systemd-detect-virt',
                stderr=DEVNULL, universal_newlines=True
            ).rstrip()
        except CalledProcessError:
            # Not a virtual environment.
            return None
        except FileNotFoundError:
            pass

        # When run as root, let's ask `virt-what` and/or `dmidecode`.
        if os.getuid() == 0:
            # We couldn't retrieve any information from `systemd-detect-virt`.
            if not environment:
                try:
                    environment = ', '.join(
                        check_output(
                            'virt-what',
                            stderr=DEVNULL, universal_newlines=True
                        ).splitlines()
                    )
                except (FileNotFoundError, CalledProcessError):
                    pass

                # Definitely not a virtual environment.
                if not environment:
                    return None

            try:
                # Sometimes we may gather info added by hosting service provider this way.
                product_name = check_output(
                    ['dmidecode', '-s', 'system-product-name'],
                    stderr=DEVNULL, universal_newlines=True
                ).rstrip()
            except (FileNotFoundError, CalledProcessError):
                pass
        elif not environment:
            # No detection tool is available...
            return None

        # If we got there with some info, this _should_ be a virtual environment.
        return f"{{}} ({environment})".format(
            product_name or self._default_strings.get('virtual_environment')
        )

    @staticmethod
    def _fetch_product_info() -> Optional[str]:
        """Tries to open specific Linux files, looking for hardware product name and version"""
        try:
            with open('/sys/devices/virtual/dmi/id/product_name') as f_product_name:
                product_name = f_product_name.read().rstrip()
        except FileNotFoundError:
            return None

        # Stop `/sys/devices/virtual/dmi/id/*` parsing on fuzzy data.
        if re.search(r'To Be Filled', product_name, re.IGNORECASE):
            return None

        try:
            with open('/sys/devices/virtual/dmi/id/product_version') as f_product_version:
                product_version = f_product_version.read().rstrip()
        except FileNotFoundError:
            product_version = ''

        if not product_version:
            return product_name

        return f"{product_name} {product_version}"

    @staticmethod
    def _fetch_sysctl_hw() -> Optional[str]:
        # `hw.model` might be populated with CPU info on BSD platforms.
        # Let's only query this OID on Darwin (macOS).
        if platform.system() == 'Darwin':
            try:
                model = check_output(
                    ['sysctl', '-n', 'hw.model'],
                    stderr=DEVNULL, universal_newlines=True
                )
            except FileNotFoundError:
                return None
            except CalledProcessError:
                pass
            else:
                return model.rstrip().replace(',', '.')

        # Any other BSD (or derivatives).
        hw_oids = []
        for hw_oid in ('vendor', 'product', 'version'):
            try:
                sysctl_output = check_output(
                    ['sysctl', '-n', f'hw.{hw_oid}'],
                    stderr=DEVNULL, universal_newlines=True
                )
            except FileNotFoundError:
                return None
            except CalledProcessError:
                pass
            else:
                sysctl_output = sysctl_output.rstrip()
                if sysctl_output != 'None':
                    hw_oids.append(sysctl_output)

        return ' '.join(hw_oids) or None

    @staticmethod
    def _fetch_raspberry_pi_revision() -> Optional[str]:
        """Tries to retrieve 'Hardware' and 'Revision IDs' from `/proc/cpuinfo`"""
        try:
            with open('/proc/cpuinfo') as f_cpu_info:
                cpu_info = f_cpu_info.read()
        except (PermissionError, FileNotFoundError):
            return None

        # If the output contains 'Hardware' and 'Revision'...
        hardware = re.search(r'(?<=Hardware\t: ).*', cpu_info)
        revision = re.search(r'(?<=Revision\t: ).*', cpu_info)
        if hardware and revision:
            # ... let's set a pretty info string with these data
            return f'Raspberry Pi {hardware.group(0)} (Rev. {revision.group(0)})'

        return None

    @staticmethod
    def _fetch_android_device_model() -> Optional[str]:
        """Tries to retrieve `brand` and `model` device properties on Android platforms"""
        try:
            brand = check_output(
                ['getprop', 'ro.product.brand'],
                universal_newlines=True
            ).rstrip()
            model = check_output(
                ['getprop', 'ro.product.model'],
                universal_newlines=True
            ).rstrip()
        except FileNotFoundError:
            return None

        return f'{brand} ({model})'
