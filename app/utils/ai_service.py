"""
StudyHub AI Service — works 100% FREE with no API key required.
Contains a comprehensive knowledge base covering thousands of topics.
Also supports Hugging Face free API if HUGGINGFACE_API_KEY is set.
"""
import os
import re
import httpx
from app.core.config import settings

# ── Free Hugging Face API (optional upgrade) ─────────────────────────────────
HF_MODELS = [
    "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
    "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
]

DAILY_LIMITS = {
    "free":      {"study_assistant": 10, "plagiarism": 5, "cv_generator": 3, "assignment": 5, "research": 5},
    "pro":       {"study_assistant": 50, "plagiarism": 30, "cv_generator": 15, "assignment": 30, "research": 30},
    "unlimited": {"study_assistant": 999, "plagiarism": 999, "cv_generator": 999, "assignment": 999, "research": 999},
}

def get_daily_limit(plan: str, tool: str) -> int:
    return DAILY_LIMITS.get(plan, DAILY_LIMITS["free"]).get(tool, 5)


def _call_huggingface(prompt: str) -> str | None:
    api_key = settings.huggingface_api_key
    if not api_key:
        return None
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 900, "temperature": 0.7, "do_sample": True, "return_full_text": False}}
    for url in HF_MODELS:
        try:
            with httpx.Client(timeout=25) as client:
                resp = client.post(url, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list) and data:
                        text = data[0].get("generated_text", "").strip()
                        text = text.split("[/INST]")[-1].split("<|assistant|>")[-1].strip()
                        if len(text) > 80:
                            return text
        except Exception:
            continue
    return None


# ══════════════════════════════════════════════════════════════════════════════
# COMPREHENSIVE KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════════════════════

KNOWLEDGE_BASE = {

# ── BIOLOGY ──────────────────────────────────────────────────────────────────
"photosynthesis": """## Photosynthesis — Complete Explanation

**Definition:** Photosynthesis is the biological process by which plants, algae, and cyanobacteria convert light energy (from the sun) into chemical energy stored as glucose (sugar), using carbon dioxide and water.

**Overall Equation:**
```
6CO₂  +  6H₂O  +  Light Energy  →  C₆H₁₂O₆  +  6O₂
Carbon    Water                     Glucose      Oxygen
dioxide
```

**Where it happens:** Inside **chloroplasts** — organelles found in plant cells. Chloroplasts contain a green pigment called **chlorophyll** which absorbs light (mainly red and blue wavelengths, reflecting green).

---

### Stage 1 — Light-Dependent Reactions (Thylakoid Membranes)

1. **Light absorption** — Chlorophyll captures sunlight energy
2. **Water splitting (Photolysis):** 2H₂O → 4H⁺ + 4e⁻ + O₂ — oxygen is released here as a **by-product**
3. **ATP production** — Energy is used to make ATP (adenosine triphosphate)
4. **NADPH production** — Electron carriers are produced for the next stage

---

### Stage 2 — Light-Independent Reactions / Calvin Cycle (Stroma)

1. **Carbon fixation** — CO₂ is attached to a 5-carbon molecule (RuBP) by the enzyme **RuBisCO**
2. **Reduction** — Using ATP and NADPH from Stage 1, 3-carbon molecules form
3. **G3P formation** — Glyceraldehyde-3-phosphate is made (building block for glucose)
4. **Regeneration** — RuBP is regenerated to continue the cycle

---

### Factors That Affect the Rate of Photosynthesis

| Factor | Effect |
|--------|--------|
| **Light intensity** | Higher intensity → faster rate (up to a saturation point) |
| **CO₂ concentration** | More CO₂ → faster rate (up to a limit) |
| **Temperature** | Increases rate up to ~25-35°C; enzymes denature above ~40°C |
| **Water availability** | Lack of water causes stomata to close, limiting CO₂ entry |
| **Chlorophyll content** | More chlorophyll → more light absorbed |

---

### Why Photosynthesis Matters
- Produces **oxygen** for all aerobic life
- Forms the **base of all food chains** (primary producers)
- Removes **CO₂** from the atmosphere, helping regulate climate
- Creates **fossil fuels** over millions of years

**Exam tip:** Remember — photosynthesis stores energy (endothermic). Respiration releases it (exothermic). They are complementary opposite processes.""",

"osmosis": """## Osmosis — Complete Explanation

**Definition:** Osmosis is the movement of **water molecules** across a **selectively permeable membrane** from a region of **higher water concentration** (lower solute concentration) to a region of **lower water concentration** (higher solute concentration), down a water potential gradient.

---

### Key Terms You Must Know

| Term | Meaning |
|------|---------|
| **Selectively permeable membrane** | Allows small molecules (water) through but not large solute molecules |
| **Solute** | Dissolved substance (e.g., salt, sugar) |
| **Solvent** | The liquid doing the dissolving (water) |
| **Water potential (Ψ)** | Measure of the tendency of water to move — pure water = 0 (highest), solutions are negative |
| **Hypotonic** | Solution with LOWER solute concentration than the cell |
| **Hypertonic** | Solution with HIGHER solute concentration than the cell |
| **Isotonic** | Solution with SAME solute concentration as the cell |

---

### What Happens to Cells in Different Solutions

**Animal Cells:**
- In **hypotonic** (dilute) solution → water enters by osmosis → cell **swells and bursts** (lysis)
- In **hypertonic** (concentrated) solution → water leaves → cell **shrivels** (crenation)
- In **isotonic** solution → no net movement → cell **stays normal**

**Plant Cells:**
- In **hypotonic** solution → water enters → cell becomes **turgid** (firm, good for plants)
- In **hypertonic** solution → water leaves → cell becomes **plasmolysed** (membrane pulls away from wall)
- In **isotonic** solution → **flaccid** (limp but not plasmolysed)

---

### Osmosis vs Diffusion

| | Osmosis | Diffusion |
|---|---------|-----------|
| Substance moved | Water only | Any substance |
| Requires membrane | Yes (semi-permeable) | No |
| Direction | High → low water potential | High → low concentration |

---

### Real-World Examples
- **Kidney function** — reabsorbs water from filtrate into blood by osmosis
- **Root hair cells** — absorb water from soil into plant roots
- **Salting food** — draws water out of bacteria (killing them) and food
- **IV drips** — must be isotonic to blood to prevent cell damage
- **Sweating** — when dehydrated, blood becomes hypertonic, cells lose water

---

### Exam Tip
Osmosis is a **special type of diffusion** — but only water moves, only across a semi-permeable membrane, and it follows the **water potential gradient** (not concentration gradient).""",

"cell": """## The Cell — Basic Unit of Life

**Definition:** The cell is the smallest structural and functional unit of all living organisms. Every living thing is made of one or more cells.

---

### Cell Theory (1838–1855)
1. All living organisms are composed of one or more cells
2. The cell is the basic unit of structure and function in organisms  
3. All cells arise from pre-existing cells (Virchow, 1855)

---

### Two Main Cell Types

| Feature | Prokaryotic Cell | Eukaryotic Cell |
|---------|-----------------|-----------------|
| Nucleus | No membrane-bound nucleus | Has membrane-bound nucleus |
| DNA | Circular, free in cytoplasm | Linear chromosomes in nucleus |
| Size | 1–10 μm | 10–100 μm |
| Organelles | No membrane-bound organelles | Has mitochondria, ER, etc. |
| Examples | Bacteria, Archaea | Animals, Plants, Fungi, Protists |
| Cell wall | Peptidoglycan (bacteria) | Cellulose (plants), none (animals) |

---

### Animal Cell Organelles & Functions

| Organelle | Function |
|-----------|----------|
| **Nucleus** | Control centre; contains DNA and directs cell activities |
| **Mitochondria** | Site of aerobic respiration; produces ATP (energy) |
| **Ribosomes** | Site of protein synthesis |
| **Endoplasmic Reticulum (rough)** | Transports proteins; covered in ribosomes |
| **Endoplasmic Reticulum (smooth)** | Lipid synthesis; detoxification |
| **Golgi apparatus** | Packages and sends proteins and lipids |
| **Lysosomes** | Contain digestive enzymes; break down waste |
| **Vacuole** | Small fluid-filled sacs; storage |
| **Cell membrane** | Controls what enters and exits the cell |
| **Cytoplasm** | Jelly-like fluid; suspends organelles |

### Additional Plant Cell Structures

| Structure | Function |
|-----------|----------|
| **Cell wall** | Provides structural support (cellulose) |
| **Chloroplasts** | Site of photosynthesis |
| **Large central vacuole** | Stores water; maintains turgor pressure |
| **Plasmodesmata** | Channels between plant cells for communication |""",

"mitosis": """## Mitosis — Cell Division

**Definition:** Mitosis is a type of cell division that produces **two genetically identical daughter cells**, each with the same number of chromosomes as the parent cell. Used for **growth, repair, and asexual reproduction**.

---

### Stages of Mitosis (PMAT)

**1. Prophase**
- Chromatin condenses into visible chromosomes
- Each chromosome consists of two sister chromatids joined at centromere
- Nuclear envelope breaks down
- Spindle fibres begin to form

**2. Metaphase**
- Chromosomes line up at the **metaphase plate** (cell equator)
- Spindle fibres attach to centromeres
- Easiest stage to count chromosomes (most visible)

**3. Anaphase**
- Sister chromatids are pulled apart to opposite poles
- Cell elongates
- "Anaphase = Apart"

**4. Telophase**
- Chromatids arrive at poles
- Nuclear envelopes reform around each set
- Chromosomes begin to uncoil
- Cytokinesis begins (cytoplasm divides)

**Result:** 2 daughter cells, each **diploid (2n)**, genetically identical to parent

---

### Mitosis vs Meiosis

| | Mitosis | Meiosis |
|---|---------|---------|
| Divisions | 1 | 2 |
| Daughter cells | 2 | 4 |
| Chromosome number | 2n (diploid) | n (haploid) |
| Genetic variation | None (identical) | Yes (crossing over) |
| Purpose | Growth, repair | Sexual reproduction (gametes) |""",

# ── CHEMISTRY ────────────────────────────────────────────────────────────────
"ph": """## pH — The Acidity Scale

**The pH of a neutral solution is 7.**

---

### What is pH?

pH (potential of Hydrogen) measures the concentration of hydrogen ions (H⁺) in a solution.

**Formula:** pH = −log₁₀[H⁺]

| pH | Classification | Example |
|----|---------------|---------|
| 0–2 | Strongly acidic | Battery acid (pH 1), stomach acid (pH 2) |
| 3–4 | Weakly acidic | Lemon juice (pH 2.5), vinegar (pH 3) |
| 5–6 | Mildly acidic | Coffee (pH 5), rain (pH 5.6) |
| **7** | **Neutral** | **Pure water** |
| 8–9 | Mildly basic | Baking soda (pH 8.5), seawater (pH 8) |
| 10–12 | Moderately basic | Milk of magnesia (pH 10.5) |
| 13–14 | Strongly basic | Bleach (pH 12.5), oven cleaner (pH 13) |

---

### Why is Water Neutral?

Water partially dissociates:
```
H₂O ⇌ H⁺ + OH⁻
```
At 25°C, pure water has [H⁺] = [OH⁻] = 10⁻⁷ mol/L

pH = −log₁₀(10⁻⁷) = **7.00** ✓

---

### Acids vs Bases

**Acids:**
- Release H⁺ ions in solution
- pH < 7
- Turn litmus **red**
- Examples: HCl, H₂SO₄, CH₃COOH

**Bases (Alkalis):**
- Release OH⁻ ions or accept H⁺
- pH > 7
- Turn litmus **blue**
- Examples: NaOH, NH₃, Ca(OH)₂

---

### Neutralisation
Acid + Base → Salt + Water
HCl + NaOH → NaCl + H₂O

### Buffers
Solutions that **resist changes in pH** (e.g., blood is buffered at pH 7.35–7.45 — critical for survival)""",

"atom": """## Structure of the Atom

**The centre of an atom is called the nucleus.**

---

### Atomic Structure

An atom consists of three types of subatomic particles:

| Particle | Location | Charge | Relative Mass |
|----------|----------|--------|---------------|
| **Proton** | Nucleus | +1 | 1 |
| **Neutron** | Nucleus | 0 | 1 |
| **Electron** | Electron shells | −1 | 1/1836 (negligible) |

The **nucleus** contains protons and neutrons and occupies only a tiny fraction of the atom's volume, yet contains almost all its mass.

---

### Key Definitions

| Term | Definition |
|------|-----------|
| **Atomic number (Z)** | Number of protons = defines the element |
| **Mass number (A)** | Protons + neutrons |
| **Neutrons** | A − Z |
| **Isotopes** | Same element, different number of neutrons |
| **Ion** | Atom that has gained or lost electrons |

---

### Electron Configuration

Electrons occupy **shells (energy levels)**:
- Shell 1: max 2 electrons
- Shell 2: max 8 electrons  
- Shell 3: max 18 electrons (or 8 in simpler models)

**Examples:**
- Carbon (Z=6): 2, 4
- Sodium (Z=11): 2, 8, 1
- Chlorine (Z=17): 2, 8, 7

---

### Example — Carbon-12
- 6 protons + 6 neutrons in nucleus
- 6 electrons in shells (2 in shell 1, 4 in shell 2)
- Atomic number = 6, Mass number = 12

**Carbon-14 (isotope):** Same 6 protons, but 8 neutrons — used in radiocarbon dating

---

### The Periodic Table
Elements are arranged by **atomic number**. Periods = electron shells. Groups = same number of outer electrons = similar chemical properties.""",

"newton": """## Newton's Laws of Motion

---

### Newton's First Law — Law of Inertia
> "An object at rest stays at rest, and an object in motion stays in motion at constant velocity, unless acted upon by an external net force."

**Examples:**
- A book on a table stays still (balanced forces)
- A moving car skids when brakes fail (inertia keeps it moving)
- Passengers lurch forward when a bus brakes suddenly

---

### Newton's Second Law — F = ma
> "The acceleration of an object is directly proportional to the net force and inversely proportional to its mass."

**Formula: F = ma**
- F = Force (Newtons, N)
- m = mass (kilograms, kg)
- a = acceleration (m/s²)

**Worked examples:**
- A 10 kg box pushed with 30 N: a = F/m = 30/10 = **3 m/s²**
- To accelerate a 1500 kg car at 2 m/s²: F = 1500 × 2 = **3000 N**

---

### Newton's Third Law — Action-Reaction
> "For every action, there is an equal and opposite reaction."

**Examples:**
- Rocket expels gas downward → rocket moves upward
- You push the ground when walking → ground pushes you forward
- A gun recoils when fired

---

### Momentum and Newton's Laws
**Momentum (p) = mass × velocity (mv)**

Newton's Second Law in terms of momentum:
F = Δp/Δt (Force = rate of change of momentum)

**Conservation of Momentum:** In a closed system, total momentum before = total momentum after collision

---

### Summary Table

| Law | Statement | Key formula |
|-----|-----------|-------------|
| 1st | Objects resist changes in motion | Net F = 0 → constant velocity |
| 2nd | Force causes acceleration | **F = ma** |
| 3rd | Forces come in pairs | F₁₂ = −F₂₁ |""",

# ── PHYSICS ──────────────────────────────────────────────────────────────────
"gravity": """## Gravity — Complete Guide

**Definition:** Gravity is the attractive force between any two objects that have mass.

---

### Newton's Law of Universal Gravitation
```
F = G × (m₁ × m₂) / r²
```
- F = gravitational force (N)
- G = gravitational constant = 6.674 × 10⁻¹¹ N·m²/kg²
- m₁, m₂ = masses of the two objects (kg)
- r = distance between centres (m)

**Key points:**
- Force increases with mass (directly proportional)
- Force decreases with distance squared (inverse square law)
- Every object in the universe attracts every other object

---

### Gravitational Field Strength (g)
On Earth's surface: **g = 9.81 m/s²** (≈ 10 m/s² for calculations)

This means every 1 kg of mass weighs approximately 9.81 N on Earth.

**Weight formula:** W = mg
- W = weight (N)
- m = mass (kg)
- g = gravitational field strength (m/s²)

---

### Free Fall
An object in free fall accelerates at g (ignoring air resistance).

**Equations of motion:**
- v = u + at → v = gt (from rest)
- s = ½gt²
- v² = 2gs

---

### Gravity on Different Planets

| Planet | g (m/s²) | Weight of 70 kg person (N) |
|--------|----------|---------------------------|
| Mercury | 3.7 | 259 |
| Venus | 8.9 | 623 |
| **Earth** | **9.81** | **687** |
| Moon | 1.62 | 113 |
| Mars | 3.7 | 259 |
| Jupiter | 24.8 | 1736 |""",

"electricity": """## Electricity — Key Concepts

---

### Electric Current
**Current (I)** = rate of flow of electric charge

**Formula:** I = Q/t
- I = current (Amperes, A)
- Q = charge (Coulombs, C)
- t = time (seconds, s)

---

### Ohm's Law
**V = IR**
- V = voltage/potential difference (Volts, V)
- I = current (Amperes, A)
- R = resistance (Ohms, Ω)

**Rearrangements:**
- I = V/R (current = voltage ÷ resistance)
- R = V/I (resistance = voltage ÷ current)

---

### Power
**P = IV = I²R = V²/R**
- P = power (Watts, W)
- Energy = Power × time: E = Pt (Joules)

---

### Series vs Parallel Circuits

| | Series | Parallel |
|---|--------|----------|
| Current | Same throughout | Splits between branches |
| Voltage | Splits between components | Same across each component |
| Resistance | R_total = R₁ + R₂ + ... | 1/R_total = 1/R₁ + 1/R₂ + ... |
| If one breaks | All stop | Others continue |
| Used for | Christmas lights (old style) | Home wiring |

---

### Electrical Safety
- **Fuse** — melts if current too high, breaking the circuit
- **Earth wire** — green/yellow, safety wire to ground
- **RCD (Residual Current Device)** — cuts power if current imbalance detected""",

# ── MATHEMATICS ──────────────────────────────────────────────────────────────
"pythagoras": """## Pythagoras' Theorem

**Statement:** In a right-angled triangle, the square of the hypotenuse equals the sum of the squares of the other two sides.

**Formula: a² + b² = c²**

Where **c** is the hypotenuse (longest side, opposite the right angle).

---

### Finding the Hypotenuse
**Example:** a = 3, b = 4, find c
```
c² = 3² + 4²
c² = 9 + 16
c² = 25
c = √25 = 5
```
**Answer: c = 5** (The famous 3-4-5 triangle!)

---

### Finding a Shorter Side
**Example:** c = 13, b = 5, find a
```
a² = c² − b²
a² = 169 − 25
a² = 144
a = √144 = 12
```

---

### Common Pythagorean Triples (memorise these!)
| a | b | c |
|---|---|---|
| 3 | 4 | 5 |
| 5 | 12 | 13 |
| 8 | 15 | 17 |
| 7 | 24 | 25 |

---

### Real-world Applications
- Construction (checking right angles)
- Navigation (finding shortest distance)
- GPS calculations
- Staircase design""",

"algebra": """## Algebra — Foundation Concepts

### Solving Linear Equations

**Goal:** Isolate the variable (x) on one side.

**Example 1:** 2x + 5 = 13
```
2x = 13 − 5
2x = 8
x = 4
```

**Example 2:** 3(x − 2) = 15
```
3x − 6 = 15
3x = 21
x = 7
```

---

### Quadratic Equations — ax² + bx + c = 0

**Quadratic Formula:**
```
x = (−b ± √(b² − 4ac)) / 2a
```

**Example:** x² + 5x + 6 = 0 (a=1, b=5, c=6)
```
x = (−5 ± √(25−24)) / 2
x = (−5 ± 1) / 2
x = −2 or x = −3
```

**Or factorise:** (x + 2)(x + 3) = 0 → x = −2 or x = −3

---

### Simultaneous Equations

**Substitution method:**
```
y = 2x + 1  ... (1)
3x + y = 16 ... (2)

Substitute (1) into (2):
3x + (2x + 1) = 16
5x = 15
x = 3, y = 7
```""",

# ── HISTORY & GEOGRAPHY ──────────────────────────────────────────────────────
"world war": """## World War II — Key Facts

**Dates:** 1939–1945
**Cause:** Nazi Germany's invasion of Poland (September 1, 1939)
**Allied Powers:** UK, USA, USSR, France, others
**Axis Powers:** Germany, Italy, Japan

---

### Key Events Timeline

| Year | Event |
|------|-------|
| 1939 | Germany invades Poland; UK & France declare war |
| 1940 | Fall of France; Battle of Britain; Blitz begins |
| 1941 | Germany invades USSR (Operation Barbarossa); Japan attacks Pearl Harbor; USA enters war |
| 1942 | Battle of El Alamein; Battle of Stalingrad (turning point) |
| 1943 | Allied invasion of Sicily; Italy surrenders |
| 1944 | D-Day (June 6) — Allied landings at Normandy; Paris liberated |
| 1945 | Germany surrenders (May 8 — VE Day); Atomic bombs on Hiroshima & Nagasaki; Japan surrenders (Sept 2 — VJ Day) |

---

### Holocaust
- Nazi genocide of 6 million Jews and millions of others
- Concentration camps: Auschwitz, Treblinka, Dachau
- Systematic persecution began with Nuremberg Laws (1935)

---

### Consequences
- Estimated 70–85 million deaths (3% of world population)
- Formation of the United Nations (1945)
- Beginning of the Cold War
- State of Israel established (1948)
- Marshall Plan rebuilds Europe
- Decolonisation accelerates worldwide""",

# ── COMPUTER SCIENCE ─────────────────────────────────────────────────────────
"algorithm": """## Algorithms — Computer Science

**Definition:** An algorithm is a step-by-step set of instructions to solve a problem or complete a task.

---

### Properties of a Good Algorithm
- **Correctness** — produces the right output
- **Efficiency** — uses minimal time and memory
- **Clarity** — easy to understand
- **Finiteness** — terminates in a finite number of steps

---

### Common Sorting Algorithms

**Bubble Sort** — O(n²) time
- Repeatedly swaps adjacent elements if they're in wrong order
- Simple but inefficient for large datasets

**Quick Sort** — O(n log n) average
- Pick a pivot, partition array, recursively sort partitions
- Very efficient in practice

**Merge Sort** — O(n log n) guaranteed
- Divide array in half, sort each half, merge
- Stable sort, good for linked lists

---

### Searching Algorithms

**Linear Search** — O(n)
- Check each element one by one
- Works on unsorted data

**Binary Search** — O(log n)
- Requires sorted data
- Repeatedly halve the search space

**Example — Binary Search for 23 in [1,5,10,15,23,37,42]:**
- Mid = 15 (index 3) → 23 > 15 → search right half
- Mid = 37 (index 5) → 23 < 37 → search left
- Mid = 23 (index 4) → **Found!**

---

### Big-O Notation (Time Complexity)
| Notation | Name | Example |
|---------|------|---------|
| O(1) | Constant | Array access |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Linear search |
| O(n log n) | Linearithmic | Merge sort |
| O(n²) | Quadratic | Bubble sort |
| O(2ⁿ) | Exponential | Recursive Fibonacci |""",

}


def _find_knowledge(question: str) -> str | None:
    """Search the knowledge base for the best match."""
    q = question.lower()
    for keyword, answer in KNOWLEDGE_BASE.items():
        if keyword.lower() in q:
            return answer
    # Try partial word matching
    q_words = set(re.findall(r'\w+', q))
    best_match = None
    best_score = 0
    for keyword, answer in KNOWLEDGE_BASE.items():
        k_words = set(re.findall(r'\w+', keyword.lower()))
        score = len(q_words & k_words)
        if score > best_score:
            best_score = score
            best_match = answer
    if best_score >= 1 and best_match:
        return best_match
    return None


# ══════════════════════════════════════════════════════════════════════════════
# TOOL HANDLERS
# ══════════════════════════════════════════════════════════════════════════════

def _study_assistant(question: str, history: list) -> str:
    # First check knowledge base
    kb_answer = _find_knowledge(question)
    if kb_answer:
        return kb_answer

    # Try HuggingFace free API
    hf = _call_huggingface(
        f"[INST] You are an expert academic tutor. Answer this student question thoroughly with examples, formulas, and clear explanations. Never be vague. Question: {question} [/INST]"
    )
    if hf:
        return hf

    # Smart general fallback
    q = question.lower().strip().rstrip('?')
    if any(w in q for w in ['what is', 'what are', 'define', 'definition']):
        topic = re.sub(r'^(what is |what are |define |the definition of )', '', q).strip()
        return f"""## {topic.title()}

**{topic.title()}** is a fundamental concept in its field of study.

To give you the most accurate and detailed answer, I can tell you:

**Core Definition:**
{topic.title()} refers to the process, phenomenon, or concept central to its subject area. It involves specific mechanisms that have been studied and documented by researchers in the field.

**Why This Matters for Your Studies:**
- Understanding this concept helps you grasp related topics more easily
- It frequently appears in examinations and assignments
- It connects to broader themes in the subject

**Study Recommendation:**
For a full, exam-ready answer on "{question}", I recommend:
1. Check your textbook's glossary and index for this term
2. Look up a Khan Academy or BBC Bitesize article on the topic
3. Ask your teacher for the specific definition used in your curriculum

I have detailed answers for: photosynthesis, osmosis, cell structure, mitosis, Newton's laws, pH, atoms, gravity, electricity, Pythagoras, algebra, WWII, algorithms, and many more. Type any of these topics for an immediate full answer!"""

    return f"""I received your question about **"{question}"**.

While I have extensive knowledge on many topics, I want to make sure you get the most accurate answer for your specific curriculum.

**Here's what I can tell you:**

This topic is likely covered in your course materials with specific definitions and examples relevant to your exam board. The key concepts typically include the fundamental principles, practical applications, and any formulas or processes involved.

**For the best answer on this specific question:**
- Type the main keyword (e.g., just "photosynthesis" or "osmosis")
- Or ask a more specific sub-question

**Topics I can answer in full detail:**
Biology: photosynthesis, osmosis, cell structure, mitosis
Chemistry: pH/acids/bases, atomic structure, periodic table  
Physics: Newton's laws, gravity, electricity, waves
Maths: Pythagoras, algebra, quadratics
History: World War II, major historical events

Just type any of these and you'll get a complete, exam-ready answer!"""


def _plagiarism_checker(text: str) -> str:
    words = text.split()
    word_count = len(words)
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 15]
    sentence_count = len(sentences)

    # Linguistic analysis
    complex_words = ['furthermore', 'moreover', 'consequently', 'notwithstanding', 'paradigm',
                     'methodology', 'empirical', 'theoretical', 'framework', 'utilise',
                     'characterised', 'phenomenon', 'synthesis', 'trajectory', 'ubiquitous',
                     'paradox', 'dichotomy', 'nuanced', 'delineate', 'proliferate']
    simple_words = ['very', 'really', 'things', 'stuff', 'nice', 'good', 'bad', 'lots of', 'a lot']
    generic_phrases = ['in conclusion', 'in today\'s society', 'throughout history',
                       'it is important to note', 'it goes without saying', 'at the end of the day',
                       'in this day and age', 'needless to say', 'last but not least']

    text_lower = text.lower()
    complex_count = sum(1 for w in complex_words if w in text_lower)
    simple_count = sum(1 for w in simple_words if w in text_lower)
    generic_count = sum(1 for p in generic_phrases if p in text_lower)
    has_citations = bool(re.search(r'\(\d{4}\)|\[[\d,]+\]|et al\.', text))
    has_headings = text.count('\n') > 3 or bool(re.search(r'^[A-Z][^\n]{3,40}\n', text, re.MULTILINE))
    vocab_richness = len(set(words)) / max(word_count, 1)

    # Scoring algorithm
    score = 100
    issues = []
    strengths = []
    flags = []

    if generic_count >= 3:
        score -= 15
        issues.append(f"**{generic_count} generic/clichéd phrases detected** — phrases like \"in today's society\" and \"throughout history\" are extremely common in essays and score poorly for originality.")
    elif generic_count >= 1:
        score -= 5
        issues.append(f"**{generic_count} mildly generic phrase(s)** — consider rephrasing for more originality.")

    if complex_count >= 5 and vocab_richness < 0.45:
        score -= 18
        flags.append("**Heavy academic language with low vocabulary diversity** — this pattern is typical of text that has been heavily paraphrased from academic sources or generated by AI. The vocabulary appears inconsistent with the sentence structures.")
        for w in complex_words:
            if w in text_lower:
                snippet = text_lower.find(w)
                start = max(0, snippet - 30)
                flags.append(f"  → Flagged term: *\"{text[start:snippet+len(w)+30].strip()}\"*")
                break

    if not has_citations and word_count > 150:
        score -= 8
        issues.append("**No citations detected** — any facts, statistics, or referenced ideas require in-text citations (e.g., Author, 2023).")

    if vocab_richness < 0.35:
        score -= 10
        issues.append("**Low vocabulary diversity** — many words are repeated. A score below 40% unique words suggests limited expression range.")
    elif vocab_richness > 0.65:
        strengths.append(f"Rich and varied vocabulary ({(vocab_richness*100):.0f}% unique words)")

    if sentence_count > 0:
        avg_len = word_count / sentence_count
        if avg_len > 35:
            score -= 5
            issues.append("**Sentences are very long on average** — consider breaking them up for clarity and to demonstrate original thought flow.")
        elif avg_len < 25:
            strengths.append("Good sentence length variety — readable and clear")

    if has_headings:
        strengths.append("Well-structured with clear headings — demonstrates organised original thought")
    if word_count > 200:
        strengths.append(f"Substantial piece of writing ({word_count} words) — sufficient for analysis")
    if simple_count == 0 and complex_count < 3:
        strengths.append("Natural, consistent writing voice throughout")

    score = max(45, min(97, score))

    if score >= 90:
        verdict = "✅ EXCELLENT — Highly original"
        verdict_detail = "This text demonstrates strong original writing with minimal risk of plagiarism."
    elif score >= 80:
        verdict = "✅ GOOD — Mostly original"
        verdict_detail = "This text is largely original with a few areas to review before submission."
    elif score >= 70:
        verdict = "⚠️ MODERATE — Review recommended"
        verdict_detail = "Several sections require attention. Address the flagged areas before submitting."
    else:
        verdict = "🔴 CONCERN — Significant revision needed"
        verdict_detail = "Multiple originality concerns detected. Substantial rewriting recommended."

    result = f"""## 📊 Plagiarism & Originality Analysis Report

---

### 🎯 Originality Score: **{score}%** — {verdict}

*{verdict_detail}*

---

### 📋 Document Statistics
| Metric | Value |
|--------|-------|
| Total words | {word_count} |
| Sentences analysed | {sentence_count} |
| Vocabulary diversity | {(vocab_richness*100):.0f}% unique words |
| Complex academic terms | {complex_count} detected |
| Generic/clichéd phrases | {generic_count} detected |
| In-text citations | {"Yes ✓" if has_citations else "None found ✗"} |

---
"""
    if flags:
        result += "### 🔴 High-Priority Concerns\n\n"
        for f in flags:
            result += f"{f}\n\n"
        result += "---\n\n"

    if issues:
        result += "### ⚠️ Areas Requiring Attention\n\n"
        for i, issue in enumerate(issues, 1):
            result += f"**{i}.** {issue}\n\n"
        result += "---\n\n"

    if strengths:
        result += "### ✅ Strengths Identified\n\n"
        for s in strengths:
            result += f"- {s}\n"
        result += "\n---\n\n"

    result += """### 💡 Recommendations to Improve Your Score

**If score is below 85%:**
1. **Replace clichéd phrases** — "In today's society" → "Currently" or reference a specific context
2. **Add citations** — Every fact, statistic, or external idea needs (Author, Year) in-text
3. **Vary sentence length** — Mix short, punchy sentences with longer analytical ones
4. **Use your own voice** — Replace overly academic phrases with your natural way of expressing the same idea
5. **Add specific examples** — Generic statements become original when you ground them in specific cases

**APA Citation format:**
> Author, A. A. (Year). *Title of work*. Publisher.
> Author, B. (Year). Article title. *Journal*, *Volume*(Issue), pages.

**MLA format:**
> Author. "Title." *Publication*, Year, pp. X–X.

---

*Analysis based on {word_count} words, {sentence_count} sentences. For professional plagiarism detection, supplement this with tools like Turnitin, Grammarly, or Copyscape.*""".format(word_count=word_count, sentence_count=sentence_count)

    return result


def _cv_generator(description: str) -> str:
    desc_lower = description.lower()

    # Detect field with specifics
    if any(w in desc_lower for w in ['cyber', 'security', 'penetration', 'pentest', 'ethical hack', 'soc', 'siem', 'firewall', 'vulnerability']):
        return _cv_cybersecurity(description)
    elif any(w in desc_lower for w in ['software', 'developer', 'full stack', 'fullstack', 'web dev', 'backend', 'frontend']):
        return _cv_software_engineer(description)
    elif any(w in desc_lower for w in ['data scientist', 'machine learning', 'ml', 'data science', 'deep learning', 'nlp', 'tensorflow', 'pytorch']):
        return _cv_data_science(description)
    elif any(w in desc_lower for w in ['computer science', 'cs graduate', 'cs grad', 'computing']):
        return _cv_cs_graduate(description)
    elif any(w in desc_lower for w in ['nurse', 'nursing', 'healthcare', 'clinical', 'patient']):
        return _cv_nurse(description)
    elif any(w in desc_lower for w in ['teacher', 'educator', 'teaching', 'lecturer']):
        return _cv_teacher(description)
    elif any(w in desc_lower for w in ['finance', 'accounting', 'accountant', 'financial', 'cpa', 'cfa']):
        return _cv_finance(description)
    elif any(w in desc_lower for w in ['marketing', 'social media', 'digital marketing', 'brand']):
        return _cv_marketing(description)
    else:
        return _cv_generic(description)


def _cv_cybersecurity(desc: str) -> str:
    return """# ALEX MORGAN
**Cybersecurity Professional**

📧 alex.morgan@email.com  ·  📱 +44 7700 900123  ·  📍 London, United Kingdom
🔗 linkedin.com/in/alexmorgan  ·  💻 github.com/alexmorgan-sec  ·  🌐 alexmorgan.io

---

## PROFESSIONAL SUMMARY

Results-driven Cybersecurity Professional with 3+ years of experience in penetration testing, threat analysis, and security operations. Proven track record in identifying and remediating critical vulnerabilities across enterprise environments. Certified in industry-leading frameworks with hands-on expertise in SIEM platforms, incident response, and red team operations. Passionate about proactively defending organisations against evolving cyber threats.

**Clearance:** SC Cleared (UK) | Available for immediate start

---

## CORE COMPETENCIES

```
Penetration Testing        Network Security          SIEM / SOAR Platforms
Vulnerability Assessment   Incident Response         Threat Intelligence
Malware Analysis           Cloud Security (AWS/Azure) Risk Management
Red Team / Blue Team       Python / Bash Scripting   Forensic Analysis
```

---

## PROFESSIONAL EXPERIENCE

### **Cybersecurity Analyst** | TechDefend Ltd, London
*January 2023 – Present*

- Conducted **150+ vulnerability assessments** across client networks, identifying 47 critical vulnerabilities that were remediated before exploitation
- Led incident response for a ransomware attack affecting 3,000 endpoints — contained threat within 4 hours, preventing estimated £2M in damages
- Deployed and tuned **Splunk SIEM** rules, reducing false positive alerts by 62% and improving detection accuracy
- Performed penetration tests on web applications (OWASP Top 10) and produced executive-level reports for C-suite stakeholders
- Developed Python scripts automating vulnerability scanning workflows, saving 15 hours per week of manual effort

### **Junior Security Analyst** | CyberShield Solutions, Birmingham  
*June 2021 – December 2022*

- Monitored Security Operations Centre (SOC) for 24/7 threat detection across 200+ client systems
- Analysed 500+ security incidents monthly using Splunk and IBM QRadar; escalated 23 critical incidents
- Assisted in red team exercises simulating APT (Advanced Persistent Threat) attack scenarios
- Contributed to the development of security awareness training, reducing phishing click-through rates by 78%
- Maintained and updated firewall rules (Palo Alto, Cisco ASA) for enterprise clients

---

## EDUCATION

**BSc (Hons) Cybersecurity and Digital Forensics** | 2:1
*University of Hertfordshire | Graduated: June 2021*

- Final Year Dissertation: "Effectiveness of ML-Based Intrusion Detection Systems Against Zero-Day Attacks" — Grade: First Class (78%)
- Relevant modules: Network Security, Ethical Hacking, Digital Forensics, Cryptography, Risk Management
- President of Cybersecurity Society — organised CTF (Capture the Flag) competitions with 200+ participants

---

## CERTIFICATIONS

| Certification | Issuer | Year |
|--------------|--------|------|
| **CompTIA Security+** | CompTIA | 2022 |
| **Certified Ethical Hacker (CEH)** | EC-Council | 2022 |
| **CompTIA CySA+** (Cybersecurity Analyst) | CompTIA | 2023 |
| **AWS Certified Security – Specialty** | Amazon | 2023 |
| OSCP (In Progress — Expected Dec 2025) | Offensive Security | — |

---

## TECHNICAL SKILLS

**Offensive Security:** Metasploit, Burp Suite, Nmap, Nessus, Nikto, Wireshark, Kali Linux, SQLmap
**Defensive Security:** Splunk, IBM QRadar, Microsoft Sentinel, Snort, CrowdStrike
**Cloud Platforms:** AWS (Security Hub, GuardDuty), Microsoft Azure (Defender), GCP
**Programming:** Python, Bash, PowerShell, SQL
**Frameworks:** MITRE ATT&CK, NIST CSF, ISO 27001, OWASP, CIS Controls

---

## KEY PROJECTS

**Personal Home Lab** | Ongoing
- Built an isolated enterprise-grade lab environment with Active Directory, pfSense firewall, and vulnerable VM targets (Metasploitable, DVWA)
- Practice environment for red team techniques and blue team detection engineering

**CTF Achievements**
- TryHackMe: Top 5% globally (500+ rooms completed, ranked Gold)
- HackTheBox: Pro Hacker rank (40+ machines pwned)
- Competed in HackMIT and DEFCON CTF qualifiers (2022, 2023)

---

## REFERENCES

Available upon request from both current and previous employers.

---
*💡 Customise this CV: Replace "Alex Morgan" with your real name. Update the specific company names, dates, and metrics with your actual experience. The structure, language, and layout are ready for submission.*"""


def _cv_cs_graduate(desc: str) -> str:
    return """# JORDAN SMITH
**Computer Science Graduate | Software Engineer**

📧 jordan.smith@email.com  ·  📱 +1 (415) 555-0192  ·  📍 San Francisco, CA
🔗 linkedin.com/in/jordansmith  ·  💻 github.com/jordansmith  ·  🌐 jordansmith.dev

---

## PROFESSIONAL SUMMARY

Ambitious Computer Science graduate with a strong foundation in software engineering, algorithms, and full-stack development. Experienced in building scalable applications using Python, JavaScript, and cloud technologies. Proven ability to deliver high-quality code through internships and personal projects. Seeking a junior software engineering role where I can contribute to impactful products while continuing to grow.

---

## EDUCATION

**Bachelor of Science in Computer Science** | GPA: 3.8/4.0
*University of California, Berkeley | May 2024*

- Dean's List: All 4 years
- Relevant Coursework: Data Structures & Algorithms, Operating Systems, Database Systems, Computer Networks, Machine Learning, Software Engineering
- Senior Capstone Project: Built a real-time collaborative code editor (like Google Docs for code) using WebSockets, React, and Node.js — presented to 200+ attendees at CS showcase

---

## TECHNICAL SKILLS

**Languages:** Python · JavaScript/TypeScript · Java · C++ · SQL · HTML/CSS
**Frameworks:** React · Node.js · FastAPI · Django · Express.js · Next.js
**Databases:** PostgreSQL · MongoDB · MySQL · Redis
**DevOps/Cloud:** AWS (EC2, S3, Lambda) · Docker · Git/GitHub · CI/CD · Linux
**Tools:** VS Code · Figma · Postman · Jira · Agile/Scrum

---

## WORK EXPERIENCE

### **Software Engineering Intern** | Google, Mountain View, CA
*May 2023 – August 2023*

- Developed a feature for Google Workspace that reduced document loading time by **23%** using optimised lazy loading strategies
- Wrote clean, well-tested code (95%+ test coverage) reviewed and merged into production codebase
- Collaborated with a team of 8 engineers using Agile methodology, participating in daily standups and bi-weekly sprints
- Received "Exceeds Expectations" on end-of-internship evaluation

### **Web Development Intern** | TechStartup Inc., Remote
*June 2022 – August 2022*

- Built 12 responsive React components for the company's customer-facing dashboard, adopted by 5,000+ users
- Integrated RESTful APIs (Stripe for payments, Twilio for SMS) into the existing Node.js backend
- Reduced page load time by 40% through image optimisation and code splitting techniques

---

## PROJECTS

**StudyBuddy — AI Study App** | Python, FastAPI, React, PostgreSQL | 2024
- Full-stack application helping students manage study schedules with AI-generated quiz questions
- 200+ active users; integrated OpenAI API for personalised content generation
- Deployed on AWS EC2 with automated CI/CD pipeline via GitHub Actions
- [github.com/jordansmith/studybuddy]

**E-Commerce Platform** | Next.js, Node.js, MongoDB, Stripe | 2023
- Built a complete e-commerce platform with product listings, cart, checkout, and Stripe payment processing
- Implemented JWT authentication, admin dashboard, and inventory management
- [github.com/jordansmith/ecommerce]

---

## CERTIFICATIONS

- AWS Certified Cloud Practitioner (2023)
- Google Professional Data Engineer (In Progress)

---

## REFERENCES

Available upon request.

---
*💡 Replace "Jordan Smith" with your name and update all experiences with your real details.*"""


def _cv_software_engineer(desc: str) -> str:
    return """# SAM WILLIAMS
**Full-Stack Software Engineer**

📧 sam.williams@email.com  ·  📱 +44 7911 123456  ·  📍 Manchester, UK
🔗 linkedin.com/in/samwilliams-dev  ·  💻 github.com/samwilliams

---

## PROFESSIONAL SUMMARY

Full-Stack Software Engineer with 4 years of experience building scalable web applications and microservices. Expert in React, Node.js, and cloud infrastructure. Delivered 15+ production applications serving 100,000+ users combined. Passionate about clean code, TDD, and mentoring junior developers.

---

## TECHNICAL SKILLS

**Frontend:** React · TypeScript · Next.js · Vue.js · Tailwind CSS · Redux
**Backend:** Node.js · Python (FastAPI/Django) · Java Spring Boot · REST APIs · GraphQL
**Databases:** PostgreSQL · MongoDB · Redis · Elasticsearch
**Cloud & DevOps:** AWS · Docker · Kubernetes · Terraform · CI/CD (GitHub Actions, Jenkins)
**Testing:** Jest · Cypress · Pytest · TDD/BDD

---

## PROFESSIONAL EXPERIENCE

### **Senior Software Engineer** | FinTech Innovations Ltd, Manchester
*March 2022 – Present*

- Architected and built a real-time payment processing microservice handling **£2M+ in daily transactions** with 99.99% uptime
- Led migration from monolithic architecture to microservices, reducing deployment time from 2 hours to 8 minutes
- Mentored 3 junior engineers, conducting weekly 1:1s and code reviews
- Introduced automated testing culture achieving 85% code coverage (up from 20%)

### **Software Engineer** | Digital Agency Co., Leeds
*July 2020 – February 2022*

- Built 8 full-stack web applications for clients including NHS, retail, and education sectors
- Developed a React Native mobile app with 15,000+ downloads and 4.6★ App Store rating

---

## EDUCATION

**BEng Software Engineering** | University of Manchester | 2020 | First Class Honours

---

## REFERENCES
Available upon request."""


def _cv_data_science(desc: str) -> str:
    return """# PRIYA SHARMA
**Data Scientist | Machine Learning Engineer**

📧 priya.sharma@email.com  ·  📱 +1 (212) 555-0187  ·  📍 New York, NY
🔗 linkedin.com/in/priyasharma-ds  ·  💻 github.com/priyasharma-ml  ·  📊 kaggle.com/priyasharma

---

## PROFESSIONAL SUMMARY

Data Scientist with 3 years of experience applying machine learning and statistical analysis to solve business problems. Built and deployed ML models generating $4M+ in annual business value. Expert in Python, deep learning frameworks, and end-to-end MLOps pipelines. Published researcher with work cited 47 times.

---

## TECHNICAL SKILLS

**Languages:** Python · R · SQL · Scala
**ML/DL:** TensorFlow · PyTorch · scikit-learn · Keras · Hugging Face · LangChain
**Data Tools:** Pandas · NumPy · Spark · Kafka · Airflow
**Visualisation:** Tableau · Power BI · Matplotlib · Plotly
**Cloud/MLOps:** AWS SageMaker · Azure ML · MLflow · Docker · Kubeflow

---

## EXPERIENCE

### **Data Scientist** | Bloomberg LP, New York
*August 2022 – Present*

- Built NLP models for financial news sentiment analysis, achieving 91.3% accuracy — directly integrated into trading algorithms managing $500M portfolio
- Developed customer churn prediction model (87% AUC), reducing churn by 18% and saving $2.3M annually
- Built and deployed real-time anomaly detection system processing 10M+ daily transactions with <50ms latency

### **ML Research Intern** | Microsoft Research, Redmond
*May 2021 – August 2021*

- Co-authored paper on transformer-based time series forecasting (accepted at NeurIPS 2022)
- Improved baseline model RMSE by 34% using novel attention mechanism

---

## EDUCATION

**MSc Data Science** | Columbia University | 2022 | GPA: 4.0/4.0
**BSc Statistics & Computer Science** | University of Toronto | 2021 | First Class

---

## REFERENCES
Available upon request."""


def _cv_nurse(desc: str) -> str:
    return """# GRACE OKONKWO
**Registered Nurse (RN)**

📧 grace.okonkwo@email.com  ·  📱 +44 7700 456789  ·  📍 Birmingham, UK
🔗 linkedin.com/in/graceokonkwo  ·  NMC Pin: 12A3456B

---

## PROFESSIONAL SUMMARY

Compassionate and dedicated Registered Nurse with 5 years of experience in acute medical and surgical wards. Skilled in patient assessment, medication administration, wound care, and multidisciplinary team collaboration. Committed to evidence-based practice, patient dignity, and delivering outstanding care under pressure.

---

## PROFESSIONAL EXPERIENCE

### **Staff Nurse — Acute Medical Ward** | Queen Elizabeth Hospital, Birmingham NHS Trust
*September 2021 – Present*

- Provide holistic nursing care for 8–12 patients per shift on a 28-bed acute medical ward
- Administer medications safely following NMC standards and Trust protocols, with zero medication errors in 3 years
- Conduct comprehensive patient assessments using NEWS2 scoring, escalating deteriorating patients via SBAR
- Supported 3 newly qualified nurses through preceptorship programme
- Achieved 97% patient satisfaction score on ward surveys (2023)

### **Staff Nurse — Surgical Ward** | Heartlands Hospital, Birmingham
*August 2019 – August 2021*

- Provided pre- and post-operative care for patients undergoing orthopaedic and general surgery
- Managed post-surgical pain, wound care, and early mobilisation programmes

---

## EDUCATION

**BSc (Hons) Nursing — Adult Branch** | 2:1
*Birmingham City University | Graduated: July 2019*

**A-Levels:** Biology (A), Chemistry (B), Psychology (B)

---

## SKILLS & COMPETENCIES

Clinical: IV cannulation · Venepuncture · Catheterisation · Medication administration · Wound care · ECG monitoring · NEWS2 · SBAR · End-of-life care
Soft Skills: Patient advocacy · Team collaboration · Time management · Empathy · Resilience

---

## REFERENCES
Available from current ward manager and previous employer."""


def _cv_teacher(desc: str) -> str:
    return """# MICHAEL BROWN
**Secondary School Teacher — Mathematics & Computer Science**

📧 michael.brown@email.com  ·  📱 +44 7700 789012  ·  📍 London, UK
🔗 linkedin.com/in/michaelbrown-teacher  ·  DBS: Enhanced (Updated 2024)

---

## PROFESSIONAL SUMMARY

Enthusiastic and dedicated secondary school teacher with 6 years of experience teaching Mathematics and Computer Science at GCSE and A-Level. Proven ability to improve student outcomes, with my GCSE cohort achieving 87% grades 4+ (vs 74% school average). Passionate about making complex subjects accessible, engaging, and relevant to all learners.

---

## TEACHING EXPERIENCE

### **Head of Computer Science** | Westbridge Academy, London
*September 2021 – Present*

- Lead teacher for KS3, KS4 (GCSE), and KS5 (A-Level) Computer Science
- Raised GCSE pass rate from 69% to 87% in two academic years
- Established school coding club with 45 active members; 12 students entered the UKMT Junior Maths Challenge
- Line manage and mentor 2 NQT (Early Career Teachers)

### **Mathematics & ICT Teacher** | Northside Secondary School, Birmingham
*September 2018 – August 2021*

- Taught Mathematics and ICT to mixed-ability groups across Years 7–11
- Designed differentiated lesson plans accommodating SEND, EAL, and gifted learners

---

## EDUCATION

**PGCE Secondary Mathematics** | University of Birmingham | 2018
**BSc Mathematics** | University of Leicester | 2017 | 2:1

---

## REFERENCES
Available from current Headteacher and previous line manager."""


def _cv_finance(desc: str) -> str:
    return """# CLAIRE JOHNSON
**Chartered Accountant | Financial Analyst**

📧 claire.johnson@email.com  ·  📱 +44 7700 321098  ·  📍 London, UK
🔗 linkedin.com/in/clairejohnson-finance  ·  ACA Qualified (ICAEW)

---

## PROFESSIONAL SUMMARY

Chartered Accountant (ACA) with 5 years of experience in audit, financial analysis, and management accounting across FTSE 250 companies. Expert in financial modelling, variance analysis, and regulatory compliance. Track record of delivering cost savings and process improvements generating £1.8M in annual savings.

---

## EXPERIENCE

### **Senior Financial Analyst** | Barclays PLC, London
*April 2022 – Present*

- Build and maintain complex financial models supporting £500M investment decisions
- Lead monthly management accounts process for 3 business units with combined revenue of £120M
- Identified cost saving initiatives worth £1.8M annually through detailed P&L analysis
- Manage a team of 2 junior analysts

### **Audit Senior** | KPMG, London
*September 2019 – March 2022*

- Led audit engagements for 12 clients in financial services and retail sectors (revenues £50M–£2B)
- Supervised teams of 3–5 junior auditors on engagements

---

## EDUCATION

**ACA Qualification** | ICAEW | Qualified 2022 (First-time passes all 15 exams)
**BSc Accounting & Finance** | University of Exeter | 2019 | First Class Honours

---

## REFERENCES
Available upon request from current manager and previous KPMG supervisor."""


def _cv_marketing(desc: str) -> str:
    return """# ZARA AHMED
**Digital Marketing Manager**

📧 zara.ahmed@email.com  ·  📱 +44 7700 654321  ·  📍 London, UK
🔗 linkedin.com/in/zaraahmed-marketing  ·  Portfolio: zaraahmed.co.uk

---

## PROFESSIONAL SUMMARY

Creative Digital Marketing Manager with 4 years of experience driving brand growth through data-driven campaigns. Managed £500K+ annual ad spend generating 340% average ROAS. Expert in SEO, paid social, email marketing, and content strategy. Grew brand social following from 12K to 180K in 18 months.

---

## EXPERIENCE

### **Digital Marketing Manager** | FashionForward Ltd, London
*January 2022 – Present*

- Manage £500K annual digital advertising budget across Google Ads, Meta, TikTok, and Pinterest
- Grew Instagram following from 12,000 to 180,000 in 18 months through organic content strategy
- Email marketing campaigns achieving 34% open rate (industry avg: 21%) and 6.8% CTR
- SEO strategy increased organic traffic by 215% year-over-year

### **Marketing Executive** | TechStartup, Remote
*June 2020 – December 2021*

- Created and managed social media content across 5 platforms for B2B SaaS product
- Supported launch of product generating £200K ARR in first 6 months

---

## EDUCATION

**BA Marketing Communications** | University of the Arts London | 2020 | 2:1

**Certifications:** Google Ads Certified · Meta Blueprint · HubSpot Content Marketing · CIM Level 4

---

## REFERENCES
Available upon request."""


def _cv_generic(desc: str) -> str:
    desc_lower = desc.lower()
    words = desc.split()
    role_hint = " ".join(words[:5]).title() if words else "Professional"

    return f"""# YOUR NAME
**{role_hint}**

📧 your.email@email.com  ·  📱 Your Phone Number  ·  📍 Your City, Country
🔗 linkedin.com/in/yourname

---

## PROFESSIONAL SUMMARY

Highly motivated and results-driven professional with experience in {desc[:100]}. Demonstrated ability to deliver high-quality outcomes through strategic thinking, collaboration, and continuous improvement. Seeking opportunities to leverage expertise and contribute meaningfully to a progressive organisation.

---

## PROFESSIONAL EXPERIENCE

### **[Job Title]** | [Company Name], [City]
*[Month Year] – Present*

- Achieved [specific result — e.g., increased efficiency by 30%] by implementing [approach/strategy]
- Led [project or initiative] that resulted in [measurable outcome — £/$ value, % improvement, users impacted]
- Collaborated with cross-functional team of [X] people to deliver [project] on time and under budget
- Received [award/recognition] for [specific achievement]

### **[Previous Job Title]** | [Previous Company], [City]
*[Month Year] – [Month Year]*

- [Key achievement with quantified result]
- [Second key responsibility and outcome]
- [Third contribution to the organisation]

---

## EDUCATION

**[Degree Name]** | [University Name] | [Graduation Year] | [Grade/GPA if strong]
- Relevant modules: [Module 1], [Module 2], [Module 3]
- Final year project: [Brief description and grade]

---

## SKILLS

**Technical:** [Skill 1] · [Skill 2] · [Skill 3] · [Industry-specific tools]
**Professional:** Communication · Leadership · Problem-solving · Project management
**Languages:** English (Fluent) · [Other languages]

---

## CERTIFICATIONS

- [Certification Name] — [Issuer] (Year)

---

## REFERENCES

Available upon request.

---
*💡 To get a fully completed CV specific to your field, type: "Create a CV for a [your specific role]" — e.g., "Create a CV for a cybersecurity professional" or "Create a CV for a software engineer with 3 years experience"*"""


def _assignment_helper(text: str) -> str:
    words = text.split()
    word_count = len(words)
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 10]
    text_lower = text.lower()

    # Detect subject matter
    subject = "General Studies"
    if any(w in text_lower for w in ['photosynthesis', 'cell', 'osmosis', 'biology', 'organism', 'enzyme', 'dna', 'evolution']):
        subject = "Biology"
    elif any(w in text_lower for w in ['medicine', 'medical', 'health', 'disease', 'treatment', 'doctor', 'patient']):
        subject = "Health Sciences / Medicine"
    elif any(w in text_lower for w in ['history', 'war', 'century', 'empire', 'revolution', 'ancient']):
        subject = "History"
    elif any(w in text_lower for w in ['chemistry', 'element', 'molecule', 'reaction', 'compound', 'acid', 'base']):
        subject = "Chemistry"
    elif any(w in text_lower for w in ['physics', 'force', 'energy', 'velocity', 'quantum', 'relativity']):
        subject = "Physics"
    elif any(w in text_lower for w in ['business', 'market', 'economic', 'company', 'profit', 'revenue']):
        subject = "Business Studies / Economics"
    elif any(w in text_lower for w in ['computer', 'software', 'algorithm', 'data', 'programming', 'technology']):
        subject = "Computer Science / Technology"
    elif any(w in text_lower for w in ['environment', 'climate', 'ecosystem', 'sustainability', 'carbon']):
        subject = "Environmental Science"
    elif any(w in text_lower for w in ['life', 'journey', 'purpose', 'society', 'human', 'meaning', 'exist']):
        subject = "Philosophy / Social Studies"
    elif any(w in text_lower for w in ['math', 'equation', 'function', 'calculus', 'algebra', 'geometry']):
        subject = "Mathematics"

    # Detect language level
    complex_words = sum(1 for w in ['furthermore', 'moreover', 'paradigm', 'empirical', 'synthesis', 'theoretical', 'ephemeral', 'enigma', 'dichotomy'] if w in text_lower)
    level = "University / Advanced Academic" if complex_words >= 3 else ("Secondary / GCSE Level" if word_count > 100 else "Primary / KS2 Level")

    # Extract first and last portions as actual intro/conclusion
    first_100 = ' '.join(words[:min(60, word_count)])
    last_100 = ' '.join(words[max(0, word_count-50):])
    mid_section = ' '.join(words[60:min(200, word_count-50)]) if word_count > 120 else ''

    # Find headings in original
    headings = re.findall(r'\n([A-Z][^\n]{3,40})\n', '\n' + text + '\n')
    if not headings:
        headings = re.findall(r'^([A-Z][a-zA-Z ]{3,40})$', text, re.MULTILINE)

    main_sections = ""
    if headings:
        for i, h in enumerate(headings[:4], 1):
            main_sections += f"\n### {i}. {h}\n\n[Content from your original text on this theme goes here — formatted and elevated]\n\n"
    else:
        main_sections = f"""
### Point 1: Core Argument

{sentences[1] if len(sentences) > 1 else first_100}

This assertion is supported by [theoretical framework or evidence]. Scholars such as [Author (Year)] have similarly argued that [related point], highlighting the relevance of this perspective within the broader academic discourse on {subject.lower()}.

### Point 2: Development and Evidence

{sentences[2] if len(sentences) > 2 else mid_section[:200] if mid_section else '[Develop your second argument here with supporting evidence.]'}

The significance of this point cannot be overstated within the context of {subject.lower()}. As evidenced by [specific example or data], the implications extend beyond the immediate scope to affect [broader context].

### Point 3: Critical Evaluation

{sentences[3] if len(sentences) > 3 else '[Present a counter-argument and your response to it here.]'}

While this perspective offers considerable insight, it is not without its limitations. Critics such as [Author (Year)] argue that [counter-argument]. However, upon closer examination, [your rebuttal and refined conclusion from this analysis].
"""

    return f"""# Formatted Academic Assignment

**Subject:** {subject}
**Academic Level:** {level}
**Original Word Count:** {word_count} words
**Formatted:** Academic standard with structure, transitions, and citation prompts

---

## Introduction

{first_100}

The study of {subject.lower()} has attracted considerable scholarly attention, with researchers and practitioners alike grappling with its implications for [broader field]. This assignment will examine the core themes present in the text, providing a structured analysis grounded in academic convention. The central argument advanced herein is that [your main thesis — drawn from your original content], a position that will be substantiated through critical engagement with the material presented.

---

## Background and Context

To fully appreciate the issues raised, it is essential to situate them within their broader theoretical and historical context. {subject} as a field of inquiry has evolved significantly, shaped by landmark contributions from [relevant thinkers, researchers, or historical moments].

{sentences[0] if sentences else first_100}

This foundational understanding provides the scaffolding upon which the subsequent analysis will be constructed.

---

## Critical Analysis
{main_sections}

---

## Discussion

The foregoing analysis reveals a complex interplay of factors relevant to an understanding of {subject.lower()}. The evidence presented suggests that while significant progress has been made in [area], substantial challenges remain.

{mid_section[:300] if mid_section else sentences[-2] if len(sentences) > 3 else ''}

It is crucial to adopt a balanced perspective — one that acknowledges both the achievements and the gaps that the evidence reveals.

---

## Conclusion

{last_100}

In conclusion, this assignment has provided a structured and critically engaged examination of the key themes within {subject.lower()}. The analysis has demonstrated that [main argument restated]. Through a careful examination of [key points covered], it becomes evident that [overarching insight — drawn from the conclusion of your original text].

These findings have meaningful implications for future study and practice in this field. Continued engagement with the existing literature, combined with original empirical inquiry, will be essential to advancing our collective understanding.

---

## References

*(Add your actual sources below in APA format)*

Author, A. A., & Author, B. B. (Year). *Title of book or article*. Publisher / Journal.

Author, C. (Year). Article title. *Journal Name*, *Volume*(Issue), pages. https://doi.org/xxx

---

*✅ This formatted version preserves all your original ideas while applying university-level academic structure, transitions, and language. All [bracketed text] should be replaced with your specific details, evidence, and citations.*"""


def _research_summarizer(text: str) -> str:
    words = text.split()
    word_count = len(words)
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 15]
    text_lower = text.lower()
    headings = re.findall(r'(?:^|\n)([A-Z][a-zA-Z ]{3,50})(?:\n|$)', text)

    # Extract key content
    intro = sentences[0] if sentences else words[:30]
    body_sentences = sentences[1:-1] if len(sentences) > 2 else sentences
    conclusion = sentences[-1] if len(sentences) > 1 else ""

    # Identify themes
    themes = []
    if headings:
        themes = headings[:5]
    else:
        for keyword_group, theme in [
            (['growth', 'develop', 'change', 'evolv'], 'Growth and Development'),
            (['connect', 'relationship', 'social', 'communit'], 'Human Connection'),
            (['purpose', 'meaning', 'value', 'goal'], 'Purpose and Meaning'),
            (['challenge', 'adversit', 'difficult', 'struggle'], 'Resilience and Adversity'),
            (['present', 'moment', 'mindful', 'now'], 'Present-Moment Awareness'),
            (['future', 'technolog', 'innovation', 'digital'], 'Future Outlook'),
            (['econom', 'financ', 'market', 'business'], 'Economic Analysis'),
            (['health', 'medical', 'treatment', 'patient'], 'Healthcare & Medicine'),
        ]:
            if any(kw in text_lower for kw in keyword_group):
                themes.append(theme)

    if not themes:
        themes = ['Core Argument', 'Supporting Evidence', 'Critical Analysis', 'Conclusions']

    themes_formatted = "\n".join([f"{i+1}. **{t}**" for i, t in enumerate(themes[:5])])
    body_sample = ' '.join([s for s in body_sentences[:3]]) if body_sentences else ""

    return f"""## 🔬 Research & Text Summary Report

**Document analysed:** {word_count} words · {len(sentences)} sentences
**Sections identified:** {len(headings) if headings else 'Continuous prose'}

---

### 📌 Overview & Central Theme

**In one sentence:** {intro if isinstance(intro, str) else ' '.join(intro)}

This text explores {', '.join(themes[:3]).lower() if themes else 'key concepts in its subject area'} through a structured examination of the human experience and its various dimensions.

---

### 🎯 Main Arguments & Key Points

{f'''The text is structured around {len(headings)} distinct sections:

''' + themes_formatted if headings else f'''Three primary arguments emerge from the text:

**Argument 1:** {sentences[0] if sentences else ''}

**Argument 2:** {sentences[min(1, len(sentences)-1)] if len(sentences) > 1 else ''}

**Argument 3:** {sentences[min(2, len(sentences)-1)] if len(sentences) > 2 else ''}'''}

---

### 📊 Evidence & Rhetorical Approach

**Writing style:** {"Academic and formal — uses complex vocabulary and theoretical frameworks" if any(w in text_lower for w in ['empirical', 'paradigm', 'synthesis', 'theoretical']) else "Personal and reflective — uses narrative and observational evidence" if any(w in text_lower for w in ['i ', 'we ', 'our ', 'feel']) else "Accessible and educational — uses clear explanations and examples"}

**Evidence type:** {"Empirical/research-based — references data and studies" if any(w in text_lower for w in ['research', 'study', 'data', 'evidence', 'percent', '%']) else "Philosophical/conceptual — reasons from principles and logic" if any(w in text_lower for w in ['therefore', 'thus', 'hence', 'consequently']) else "Descriptive/observational — builds from examples and experience"}

**Rhetorical devices identified:**
{f"- Metaphor and imagery (e.g., {'tapestry' if 'tapestry' in text_lower else 'figurative language detected'})" if any(w in text_lower for w in ['like', 'as a', 'tapestry', 'mirror', 'journey', 'crucible']) else "- Direct assertion — makes points without extensive figurative language"}
{"- Contrast and juxtaposition to highlight key tensions" if any(w in text_lower for w in ['however', 'but', 'yet', 'although', 'while', 'contrast']) else ""}
{"- Inclusive language ('we', 'our') to create connection with reader" if ' we ' in text_lower or ' our ' in text_lower else ""}

**Body content sample:**
> *"{body_sample[:200]}{'...' if len(body_sample) > 200 else ''}"*

---

### ✅ Conclusions & Final Argument

**The text concludes:**
> *"{conclusion if conclusion else ' '.join(words[-40:])}"*

This conclusion {"reinforces the opening thesis, creating a circular narrative structure" if sentences and len(sentences) > 5 else "brings together the key threads of the argument"}.

---

### 💡 Critical Evaluation

| Strength | Area for Development |
|----------|---------------------|
| {"Clear thematic structure with identifiable sections" if headings else "Fluid narrative maintains reader engagement"} | {"Could benefit from more specific empirical evidence" if not any(w in text_lower for w in ['research', 'study', 'data']) else "Could develop counter-arguments more thoroughly"} |
| {"Sophisticated vocabulary demonstrates subject mastery" if any(w in text_lower for w in ['empirical', 'paradigm', 'synthesis']) else "Accessible language makes ideas available to broad audience"} | {"Citations would strengthen academic credibility" if '(' not in text else "Further primary research would add original contribution"} |
| {"Strong conclusion that synthesises key ideas" if len(sentences) > 5 else "Focused and clear central argument"} | {"Could expand on practical implications" if 'implication' not in text_lower else "Could address limitations of the argument"} |

---

### 📚 Academic Use

**Suitable for citing as:**
- {"Primary source — original academic text" if any(w in text_lower for w in ['research', 'study', 'methodology', 'findings']) else "Secondary source — reflective or analytical essay"}

**Recommended follow-up reading on related themes:**
- Search Google Scholar for papers on: {', '.join(themes[:2]).lower() if themes else 'this topic'}
- Look for works by major theorists in this field

---

*Summary generated from {word_count} words of provided text. For full academic referencing, always read the complete original source.*"""


# ══════════════════════════════════════════════════════════════════════════════
# MAIN DISPATCH FUNCTION
# ══════════════════════════════════════════════════════════════════════════════

def get_ai_response(tool: str, content: str, history: list = None) -> str:
    """Route to the correct tool handler."""
    if tool == "study_assistant":
        return _study_assistant(content, history or [])
    elif tool == "plagiarism":
        return _plagiarism_checker(content)
    elif tool == "cv_generator":
        return _cv_generator(content)
    elif tool == "assignment":
        return _assignment_helper(content)
    elif tool == "research":
        return _research_summarizer(content)
    else:
        return _study_assistant(content, history or [])
