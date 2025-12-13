import os
import tempfile
import datetime
from tkinter import ttk, messagebox
import tkinter as tk

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PIL import Image, ImageDraw, ImageFont

class ReceiptViewer:
    def __init__(self, parent, receipt):
        self.parent = parent
        self.receipt = receipt
        self.win = tk.Toplevel(parent)
        self.win.title(f"Receipt - {receipt.get('id','')}")
        self.win.geometry("480x640")
        self.create_widgets()
        self.populate()

    def create_widgets(self):
        top = ttk.Frame(self.win, padding=8)
        top.pack(fill=tk.BOTH, expand=True)

        # Text display (read-only)
        self.text = tk.Text(top, wrap=tk.NONE, state=tk.NORMAL, font=("Courier", 10))
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbars
        v = ttk.Scrollbar(top, orient=tk.VERTICAL, command=self.text.yview)
        v.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=v.set)

        # Buttons
        btn_frame = ttk.Frame(self.win, padding=8)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="Print to PDF", command=self.export_pdf).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Save Image (PNG)", command=self.save_image).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Close", command=self.win.destroy).pack(side=tk.RIGHT, padx=4)

    def populate(self):
        txt = self.format_receipt_text(self.receipt)
        self.text.configure(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, txt)
        self.text.configure(state=tk.DISABLED)

    def format_receipt_text(self, r):
        # Build a simple header-only receipt text from the provided dict.
        # Accepts keys: company (dict), id, date, worker, customer (optional).
        lines = []
        comp = r.get("company") or {}
        name = comp.get("name") or r.get("company_name") or "Shoppy"
        addr = comp.get("address") or r.get("company_address") or "Lobo, Eyang"
        phone = comp.get("phone") or r.get("company_phone") or ""

        # Company header
        lines.append(name)
        if addr:
            lines.append(addr)
        if phone:
            lines.append(f"Tel: {phone}")

        lines.append("-" * 32)

        # Receipt metadata
        rid = r.get("id") or r.get("receipt_id") or ""
        date = r.get("date") or r.get("datetime") or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worker = r.get("worker") or r.get("worker_name") or r.get("served_by") or ""
        customer = r.get("customer") or r.get("customer_name") or ""

        lines.append(f"Receipt: {rid}")
        lines.append(f"Date: {date}")
        if customer:
            lines.append(f"Customer: {customer}")
        if worker:
            lines.append(f"Served by: {worker}")

        lines.append("-" * 32)
        lines.append("")
        # If items exist in the receipt dict, show them and the total
        items = r.get("items") or r.get("lines") or []
        if items:
            lines.append(f"{'Item':<25} {'Qty':>5} {'Price':>12} {'Total':>12}")
            lines.append("-" * 60)
            total_sum = r.get("total", 0)
            for item in items:
                name = item.get("name", "")[:25]
                qty = item.get("quantity", item.get("qty", 0))
                unit_raw = item.get("unit_price", 0)
                total_raw = item.get("total", qty * unit_raw)
                # unit_price in your app is stored as cents; display FCFA
                try:
                    unit = float(unit_raw) 
                    total_price = float(total_raw)
                except Exception:
                    unit = unit_raw
                    total_price = total_raw
                lines.append(f"{name:<25} {qty:>5} FCFA {unit:>10.2f} FCFA {total_price:>10.2f}")
            lines.append("-" * 60)
            # show total (convert if needed)
            try:
                total_display = float(total_sum)
            except Exception:
                total_display = total_sum
            lines.append(f"{'':>35} {'TOTAL:':<10} FCFA {total_display:>11.2f}")

        lines.append("")
        lines.append("Thank you for your purchase!")
        return "\n".join(lines)

    def export_pdf(self):
        # Ask for file path
        import tkinter.filedialog as fd
        default_name = f"{self.receipt.get('id','receipt')}.pdf"
        path = fd.asksaveasfilename(defaultextension=".pdf", initialfile=default_name,
                                    filetypes=[("PDF files","*.pdf")])
        if not path:
            return
        try:
            self._write_pdf(path)
            messagebox.showinfo("Exported", f"Saved PDF to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {e}")

    def _write_pdf(self, path):
        # Simple text layout using ReportLab
        c = canvas.Canvas(path, pagesize=A4)
        width, height = A4
        margin = 15 * mm
        x = margin
        y = height - margin
        line_height = 10  # points

        text_lines = self.format_receipt_text(self.receipt).splitlines()
        c.setFont("Courier", 10)
        for line in text_lines:
            if y < margin + line_height:
                c.showPage()
                y = height - margin
                c.setFont("Courier", 10)
            c.drawString(x, y, line)
            y -= line_height
        c.showPage()
        c.save()

    def save_image(self):
        # Ask for file path
        import tkinter.filedialog as fd
        default_name = f"{self.receipt.get('id','receipt')}.png"
        path = fd.asksaveasfilename(defaultextension=".png", initialfile=default_name,
                                    filetypes=[("PNG image","*.png")])
        if not path:
            return
        try:
            self._write_image(path)
            messagebox.showinfo("Saved", f"Saved image to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")

    def _write_image(self, path):
        # Render receipt text into an image using Pillow
        txt = self.format_receipt_text(self.receipt)
        # Set font: try a monospace font; fallback to default
        try:
            font = ImageFont.truetype("DejaVuSansMono.ttf", 14)
        except Exception:
            font = ImageFont.load_default()
        # Determine size
        lines = txt.splitlines()
        max_w = 0
        line_h = font.getsize("A")[1] + 2
        for ln in lines:
            w = font.getsize(ln)[0]
            if w > max_w:
                max_w = w
        img_w = max_w + 20
        img_h = line_h * (len(lines) + 2)
        img = Image.new("RGB", (img_w, img_h), "white")
        draw = ImageDraw.Draw(img)
        y = 5
        for ln in lines:
            draw.text((5, y), ln, font=font, fill="black")
            y += line_h
        img.save(path)

    def print_receipt(self):
        # Export temp PDF and send to default printer (Windows)
        try:
            fd = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            fd.close()
            tmp_path = fd.name
            self._write_pdf(tmp_path)
            # Windows printing:
            if os.name == "nt":
                # This will send to default printer (it may open an app to print)
                os.startfile(tmp_path, "print")
                messagebox.showinfo("Printing", "Sent to printer (default).")
            else:
                # On other OSes, try lpr if available
                try:
                    import subprocess
                    subprocess.run(["lp", tmp_path], check=True)
                    messagebox.showinfo("Printing", "Sent to printer.")
                except Exception:
                    messagebox.showwarning("Printing", f"Could not print automatically. PDF saved to {tmp_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print: {e}")