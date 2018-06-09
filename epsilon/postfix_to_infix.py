import os, sys, logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(os.path.basename(__file__))

def postfixToInfix(s):
    vars = []
    infix = ''
    for char in s:
        s = s[1:]
        if char in ('+', '-'):
            if len(vars) >= 2:
                infix0 = vars[0][0]
                infix1 = vars[1][0]

                infix = infix1 + char + infix0
                vars = vars[2:] # remove used variables
                vars.insert(0, [infix, char])
            else:
                return 'invalid'

            logger.debug(infix)
            if len(vars) == 1 and len(s) == 0:
                return infix
        elif char == '*':
            if len(vars) >= 2:
                infix0 = vars[0]
                infix1 = vars[1]

                if len(infix0) > 1:
                    last_op = infix0[1]
                    if last_op in ('+', '-'):
                        infix0 = '(' + infix0[0] + ')'
                else:
                    infix0 = infix0[0]

                if len(infix1) > 1:
                    last_op = infix1[1]
                    if last_op in ('+', '-'):
                        infix1 = '(' + infix1[0] + ')'
                else:
                    infix1 = infix1[0]

                infix = infix1 + char + infix0
                vars = vars[2:] # remove used variables
                vars.insert(0, [infix, char])
            else:
                return 'invalid'

            logger.debug(infix)
            if len(vars) == 1 and len(s) == 0:
                return infix
        elif char.isalpha():
            # if it is a letter, it is regarded as a variable
            vars.insert(0, [char])
            logger.debug(vars)
        else:
            return 'invalid'

    return 'invalid'

if __name__ == '__main__':
    #logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)

    s = 'ab+c*'
    logger.info(s)
    logger.info('Returned: %s',  postfixToInfix(s))

    logger.info('======================')
    s = 'abc*+'
    logger.info(s)
    logger.info('Returned: %s',  postfixToInfix(s))

    logger.info('======================')
    s = 'abc+*'
    logger.info(s)
    logger.info('Returned: %s',  postfixToInfix(s))

    logger.info('======================')
    s = 'abc++*'
    logger.info(s)
    logger.info('Returned: %s',  postfixToInfix(s))

    logger.info('======================')
    s = 'abc+dx+*-'
    logger.info(s)
    logger.info('Returned: %s',  postfixToInfix(s))

    logger.info('======================')
    s = 'abc/+*'
    logger.info(s)
    logger.info('Returned: %s',  postfixToInfix(s))

    logger.info('======================')
    s = 'ab*c-'
    logger.info(s)
    logger.info('Returned: %s',  postfixToInfix(s))

    logger.info('======================')
    s = 'ab*c-ab+*'
    logger.info(s)
    logger.info('Returned: %s',  postfixToInfix(s))
