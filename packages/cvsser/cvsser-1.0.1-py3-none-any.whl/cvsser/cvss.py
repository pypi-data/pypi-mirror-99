# -*- coding: utf-8 -*-

from .cvss_guide import cvss_guide

class VectorString:
    def __init__(self, vector_string=None, guide_only=False):
        self.guide = cvss_guide
        if not guide_only:
            if not vector_string:
                raise TypeError("No vector string input was provided.")
            if type(vector_string) != str:
                raise TypeError('Input is not a string.')
            if vector_string == '':
                raise TypeError('An empty string was passed to the function.')
            self._parse(vector_string)

    def _parse(self, vector_string):
        metrics = vector_string.split('/')
        met0 = metrics[0].split(':')

        # Provisionally determine the version
        if met0[0] == "CVSS":
            metrics = metrics[1:]
            if len(metrics) < 8:
                raise ValueError('String input does not include enough metrics to be a valid CVSS vector string.')
            if met0[1] == "3.0":
                prov_version = "v3.0"
            elif met0[1] == "3.1":
                prov_version = "v3.1"
            else:
                raise ValueError('Invalid CVSS version specified.')
        else:
            if len(metrics) < 6:
                raise ValueError('String input does not include enough metrics to be a valid CVSS vector string.')
            prov_version = "v2.0"

        # Create dictionary of metrics key/value pairs
        temp_di = {}
        for m in metrics:
            kv = m.split(':')
            if len(kv) != 2:
                raise ValueError('String input has at least one metric with invalid syntax.')
            if kv[0] not in temp_di:
                temp_di[kv[0]] = kv[1]
            else:
                raise ValueError('String input has at least one duplicated metric.')

        v2_required_metrics = [k for k,v in self.guide["v2.0"].items() if v["mandatory"]]
        v2_all_metrics = list(self.guide["v2.0"])
        v3_required_metrics = [k for k,v in self.guide["v3.0"].items() if v["mandatory"]]
        v3_all_metrics = list(self.guide["v3.0"])
        included_metrics = [k for k in temp_di]

        # Check that all required metrics are present:
        if prov_version == "v2.0":
            if not all(item in included_metrics for item in v2_required_metrics):
                raise ValueError(f'Not all of the mandatory metrics ({",".join(v2_required_metrics)}) are included in the vector string')
        if prov_version == "v3.0" or prov_version == "v3.1":
            if not all(item in included_metrics for item in v3_required_metrics):
                raise ValueError(f'Not all of the mandatory metrics ({",".join(v3_required_metrics)}) are included in the vector string')

        # Check that all included metrics are valid:
        if prov_version == "v2.0":
            for m in included_metrics:
                if m not in v2_all_metrics:
                    raise ValueError(f'At least one included metric ({m}) is invalid.')
        if prov_version == "v3.0" or prov_version == "v3.1":
            for m in included_metrics:
                if m not in v3_all_metrics:
                    raise ValueError(f'At least one included metric ({m}) is invalid.')

        # Check that all values are valid:
        if prov_version in ["v3.0", "v3.1"]:
            for k,v in temp_di.items():
                if v not in self.guide["v3.0"][k]["values"]:
                    raise ValueError(f'At least one metric ({k}) has an invalid value ({v}).')

        self.metrics = temp_di
        self.version = prov_version

        if self.version == "v2.0":
            self.av = self.metrics.get("AV")
            self.access_vector = self.metrics.get("AV")
            self.ac = self.metrics.get("AC")
            self.access_complexity = self.metrics.get("AC")
            self.au = self.metrics.get("Au")
            self.authentication = self.metrics.get("Au")
            self.c = self.metrics.get("C")
            self.confidentiality_impact = self.metrics.get("C")
            self.i = self.metrics.get("I")
            self.integrity_impact = self.metrics.get("I")
            self.a = self.metrics.get("A")
            self.availability_impact = self.metrics.get("A")
            self.e = self.metrics.get("E", "ND")
            self.exploitability = self.metrics.get("E","ND")
            self.rl = self.metrics.get("RL", "ND")
            self.remediation_level = self.metrics.get("RL", "ND")
            self.rc = self.metrics.get("RC", "ND")
            self.report_confidence = self.metrics.get("RC", "ND")
            self.cdp = self.metrics.get("CDP", "ND")
            self.collateral_damage_potential = self.metrics.get("CDP", "ND")
            self.td = self.metrics.get("TD", "ND")
            self.target_distribution = self.metrics.get("TD", "ND")
            self.cr = self.metrics.get("CR", "ND")
            self.confidentiality_requirement = self.metrics.get("CR", "ND")
            self.ir = self.metrics.get("IR", "ND")
            self.integrity_requirement = self.metrics.get("IR", "ND")
            self.ar = self.metrics.get("AR", "ND")
            self.availability_requirement = self.metrics.get("AR", "ND")

        if self.version in ["v3.0", "v3.1"]:
            self.av = self.metrics.get("AV")
            self.attack_vector = self.metrics.get("AV")
            self.ac = self.metrics.get("AC")
            self.attack_complexity = self.metrics.get("AC")
            self.pr = self.metrics.get("PR")
            self.privileges_required = self.metrics.get("PR")
            self.ui = self.metrics.get("UI")
            self.user_interaction = self.metrics.get("UI")
            self.s = self.metrics.get("S")
            self.scope = self.metrics.get("S")
            self.c = self.metrics.get("C")
            self.confidentiality = self.metrics.get("C")
            self.confidentiality_impact = self.metrics.get("C")
            self.i = self.metrics.get("I")
            self.integrity = self.metrics.get("I")
            self.integrity_impact = self.metrics.get("I")
            self.a = self.metrics.get("A")
            self.availability = self.metrics.get("A")
            self.availability_impact = self.metrics.get("A")
            self.e = self.metrics.get("E", "X")
            self.exploit_code_maturity = self.metrics.get("E", "X")
            self.rl = self.metrics.get("RL", "X")
            self.remediation_level = self.metrics.get("RL", "X")
            self.rc = self.metrics.get("RC", "X")
            self.report_confidence = self.metrics.get("RC", "X")
            self.cr = self.metrics.get("CR", "X")
            self.confidentiality_requirement = self.metrics.get("CR", "X")
            self.ir = self.metrics.get("IR", "X")
            self.integrity_requirement = self.metrics.get("IR", "X")
            self.ar = self.metrics.get("AR", "X")
            self.availability_requirement = self.metrics.get("AR", "X")
            self.mav = self.metrics.get("MAV", "X")
            self.modified_attack_vector = self.metrics.get("MAV", "X")
            self.mac = self.metrics.get("MAC", "X")
            self.modified_attack_complexity = self.metrics.get("MAC", "X")
            self.mpr = self.metrics.get("MPR", "X")
            self.modified_privileges_required = self.metrics.get("MPR", "X")
            self.mui = self.metrics.get("MUI", "X")
            self.modified_user_interaction = self.metrics.get("MUI", "X")
            self.ms = self.metrics.get("MS", "X")
            self.modified_scope = self.metrics.get("MS", "X")
            self.mc = self.metrics.get("MC", "X")
            self.modified_confidentiality = self.metrics.get("MC", "X")
            self.modified_confidentiality_impact = self.metrics.get("MC", "X")
            self.mi = self.metrics.get("MI", "X")
            self.modified_integrity = self.metrics.get("MI", "X")
            self.modified_integrity_impact = self.metrics.get("MI", "X")
            self.ma = self.metrics.get("MA", "X")
            self.modified_availability = self.metrics.get("MA", "X")
            self.modified_availability_impact = self.metrics.get("MA", "X")

    def to_dict(self, style='default', parentheticals='none', include='all'):
        if style == 'default':
            if parentheticals != "none":
                raise AttributeError("""The 'parentheticals' attribute is only compatible with the 'verbose' style.""")
            response = {}
            for c in self.guide[self.version]:
                response[c] = self.metrics.get(c,"X")
        elif style == 'verbose':
            response = {}
            for k,v in self.guide[self.version].items():
                if include == 'mandatory' or include == 'base':
                    if v["type"] == "Base":
                        if parentheticals == "both":
                            name = f"""{v["name"]} ({k})"""
                            if self.version in ["v3.0", "v3.1"]:
                                val = f"""{v["values"][self.metrics.get(k,"X")]} ({self.metrics.get(k,"X")})"""
                            elif self.version in ["v2.0"]:
                                val = f"""{v["values"][self.metrics.get(k, "ND")]} ({self.metrics.get(k, "ND")})"""
                        elif parentheticals == "metrics":
                            name = f"""{v["name"]} ({k})"""
                            if self.version in ["v3.0", "v3.1"]:
                                val = v["values"][self.metrics.get(k,"X")]
                            elif self.version in ["v2.0"]:
                                val = v["values"][self.metrics.get(k, "ND")]
                        elif parentheticals == "values":
                            name = v["name"]
                            if self.version in ["v3.0", "v3.1"]:
                                val = f"""{v["values"][self.metrics.get(k,"X")]} ({self.metrics.get(k,"X")})"""
                            if self.version in ["v2.0"]:
                                val = f"""{v["values"][self.metrics.get(k, "ND")]} ({self.metrics.get(k, "ND")})"""
                        elif parentheticals == "none":
                            name = v["name"]
                            if self.version in ["v3.0", "v3.1"]:
                                val = v["values"][self.metrics.get(k,"X")]
                            elif self.version in ["v2.0"]:
                                val = v["values"][self.metrics.get(k, "ND")]
                        response[name] = val
                elif include == 'all':
                    if parentheticals == "both":
                        name = f"""{v["name"]} ({k})"""
                        if self.version in ["v3.0", "v3.1"]:
                            val = f"""{v["values"][self.metrics.get(k,"X")]} ({self.metrics.get(k,"X")})"""
                        elif self.version in ["v2.0"]:
                            val = f"""{v["values"][self.metrics.get(k, "ND")]} ({self.metrics.get(k, "ND")})"""
                    elif parentheticals == "metrics":
                        name = f"""{v["name"]} ({k})"""
                        if self.version in ["v3.0", "v3.1"]:
                            val = v["values"][self.metrics.get(k,"X")]
                        elif self.version in ["v2.0"]:
                            val = v["values"][self.metrics.get(k, "ND")]
                    elif parentheticals == "values":
                        name = v["name"]
                        if self.version in ["v3.0", "v3.1"]:
                            val = f"""{v["values"][self.metrics.get(k,"X")]} ({self.metrics.get(k,"X")})"""
                        if self.version in ["v2.0"]:
                            val = f"""{v["values"][self.metrics.get(k, "ND")]} ({self.metrics.get(k, "ND")})"""
                    elif parentheticals == "none":
                        name = v["name"]
                        if self.version in ["v3.0", "v3.1"]:
                            val = v["values"][self.metrics.get(k,"X")]
                        elif self.version in ["v2.0"]:
                            val = v["values"][self.metrics.get(k, "ND")]
                response[name] = val
        return response
