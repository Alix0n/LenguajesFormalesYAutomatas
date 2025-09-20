import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from automata.fa.dfa import DFA


class DFAViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Taller 1. Ejercicio 1")
        self.root.geometry("900x600")

        self.dfa = DFA(
            states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'},
            input_symbols={'a', 'b'},
            transitions={
                'q0': {'a': 'q2', 'b': 'q1'},
                'q1': {'a': 'q3', 'b': 'q6'},
                'q2': {'a': 'q4', 'b': 'q5'},
                'q3': {'a': 'q4', 'b': 'q5'},
                'q4': {'a': 'q4', 'b': 'q5'},
                'q5': {'a': 'q4', 'b': 'q6'},
                'q6': {'a': 'q6', 'b': 'q6'}
            },
            initial_state='q0',
            final_states={'q4'}
        )

        self.setup_ui()
        self.draw_dfa()

    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.graph_frame = tk.Frame(main_frame, bg="#E8AFA7")
        self.graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        control_frame = tk.Frame(main_frame, width=300, bg='#CAEDE0')
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        control_frame.pack_propagate(False)

        controls_inner = tk.Frame(control_frame, bg='#CAEDE0')
        controls_inner.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(controls_inner, text="Cadena:", bg='#CAEDE0',
                 font=('Times New Roman', 13, 'bold')).pack(pady=5)
        self.entry = tk.Entry(controls_inner, width=22, font=('Times New Roman', 11))
        self.entry.pack(pady=5)

        tk.Button(controls_inner, text="Definición Formal", command=self.show_definition,
                  bg="#83AEF4", font=('Arial', 11, 'bold'), width=18, height=2).pack(pady=8)
        
        tk.Button(controls_inner, text="Verificar Cadena", command=self.verify_string,
                  bg='#D2B1E6', font=('Arial', 11, 'bold'), width=18, height=2).pack(pady=8)

        tk.Button(controls_inner, text="Ver Traza", command=self.show_process,
                  bg='#E6B1B4', font=('Arial', 11, 'bold'), width=18, height=2).pack(pady=8)

        tk.Button(controls_inner, text="Cargar Archivo", command=self.load_file,
                  bg='#BCE6B1', font=('Arial', 11, 'bold'), width=18, height=2).pack(pady=8)

        self.result_label = tk.Label(controls_inner, text="", bg='#CAEDE0',
                                     font=('Arial', 13, 'bold'))
        self.result_label.pack(pady=10)

    def draw_dfa(self):
        fig, ax = plt.subplots(figsize=(6, 5))

        fig.patch.set_facecolor("#EFE1DF")  
        ax.set_facecolor("#FFF8F6")   

        G = nx.DiGraph()

        for state in self.dfa.states:
            G.add_node(state)

        for from_state, transitions in self.dfa.transitions.items():
            for symbol, to_state in transitions.items():
                if G.has_edge(from_state, to_state):
                    G[from_state][to_state]['label'] += f',{symbol}'
                else:
                    G.add_edge(from_state, to_state, label=symbol)

        pos = nx.spring_layout(G, k=2, iterations=50)

        nx.draw_networkx_nodes(G, pos, node_color='#D6B26B',
                               node_size=900, ax=ax)

        nx.draw_networkx_nodes(G, pos, nodelist=[self.dfa.initial_state],
                               node_color='#88C8DB', node_size=1000, ax=ax)

        nx.draw_networkx_nodes(G, pos, nodelist=list(self.dfa.final_states),
                               node_color='#99DB88', node_size=1000, ax=ax)

        nx.draw_networkx_edges(G, pos, edge_color='gray',
                               connectionstyle="arc3,rad=0.1",
                               arrows=True, arrowsize=20,
                               arrowstyle='->', ax=ax)

        nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)

        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=9, ax=ax)

        ax.set_title("Autómata Finito Determinista - Ejercicio 1")
        ax.axis('off')

        canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_definition(self):
        definicion = (
            "El autómata se define como:\n\n"
            "A = (Q, Σ, δ, q0, F)\n\n"
            "donde:\n"
            "Q = {q0, q1, q2, q3, q4, q5, q6}\n"
            "Σ = {a, b}\n"
            "q0 es el estado inicial\n"
            "F = {q4}\n"
            "δ es la función de transición descrita en la tabla de transición.\n\n"
            "Lenguaje reconocido:\n"
            "L1 = { w ∈ {a, b}* | #a(w) ≥ 2 ∧ bb ∉ w ∧ w termina en a }\n"
        )
        messagebox.showinfo("Definición Formal", definicion)

    def verify_string(self):
        string = self.entry.get().strip()
        try:
            if self.dfa.accepts_input(string):
                self.result_label.config(text="ACEPTADA", fg='green')
            else:
                self.result_label.config(text="RECHAZADA", fg='red')
        except:
            self.result_label.config(text="ERROR", fg='red')

    def show_process(self):
        string = self.entry.get().strip()
        try:
            current_state = self.dfa.initial_state
            process = [f"Estado inicial: {current_state}"]

            for symbol in string:
                next_state = self.dfa.transitions[current_state][symbol]
                process.append(f"{current_state} - {symbol} -> {next_state}")
                current_state = next_state

            final_status = "ACEPTADA" if current_state in self.dfa.final_states else "RECHAZADA"
            process.append(f"Estado final: {current_state} - {final_status}")

            messagebox.showinfo("Traza", "\n".join(process))
        except:
            messagebox.showerror("Error", "Cadena inválida")

    
    def load_file(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            try:
                with open(filename, 'r') as f:
                    strings = [line.strip() for line in f.readlines() if line.strip()]

                result_window = tk.Toplevel(self.root)
                result_window.title("Cadenas leidas")
                result_window.geometry("650x450")

                main_frame = tk.Frame(result_window)
                main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

                tree = ttk.Treeview(main_frame, columns=("Numero", "Cadena", "Resultado"), show="headings", height=15)
                tree.heading("Numero", text="#")
                tree.heading("Cadena", text="Cadena")
                tree.heading("Resultado", text="Resultado")

                tree.column("Numero", width=40, anchor="center")
                tree.column("Cadena", width=250, anchor="center")
                tree.column("Resultado", width=150, anchor="center")

                scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)

                tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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
