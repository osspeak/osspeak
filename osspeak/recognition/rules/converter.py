import xml.etree.ElementTree as ET
from recognition.rules import astree
from pprint import pprint

class SrgsXmlConverter:

    def __init__(self, node_ids):
        self.grammar_attrib = {
            'version': '1.0',
            'mode': 'voice',
            'xmlns': 'http://www.w3.org/2001/06/grammar',
            'xml:lang': 'en-US',
            'root': 'root',
            'tag-format': 'semantics/1.0'
        }
        self.node_ids = node_ids
        self.root = ET.Element('grammar', attrib=self.grammar_attrib)
        self.ruleref_container_id = 'ruleref_container'

    def build_grammar(self, rules):
        self.root = ET.Element('grammar', attrib=self.grammar_attrib)
        self.root.append(self.build_root_rule())
        top_level_choices = self.build_top_level_choices()
        for rule_node in rules:
            self.append_rule_node(rule_node, top_level_choices)
        return self.root

    def append_rule_node(self, rule_node, top_level_choices):
        rule = self.convert_rule_element(rule_node)
        self.root.append(rule)
        if rule_node.name is None:
            tag_text = f'out += "-command-{self.node_ids[rule_node]}:" + rules.latest();'
            top_level_choices.append(self.get_ruleref_item(self.node_ids[rule_node], text=tag_text))

    def build_root_rule(self):
        root_rule = ET.Element('rule', attrib={'id': self.grammar_attrib['root']})
        item = ET.Element('item')
        item.append(self.get_ruleref_item(self.ruleref_container_id, text='out += rules.latest();'))
        root_rule.append(item)
        return root_rule

    def build_top_level_choices(self):
        ruleref_container = ET.Element('rule', attrib={'id': self.ruleref_container_id})
        self.root.append(ruleref_container)
        repeat_item = ET.Element('item', attrib={'repeat': '1-'})
        top_level_choices = ET.Element('one-of', attrib={})
        repeat_item.append(top_level_choices)
        ruleref_container.append(repeat_item)
        return top_level_choices
    
    def get_ruleref_item(self, ruleid, outid=None, text=None, low=1, high=1):
        outid = ruleid if outid is None else outid
        ruleref_item = ET.Element('item')
        ruleref = ET.Element('ruleref', attrib={'uri': f'#{ruleid}'})
        self.apply_repeat_attrib(ruleref_item, low, high)
        ruleref_item.append(ruleref)
        tag = ET.Element('tag')
        tag.text = f'out += "{outid}=|" + rules.latest();' if text is None else text
        ruleref_item.append(tag)
        return ruleref_item

    def convert_rule_element(self, rule_node):
        rule = ET.Element('rule', attrib={'id': self.node_ids[rule_node]})
        choices = ET.Element('one-of')
        rule.append(choices)
        self.fill_choices(rule_node, choices)
        return rule

    def fill_choices(self, node, choices):
        choices.append(ET.Element('item'))
        for child in node.children:
            if isinstance(child, astree.OrNode):
                choices.append(ET.Element('item'))
            elif isinstance(child, astree.WordNode):
                if child.action_substitute is not None:
                    self.add_substitute_word(child, choices)
                else:
                    self.add_text_to_item_elem(choices[-1], child, node)
            elif isinstance(child, astree.GroupingNode):
                self.add_grouping(child, choices)
            elif isinstance(child, astree.Rule):
                self.add_rule(child, choices)
            else:
                raise TypeError(f'Unable to serialize element {child}')

    def add_rule_reference(self, ruleref_node, choices):
        if ruleref_node.rule_name == '_dictate':
            # '<ruleref uri="grammar:dictation" type="application/srgs+xml"/><tag>out.SpokenText=rules.latest();</tag>'
            ruleref = ET.Element('ruleref', attrib={'uri': 'grammar:dictation', 'type': 'application/srgs+xml'})
            choices[-1].append(ruleref)
            tag = ET.Element('tag')
            tag.text = f'out += "dictation-{self.node_ids[ruleref_node]}=" + rules.latest(); + "|"'
            choices[-1].append(tag)
            return
        # all rule nodes here should be copies that refer to base rule
        base_rule = self.rule_id_map[ruleref_node.rule_name]
        rritem = self.get_ruleref_item(self.node_ids[base_rule], outid=self.node_ids[ruleref_node], text=None,
                low=ruleref_node.repeat_low, high=ruleref_node.repeat_high)
        choices[-1].append(rritem)

    def add_rule(self, rule_node, choices):
        if rule_node.name == '_dictate':
            # '<ruleref uri="grammar:dictation" type="application/srgs+xml"/><tag>out.SpokenText=rules.latest();</tag>'
            ruleref = ET.Element('ruleref', attrib={'uri': 'grammar:dictation', 'type': 'application/srgs+xml'})
            choices[-1].append(ruleref)
            tag = ET.Element('tag')
            tag.text = f'out += "dictation-{self.node_ids[rule_node]}=" + rules.latest(); + "|"'
            choices[-1].append(tag)
            return
        # all rule nodes here should be copies that refer to base rule
        rritem = self.get_ruleref_item(self.node_ids[rule_node.base_rule], outid=self.node_ids[rule_node], text=None,
                low=rule_node.repeat_low, high=rule_node.repeat_high)
        choices[-1].append(rritem)
        
    def add_grouping(self, child, choices):
        rule = ET.Element('rule', attrib={'id': self.node_ids[child]})
        self.root.append(rule)
        child_choices = ET.Element('one-of')
        rule.append(child_choices)
        rritem = self.get_ruleref_item(self.node_ids[child], low=child.repeat_low, high=child.repeat_high)
        choices[-1].append(rritem)
        self.fill_choices(child, child_choices)

    def add_substitute_word(self, child, choices):
        rule = ET.Element('rule', attrib={'id': self.node_ids[child]})
        self.root.append(rule)
        word_item = ET.Element('item')
        word_item.text = child.text
        rule.append(word_item)
        text = f'out += "{self.node_ids[child]}=" + rules.latest() + "|";'
        rritem = self.get_ruleref_item(self.node_ids[child], text=text)
        choices[-1].append(rritem)

    def add_text_to_item_elem(self, parent_elem, word_node, parent_node):
        assert self.get_repeat_vals(parent_elem) == (1, 1)
        text = word_node.text
        if (not parent_elem or parent_elem[-1].tag != 'item' or
        (parent_elem[-1] and parent_elem[-1].find('ruleref') is not None) or
        not word_node.is_single):
            parent_elem.append(ET.Element('item'))
            if self.is_not_named_rule(parent_node):
                parent_elem[-1].append(ET.Element('tag'))
        self.apply_repeat_attrib(parent_elem[-1], word_node.repeat_low, word_node.repeat_high)
        self.append_text(parent_elem[-1], text)
        if self.is_not_named_rule(parent_node):
            text_tag = parent_elem[-1].find('tag')
            # text_tag.text = f'out += "literal-{parent_node.id}={parent_elem[-1].text}|";'
            text_tag.text = f'out += "{self.node_ids[word_node]}={parent_elem[-1].text}|";'

    def is_not_named_rule(self, node):
        return not isinstance(node, astree.Rule) or node.name is None

    def apply_repeat_attrib(self, elem, low, high):
        elem.attrib.pop('repeat', None)
        if (low, high) != (1, 1):
            elem.attrib['repeat'] = f'{low or 0}-{high or 99}'

    def append_text(self, elem, text):
        elem.text = text if elem.text is None else f'{elem.text} {text}'

    def get_repeat_vals(self, elem):
        repeat_str = elem.attrib.get('repeat', '1-1')
        low, high = repeat_str.split('-')
        return int(low) if low else 0, int(high) if high else None

    