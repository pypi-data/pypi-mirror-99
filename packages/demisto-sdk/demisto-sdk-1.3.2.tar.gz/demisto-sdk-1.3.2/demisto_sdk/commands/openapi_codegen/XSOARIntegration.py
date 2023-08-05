import json
from typing import Optional

import yaml


class XSOARIntegration:
    def __init__(self, commonfields, name, display, category, description, configuration, script):
        self.commonfields = commonfields
        self.name = name
        self.display = display
        self.category = category
        self.description = description
        self.configuration = configuration
        self.script = script

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def to_yaml(self) -> dict:
        return yaml.safe_load(self.to_json())

    @classmethod
    def get_base_integration(cls):
        commonfields = XSOARIntegration.CommonFields('GeneratedIntegration', -1)
        name = 'GeneratedIntegration'
        display = 'GeneratedIntegration'
        category = 'Utilities'
        description = 'This integration was auto generated by the Cortex XSOAR SDK.'

        configurations = [
            XSOARIntegration.Configuration(display='Fetch incidents',
                                           name='isFetch',
                                           type_=8,
                                           required=False),
            XSOARIntegration.Configuration(display='Incident type',
                                           name='incidentType',
                                           type_=13,
                                           required=False),
            XSOARIntegration.Configuration(display='Maximum number of incidents per fetch',
                                           name='max_fetch',
                                           defaultvalue='10',
                                           type_=0,
                                           required=False),
            XSOARIntegration.Configuration(display='API Key',
                                           name='apikey',
                                           type_=4,
                                           required=True),
            XSOARIntegration.Configuration(display='Score threshold for ip reputation command (0-100)',
                                           name='threshold_ip',
                                           defaultvalue='65',
                                           type_=0,
                                           required=False),
            XSOARIntegration.Configuration(display='Score threshold for domain reputation command (0-100)',
                                           name='threshold_domain',
                                           defaultvalue='65',
                                           type_=0,
                                           required=False),
            XSOARIntegration.Configuration(display='Fetch alerts with status (ACTIVE, CLOSED)',
                                           name='alert_status',
                                           defaultvalue='ACTIVE',
                                           type_=15,
                                           required=False,
                                           options=['ACTIVE', 'CLOSED']),
            XSOARIntegration.Configuration(display='Fetch alerts with type',
                                           name='alert_type',
                                           type_=0,
                                           required=False),
            XSOARIntegration.Configuration(display='Minimum severity of alerts to fetch',
                                           name='min_severity',
                                           defaultvalue='Low',
                                           type_=15,
                                           required=True,
                                           options=['Low', 'Medium', 'High', 'Critical']),
            XSOARIntegration.Configuration(display='Trust any certificate (not secure)',
                                           name='insecure',
                                           type_=8,
                                           required=False),
            XSOARIntegration.Configuration(display='Use system proxy settings',
                                           name='proxy',
                                           type_=8,
                                           required=False)]

        script = XSOARIntegration.Script('', 'python', 'python3', 'demisto/python3:3.8.3.9324', True, None)

        return cls(commonfields, name, display, category, description, configurations,
                   script)

    class CommonFields:
        def __init__(self, id_: str, version: int = -1):
            self.id = id_
            self.version = version

    class Configuration:
        def __init__(self, name: str, display: str, type_: int, required: bool, defaultvalue: str = '',
                     options: Optional[list] = None):
            self.name = name
            self.display = display
            self.defaultvalue = defaultvalue
            self.type = type_
            self.required = required
            if options:
                self.options = options
            if defaultvalue:
                self.defaultvalue = defaultvalue

    class Script:
        def __init__(self, script: str, type_: str, subtype: str, dockerimage: str, isfetch: bool,
                     commands: list = None):
            self.script = script
            self.type = type_
            self.subtype = subtype
            self.dockerimage = dockerimage
            self.isfetch = isfetch
            if commands:
                self.commands = commands

        class Command:
            def __init__(self, name: str, description: str, arguments: Optional[list] = None,
                         outputs: Optional[list] = None):
                self.name = name
                self.description = description
                if arguments:
                    self.arguments = arguments
                if outputs:
                    self.outputs = outputs

            class Argument:
                def __init__(self, name: str, description: str, required: bool, auto: Optional[str] = None,
                             predefined: Optional[str] = None, is_array: bool = False):
                    self.name = name
                    self.description = description
                    self.required = required
                    self.isArray = is_array
                    if auto:
                        self.auto = auto
                    if predefined:
                        self.predefined = predefined

            class Output:
                def __init__(self, type_: str, context_path: str, description: str):
                    self.type = type_
                    self.contextPath = context_path
                    self.description = description
