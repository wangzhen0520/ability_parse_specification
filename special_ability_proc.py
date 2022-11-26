# -*- coding: utf-8 -*-

from config import ITGT_SUPPORT_MODE_LIST


class SpecialProc:
    def __init__(self, spec_ability, device_type, attr_key, attr_value):
        self.ability = spec_ability
        self.device_type = device_type
        self.attr_key = attr_key
        self.attr_value = attr_value

    def proc_num(self):
        self.ability.write_cell(self.device_type, self.attr_key, int(self.attr_value['num']) if (self.attr_value is not None and 'num' in self.attr_value) else u'不支持')

    def proc_size(self):
        value = int(self.attr_value['size'].strip(u'\u202c')) if (self.attr_value is not None and 'size' in self.attr_value) else u'不支持'
        # print "size: ", value, self.attr_value
        self.ability.write_cell(self.device_type, self.attr_key, value)

    def proc_min_max(self):
        value_min = self.attr_value['Min'] if (self.attr_value is not None and 'Min' in self.attr_value) else '0'
        value_max = self.attr_value['Max'] if (self.attr_value is not None and 'Max' in self.attr_value) else '0'
        value = u'不支持' if (value_min == '0' and value_max == '0') else (value_min + '~' + value_max)
        self.ability.write_cell(self.device_type, self.attr_key, value)

    def proc_SingPicNumLimit(self):
        value = self.attr_value['Enable'] if (self.attr_value is not None and 'Enable' in self.attr_value) else '0'
        self.ability.write_cell(self.device_type, self.attr_key, u'支持' if value == '1' else u'不支持')

    def proc_ITGT_SUPPORT_MODE_LIST(self):
        value = ''
        if self.attr_value is not None and 'mode' in self.attr_value:
            for item in self.attr_value['mode']:
                value += item + ': ' + ITGT_SUPPORT_MODE_LIST[item] + '\r'
        self.ability.write_cell(self.device_type, self.attr_key, u'不支持' if value == '' else value)

    def procYTNInfo(self):
        value = self.attr_value['Resolution'] if (self.attr_value is not None and 'Resolution' in self.attr_value) else '0'
        self.ability.write_cell(self.device_type, self.attr_key, int(value) if value != '0' else u'不支持')