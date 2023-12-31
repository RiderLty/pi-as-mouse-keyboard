#!/bin/bash
# this is a stripped down version of https://github.com/ckuethe/usbarmory/wiki/USB-Gadgets - I don't claim any rights

modprobe libcomposite


cd /sys/kernel/config/usb_gadget/
mkdir -p g1
cd g1
echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2.0

echo 0xEF > bDeviceClass
echo 0x02 > bDeviceSubClass
echo 0x01 > bDeviceProtocol

mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "MF" > strings/0x409/manufacturer
echo "POD" > strings/0x409/product

mkdir -p configs/c.1

mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 6 > functions/hid.usb0/report_length
echo -ne \\x05\\x01\\x09\\x05\\xa1\\x01\\x85\\x01\\x09\\x30\\x09\\x31\\x09\\x32\\x09\\x35\\x09\\x33\\x09\\x34\\x15\\x00\\x26\\xff\\x00\\x75\\x08\\x95\\x06\\x81\\x02\\x06\\x00\\xff\\x09\\x20\\x95\\x01\\x81\\x02\\x05\\x01\\x09\\x39\\x15\\x00\\x25\\x07\\x35\\x00\\x46\\x3b\\x01\\x65\\x14\\x75\\x04\\x95\\x01\\x81\\x42\\x65\\x00\\x05\\x09\\x19\\x01\\x29\\x0f\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x0f\\x81\\x02\\x06\\x00\\xff\\x09\\x21\\x95\\x0d\\x81\\x02\\x06\\x00\\xff\\x09\\x22\\x15\\x00\\x26\\xff\\x00\\x75\\x08\\x95\\x34\\x81\\x02\\x85\\x02\\x09\\x23\\x95\\x2f\\x91\\x02\\x85\\x05\\x09\\x33\\x95\\x28\\xb1\\x02\\x85\\x08\\x09\\x34\\x95\\x2f\\xb1\\x02\\x85\\x09\\x09\\x24\\x95\\x13\\xb1\\x02\\x85\\x0a\\x09\\x25\\x95\\x1a\\xb1\\x02\\x85\\x20\\x09\\x26\\x95\\x3f\\xb1\\x02\\x85\\x21\\x09\\x27\\x95\\x04\\xb1\\x02\\x85\\x22\\x09\\x40\\x95\\x3f\\xb1\\x02\\x85\\x80\\x09\\x28\\x95\\x3f\\xb1\\x02\\x85\\x81\\x09\\x29\\x95\\x3f\\xb1\\x02\\x85\\x82\\x09\\x2a\\x95\\x09\\xb1\\x02\\x85\\x83\\x09\\x2b\\x95\\x3f\\xb1\\x02\\x85\\x84\\x09\\x2c\\x95\\x3f\\xb1\\x02\\x85\\x85\\x09\\x2d\\x95\\x02\\xb1\\x02\\x85\\xa0\\x09\\x2e\\x95\\x01\\xb1\\x02\\x85\\xe0\\x09\\x2f\\x95\\x3f\\xb1\\x02\\x85\\xf0\\x09\\x30\\x95\\x3f\\xb1\\x02\\x85\\xf1\\x09\\x31\\x95\\x3f\\xb1\\x02\\x85\\xf2\\x09\\x32\\x95\\x0f\\xb1\\x02\\x85\\xf4\\x09\\x35\\x95\\x3f\\xb1\\x02\\x85\\xf5\\x09\\x36\\x95\\x03\\xb1\\x02\\xc0 > functions/hid.usb0/report_desc
ln -s functions/hid.usb0 configs/c.1/

echo 1       > os_desc/use
echo 0xcd    > os_desc/b_vendor_code
echo MSFT100 > os_desc/qw_sign
ln -s configs/c.1 os_desc

mkdir -p configs/c.1/strings/0x409
echo "Config 1: DS5" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower
ls /sys/class/udc > UDC
