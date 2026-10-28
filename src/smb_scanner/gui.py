"""Graphical Desktop Interface for SMB Scanner Lite (Public Sandbox Edition)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from ._core import render_sandbox_html, render_sandbox_text, run_sandbox_assessment
from .consent import (
    ALLOWED_SANDBOX_DOMAINS,
    APP_NAME,
    CONSENT_STATEMENT,
    EDITION,
    SANDBOX_DOMAIN_DESCRIPTIONS,
    VERSION,
    ConsentRequiredError,
    SandboxRestrictionError,
    record_consent_proof,
)

GUI_PALETTE = {
    "bg": "#0A0F1E",
    "panel": "#111936",
    "card": "#182242",
    "fg": "#EDF2FF",
    "dim": "#A3B1D4",
    "accent": "#6C8CFF",
    "teal": "#3ED6C5",
    "good": "#3DDC97",
    "warn": "#FFC24B",
    "bad": "#FF6B81",
}


def run_gui() -> int:
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
    except Exception as exc:
        print(
            f"Tkinter GUI is unavailable in this environment ({exc}). "
            f"Use CLI mode: smb-scanner example.com --accept-privacy-policy --consent-user 'Your Name'",
            file=sys.stderr,
        )
        return 2

    root = tk.Tk()
    root.title(f"{APP_NAME} v{VERSION} — {EDITION}")
    root.geometry("920x680")
    root.configure(bg=GUI_PALETTE["bg"])

    last_report: dict | None = None

    header = tk.Frame(root, bg=GUI_PALETTE["panel"], padx=18, pady=14)
    header.pack(fill="x")
    tk.Label(
        header,
        text=f"{APP_NAME} v{VERSION} · {EDITION}",
        bg=GUI_PALETTE["panel"],
        fg=GUI_PALETTE["fg"],
        font=("Segoe UI", 15, "bold"),
    ).pack(anchor="w")
    tk.Label(
        header,
        text="Restricted to 5 publicly free-to-use testing domains · Mandatory pre-scan user consent",
        bg=GUI_PALETTE["panel"],
        fg=GUI_PALETTE["teal"],
        font=("Segoe UI", 10),
    ).pack(anchor="w")

    form = tk.Frame(root, bg=GUI_PALETTE["bg"], padx=18, pady=12)
    form.pack(fill="x")

    tk.Label(form, text="Approved Sandbox Domain:", bg=GUI_PALETTE["bg"], fg=GUI_PALETTE["fg"]).grid(
        row=0, column=0, sticky="w", pady=4
    )
    domain_var = tk.StringVar(value=ALLOWED_SANDBOX_DOMAINS[0])
    domain_combo = ttk.Combobox(
        form, textvariable=domain_var, values=list(ALLOWED_SANDBOX_DOMAINS), state="readonly", width=28
    )
    domain_combo.grid(row=0, column=1, sticky="w", padx=8, pady=4)

    tk.Label(form, text="Your Name / Handle (Consent Signer):", bg=GUI_PALETTE["bg"], fg=GUI_PALETTE["fg"]).grid(
        row=1, column=0, sticky="w", pady=4
    )
    user_var = tk.StringVar(value="")
    tk.Entry(form, textvariable=user_var, width=32).grid(row=1, column=1, sticky="w", padx=8, pady=4)

    consent_var = tk.BooleanVar(value=False)
    tk.Checkbutton(
        form,
        text=CONSENT_STATEMENT,
        variable=consent_var,
        wraplength=760,
        justify="left",
        bg=GUI_PALETTE["bg"],
        fg=GUI_PALETTE["dim"],
        selectcolor=GUI_PALETTE["card"],
        activebackground=GUI_PALETTE["bg"],
        activeforeground=GUI_PALETTE["fg"],
    ).grid(row=2, column=0, columnspan=3, sticky="w", pady=8)

    output = tk.Text(
        root,
        bg=GUI_PALETTE["panel"],
        fg=GUI_PALETTE["fg"],
        font=("Consolas", 10),
        padx=12,
        pady=12,
    )
    output.pack(fill="both", expand=True, padx=18, pady=8)
    output.insert(
        "1.0",
        "Select one of the 5 approved public testing domains above, enter your name, "
        "accept the Privacy Policy & User Consent Agreement, and click 'Run Sandbox Scan'.\n\n"
        + "\n".join(f"  • {d}: {SANDBOX_DOMAIN_DESCRIPTIONS[d]}" for d in ALLOWED_SANDBOX_DOMAINS),
    )

    def _on_scan() -> None:
        nonlocal last_report
        try:
            receipt = record_consent_proof(
                operator=user_var.get(),
                target=domain_var.get(),
                accepted_policy=consent_var.get(),
                interface="gui",
            )
            last_report = run_sandbox_assessment(domain_var.get(), receipt)
            output.delete("1.0", "end")
            output.insert("1.0", render_sandbox_text(last_report))
        except (ConsentRequiredError, SandboxRestrictionError) as exc:
            messagebox.showwarning("Consent or Sandbox Restriction", str(exc))

    def _on_export_html() -> None:
        if not last_report:
            messagebox.showinfo("Export", "Run a sandbox assessment first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML", "*.html")])
        if path:
            Path(path).write_text(render_sandbox_html(last_report), encoding="utf-8")

    def _on_export_json() -> None:
        if not last_report:
            messagebox.showinfo("Export", "Run a sandbox assessment first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if path:
            Path(path).write_text(json.dumps(last_report, indent=2) + "\n", encoding="utf-8")

    btn_bar = tk.Frame(root, bg=GUI_PALETTE["bg"], padx=18, pady=8)
    btn_bar.pack(fill="x")
    tk.Button(
        btn_bar,
        text="Sign Consent & Run Sandbox Scan",
        command=_on_scan,
        bg=GUI_PALETTE["accent"],
        fg="#FFFFFF",
        padx=14,
        pady=6,
    ).pack(side="left", padx=(0, 8))
    tk.Button(btn_bar, text="Export HTML Report", command=_on_export_html, padx=10, pady=6).pack(
        side="left", padx=4
    )
    tk.Button(btn_bar, text="Export JSON + Consent Proof", command=_on_export_json, padx=10, pady=6).pack(
        side="left", padx=4
    )

    root.mainloop()
    return 0
