import ctypes
import os

dll_path = r"C:\Users\ASUS\Desktop\Machine Learning Projects\video-notes-ai\notesAI\Lib\site-packages\ctranslate2\ctranslate2.dll"

if os.path.exists(dll_path):
    try:
        ctypes.CDLL(dll_path)
        print("✅ DLL loaded successfully!")
    except OSError as e:
        print("❌ Failed to load DLL:")
        print(e)
else:
    print("❌ DLL not found.")
