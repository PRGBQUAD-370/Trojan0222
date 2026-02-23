import ctypes
import time
import random
import os

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32
winmm = ctypes.windll.winmm

# Hide console window
SW_HIDE = 0
console = kernel32.GetConsoleWindow()
if console:
    user32.ShowWindow(console, SW_HIDE)

# MessageBox constants
MB_OKCANCEL = 0x1
MB_ICONWARNING = 0x30
IDCANCEL = 2

# Warning message boxes
resp = user32.MessageBoxW(
    0,
    "Trojan0222:\n\nIf you did not know what you just opend press cancel and nothing will happen this malware has been known to cause seroius damage to the MBR and can make display corruptions\n\nIf you are doing this is a isolated Environment press ok to continue.\n\nContinue?",
    "Virus Infection Alert",
    MB_OKCANCEL | MB_ICONWARNING
)

if resp == IDCANCEL:
    exit()

resp = user32.MessageBoxW(
    0,
    "FINAL WARNING:\n\nThe creator of Trojan0222 from github is not resonsible for any display corruptions and MBR damages\n\nTHIS IS THE LAST TIME YOU CAN STOP THIS PROGRAM BEFORE IT RUNS MALICOUS CODE ON YOUR DEVICE!!!",
    "Final Warning",
    MB_OKCANCEL | MB_ICONWARNING
)

if resp == IDCANCEL:
    exit()

# ---- PLAY MP3 AUDIO ON LOOP ----
audio_file = os.path.abspath("audio.mp3")
winmm.mciSendStringW(f'open "{audio_file}" type mpegvideo alias mp3', None, 0, None)
winmm.mciSendStringW("play mp3 repeat", None, 0, None)

# Screen info
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)
hdc = user32.GetDC(0)

# GDI raster operations
effects = [
    0x00660046,  # SRCINVERT
    0x00330008,  # NOTSRCCOPY
    0x00550009,  # DSTINVERT
    0x00CC0020,  # SRCCOPY
]

start_time = time.time()
duration = 120
effect_duration = 10
effect_index = 0
last_switch = start_time

# ---- SCREEN REFRESH TIMER (NEW) ----
last_refresh = start_time
refresh_interval = 5  # seconds

# RedrawWindow flags
RDW_INVALIDATE = 0x0001
RDW_ERASE = 0x0004
RDW_ALLCHILDREN = 0x0080

try:
    while time.time() - start_time < duration:
        now = time.time()

        if now - last_switch >= effect_duration:
            effect_index = (effect_index + 1) % len(effects)
            last_switch = now

        # ---- FORCE SCREEN REFRESH EVERY 5 SECONDS ----
        if now - last_refresh >= refresh_interval:
            user32.RedrawWindow(
                0,
                None,
                None,
                RDW_INVALIDATE | RDW_ERASE | RDW_ALLCHILDREN
            )
            last_refresh = now

        effect = effects[effect_index]

        x = random.randint(-40, 40)
        y = random.randint(-40, 40)

        gdi32.BitBlt(
            hdc,
            x,
            y,
            width,
            height,
            hdc,
            0,
            0,
            effect
        )

        time.sleep(0.03)

except KeyboardInterrupt:
    pass

# Cleanup
user32.ReleaseDC(0, hdc)

winmm.mciSendStringW("stop mp3", None, 0, None)
winmm.mciSendStringW("close mp3", None, 0, None)
