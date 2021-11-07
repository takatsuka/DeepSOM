# -*- mode: python -*-

block_cipher = None

added_files = [
    ('./gui', 'gui')
]


a = Analysis(
    ['./src/index.py'],
    pathex=['./dist'],
    hookspath=["."],
    binaries=[],
    datas=added_files,
    hiddenimports=['pysom'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=True,
    cipher=block_cipher
)


pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)


exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    exclude_binaries=False,
    name='PySOM Creator',
    debug=True,
    strip=False,
    # icon='.\\src\\assets\\logo.ico',
    upx=True,
    console=True)  # set this to see error output of the executable

app = BUNDLE(exe,
             name='PySOM Creator.app',
            #  icon='dev/icon/moccasin.icns',
             bundle_identifier=None,
             info_plist={'NSHighResolutionCapable': 'True'},
             )
