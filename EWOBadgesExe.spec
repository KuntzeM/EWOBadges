# -*- mode: python -*-

block_cipher = None


a = Analysis(['EWOBadges.py'],
             pathex=['E:\\Coding\\Anaconda3\\Lib\\site-packages\\PyQt4',
                     'E:\\Coding\\Python\\EWOBadges',
                     'E:\\Coding\\Anaconda3\\Lib\\site-packages\\reportlab'],
             binaries=None,
             datas=None,
             hiddenimports=['six','packaging', 'packaging.version', 'packaging.specifiers'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('misc\\images\\fileopen.gif','E:\\Coding\\Python\\EWOBadges\\misc\\images\\fileopen.gif', 'DATA')]
a.datas += [('misc\\fonts\\agency-fb.ttf','E:\\Coding\\Python\\EWOBadges\\misc\\fonts\\agency-fb.ttf', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='EWOBadges',
          debug=False,
          strip=False,
          upx=True,
          console=True )
