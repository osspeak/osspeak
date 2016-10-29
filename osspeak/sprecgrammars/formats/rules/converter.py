import xml.etree.ElementTree as ET
from sprecgrammars.formats.rules import astree
import uuid
from pprint import pprint

class SrgsXmlConverter:

    def __init__(self):
        self.convert_map = {
            astree.Rule: self.convert_rule,
            astree.GrammarNode: self.convert_grammar,
            # astree.OrNode: self.convert_or_node,
            # astree.WordNode: self.convert_word_node,
        }
        self.grammar_attrib = {
            'version': '1.0',
            'mode': 'voice',
            'xmlns': 'http://www.w3.org/2001/06/grammar',
            'xml:lang': 'en-US',
            'root': 'r' + str(uuid.uuid4()).replace('-', ''),
            'tag-format': 'semantics/1.0'
        }
        self.root = ET.Element('grammar', attrib=self.grammar_attrib)
        self.ruleref_container_id = 'r' + str(uuid.uuid4()).replace('-', '')

    def convert(self, node):
        return self.convert_map[type(node)](node)

    def convert_grammar(self, grammar_node):
        self.root = ET.Element('grammar', attrib=self.grammar_attrib)
        self.build_root_rule()
        top_level_choices = self.build_top_level_choices()
        for rule_node in grammar_node.rules:
            self.append_rule_node(rule_node, top_level_choices)
        for rule_node in (var.rule for var in grammar_node.variables):
            self.append_rule_node(rule_node, top_level_choices)
        return self.root

    def append_rule_node(self, rule_node, top_level_choices):
        rule = self.convert_rule(rule_node)
        self.root.append(rule)
        if not rule_node.is_variable:
            tag_text = 'out += "-command-{}:" + rules.latest();'.format(rule_node.id)
            top_level_choices.append(self.get_ruleref_item(rule_node.id, text=tag_text))

    def build_root_rule(self):
        root_rule = ET.Element('rule', attrib={'id': self.grammar_attrib['root']})
        self.root.append(root_rule)
        item = ET.Element('item')
        item.append(self.get_ruleref_item(self.ruleref_container_id, text='out += rules.latest();'))
        root_rule.append(item)

    def build_top_level_choices(self):
        ruleref_container = ET.Element('rule', attrib={'id': self.ruleref_container_id})
        self.root.append(ruleref_container)
        repeat_item = ET.Element('item', attrib={'repeat': '1-'})
        top_level_choices = ET.Element('one-of', attrib={})
        repeat_item.append(top_level_choices)
        ruleref_container.append(repeat_item)
        return top_level_choices
    
    def get_ruleref_item(self, ruleid, text=None, low=1, high=1):
        ruleref_item = ET.Element('item')
        ruleref = ET.Element('ruleref', attrib={'uri': '#{}'.format(ruleid)})
        self.apply_repeat_attrib(ruleref_item, low, high)
        ruleref_item.append(ruleref)
        tag = ET.Element('tag')
        tag.text = 'out += "{}=|" + rules.latest();'.format(ruleid) if text is None else text
        ruleref_item.append(tag)
        return ruleref_item

    def convert_rule(self, rule_node):
        rule = ET.Element('rule', attrib={'id': rule_node.id})
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
            elif isinstance(child, astree.VariableNode):
                text = 'out += "{}=|" + rules.latest();'.format(child.rule.id)
                rritem = self.get_ruleref_item(child.rule.id, text=None, low=child.repeat_low, high=child.repeat_high)
                choices[-1].append(rritem)

    def add_grouping(self, child, choices):
        rule = ET.Element('rule', attrib={'id': child.id})
        self.root.append(rule)
        child_choices = ET.Element('one-of')
        rule.append(child_choices)
        rritem = self.get_ruleref_item(child.id, low=child.repeat_low, high=child.repeat_high)
        choices[-1].append(rritem)
        self.fill_choices(child, child_choices)

    def add_substitute_word(self, child, choices):
        rule = ET.Element('rule', attrib={'id': child.id})
        self.root.append(rule)
        word_item = ET.Element('item')
        word_item.text = child.text
        rule.append(word_item)
        text = 'out += "{}=" + rules.latest() + "|";'.format(child.id)
        rritem = self.get_ruleref_item(child.id, text=text)
        choices[-1].append(rritem)

    def add_text_to_item_elem(self, parent_elem, word_node, parent_node):
        assert self.get_repeat_vals(parent_elem) == (1, 1)
        text = word_node.text
        if (not parent_elem or parent_elem[-1].tag != 'item' or
        (parent_elem[-1] and parent_elem[-1].find('ruleref') is not None) or
        not word_node.is_single):
            parent_elem.append(ET.Element('item'))
            if not isinstance(parent_node, astree.Rule):
                parent_elem[-1].append(ET.Element('tag'))
        self.apply_repeat_attrib(parent_elem[-1], word_node.repeat_low, word_node.repeat_high)
        self.append_text(parent_elem[-1], text)
        if not isinstance(parent_node, astree.Rule):
            text_tag = parent_elem[-1].find('tag')
            text_tag.text = 'out += "literal-{}={}|";'.format(parent_node.id, parent_elem[-1].text)

    def apply_repeat_attrib(self, elem, low, high, low_default=0, high_default=99):
        print('foo', elem, low, high)
        elem.attrib.pop('repeat', None)
        low = low_default if low is None else low
        high = high_default if high is None else high
        if (low, high) != (1, 1):
            elem.attrib['repeat'] = '{}-{}'.format(low, high)

    def append_text(self, elem, text):
        elem.text = text if elem.text is None else '{} {}'.format(elem.text, text)

    def get_repeat_vals(self, elem):
        repeat_str = elem.attrib.get('repeat', '1-1')
        low, high = repeat_str.split('-')
        return int(low) if low else 0, int(high) if high else None

        