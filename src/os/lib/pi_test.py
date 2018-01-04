from fona import get_output
from fona_commands import get_model

import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(module)s::%(funcName)s: '
        '%(message)s', datefmt='%Y-%m-%d %H:%M:%S %Z')
    logger = logging.getLogger(__name__)

    logger.info('FONA DEVICE REMOVAL TEST: send model name command, save '
        'output, remove FONA device, send model name command, observe '
        'differences in output')

    logger.info('Setup FONA device; press ENTER when ready to begin test')
    input_string = raw_input()

    logger.info('FONA output:\n%s' % get_model())
    logger.info('Command sent SUCCESSFULLY. Remove FONA device; press ENTER '
        'when ready to begin test')
    input_string = raw_input()

    logger.info('Command sent UNSUCCESSFULLY. Output:\n%s' % get_model())
