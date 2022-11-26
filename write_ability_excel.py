# -*- encoding: utf-8 -*-
import os
from operator import methodcaller
from config import Chain_Attr_Info, Intell_Info, YTN_Info
from special_ability_proc import SpecialProc
from intell_ability_config import IntellAbility
from specification_ability import SpecAbility

all_model_config_path = 'D:/code/HoloSens_SDC/os/board/config/all_model_config'

if __name__ == "__main__":
    speAbility = SpecAbility()
    device_list = speAbility.get_device_list()

    exists_dir_list = []
    all_mode_device_list = []
    for type_name in device_list:
        # print "type: ", type_name
        type_dir = os.path.join(all_model_config_path, type_name)
        all_mode_device_list.append(type_name)
        if os.path.exists(type_dir):
            exists_dir_list.append(type_dir)

    print "all device size:", len(all_mode_device_list), "support device size:", len(exists_dir_list)
    for item in all_mode_device_list:
        device_type = item
        real_type_name = item.split('(B')[0]
        dir_path = os.path.join(all_model_config_path, real_type_name)
        print "dir path:", dir_path, device_type

        ability = IntellAbility(dir_path)
        ability.format_all_ability()
        chain_attr_info_list = ability.get_chain_attr_info_list()
        intell_info_list = ability.get_intell_info_list()
        ytn_info = ability.get_ytn_info()

        for i in Chain_Attr_Info.keys():
            name = Chain_Attr_Info[i]['name']
            func = Chain_Attr_Info[i]['func']
            attr_value = chain_attr_info_list.get(name)
            if len(func) > 0:
                spec_proc = SpecialProc(speAbility, device_type, i, attr_value)
                methodcaller(func)(spec_proc)
            else:
                value = attr_value['Enable'] if (attr_value is not None and 'Enable' in attr_value) else '0'
                value = u'支持' if value == '1' else u'不支持'
                speAbility.write_cell(device_type, i, value)

        for i in Intell_Info.keys():
            name = Intell_Info[i]['name']
            func = Intell_Info[i]['func']
            attr_value = intell_info_list.get(name)
            if len(func) > 0:
                spec_proc = SpecialProc(speAbility, device_type, i, attr_value)
                methodcaller(func)(spec_proc)

        for i in YTN_Info.keys():
            name = YTN_Info[i]['name']
            func = YTN_Info[i]['func']
            attr_value = ytn_info.get(name)
            if len(func) > 0:
                spec_proc = SpecialProc(speAbility, device_type, i, attr_value)
                methodcaller(func)(spec_proc)

    speAbility.close()
