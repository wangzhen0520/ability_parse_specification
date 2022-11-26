# -*- encoding: utf-8 -*-
import os
import xml.etree.ElementTree as ET


class IntellAbility():
    def __init__(self, path):
        self.unique_id = 1
        self.chainAttrInfoList = {}
        self.intellInfoList = {}
        self.ytnInfo = {}
        self.path = path

    def walk_data(self, root_node, tag, level, result_list):
        temp_list = [self.unique_id, level, tag, root_node.tag, root_node.attrib]
        result_list.append(temp_list)

        # print temp_list
        if tag == 'ChainAttrInfo' and level == 4:
            self.chainAttrInfoList[root_node.tag] = root_node.attrib
        if tag == 'IntelligentInfo' and level == 3:
            self.intellInfoList[root_node.tag] = root_node.attrib
        if tag == 'ITGT_SUPPORT_MODE_LIST' and level == 4:
            # print root_node.tag, root_node.text
            if root_node.tag not in self.intellInfoList[tag]:
                self.intellInfoList[tag][root_node.tag] = []
            self.intellInfoList[tag][root_node.tag].append(root_node.text)
        if tag == 'message' and root_node.tag == 'YTNInfo' and level == 2:
            self.ytnInfo[root_node.tag] = root_node.attrib

        self.unique_id += 1
        # 遍历每个子节点
        children_node = root_node.getchildren()
        if len(children_node) == 0:
            return
        for child in children_node:
            self.walk_data(child, root_node.tag, level + 1, result_list)
        return

    def get_xml_data(self, root):
        level = 1  # 节点的深度从1开始
        result_list = []
        self.walk_data(root, root.tag, level, result_list)
        return result_list

    def format_all_ability(self):
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filepath in filenames:
                if filepath != 'ability.xml':
                    continue
                ab_file = os.path.join(dirpath, filepath)
                print "parse ability path:", ab_file
                root = ET.parse(ab_file).getroot()
                self.get_xml_data(root)

    def get_chain_attr_info_list(self):
        return self.chainAttrInfoList

    def get_intell_info_list(self):
        return self.intellInfoList

    def get_ytn_info(self):
        return self.ytnInfo