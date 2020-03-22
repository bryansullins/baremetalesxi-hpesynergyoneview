# Ansible Modules for HPE OneView Change Log

## Notes on this repo:
- This repo started as a clone from [Hewlett Packard's Oneview Ansible github] (https://github.com/HewlettPackard/oneview-ansible "Hewlett Packard's Oneview Ansible github"). Please consult their repo for HPE-specific changes.

## Initial 1.0.0 Release Date: 3/22/2020

### Added
- Includes the playbook baremetalesxirollouts.yml, which includes customized code for ESXi Baremetal rollouts using Synergy with [HPE's OS/Image Streamer] (https://support.hpe.com/hpesc/public/docDisplay?docId=emr_na-a00003508en_us)
- networksetfacts.yml - included here for getting the network facts needed to include in the main bare metal playbook (as above).