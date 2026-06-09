import importlib, pathlib, json

ROOT = pathlib.Path('D:/portable-ai-toolkit')
results = []

def check(label, ok):
    print(f"  {'[PASS]' if ok else '[FAIL]'} {label}")
    results.append(ok)

print('\n=== Portable AI Toolkit - Self Test ===\n')

for d in ['ai-voice-assistant','scripts','config','docs','creative-file-manager']:
    check(f'Folder: {d}', (ROOT / d).is_dir())

check('settings.json', (ROOT / 'config' / 'settings.json').is_file())

for pkg in ['speech_recognition','pyttsx3','yaml','watchdog','rich','click','whisper','torch']:
    check(f'Package: {pkg}', importlib.util.find_spec(pkg) is not None)

passed, total = sum(results), len(results)
print(f"\n{'All tests passed!' if passed == total else 'Some tests failed.'} ({passed}/{total})\n")
if passed < total:
    print('  Fix: python -m pip install speechrecognition pyaudio pyttsx3 openai-whisper torch transformers pyyaml watchdog rich click\n')
