# Container Technology
---
### What People Often Forget About Containers  
- **Definition**: A container is a group of processes that are isolated within a private root file system and process namespace. 
- Containers are built on top of well-established UNIX/Linux features that have existed for years — even decades. 
- They rely on kernel-level capabilities like **cgroups** and **namespaces**, along with: 
  - Filesystem techniques like **chroot** 
  - Network configurations using **virtual adapters**
  
### Container File Systems
---
#### Local Read/Write Layers in Containers  
- Containers use a layered file system, with a top-level writable layer.
- A **volume** is a standalone, writable directory that can be mounted into a container. 
- This is ideal for data-heavy applications (e.g., databases), where data needs to persist beyond the life of the container.

#### Bind Mounts  
- A **bind mount** connects a specific directory on the host (e.g., `~/examples/data`) to a location inside the container (e.g., `/data`).
- Changes made in either the host or the container are reflected in both places.

#### Limitations of Volumes  
- Remember, the main purpose of containers is to run applications — not to mimic full system environments.
- Persistent volumes can go against this philosophy by introducing state into containers, which are meant to be ephemeral and portable.

### How the Kernel Enables Containers
---
#### Application and Kernel Interaction  
- The **kernel** serves as a bridge between hardware and software, managing system resources and enforcing isolation.
- **System libraries** provide a higher-level, more developer-friendly interface to interact with kernel features.
- However, applications can bypass these libraries and interact directly with the kernel using **system calls (syscalls)** when needed.

#### Bash syscalls (abbreviated)
- Where to search for files:
```
$ echo $PATH
/home/kscrivnor/.local/bin:/home/kscrivnor/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/us
r/sbin
```
- Syscalls
```
[…]
stat("/home/kscrivnor/.local/bin/ls", 0x7ffcb7244ab0) = -1 ENOENT (No such file or directory)
stat("/home/kscrivnor/bin/ls", 0x7ffcb7244ab0) = -1 ENOENT (No such file or directory)
stat("/usr/local/bin/ls", 0x7ffcb7244ab0) = -1 ENOENT (No such file or directory)
stat("/usr/bin/ls", {st_mode=S_IFREG|0755, st_size=143368, ...}) = 0
[…]
access("/usr/bin/ls", X_OK)= 0
access("/usr/bin/ls", R_OK)= 0
[…]
clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD,
child_tidptr=0x7f857c80ea10) = 1849
```
#### Going down the rabbit hole of syscalls
- Rabbit hole (in the directory, literally)
- Rabbit hole (common use, idiom, connection)
- Let's look at executing the command: cat /etc/passwd
#### Reading the File: cat /etc/passwd
- Execute the command $ cat /etc/passwd
- The command displays the contents to the screen
- $ strace -o cat_strace cat /etc/passwd
#### Analyzing cat_strace
- openat(AT_FDCWD, "/etc/passwd", O_RDONLY) = 3
- fstat(3, {st_mode=S_IFREG|0644, st_size=2129, ...}) = 0
- fadvise64(3, 0, 0, POSIX_FADV_SEQUENTIAL) = 0
- mmap(NULL, 139264, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7fd0cc710000
- read(3, "root:x:0:0:root:/root:/bin/bash\n"..., 131072) = 2129
- write(1, "root:x:0:0:root:/root:/bin/bash\n"..., 2129) = 2129
#### Analyzing the C Program syscalls
- openat(AT_FDCWD, "/etc/passwd", O_RDONLY) = 3
- fstat(3, {st_mode=S_IFREG|0644, st_size=2129, ...}) = 0
- read(3, "root:x:0:0:root:/root:/bin/bash\n"..., 4096) = 2129
- fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0x3), ...}) = 0
- write(1, "root:x:0:0:root:/root:/bin/bash\n", 32) = 32
- write(1, "bin:x:1:1:bin:/bin:/sbin/nologin"..., 33) = 33
- write(1, "daemon:x:2:2:daemon:/sbin:/sbin/"..., 40) = 40
- write(1, "adm:x:3:4:adm:/var/adm:/sbin/nol"..., 37) = 37
- write(1, "lp:x:4:7:lp:/var/spool/lpd:/sbin"..., 41) = 41
- write(1, "sync:x:5:0:sync:/sbin:/bin/sync\n", 32) = 32
- write(1, "shutdown:x:6:0:shutdown:/sbin:/s"..., 45) = 45
- write(1, "halt:x:7:0:halt:/sbin:/sbin/halt"..., 33) = 33
- write(1, "mail:x:8:12:mail:/var/spool/mail"..., 47) = 47

### Container Enabling Technology: **cgroups**
---
#### What Are Control Groups (cgroups)?
- According to the kernel documentation, **"cgroup"** stands for **control group** (and is always written in lowercase).  
- cgroups have **two main parts**:
  1. A **core mechanism** for organizing processes into a hierarchy.
  2. A collection of **controllers** that manage and monitor those processes.  
     - Common controllers include: `memory`, `cpu`, `io`, `pid`, `rdma`, and others.
**Purpose**:  
- To divide and isolate system resources between workloads — for example, separating high-priority applications from background tasks.

#### What Can cgroups Do?
- **Limit resources** for a process group:
  - CPU time
  - Memory usage
  - Device access
  - Specific CPU cores
- **Monitor usage** of:
  - Memory
  - CPU
  - I/O
  - Network bandwidth
  
#### Checking for cgroups v2
- Run: 
  ```bash
  sudo grep cgroup /proc/mounts
  ``` 
  to see whether your system uses cgroups v1 or v2.

- On **Debian-based systems**, you may need to explicitly enable cgroup v2 depending on your kernel version and configuration.

#### cgroups Use a Pseudo-Filesystem Interface
- The **cgroup hierarchy** is represented as a directory structure in a special virtual filesystem.  
- You can:
  - Use `mkdir` to create new cgroups.
  - Use `rmdir` to remove them.
- When a new directory is created, the **kernel auto-populates it** with relevant files.
These files include:
- **Management files** for controlling group membership
- **Controller-specific files** for setting limits and policies
- **Metrics files** that report usage data for processes within the group

#### Example: Creating and Using a cgroup
1. **Create a new cgroup**  
   ```bash
   mkdir vmuser
   ```
2. **Add your current shell to the new cgroup**  
   ```bash
   echo $$ > vmuser/cgroup.procs
   ```
3. **Set a limit on the number of processes (max 5)**  
   ```bash
   echo 5 > vmuser/pids.max
   ```
4. **Test the limit by trying to spawn more processes than allowed**  
   ```bash
   for i in {1..10}; do sleep 30 & done
   ```
