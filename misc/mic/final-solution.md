# Internal Mic Troubleshooting — ASUS X515DA (Realtek ALC256)

## TL;DR — The Fix

The internal mic recorded silence and failed in desktop/meeting applications because the Realtek ALC256 driver presented a **disabled, unconnected pin (`0x13`)** alongside the real microphone node (`0x1b`). PipeWire/PulseAudio defaulted to routing audio capture through `0x13`.

To fix this permanently across all applications and reboots, use `hdajackretask` to mask out the dead pin at the kernel level:

1. Launch `sudo hdajackretask`.
2. Check **Show unconnected pins**.
3. Set **Node `0x13`** → Check **Override** → Set to **`Not connected`**.
4. Set **Node `0x1b`** → Check **Override** → Set to **`Internal Mic`**.
5. Click **Install boot override** and reboot.

---

## Hardware

- **Laptop:** ASUS X515DA
- **Codec:** Realtek **ALC256** (`Vendor Id 0x10ec0256`, `Subsystem 0x10431e3e`)
- **Card:** `card 1: HD-Audio Generic`, capture device `hw:1,0` (ALC256 Analog)

---

## Symptoms

- Raw recordings sounded like a short pop/click, followed by complete silence.
- Running `arecord -D hw:1,0` directly worked after manually selecting `amixer -c 1 sset 'Internal Mic 1' cap`, but:
  - The fix reset back to silence upon reboot.
  - Desktop sound servers (PipeWire/PulseAudio) still routed meeting apps (Zoom, Discord, Browsers) to silence.
  - Running terminal tests while an app was using the mic caused `Device or resource busy` errors.

---

## Root Cause

The codec exposes **two** internal-mic capture nodes in the same capture group:

| Mixer Control    | Codec Node | Pin Default   | Status                       | Audio Routing             |
| ---------------- | ---------- | ------------- | ---------------------------- | ------------------------- |
| `Internal Mic`   | `0x13`     | `0x411111f0`  | **Unconnected / Dead Pin**   | PipeWire Default (Silent) |
| `Internal Mic 1` | `0x1b`     | `0x90a70130`  | **Fixed Mic at Int (Real)**  | Inactive                  |

### Key Insights:

1. **ALSA vs. PipeWire Layering:** `amixer` changes ALSA routing directly, but modern sound servers (PipeWire) dynamically re-evaluate hardware profiles at boot and override raw ALSA state (`alsactl store`), pulling input back to `0x13`.
2. **Exclusive Hardware Locks:** Direct access via `arecord -D hw:1,0` grabs exclusive ALSA locks. When PipeWire controls the hardware node for desktop apps, running direct `arecord` commands causes lock errors (`Device or resource busy`). Apps must route *through* PipeWire rather than around it.
3. **Single GUI Port Mapping:** `pavucontrol` only displayed one "Internal Microphone" entry because PipeWire collapsed both nodes into one port profile, silently binding it to `0x13`.

---

## Diagnosis Steps

1. **waveform Analysis:** Recording directly from `hw:1,0` yielded a flat line with an RMS ~131, confirming an ADC pinned to an open/unconnected pin.
2. **Codec Dump Verification:** Inspection of `/proc/asound/card1/codec#0` confirmed node `0x1b` was the physical "Mic at Int", whereas `0x13` was unconnected.
3. **Manual Pin Test:** Executing `amixer -c 1 sset 'Internal Mic 1' cap` temporarily redirected capture to node `0x1b`, restoring vocal input in raw test recordings.

---

## Permanent Solution

Instead of relying on user-space scripts or temporary ALSA overrides, apply a kernel firmware patch via `hdajackretask` (part of `alsa-tools`):

1. **Mask Pin `0x13`:** Setting node `0x13` to `Not connected` tells the kernel driver that the pin does not physically exist.
2. **Expose Pin `0x1b`:** Setting node `0x1b` to `Internal Mic` forces the kernel to treat `0x1b` as the primary internal microphone.
3. **Persist at Boot:** Clicking **Install boot override** writes a sysfs/modprobe firmware patch.

Upon reboot:
- ALSA exposes only node `0x1b`.
- PipeWire/PulseAudio binds directly to `0x1b`.
- All meeting applications automatically pick up the microphone without software lockups or manual terminal tweaks.
