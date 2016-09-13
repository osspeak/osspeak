import xml.etree.ElementTree as ET
from sprecgrammars import astree
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


    def convert(self, node):
        return self.convert_map[type(node)](node)

    def convert_grammar(self, grammar_node):
        self.root = ET.Element('grammar', attrib=self.grammar_attrib)
        ruleref_container = ET.Element('rule', attrib={'id': self.grammar_attrib['root']})
        self.root.append(ruleref_container)
        repeat_item = ET.Element('item', attrib={'repeat': '1-'})
        top_level_choices = ET.Element('one-of', attrib={})
        repeat_item.append(top_level_choices)
        ruleref_container.append(repeat_item)
        for rule_node in grammar_node.rules:
            rule = self.convert_rule(rule_node)
            self.root.append(rule)
            top_level_choices.append(self.get_ruleref_item(rule_node.id))
        return self.root

    def get_ruleref_item(self, ruleid):
        ruleref_item = ET.Element('item')
        ruleref = ET.Element('ruleref', attrib={'uri': '#{}'.format(ruleid)})
        ruleref_item.append(ruleref)
        tag = ET.Element('tag')
        tag.text = 'out.{0}=rules.{0};'.format(ruleid)
        ruleref_item.append(tag)
        return ruleref_item

    def convert_rule(self, rule_node):
        rule = ET.Element('rule', attrib={'id': rule_node.id})
        choices = ET.Element('one-of')
        rule.append(choices)
        self.fill_choices(rule_node, choices)
        pprint(ET.tostring(rule))
        return rule

    def fill_choices(self, node, choices):
        choices.append(ET.Element('item'))
        for child in node.children:
            if isinstance(child, astree.OrNode):
                choices.append(ET.Element('item'))
            elif isinstance(child, astree.WordNode):
                self.add_text_to_item_elem(choices[-1], child)
            elif isinstance(child, astree.GroupingNode):
                rule = ET.Element('rule', attrib={'id': child.id})
                child_choices = ET.Element('one-of')
                rule.append(child_choices)
                self.root.append(rule)
                rritem = self.get_ruleref_item(child.id)
                choices[-1].append(rritem)
                self.fill_choices(child, child_choices)

    def add_text_to_item_elem(self, parent_item, word_node):
        assert self.get_repeat_vals(parent_item) == (1, 1)
        text = word_node.text
        if not parent_item:
            if word_node.is_single:
                self.append_text(parent_item, word_node.text)
                return
            else:
                text = text if parent_item.text is None else '{} {}'.format(parent_item.text, text)
                parent_item.text = None
        if not parent_item or parent_item[-1].tag != 'item' or parent_item[-1] or not word_node.is_single:
            parent_item.append(ET.Element('item'))
        self.apply_repeat_attrib(parent_item[-1], word_node.repeat_low, word_node.repeat_high)
        self.append_text(parent_item[-1], text)

    def apply_repeat_attrib(self, elem, low, high):
        elem.attrib.pop('repeat', None)
        if (low, high) != (1, 1):
            elem.attrib['repeat'] = '{}-{}'.format(low, high if high else '')

    def append_text(self, elem, text):
        elem.text = text if elem.text is None else '{} {}'.format(elem.text, text)

    def get_repeat_vals(self, elem):
        repeat_str = elem.attrib.get('repeat', '1-1')
        low, high = repeat_str.split('-')
        return int(low) if low else 0, int(high) if high else None

        