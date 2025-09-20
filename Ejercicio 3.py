import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from automata.fa.dfa import DFA


class DFAViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Construcción de un Software")
        self.root.geometry("900x600")

        self.dfa = DFA(
            states={'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7'},
            input_symbols={'1', '0'},
            transitions={
                'F0': {'1': 'F1', '0': 'F0'},
                'F1': {'1': 'F2', '0': 'F1'},
                'F2': {'1': 'F3', '0': 'F2'},
                'F3': {'1': 'F4', '0': 'F3'},
                'F4': {'1': 'F5', '0': 'F4'},
                'F5': {'1': 'F6', '0': 'F5'},
                'F6': {'1': 'F7', '0': 'F6'},
                'F7': {'1': 'F7', '0': 'F6'}
            },
            initial_state='F0',
            final_states={'F7'}
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

        ax.set_title("Construcción de un Software")
        ax.axis('off')

        canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_definition(self):
        definicion = (
            "El autómata se define como:\n\n"
            "A = (Q, Σ, δ, q0, F)\n\n"
            "donde:\n"
            "Q = {F0, F1, F2, F3, F4, F5, F6, F7}\n"
            "Σ = {1, 0}\n"
            "F0 es el estado inicial\n"
            "F = {F7}\n"
            "δ es la función de transición descrita en la tabla de transición.\n\n"
            "Lenguaje reconocido:\n"
            "L = { w ∈ Σ* | |w| ≥ 7 ∧ w termina en 1 }\n"
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
