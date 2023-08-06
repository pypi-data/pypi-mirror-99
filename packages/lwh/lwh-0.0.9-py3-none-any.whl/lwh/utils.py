import sys
from lwh.report.report import template_string



def get_template(template_arg: str):

    if template_arg is None:
        return template_string
    else:
        with open(template_arg, 'r') as file:
            return file.read()