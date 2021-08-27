# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\lalko\\PycharmProjects\\AutoGuiBot_'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += Tree('C:\\Users\\lalko\\PycharmProjects\\AutoGuiBot_\\image_to_check', prefix='image_to_check\\')
a.datas += Tree('C:\\Users\\lalko\\PycharmProjects\\AutoGuiBot_\\log', prefix='log\\')
a.datas += Tree('C:\\Users\\lalko\\PycharmProjects\\AutoGuiBot_\\result', prefix='result\\')
a.datas += Tree('C:\\Users\\lalko\\PycharmProjects\\AutoGuiBot_\\console_app', prefix='console_app\\')
a.datas += Tree('C:\\Users\\lalko\\PycharmProjects\\AutoGuiBot_\\backup', prefix='console_app\\')
a.datas += Tree('C:\\Users\\lalko\\PycharmProjects\\AutoGuiBot_\\qt_views', prefix='qt_views\\')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
