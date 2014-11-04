#!/usr/bin/python

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp


version = imp.load_source('version', 'lib/version.py')
util = imp.load_source('version', 'lib/util.py')

if sys.version_info[:3] < (2, 6, 0):
    sys.exit("Error: Electrum requires Python version >= 2.6.0...")

usr_share = '/usr/share'
if not os.access(usr_share, os.W_OK):
    usr_share = os.getenv("XDG_DATA_HOME", os.path.join(os.getenv("HOME"), ".local", "share"))

data_files = []
if (len(sys.argv) > 1 and (sys.argv[1] == "sdist")) or (platform.system() != 'Windows' and platform.system() != 'Darwin'):
    print "Including all files"
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-dvc.desktop']),
        (os.path.join(usr_share, 'app-install', 'icons/'), ['icons/electrum-dvc.png'])
    ]
    if not os.path.exists('locale'):
        os.mkdir('locale')
    for lang in os.listdir('locale'):
        if os.path.exists('locale/%s/LC_MESSAGES/electrum.mo' % lang):
            data_files.append((os.path.join(usr_share, 'locale/%s/LC_MESSAGES' % lang), ['locale/%s/LC_MESSAGES/electrum.mo' % lang]))


appdata_dir = util.appdata_dir()
if not os.access(appdata_dir, os.W_OK):
    appdata_dir = os.path.join(usr_share, "electrum-dvc")

data_files += [
    (appdata_dir, ["data/README"]),
    (os.path.join(appdata_dir, "cleanlook"), [
        "data/cleanlook/name.cfg",
        "data/cleanlook/style.css"
    ]),
    (os.path.join(appdata_dir, "sahara"), [
        "data/sahara/name.cfg",
        "data/sahara/style.css"
    ]),
    (os.path.join(appdata_dir, "dark"), [
        "data/dark/name.cfg",
        "data/dark/style.css"
    ])
]

for lang in os.listdir('data/wordlist'):
    data_files.append((os.path.join(appdata_dir, 'wordlist'), ['data/wordlist/%s' % lang]))


setup(
    name="Electrum-dvc",
    version=version.ELECTRUM_VERSION,
    install_requires=[
        'slowaes',
        'ecdsa>=0.9',
        'pbkdf2',
        'requests',
        'pyasn1',
        'pyasn1-modules',
        'qrcode',
        'SocksiPy-branch',
        'tlslite'
    ],
    package_dir={
        'electrum_dvc': 'lib',
        'electrum_dvc_gui': 'gui',
        'electrum_dvc_plugins': 'plugins',
    },
    scripts=['electrum-dvc'],
    data_files=data_files,
    py_modules=[
        'electrum_dvc.account',
        'electrum_dvc.bitcoin',
        'electrum_dvc.blockchain',
        'electrum_dvc.bmp',
        'electrum_dvc.commands',
        'electrum_dvc.daemon',
        'electrum_dvc.i18n',
        'electrum_dvc.interface',
        'electrum_dvc.mnemonic',
        'electrum_dvc.msqr',
        'electrum_dvc.network',
        'electrum_dvc.network_proxy',
        'electrum_dvc.old_mnemonic',
        'electrum_dvc.paymentrequest',
        'electrum_dvc.paymentrequest_pb2',
        'electrum_dvc.plugins',
        'electrum_dvc.qrscanner',
        'electrum_dvc.simple_config',
        'electrum_dvc.synchronizer',
        'electrum_dvc.transaction',
        'electrum_dvc.util',
        'electrum_dvc.verifier',
        'electrum_dvc.version',
        'electrum_dvc.wallet',
        'electrum_dvc.x509',
        'electrum_dvc_gui.gtk',
        'electrum_dvc_gui.qt.__init__',
        'electrum_dvc_gui.qt.amountedit',
        'electrum_dvc_gui.qt.console',
        'electrum_dvc_gui.qt.history_widget',
        'electrum_dvc_gui.qt.icons_rc',
        'electrum_dvc_gui.qt.installwizard',
        'electrum_dvc_gui.qt.lite_window',
        'electrum_dvc_gui.qt.main_window',
        'electrum_dvc_gui.qt.network_dialog',
        'electrum_dvc_gui.qt.password_dialog',
        'electrum_dvc_gui.qt.paytoedit',
        'electrum_dvc_gui.qt.qrcodewidget',
        'electrum_dvc_gui.qt.qrtextedit',
        'electrum_dvc_gui.qt.receiving_widget',
        'electrum_dvc_gui.qt.seed_dialog',
        'electrum_dvc_gui.qt.transaction_dialog',
        'electrum_dvc_gui.qt.util',
        'electrum_dvc_gui.qt.version_getter',
        'electrum_dvc_gui.stdio',
        'electrum_dvc_gui.text',
        'electrum_dvc_plugins.btchipwallet',
        'electrum_dvc_plugins.coinbase_buyback',
        'electrum_dvc_plugins.cosigner_pool',
        'electrum_dvc_plugins.exchange_rate',
        'electrum_dvc_plugins.greenaddress_instant',
        'electrum_dvc_plugins.labels',
        'electrum_dvc_plugins.trezor',
        'electrum_dvc_plugins.virtualkeyboard',
    ],
    description="Lightweight Devcoin Wallet",
    author="Thomas Voegtlin",
    author_email="thomasv1@gmx.de",
    license="GNU GPLv3",
    url="https://dvc.electrum-alt.org",
    long_description="""Lightweight Devcoin Wallet"""
)
