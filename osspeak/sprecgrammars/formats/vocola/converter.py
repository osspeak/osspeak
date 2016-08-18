import xml.etree.ElementTree as ET
from osspeak.sprecgrammars import astree
import uuid

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

    def convert(self, node):
        return self.convert_map[type(node)](node)

    def convert_grammar(self, grammar_node):
        root = ET.Element('grammar', attrib=self.grammar_attrib)
        ruleref_container = ET.Element('rule', attrib={'id': self.grammar_attrib['root']})
        root.append(ruleref_container)
        choices = ET.Element('one-of')
        ruleref_container.append(choices)
        for rule_node in grammar_node.rules:
            rule = self.convert_rule(rule_node)
            root.append(rule)
            ruleref_item = ET.Element('item')
            ruleref = ET.Element('ruleref', attrib={'uri': '#{}'.format(rule_node.id)})
            ruleref_item.append(ruleref)
            choices.append(ruleref_item)
        return root

    def convert_rule(self, node):
        rule = ET.Element('rule', attrib={'id': node.id})
        choices = ET.Element('one-of')
        rule.append(choices)
        choices.append(ET.Element('item'))
        for child in node.children:
            if isinstance(child, astree.OrNode):
                choices.append(ET.Element('item'))
            elif isinstance(child, astree.WordNode):
                choices[-1].text = child.text if choices[-1].text is None else '{} {}'.format(choices[-1].text, child.text)
        return rule