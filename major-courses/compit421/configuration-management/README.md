# Configuration Management
---
## Part 1
---
### **DevOps Overview**
---
- **Application Developers** aim to rapidly deliver new features and updates.
- **Operations Teams** focus on stability and uptime, often resisting change to preserve reliability.
- The shift from **Waterfall** to **Agile** methodologies led to faster development cycles.
  - **Example**:
    - Traditional (Waterfall-style): `Oracle Linux 7.0 → 7.1 → 7.2 → 7.3 → 8.0 → 8.1`
    - Agile (Rolling-style): `CentOS Stream 20210328 → 20210413 → 20210421`
- The pace of development outpaced traditional operations processes.
- **DevOps** bridges this gap through collaboration, speed, and automation.

#### **CLAMS: DevOps in a Nutshell**
- **Culture**: Collaboration across development, operations, QA, and other teams to support a shared business goal throughout the application lifecycle.
- **Lean**: Emphasis on reducing waste and encouraging real-time communication and feedback loops.
- **Automation**: Eliminates manual, error-prone tasks and increases deployment speed and reliability.
- **Measurement**: Constant monitoring of systems and services to gain actionable insights.
- **Sharing**: Transparency and open communication of knowledge, tools, and processes.
### **Automation in DevOps**
---
#### **Key Tools by Category**
- **Systems Level Automation**:  
  - Tools: *Ansible*, *SaltStack*, *Puppet*, *Chef*  
  - Automate configuration management and provisioning.
  
- **Continuous Integration (CI) / Delivery (CD)**:  
  - Tools: *Jenkins*, *GitLab CI/CD*, *Bamboo*  
  - Automate building, testing, and deploying code.

- **Infrastructure as Code (IaC)**:  
  - Tools: *Terraform*, *Packer*  
  - Automate infrastructure provisioning and VM/container image creation.
### **What Should Be Automated First?**
---
1. **Automated Setup of New Machines**
   - Tools/Methods: *Preseed* (for Debian/Ubuntu), *Kickstart* (for Red Hat/CentOS), *cloud-init*
   
2. **Automated Configuration Management**
   - Tools: *Ansible* (agentless, YAML-based), *Puppet*, *Chef*

3. **Automated Code Promotion**
   - Pipeline: From Git repo → automated tests → development → staging → production
   - Tools: *Jenkins*, *GitLab CI/CD*

4. **Automated Patching/Updating**
   - Tools: *Ansible* with roles/playbooks for rolling updates, patch management

### **Measurement in DevOps**
---
- **Legacy Monitoring Tools**:  
  - *Nagios*, *Cacti*: Basic alerting and system monitoring.

- **Modern Monitoring and Observability**:
  - Sub-second precision data collection across entire stack (App, OS, Network)
  - Tools:
    - *Prometheus*: Time-series database for metrics
    - *Grafana*: Visualization and alerting on metrics from Prometheus and others

### **YAML Review**
---
#### **What is YAML?**
- YAML stands for “**YAML Ain’t Markup Language**.”
- It’s a human-readable data serialization format, often used for configuration files and data exchange.
- Designed to be readable and easy to write, especially for structured data.

#### **YAML Format Basics**
- **Indentation matters** – usually 2 spaces, no tabs.
- **Structure**:
  ```yaml
  key: value            # Dictionary (mapping)
  list:
    - item1
    - item2             # List (sequence)
  ```
#### **YAML Dictionaries**
- Represented as key-value pairs:
  ```yaml
  user:
    name: Alice
    age: 30
    admin: true
  ```
#### **YAML Booleans**
- YAML supports boolean values:
  ```yaml
  is_admin: true
  is_active: false
  ```
- YAML recognizes multiple boolean representations (though it's best to stick with `true` and `false`):
  - **True values**: `true`, `True`, `TRUE`, `yes`, `on`
  - **False values**: `false`, `False`, `FALSE`, `no`, `off`
### **Understanding the Ansible Playbook Structure**
---
Ansible organizes automation into a structured, modular format to make it scalable, reusable, and easy to manage. Here's a breakdown of the key components involved:

#### **1. Inventory Files (hosts)**
- Define the **list of servers** (hosts) Ansible will manage.
- Can be static (`inventory.ini`) or dynamic (via plugins or scripts).
- Hosts are grouped for easier targeting:
  ```ini
  [webservers]
  web1.example.com
  web2.example.com

  [dbservers]
  db1.example.com
  ```

#### **2. Master Playbook**
- The **main entry point** that calls other playbooks, roles, or tasks.
- Can orchestrate multiple roles or plays across different groups of servers.
  ```yaml
  - hosts: all
    roles:
      - common
      - webserver
  ```

#### **3. Specific Playbooks**
- Target a **specific role or server group**.
- Good for modularizing configurations.
- Example: `webserver.yml`, `database.yml`

#### **4. Roles**
- A **self-contained unit of configuration**, ideal for reuse and sharing.
- Each role has a standard directory structure:
  ```
  roles/
    webserver/
      tasks/
      handlers/
      templates/
      files/
      vars/
  ```

#### **5. Tasks**
- Define the **actual steps** to perform on the system.
- Written in YAML within playbooks or roles:
  ```yaml
  - name: Install nginx
    apt:
      name: nginx
      state: present
  ```

#### **6. Handlers**
- Triggered by **task notifications**, typically used for actions like restarting services:
  ```yaml
  - name: restart nginx
    service:
      name: nginx
      state: restarted
  ```

#### **7. Templates**
- **Jinja2-based files** that allow dynamic content using variables.
- Useful for generating configuration files:
  Example: `nginx.conf.j2`
  ```nginx
  server_name {{ server_name }};
  ```

#### **8. Files**
- Static files that need to be copied directly to target hosts.
- Used when no templating or variable substitution is needed.

#### **9. Variables**
- Used for customization and flexibility.
- Can be defined in:
  - Inventory files
  - `vars/` directory in a role
  - Host or group vars
  - Inline in playbooks
- Example:
  ```yaml
  vars:
    nginx_port: 80
  ```
## Part 2
---
### Agent-Based vs. Agentless Configuration Management
---
#### Agent-Based Platforms
- An **agent** is extra software that needs to be installed on each managed system.
- **Typical setup process:**
  1. Install the agent on the managed node.
  2. Set up network communication between the agent and the control node.
  3. Configure the agent settings.
  4. Enroll the system so the control node can recognize and manage it.

#### Agentless Platforms (e.g., Ansible)
- No additional software is required on the managed node.
- Requirements:
  - SSH access
  - Privileged user (e.g., root or sudo access)
  - Python installed at `/usr/bin/python`

### Avoiding "Snowflake" Systems
---
- A **snowflake system** is one that’s uniquely configured — like a snowflake, it's one of a kind.
- **Why this is bad:**
  - Unique configurations lead to unique issues.
  - Managing many unique systems increases complexity and risk.

#### The Solution:
- Use **centralized configuration management** (e.g., Ansible).
- Store configurations in **version control (e.g., Git)** for tracking and review.
- Automate deployments with tools like:
  - **Red Hat Ansible Tower**
  - **AWX**
  - **Oracle Linux Automation Platform**
### A Structured Approach to Change
---
#### For Major Changes:
1. Create a **new branch**.
2. Add or modify **Ansible playbook** code.
3. Submit a **pull request** for team review.
4. Once approved, **merge** and **deploy**.

#### For Hotfixes:
- Commit directly to the main branch.
- Skip the review or do a quick one.
- Deploy changes **immediately** to resolve the issue.

#### Ansible Hosts file
- Inventory: hosts, proj03-2-inv
- INI format
- section
- Sections are referenced in the playbook
```
$ head -n4 ops.yml
---
# Main playbook for ops fleet
- name: Maintain the ops specific servers
 hosts: ops
```
- hosts: references the sections from the specified inventory file
```
$ ansible-playbook –Ki proj03-2-inv ops.yml
```
#### Recall the Playbook Structure
- If roles/common/tasks/main.yml
- References "prom.cfg"
- src: prom.cfg
- Ansible looks in roles/common/files/
- References "dns.conf.j2"
- template: dns.conf.j2
- Ansible looks in roles/common/templates/
- If there is a variable defined in roles/mgmt_prep/vars/main.yml
- site.yml is the playbook
- invertory is the hosts/inventory file

#### Ansible Variables
- Variables are defined
- In vars/main.yml
- Referenced anywhere else in the role
- Uses a jinja-like syntax
```
---
# roles/install/vars/main.yml
software:
 - vim
 - bash-completion

---
# roles/install/tasks/main.yml
- name: install the required software
 apt:
 name: "{{ item }}"
 state: present
 loop: "{{ software }}"
```
#### Jinja Templates with Ansible
```
---
# roles/example/vars/main.yml
people:
 - name: natheral
 ip: 192.168.56.
 - name: siricer
 ip: 192.168.56.100

# Ansible managed file, do NOT edit!
List of people:
{% for person in people %}
{{ person.name }} uses IP address {{
person.ip }}
{% endfor %}
```
#### Using the Jinja Template in a Task
```
---
# roles/example/tasks/main.yml
- name: Install the Users File
ansible.builtin.template:
src: users.txt.j2
dest: /opt/users
owner: root
group: root
mode: '0640'
```
- The template, users.txt.j2 is the file from previous slide.
- The variables for the template are pulled from the vars/main.yml file
#### Ansible Glossary for Reference
- Control Node: any machine with Ansible installed that runs commands/playbooks to configure other nodes. Cannot be a windows machine.
- Managed Node: hosts that are managed by Ansible via SSH
- Inventory: a list of managed hosts that Ansible uses.
- Tasks: a unit of action in Ansible (ie. Install a package, create a user)
- Playbooks: Ordered lists of tasks.
- Modules: Tasks are implemented using various modules (the code that is executed by the task).
#### Playbook Structure for Reference
- Inventory files
- Master playbook for all servers
- Playbooks for specific servers
- Roles
- Tasks
- Handlers
- Templates
- Files
- Variables

### **Example Project: Deploy a Basic Nginx Web Server**
---
#### ** Project Structure**
```
webserver-ansible/
├── inventory.ini
├── site.yml
├── group_vars/
│   └── webservers.yml
├── roles/
│   └── webserver/
│       ├── tasks/
│       │   └── main.yml
│       ├── handlers/
│       │   └── main.yml
│       ├── templates/
│       │   └── nginx.conf.j2
│       ├── files/
│       │   └── index.html
│       └── vars/
│           └── main.yml
```

####  **1. inventory.ini**
Define the hosts and groups.

```ini
[webservers]
192.168.56.10
192.168.56.11
```

#### **2. site.yml**  
Master playbook to orchestrate everything.

```yaml
- name: Deploy webserver role
  hosts: webservers
  become: yes
  roles:
    - webserver
```

#### **3. group_vars/webservers.yml**
Group-specific variables.

```yaml
nginx_port: 8080
server_name: myserver.local
```

#### **4. roles/webserver/tasks/main.yml**
Tasks to install and configure Nginx.

```yaml
- name: Install nginx
  apt:
    name: nginx
    state: present
    update_cache: yes

- name: Copy index.html
  copy:
    src: index.html
    dest: /var/www/html/index.html

- name: Configure nginx
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/sites-available/default
  notify: restart nginx
```

#### **5. roles/webserver/handlers/main.yml**
Handlers are called when notified (like restarting services).

```yaml
- name: restart nginx
  service:
    name: nginx
    state: restarted
```

#### **6. roles/webserver/templates/nginx.conf.j2**
Jinja2 template for dynamic configuration.

```nginx
server {
    listen {{ nginx_port }};
    server_name {{ server_name }};

    location / {
        root /var/www/html;
        index index.html;
    }
}
```

#### **7. roles/webserver/files/index.html**
Static web content.

```html
<!DOCTYPE html>
<html>
<head><title>Welcome</title></head>
<body>
<h1>It works!</h1>
</body>
</html>
```
#### **8. roles/webserver/vars/main.yml**
Role-specific variables (less common if you use `group_vars`).

```yaml
welcome_message: "Welcome to the server!"
```
#### Running the Playbook

```bash
ansible-playbook -i inventory.ini site.yml
```
