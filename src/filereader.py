import tkinter as tk
from tkinter import filedialog
from bibtex import parse_bibtex_file, bibtex_titles, bibtex_differences


class FileReader:
    ocrefs = None

    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack(expand=False)
        self.textpane = tk.Frame(master)
        self.textpane.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        # set a text pane with a scrollbar
        scrollbar = tk.Scrollbar(self.textpane)
        self.text = tk.Text(self.textpane, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text.pack(fill=tk.BOTH, expand=True)

        self.text.insert(tk.END, "Please choose a Google file and an ORCID file above.")

        self.gsbutton = tk.Button(self.frame, text="Choose the Google Scholar file", fg='black',
                                  command=lambda: self.get_file("Google"))
        self.gsbutton.grid(row=0, column=0)
        self.gsrefs = tk.Label(self.frame, text="No references read yet")
        self.gsrefs.grid(row=0, column=1)

        self.ocbutton = tk.Button(self.frame, text="Choose the ORCID file", fg='black',
                                  command=lambda: self.get_file("ORCID"))
        self.ocbutton.grid(row=1, column=0)
        self.ocrefs = tk.Label(self.frame, text="No references read yet")
        self.ocrefs.grid(row=1, column=1)
        self.gnoto = tk.Button(self.frame, text="Google Not ORCID", command=self.google_not_orcid, state="disabled")
        self.comp = tk.Button(self.frame, text="Compare Both", command=self.compare_refs, state="disabled")
        self.onotg = tk.Button(self.frame, text="ORCID Not Google", command=self.orcid_not_google, state="disabled")
        self.comp.grid(row=2, columnspan=2)
        self.gnoto.grid(row=3, column=0)
        self.onotg.grid(row=3, column=1)
        self.google_file = None
        self.orcid_file = None
        self.google_bib = None
        self.orcid_bib = None
        self.google_titles = None
        self.orcid_titles = None
        self.g_bib = None
        self.o_bib = None

    def get_file(self, which):
        filetypes = (
            ('Text files', '*.TXT'),
            ('Bib files', '*.BIB'),
            ('All files', '*.*'),
        )

        filename = tk.filedialog.askopenfilename(
            title=f'Choose the {which} file...',
            filetypes=filetypes,
        )
        if not filename:
            return

        if which == "Google":
            self.gsbutton.config(state="disabled")
            self.google_file = filename
            self.google_bib = parse_bibtex_file(self.google_file, False)
            self.google_titles = bibtex_titles(self.google_bib, False)
            self.gsrefs.config(text=f"Read {len(self.google_titles)} references")

        if which == 'ORCID':
            self.ocbutton.config(state="disabled")
            self.orcid_file = filename
            self.orcid_bib = parse_bibtex_file(self.orcid_file, False)
            self.orcid_titles = bibtex_titles(self.orcid_bib, False)
            self.ocrefs.config(text=f"Read {len(self.orcid_titles)} references")

        if self.orcid_file and self.google_file:
            self.comp.config(state="active")
            self.gnoto.config(state="active")
            self.onotg.config(state="active")
            self.text.delete(1.0, 'end')
            self.g_bib, self.o_bib = bibtex_differences(self.google_bib, self.google_titles, self.orcid_bib,
                                                        self.orcid_titles, False)
            self.text.insert(tk.END, "Ready to compare the files!")
        elif self.orcid_file:
            self.text.delete(1.0, 'end')
            self.text.insert(tk.END, "Please choose a Google file above.")
        elif self.google_file:
            self.text.delete(1.0, 'end')
            self.text.insert(tk.END, "Please choose an ORCID file above.")

    def compare_refs(self):
        self.text.delete(1.0, 'end')
        self.text.insert(tk.END, "REFERENCES IN GOOGLE NOT ORCID\n")
        self.text.insert(tk.END, self.g_bib.to_string("bibtex"))

        self.text.insert(tk.END, "\n\n\nREFERENCES IN ORCID NOT GOOGLE\n")
        self.text.insert(tk.END, self.o_bib.to_string("bibtex"))

    def google_not_orcid(self):
        self.text.delete(1.0, 'end')
        self.text.insert(tk.END, "REFERENCES IN GOOGLE NOT ORCID\n")
        self.text.insert(tk.END, self.g_bib.to_string("bibtex"))

    def orcid_not_google(self):
        self.text.delete(1.0, 'end')
        self.text.insert(tk.END, "REFERENCES IN ORCID NOT GOOGLE\n")
        self.text.insert(tk.END, self.o_bib.to_string("bibtex"))
