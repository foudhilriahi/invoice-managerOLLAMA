import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ocr import extract_text
from ollama_llm import generate_invoice_json
from database import insert_invoice, fetch_all_invoices, fetch_invoice_raw_json
from utils import is_valid_json
import json
import csv
from config import AVAILABLE_MODELS, SELECTED_MODEL

class InvoiceApp:
    def __init__(self, root):
        self.root = root
        root.title("Offline Invoice Manager")
        root.geometry("1150x780")

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=True, fill='both')

        self.tab_process = ttk.Frame(self.tabs)
        self.tab_viewer = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_process, text="Process Invoice")
        self.tabs.add(self.tab_viewer, text="View Invoices")

        self.model_var = tk.StringVar(value=SELECTED_MODEL)

        self.build_process_tab()
        self.build_viewer_tab()
        self.load_invoices()

    def build_process_tab(self):
        frame = self.tab_process

        tk.Label(frame, text="Select LLM Model:", font=("Arial", 12)).pack(pady=5)
        model_dropdown = ttk.Combobox(frame, textvariable=self.model_var, values=AVAILABLE_MODELS, state="readonly", width=15)
        model_dropdown.pack(pady=2)

        tk.Button(frame, text="Upload Invoice File", command=self.process_file, font=("Arial", 12)).pack(pady=10)

        self.text_box = tk.Text(frame, wrap=tk.WORD, height=30, width=140)
        self.text_box.pack(pady=10)

    def build_viewer_tab(self):
        frame = self.tab_viewer

        columns = ("ID", "Summary")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', height=28)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Summary", text="Summary (Supplier / Invoice Number / Date / Total)")
        self.tree.column("ID", width=60, anchor=tk.CENTER)
        self.tree.column("Summary", width=1050, anchor=tk.W)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        btn_export = tk.Button(frame, text="Export All to CSV", command=self.export_csv)
        btn_export.pack(side=tk.TOP, padx=10, pady=10)

        self.tree.bind("<Double-1>", self.on_invoice_select)

    def load_invoices(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        invoices = fetch_all_invoices()
        for inv_id, raw_json in invoices:
            try:
                data = json.loads(raw_json)
                supplier = data.get("supplier", "N/A")
                invoice_number = data.get("invoice_number", "N/A")
                date = data.get("date", "N/A")
                total = data.get("total_amount", data.get("total", "N/A"))
                summary = f"{supplier} / {invoice_number} / {date} / {total}"
            except Exception:
                summary = "Invalid JSON"

            self.tree.insert("", "end", values=(inv_id, summary))

    def export_csv(self):
        invoices = fetch_all_invoices()
        if not invoices:
            messagebox.showinfo("Export CSV", "No invoices to export.")
            return

        all_keys = set()
        json_objs = []
        for _, raw_json in invoices:
            try:
                obj = json.loads(raw_json)
                json_objs.append(obj)
                all_keys.update(obj.keys())
            except Exception:
                pass

        all_keys = sorted(all_keys)

        filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv")],
                                                title="Save invoices as CSV")
        if not filepath:
            return

        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID"] + all_keys)
                for idx, obj in zip([inv[0] for inv in invoices], json_objs):
                    row = [idx] + [obj.get(k, "") for k in all_keys]
                    writer.writerow(row)
            messagebox.showinfo("Export CSV", f"Successfully exported {len(invoices)} invoices.")
        except Exception as e:
            messagebox.showerror("Export CSV", f"Failed to export CSV:\n{e}")

    def on_invoice_select(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        item = self.tree.item(selected_item)
        invoice_id = item['values'][0]

        raw_json = fetch_invoice_raw_json(invoice_id)
        if not raw_json:
            messagebox.showinfo("Details", "No detail data found.")
            return

        try:
            data = json.loads(raw_json)
        except Exception:
            messagebox.showerror("Error", "Invoice JSON corrupted or invalid.")
            return

        text = "\n".join(f"{k}: {v}" for k, v in data.items())

        detail_win = tk.Toplevel(self.root)
        detail_win.title(f"Invoice #{invoice_id} Details")
        detail_win.geometry("600x600")
        text_box = tk.Text(detail_win, width=80, height=35)
        text_box.pack(padx=10, pady=10)
        text_box.insert(tk.END, text)
        text_box.config(state=tk.DISABLED)

    def process_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF/Images", "*.pdf *.png *.jpg *.jpeg")])
        if not file_path:
            return

        self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, f"📥 Loading file: {file_path}\n")

        try:
            ocr_text = extract_text(file_path)
            self.text_box.insert(tk.END, f"\n📄 OCR Text:\n{ocr_text}\n")

            selected_model = self.model_var.get()
            llm_output = generate_invoice_json(ocr_text, model_name=selected_model)
            self.text_box.insert(tk.END, f"\n🤖 LLM Output (Model: {selected_model}):\n{llm_output}\n")

            valid, data = is_valid_json(llm_output)
            if valid:
                insert_invoice(data)
                self.text_box.insert(tk.END, "\n✅ Invoice saved to database.\n")

                self.text_box.insert(tk.END, "\n💡 Parsed Invoice Data:\n")
                for k, v in data.items():
                    self.text_box.insert(tk.END, f"{k}: {v}\n")

                self.load_invoices()
            else:
                self.text_box.insert(tk.END, "\n❌ Invalid JSON returned.\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))
