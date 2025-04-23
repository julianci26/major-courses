#!/bin/bash

# Develop the directory included in your playbook
base_dir="first-playbook"

# List of all directories you want to create
dirs=(
	"$base_dir"
	"$base_dir/roles"
	"$base_dir/roles/common"
	"$base_dir/roles/common/ftp"
	"$base_dir/roles/common/ftp/tasks"
	"$base_dir/roles/common/motd"
	"$base_dir/roles/common/motd/files"
	"$base_dir/roles/common/motd/tasks"
	"$base_dir/roles/activity"
	"$base_dir/roles/activity/tasks"
	"$base_dir/roles/activity/templates"
	"$base_dir/roles/activity/vars"
)

# Create all directories
for dir in "${dirs[@]}"; do
	mkdir -p "$dir"
done

# Create empty files
touch "$base_dir/hosts"
touch "$base_dir/activity.yml"
touch "$base_dir/update.yml"
touch "$base_dir/site.yml"
