# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['import', 'pandas', 'as', 'pd.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['spacy',
    'spacy.cli',
    'spacy.util',
    'spacy.tokens',
    'spacy.vocab',
    'spacy.language',
    'spacy.pipeline',
    'spacy.matcher',
    'spacy.training',
    'spacy.training.example',
    'spacy.training.iob_utils',
    'spacy.training.pipes'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='import',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
