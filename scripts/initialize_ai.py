import json, pathlib

ROOT = pathlib.Path('D:/portable-ai-toolkit')
DIRS = ['ai-voice-assistant','creative-file-manager','windows-recovery-tools','research-assistant','cross-machine-sync','scripts','config','docs']

print('\n=== Portable AI Toolkit - Initializer ===\n')
for d in DIRS:
    (ROOT / d).mkdir(parents=True, exist_ok=True)
    print(f'  [OK] {ROOT / d}')

cfg = ROOT / 'config' / 'settings.json'
if not cfg.exists():
    cfg.write_text(json.dumps({'wake_word':'hey ai','confirm_before_action':True,'undo_enabled':True,'onedrive_enabled':True,'platforms':['BandLab','Suno','YouTube','TikTok','OneDrive']}, indent=2))
    print(f'  [OK] Config written')

bat = ROOT / 'START_HERE.bat'
bat.write_text('@echo off\ncd /d D:\\portable-ai-toolkit\npython ai-voice-assistant\\main.py\npause\n')
print(f'  [OK] START_HERE.bat created')
print('\nInitialization complete! Run scripts\\test_setup.py next.\n')
