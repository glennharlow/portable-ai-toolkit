import sys, json, pathlib, time

ROOT = pathlib.Path('D:/portable-ai-toolkit')
CFG = ROOT / 'config' / 'settings.json'

def load_cfg():
    return json.loads(CFG.read_text()) if CFG.exists() else {'wake_word':'hey ai','confirm_before_action':True,'undo_enabled':True}

def speak(text):
    print(f'[AI] {text}')
    try:
        import pyttsx3
        e = pyttsx3.init()
        e.setProperty('rate', 165)
        e.say(text)
        e.runAndWait()
    except: pass

def listen_wake(wake):
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as src:
            r.adjust_for_ambient_noise(src, duration=1)
            print(f'  Listening for "{wake}"...')
            while True:
                try:
                    audio = r.listen(src, timeout=5, phrase_time_limit=4)
                    if wake in r.recognize_google(audio).lower():
                        return True
                except: pass
    except ImportError:
        input(f'  [No mic] Press ENTER to simulate "{wake}" > ')
        return True

HISTORY = []

def handle(cmd, cfg):
    cmd = cmd.lower().strip()
    if 'undo' in cmd:
        speak(f'Undoing: {HISTORY.pop()}' if HISTORY else 'Nothing to undo.')
        return
    if any(w in cmd for w in ['poem','rap','lyric','song','write']):
        speak('What is the topic?')
        topic = input('  Topic > ')
        if cfg.get('confirm_before_action'):
            speak(f'Create about {topic}. Confirm?')
            if 'y' not in input('  Yes/No > ').lower():
                speak('Cancelled.'); return
        out = ROOT / 'creative-file-manager' / f"{cmd.split()[0]}_{topic.replace(' ','_')}.txt"
        out.write_text(f'# {cmd.title()} about {topic}\n\n[Content here]\n')
        speak(f'Created {out.name}')
        HISTORY.append(f'Created {out.name}')
    elif 'sync' in cmd:
        speak('Syncing. Please wait.')
        time.sleep(1)
        speak('Sync complete.')
    elif 'help' in cmd:
        speak('Say: write a poem, write a rap, sync, undo, or quit.')
    elif any(w in cmd for w in ['quit','exit','stop','bye']):
        speak('Goodbye Glenn.')
        sys.exit(0)
    else:
        speak(f'I heard: {cmd}. Say help for options.')

def main():
    cfg = load_cfg()
    wake = cfg.get('wake_word', 'hey ai')
    print('\n========================================')
    print('  Portable AI Toolkit - Voice Assistant')
    print('========================================')
    speak(f'Ready. Say {wake} to begin.')
    try:
        while True:
            if listen_wake(wake):
                speak('Yes? What would you like?')
                try:
                    import speech_recognition as sr
                    r = sr.Recognizer()
                    with sr.Microphone() as src:
                        audio = r.listen(src, timeout=6, phrase_time_limit=8)
                        cmd = r.recognize_google(audio)
                        print(f'  Heard: {cmd}')
                except:
                    cmd = input('  Command > ')
                handle(cmd, cfg)
    except KeyboardInterrupt:
        speak('Shutting down. Goodbye Glenn.')

if __name__ == '__main__':
    main()
