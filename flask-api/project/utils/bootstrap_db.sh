#!/bin/bash

# Function to send a POST request to create a customer
create_customer() {
	customer_name="$1"
	echo "Base URL: $base_url"
	curl -X POST -H "Content-Type: application/json" -d "{\"customer_name\":\"$customer_name\"}" "$base_url/customers"
}

# Function to send a POST request to create a device
create_device() {
	customer_name="$1"
	mac_address="$2"
	ip_address="$3"
	device_category="$4"
	device_status="$5"
	echo "$customer_name"
	echo "$mac_address"
	echo "$ip_address"
	echo "$device_category"
	echo "$device_status"
	curl -X POST -H "Content-Type: application/json" -d "{\"device_mac_address\":\"$mac_address\",\"device_ip_v4_address\":\"$ip_address\",\"device_category\":\"$device_category\",\"device_status\":\"$device_status\",\"customer_name\":\"$customer_name\"}" "$base_url/devices"
}

# Parse command-line arguments
if [[ $# -lt 1 ]]; then
	echo "Usage: $0 <customer_name>"
	exit 1
fi

customer_name="$1"

# Base URL of the API
base_url="http://127.0.0.1:5000"

# Create the customer
create_customer "$customer_name"

# Array of device categories
device_categories=("ROUTER" "SWITCH" "BRIDGE" "REPEATER" "WIRELESS ACCESS POINT" "NETWORK INTERFACE CARD" "FIREWALL" "HUB" "MODEM" "GATEWAY")

# Array of device statuses
device_statuses=("ACTIVE" "NOT ACTIVE" "DISABLED")

# Populate devices for the customer
for device_category in "${device_categories[@]}"; do
	for device_status in "${device_statuses[@]}"; do
		# Generate a unique MAC address for each device
		mac_address=$(hexdump -n6 -e '6/1 ":%02x"' /dev/urandom | awk ' { sub(/^:../, "02"); print } ')

		# Generate a unique IP address for each device
		ip_address=$(printf %d.%d.%d.%d $((RANDOM % 255 + 1)) $((RANDOM % 256)){,,})

		create_device "$customer_name" "$mac_address" "$ip_address" "$device_category" "$device_status"
	done
done
