# ESXi Baremetal Provisioning with HPE OS Streamer and Ansible
> Single touch ESXi baremetal provisioning on HPE Synergy Blades with Ansible/OneView/OS Streamer.

## Assumptions
- It is assumed you are well-versed in:
  - The HPE OneView Gold Image Capture Process.
  - The HPE Oneview Server Template Profile  and Server Profile Creation Process.
  - The HPE Oneview OS Streamer OS Deployment Process, including OS Deployment plans and their components.
  - Your ESXi and vCenter needed configutation items (only some well-known configuration items are included here).

## Requirements
- This Repo includes the library and module utils from [Hewlett Packard's Oneview Ansible github] (https://github.com/HewlettPackard/oneview-ansible "Hewlett Packard's Oneview Ansible github"). Please check there for updates to their portion of the code, as these here are static.
- It is recommended you use virtualenv.
- pip3 freeze shows these python modules are needed:

    ansible==2.9.2    
    certifi==2019.11.28    
    cffi==1.13.2    
    chardet==3.0.4    
    cryptography==2.8    
    future==0.18.2    
    hpICsp==1.0.2    
    hpOneView==5.0.0    
    idna==2.8    
    Jinja2==2.10.3    
    MarkupSafe==1.1.1    
    pycparser==2.19    
    python-hpilo==4.3    
    pyvmomi==6.7.3    
    PyYAML==5.2    
    requests==2.22.0    
    six==1.13.0    
    urllib3==1.25.7     

## Usage example

I have made comments throughout for guidance through the playbook and repo. As long as you know the HPE Oneview process with OS/Image streamer, you should be able to fill in the blanks. The same goes for anything related to the VMware plays (which, in my humble opinion, is the easy part).

    ansible-playbook -i inventory/hosts --limit localhost baremetalesxirollouts.yml --ask-vault-pass -vvvv # <- Verbose for debugging.

## Release History

* 1.0.0
    * First Release 3/22/2020

## Meta

Bryan Sullins – [@RussianLitGuy](https://twitter.com/RussianLitGuy) – bryansullins@thinkingoutcloud.org

[https://github.com/bryansullins](https://github.com/bryansullins)

## Contributing

Pull Requests are always welcome! Make it better!

