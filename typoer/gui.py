import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, colorchooser
import threading
import json
import os
import time
import logging
import keyboard
from .typoer import typoer

class TypoerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Typoer')
        self.root.geometry('1000x700')
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('typoer_gui_debug.log'), logging.StreamHandler()])
        self.settings_file = os.path.join(os.path.expanduser('~'), '.typoer_settings.json')
        self.settings = self.load_settings()
        self.wpm = tk.DoubleVar(value=self.settings.get('wpm', 60))
        self.acc = tk.DoubleVar(value=self.settings.get('accuracy', 0.95))
        self.bksp = tk.DoubleVar(value=self.settings.get('backspace_duration', 0.1))
        self.corr = tk.DoubleVar(value=self.settings.get('correction_coefficient', 0.4))
        self.kb = tk.StringVar(value=self.settings.get('keybind', 'ctrl+shift+t'))
        self.wk = tk.StringVar(value=self.settings.get('wait_key', ''))
        self.bk = tk.StringVar(value=self.settings.get('break_key', 'esc'))
        self.is_code = tk.BooleanVar(value=self.settings.get('is_code', False))
        self.lang = tk.StringVar(value=self.settings.get('language', 'plaintext'))
        self.is_rec = False
        self.make_widgets()
        self.set_kb()
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        logging.info('Typoer GUI initialized.')

    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except:
            return {}

    def save_settings(self):
        s = {'wpm': self.wpm.get(), 'accuracy': self.acc.get(), 'backspace_duration': self.bksp.get(), 'correction_coefficient': self.corr.get(), 'wait_key': self.wk.get(), 'break_key': self.bk.get(), 'keybind': self.kb.get(), 'is_code': self.is_code.get(), 'language': self.lang.get()}
        with open(self.settings_file, 'w') as f:
            json.dump(s, f, indent=4)

    def make_widgets(self):
        mf = ttk.Frame(self.root, padding='10')
        mf.pack(fill=tk.BOTH, expand=True)
        ttk.Label(mf, text='Text to Type:').pack(anchor=tk.W)
        self.txt = scrolledtext.ScrolledText(mf, height=15, width=80)
        self.txt.pack(fill=tk.BOTH, expand=True, pady=5)
        ff = ttk.Frame(mf)
        ff.pack(fill=tk.X, pady=5)
        ttk.Button(ff, text='Open File', command=self.open_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(ff, text='Save Text', command=self.save_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(ff, text='Clear', command=self.clear_text).pack(side=tk.LEFT, padx=5)
        sf = ttk.LabelFrame(mf, text='Typing Settings', padding='5')
        sf.pack(fill=tk.X, pady=10)
        ttk.Label(sf, text='WPM:').grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(sf, textvariable=self.wpm, width=10).grid(row=0, column=1, padx=5)
        ttk.Label(sf, text='Accuracy (0-1):').grid(row=0, column=2, sticky=tk.W)
        ttk.Entry(sf, textvariable=self.acc, width=10).grid(row=0, column=3, padx=5)
        ttk.Label(sf, text='Backspace Duration:').grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(sf, textvariable=self.bksp, width=10).grid(row=1, column=1, padx=5)
        ttk.Label(sf, text='Correction Coefficient:').grid(row=1, column=2, sticky=tk.W)
        ttk.Entry(sf, textvariable=self.corr, width=10).grid(row=1, column=3, padx=5)
        ttk.Label(sf, text='Language:').grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(sf, textvariable=self.lang, width=15).grid(row=2, column=1, padx=5)
        ttk.Checkbutton(sf, text='Code Mode', variable=self.is_code).grid(row=2, column=2, sticky=tk.W)
        kbf = ttk.LabelFrame(mf, text='Keybind Settings', padding='5')
        kbf.pack(fill=tk.X, pady=10)
        ttk.Label(kbf, text='Start Keybind:').grid(row=0, column=0, sticky=tk.W)
        self.kb_entry = ttk.Entry(kbf, textvariable=self.kb, width=20)
        self.kb_entry.grid(row=0, column=1, padx=5)
        self.kb_btn = ttk.Button(kbf, text='Record Keybind', command=self.record_kb)
        self.kb_btn.grid(row=0, column=2, padx=5)
        ttk.Label(kbf, text='Wait Key:').grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(kbf, textvariable=self.wk, width=20).grid(row=1, column=1, padx=5)
        ttk.Label(kbf, text='Break Key:').grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(kbf, textvariable=self.bk, width=20).grid(row=2, column=1, padx=5)
        bf = ttk.Frame(mf)
        bf.pack(pady=10)
        self.start_btn = ttk.Button(bf, text='Start Typing', command=self.start_typing)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = ttk.Button(bf, text='Stop Typing', command=self.stop_typing)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.save_btn = ttk.Button(bf, text='Save Settings', command=self.save_settings)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        self.status = tk.StringVar(value='Ready')
        ttk.Label(mf, textvariable=self.status).pack(anchor=tk.W, pady=5)

    def open_file(self):
        fp = filedialog.askopenfilename(filetypes=[('All files', '*.*')])
        if fp:
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    self.txt.delete('1.0', tk.END)
                    self.txt.insert('1.0', f.read())
            except Exception as e:
                messagebox.showerror('Error', f'Could not open file: {str(e)}')

    def save_text(self):
        fp = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt'), ('All files', '*.*')])
        if fp:
            try:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(self.txt.get('1.0', tk.END))
            except Exception as e:
                messagebox.showerror('Error', f'Could not save file: {str(e)}')

    def clear_text(self):
        self.txt.delete('1.0', tk.END)

    def set_kb(self):
        def on_kb():
            if not self.is_rec:
                self.start_typing()
        try:
            keyboard.remove_hotkey(self.kb.get())
        except Exception:
            pass
        try:
            kb = self.kb.get().replace(' ', '').lower()
            keyboard.add_hotkey(kb, on_kb)
            self.status.set(f'Keybind set to: {kb}')
        except Exception as e:
            self.status.set(f'Error setting keybind: {str(e)}')

    def record_kb(self):
        self.status.set('Press your desired key combination...')
        self.kb_btn.config(state='disabled')
        self.kb_entry.config(state='disabled')
        self.root.update()
        rec = []
        def on_key(e):
            if e.event_type == 'down':
                if e.name not in rec:
                    rec.append(e.name)
            if e.event_type == 'up':
                keyboard.unhook_all()
                combo = '+'.join(rec).replace(' ', '').lower()
                self.kb.set(combo)
                self.status.set(f'Keybind set to: {combo}')
                self.kb_btn.config(state='normal')
                self.kb_entry.config(state='normal')
                self.set_kb()
        keyboard.hook(on_key)

    def start_typing(self):
        if self.is_rec:
            return
        text = self.txt.get('1.0', tk.END).strip()
        if not text:
            self.status.set('Please enter some text to type')
            return
        self.is_rec = True
        self.status.set('Typing... Press Escape to stop')
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        def t_thread():
            try:
                typoer(
                    text=text,
                    wpm=self.wpm.get(),
                    accuracy=self.acc.get(),
                    backspace_duration=self.bksp.get(),
                    correction_coefficient=self.corr.get(),
                    wait_key=self.wk.get(),
                    break_key=self.bk.get(),
                    is_code=self.is_code.get(),
                    language=self.lang.get()
                )
            except Exception as e:
                self.status.set(f'Error: {str(e)}')
            finally:
                self.is_rec = False
                self.status.set('Ready')
                self.start_btn.config(state='normal')
                self.stop_btn.config(state='disabled')
        threading.Thread(target=t_thread, daemon=True).start()

    def stop_typing(self):
        if not self.is_rec:
            return
        keyboard.press_and_release(self.bk.get())
        self.is_rec = False
        self.status.set('Ready')
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')

    def on_close(self):
        self.save_settings()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = TypoerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 