# Container (with Docker)
---
## Containers vs. Virtualization
- **Containers** offer a lightweight form of isolation by leveraging **kernel features** such as namespaces and cgroups. These isolate a process and its resources from other processes and containers.
- Unlike virtual machines, containers share the **host operating system kernel** but still maintain isolated execution environments.

## Virtual Machines and Containers Are Different
- A **virtual machine (VM)** is a complete operating system instance running on top of a **hypervisor**.
- The **hypervisor** acts as an abstraction layer between the VM and the physical hardware, enabling multiple OS instances to run on a single machine.

## Type 1 vs. Type 2 Hypervisors
- **Type 1 Hypervisor (Bare-metal)**: Runs directly on the hardware without needing a host operating system. Example: VMware ESXi, Microsoft Hyper-V (bare-metal).
- **Type 2 Hypervisor (Hosted)**: Runs on top of a general-purpose OS. Example: VirtualBox, VMware Workstation.

## Full Virtualization
- In **full virtualization**, hardware is **completely emulated**, allowing unmodified guest OSes to run as if they were on real hardware.
- Emulated components include:
  - Hard disks
  - Network interfaces
  - Interrupts
  - Motherboard components
- **Example**: [QEMU](https://qemu.org) — often used to create system images or automate the setup of embedded devices like the Raspberry Pi.

## Paravirtualization
- Introduced by the **Xen hypervisor**, **paravirtualization** involves modifying the guest OS so that it is aware it's running in a virtualized environment.
- This cooperation allows the guest to interact more efficiently with the hypervisor but requires maintaining modified guest OS kernels.
- While efficient, it can be high-maintenance and lacks compatibility with unmodified operating systems.

## Hardware-Assisted Virtualization
- Modern CPUs include **hardware virtualization extensions** that eliminate the need to modify guest OSes:
  - **Intel VT-x (Virtualization Technology)**
  - **AMD-V (AMD Virtualization)**
- These technologies allow for efficient VM execution while maintaining compatibility with stock operating systems.

## Paravirtualized Drivers
- Rather than paravirtualizing the entire OS, **paravirtualized drivers** can be installed to improve performance of specific hardware functions (like disk, network, or video).
- These drivers communicate directly with the hypervisor for faster I/O operations, simplifying VM management.

## Modern Virtualization: A Hybrid Approach
- Today’s virtualization stacks blend:
  - **Hardware virtualization (Intel VT, AMD-V)**
  - **Paravirtualized drivers**
  - **Selective kernel modifications**
- This combination allows **high performance** while **minimizing the need** for guest OS changes.


## Container Glossary

- **Image**: A packaged snapshot of a filesystem and application needed to run a container. Pulled from a **registry**.
- **OCI (Open Container Initiative)**: A standards body focused on defining **container runtime** and **image specifications**, ensuring interoperability.
- **Image Format**: A standardized layout for container images, defining layers, configuration, and metadata.
- **Engine**: Software responsible for building, running, and managing containers. Example: Docker Engine, containerd.
- **Container**: A running instance of an image. It's an isolated process that behaves like a lightweight virtual machine.
- **Container Host**: The system (typically a Linux server) where containers are executed. It includes the kernel and the container engine.
- **Registry Server**: A service (like Docker Hub or a private registry) where container images are stored and distributed.
- **Orchestration**: Tools like Kubernetes or Docker Swarm used to manage container deployment, scaling, and networking across clusters.
- **Runtime**: The low-level component responsible for managing container lifecycle. Example: runc.
- **Image Layer**: Images are built in layers. Each layer represents a filesystem change, and multiple layers form the final image.
- **Tag**: A label used to reference specific versions of images. Default is `latest`, but can be any string like `v1.0.2`.


## Docker Architecture Overview
- Docker consists of several components:
  - **Docker Daemon** (`dockerd`): Core service that manages containers, images, and networks.
  - **Docker CLI** (`docker`): Command-line interface used to interact with the daemon.
  - **Docker Images**: Templates used to create containers.
  - **Docker Containers**: Running instances of Docker images.
  - **Docker Registry**: Central location where Docker images are stored and pulled from.
- The architecture follows a client-server model where the CLI communicates with the daemon over REST APIs.

## Containers as "Containerized Processes"
- Containers are essentially **isolated processes** on the host system, limited in their view and resource access.
- They don’t run their own kernel but share the host’s kernel, unlike VMs.

## Frequently Used Docker Commands
- `docker run`: Create and start a container.
- `docker ps`: List running containers.
- `docker build`: Build an image from a Dockerfile.
- `docker pull`: Download an image from a registry.
- `docker push`: Upload an image to a registry.
- `docker exec`: Run commands inside a running container.
- `docker logs`: Fetch logs from a container.
- `docker stop`: Stop a running container.
- `docker rm`: Remove a container.
- `docker rmi`: Remove an image.

## Components of a Container Image
- **Root Filesystem**: A snapshot of a Linux filesystem (e.g., based on Ubuntu, Alpine) that the container uses.
- **Configuration Metadata**: Instructions like default command (`CMD`), environment variables (`ENV`), working directory (`WORKDIR`), and ports (`EXPOSE`).
