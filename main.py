from PIL import Image
import keyboard
import os
import win32clipboard
import zipfile





def hide_console_window():
    if os.name == 'nt':  
        import ctypes
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd != 0:
            ctypes.windll.user32.ShowWindow(hwnd, 0)  

hide_console_window()



def convert_image(image_path):
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return

    file_extension = os.path.splitext(image_path)[1].lower()
    
    if file_extension == '.jpg':
        new_path = image_path[:-4] + '.png'
        img = Image.open(image_path)
        img.save(new_path, 'PNG')
        os.remove(image_path)
        print(f"Converted {image_path} to {new_path}")
    
    elif file_extension == '.png':
        new_path = image_path[:-4] + '.jpg'
        img = Image.open(image_path)
        img = img.convert("RGB")
        img.save(new_path, 'JPEG')
        os.remove(image_path)
        print(f"Converted {image_path} to {new_path}")
        
    elif file_extension == '.webp':
        new_path = image_path[:-5] + '.png'
        img = Image.open(image_path)
        img.save(new_path, 'PNG')
        os.remove(image_path)
        print(f"Converted {image_path} to {new_path}")
    else:
        print("No supported format found for conversion.")

def extract_zip(archive_path):
    if not os.path.exists(archive_path):
        print(f"Archive not found: {archive_path}")
        return

   
    folder_name = os.path.splitext(os.path.basename(archive_path))[0]
    output_dir = os.path.join(os.path.dirname(archive_path), folder_name)
    
    
    os.makedirs(output_dir, exist_ok=True)
    
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
        print(f"Extracted {archive_path} to {output_dir}")

def get_file_path_from_clipboard():
    win32clipboard.OpenClipboard()
    try:
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):
            files = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
            for file_path in files:
                if file_path.lower().endswith(('.jpg', '.png', '.webp', '.zip')):
                    return file_path
    finally:
        win32clipboard.CloseClipboard()
    return None

def monitor_shortcut():
    print("Running... Press Ctrl + F2 to process selected file.")
    while True:
        if keyboard.is_pressed('ctrl+f2'):
            file_path = get_file_path_from_clipboard()
            if file_path:
                if file_path.lower().endswith('.zip'):
                    extract_zip(file_path)
                else:
                    convert_image(file_path)
            else:
                print("No valid file in the clipboard. Copy the file path first!")

monitor_shortcut()

