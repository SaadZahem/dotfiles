# Internal Mic Troubleshooting — ASUS X515DA (Realtek ALC256)

## TL;DR — the fix

The internal mic recorded silence because the ALC256 driver defaulted the
capture source to a **disabled, unconnected pin** instead of the real mic.
Select the correct source and persist it:

```bash
amixer -c 1 sset 'Internal Mic 1' cap   # route the real internal-mic node to the ADC
sudo alsactl store 1                     # persist so alsa-restore reapplies it at boot
```

No reboot and **no `snd-hda-intel` module quirk** are needed.

---

## Hardware

- Laptop: ASUS X515DA
- Codec: Realtek **ALC256** (`Vendor Id 0x10ec0256`, `Subsystem 0x10431e3e`)
- Card: `card 1: HD-Audio Generic`, capture device `hw:1,0` (ALC256 Analog)

## Symptom

- Recordings sounded like a short pop for a fraction of a second, then silence.
- Speaking into the mic never registered.

## Root cause

The driver exposes **two** internal-mic capture sources in the same
capture-exclusive group, and defaulted to the wrong one:

| Mixer control    | Codec node | Pin default   | Meaning                    | Status (bad) |
|------------------|-----------|---------------|----------------------------|--------------|
| `Internal Mic`   | `0x13`    | `0x411111f0`  | **not connected / disabled** | selected `[on]` |
| `Internal Mic 1` | `0x1b`    | `0x90a70130`  | **Fixed Mic at Int (real mic)** | `[off]`      |

The ADC was listening to the dead pin (`0x13`), so capture produced a frozen
noise floor that ignored actual sound. The real microphone is node `0x1b`,
exposed as **`Internal Mic 1`**.

> Note: an earlier attempt commented out `options snd-hda-intel
> model=laptop-dmic` in `/etc/modprobe.d/alsa-base.conf`. That was a red
> herring for this symptom — it can stay commented out; it's harmless either
> way. The real fix is the capture-source selection above.

## How it was diagnosed

1. Confirmed the capture device exists and mixer levels were fully open
   (Capture 63/63 @ +30dB, Internal Mic Boost maxed, Auto-Mute disabled):

   ```bash
   arecord -l
   amixer -c 1
   ```

2. Recorded and analyzed the waveform over time. The signal showed a large
   startup DC transient pinned at the +32767 rail, an ~2s RC decay, then a
   **perfectly flat RMS ~131 that never responded to speech** — the tell-tale
   sign of an ADC with nothing connected:

   ```bash
   arecord -D hw:1,0 -f S16_LE -r 44100 -c 2 -d 4 /tmp/mic.wav
   # analyze per-100ms mean(DC)/rms/peak with a short python snippet
   ```

3. Dumped the codec to find the real mic node and the mis-selected source:

   ```bash
   cat /proc/asound/card1/codec#0        # look for 'Mic at Int' pins + their nodes
   ```

4. Switched the capture source to node `0x1b` (`Internal Mic 1`) and re-tested:
   RMS jumped from a frozen 131 to 10,000+ and varied with sound → mic alive.

## Verify it works

```bash
# Live VU meter — tap the mic and watch the bar move (Ctrl+C to stop)
arecord -D hw:1,0 -f cd -V mono /dev/null

# Or record-and-playback
arecord -D hw:1,0 -f cd -d 5 /tmp/test.wav && aplay /tmp/test.wav
```

## If it reverts after a reboot

`alsactl store` saves ALSA state, restored at boot by `alsa-restore.service`.
If PipeWire/PulseAudio or a desktop setting re-selects the wrong source, force
it at login instead, e.g. add to a startup script (`~/.xinitrc`) or a user
systemd unit:

```bash
amixer -c 1 sset 'Internal Mic 1' cap
```
