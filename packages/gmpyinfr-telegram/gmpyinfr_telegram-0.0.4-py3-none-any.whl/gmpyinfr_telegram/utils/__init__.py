"""
utils
"""

import re

def read_conf_file(filepath):
    """
    Faz a leitura do arquivo de configuração.

    Arquivo deve ter a seguinte configuração:
    	token=<token do bot do telegram>
        error=<ids a receber mensagens de erro, separados por vírgula>
        warn=<ids a receber mensagens de warn, separados por vírgula>

    Por favor, mantenha esta configuração. Separe as linhas apenas por quebras.
    Linhas em branco serão ignoradas. Linhas iniciadas por # também são ignoradas.

    Params:
        - filepath : str path do arquivo de configuração do bot

    Returns:
        tuple contendo as configurações do bot
    """

    must = set(['token', 'error', 'warn'])
    special_parse = ['error', 'warn']
    parse = lambda x: list(map(int, x.split(',')))

    with open(filepath, 'r') as _f:
        confs = map(lambda x: x.strip(), _f.read().split('\n'))

    confs = [x for x in confs if x and not x.startswith('#')]
    if not confs:
        raise ValueError("Arquivo de configuração deve conter configurações.")

    regex = re.compile(r'^(\w+)\s*=\s*(.+)$')
    confs = {k.lower(): v for k, v in [regex.findall(c)[0] for c in confs]}
    missing = must - set(confs.keys())
    if missing:  # uma config óbrigatória está faltando
        raise ValueError("Arquivo de configuração não contém os campos: '{}'".format(
            "', '".join(missing)))

    for c in special_parse:
    	confs[c] = parse(confs[c])

    return confs
