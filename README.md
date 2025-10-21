# Left Recursion Elimination Algorithm

This project implements the left recursion elimination algorithm for Context-Free Grammars (CFG) as presented in Aho's Compilers book. The algorithm systematically removes both immediate and indirect left recursion from grammar productions.

---

## 👥 Student Names

- **Pablo José Benítez Trujillo**
- **Juan Hernandez Martelo**

---

## 🏫 Class Number

**Lenguajes Formales-C2566-SI2002-5730**

---

## 💻 OS Version

**Windows 10/11**

---

## 🐍 Language and Libraries

- **Language:** Python 3
- **Libraries:**
  - **sys:** Standard library for:
    - `sys.argv`: Command-line argument handling
    - `sys.stdin`: Input stream management
  - **io:** Standard library for:
    - `io.StringIO`: String buffer manipulation for input redirection

---

## 🚀 Mission

Provide an efficient implementation for eliminating left recursion in context-free grammars, facilitating the learning and practical application of compiler design algorithms.

---

## ⚙️ Algorithm Methodology

The algorithm operates in **three well-defined sequential phases** following Aho's textbook approach:

### 1️⃣ Grammar Ordering and Setup Phase

All non-terminals are ordered in a specific sequence (A₁, A₂, ..., Aₙ). This ordering is crucial for the systematic elimination of both immediate and indirect left recursion. The algorithm maintains a set of used non-terminals to generate new symbols when needed.

### 2️⃣ Substitution and Expansion Phase

This is the core iterative phase of the algorithm:
- For each non-terminal Aᵢ (i = 1 to n):
  - For each j < i, replace productions of the form Aᵢ → Aⱼγ by expanding all productions of Aⱼ
  - This substitution eliminates indirect left recursion by converting it into immediate left recursion
- The process continues systematically through all non-terminals in order

### 3️⃣ Immediate Recursion Elimination Phase

For each non-terminal with immediate left recursion:
- Productions of the form A → Aα₁ | Aα₂ | ... | Aαₘ | β₁ | β₂ | ... | βₙ
- Are transformed into:
  - A → β₁A' | β₂A' | ... | βₙA'
  - A' → α₁A' | α₂A' | ... | αₘA' | ε
- A new non-terminal A' is introduced to handle the recursive part
- The result is a grammar without left recursion

---

## ✨ Implementation Features

- **Dual Mode Operation:** 
  - Command-line mode for direct grammar input
  - Interactive mode for step-by-step grammar processing
- **Flexibility:** Handles both simple and complex grammars with multiple productions
- **Robustness:** Automatic generation of new non-terminals without conflicts
- **User-Friendly:** Clear output formatting with input/output separation
- **Batch Processing:** Can process multiple grammars in a single execution

---

## 🛠️ How to Run the Code?

### **Method 1: Command-Line Mode**

Run the script with a grammar as an argument:

```powershell
python run_prueba.py "A -> Aa | b"
```

### **Method 2: Interactive Mode**

Run the script without arguments for interactive mode:

```powershell
python run_prueba.py
```

Then follow the prompts to enter your grammar.

### **Method 3: Input File Method**

1. **Prepare the Input File**  
   Create a file named `input.txt` with the following structure:

2. **Run the Command**  
   ```powershell
   Get-Content input.txt | python run_prueba.py
   ```

---

## 📄 Input File Format

The `input.txt` file should follow this structure:

- **First line:** Number of grammars (n)
- **For each grammar:**
  - **First line:** Number of non-terminals (k)
  - **Next k lines:** Productions in the format: `NonTerminal -> production1 | production2 | ...`

---

### 📝 Example Input

```text
2
1
A -> Aa | b
2
S -> Sa | Sb | c
E -> E+T | T
```

### 📤 Example Output

```text
A -> bB
B -> aB | e

S -> cC
C -> aC | bC | e
E -> TD
D -> +TD | e
```

---

## 🎯 Grammar Input Format

When entering a grammar (either via command-line or interactive mode), use this format:

- Use `->` to separate the non-terminal from its productions
- Use `|` to separate alternative productions
- Example: `A -> Aa | Ab | c`

---

## 📚 Reference

- Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Addison-Wesley.

---

> This implementation provides an efficient and robust approach to left recursion elimination, following high academic standards and compiler design best practices.
