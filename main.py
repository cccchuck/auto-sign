from utils import Log, InSchool

import json


log = Log()


def invoke(accounts):
    for account in accounts:
        inschool = InSchool(account, log)
        JWSESSION = inschool.getJwsession()
        if JWSESSION:
            account['JWSESSION'] = JWSESSION

    return accounts


def main():
    with open('./conf.json', 'r') as f:
        config = json.load(f)
        accounts = config['accounts']

    config['accounts'] = invoke(accounts)

    with open('./conf.json', 'w') as f:
        json.dump(config, f, ensure_ascii=False)

    log.save()
    return None


main()
