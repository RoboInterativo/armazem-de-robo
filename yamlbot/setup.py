"""Настройки приложения, обработчик параметров командной строки и локализация"""

import sys
import os
import argparse
import locale
from gettext import gettext as _
import gettext

SETTINGS = {
    'project_name': 'MyProject',
    'version': '1.0',
    'domain': 'myapp',
    'dir': {
        'exec': '',
        'lang': '',
    },
    'locales': {'en': 'en_US', 'ru': 'ru_RU'},
    'locale': 'ru_RU',
}


def __translate_standard_messages():
    """Эта функция нужна только для того, чтобы Poedit при сканировании
       добавлял соответствующие строки в .po-файл для их перевода.
       Строки скопированы из стандартного модуля Python argparse.py.
    """
    # argparse
    _('%(prog)s: error: %(message)s\n')
    _('expected one argument')
    _('invalid choice: %(value)r (choose from %(choices)s)')
    _('not allowed with argument %s')
    _('optional arguments')
    _('positional arguments')
    _('show this help message and exit')
    _('usage: ')


def _get_locale():
    """
    Предварительное сканирование параметров командной строки для определения
    параметров локализации.

    :return: наименование локали ('en_US' и т.п.)
    :rtype: str
    """
    _locale, _encoding = locale.getdefaultlocale()  # Значения по умолчанию

    parser = argparse.ArgumentParser(add_help=False)
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        '-l', '--lang', choices=list(SETTINGS['locales']),
        default=None, help='Language to use.'
    )

    group.add_argument(
        '--locale', choices=list(SETTINGS['locales'].values()),
        default=_locale, help='Locale to use.'
    )

    # Не будет ругаться на неизвестные параметры
    args, _ignore = parser.parse_known_args()

    if args.lang:
        return SETTINGS['locales'][args.lang]
    else:  # У этого параметра всегда будет значение по умолчанию
        return args.locale


def _version_info():
    print(_('{name} version {ver}.'.format(name=SETTINGS['project_name'], ver=SETTINGS['version'])))
    sys.exit()


def _parse_args():
    parser = argparse.ArgumentParser()

    # Эта группа добавляется исключительно с целью показывать локализованные
    # значения справки. Сами параметры уже обработаны в _get_locale()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-l', '--lang', choices=list(SETTINGS['locales']),
        help=_('Language to use.')
    )
    group.add_argument(
        '--locale', choices=list(SETTINGS['locales'].values()),
        help=_('Locale to use.')
    )

    parser.add_argument(
        '-v', '--version', action='store_true', default=False, help=_('Display version information.')
    )

    args = parser.parse_args()

    if args.version:
        _version_info()


def set_up():
    # Определяем абсолютные пути независимо от папки, из которой был запущен скрипт
    path = sys.argv[0]
    lang = 'lang'
    SETTINGS['dir']['exec'] = os.path.realpath(os.path.dirname(path))
    SETTINGS['dir']['lang'] = os.path.realpath(os.path.join(os.path.dirname(path), lang))

    SETTINGS['locale'] = _get_locale()

    # Это заставит все стандартные модули Python использовать наш домен
    # и путь к файлам с переводом
    os.environ['LANGUAGE'] = SETTINGS['locale']
    gettext.textdomain(SETTINGS['domain'])
    gettext.bindtextdomain(SETTINGS['domain'], SETTINGS['dir']['lang'])
    print (os.environ['LANGUAGE'],SETTINGS['dir']['lang'],SETTINGS['domain'])
    print  (SETTINGS)
    _parse_args()


def main():
    return _('This module should not be executed directly.')


if __name__ == '__main__':
    sys.exit(main())
