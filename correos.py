import string
from automata.fa.dfa import DFA

class CorreoUPTC:
    def __init__(self):

        letters_lower = set(string.ascii_lowercase)  
        digits = set(string.digits)                  
        specials = {'@', '.'}                        
        self.symbols = letters_lower | digits | specials

        def all_to(state):
            return {s: state for s in self.symbols}

        transitions = {}
        t = all_to('q14')
        for ch in letters_lower:
            t[ch] = 'q1'
        transitions['q0'] = t
        t = all_to('q14')
        for ch in (letters_lower | digits):
            t[ch] = 'q1'
        t['@'] = 'q2'
        transitions['q1'] = t
        transitions['q2']  = all_to('q14'); transitions['q2']['u'] = 'q3'
        transitions['q3']  = all_to('q14'); transitions['q3']['p'] = 'q4'
        transitions['q4']  = all_to('q14'); transitions['q4']['t'] = 'q5'
        transitions['q5']  = all_to('q14'); transitions['q5']['c'] = 'q6'
        transitions['q6']  = all_to('q14'); transitions['q6']['.'] = 'q7'
        transitions['q7']  = all_to('q14'); transitions['q7']['e'] = 'q8'
        transitions['q8']  = all_to('q14'); transitions['q8']['d'] = 'q9'
        transitions['q9']  = all_to('q14'); transitions['q9']['u'] = 'q10'
        transitions['q10'] = all_to('q14'); transitions['q10']['.'] = 'q11'
        transitions['q11'] = all_to('q14'); transitions['q11']['c'] = 'q12'
        transitions['q12'] = all_to('q14'); transitions['q12']['o'] = 'q13'
        transitions['q13'] = all_to('q14')
        transitions['q14'] = all_to('q14')

        self.dfa = DFA(
            states={f'q{i}' for i in range(15)},
            input_symbols=self.symbols,
            transitions=transitions,
            initial_state='q0',
            final_states={'q13'}
        )

    def validar(self, cadena: str) -> bool:
        """Valida la cadena:
           - devuelve False si contiene símbolos no permitidos (mayúsculas, espacios, etc.)
           - en caso contrario devuelve el resultado del DFA
        """
        if not cadena:
            return False

        for ch in cadena:
            if ch not in self.symbols:
                return False

        try:
            return self.dfa.accepts_input(cadena)
        except Exception:
            return False


if __name__ == "__main__":
    automata = CorreoUPTC()

  #  pruebas = [
      #  "juan3@uptc.edu.co",  
      #  "maria@uptc.edu.co",   
      #  "abc123@uptc.edu.co",  
       # "123juan@uptc.edu.co", 
       # "MARIA@uptc.edu.co"   
   # ]

   # for cadena in pruebas:
   #     print(f"{cadena:30} -> {'Aceptado ' if automata.validar(cadena) else 'Rechazado'}")

    while True:
        s = input("Ingresa cadena: ").strip()
        if s.lower() == 'salir':
            break
        print("Resultado:", "Aceptada " if automata.validar(s) else "Rechazada ")
