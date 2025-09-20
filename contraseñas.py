import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from automata.fa.nfa import NFA
import string

class DFAViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Taller 2 - Ejercicio 1")
        self.root.geometry("900x600")

        # Definir símbolos de entrada
        letters_upper = set(string.ascii_uppercase)  # A-Z
        letters_lower = set(string.ascii_lowercase)  # a-z
        digits = set(string.digits)  # 0-9

        # Crear el AFN según la tabla
        self.dfa = NFA(
            states={'P1', 'P2', 'P3', 'P4'},  
            input_symbols=letters_upper | letters_lower | digits,
            transitions={
                'P1': {ch: {'P2', 'P4'} for ch in letters_upper},
                'P2': {ch: {'P2'} for ch in letters_lower} |
                      {ch: {'P3'} for ch in digits}, 
                'P3': {ch: {'P3'} for ch in digits},
                'P4': {ch: {'P3'} for ch in digits},
            },
            initial_state='P1',
            final_states={'P3'}
        )

        self.setup_ui()
        self.draw_dfa()

    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Panel gráfico
        self.graph_frame = tk.Frame(main_frame, bg="#CFCAED")
        self.graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Panel de controles
        control_frame = tk.Frame(main_frame, width=300, bg="#CFCAED")
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        control_frame.pack_propagate(False)

        controls_inner = tk.Frame(control_frame, bg="#CFCAED")
        controls_inner.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(controls_inner, text="Cadena:", bg='#CFCAED',
                 font=('Times New Roman', 13, 'bold')).pack(pady=5)
        self.entry = tk.Entry(controls_inner, width=22, font=('Times New Roman', 11))
        self.entry.pack(pady=5)

        tk.Button(controls_inner, text="Verificar Cadena", command=self.verify_string,
                  bg="#E6B1C3", font=('Arial', 11, 'bold'), width=18, height=2).pack(pady=8)

        tk.Button(controls_inner, text="Cargar Archivo", command=self.load_file,
                  bg="#D1B1E6", font=('Arial', 11, 'bold'), width=18, height=2).pack(pady=8)

        self.result_label = tk.Label(controls_inner, text="", bg='#CFCAED',
                                     font=('Arial', 13, 'bold'))
        self.result_label.pack(pady=10)

    def draw_dfa(self):
        fig, ax = plt.subplots(figsize=(6, 5))
        fig.patch.set_facecolor("#DFEFE7")
        ax.set_facecolor("#FFF8F6")

        G = nx.DiGraph()

        for state in self.dfa.states:
            G.add_node(state)

        # Posiciones fijas para claridad
        pos = {'P1': (0, 0), 'P2': (3, 1), 'P3': (6, 0), 'P4': (3, -1)}

        # Agrupar transiciones en [A-Z], [a-z], [0-9]
        for from_state, transitions in self.dfa.transitions.items():
            grouped = {}
            for symbol, to_states in transitions.items():
                for to_state in to_states:
                    if symbol in string.ascii_uppercase:
                        symbol_group = '[A-Z]'
                    elif symbol in string.ascii_lowercase:
                        symbol_group = '[a-z]'
                    elif symbol in string.digits:
                        symbol_group = '[0-9]'
                    else:
                        symbol_group = symbol

                    grouped.setdefault((from_state, to_state), set()).add(symbol_group)

            for (f, t), groups in grouped.items():
                G.add_edge(f, t, label=",".join(sorted(groups)))

        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, node_color='#D6B26B', node_size=900, ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=[self.dfa.initial_state],
                               node_color='#88C8DB', node_size=1000, ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=list(self.dfa.final_states),
                               node_color='#99DB88', node_size=1000, ax=ax)

        # Dibujar aristas
        nx.draw_networkx_edges(G, pos, edge_color='gray',
                               connectionstyle="arc3,rad=0.1",
                               arrows=True, arrowsize=20,
                               arrowstyle='->', ax=ax)

        # Etiquetas
        nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=9, ax=ax)

        ax.set_title("Sistema de seguridad informática para contraseñas temporales", fontweight='bold')
        ax.axis('off')

        canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def verify_string(self):
        string = self.entry.get().strip()
        try:
            if self.dfa.accepts_input(string):
                self.result_label.config(text="ACEPTADA", fg='green')
            else:
                self.result_label.config(text="RECHAZADA", fg='red')
        except Exception as e:
            self.result_label.config(text=f"ERROR: {e}", fg='red')

    def load_file(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            try:
                with open(filename, 'r') as f:
                    strings = [line.strip() for line in f.readlines() if line.strip()]

                # Crear ventana de resultados
                result_window = tk.Toplevel(self.root)
                result_window.title("Cadenas leidas")
                result_window.geometry("750x550")

                # Frame principal
                main_frame = tk.Frame(result_window)
                main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

                # Treeview con numeración
                tree = ttk.Treeview(main_frame, columns=("Numero", "Cadena", "Resultado"), show="headings", height=15)
                tree.heading("Numero", text="#")
                tree.heading("Cadena", text="Cadena")
                tree.heading("Resultado", text="Resultado")

                tree.column("Numero", width=40, anchor="center")
                tree.column("Cadena", width=250, anchor="center")
                tree.column("Resultado", width=150, anchor="center")

                # Scrollbar
                scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)

                tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                # Procesar cadenas
                for idx, s in enumerate(strings, start=1):
                    try:
                        accepted = self.dfa.accepts_input(s)
                        result = "ACEPTADA" if accepted else "RECHAZADA"
                        tree.insert("", "end", values=(idx, s, result))
                    except:
                        tree.insert("", "end", values=(idx, s, "ERROR"))

            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar archivo: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DFAViewer(root)
    root.mainloop()
