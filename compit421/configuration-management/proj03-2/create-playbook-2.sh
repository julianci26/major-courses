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
)

# Create all directories
for dir in "${dirs[@]}"; do
	mkdir -p "$dir"
done

# Create empty files
touch "$base_dir/hosts"
touch "$base_dir/enroll.yml"
touch "$base_dir/roles/enroll/files/ans"
touch "$base_dir/roles/enroll/tasks/main.yml"

