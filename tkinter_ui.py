import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
import os

# ─── Theme Colors ─────────────────────────────────────────────────────────────
BG        = "#0f0f1a"
BG2       = "#1a1a2e"
CARD      = "#1e1e35"
ACCENT    = "#4f63ff"
ACCENT2   = "#7a4fff"
TEXT      = "#e0e0ff"
TEXT_DIM  = "#8888bb"
SUCCESS   = "#00e890"
DANGER    = "#ff6b6b"
WARNING   = "#f0a500"
BORDER    = "#2e2e50"
INPUT_BG  = "#161628"
BTN_HV    = "#3a4fdd"

FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_LABEL  = ("Segoe UI", 10)
FONT_BUTTON = ("Segoe UI", 10, "bold")
FONT_MONO   = ("Consolas", 9)
FONT_ITEM   = ("Consolas", 9)


# ─── Helpers ──────────────────────────────────────────────────────────────────
def list_items():
    return list(Path('.').rglob('*'))


class StyledButton(tk.Button):
    def __init__(self, parent, text, command, color=ACCENT, **kwargs):
        super().__init__(
            parent, text=text, command=command,
            bg=color, fg=TEXT, activebackground=BTN_HV, activeforeground=TEXT,
            relief="flat", cursor="hand2", font=FONT_BUTTON,
            padx=16, pady=8, bd=0, **kwargs
        )
        self.bind("<Enter>", lambda e: self.config(bg=BTN_HV))
        self.bind("<Leave>", lambda e: self.config(bg=color))


class StyledEntry(tk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT,
            relief="flat", font=FONT_LABEL, bd=0,
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=ACCENT, **kwargs
        )


class StyledText(scrolledtext.ScrolledText):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT,
            relief="flat", font=FONT_MONO, bd=0,
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=ACCENT, wrap=tk.WORD, **kwargs
        )


# ─── Main App ─────────────────────────────────────────────────────────────────
class FileManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🗂️ File Manager")
        self.geometry("960x660")
        self.resizable(True, True)
        self.configure(bg=BG)
        self.minsize(800, 560)

        self._build_layout()
        self.show_panel("browse")

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_layout(self):
        # ── Sidebar ──
        sidebar = tk.Frame(self, bg=BG2, width=210)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="🗂️", font=("Segoe UI", 32), bg=BG2, fg=ACCENT).pack(pady=(28, 4))
        tk.Label(sidebar, text="File Manager", font=("Segoe UI", 13, "bold"), bg=BG2, fg=TEXT).pack()
        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=20, pady=18)

        self.nav_buttons = {}
        nav_items = [
            ("browse",         "📋  Browse"),
            ("create_file",    "➕  Create File"),
            ("read_file",      "📖  Read File"),
            ("update_file",    "✏️   Update File"),
            ("delete_file",    "🗑️   Delete File"),
            ("rename_file",    "🔤  Rename File"),
            ("create_folder",  "📁  Create Folder"),
            ("delete_folder",  "🗑️   Delete Folder"),
        ]
        for key, label in nav_items:
            btn = tk.Button(
                sidebar, text=label, font=FONT_LABEL,
                bg=BG2, fg=TEXT_DIM, activebackground=CARD, activeforeground=TEXT,
                relief="flat", anchor="w", padx=22, pady=10, bd=0,
                cursor="hand2", command=lambda k=key: self.show_panel(k)
            )
            btn.pack(fill="x")
            self.nav_buttons[key] = btn

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=20, pady=18)
        tk.Label(sidebar, text="Python · Tkinter", font=("Segoe UI", 8),
                 bg=BG2, fg=TEXT_DIM).pack(side="bottom", pady=12)

        # ── Main Content ──
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

        # ── Status bar ──
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self, textvariable=self.status_var,
                              font=("Segoe UI", 9), bg=CARD, fg=TEXT_DIM,
                              anchor="w", padx=16, pady=6)
        status_bar.pack(side="bottom", fill="x")

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _header(self, title):
        hdr = tk.Frame(self.content, bg=BG, pady=6)
        hdr.pack(fill="x", padx=30, pady=(24, 0))
        tk.Label(hdr, text=title, font=FONT_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        tk.Frame(self.content, bg=BORDER, height=1).pack(fill="x", padx=30, pady=10)

    def _card(self, parent=None):
        parent = parent or self.content
        c = tk.Frame(parent, bg=CARD, padx=22, pady=18)
        c.pack(fill="x", padx=30, pady=8)
        return c

    def _label(self, parent, text, color=TEXT_DIM):
        tk.Label(parent, text=text, font=FONT_LABEL, bg=CARD, fg=color).pack(anchor="w", pady=(6, 2))

    def _result(self, msg, kind="success"):
        color = SUCCESS if kind == "success" else (DANGER if kind == "error" else "#7fa0ff")
        self.status_var.set(("✅ " if kind == "success" else "❌ " if kind == "error" else "ℹ️ ") + msg)

    def _highlight_nav(self, active_key):
        for key, btn in self.nav_buttons.items():
            if key == active_key:
                btn.config(bg=CARD, fg=TEXT, font=("Segoe UI", 10, "bold"))
            else:
                btn.config(bg=BG2, fg=TEXT_DIM, font=FONT_LABEL)

    # ── File browser widget ───────────────────────────────────────────────────
    def _file_browser(self):
        card = self._card()
        tk.Label(card, text="Current Directory", font=("Segoe UI", 10, "bold"),
                 bg=CARD, fg=ACCENT).pack(anchor="w", pady=(0, 8))

        frame = tk.Frame(card, bg=CARD)
        frame.pack(fill="both", expand=True)

        scroll = tk.Scrollbar(frame, bg=CARD, troughcolor=BG2)
        scroll.pack(side="right", fill="y")

        listbox = tk.Listbox(
            frame, bg=INPUT_BG, fg=TEXT, selectbackground=ACCENT,
            font=FONT_ITEM, relief="flat", bd=0, activestyle="none",
            highlightthickness=0, yscrollcommand=scroll.set, height=10
        )
        listbox.pack(fill="both", expand=True)
        scroll.config(command=listbox.yview)

        items = list_items()
        if not items:
            listbox.insert(tk.END, "  (empty directory)")
        for item in items:
            icon = "📁" if item.is_dir() else "📄"
            listbox.insert(tk.END, f"  {icon}  {item}")
        return listbox

    # ── Panel router ─────────────────────────────────────────────────────────
    def show_panel(self, key):
        self._clear_content()
        self._highlight_nav(key)
        self.status_var.set("Ready")
        {
            "browse":        self._panel_browse,
            "create_file":   self._panel_create_file,
            "read_file":     self._panel_read_file,
            "update_file":   self._panel_update_file,
            "delete_file":   self._panel_delete_file,
            "rename_file":   self._panel_rename_file,
            "create_folder": self._panel_create_folder,
            "delete_folder": self._panel_delete_folder,
        }[key]()

    # ══ Browse ════════════════════════════════════════════════════════════════
    def _panel_browse(self):
        self._header("📋 Browse Files & Folders")
        self._file_browser()
        StyledButton(self.content, "🔄  Refresh",
                     command=lambda: self.show_panel("browse")).pack(padx=30, pady=10, anchor="w")

    # ══ Create File ══════════════════════════════════════════════════════════
    def _panel_create_file(self):
        self._header("➕ Create New File")
        self._file_browser()

        card = self._card()
        self._label(card, "File name:")
        name_var = tk.StringVar()
        StyledEntry(card, textvariable=name_var, width=50).pack(fill="x", pady=(0, 8))
        self._label(card, "Content:")
        txt = StyledText(card, height=7)
        txt.pack(fill="both", expand=True)

        def do_create():
            name = name_var.get().strip()
            if not name:
                self._result("Enter a file name.", "error"); return
            p = Path(name)
            if p.exists():
                self._result(f"'{name}' already exists!", "error"); return
            try:
                p.write_text(txt.get("1.0", tk.END).rstrip("\n"))
                self._result(f"File '{name}' created!"); self.show_panel("create_file")
            except Exception as e:
                self._result(str(e), "error")

        StyledButton(card, "➕  Create File", do_create).pack(pady=(12, 0), anchor="w")

    # ══ Read File ════════════════════════════════════════════════════════════
    def _panel_read_file(self):
        self._header("📖 Read File")
        self._file_browser()

        card = self._card()
        self._label(card, "File name:")
        name_var = tk.StringVar()
        StyledEntry(card, textvariable=name_var, width=50).pack(fill="x", pady=(0, 8))

        output = StyledText(card, height=8, state="disabled")
        output.pack(fill="both", expand=True, pady=(8, 0))

        def do_read():
            name = name_var.get().strip()
            if not name:
                self._result("Enter a file name.", "error"); return
            p = Path(name)
            if p.exists() and p.is_file():
                content = p.read_text()
                output.config(state="normal")
                output.delete("1.0", tk.END)
                output.insert(tk.END, content or "(empty file)")
                output.config(state="disabled")
                self._result(f"Showing '{name}'")
            else:
                self._result(f"'{name}' not found.", "error")

        StyledButton(card, "📖  Read File", do_read).pack(pady=(12, 0), anchor="w")

    # ══ Update File ══════════════════════════════════════════════════════════
    def _panel_update_file(self):
        self._header("✏️ Update File")
        self._file_browser()

        card = self._card()
        self._label(card, "File name:")
        name_var = tk.StringVar()
        StyledEntry(card, textvariable=name_var, width=50).pack(fill="x", pady=(0, 8))

        mode_var = tk.StringVar(value="Overwrite")
        row = tk.Frame(card, bg=CARD)
        row.pack(anchor="w", pady=(4, 8))
        for m in ("Overwrite", "Append"):
            tk.Radiobutton(row, text=m, variable=mode_var, value=m,
                           bg=CARD, fg=TEXT, selectcolor=ACCENT,
                           activebackground=CARD, activeforeground=TEXT,
                           font=FONT_LABEL).pack(side="left", padx=(0, 16))

        self._label(card, "New content:")
        txt = StyledText(card, height=7)
        txt.pack(fill="both", expand=True)

        def do_update():
            name = name_var.get().strip()
            if not name:
                self._result("Enter a file name.", "error"); return
            p = Path(name)
            if not (p.exists() and p.is_file()):
                self._result(f"'{name}' does not exist.", "error"); return
            try:
                mode = 'w' if mode_var.get() == "Overwrite" else 'a'
                with open(name, mode) as f:
                    f.write(txt.get("1.0", tk.END).rstrip("\n"))
                self._result(f"'{name}' updated ({mode_var.get().lower()})!")
            except Exception as e:
                self._result(str(e), "error")

        StyledButton(card, "✏️  Update File", do_update).pack(pady=(12, 0), anchor="w")

    # ══ Delete File ══════════════════════════════════════════════════════════
    def _panel_delete_file(self):
        self._header("🗑️ Delete File")
        self._file_browser()

        card = self._card()
        self._label(card, "File name:")
        name_var = tk.StringVar()
        StyledEntry(card, textvariable=name_var, width=50).pack(fill="x", pady=(0, 12))

        def do_delete():
            name = name_var.get().strip()
            if not name:
                self._result("Enter a file name.", "error"); return
            p = Path(name)
            if not (p.exists() and p.is_file()):
                self._result(f"'{name}' not found.", "error"); return
            confirmed = messagebox.askyesno(
                "Confirm Delete", f"Permanently delete '{name}'?", icon="warning")
            if confirmed:
                try:
                    os.remove(p)
                    self._result(f"File '{name}' deleted.")
                    self.show_panel("delete_file")
                except Exception as e:
                    self._result(str(e), "error")

        StyledButton(card, "🗑️  Delete File", do_delete, color="#c0392b").pack(anchor="w")

    # ══ Rename File ══════════════════════════════════════════════════════════
    def _panel_rename_file(self):
        self._header("🔤 Rename File")
        self._file_browser()

        card = self._card()
        self._label(card, "Current file name:")
        old_var = tk.StringVar()
        StyledEntry(card, textvariable=old_var, width=50).pack(fill="x", pady=(0, 8))
        self._label(card, "New file name:")
        new_var = tk.StringVar()
        StyledEntry(card, textvariable=new_var, width=50).pack(fill="x", pady=(0, 12))

        def do_rename():
            old = old_var.get().strip()
            new = new_var.get().strip()
            if not old or not new:
                self._result("Fill in both fields.", "error"); return
            p = Path(old)
            if not p.exists():
                self._result(f"'{old}' not found.", "error"); return
            try:
                p.rename(new)
                self._result(f"Renamed '{old}' → '{new}'")
                self.show_panel("rename_file")
            except Exception as e:
                self._result(str(e), "error")

        StyledButton(card, "🔤  Rename", do_rename).pack(anchor="w")

    # ══ Create Folder ════════════════════════════════════════════════════════
    def _panel_create_folder(self):
        self._header("📁 Create Folder")
        self._file_browser()

        card = self._card()
        self._label(card, "Folder name:")
        name_var = tk.StringVar()
        StyledEntry(card, textvariable=name_var, width=50).pack(fill="x", pady=(0, 12))

        def do_create():
            name = name_var.get().strip()
            if not name:
                self._result("Enter a folder name.", "error"); return
            p = Path(name)
            if p.exists():
                self._result(f"'{name}' already exists!", "error"); return
            try:
                p.mkdir(parents=True)
                self._result(f"Folder '{name}' created!")
                self.show_panel("create_folder")
            except Exception as e:
                self._result(str(e), "error")

        StyledButton(card, "📁  Create Folder", do_create).pack(anchor="w")

    # ══ Delete Folder ════════════════════════════════════════════════════════
    def _panel_delete_folder(self):
        self._header("🗑️ Delete Folder")
        self._file_browser()

        card = self._card()
        self._label(card, "Folder name:")
        name_var = tk.StringVar()
        StyledEntry(card, textvariable=name_var, width=50).pack(fill="x", pady=(0, 12))

        def do_delete():
            name = name_var.get().strip()
            if not name:
                self._result("Enter a folder name.", "error"); return
            p = Path(name)
            if not (p.exists() and p.is_dir()):
                self._result(f"'{name}' not found.", "error"); return
            confirmed = messagebox.askyesno(
                "Confirm Delete", f"Delete folder '{name}'?", icon="warning")
            if confirmed:
                try:
                    p.rmdir()
                    self._result(f"Folder '{name}' deleted.")
                    self.show_panel("delete_folder")
                except OSError:
                    self._result(f"Folder '{name}' is not empty!", "error")
                except Exception as e:
                    self._result(str(e), "error")

        StyledButton(card, "🗑️  Delete Folder", do_delete, color="#c0392b").pack(anchor="w")


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = FileManagerApp()
    app.mainloop()