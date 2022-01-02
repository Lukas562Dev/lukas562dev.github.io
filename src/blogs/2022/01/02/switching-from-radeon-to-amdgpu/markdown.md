How to switch from the Radeon driver to the AMDGPU driver on Arch Linux.

**NOTE: This guide is for Southern Islands and Sea Islands cards**

*Please see the following [ArchWiki](https://wiki.archlinux.org) articles for more information.*
* [Kernel parameters](https://wiki.archlinux.org/title/Kernel_parameters)
* [AMDGPU](https://wiki.archlinux.org/title/AMDGPU)
* [Mkinitcpio](https://wiki.archlinux.org/title/Mkinitcpio)

## TL;DR

```bash
sudo pacman -S mesa vulkan-radeon
SI_CHECKER='GRUB_CMDLINE_LINUX_DEFAULT=".*\(radeon.si_support=0.*amdgpu.si_support=1\)\|\(amdgpu.si_support=1.*radeon.si_support=0)\)'
sed "/^$SI_CHECKER/! s|^GRUB_CMDLINE_LINUX_DEFAULT=\"\\(.*\\)\"|GRUB_CMDLINE_LINUX_DEFAULT=\"\1 radeon.si_support=0 amdgpu.si_support=1\"|" /etc/default/grub | sudo tee /etc/default/grub
CIK_CHECKER='GRUB_CMDLINE_LINUX_DEFAULT=".*radeon.cik_support=0.*amdgpu.cik_support=1|amdgpu.cik_support=1.*radeon.cik_support=0)'
sed "/^$CIK_CHECKER/! s|^GRUB_CMDLINE_LINUX_DEFAULT=\"\\(.*\\)\"|GRUB_CMDLINE_LINUX_DEFAULT=\"\1 radeon.cik_support=0 amdgpu.cik_support=1\"|" /etc/default/grub | sudo tee /etc/default/grub
sed '/^MODULES=(amdgpu/! s|^MODULES=(|MODULES=(amdgpu radeon |' /etc/mkinitcpio.conf | sudo tee /etc/mkinitcpio.conf
sudo mkinitcpio -P
```

After the script has run, reboot your system and verify the installation with the following one-liner:
```bash
sudo lspci -v | grep 'driver in use: amdgpu' > /dev/null && echo 'Success!' || echo 'Failure!'
```

## Full explanation

### Installing the driver
*You can also install amdvlk or vulkan-radeon for Vulkan support*
```bash
sudo pacman -S mesa
```
### Loading the driver at boot
#### Set module parameters in kernel command line
*You can use both parameters if you are unsure which kernel card you have.*
* Southern Islands (SI): `radeon.si_support=0 amdgpu.si_support=1`
* Sea Islands (CIK): `radeon.cik_support=0 amdgpu.cik_support=1`
**The following script is for GRUB only**
```bash
# Add the parameters to the `GRUB_CMDLINE_LINUX_DEFAULT` variable in `/etc/default/grub` if they are not there yet.

# SI parameters
SI_CHECKER='GRUB_CMDLINE_LINUX_DEFAULT=".*\(radeon.si_support=0.*amdgpu.si_support=1\)\|\(amdgpu.si_support=1.*radeon.si_support=0)\)'
sed "/^$SI_CHECKER/! s|^GRUB_CMDLINE_LINUX_DEFAULT=\"\\(.*\\)\"|GRUB_CMDLINE_LINUX_DEFAULT=\"\1 radeon.si_support=0 amdgpu.si_support=1\"|" /etc/default/grub | sudo tee /etc/default/grub

# CIK parameters
CIK_CHECKER='GRUB_CMDLINE_LINUX_DEFAULT=".*radeon.cik_support=0.*amdgpu.cik_support=1|amdgpu.cik_support=1.*radeon.cik_support=0)'
sed "/^$CIK_CHECKER/! s|^GRUB_CMDLINE_LINUX_DEFAULT=\"\\(.*\\)\"|GRUB_CMDLINE_LINUX_DEFAULT=\"\1 radeon.cik_support=0 amdgpu.cik_support=1\"|" /etc/default/grub | sudo tee /etc/default/grub
```
#### Specify the correct module order
```bash
# Make sure the `amdgpu` module has been set first in the Mkinitcpio MODULES array and then regenerate the initramfs.
sed '/^MODULES=(amdgpu/! s|^MODULES=(|MODULES=(amdgpu radeon |' /etc/mkinitcpio.conf | sudo tee /etc/mkinitcpio.conf
sudo mkinitcpio -P
```

### Reboot your system and verify the installation
```bash
sudo lspci -v | grep 'driver in use: amdgpu' > /dev/null && echo 'Success!' || echo 'Failure!'
```
