
import os

from jinja2 import TemplateError

Template = r'echo -ne {} > functions/hid.usb1/report_desc'
hid_data = open(os.path.join(os.path.dirname(__file__), 'mouse.dat'), 'r').read()
hid_data = r"\\x"+ hid_data.replace(" ",r"\\x")[:-3]
hid_data = hid_data.lower()
print(Template.format(hid_data))

