# Shell Scripting (with Bash)
---
## **Scripting vs. Configuration Management**

Scripting and configuration management are often used together but serve different purposes:

- **Scripting** involves writing code (typically in languages like Bash, Python, or Perl) to automate tasks such as file manipulation, system updates, or batch processing.
- **Configuration Management** uses tools (like Ansible, Puppet, or Chef) to define system states and enforce consistency across environments. It’s about **infrastructure as code (IaC)** and maintaining scalability and repeatability in deployments.

Understanding when to script and when to use a config management tool is essential for effective system administration.

## **Learn a Few Things (Very) Well**

Instead of trying to master every tool or language, focus on becoming highly proficient in a few core areas:

- **A scripting language** (like Bash or Python)
- **A configuration management tool** (like Ansible)
- **Core Unix/Linux command-line tools** (e.g., `grep`, `awk`, `sed`, `find`, etc.)

Depth of knowledge in these tools yields better results than shallow familiarity with many.


## **Picking the Correct Scripting Language**

### **Shell (Bash)**
- Ideal for **simple tasks** and **system-level scripting**.
- Fast execution for short scripts.
- Built-in support on virtually all Unix/Linux systems.
- Best used for glue code and orchestration of Unix utilities.

### **Perl**
- Great for **text processing**, **log parsing**, and one-liners.
- Legacy systems may still rely on Perl scripts.
- Rich in built-in regular expression support.
- Slower to write and maintain for large projects.

### **Python / Ruby**
- More readable and maintainable than shell or Perl.
- Python has extensive **standard libraries**, is widely used for **automation**, **DevOps**, and **system scripting**.
- Ruby is the foundation for **Chef** and can be used for scripting, though it's less common now.

### **Go (Golang)**
- Not a traditional scripting language but used for building **fast**, **compiled** automation tools.
- Excellent for system utilities and small command-line tools.
- Offers strong concurrency support.

## **Startup Files**

When a shell session starts, it loads specific files depending on the shell type (login, interactive, etc.):

- **Bash startup files**:  
  - `/etc/profile`  
  - `~/.bash_profile` or `~/.profile` (login shells)  
  - `~/.bashrc` (interactive non-login shells)

These files are used to configure environment variables, aliases, and functions.

## **Writing and Executing a Simple Shell Script**

Steps:
1. **Create a file**:  
   ```bash
   nano myscript.sh
   ```
2. **Add the shebang**:  
   ```bash
   #!/bin/bash
   echo "Hello, world!"
   ```
3. **Make it executable**:  
   ```bash
   chmod +x myscript.sh
   ```
4. **Run it**:  
   ```bash
   ./myscript.sh
   ```

## **Control Operators**

Used to control how commands are executed in relation to each other:

- `;` – Run sequentially regardless of success.
- `&&` – Run next command **only if previous succeeds**.
- `||` – Run next command **only if previous fails**.
- `&` – Run command **in the background**.
- `|` – **Pipe output** of one command into another.

## **Job Control**

Allows you to manage processes from the command line:

- `&` – Run a command in the background.
- `jobs` – View background jobs.
- `fg %1` – Bring job 1 to the foreground.
- `bg %1` – Resume job 1 in the background.
- `kill %1` – Kill a job by job number.

## **Special Characters**

Key symbols in shell scripting with specific meanings:

- `$` – Access variables: `$HOME`, `$1`, `$?`
- `*`, `?`, `[]` – Wildcards/globs
- `\` – Escape characters
- `'` and `"` – Quoting
- `()` – Subshells or grouping commands
- `{}` – Parameter expansion, block grouping
- `` ` `` or `$(...)` – Command substitution

## **Time**

Time commands or scripts:

- `time command` – Measure the execution time of a command.
- `sleep 5` – Pause execution for 5 seconds.
- `date` – Display or set the system date/time.
- `at` and `cron` – Schedule one-time or recurring jobs.

## **Processes**

Understanding how processes work is essential:

- `ps aux` – View running processes.
- `top` / `htop` – Real-time process monitoring.
- `kill PID` – Send signals to processes (e.g., `SIGTERM`, `SIGKILL`).
- `nice`, `renice` – Change process priority.
- `&`, `wait`, `fg`, `bg` – Manage background and foreground processes.

## **History**
Shell keeps a record of previously executed commands:

- `history` – View command history.
- `!n`, `!-1`, `!!` – Run previous commands.
- `history -c` – Clear command history.
- `~/.bash_history` – File storing history between sessions.

## **Example 1: Command-Line Flags Parser**
---
We'll make a script that accepts flags like:

```bash
./user_info.sh -n Alice -a 25
```

### `user_info.sh`:

```bash
#!/bin/bash

# Default values
name="Unknown"
age="Not provided"

# Parse options using a while loop
while [[ $# -gt 0 ]]; do
    case "$1" in
        -n|--name)
            name="$2"
            shift 2
            ;;
        -a|--age)
            age="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 -n <name> -a <age>"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h for help."
            exit 1
            ;;
    esac
done

echo "User Info:"
echo "Name: $name"
echo "Age: $age"
```

>  **How to run it:**
```bash
chmod +x user_info.sh
./user_info.sh -n Bob -a 40
```

## **Example 2: Interactive User Input**
---
This script will **ask the user** for input, then respond based on what they say.

### `interactive.sh`:

```bash
#!/bin/bash

read -p "What's your name? " name
read -p "How old are you? " age

echo ""
echo "Nice to meet you, $name!"
if (( age < 18 )); then
    echo "You're a minor."
elif (( age < 65 )); then
    echo "You're an adult."
else
    echo "You're a senior."
fi
```

> **How to run it:**
```bash
chmod +x interactive.sh
./interactive.sh
```

