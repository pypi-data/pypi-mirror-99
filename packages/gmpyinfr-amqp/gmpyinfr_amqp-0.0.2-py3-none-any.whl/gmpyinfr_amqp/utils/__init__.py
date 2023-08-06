"""
Utils
"""

import re

def read_conf_file(filepath):
    """
    Faz a leitura do arquivo de configuração.

    Arquivo deve ter a seguinte configuração:
        routingkey=<routingkey>
        user=<user>
        pwd=<pwd>
        virtualhost=<virtualhost>
        host=<host>
        port=<port>

    Por favor, mantenha esta configuração. Separe as linhas apenas por quebras.
    Linhas em branco serão ignoradas. Linhas iniciadas por # também são ignoradas.

    Params:
        - filepath : str path do arquivo de configuração da conexão

    Returns:
        tuple contendo as configurações de conexão
    """

    must = {'routingkey': str, 'user': str, 'pwd': str,
            'host': str, 'port': int, 'virtualhost': str}

    with open(filepath, 'r') as _f:
        confs = map(lambda x: x.strip(), _f.read().split('\n'))

    confs = [x for x in confs if x and not x.startswith('#')]
    if not confs:
        raise ValueError("Arquivo de configuração deve conter configurações.")

    regex = re.compile(r'^(\w+)\s*=\s*(.+)$')
    confs = {k.lower(): v for k, v in [regex.findall(c)[0] for c in confs]}
    missing = set(must.keys()) - set(confs.keys())
    if missing:  # uma config obrigatória está faltando
        raise ValueError("Arquivo de configuração não contém os campos: '{}'".format(
            "', '".join(missing)))

    # faz a conversão dos tipos
    confs = {k: must[k](v) for k, v in confs.items()}

    return confs
