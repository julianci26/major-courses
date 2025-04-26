# Configuration Managment with Ansible
### Setup the Enrollment File
Ansible needs to be created by having the user configured to the enrollment playbook for creating the role `enroll` to setup the ansible user. By using the `remote_user` for the ansible user to create the initial virtual machines for the automation as a specific file.
```
---
# Enrollment Playbook
- name: Prepare a system to be managed by Ansible
  hosts: fleet
  remote_user: kscrivnor
  become: true

  roles:
    - enroll
```

### User Setup
In Ansible, it's important to have a user with a name called `ansible` to run automation tasks and manage systems. This user is set up with the default shell `/bin/bash`, which allows it to run standard commands and scripts from the terminal. A home directory is also created, typically at `/home/ansible`, where Ansible keeps files like SSH keys and configuration settings. Setting up this user helps keep everything organized and makes sure tasks run smoothly and securely. To create a user for configuration management using Ansible, utilize the `ansible.builtin.user` module in the playbook. As shown in this script below:
```
---
- name: Create Ansible user
  ansible.builtin.user:
    name: ansible
    shell: /bin/bash
    become: true
```
This script creates a new user named `ansible` that uses a basic format to update the system and ensures a package is installed. Generates a new SSH key publicly using `ssh-keygen` command to be displayed in the `/home/username/.ssh/id_rsa.pub` file. The new key is then copied to the `authorized_keys` file for the new user by using `ansible.posix.authorized_key` to allow the user to login as the `ansible` without needing a password. 
```
---
- name: Add public key to Ansible user
  ansible.posix.authorized_key:
    user: ansible
    state: present
    key: "{{ lookup('file', '/home/youruser/.ssh/id_rsa.pub') }}"
```
Enabling passwordless `sudo` command using `ansible.builtin.copy` to place a sudoers file `/etc/sudoers.d/ans` with an entry that allows the `ansible` user to run **any** command as the root via `sudo` **without being prompted for a password**. The `mode: '0440'` parameter in Ansible ensures that the permissions for the authorized_keys file are set correctly, making it read-only for security. 

```
---
- name: Allow ansible user passwordless sudo
  ansible.builtin.copy:
    dest: /etc/sudoers.d/ans
    content: "ansible ALL=(ALL) NOPASSWD: ALL\n"
    mode: '0440'
```
