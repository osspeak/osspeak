from recognition.commands import monitor

def command_modules():
    return {
    'name': 'root',
    'toggled': True,
    'children': [
        {
            'name': 'parent',
            'children': [
                { 'name': 'child1' },
                { 'name': 'child2' }
            ]
        },
        {
            'name': 'loading parent',
            'loading': True,
            'children': []
        },
        {
            'name': 'parent',
            'children': [
                {
                    'name': 'nested parent',
                    'children': [
                        { 'name': 'nested child 1' },
                        { 'name': 'nested child 2' }
                    ]
                }
            ]
        }
    ]
}