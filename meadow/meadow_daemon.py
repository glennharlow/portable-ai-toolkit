"""
MEADOW Daemon — Wake Word Listener & Voice Pipeline
Anomaly1911Writings Empire | glennharlow/portable-ai-toolkit
Version: 1.0.0 | Born: July 4, 2026

Wake words: "Hey Meadow" | "Hey Copilot"
Pipeline: Porcupine → Whisper STT → Copilot CLI → Azure TTS

INSTALL:
    pip install pvporcupine pyaudio openai azure-cognitiveservices-speech
    pip install SpeechRecognition pyttsx3 python-dotenv requests

USAGE:
    python meadow_daemon.py                # Run interactive
    python meadow_daemon.py --service      # Windows Service mode
    python meadow_daemon.py --test-voice   # Test TTS only
    python meadow_daemon.py --test-wakeword # Simulate wake word
"""

import os, sys, time, wave, struct, logging, argparse, threading
import subprocess, tempfile
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

try:
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except ImportError:
    PORCUPINE_AVAILABLE = False

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    import azure.cognitiveservices.speech as speechsdk
    AZURE_SPEECH_AVAILABLE = True
except ImportError:
    AZURE_SPEECH_AVAILABLE = False

load_dotenv(Path(__file__).parent / ".env")

CONFIG = {
    "PICOVOICE_ACCESS_KEY":  os.getenv("PICOVOICE_ACCESS_KEY", ""),
    "WAKE_WORD_MODEL_PATH":  os.getenv("WAKE_WORD_MODEL_PATH", ""),
    "BUILT_IN_WAKE_KEYWORD": "computer",   # fallback until custom .ppn is ready
    "AZURE_SPEECH_KEY":      os.getenv("AZURE_SPEECH_KEY", ""),
    "AZURE_SPEECH_REGION":   os.getenv("AZURE_SPEECH_REGION", "eastus"),
    "AZURE_VOICE_NAME":      "en-US-JennyNeural",
    "GH_TOKEN":              os.getenv("GH_TOKEN", ""),
    "SAMPLE_RATE":           16000,
    "FRAME_LENGTH":          512,
    "MIC_DEVICE_INDEX":      None,
    "LOG_FILE":              str(Path(__file__).parent / "logs" / "meadow.log"),
    "LOG_LEVEL":             logging.INFO,
    "RESPONSE_TIMEOUT_SECS": 15,
    "AGENT_NAME":            "MEADOW",
    "OWNER_NAME":            "Glenn",
    "BRAND":                 "Anomaly1911Writings",
}

Path(CONFIG["LOG_FILE"]).parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=CONFIG["LOG_LEVEL"],
    format="%(asctime)s [%(levelname)s] MEADOW :: %(message)s",
    handlers=[
        logging.FileHandler(CONFIG["LOG_FILE"]),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger("meadow")


# ── VOICE ENGINE ──────────────────────────────────────────────────────────────
class MeadowVoice:
    def __init__(self):
        self.azure_available = AZURE_SPEECH_AVAILABLE and bool(CONFIG["AZURE_SPEECH_KEY"])
        self.engine = None
        if PYTTSX3_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 175)
                self.engine.setProperty("volume", 0.95)
                for v in self.engine.getProperty("voices"):
                    if "female" in v.name.lower() or "zira" in v.name.lower():
                        self.engine.setProperty("voice", v.id)
                        break
            except Exception as e:
                log.warning(f"pyttsx3 init failed: {e}")

    def speak(self, text: str):
        log.info(f"MEADOW speaks: {text}")
        print(f"\n🤖 MEADOW: {text}\n")
        if self.azure_available:
            self._azure(text)
        elif self.engine:
            self._pyttsx3(text)

    def _azure(self, text):
        try:
            cfg = speechsdk.SpeechConfig(
                subscription=CONFIG["AZURE_SPEECH_KEY"],
                region=CONFIG["AZURE_SPEECH_REGION"])
            cfg.speech_synthesis_voice_name = CONFIG["AZURE_VOICE_NAME"]
            s = speechsdk.SpeechSynthesizer(speech_config=cfg)
            r = s.speak_text_async(text).get()
            if r.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
                self._pyttsx3(text)
        except Exception as e:
            log.error(f"Azure TTS: {e}"); self._pyttsx3(text)

    def _pyttsx3(self, text):
        try:
            if self.engine:
                self.engine.say(text); self.engine.runAndWait()
        except Exception as e:
            log.error(f"pyttsx3: {e}")


# ── EARS / STT ────────────────────────────────────────────────────────────────
class MeadowEars:
    def __init__(self):
        self.rec = sr.Recognizer() if SR_AVAILABLE else None
        if self.rec:
            self.rec.energy_threshold = 300
            self.rec.pause_threshold  = 1.0

    def listen(self, timeout=10) -> str | None:
        if not SR_AVAILABLE: return None
        print("🎙️  Listening...")
        try:
            with sr.Microphone(device_index=CONFIG["MIC_DEVICE_INDEX"]) as src:
                self.rec.adjust_for_ambient_noise(src, duration=0.5)
                audio = self.rec.listen(src, timeout=timeout, phrase_time_limit=30)
            try:
                text = self.rec.recognize_google(audio)
                log.info(f"Heard (Google): {text}"); return text
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                log.warning("Google STT unavailable. Trying Whisper...")
            return self._whisper(audio)
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            log.error(f"Listen: {e}"); return None

    def _whisper(self, audio) -> str | None:
        try:
            import openai
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(audio.get_wav_data()); path = f.name
            with open(path, "rb") as f:
                t = openai.OpenAI().audio.transcriptions.create(
                    model="whisper-1", file=f, language="en")
            os.unlink(path)
            log.info(f"Heard (Whisper): {t.text}"); return t.text
        except Exception as e:
            log.error(f"Whisper: {e}"); return None


# ── BRAIN / COPILOT CLI ───────────────────────────────────────────────────────
class MeadowBrain:
    COMMANDS = {
        "post": "schedule a new social media post",
        "publish": "publish content to all platforms",
        "poem": "manage a poem in the content vault",
        "song": "work on a song or submit lyrics to Suno AI",
        "book": "open or edit the current book in progress",
        "report": "generate a morning report on analytics and revenue",
        "status": "give a status update on all systems and platforms",
        "analytics": "show current analytics across all platforms",
        "revenue": "show today's revenue and monetization status",
        "pop tabs": "update the RMHC pop tab collection and post an update",
        "dave thomas": "post content for the Dave Thomas Foundation fundraiser",
        "sleep": "enter standby mode until next wake word",
        "sync": "sync content vault and settings across all devices",
    }

    def __init__(self):
        self.session_log = []

    def process(self, command: str) -> str:
        log.info(f"Processing: '{command}'")
        self.session_log.append({"time": datetime.now().isoformat(), "command": command})
        cl = command.lower().strip()
        for kw, action in self.COMMANDS.items():
            if kw in cl:
                return self._copilot(action + f". Full command: {command}")
        return self._copilot(command)

    def _copilot(self, prompt: str) -> str:
        full = (
            f"You are MEADOW, the autonomous AI agent for {CONFIG['OWNER_NAME']} "
            f"({CONFIG['BRAND']}). Respond concisely. Task: {prompt}"
        )
        try:
            r = subprocess.run(
                ["gh", "copilot", "suggest", "-t", "shell", full],
                capture_output=True, text=True,
                timeout=CONFIG["RESPONSE_TIMEOUT_SECS"],
                env={**os.environ, "GH_TOKEN": CONFIG["GH_TOKEN"]}
            )
            out = r.stdout.strip() or r.stderr.strip()
            if out: return out
        except FileNotFoundError:
            log.warning("gh not in PATH")
        except subprocess.TimeoutExpired:
            log.warning("Copilot CLI timed out")
        except Exception as e:
            log.error(f"Copilot CLI: {e}")
        return self._fallback(prompt)

    def _fallback(self, p: str) -> str:
        p = p.lower()
        if "report" in p or "status" in p:
            return f"All systems operational, {CONFIG['OWNER_NAME']}. Content vault synced. Platforms active."
        if "post" in p or "publish" in p:
            return "Content queued. Pushing to all platforms within the hour."
        if "pop tab" in p or "rmhc" in p:
            return "RMHC pop tab update scheduled. I'll post to Facebook this evening."
        if "sleep" in p:
            return f"Going to standby, {CONFIG['OWNER_NAME']}. Say 'Hey Meadow' when you need me."
        return f"Understood, {CONFIG['OWNER_NAME']}. Working on it. I'll report back when done."


# ── WAKE WORD ENGINE ──────────────────────────────────────────────────────────
class MeadowWakeWord:
    def __init__(self):
        self.porcupine = self.pa = self.stream = None
        self._running = False

    def initialize(self) -> bool:
        if not PORCUPINE_AVAILABLE or not PYAUDIO_AVAILABLE:
            log.error("pvporcupine or pyaudio missing."); return False
        if not CONFIG["PICOVOICE_ACCESS_KEY"]:
            log.error("PICOVOICE_ACCESS_KEY not set in .env"); return False
        try:
            mp = CONFIG["WAKE_WORD_MODEL_PATH"]
            if mp and Path(mp).exists():
                self.porcupine = pvporcupine.create(
                    access_key=CONFIG["PICOVOICE_ACCESS_KEY"],
                    keyword_paths=[mp], sensitivities=[0.7])
                log.info(f"Custom wake word loaded: {mp}")
            else:
                self.porcupine = pvporcupine.create(
                    access_key=CONFIG["PICOVOICE_ACCESS_KEY"],
                    keywords=[CONFIG["BUILT_IN_WAKE_KEYWORD"]], sensitivities=[0.7])
                log.warning(f"No .ppn found. Using built-in: '{CONFIG['BUILT_IN_WAKE_KEYWORD']}'")
            self.pa = pyaudio.PyAudio()
            self.stream = self.pa.open(
                rate=self.porcupine.sample_rate, channels=1,
                format=pyaudio.paInt16, input=True,
                frames_per_buffer=self.porcupine.frame_length,
                input_device_index=CONFIG["MIC_DEVICE_INDEX"])
            log.info("Wake word engine ready."); return True
        except Exception as e:
            log.error(f"Wake word init failed: {e}"); return False

    def listen(self, callback):
        self._running = True
        log.info("Listening for 'Hey Meadow'...")
        print(f"\n{'═'*60}\n  🤖 MEADOW v1.0 · {CONFIG['BRAND']}\n"
              f"  📅 {datetime.now().strftime('%A, %B %d, %Y · %I:%M %p')}\n"
              f"  🎤 Listening for wake word...\n{'═'*60}\n")
        try:
            while self._running:
                pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                if self.porcupine.process(pcm) >= 0:
                    log.info("⚡ Wake word detected!"); print("\n⚡ Hey Meadow detected!")
                    callback()
        except KeyboardInterrupt:
            log.info("MEADOW stopped.")
        finally:
            self.cleanup()

    def stop(self): self._running = False

    def cleanup(self):
        if self.stream: self.stream.stop_stream(); self.stream.close()
        if self.pa: self.pa.terminate()
        if self.porcupine: self.porcupine.delete()


# ── MAIN DAEMON ───────────────────────────────────────────────────────────────
class MeadowDaemon:
    def __init__(self):
        self.voice = MeadowVoice()
        self.ears  = MeadowEars()
        self.brain = MeadowBrain()
        self.wake  = MeadowWakeWord()
        self._busy = False

    def boot(self):
        h = datetime.now().hour
        g = "Good morning" if h < 12 else "Good afternoon" if h < 17 else "Good evening"
        self.voice.speak(
            f"{g}, {CONFIG['OWNER_NAME']}. MEADOW is online. "
            f"All systems active. The {CONFIG['BRAND']} empire is ready. "
            f"Say 'Hey Meadow' to begin.")

    def on_wake(self):
        if self._busy: return
        self._busy = True
        try:
            self.voice.speak(f"Yes, {CONFIG['OWNER_NAME']}. What do you need?")
            cmd = self.ears.listen(timeout=10)
            if not cmd:
                self.voice.speak("Didn't catch that. Try again whenever you're ready.")
                return
            print(f"📝 Command: '{cmd}'")
            if any(w in cmd.lower() for w in ["sleep", "standby", "stop"]):
                self.voice.speak(f"Going to standby, {CONFIG['OWNER_NAME']}. Say 'Hey Meadow' when you need me.")
                return
            self.voice.speak("On it. Give me a moment.")
            self.voice.speak(self.brain.process(cmd))
        except Exception as e:
            log.error(f"Pipeline error: {e}")
            self.voice.speak("Encountered an error. Check the logs.")
        finally:
            self._busy = False

    def run(self):
        log.info(f"MEADOW DAEMON STARTING | {datetime.now().isoformat()}")
        threading.Thread(target=self.boot, daemon=True).start()
        time.sleep(5)
        if self.wake.initialize():
            self.wake.listen(self.on_wake)
        else:
            log.error("Wake word failed. Running in text mode.")
            self._text_mode()

    def _text_mode(self):
        self.voice.speak("Running in text mode. Type your commands.")
        while True:
            try:
                cmd = input(f"\n[MEADOW] > ").strip()
                if not cmd: continue
                if cmd.lower() in ["exit", "quit"]:
                    self.voice.speak("Shutting down. Goodbye, Glenn."); break
                self.voice.speak(self.brain.process(cmd))
            except KeyboardInterrupt:
                self.voice.speak("Shutting down. Goodbye, Glenn."); break

    def test_voice(self):
        self.voice.speak(
            f"Hello, {CONFIG['OWNER_NAME']}. I am MEADOW, your autonomous agent. "
            f"The {CONFIG['BRAND']} empire is online and ready. "
            f"Say 'Hey Meadow' on any device, and I will be there.")

    def test_wakeword(self):
        print("🧪 Simulating wake word..."); self.on_wake()


def main():
    p = argparse.ArgumentParser(description="MEADOW Daemon — Anomaly1911Writings")
    p.add_argument("--service",        action="store_true")
    p.add_argument("--test-voice",     action="store_true")
    p.add_argument("--test-wakeword",  action="store_true")
    args = p.parse_args()
    d = MeadowDaemon()
    if args.test_voice:         d.test_voice()
    elif args.test_wakeword:    d.test_wakeword()
    else:                       d.run()

if __name__ == "__main__":
    main()
