DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS devices;

CREATE TABLE customers (
  customer_name TEXT CHECK(LENGTH(customer_name) >= 1) PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER update_customers_updated_at
AFTER UPDATE ON customers
BEGIN
  UPDATE customers
  SET updated_at = CURRENT_TIMESTAMP
  WHERE customer_name IN (SELECT NEW.customer_name FROM NEW);
END;

CREATE TABLE devices (
  device_id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_mac_address TEXT CHECK(LENGTH(device_mac_address) = 17) NOT NULL UNIQUE,
  device_ip_v4_address TEXT CHECK(LENGTH(device_ip_v4_address) BETWEEN 7 AND 15) NOT NULL,
  device_category TEXT CHECK(device_category IN ('ROUTER', 'SWITCH', 'BRIDGE', 'REPEATER', 'WIRELESS ACCESS POINT', 'NETWORK INTERFACE CARD', 'FIREWALL', 'HUB', 'MODEM', 'GATEWAY')) NOT NULL,
  device_status TEXT CHECK(device_status IN ('ACTIVE', 'NOT ACTIVE', 'DISABLED')) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  customer_name TEXT,
  FOREIGN KEY(customer_name) REFERENCES customers(customer_name)
);

CREATE TRIGGER update_devices_updated_at
AFTER UPDATE ON devices
BEGIN
  UPDATE devices
  SET updated_at = CURRENT_TIMESTAMP
  WHERE device_id IN (SELECT NEW.device_id FROM NEW);
END;
