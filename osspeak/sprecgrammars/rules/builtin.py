rules = {
    '_any': any_rule
}

def any_rule(*a):
    return '<ruleref uri="grammar:dictation" type="application/srgs+xml"/><tag>out.SpokenText=rules.latest();</tag>'
