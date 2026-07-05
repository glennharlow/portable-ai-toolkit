# SUNO INTEGRATION — MEADOW / Anomaly1911Writings

## Status: CONNECTED — MANUAL ONLY

**This integration slot is reserved and intentionally locked from all automation.**

Suno will NEVER be called autonomously by MEADOW, Copilot, or any platform or script.
Every Suno action requires Glenn's explicit, direct approval — no exceptions.

---

## Why Manual-Only

- Glenn holds a Suno Pro account. Copyright ownership of generated tracks depends
  on that account remaining active and in good standing.
- Glenn's music — lyrics, beats, vocal direction — is his creative property and
  will only be submitted to Suno when Glenn decides it is ready.
- No agent, workflow, scheduler, or automated pipeline may trigger Suno on his behalf.

---

## Integration Design (Future — Glenn-Initiated Only)

When Glenn is ready to connect Suno, the workflow will be:

1. Glenn reviews a song or lyric file in vault/songs/
2. Glenn explicitly says "Hey Meadow, submit this to Suno" OR manually runs the command
3. MEADOW presents a confirmation before any submission — Glenn approves
4. MEADOW submits to Suno API with Glenn's chosen style/voice parameters
5. Generated track is returned to vault/songs/generated/ for Glenn's review
6. Glenn decides whether to publish, revise, or discard — MEADOW does NOT auto-publish

---

## API Slot

The SUNO_API_KEY placeholder exists in .env but is intentionally inactive.
Do not populate it until Glenn is ready to activate this integration.

```
# .env — Suno slot (leave blank until Glenn activates)
SUNO_API_KEY=
```

---

## Platforms This Applies To

- MEADOW daemon (meadow_daemon.py) — NO autonomous Suno calls
- Content Transformer (transformer.py) — NO autonomous Suno calls
- Morning Report workflow — NO Suno triggers
- GitHub Actions / any future workflow — NO Suno triggers
- MEADOW Mobile (phone PWA) — confirm dialog required before any Suno action

---

*Last updated: July 5, 2026 — Documented at Glenn's explicit direction.*
*Anomaly1911Writings | glennharlow/portable-ai-toolkit*
