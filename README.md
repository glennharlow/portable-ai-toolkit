# Portable AI Toolkit for Creative & Technical Workflows

A comprehensive, offline-capable AI toolkit designed for your creative writing, music production, digital forensics, and multi-machine management. Everything runs from your USB drive with voice-first interaction.

## 🎯 Core Features

### 1. **Voice-First AI Assistant**
- Always-listening local wake word activation
- Works offline with advanced local LLMs
- Minimal typing required
- Runs across all 7 of your machines when USB is plugged in
- Deep psychological/emotional feedback on your creative work

### 2. **Creative Writing & Music Management**
- Intelligent file organization for poems, raps, songs, lyrics
- Auto-categorization by mood, genre, theme
- Psychology-based feedback on emotional impact
- Integration hooks for BandLab, Suno, YouTube, TikTok
- Batch metadata management for your music platforms

### 3. **File Repair & Organization**
- Auto-fixes corrupted filetypes
- Corrects misplaced files in wrong folders
- Recovers from read-only/archive flag mistakes
- Undo-safe operations with automatic backups
- Handles your "mess" gracefully

### 4. **Windows Settings Recovery**
- Quick fixes for your common mistakes
- Safe, reversible changes with full backup
- Works across Windows 10/11
- One-click recovery for frequently changed settings
- Tracks all modifications with clear logs

### 5. **Research & Digital Forensics Tools**
- Deep research capabilities (finance, cybersecurity, forensics)
- Bookmark and organize findings
- Voice-activated research capture
- Psychology-focused analysis
- Knowledge base searchable across sessions

### 6. **Cross-Machine Sync Framework**
- Sync settings and preferences across your 7 machines
- Cloud backup integration (OneDrive, Google Drive)
- Portable development environment
- Git version control for your creative work
- Local caching for offline work

---

## 📁 Project Structure

```
portable-ai-toolkit/
├── README.md                          # This file
├── SETUP.md                           # USB setup instructions
├── QUICK_START.md                     # First-time user guide
│
├── ai-voice-assistant/                # Voice-first AI core
│   ├── requirements.txt
│   ├── main.py
│   ├── wake_word_detector.py
│   ├── llm_engine.py
│   ├── voice_input.py
│   └── README.md
│
├── creative-file-manager/             # Music & writing organization
│   ├── requirements.txt
│   ├── file_organizer.py
│   ├── metadata_manager.py
│   ├── platform_integrations.py
│   ├── config.yaml
│   └── README.md
│
├── windows-recovery-tools/            # File & settings recovery
│   ├── file_type_fixer.py
│   ├── settings_recovery.ps1
│   ├── attribute_corrector.py
│   ├── backup_manager.py
│   └── README.md
│
├── research-assistant/                # Digital forensics & learning
│   ├── requirements.txt
│   ├── research_engine.py
│   ├── psychology_analyzer.py
│   ├── forensics_tools.py
│   └── README.md
│
├── cross-machine-sync/                # Multi-device synchronization
│   ├── sync_engine.py
│   ├── cloud_integrations.py
│   ├── config_manager.py
│   └── README.md
│
├── scripts/                           # Quick utility scripts
│   ├── setup_usb.sh (for Mac/Linux)
│   ├── setup_usb.ps1 (for Windows)
│   ├── initialize_ai.py
│   └── test_setup.py
│
├── config/                            # Configuration templates
│   ├── voice_config.yaml
│   ├── creative_config.yaml
│   ├── sync_config.yaml
│   └── platforms_config.yaml
│
└── docs/                              # Extended documentation
    ├── VOICE_SETUP.md
    ├── FILE_ORGANIZATION.md
    ├── WINDOWS_RECOVERY.md
    ├── RESEARCH_TOOLS.md
    ├── CROSS_MACHINE.md
    ├── TROUBLESHOOTING.md
    └── API_INTEGRATIONS.md
```

---

## 🚀 Quick Start

1. **Clone to your USB**: See [SETUP.md](SETUP.md)
2. **Run initialization**: `python scripts/initialize_ai.py`
3. **Configure your platforms**: Edit `config/platforms_config.yaml`
4. **Test voice assistant**: `python ai-voice-assistant/main.py`
5. **Start using**: Say "Hey AI" to activate

---

## 💻 System Requirements

- **USB Drive**: 32GB (you have this ✓)
- **Python**: 3.9+ (portable version included)
- **RAM**: 8GB+ recommended
- **Windows**: 10 or 11
- **Disk Space**: ~25GB for local LLM models

---

## 🎤 Voice Commands Examples

```
"Hey AI, read my latest poem and give me psychological feedback"
"Hey AI, organize my music files by emotional tone"
"Hey AI, fix my corrupted song files"
"Hey AI, research cybersecurity backdoor vulnerabilities"
"Hey AI, help me write my screenplay"
"Hey AI, sync my settings across all my machines"
"Hey AI, recover my settings from that mistake I made"
```

---

## 🔗 Platform Integrations

Ready-to-configure integration hooks for:
- BandLab
- Suno
- YouTube / YouTube Music
- TikTok
- Facebook
- Instagram
- OneDrive
- Google Drive
- Outlook
- Microsoft 365

See [docs/API_INTEGRATIONS.md](docs/API_INTEGRATIONS.md) for setup details.

---

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - USB setup and installation
- **[QUICK_START.md](QUICK_START.md)** - First-time user guide
- **[VOICE_SETUP.md](docs/VOICE_SETUP.md)** - Voice assistant configuration
- **[FILE_ORGANIZATION.md](docs/FILE_ORGANIZATION.md)** - Creative file management
- **[WINDOWS_RECOVERY.md](docs/WINDOWS_RECOVERY.md)** - Settings & file recovery
- **[RESEARCH_TOOLS.md](docs/RESEARCH_TOOLS.md)** - Research & forensics
- **[CROSS_MACHINE.md](docs/CROSS_MACHINE.md)** - Sync across your 7 machines
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues & fixes
- **[API_INTEGRATIONS.md](docs/API_INTEGRATIONS.md)** - Platform integrations

---

## 🛠️ Features by Use Case

### For Your Creative Work
- ✅ Voice feedback on poems, raps, songs
- ✅ Psychology-based emotional analysis
- ✅ Metadata management for multiple platforms
- ✅ Batch upload preparation
- ✅ Lyric/script brainstorming assistant

### For Your Technical Work
- ✅ Digital forensics research tools
- ✅ Cybersecurity vulnerability research
- ✅ Scripting and coding helpers
- ✅ Windows settings recovery
- ✅ File repair and recovery

### For Your Head Injury Accommodations
- ✅ Voice-first (minimal typing)
- ✅ Confirmation before any changes
- ✅ Automatic backups and undo
- ✅ Clear logging of all actions
- ✅ Confused file/folder recovery
- ✅ Patient, non-judgmental feedback

### For Your Multi-Machine Workflow
- ✅ Sync across all 7 computers
- ✅ Settings persistence
- ✅ Cloud backup integration
- ✅ Portable configuration
- ✅ Works on Windows 10 and 11

---

## 🔐 Security & Privacy

- **100% Offline**: Core AI runs locally, no data sent to cloud unless you choose
- **Your Control**: Every action requires explicit permission
- **Backups**: Automatic backups before any system changes
- **Encrypted Storage**: Optional encryption for sensitive files
- **No Tracking**: Runs only when you command it
- **Open Source**: You can inspect and modify all code

---

## 🚦 Getting Started

**Next Steps:**
1. Read [SETUP.md](SETUP.md) for USB installation
2. Run the initialization script
3. Configure your voice wake word
4. Add your platform credentials
5. Start with a simple voice command

**Need Help?**
See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) or check the README in each module.

---

## 📝 Customization

Everything is modular and extensible:
- Add new research sources
- Configure additional platforms
- Customize voice commands
- Build new file organization rules
- Create custom psychology analysis prompts

See individual module READMEs for extension guides.

---

## 📄 License

MIT License - You own and control everything

---

## 🤝 Support & Contributions

- **Questions?** Check TROUBLESHOOTING.md
- **Want to add features?** See module READMEs for contribution guides
- **Found an issue?** Document it clearly with your setup details

---

## 🎯 Your AI That Actually Works For You

This toolkit is built around **your actual needs**:
- Creative workflows with multiple platforms
- Technical/forensics research and learning
- Multi-machine management
- Head injury accommodations (voice-first, confirmation, clarity)
- Portable accessibility (always on your keychain)
- Offline capability (works anywhere)

**You're not fitting into the AI. The AI fits into your life.**

---

Start with [SETUP.md](SETUP.md) when you're ready! 🚀
