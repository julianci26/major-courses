#!/bin/bash

# Develop the directory included in your playbook
base_dir="second-playbook"

# List of all directories you want to create
dirs=(
	"$base_dir"
	"$base_dir/roles"
	"$base_dir/roles/enroll"
	"$base_dir/roles/enroll/files"
	"$base_dir/roles/enroll/tasks"
	"$base_dir/roles/devs"
	"$base_dir/roles/devs/tasks"
	"$base_dir/roles/devs/vars"
 	"$base_dir/roles/common"
 	"$base_dir/roles/common/files"
  	"$base_dir/roles/common/tasks"
   	"$base_dir/roles/common/templates"
    	"$base_dir/roles/common/vars"
     	"$base_dir/roles/banana"
      	"$base_dir/roles/banana/tasks"
)

# Create all directories
for dir in "${dirs[@]}"; do
	mkdir -p "$dir"
done
echo "All Directories Made"
files=(
	"$base_dir/dev.yml"
	"$base_dir/enroll.yml"
	"$base_dir/hosts"
 	"$base_dir/hosts-control.yml"
  	"$base_dir/ops.yml"
   	"$base_dir/site.yml"
	"$base_dir/roles/enroll/files/ans"
	"$base_dir/roles/enroll/tasks/main.yml"
	"$base_dir/roles/devs/tasks/main.yml"
	"$base_dir/roles/devs/vars/main.yml"
 	"$base_dir/roles/common/files/motd"
  	"$base_dir/roles/common/tasks/main.yml"
   	"$base_dir/roles/common/templates/hosts.j2"
    	"$base_dir/roles/common/vars/main.yml"
     	"$base_dir/roles/banana/tasks/main.yml"
)

# Create empty files
for file in "${files[@]}"; do
	touch "$file"
done
echo "All Files Made"
echo "Let's start configuring all the files to all the systems available"
