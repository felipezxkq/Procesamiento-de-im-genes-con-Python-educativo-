# -*- mode: python -*-

block_cipher = None


a = Analysis(['matrizIntensidad.py'],
             pathex=['C:\\Users\\Felipe\\Desktop\\Guthub\\Procesamiento-de-imagenes-con-Python\\Programas'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='matrizIntensidad',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='insignia_ubb.ico')
