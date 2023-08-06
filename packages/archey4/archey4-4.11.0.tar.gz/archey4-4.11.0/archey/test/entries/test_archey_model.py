"""Test module for Archey's device's model detection module"""

from subprocess import CalledProcessError

import unittest
from unittest.mock import MagicMock, mock_open, patch

from archey.configuration import DEFAULT_CONFIG
from archey.entries.model import Model
from archey.test.entries import HelperMethods


class TestModelEntry(unittest.TestCase):
    """
    For this test we have to go through several eventualities :
    * Laptop / Desktop "regular" environments
    * Raspberry Pi
    * Virtual environment (as a VM or a container)
    * Android devices
    """
    @patch('archey.entries.model.os.getuid')
    @patch('archey.entries.model.check_output')
    @HelperMethods.patch_clean_configuration
    def test_fetch_virtual_env_info(self, check_output_mock, getuid_mock):
        """Test `_fetch_virtual_env_info` method"""
        model_mock = HelperMethods.entry_mock(Model)

        with self.subTest('Detected virtual environment.'):
            check_output_mock.side_effect = [
                FileNotFoundError(),  # `systemd-detect-virt` is not available.
                'xen\nxen-domU\n',    # `virt-what` example output.
                'HYPERVISOR-NAME\n'   # `dmidecode` example output.
            ]
            getuid_mock.return_value = 0

            self.assertEqual(
                Model._fetch_virtual_env_info(model_mock),  # pylint: disable=protected-access
                'HYPERVISOR-NAME (xen, xen-domU)'
            )

        with self.subTest('Virtual environment without `dmidecode`.'):
            check_output_mock.reset_mock()
            getuid_mock.reset_mock()
            check_output_mock.side_effect = [
                FileNotFoundError(),  # `systemd-detect-virt` is not available.
                'xen\nxen-domU\n',    # `virt-what` example output.
                FileNotFoundError()   # `dmidecode` will fail.
            ]
            getuid_mock.return_value = 0

            self.assertEqual(
                Model._fetch_virtual_env_info(model_mock),  # pylint: disable=protected-access
                f"{DEFAULT_CONFIG['default_strings']['virtual_environment']} (xen, xen-domU)"
            )

        with self.subTest('Virtual environment with systemd only.'):
            check_output_mock.reset_mock()
            getuid_mock.reset_mock()
            check_output_mock.side_effect = [
                'systemd-nspawn\n'  # `systemd-detect-virt` output.
            ]
            getuid_mock.return_value = 1000  # `virt-what` and `dmidecode` won't be called.

            self.assertEqual(
                Model._fetch_virtual_env_info(model_mock),  # pylint: disable=protected-access
                f"{DEFAULT_CONFIG['default_strings']['virtual_environment']} (systemd-nspawn)"
            )

        with self.subTest('Virtual environment with systemd and `dmidecode`.'):
            check_output_mock.reset_mock()
            getuid_mock.reset_mock()
            check_output_mock.side_effect = [
                'systemd-nspawn\n',  # `systemd-detect-virt` example output.
                                     # `virt-what` won't be called (systemd call succeeded).
                'HYPERVISOR-NAME\n'  # `dmidecode` example output.
            ]
            getuid_mock.return_value = 0

            self.assertEqual(
                Model._fetch_virtual_env_info(model_mock),  # pylint: disable=protected-access
                'HYPERVISOR-NAME (systemd-nspawn)'
            )

        with self.subTest('Not a virtual environment (systemd).'):
            check_output_mock.reset_mock()
            getuid_mock.reset_mock()
            check_output_mock.side_effect = CalledProcessError(1, 'systemd-detect-virt', 'none\n')

            self.assertIsNone(
                Model._fetch_virtual_env_info(model_mock)  # pylint: disable=protected-access
            )

        with self.subTest('Not a virtual environment (virt-what).'):
            check_output_mock.reset_mock()
            getuid_mock.reset_mock()
            check_output_mock.side_effect = [
                FileNotFoundError(),  # `systemd-detect-virt` won't be available.
                '\n'                  # `virt-what` won't detect anything.
                                      # `dmidecode` won't even be called.
            ]
            getuid_mock.return_value = 0

            self.assertIsNone(
                Model._fetch_virtual_env_info(model_mock)  # pylint: disable=protected-access
            )

        with self.subTest('Not a virtual environment (no tools, no root)'):
            check_output_mock.reset_mock()
            getuid_mock.reset_mock()
            check_output_mock.side_effect = [
                FileNotFoundError()  # `systemd-detect-virt` won't be available.
            ]
            getuid_mock.return_value = 1000  # `virt-what` and `dmidecode` won't be called.

            self.assertIsNone(
                Model._fetch_virtual_env_info(model_mock)  # pylint: disable=protected-access
            )

    def test_fetch_product_info(self):
        """Test `_fetch_product_info` static method"""
        # Product name and version available.
        with patch('archey.entries.model.open', mock_open()) as mock:
            mock.return_value.read.side_effect = [
                'MY-LAPTOP-NAME\n',
                'MY-LAPTOP-VERSION\n'
            ]

            self.assertEqual(
                Model._fetch_product_info(),  # pylint: disable=protected-access
                'MY-LAPTOP-NAME MY-LAPTOP-VERSION'
            )

        # Only product name is available.
        with patch('archey.entries.model.open', mock_open()) as mock:
            mock.return_value.read.side_effect = [
                'MY-LAPTOP-NAME\n',
                FileNotFoundError()
            ]

            self.assertEqual(
                Model._fetch_product_info(),  # pylint: disable=protected-access
                'MY-LAPTOP-NAME'
            )

        # Product name is available but product version is empty.
        with patch('archey.entries.model.open', mock_open()) as mock:
            mock.return_value.read.side_effect = [
                'MY-LAPTOP-NAME\n',
                '\n'
            ]

            self.assertEqual(
                Model._fetch_product_info(),  # pylint: disable=protected-access
                'MY-LAPTOP-NAME'
            )

        # Neither product name nor version are available.
        with patch('archey.entries.model.open', mock_open()) as mock:
            mock.return_value.read.side_effect = [
                FileNotFoundError(),
                FileNotFoundError()
            ]

            self.assertIsNone(Model._fetch_product_info())  # pylint: disable=protected-access

        # Product information are really weird...
        with patch('archey.entries.model.open', mock_open()) as mock:
            mock.return_value.read.side_effect = [
                'To Be Filled By O.E.M.\n'  # Only `product_name` will be read.
            ]

            self.assertIsNone(Model._fetch_product_info())  # pylint: disable=protected-access

    @patch(
        'archey.entries.model.platform.system',
        side_effect=[
            'Darwin',
            'Darwin',
            'OpenBSD',
            'OpenBSD',
            'OpenBSD'
        ]
    )
    @patch(
        'archey.entries.model.check_output',
        side_effect=[
            # First case [Darwin] (`sysctl` won't be available).
            FileNotFoundError(),
            # Second case [Darwin] OK.
            'MacBookPro14,2',
            # Fifth case [BSD] (`sysctl` won't be available).
            FileNotFoundError(),
            # Third case [BSD] (OK).
            'VMware, Inc.\n',
            'VMware Virtual Platform\n',
            'None\n',
            # Fourth case [BSD] (partially-OK).
            CalledProcessError(1, 'sysctl'),
            'KALAP10D300EA\n',
            '1\n'
        ]
    )
    def test_fetch_sysctl_hw(self, _, __):
        """Test `_fetch_sysctl_hw` static method"""
        # pylint: disable=protected-access
        # Dawin cases.
        self.assertIsNone(Model._fetch_sysctl_hw())
        self.assertEqual(Model._fetch_sysctl_hw(), 'MacBookPro14.2')
        # BSD cases.
        self.assertIsNone(Model._fetch_sysctl_hw())
        self.assertEqual(
            Model._fetch_sysctl_hw(),
            'VMware, Inc. VMware Virtual Platform'
        )
        self.assertEqual(Model._fetch_sysctl_hw(), 'KALAP10D300EA 1')
        # pylint: enable=protected-access

    def test_fetch_raspberry_pi_revision(self):
        """Test `_fetch_raspberry_pi_revision` static method"""
        with patch('archey.entries.model.open', mock_open()) as mock:
            mock.return_value.read.side_effect = [
                'Hardware\t: HARDWARE\nRevision\t: REVISION\n',
                'processor   : 0\ncpu family  : X\n'
            ]

            self.assertEqual(
                Model._fetch_raspberry_pi_revision(),  # pylint: disable=protected-access
                'Raspberry Pi HARDWARE (Rev. REVISION)'
            )
            self.assertIsNone(
                Model._fetch_raspberry_pi_revision()  # pylint: disable=protected-access
            )

    @patch(
        'archey.entries.model.check_output',
        side_effect=[
            'PHONE-BRAND\n',     # First `getprop` call.
            'PHONE-DEVICE\n',    # Second `getprop` call.
            FileNotFoundError()  # Second test will fail.
        ]
    )
    def test_fetch_android_device_model(self, _):
        """Test `_fetch_android_device_model` static method"""
        self.assertEqual(
            Model._fetch_android_device_model(),  # pylint: disable=protected-access
            'PHONE-BRAND (PHONE-DEVICE)'
        )
        self.assertIsNone(
            Model._fetch_android_device_model()  # pylint: disable=protected-access
        )

    @HelperMethods.patch_clean_configuration
    def test_no_match(self):
        """Test when no information could be retrieved"""
        model_instance_mock = HelperMethods.entry_mock(Model)

        output_mock = MagicMock()
        Model.output(model_instance_mock, output_mock)

        self.assertIsNone(model_instance_mock.value)
        self.assertEqual(
            output_mock.append.call_args[0][1],
            DEFAULT_CONFIG['default_strings']['not_detected']
        )


if __name__ == '__main__':
    unittest.main()
