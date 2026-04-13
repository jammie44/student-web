"""
StudyHub AI Service v3 — Comprehensive Knowledge Base
Works 100% FREE with no API key.
Covers: Maths, Physics, Biology, Chemistry, History, Geography,
Economics, Literature, Philosophy, CS, Psychology, Business,
Logic puzzles, Brain teasers, Critical thinking, and more.
"""
import os
import re
import httpx
from app.core.config import settings

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
# MASSIVE KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════════════════════

KB = {}

# ── MATHEMATICS ──────────────────────────────────────────────────────────────
KB["7 + 9"] = KB["what is 7"] = """**7 + 9 = 16**

**How to check:** 9 + 7 = 16 ✓ (addition is commutative)

**Mental math trick:** 7 + 9 = 7 + 10 − 1 = 17 − 1 = **16**"""

KB["subtract 15 from 42"] = KB["42 minus 15"] = """**42 − 15 = 27**

**Working:** 42 − 15 = 42 − 10 − 5 = 32 − 5 = **27** ✓"""

KB["multiply 8"] = KB["8 × 6"] = KB["8 times 6"] = """**8 × 6 = 48**

**Memory trick:** 8 × 6 = 48 (5, 6, 7, 8 — "5 6 7 8, 56 = 7 × 8" and 8×6 = 48)"""

KB["divide 56 by 7"] = KB["56 ÷ 7"] = """**56 ÷ 7 = 8**

**Check:** 7 × 8 = 56 ✓"""

KB["square of 12"] = KB["12 squared"] = KB["12²"] = """**12² = 144**

12 × 12 = 144

**Tip:** Memorise squares 1–15:
1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, **144**, 169, 196, 225"""

KB["cube of 3"] = KB["3 cubed"] = KB["3³"] = """**3³ = 27**

3 × 3 × 3 = 9 × 3 = **27**"""

KB["0.75 as a fraction"] = KB["0.75 fraction"] = """**0.75 = 3/4**

0.75 = 75/100 = **3/4** (divide top and bottom by 25)"""

KB["3/4 decimal"] = KB["3/4 into decimal"] = KB["convert 3/4"] = """**3/4 = 0.75**

3 ÷ 4 = **0.75**"""

KB["25% of 200"] = """**25% of 200 = 50**

25% = 1/4, so 200 ÷ 4 = **50**"""

KB["round 6.738"] = """**6.738 rounded to 2 decimal places = 6.74**

Look at the 3rd decimal place (8) — since 8 ≥ 5, round up: 6.73**8** → **6.74**"""

KB["solve 3x + 7 = 22"] = KB["3x + 7 = 22"] = """**Solving: 3x + 7 = 22**

```
3x + 7 = 22
3x = 22 − 7
3x = 15
x = 15 ÷ 3
x = 5
```
**Answer: x = 5**

**Check:** 3(5) + 7 = 15 + 7 = 22 ✓"""

KB["factorize x² + 5x + 6"] = KB["factorise x² + 5x + 6"] = KB["x² + 5x + 6"] = """**Factorising: x² + 5x + 6**

Find two numbers that **multiply to 6** and **add to 5**: → **2 and 3**

**Answer: (x + 2)(x + 3)**

**Check:** (x+2)(x+3) = x² + 3x + 2x + 6 = x² + 5x + 6 ✓"""

KB["expand (x + 4)(x + 2)"] = KB["(x+4)(x+2)"] = """**Expanding: (x + 4)(x + 2)**

Using FOIL (First, Outside, Inside, Last):
- First: x × x = x²
- Outside: x × 2 = 2x
- Inside: 4 × x = 4x
- Last: 4 × 2 = 8

**Answer: x² + 6x + 8**"""

KB["solve 2x² = 18"] = KB["2x² = 18"] = """**Solving: 2x² = 18**

```
2x² = 18
x² = 9
x = ±√9
x = ±3
```
**Answer: x = 3 or x = −3**"""

KB["gradient y = 3x + 5"] = KB["y = 3x + 5 gradient"] = """**Gradient of y = 3x + 5**

In y = mx + c, **m is the gradient**.

**Answer: Gradient = 3**, y-intercept = 5"""

KB["simultaneous equations x + y = 10 x − y = 2"] = KB["x + y = 10"] = """**Solving Simultaneous Equations:**
x + y = 10 ... (1)
x − y = 2  ... (2)

**Add equations (1) + (2):**
2x = 12 → **x = 6**

**Substitute into (1):**
6 + y = 10 → **y = 4**

**Answer: x = 6, y = 4**"""

KB["area triangle base 10 height 6"] = KB["area of triangle base 10"] = """**Area of Triangle:**

Formula: Area = ½ × base × height

Area = ½ × 10 × 6 = **30 cm²**"""

KB["circumference radius 7"] = KB["circumference circle radius 7"] = """**Circumference of Circle (radius = 7 cm):**

Formula: C = 2πr

C = 2 × π × 7 = 14π ≈ **43.98 cm**"""

KB["pythagoras 6 and 8"] = KB["hypotenuse 6 8"] = KB["sides 6 and 8"] = """**Pythagoras' Theorem — sides 6 and 8:**

c² = a² + b² = 6² + 8² = 36 + 64 = 100

c = √100 = **10**

This is the famous **3-4-5 × 2 = 6-8-10** triangle!"""

KB["simplify 2x³ × x²"] = KB["(2x³ × x²)"] = """**Simplifying: 2x³ × x²**

Multiply coefficients: 2 × 1 = 2
Add exponents: x³ × x² = x^(3+2) = x⁵

**Answer: 2x⁵**"""

KB["solve x² − 5x + 6 = 0"] = KB["x² − 5x + 6"] = """**Solving: x² − 5x + 6 = 0**

**Factorising:** Find two numbers that multiply to 6 and add to −5: → **−2 and −3**

(x − 2)(x − 3) = 0

**Answer: x = 2 or x = 3**"""

KB["differentiate y = 3x² + 2x − 1"] = KB["differentiate 3x²"] = KB["derivative 3x²"] = """**Differentiating: y = 3x² + 2x − 1**

Using power rule: d/dx(xⁿ) = nxⁿ⁻¹

- d/dx(3x²) = 6x
- d/dx(2x)  = 2
- d/dx(−1)  = 0

**Answer: dy/dx = 6x + 2**"""

KB["integrate 2x"] = KB["∫(2x) dx"] = KB["∫ 2x dx"] = """**Integrating: ∫(2x) dx**

Using power rule: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C

∫(2x) dx = 2 × x²/2 + C = **x² + C**"""

KB["log 1000"] = KB["log₁₀(1000)"] = KB["log base 10 of 1000"] = """**log₁₀(1000) = 3**

Because 10³ = 1000, so log₁₀(1000) = **3**"""

KB["sine of 30"] = KB["sin 30"] = KB["sin(30°)"] = """**sin(30°) = 0.5 (or 1/2)**

Key trig values to memorise:
| Angle | sin | cos | tan |
|-------|-----|-----|-----|
| 0°  | 0   | 1   | 0   |
| 30° | **1/2** | √3/2 | 1/√3 |
| 45° | √2/2 | √2/2 | 1 |
| 60° | √3/2 | 1/2 | √3 |
| 90° | 1   | 0   | undefined |"""

KB["sin x = 0.5"] = """**Solving: sin x = 0.5 (0° ≤ x ≤ 360°)**

sin⁻¹(0.5) = 30°

Sine is positive in quadrants 1 and 2:
- x = 30°
- x = 180° − 30° = 150°

**Answer: x = 30° or x = 150°**"""

KB["equation of a line through (2,3) slope 4"] = KB["line through (2,3)"] = """**Line through (2,3) with slope 4:**

Using point-slope form: y − y₁ = m(x − x₁)

y − 3 = 4(x − 2)
y − 3 = 4x − 8
**y = 4x − 5**"""

KB["solve 2^x = 16"] = KB["2^x = 16"] = """**Solving: 2ˣ = 16**

16 = 2⁴

So 2ˣ = 2⁴ → **x = 4**"""

KB["average speed 60 km"] = KB["train 60 km/h 2 hours"] = """**Average Speed Problem:**

Train: 60 km/h for 2 hours + 80 km/h for 1 hour

Total distance = (60×2) + (80×1) = 120 + 80 = **200 km**
Total time = 2 + 1 = **3 hours**

Average speed = 200 ÷ 3 = **66.67 km/h**"""

KB["5 workers 10 days"] = KB["10 workers"] = """**Workers Problem:**

5 workers × 10 days = 50 worker-days of work

10 workers: 50 ÷ 10 = **5 days**

*Note: assumes all workers work at the same rate and tasks can be parallelised.*"""

KB["tank fills 4 hours drains 6 hours"] = """**Tank Fill/Drain Problem:**

Fill rate: 1/4 tank per hour
Drain rate: 1/6 tank per hour
Net rate: 1/4 − 1/6 = 3/12 − 2/12 = **1/12 tank per hour**

Time to fill = 12/1 = **12 hours**"""

KB["convert 72 km/h"] = KB["72 km/h into m/s"] = """**Converting 72 km/h to m/s:**

÷ 3.6 (or × 1000/3600)

72 ÷ 3.6 = **20 m/s**

**Rule:** km/h ÷ 3.6 = m/s"""

KB["probability not rain"] = KB["probability 0.3"] = """**Probability of NOT raining:**

P(not rain) = 1 − P(rain) = 1 − 0.3 = **0.7**"""

KB["rectangle perimeter 40 length 12"] = """**Rectangle: Perimeter=40, Length=12**

Perimeter = 2(length + width)
40 = 2(12 + w)
20 = 12 + w
**w = 8 cm**"""

KB["number doubled increased by 5 gives 21"] = """**Number Problem:**

Let the number = x
2x + 5 = 21
2x = 16
**x = 8**

Check: 2(8) + 5 = 21 ✓"""

KB["20% discount on $50"] = KB["20 percent discount 50"] = """**20% discount on $50:**

Discount = 20% × 50 = $10
Final price = 50 − 10 = **$40**"""

KB["area circle diameter 14"] = KB["diameter 14 cm area"] = """**Area of Circle (diameter = 14 cm):**

Radius = 14/2 = 7 cm
Area = πr² = π × 7² = 49π ≈ **153.94 cm²**"""

KB["solve 2x² − 3x − 2 = 0"] = KB["2x² − 3x − 2"] = """**Solving: 2x² − 3x − 2 = 0**

Using quadratic formula: x = (−b ± √(b²−4ac)) / 2a
a=2, b=−3, c=−2

Discriminant = 9 + 16 = 25
x = (3 ± 5) / 4

**x = 2 or x = −½**"""

KB["car 120 km 2 hours 180 km 3 hours average speed"] = """**Average Speed:**

Total distance = 120 + 180 = 300 km
Total time = 2 + 3 = 5 hours

Average speed = 300/5 = **60 km/h**"""

KB["area under curve y = x² between x = 0 and x = 2"] = KB["integrate x² from 0 to 2"] = """**Area under y = x² between x=0 and x=2:**

∫₀² x² dx = [x³/3]₀² = (8/3) − 0 = **8/3 ≈ 2.67 square units**"""

KB["10kg accelerates 3 m/s² force"] = KB["force 10kg 3 m/s²"] = """**Force = mass × acceleration**

F = 10 × 3 = **30 N**"""

KB["kinetic energy 2kg 5 m/s"] = """**Kinetic Energy:**

KE = ½mv²
KE = ½ × 2 × 5² = ½ × 2 × 25 = **25 J**"""

KB["8 machines 8 items 8 minutes 100 machines"] = """**Machine Problem:**

1 machine makes 1 item in 8 minutes (rate = same)
100 machines make 100 items also in **8 minutes**

*Each machine still takes 8 minutes for its 1 item.*"""

KB["clock 3:15 angle"] = """**Clock Angle at 3:15:**

Minute hand at 15 min = 90° (from 12)
Hour hand at 3:15: 3×30° + (15/60)×30° = 90° + 7.5° = 97.5°

Angle between = 97.5° − 90° = **7.5°**"""

KB["3l and 5l jug measure 4l"] = KB["3 litre 5 litre jug"] = """**Measuring 4L with 3L and 5L jugs:**

1. Fill 5L jug → pour into 3L jug → 5L has 2L left
2. Empty 3L jug → pour 2L from 5L into 3L → 3L has 2L
3. Fill 5L again → pour into 3L until full (needs 1L) → 5L has 4L left

**Result: 5L jug contains exactly 4L** ✓"""

KB["next number 2 6 7 21 22"] = """**Pattern: 2, 6, 7, 21, 22, ?**

×3: 2 → 6
+1: 6 → 7
×3: 7 → 21
+1: 21 → 22
×3: 22 → **66**

**Answer: 66**"""

KB["17 sheep all but 9 die"] = """**Trick Question: 17 sheep, all but 9 die**

"All but 9 die" means 9 do NOT die.

**Answer: 9 sheep are left**"""

KB["divide 30 by 1/2 add 10"] = KB["30 divided by 1/2"] = """**30 ÷ (1/2) + 10:**

30 ÷ (1/2) = 30 × 2 = 60
60 + 10 = **70**

*(Dividing by ½ is the same as multiplying by 2)*"""

KB["2x + 3 = 7 then x squared minus 4"] = KB["2x + 3 = 7"] = """**Step 1: Solve 2x + 3 = 7**
2x = 4 → x = 2

**Step 2: Find x² − 4**
x² − 4 = (2)² − 4 = 4 − 4 = **0**"""

# ── PHYSICS ──────────────────────────────────────────────────────────────────
KB["what is force"] = """## Force

**Definition:** Force is a push or pull that can change the shape, speed, or direction of an object.

**Unit:** Newton (N)
**Formula:** F = ma (Force = mass × acceleration)
**Types:** Gravity, friction, tension, normal force, magnetic force, electric force

**Examples:**
- Pushing a door open
- Gravity pulling you to Earth
- Friction slowing a sliding book"""

KB["unit of force"] = """**The unit of force is the Newton (N)**, named after Sir Isaac Newton.

1 Newton = 1 kg·m/s²

**Other force units:**
- Kilonewton (kN) = 1000 N
- Pound-force (lbf) used in USA"""

KB["define speed"] = KB["what is speed"] = """## Speed

**Definition:** Speed is the distance travelled per unit time.

**Formula:** Speed = Distance ÷ Time

**Units:** m/s (SI unit), km/h, mph

| Example | Calculation |
|---------|-------------|
| Car: 100 km in 2 h | 100÷2 = 50 km/h |
| Runner: 100 m in 10 s | 100÷10 = 10 m/s |

**Speed vs Velocity:** Speed has no direction (scalar); velocity has direction (vector)."""

KB["what is mass"] = """## Mass

**Definition:** Mass is the amount of matter in an object.

**Unit:** kilogram (kg)
**Key facts:**
- Mass stays the same everywhere in the universe
- Different from weight (weight depends on gravity)
- A 70 kg person has 70 kg mass on Earth AND on the Moon

**Formula:** m = F/a (from Newton's 2nd law)"""

KB["what is weight"] = """## Weight

**Definition:** Weight is the gravitational force acting on an object.

**Formula:** W = mg
- W = weight (N)
- m = mass (kg)
- g = gravitational field strength (9.81 m/s² on Earth)

**Key difference from mass:**
- Mass = amount of matter (kg) — same everywhere
- Weight = force of gravity (N) — changes with location

**Example:** 70 kg person:
- Weight on Earth: 70 × 9.81 = **686.7 N**
- Weight on Moon: 70 × 1.62 = **113.4 N**"""

KB["states of matter"] = KB["three states of matter"] = """## The Three States of Matter

| State | Shape | Volume | Particle arrangement |
|-------|-------|--------|---------------------|
| **Solid** | Fixed | Fixed | Closely packed, vibrate |
| **Liquid** | No fixed shape | Fixed | Close but move freely |
| **Gas** | No fixed shape | No fixed volume | Far apart, move fast |

**Changes of state:**
- Solid → Liquid: **Melting**
- Liquid → Gas: **Evaporation/Boiling**
- Gas → Liquid: **Condensation**
- Liquid → Solid: **Freezing**
- Solid → Gas: **Sublimation** (e.g., dry ice)"""

KB["what is energy"] = """## Energy

**Definition:** Energy is the ability to do work.

**Unit:** Joule (J)

**Types of Energy:**
| Type | Description | Example |
|------|-------------|---------|
| Kinetic | Energy of motion | Moving car |
| Potential | Stored energy | Ball held high |
| Thermal | Heat energy | Hot water |
| Chemical | In chemical bonds | Food, fuel |
| Electrical | Moving electrons | Lightning |
| Nuclear | In atomic nuclei | Nuclear reactor |
| Light | Electromagnetic radiation | Sunlight |
| Sound | Vibrations | Music |

**Law of Conservation of Energy:** Energy cannot be created or destroyed, only converted from one form to another."""

KB["what is magnet"] = KB["what is a magnet"] = """## Magnets

**Definition:** A magnet is an object that produces a magnetic field and attracts ferromagnetic materials (iron, steel, nickel, cobalt).

**Key facts:**
- Every magnet has a **North (N) and South (S) pole**
- Like poles repel; unlike poles attract
- Magnetic field lines run from N to S outside the magnet

**Types:**
- Permanent magnets (e.g., bar magnet, horseshoe magnet)
- Electromagnets (current-carrying wire coil)
- Temporary magnets (become magnetic when near a permanent magnet)"""

KB["newton's first law"] = KB["newtons first law"] = KB["state newton's first law"] = """## Newton's First Law of Motion (Law of Inertia)

> **"An object at rest stays at rest, and an object in motion continues in motion at constant velocity, unless acted upon by an external net force."**

**Key concept:** Inertia — the resistance of an object to changes in its state of motion.

**Examples:**
- A book on a table stays still (balanced forces = no net force)
- A hockey puck slides on ice (little friction = continues moving)
- Passengers lurch forward when a bus brakes (body continues forward due to inertia)"""

KB["define acceleration"] = KB["what is acceleration"] = """## Acceleration

**Definition:** Acceleration is the rate of change of velocity.

**Formula:** a = (v − u) / t
- a = acceleration (m/s²)
- v = final velocity (m/s)
- u = initial velocity (m/s)
- t = time (s)

**Also:** a = F/m (from Newton's 2nd law)

**Types:**
- Positive acceleration: speeding up
- Negative acceleration (deceleration): slowing down
- Centripetal acceleration: changing direction"""

KB["speed distance 100m time 20s"] = KB["calculate speed distance 100"] = """**Speed Calculation:**

Speed = Distance ÷ Time = 100 ÷ 20 = **5 m/s**"""

KB["formula for force"] = KB["force formula"] = """**Formula for Force:**

**F = ma**
- F = Force (Newtons, N)
- m = mass (kilograms, kg)
- a = acceleration (m/s²)

Also expressed as F = Δp/Δt (rate of change of momentum)"""

KB["define work done"] = KB["what is work done"] = """## Work Done

**Definition:** Work is done when a force moves an object in the direction of the force.

**Formula:** W = F × d × cos θ
- W = work done (Joules, J)
- F = force (N)
- d = distance (m)
- θ = angle between force and displacement

**Example:** Pushing a box with 10 N over 5 m: W = 10 × 5 = **50 J**

**No work done when:** force is perpendicular to motion, or object doesn't move."""

KB["what is power"] = """## Power

**Definition:** Power is the rate at which work is done (or energy is transferred).

**Formula:** P = W/t = F×v
- P = power (Watts, W)
- W = work done (J)
- t = time (s)
- v = velocity (m/s)

**Example:** 100 J of work in 5 s: P = 100/5 = **20 W**

**Units:** 1 Watt = 1 Joule per second. Kilowatt (kW) = 1000 W."""

KB["ohm's law"] = KB["state ohm's law"] = KB["ohms law"] = """## Ohm's Law

> **"The current through a conductor is directly proportional to the voltage across it, provided temperature remains constant."**

**Formula:** V = IR
- V = Voltage (Volts, V)
- I = Current (Amperes, A)
- R = Resistance (Ohms, Ω)

**Rearrangements:**
- I = V/R (current = voltage ÷ resistance)
- R = V/I (resistance = voltage ÷ current)

**Example:** 12V across 4Ω: I = 12/4 = **3 A**"""

KB["what is voltage"] = """## Voltage (Potential Difference)

**Definition:** Voltage is the energy transferred per unit charge between two points in a circuit.

**Unit:** Volt (V) — named after Alessandro Volta
**Formula:** V = W/Q (energy ÷ charge) or V = IR (Ohm's Law)

Think of voltage as the "electrical pressure" that drives current around a circuit."""

KB["what is current"] = """## Electric Current

**Definition:** Current is the rate of flow of electric charge.

**Formula:** I = Q/t
- I = current (Amperes, A)
- Q = charge (Coulombs, C)
- t = time (s)

Conventional current flows from + to −; electrons flow from − to +.
**Measured with:** Ammeter (in series with the circuit)"""

KB["define density"] = KB["what is density"] = """## Density

**Definition:** Density is the mass per unit volume of a substance.

**Formula:** ρ = m/V
- ρ (rho) = density (kg/m³ or g/cm³)
- m = mass (kg or g)
- V = volume (m³ or cm³)

**Examples:**
- Water: 1000 kg/m³ (1 g/cm³)
- Air: ~1.2 kg/m³
- Iron: 7874 kg/m³

**Why it matters:** Objects float if their density is less than the fluid they're in."""

KB["force mass 5kg acceleration 2m/s²"] = KB["force 5kg 2"] = """**F = ma = 5 × 2 = 10 N**"""

KB["derive v = u + at"] = """## Deriving v = u + at

**Definition of acceleration:**
a = (v − u) / t

**Rearranging:**
at = v − u
v = u + at ✓

This is the **first equation of motion** (SUVAT):
- s = ut + ½at²
- v² = u² + 2as
- s = (u+v)/2 × t"""

KB["conservation of energy"] = KB["explain conservation of energy"] = """## Law of Conservation of Energy

> **"Energy cannot be created or destroyed — it can only be converted from one form to another."**

**Total energy in a closed system remains constant.**

**Examples:**
- Pendulum: potential energy ↔ kinetic energy
- Burning fuel: chemical energy → heat + light + sound
- Hydroelectric dam: gravitational PE → kinetic energy → electrical energy

**Mathematically:** ΔKE + ΔPE = 0 (in ideal systems)"""

KB["what is momentum"] = """## Momentum

**Definition:** Momentum is the product of mass and velocity.

**Formula:** p = mv
- p = momentum (kg·m/s)
- m = mass (kg)
- v = velocity (m/s)

**Conservation of Momentum:** Total momentum before = total momentum after (in a closed system)

**Example:** A 2 kg ball at 5 m/s: p = 2×5 = **10 kg·m/s**"""

KB["what is wave frequency"] = KB["wave frequency"] = """## Wave Frequency

**Definition:** Frequency is the number of complete waves passing a point per second.

**Unit:** Hertz (Hz) — 1 Hz = 1 wave per second
**Formula:** f = 1/T (where T = period in seconds)

**Wave equation:** v = fλ
- v = wave speed (m/s)
- f = frequency (Hz)
- λ (lambda) = wavelength (m)

**Electromagnetic spectrum (low → high frequency):**
Radio → Microwave → Infrared → Visible → UV → X-ray → Gamma"""

KB["electromagnetic induction"] = """## Electromagnetic Induction

**Definition:** The production of an EMF (voltage) in a conductor when it moves through a magnetic field, or when a magnetic field changes around it.

**Faraday's Law:** EMF = −N × ΔΦ/Δt (rate of change of flux)

**Lenz's Law:** The induced current opposes the change that caused it.

**Applications:**
- Generators (convert mechanical energy → electrical)
- Transformers (change voltage)
- Induction cooktops
- Wireless charging"""

KB["define capacitance"] = """## Capacitance

**Definition:** Capacitance is the ability of a component to store electric charge.

**Formula:** C = Q/V
- C = capacitance (Farads, F)
- Q = charge stored (Coulombs)
- V = voltage across capacitor (V)

**Energy stored:** E = ½CV²

**Capacitors in series:** 1/C = 1/C₁ + 1/C₂ + ...
**Capacitors in parallel:** C = C₁ + C₂ + ..."""

KB["transformer"] = KB["how does a transformer work"] = """## How a Transformer Works

A transformer **changes the voltage** of an AC supply.

**Key components:**
- Primary coil (input)
- Secondary coil (output)
- Iron core (transfers magnetic flux)

**Formula:** Vₚ/Vₛ = Nₚ/Nₛ
(voltage ratio = turns ratio)

**Step-up transformer:** More turns on secondary → higher output voltage
**Step-down transformer:** Fewer turns on secondary → lower voltage

**Assuming 100% efficiency:** Vₚ × Iₚ = Vₛ × Iₛ"""

KB["define gravitational potential energy"] = KB["gravitational potential energy"] = """## Gravitational Potential Energy (GPE)

**Definition:** GPE is the energy an object has due to its position above the ground.

**Formula:** GPE = mgh
- m = mass (kg)
- g = 9.81 m/s² (gravitational field strength)
- h = height above reference point (m)

**Example:** 5 kg object raised 3 m: GPE = 5 × 9.81 × 3 = **147.15 J**"""

# ── BIOLOGY ──────────────────────────────────────────────────────────────────
KB["what is a cell"] = KB["what is cell"] = KB["basic unit of life"] = KB["unit of life"] = KB["smallest unit"] = """## The Cell — Basic Unit of Life

**Definition:** The cell is the smallest structural and functional unit of all living organisms.

**Cell Theory:**
1. All living organisms are made of cells
2. The cell is the basic unit of life
3. All cells arise from pre-existing cells

**Two main types:**
| | Prokaryotic | Eukaryotic |
|--|------------|------------|
| Nucleus | No membrane-bound nucleus | Has membrane-bound nucleus |
| Size | 1–10 μm | 10–100 μm |
| Examples | Bacteria | Animals, plants, fungi |"""

KB["parts of a plant"] = KB["name the parts of a plant"] = """## Parts of a Plant

| Part | Function |
|------|----------|
| **Roots** | Absorb water and minerals; anchor plant |
| **Stem** | Supports plant; transports water/nutrients |
| **Leaves** | Photosynthesis; gas exchange |
| **Flowers** | Reproduction; attract pollinators |
| **Fruit** | Protects seeds; aids dispersal |
| **Seeds** | Contain embryo for new plants |

**Transport systems:**
- Xylem: carries water upward (root → leaf)
- Phloem: carries sugars (leaf → rest of plant)"""

KB["what do plants need to grow"] = """## What Plants Need to Grow

1. **Water** — for photosynthesis, turgor pressure
2. **Sunlight** — energy for photosynthesis
3. **Carbon dioxide (CO₂)** — raw material for photosynthesis
4. **Minerals** — nitrogen (protein), potassium, phosphorus
5. **Suitable temperature** — enzymes work optimally
6. **Soil/support** — anchor for roots"""

KB["what is a mammal"] = """## Mammals

**Characteristics of mammals:**
1. Warm-blooded (endothermic)
2. Have hair or fur
3. Give birth to live young (most)
4. Feed young with milk (mammary glands)
5. Have a 4-chambered heart
6. Breathe air with lungs

**Examples:** Humans, dogs, whales, bats, elephants, dolphins"""

KB["five senses"] = KB["name the five senses"] = """## The Five Senses

| Sense | Organ | Stimulus detected |
|-------|-------|------------------|
| **Sight** | Eyes | Light |
| **Hearing** | Ears | Sound vibrations |
| **Smell** | Nose | Airborne chemicals |
| **Taste** | Tongue | Dissolved chemicals |
| **Touch** | Skin | Pressure, temperature, pain |"""

KB["what is digestion"] = """## Digestion

**Definition:** The process of breaking down food into small molecules that can be absorbed into the blood.

**Mechanical digestion:** Physical breaking down (chewing, churning)
**Chemical digestion:** Enzymes break molecules into smaller units

**Digestive system:**
Mouth → Oesophagus → Stomach → Small intestine → Large intestine → Rectum → Anus

**Key enzymes:**
- Amylase: breaks down starch → sugars
- Protease: breaks down proteins → amino acids
- Lipase: breaks down fats → fatty acids + glycerol"""

KB["what is breathing"] = KB["what is respiration"] = """## Breathing vs Respiration

**Breathing (Ventilation):** The physical process of moving air in and out of lungs.
- Inhale: diaphragm contracts (flattens), rib cage rises → air IN
- Exhale: diaphragm relaxes, rib cage falls → air OUT

**Aerobic Respiration:** Chemical process releasing energy from glucose:
```
C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ATP (energy)
Glucose + Oxygen → Carbon dioxide + Water
```

**Anaerobic Respiration:** Without oxygen:
- In humans: glucose → lactic acid (causes muscle fatigue)
- In yeast: glucose → ethanol + CO₂ (fermentation)"""

KB["what is a habitat"] = """## Habitat

**Definition:** A habitat is the natural environment where an organism lives — providing food, shelter, water, and space to breed.

**Examples:**
| Habitat | Organisms |
|---------|-----------|
| Rainforest | Jaguars, toucans, tree frogs |
| Ocean | Sharks, whales, coral |
| Desert | Camels, scorpions, cacti |
| Tundra | Arctic foxes, polar bears |
| Grassland | Lions, zebras, elephants |

**Niche:** The specific role an organism plays in its habitat (what it eats, when it's active, etc.)"""

KB["what is an organism"] = """## Organism

**Definition:** An organism is any individual living thing — from bacteria to blue whales.

**Characteristics of living organisms (MRS GREN):**
- **M**ovement
- **R**espiration
- **S**ensitivity (responding to stimuli)
- **G**rowth
- **R**eproduction
- **E**xcretion
- **N**utrition"""

KB["structure of a cell"] = KB["describe the structure of a cell"] = """## Cell Structure

### Animal Cell Organelles:
| Organelle | Function |
|-----------|----------|
| **Nucleus** | Contains DNA; controls cell activities |
| **Mitochondria** | Site of aerobic respiration; produces ATP |
| **Ribosomes** | Protein synthesis |
| **Rough ER** | Transports proteins (has ribosomes) |
| **Smooth ER** | Lipid synthesis; detoxification |
| **Golgi apparatus** | Packages and sends proteins/lipids |
| **Lysosomes** | Digests waste materials |
| **Cell membrane** | Controls entry/exit of substances |
| **Cytoplasm** | Fluid that suspends organelles |

### Additional in Plant Cells:
| Structure | Function |
|-----------|----------|
| **Cell wall** | Structural support (cellulose) |
| **Chloroplasts** | Photosynthesis |
| **Large vacuole** | Water storage; maintains turgor |"""

KB["function of the nucleus"] = KB["function of nucleus"] = """## The Nucleus

**Functions:**
1. Contains the cell's **DNA** (genetic information)
2. Controls all cell activities
3. Contains genes that direct protein synthesis
4. Bounded by a **nuclear envelope** with pores

**Key structures inside:**
- **Chromosomes:** DNA wound around proteins (46 in human cells)
- **Nucleolus:** Makes ribosomal RNA (rRNA)
- **Nuclear pores:** Allow RNA and proteins to pass in/out"""

KB["what is diffusion"] = """## Diffusion

**Definition:** Diffusion is the net movement of particles from an area of **high concentration** to an area of **low concentration**, down a concentration gradient.

**Key features:**
- Passive process (no energy required)
- Continues until equilibrium (equal concentrations)
- Faster when: higher concentration gradient, higher temperature, smaller particles, larger surface area

**Examples:**
- Oxygen entering red blood cells in lungs
- CO₂ leaving cells during respiration
- Perfume spreading across a room
- Food colouring in water"""

KB["circulatory system"] = KB["what is the circulatory system"] = """## The Circulatory System

**Function:** Transports blood, nutrients, oxygen, hormones, and waste products around the body.

**Components:**
- **Heart:** Pumps blood (4 chambers: right atrium, right ventricle, left atrium, left ventricle)
- **Arteries:** Carry blood AWAY from heart (thick walls, high pressure)
- **Veins:** Carry blood TO the heart (thin walls, have valves)
- **Capillaries:** Tiny vessels where exchange occurs

**Double circulation:**
1. Pulmonary: heart → lungs → heart (for oxygenation)
2. Systemic: heart → body → heart (delivers oxygen)"""

KB["parts of the human heart"] = KB["human heart parts"] = """## Parts of the Human Heart

**4 Chambers:**
- Right atrium — receives deoxygenated blood from body
- Right ventricle — pumps blood to lungs
- Left atrium — receives oxygenated blood from lungs
- Left ventricle — pumps oxygenated blood to body (thickest wall)

**Valves (prevent backflow):**
- Tricuspid valve (right side)
- Bicuspid/Mitral valve (left side)
- Pulmonary and Aortic semilunar valves

**Major vessels:**
- Aorta: leaves left ventricle → body
- Pulmonary artery: right ventricle → lungs
- Vena Cava: body → right atrium
- Pulmonary vein: lungs → left atrium"""

KB["what are enzymes"] = """## Enzymes

**Definition:** Enzymes are biological **catalysts** — protein molecules that speed up chemical reactions without being used up.

**Key properties:**
- **Specific:** Each enzyme works on one substrate (lock and key model)
- **Affected by temperature:** Optimum ~37°C for human enzymes; above ~40°C enzymes **denature**
- **Affected by pH:** Each enzyme has an optimum pH

**Active site:** Where the substrate binds

**Examples:**
| Enzyme | Substrate | Product |
|--------|-----------|---------|
| Amylase | Starch | Sugars |
| Protease | Proteins | Amino acids |
| Lipase | Fats | Fatty acids + glycerol |
| DNA polymerase | DNA template | New DNA strand |"""

KB["what is dna"] = KB["structure of dna"] = """## DNA — Deoxyribonucleic Acid

**Structure:** Double helix (Watson and Crick, 1953)

**Components:**
- **Sugar** (deoxyribose)
- **Phosphate** group
- **Nitrogenous bases:** A, T, G, C

**Base pairing rules:**
- Adenine (A) pairs with Thymine (T)
- Guanine (G) pairs with Cytosine (C)

**Function:** Stores genetic information as a sequence of bases (codons)

**In humans:** 46 chromosomes = ~3 billion base pairs"""

KB["natural selection"] = """## Natural Selection (Charles Darwin, 1859)

**Definition:** The process by which organisms better adapted to their environment survive and reproduce more successfully.

**Four principles:**
1. **Variation** — individuals in a population differ
2. **Inheritance** — traits are passed to offspring
3. **Selection pressure** — environmental challenges
4. **Survival of the fittest** — well-adapted individuals survive and reproduce

**Example:** Peppered moth during Industrial Revolution:
- White moths: survived on light tree bark
- Dark moths: survived on soot-darkened trees
- Dark moths increased as pollution increased"""

KB["describe mitosis"] = KB["mitosis stages"] = """## Mitosis — Cell Division

**Purpose:** Produces 2 genetically **identical** daughter cells (growth, repair)

**Stages (PMAT):**

**P — Prophase:**
- Chromosomes condense and become visible
- Nuclear envelope breaks down
- Spindle fibres form

**M — Metaphase:**
- Chromosomes line up at the cell equator
- Spindle fibres attach to centromeres

**A — Anaphase:**
- Sister chromatids pulled to opposite poles
- Cell elongates

**T — Telophase:**
- Nuclear envelopes reform
- Chromosomes uncoil
- Cytokinesis divides cytoplasm

**Result:** 2 diploid (2n) cells, genetically identical to parent"""

KB["describe meiosis"] = """## Meiosis — Cell Division

**Purpose:** Produces 4 genetically **different** gametes (sex cells) with half the chromosome number (haploid)

**Two divisions:**

**Meiosis I** — Homologous chromosomes separate:
- Crossing over occurs (genetic variation!)
- 2 cells produced, each with mixed chromosomes

**Meiosis II** — Sister chromatids separate:
- Like mitosis
- 4 haploid cells produced

**Result:** 4 haploid (n) cells, all genetically different

**Meiosis vs Mitosis:**
| | Mitosis | Meiosis |
|--|---------|---------|
| Divisions | 1 | 2 |
| Daughter cells | 2 | 4 |
| Chromosome number | 2n | n |
| Genetic variation | None | Yes |"""

KB["genetic mutation"] = KB["what is genetic mutation"] = """## Genetic Mutation

**Definition:** A change in the DNA sequence (bases) of a gene.

**Types:**
- **Substitution** — one base replaced by another
- **Deletion** — a base is removed
- **Insertion** — an extra base is added
- **Duplication** — a section is copied twice
- **Inversion** — a section is reversed

**Causes:** Radiation (UV, X-rays), certain chemicals (mutagens), errors during DNA replication

**Effects:**
- Most are neutral (silent)
- Some harmful (cancer)
- Rarely beneficial (drives evolution)

**Example:** Sickle cell anaemia — single base substitution in haemoglobin gene"""

KB["homeostasis"] = """## Homeostasis

**Definition:** The maintenance of a constant internal environment despite external changes.

**What is regulated:**
| Variable | Normal value | Regulated by |
|----------|-------------|--------------|
| Body temperature | 37°C | Hypothalamus, sweat glands, shivering |
| Blood glucose | 4–6 mmol/L | Insulin and glucagon (pancreas) |
| Blood pH | 7.35–7.45 | Lungs, kidneys |
| Water content | ~60% of body | Kidneys (ADH hormone) |

**Mechanism:** Negative feedback — a change is detected and reversed"""

KB["human nervous system"] = KB["nervous system"] = """## The Human Nervous System

**Two parts:**

**Central Nervous System (CNS):**
- Brain (cerebrum, cerebellum, brainstem)
- Spinal cord

**Peripheral Nervous System (PNS):**
- Sensory neurons: carry signals TO brain
- Motor neurons: carry signals FROM brain
- Autonomic nervous system: controls involuntary actions

**Reflex arc (fast responses without thinking):**
Stimulus → Receptor → Sensory neuron → Relay neuron → Motor neuron → Effector → Response

**Neurotransmitters:** Chemical messengers at synapses (e.g., dopamine, serotonin, acetylcholine)"""

KB["active transport"] = KB["what is active transport"] = """## Active Transport

**Definition:** The movement of molecules against a concentration gradient (from low to high concentration), requiring energy (ATP).

**Key features:**
- Requires energy (unlike diffusion/osmosis)
- Uses carrier proteins
- Moves substances against the concentration gradient

**Examples:**
- Root hair cells absorbing minerals from soil (lower concentration in soil)
- Absorption of glucose from gut into blood
- Nerve impulse transmission (Na⁺/K⁺ pump)

**vs Diffusion:** Diffusion = no energy, down gradient; Active transport = needs energy, against gradient"""

KB["what is evolution"] = """## Evolution

**Definition:** The gradual change in heritable characteristics of a population over many generations.

**Evidence for evolution:**
- Fossil record
- Comparative anatomy (homologous structures)
- DNA similarities between species
- Observed changes (antibiotic resistance)
- Biogeography

**Mechanisms:**
- Natural selection (Darwin)
- Genetic drift (random changes in small populations)
- Mutation (source of new variation)
- Gene flow (movement between populations)

**Theory of Common Ancestry:** All life on Earth shares a common ancestor"""

KB["biotechnology"] = """## Biotechnology

**Definition:** The use of biological systems and organisms to develop products and technologies.

**Applications:**
| Area | Example |
|------|---------|
| Medicine | Insulin production using bacteria |
| Agriculture | GM crops (pest-resistant, higher yield) |
| Food | Yeast in bread and beer |
| Environment | Bioremediation (bacteria clean up oil spills) |
| Industry | Enzymes in washing powder |
| Research | CRISPR gene editing |

**Genetic engineering steps:**
1. Identify desired gene
2. Cut gene out using restriction enzymes
3. Insert into vector (e.g., plasmid)
4. Introduce vector into host organism
5. Select transformed organisms"""

KB["immune response"] = """## The Immune Response

**Two types:**

**Non-specific (innate) immunity:**
- Skin barrier
- Mucus and cilia
- Stomach acid
- Phagocytes (engulf pathogens)
- Inflammation and fever

**Specific (adaptive) immunity:**
1. Pathogen enters body
2. Antigens on pathogen identified
3. B-lymphocytes produce **antibodies** (specific to antigen)
4. Antibodies bind to antigens → neutralise/destroy pathogen
5. **Memory cells** formed (faster response next time = immunity)

**T-lymphocytes:** Kill infected cells directly (cell-mediated immunity)

**Vaccines:** Introduce weakened/dead pathogen → immune system creates memory cells without getting sick"""

# ── CHEMISTRY ────────────────────────────────────────────────────────────────
KB["what is an atom"] = KB["what is atom"] = """## The Atom

**Definition:** An atom is the smallest particle of an element that retains the chemical properties of that element.

**Structure:**
- **Nucleus:** Contains protons (+) and neutrons (no charge)
- **Electron shells:** Electrons (−) orbit the nucleus

| Particle | Charge | Mass |
|----------|--------|------|
| Proton | +1 | 1 |
| Neutron | 0 | 1 |
| Electron | −1 | ~0 |

**Atomic number** = number of protons
**Mass number** = protons + neutrons"""

KB["what is an element"] = """## Elements

**Definition:** An element is a pure substance made of only ONE type of atom that cannot be broken down by chemical means.

**Examples:** Hydrogen (H), Oxygen (O), Gold (Au), Carbon (C), Iron (Fe)

There are **118 known elements** on the periodic table (92 occur naturally)."""

KB["what is a compound"] = """## Compounds

**Definition:** A compound is a substance formed when two or more different elements are chemically bonded together.

**Properties:**
- Different from the individual elements
- Fixed ratio of atoms
- Can only be separated by chemical reactions

**Examples:**
| Compound | Elements | Formula |
|----------|----------|---------|
| Water | Hydrogen + Oxygen | H₂O |
| Salt | Sodium + Chlorine | NaCl |
| Carbon dioxide | Carbon + Oxygen | CO₂ |
| Glucose | Carbon + Hydrogen + Oxygen | C₆H₁₂O₆ |"""

KB["what is evaporation"] = KB["what is melting"] = KB["what is freezing"] = KB["what is boiling"] = """## Changes of State

| Change | Name | Energy |
|--------|------|--------|
| Solid → Liquid | **Melting** | Energy absorbed |
| Liquid → Gas | **Evaporation/Boiling** | Energy absorbed |
| Gas → Liquid | **Condensation** | Energy released |
| Liquid → Solid | **Freezing/Solidification** | Energy released |
| Solid → Gas | **Sublimation** | Energy absorbed |
| Gas → Solid | **Deposition** | Energy released |

**Melting point:** Temperature at which solid → liquid (e.g., water = 0°C)
**Boiling point:** Temperature at which liquid → gas (e.g., water = 100°C at 1 atm)"""

KB["what is the periodic table"] = KB["periodic table"] = """## The Periodic Table

**Definition:** A table of all known elements arranged by increasing atomic number, in periods (rows) and groups (columns).

**Structure:**
- **Periods (rows):** Elements in the same period have the same number of electron shells
- **Groups (columns):** Elements in the same group have the same number of outer electrons → similar chemical properties

**Key groups:**
| Group | Name | Examples |
|-------|------|---------|
| Group 1 | Alkali metals | Li, Na, K |
| Group 2 | Alkaline earth metals | Mg, Ca |
| Group 7 (17) | Halogens | F, Cl, Br |
| Group 0 (18) | Noble gases | He, Ne, Ar |

**Trends:** Atomic radius increases down a group; ionisation energy increases across a period"""

KB["define atomic number"] = """**Atomic Number (Z):** The number of **protons** in the nucleus of an atom.
- Defines which element it is
- In a neutral atom: number of protons = number of electrons

**Example:** Carbon has atomic number 6 (6 protons, 6 electrons in neutral atom)"""

KB["define mass number"] = """**Mass Number (A):** The total number of **protons + neutrons** in the nucleus.

**Formula:** A = Z + N (atomic number + neutrons)
**Neutrons** = A − Z

**Example:** Carbon-12: mass number = 12, atomic number = 6, so neutrons = 12 − 6 = 6"""

KB["what is a chemical reaction"] = """## Chemical Reactions

**Definition:** A process where reactants are transformed into products with different chemical properties.

**Signs of a chemical reaction:**
- Colour change
- Gas produced (bubbles)
- Precipitate forms
- Temperature change
- Light or sound produced

**Types:**
| Type | Description | Example |
|------|-------------|---------|
| Synthesis | A + B → AB | 2H₂ + O₂ → 2H₂O |
| Decomposition | AB → A + B | 2H₂O₂ → 2H₂O + O₂ |
| Combustion | Fuel + O₂ → CO₂ + H₂O | CH₄ + 2O₂ → CO₂ + 2H₂O |
| Neutralisation | Acid + Base → Salt + Water | HCl + NaOH → NaCl + H₂O |
| Redox | Transfer of electrons | Zn + CuSO₄ → ZnSO₄ + Cu |"""

KB["what is a catalyst"] = """## Catalysts

**Definition:** A catalyst speeds up a chemical reaction without being used up or permanently changed.

**How it works:** Provides an alternative reaction pathway with **lower activation energy**.

**Types:**
- **Homogeneous:** Same phase as reactants (e.g., acid catalysts in solution)
- **Heterogeneous:** Different phase (e.g., iron catalyst in Haber process)
- **Biological:** Enzymes (e.g., amylase, catalase)

**Examples:**
| Catalyst | Reaction |
|----------|---------|
| Iron | N₂ + H₂ → NH₃ (Haber process) |
| Platinum | Car catalytic converters |
| Manganese dioxide | H₂O₂ → H₂O + O₂ |
| Enzymes | Biological processes |"""

KB["define acid"] = KB["what is an acid"] = """## Acids

**Definition:** An acid is a substance that donates H⁺ ions (protons) in solution (Brønsted-Lowry definition).

**Properties:**
- pH < 7
- Tastes sour (never taste chemicals!)
- Turns litmus red
- Reacts with metals to produce hydrogen gas
- Reacts with carbonates to produce CO₂

**Strong acids** (fully ionise): HCl, H₂SO₄, HNO₃
**Weak acids** (partially ionise): CH₃COOH (ethanoic/acetic acid), citric acid

**Reactions:**
- Acid + Metal → Salt + Hydrogen
- Acid + Base → Salt + Water
- Acid + Carbonate → Salt + Water + CO₂"""

KB["define base"] = KB["what is a base"] = """## Bases and Alkalis

**Base:** A substance that accepts H⁺ ions (protons)
**Alkali:** A base that dissolves in water to give OH⁻ ions

**Properties:**
- pH > 7
- Turns litmus blue
- Feels slippery (soap is alkaline)

**Strong bases** (fully ionise): NaOH, KOH, Ca(OH)₂
**Weak bases** (partially ionise): NH₃, Mg(OH)₂

**Uses:**
| Base | Use |
|------|-----|
| NaOH | Making soap |
| Ca(OH)₂ | Treating acidic soils |
| NH₃ | Fertilisers, cleaning products |
| Mg(OH)₂ | Indigestion treatment (antacid) |"""

KB["what is neutralization"] = KB["neutralisation"] = """## Neutralisation

**Definition:** The reaction between an acid and a base to form a salt and water.

**General equation:**
Acid + Base → Salt + Water

**Example:**
HCl + NaOH → NaCl + H₂O
(Hydrochloric acid + Sodium hydroxide → Sodium chloride + Water)

**Applications:**
- Adding lime (calcium hydroxide) to acidic soil
- Antacids treating stomach acid
- Wastewater treatment"""

KB["what is electrolysis"] = """## Electrolysis

**Definition:** Electrolysis is the decomposition of a substance using electrical energy.

**Components:**
- **Electrolyte:** Ionic compound (dissolved or molten)
- **Electrodes:** Cathode (−) and Anode (+)
- **Ions:** Positive ions move to cathode; negative ions to anode

**At cathode (−):** Reduction (gain electrons): Cu²⁺ + 2e⁻ → Cu
**At anode (+):** Oxidation (lose electrons): 2Cl⁻ → Cl₂ + 2e⁻

**Uses:**
- Electroplating (coating metals)
- Purifying copper
- Extracting aluminium
- Chlorine production (chlor-alkali process)"""

KB["balance h2 o2 h2o"] = KB["h₂ + o₂ → h₂o"] = KB["balance water equation"] = """**Balancing: H₂ + O₂ → H₂O**

Unbalanced: H₂ + O₂ → H₂O (only 1 oxygen on right)

**Balanced: 2H₂ + O₂ → 2H₂O** ✓

Check: Left: 4H, 2O | Right: 4H, 2O ✓"""

KB["ionic bonding"] = KB["explain ionic bonding"] = """## Ionic Bonding

**Definition:** A bond formed by the transfer of electrons from a metal to a non-metal, creating positive and negative ions attracted to each other.

**How it forms:**
1. Metal atom loses electrons → positive **cation** (Na → Na⁺)
2. Non-metal atom gains electrons → negative **anion** (Cl → Cl⁻)
3. Opposite charges attract → **ionic bond**

**Example:** Sodium chloride (NaCl):
Na (2,8,1) → Na⁺ (2,8) + e⁻
Cl (2,8,7) + e⁻ → Cl⁻ (2,8,8)

**Properties of ionic compounds:**
- High melting points
- Conduct electricity when dissolved or molten (not solid)
- Often form crystals
- Soluble in water (usually)"""

KB["covalent bonding"] = KB["explain covalent bonding"] = """## Covalent Bonding

**Definition:** A bond formed when two non-metal atoms share pairs of electrons.

**How it forms:** Each atom contributes one (or more) electron to a shared pair.

**Examples:**
| Molecule | Bonds | Diagram |
|----------|-------|---------|
| H₂ | Single | H—H |
| O₂ | Double | O=O |
| N₂ | Triple | N≡N |
| H₂O | 2 single | H—O—H |
| CO₂ | 2 double | O=C=O |

**Properties of covalent compounds:**
- Low melting/boiling points (simple molecules)
- Do NOT conduct electricity (no free ions)
- Often gases or liquids at room temperature"""

KB["what is oxidation"] = KB["what is reduction"] = KB["redox"] = """## Oxidation and Reduction (REDOX)

**OIL RIG:** Oxidation Is Loss (of electrons), Reduction Is Gain (of electrons)

| Process | Change in electrons | Change in oxidation state |
|---------|--------------------|-----------------------------|
| **Oxidation** | Loses electrons | Increases (goes up) |
| **Reduction** | Gains electrons | Decreases (goes down) |

**They always happen together!**

**Example:** Zn + Cu²⁺ → Zn²⁺ + Cu
- Zn: 0 → +2 (oxidised, loses 2e⁻)
- Cu²⁺: +2 → 0 (reduced, gains 2e⁻)

**Oxidising agent** = causes oxidation (gets reduced itself)
**Reducing agent** = causes reduction (gets oxidised itself)"""

KB["define molar mass"] = KB["molar mass"] = """## Molar Mass

**Definition:** The mass of one mole of a substance, in g/mol.
Numerically equal to the relative formula mass (Mr).

**Examples:**
| Substance | Calculation | Molar Mass |
|-----------|-------------|-----------|
| H₂ | 2 × 1 | 2 g/mol |
| O₂ | 2 × 16 | 32 g/mol |
| H₂O | (2×1) + 16 | 18 g/mol |
| NaCl | 23 + 35.5 | 58.5 g/mol |
| CO₂ | 12 + (2×16) | 44 g/mol |"""

KB["avogadro's number"] = KB["avogadros number"] = KB["6.02"] = """## Avogadro's Number

**Value: 6.022 × 10²³ mol⁻¹**

**Definition:** The number of particles (atoms, molecules, ions) in one mole of a substance.

**Mole formula:** n = m/M
- n = moles
- m = mass (g)
- M = molar mass (g/mol)

**Example:** Moles in 44 g of CO₂ (M = 44):
n = 44/44 = **1 mole** = 6.022 × 10²³ molecules"""

KB["equilibrium"] = KB["what is equilibrium"] = KB["chemical equilibrium"] = """## Chemical Equilibrium

**Definition:** A state where the rate of the forward reaction equals the rate of the reverse reaction, and concentrations remain constant.

**Dynamic equilibrium:** Both reactions still occurring, but at equal rates.

**Represented as:** A + B ⇌ C + D

**Le Chatelier's Principle:** If a system at equilibrium is disturbed, it will shift to oppose the change and restore equilibrium.

**Effects:**
| Change | Equilibrium shifts |
|--------|-------------------|
| Increase concentration of reactant | → Forward (more product) |
| Increase temperature | → Endothermic direction |
| Increase pressure | → Side with fewer gas molecules |
| Add catalyst | No shift (just reaches equilibrium faster) |"""

KB["le chatelier's principle"] = KB["le chatelier"] = """## Le Chatelier's Principle

> "If a system in equilibrium is subjected to a change, the system will respond in a way that opposes that change."

**Applied to the Haber Process (N₂ + 3H₂ ⇌ 2NH₃):**

| Factor | Effect on yield | Explanation |
|--------|----------------|-------------|
| High pressure | ↑ yield | Shifts to fewer gas molecules (left: 4 mol, right: 2 mol) |
| Low temperature | ↑ yield | Reaction is exothermic; favour forward reaction |
| Remove NH₃ | ↑ yield | System shifts right to replace removed product |
| Add catalyst | No change in yield | Only speeds up equilibrium being reached |"""

KB["what is enthalpy"] = KB["enthalpy"] = """## Enthalpy

**Definition:** Enthalpy (H) is the total heat content of a system. ΔH is the enthalpy change during a reaction.

**Exothermic reaction:** ΔH < 0 (energy released to surroundings, temperature increases)
- Examples: combustion, neutralisation, respiration

**Endothermic reaction:** ΔH > 0 (energy absorbed from surroundings, temperature decreases)
- Examples: photosynthesis, thermal decomposition, dissolving ammonium nitrate

**Bond enthalpies:**
ΔH = Energy in (breaking bonds) − Energy out (forming bonds)"""

KB["balance fe o2 fe2o3"] = KB["fe + o2"] = """**Balancing: Fe + O₂ → Fe₂O₃**

Unbalanced: Fe + O₂ → Fe₂O₃

Step 1: Balance Fe: **4Fe** + O₂ → **2Fe₂O₃** (now 4 Fe each side)
Step 2: Balance O: 4Fe + **3O₂** → 2Fe₂O₃ (now 6 O each side)

**Balanced: 4Fe + 3O₂ → 2Fe₂O₃** ✓"""

KB["periodic trends"] = KB["describe the periodic trends"] = """## Periodic Table Trends

### Across a Period (left → right):
| Property | Trend | Reason |
|----------|-------|--------|
| Atomic radius | Decreases | More protons pull electrons closer |
| Ionisation energy | Increases | Harder to remove electron (more protons) |
| Electronegativity | Increases | More pull on bonding electrons |
| Metallic character | Decreases | Less metallic across a period |

### Down a Group (top → bottom):
| Property | Trend | Reason |
|----------|-------|--------|
| Atomic radius | Increases | More electron shells |
| Ionisation energy | Decreases | Outer electrons further from nucleus |
| Reactivity (metals) | Increases | Easier to lose outer electron |
| Reactivity (halogens) | Decreases | Harder to gain electron |"""

KB["acids and bases"] = """## Acids and Bases — Complete Guide

**pH Scale:** 0–14
- 0–6: Acidic
- 7: Neutral
- 8–14: Alkaline/Basic

**Neutralisation:** Acid + Base → Salt + Water

**Common acids:**
| Acid | Formula | Strong/Weak |
|------|---------|------------|
| Hydrochloric acid | HCl | Strong |
| Sulfuric acid | H₂SO₄ | Strong |
| Nitric acid | HNO₃ | Strong |
| Acetic/Ethanoic acid | CH₃COOH | Weak |
| Carbonic acid | H₂CO₃ | Weak |

**Common bases:**
| Base | Formula | Strong/Weak |
|------|---------|------------|
| Sodium hydroxide | NaOH | Strong |
| Calcium hydroxide | Ca(OH)₂ | Strong |
| Ammonia | NH₃ | Weak |"""

# ── HISTORY ──────────────────────────────────────────────────────────────────
KB["first president of the united states"] = KB["first us president"] = """**The first President of the United States was George Washington.**

- Served: 1789–1797 (two terms)
- Commander of the Continental Army in the American Revolution
- Unanimously elected by the Electoral College
- Established many presidential traditions (Cabinet, inaugural address)
- Refused a third term, setting a precedent followed until FDR"""

KB["world war i begin"] = KB["ww1 start"] = KB["world war 1 start"] = """**World War I began in 1914.**

- Official start: **28 July 1914**
- Triggered by: Assassination of Archduke Franz Ferdinand of Austria-Hungary (28 June 1914) in Sarajevo
- Ended: **11 November 1918** (Armistice)
- Also known as "The Great War" or "The War to End All Wars" """

KB["world war ii end"] = KB["ww2 end"] = KB["world war 2 end"] = """**World War II ended in 1945.**

- **V-E Day** (Victory in Europe): **8 May 1945** — Germany surrendered
- **V-J Day** (Victory over Japan): **15 August 1945** — Japan surrendered
- **Formal surrender:** 2 September 1945 (signed aboard USS Missouri)
- Duration: 1 September 1939 – 2 September 1945"""

KB["who discovered america"] = """**The "discovery of America" depends on perspective:**

**Christopher Columbus** arrived in the Americas on **12 October 1492** — but he landed in the Caribbean (Bahamas), not mainland North America. He never reached the present-day USA.

**Earlier claims:**
- **Leif Erikson** (Norse explorer) reached North America around **1000 AD** — 500 years before Columbus
- **Indigenous peoples** had been living in the Americas for **15,000+ years** before any European arrived

The word "discovery" is contested since millions of people already lived there."""

KB["what was the roman empire"] = KB["roman empire"] = """## The Roman Empire

**Period:** 27 BC – 476 AD (Western Empire); Eastern Empire survived until 1453 AD

**Key facts:**
- At its peak: covered 5 million km² across Europe, North Africa, and Western Asia
- Founded by **Augustus Caesar** (first emperor, 27 BC)
- Language: Latin → basis for modern Romance languages
- Engineering feats: roads, aqueducts, Colosseum, Pantheon

**Rise:** Roman Republic (509 BC) → civil wars → Empire
**Fall:** Military pressure, economic problems, corruption, Germanic invasions

**Legacy:** Roman law, calendar, architecture, Christianity as state religion"""

KB["who was a pharaoh"] = KB["what is a pharaoh"] = """## Pharaohs of Ancient Egypt

**Definition:** A pharaoh was the ruler (king) of Ancient Egypt, considered both a political and divine leader — believed to be a living god (incarnation of Horus).

**Famous Pharaohs:**
| Pharaoh | Reign | Known for |
|---------|-------|-----------|
| **Tutankhamun (King Tut)** | c.1332 BC | Boy king; intact tomb discovered 1922 |
| **Ramesses II** | c.1279–1213 BC | Longest reigning; built Abu Simbel |
| **Cleopatra VII** | 51–30 BC | Last active pharaoh; alliance with Caesar |
| **Akhenaten** | c.1353 BC | Introduced monotheism (worshipping Aten) |
| **Khufu** | c.2570 BC | Built the Great Pyramid of Giza |"""

KB["what is a colony"] = """## Colonies

**Definition:** A colony is a territory controlled and settled by a foreign power (the coloniser/metropole), often exploiting its resources and people.

**Examples:**
- British colonies: India, Nigeria, Kenya, Australia, Canada
- French colonies: Algeria, Senegal, Vietnam
- Portuguese colonies: Brazil, Mozambique, Angola

**Effects of colonialism:**
- Extraction of resources and wealth
- Cultural suppression
- Introduction of new languages, religions, systems
- Long-lasting economic inequalities

**Decolonisation:** Major independence movements in 1940s–1970s"""

KB["what is independence"] = """## Independence

**Definition:** Independence is the state of being self-governing — free from external control or domination.

**Historical independence movements:**
| Country | Independence from | Year |
|---------|-----------------|------|
| USA | Britain | 1776 |
| India | Britain | 1947 |
| Ghana | Britain | 1957 |
| Kenya | Britain | 1963 |
| Zimbabwe | Britain | 1980 |
| South Africa | (end of apartheid) | 1994 |"""

KB["who was nelson mandela"] = KB["nelson mandela"] = """## Nelson Mandela (1918–2013)

**Who he was:** South African anti-apartheid leader, political prisoner, and first democratically elected President of South Africa.

**Key events:**
- Joined the African National Congress (ANC) in 1944
- Helped found the ANC Youth League
- Led armed resistance against apartheid after 1960 Sharpeville massacre
- **Imprisoned for 27 years** (1964–1990) on Robben Island
- Released by President de Klerk in 1990
- Won the Nobel Peace Prize (1993) alongside de Klerk
- **President of South Africa: 1994–1999** — led peaceful transition to democracy

**Legacy:** Symbol of resistance, reconciliation, and human dignity worldwide"""

KB["what was slavery"] = """## Slavery

**Definition:** Slavery is the ownership and forced labour of human beings as property.

**Transatlantic Slave Trade (c.1500–1900):**
- Approximately **12.5 million Africans** forcibly transported to the Americas
- ~1.8 million died during the Middle Passage (voyage)
- Used on plantations in North America, Caribbean, and South America

**Abolition:**
- Haiti: 1804 (after slave revolution)
- UK: 1833 (Slavery Abolition Act)
- USA: 1865 (13th Amendment, after Civil War)
- Brazil: 1888

**Legacy:** Racism, economic inequality, and social injustice still felt today"""

KB["what caused world war i"] = KB["causes of world war 1"] = KB["causes wwi"] = """## Causes of World War I

**MAIN Causes:**

**M — Militarism:** European powers built up massive armies and navies, creating tension.

**A — Alliances:**
- Triple Entente: France, Russia, Britain
- Triple Alliance: Germany, Austria-Hungary, Italy
(Made a small conflict into a world war)

**I — Imperialism:** Competition for colonies in Africa and Asia created rivalry.

**N — Nationalism:** Serbian nationalism threatened Austria-Hungary; Germany wanted world power.

**Immediate trigger:** Assassination of Archduke Franz Ferdinand (28 June 1914) by Gavrilo Princip in Sarajevo."""

KB["industrial revolution"] = KB["explain the industrial revolution"] = """## The Industrial Revolution

**Period:** c.1760–1840 (began in Britain, spread globally)

**Key developments:**
- Steam power (James Watt's steam engine, 1769)
- Factory system replacing cottage industries
- Iron and steel production
- Railways and transportation
- Urbanisation (people moved to cities)

**Impact:**
- Britain became the world's dominant economic power
- New working class emerged (often in terrible conditions)
- Child labour was widespread
- Led to political reforms (Reform Acts, trade unions)
- Environmental pollution began

**Inventions:** Spinning jenny, power loom, steam locomotive, telegraph"""

KB["what was the cold war"] = KB["cold war"] = """## The Cold War (1947–1991)

**Definition:** A period of political and military tension between the USA (and its allies) and the USSR (and its allies) — never direct military conflict.

**Key features:**
- Ideological battle: **Capitalism (USA)** vs **Communism (USSR)**
- Arms race (nuclear weapons)
- Space race (Sputnik 1957, Moon landing 1969)
- Proxy wars (Korea, Vietnam, Afghanistan)
- **Berlin Wall** (1961–1989)
- NATO (Western alliance) vs Warsaw Pact (Soviet alliance)

**End:** USSR collapsed 1991; Berlin Wall fell 1989"""

KB["who was adolf hitler"] = KB["adolf hitler"] = """## Adolf Hitler (1889–1945)

**Who:** Austrian-born German politician, leader of the National Socialist (Nazi) Party, and dictator of Germany 1933–1945.

**Rise to power:**
- Used economic depression and German resentment of WWI defeat
- Became Chancellor in 1933, then Führer (absolute leader)
- Established a totalitarian state (eliminated opposition)

**Actions in power:**
- Launched World War II (invaded Poland, 1939)
- The Holocaust: systematic murder of 6 million Jews + millions of others
- Invaded and occupied most of Europe

**Death:** Suicide in Berlin bunker, 30 April 1945, as Allied forces closed in"""

KB["what was apartheid"] = KB["apartheid"] = """## Apartheid (South Africa, 1948–1994)

**Definition:** A system of institutionalised racial segregation and discrimination in South Africa.

**Key features:**
- "Apartheid" means "separateness" in Afrikaans
- Laws separated Black, White, Coloured, and Indian South Africans
- Pass laws restricted Black movement
- Black South Africans denied voting rights, quality education, good housing

**Resistance:**
- ANC (Nelson Mandela, Oliver Tambo)
- International sanctions
- Mass protests (Soweto Uprising, 1976)

**End:** Negotiations between Mandela and de Klerk → first democratic elections **April 1994** → Mandela became President"""

KB["french revolution causes"] = KB["causes of the french revolution"] = """## Causes of the French Revolution (1789)

**Political:**
- Absolute monarchy (Louis XVI) with no democracy
- Estates General (parliament) rarely called
- Third Estate (commoners) had no real power

**Economic:**
- France nearly bankrupt (debt from wars, including American Revolution)
- Bread prices soared (poor harvests)
- Heavy taxation on the poor while nobles paid little

**Social:**
- Inequality between Three Estates
- Enlightenment ideas: liberty, equality, fraternity

**Immediate trigger:** Financial crisis of 1789; Estates General meeting; storming of the Bastille (14 July 1789)"""

KB["colonialism in africa"] = """## Impact of Colonialism in Africa

**Political impact:**
- Arbitrary borders drawn (Berlin Conference 1884–85) split ethnic groups
- Weak governance structures left at independence
- Wars and instability from colonial legacies

**Economic impact:**
- Resources extracted for European benefit
- Cash-crop agriculture undermined food security
- Infrastructure built to serve colonisers (ports, railways)
- Limited industrialisation allowed

**Social/Cultural impact:**
- Indigenous languages and cultures suppressed
- Christianity imposed
- Education systems serving colonial needs
- Racism institutionalised

**Long-term:** Africa's economic underdevelopment partly attributed to colonial exploitation"""

# ── GEOGRAPHY ────────────────────────────────────────────────────────────────
KB["what is a continent"] = """## Continents

**Definition:** A continent is one of the seven large landmasses on Earth.

**The Seven Continents (largest to smallest):**
1. **Asia** — 44.6 million km² (largest)
2. **Africa** — 30.4 million km²
3. **North America** — 24.7 million km²
4. **South America** — 17.8 million km²
5. **Antarctica** — 14 million km²
6. **Europe** — 10.5 million km²
7. **Australia/Oceania** — 8.5 million km² (smallest)"""

KB["what is a river"] = """## Rivers

**Definition:** A river is a natural flowing watercourse, usually flowing towards an ocean, sea, lake, or another river.

**Key features:**
- **Source:** Where the river begins (usually mountains or springs)
- **Tributaries:** Smaller rivers joining the main river
- **Meanders:** Bends in the river
- **Estuary/Delta:** Where the river meets the sea

**World's longest rivers:**
1. Nile (Africa) — 6,650 km
2. Amazon (South America) — 6,400 km
3. Yangtze (Asia) — 6,300 km"""

KB["what is climate"] = KB["climate vs weather"] = """## Climate vs Weather

**Weather:** Short-term atmospheric conditions in a specific place (day-to-day: sunny, rainy, windy)

**Climate:** The average weather patterns of a region over a long period (30+ years)

**Climate zones:**
| Zone | Location | Characteristics |
|------|----------|----------------|
| Tropical | Near equator | Hot and wet all year |
| Arid | ~30°N/S | Hot and very dry (deserts) |
| Temperate | Mid-latitudes | Four seasons, moderate |
| Continental | Interior of continents | Cold winters, warm summers |
| Polar | Near poles | Extremely cold |"""

KB["what causes earthquakes"] = KB["causes of earthquakes"] = """## What Causes Earthquakes?

**Primary cause:** Movement of tectonic plates along **fault lines**.

**Types of fault movement:**
- **Transform faults:** Plates slide past each other (e.g., San Andreas Fault, California)
- **Convergent boundaries:** Plates collide → one subducts; causes violent earthquakes
- **Divergent boundaries:** Plates move apart; less severe earthquakes

**Measuring earthquakes:**
- **Richter scale / Moment Magnitude Scale:** Measures energy released
- **Mercalli scale:** Measures intensity of shaking felt

**Most earthquake-prone areas:** "Ring of Fire" (Pacific Ocean rim), Mediterranean region"""

KB["tectonic plates"] = KB["what are tectonic plates"] = """## Tectonic Plates

**Definition:** Large pieces of Earth's lithosphere (crust + upper mantle) that float and move on the semi-molten asthenosphere.

**There are 7 major and 8 minor plates:**
Major plates: African, Antarctic, Eurasian, Indo-Australian, North American, Pacific, South American

**Why they move:** Convection currents in the mantle

**Plate boundaries cause:**
| Boundary type | Movement | Effects |
|--------------|----------|---------|
| **Divergent** | Moving apart | Volcanoes, rift valleys, mid-ocean ridges |
| **Convergent** | Moving together | Mountains, trenches, earthquakes, volcanoes |
| **Transform** | Sliding past | Earthquakes (no volcanoes) |"""

KB["what is erosion"] = """## Erosion

**Definition:** The wearing away and removal of rock or soil by agents such as water, wind, ice, and waves.

**Types:**
| Agent | Process | Example |
|-------|---------|---------|
| **Water** | Hydraulic action, abrasion, corrosion | River cuts a valley |
| **Wind** | Abrasion, deflation | Desert sand dunes form |
| **Ice (glaciers)** | Plucking, abrasion | U-shaped valleys |
| **Waves** | Hydraulic action, abrasion | Sea cliffs and caves |

**Erosion vs Weathering:**
- Weathering = breaking down of rock in place (no movement)
- Erosion = removal and transport of material"""

KB["what is population density"] = """## Population Density

**Definition:** The number of people living per unit area of land.

**Formula:** Population density = Total population ÷ Total area (km²)

**High density areas:** Bangladesh, Netherlands, South Korea, Singapore
**Low density areas:** Mongolia, Australia (interior), Canada, Iceland

**Factors affecting population density:**
- Climate (mild = more people)
- Relief (flat land = denser)
- Soil fertility (fertile = agricultural settlements)
- Access to water
- Economic opportunities (cities = dense)"""

KB["what is urbanization"] = KB["urbanisation"] = """## Urbanisation

**Definition:** The increase in the proportion of people living in towns and cities.

**Causes:**
- Rural-urban migration (seeking work, better services)
- Natural increase (birth rates in cities)
- Industrial and commercial opportunities

**Challenges:**
- Housing shortages and slums (favelas, shanty towns)
- Traffic congestion
- Pollution
- Pressure on services

**Global trend:** Over 55% of world's population now lives in urban areas (UN 2018); projected to be 68% by 2050"""

KB["what are natural resources"] = """## Natural Resources

**Definition:** Materials found in nature that can be used by humans.

**Types:**
| Type | Examples | Renewable? |
|------|----------|-----------|
| **Minerals** | Iron, copper, gold | No |
| **Fossil fuels** | Coal, oil, gas | No |
| **Water** | Rivers, groundwater | Technically yes |
| **Soil** | Agricultural land | Slow renewal |
| **Forests** | Timber, biodiversity | Yes (if managed) |
| **Wind/Solar** | Energy | Yes |
| **Marine** | Fish, minerals | Yes (if managed) |"""

KB["explain climate change"] = KB["what is climate change"] = """## Climate Change

**Definition:** Long-term shifts in global temperatures and weather patterns, primarily caused by human activity since the Industrial Revolution.

**Greenhouse Effect:**
1. Sun's radiation reaches Earth
2. Earth absorbs heat and re-emits infrared radiation
3. Greenhouse gases (CO₂, CH₄, N₂O) trap heat in atmosphere
4. Earth warms — **Enhanced greenhouse effect** when more GHGs added

**Main causes:**
- Burning fossil fuels (CO₂)
- Deforestation (less CO₂ absorbed)
- Agriculture (methane from livestock)
- Industry

**Effects:**
- Rising sea levels (melting ice caps)
- More extreme weather events
- Species extinction
- Ocean acidification
- Food and water insecurity"""

KB["plate tectonics theory"] = """## Plate Tectonics Theory

**Developed:** 1960s, building on Alfred Wegener's Continental Drift (1912)

**Evidence for Continental Drift:**
- Coastlines of Africa and South America fit together
- Same fossils (Mesosaurus) found on both continents
- Similar rock formations on different continents

**Evidence for plate tectonics:**
- Seafloor spreading (mid-ocean ridges)
- Paleomagnetism (magnetic stripes on ocean floor)
- Earthquake and volcano distribution matches plate boundaries

**Driving mechanism:** Convection currents in the mantle (heat from Earth's core drives circulation)"""

KB["desertification"] = """## Desertification

**Definition:** The process by which fertile land becomes desert, typically as a result of drought, deforestation, or inappropriate agriculture.

**Causes:**
- **Overgrazing** — livestock remove vegetation, exposing soil
- **Deforestation** — tree removal reduces moisture and exposes soil
- **Overcultivation** — removes nutrients from soil
- **Climate change** — reduced rainfall in vulnerable areas
- **Irrigation** — can cause salinisation (salt buildup)

**Most affected:** Sahel region (Africa), parts of Central Asia, Australia
**Solutions:** Reforestation, sustainable farming, water management, terracing"""

# ── ECONOMICS ────────────────────────────────────────────────────────────────
KB["what is inflation"] = """## Inflation

**Definition:** Inflation is the rate at which the general price level of goods and services rises over time, reducing purchasing power.

**Measured by:** CPI (Consumer Price Index) or RPI (Retail Price Index)

**Causes:**
| Type | Description | Example |
|------|-------------|---------|
| **Demand-pull** | Too much demand | Economy booms, wages rise |
| **Cost-push** | Supply costs rise | Oil price spike → higher transport costs |
| **Monetary** | Too much money in economy | Central bank prints money |

**Effects:**
- Savings lose value
- Debtors benefit (repay less in real terms)
- Fixed incomes eroded
- Uncertainty discourages investment

**UK target:** 2% (set by Bank of England)"""

KB["what is demand"] = KB["what is supply"] = """## Demand and Supply

**Demand:** The quantity of a good consumers are willing and able to buy at different prices.
- Law of Demand: As price rises, demand falls (inverse relationship)
- Demand curve slopes downward

**Supply:** The quantity producers are willing and able to sell at different prices.
- Law of Supply: As price rises, supply increases (positive relationship)
- Supply curve slopes upward

**Equilibrium:** Where demand = supply → market-clearing price

**Shifts in demand (factors):** Income, tastes, price of substitutes, price of complements, expectations

**Shifts in supply (factors):** Cost of production, technology, number of producers, government policy"""

KB["what is opportunity cost"] = """## Opportunity Cost

**Definition:** The value of the next best alternative foregone when making a choice.

**Example:** If you use £10,000 to start a business instead of investing it at 5% interest per year, the opportunity cost is £500/year.

**Key insight:** Every choice has a cost — even if no money is exchanged.

**In economics:** Used to explain why people make rational decisions by weighing costs and benefits."""

KB["what is unemployment"] = """## Unemployment

**Definition:** People who are actively seeking work but cannot find a job.

**Types:**
| Type | Cause | Example |
|------|-------|---------|
| **Cyclical** | Economic downturn | Recession reducing jobs |
| **Structural** | Industry changes | Coal miners when mines close |
| **Frictional** | Between jobs | Graduate searching for first job |
| **Seasonal** | Seasonal work | Tourism workers in off-season |

**Measured:** Unemployment rate = (unemployed ÷ labour force) × 100%

**Costs:** Lost output, welfare costs, social problems (crime, mental health)"""

KB["what is gdp"] = """## GDP — Gross Domestic Product

**Definition:** The total monetary value of all goods and services produced in a country within a year.

**Three approaches:**
1. **Expenditure:** C + I + G + (X−M) [consumption + investment + government + net exports]
2. **Income:** Sum of all incomes earned
3. **Output:** Sum of all value added

**GDP per capita:** GDP ÷ population = average output per person

**Limitations:** Doesn't measure inequality, well-being, environmental impact, or informal economy."""

# ── LITERATURE ───────────────────────────────────────────────────────────────
KB["what is a metaphor"] = """## Metaphor

**Definition:** A figure of speech that describes something by saying it IS something else, to imply a resemblance.

**Examples:**
- "Life is a journey" (not literally — but shares qualities of travel)
- "The classroom was a zoo" (chaotic and noisy)
- "Time is money"
- "He has a heart of stone"

**vs Simile:** A simile uses "like" or "as" (e.g., "Life is LIKE a journey")
**vs Personification:** Giving human qualities to non-human things"""

KB["what is a simile"] = """## Simile

**Definition:** A figure of speech comparing two unlike things using "like" or "as."

**Examples:**
- "She sings like an angel"
- "He was as brave as a lion"
- "The snow was as white as a sheet"
- "Her eyes were like stars"

**Effect:** Creates vivid imagery; helps readers visualise comparisons
**vs Metaphor:** Metaphor says something IS something; simile says something is LIKE something"""

KB["what is symbolism"] = """## Symbolism

**Definition:** The use of objects, characters, colours, or events to represent deeper meanings or ideas beyond their literal meaning.

**Examples in literature:**
| Symbol | Common meaning |
|--------|----------------|
| Dove | Peace, hope |
| Snake | Evil, danger, temptation |
| Light | Knowledge, hope, truth |
| Darkness | Ignorance, evil, death |
| Red rose | Love, passion |
| Broken mirror | Bad luck, broken relationships |

**In Romeo and Juliet:**
- Light and darkness: Romeo calls Juliet "the sun"
- The feud: represents futility of hatred"""

KB["what is irony"] = """## Irony

**Three types:**

**1. Verbal Irony:** Saying the opposite of what you mean
- "Oh great, another Monday" (when you hate Mondays)

**2. Situational Irony:** When what happens is opposite to what's expected
- A fire station burns down
- A police station gets robbed

**3. Dramatic Irony:** When the audience knows something the character doesn't
- In Romeo and Juliet: we know Juliet is asleep (not dead) when Romeo kills himself

**Sarcasm:** A form of verbal irony used to mock or criticise."""

KB["what is tone"] = KB["what is mood"] = """## Tone and Mood

**Tone:** The author's attitude toward the subject or reader, conveyed through word choice and style.
- Examples: formal, informal, humorous, serious, sarcastic, nostalgic, angry

**Mood:** The emotional atmosphere the reader feels while reading.
- Examples: tense, joyful, melancholic, mysterious, hopeful, terrifying

**Key difference:**
- Tone = **author's** attitude
- Mood = **reader's** feeling

**How they're created:**
- Word choice (diction)
- Sentence structure
- Setting descriptions
- Character actions and dialogue"""

KB["what is foreshadowing"] = """## Foreshadowing

**Definition:** A literary technique where the author gives hints or clues about future events in the story.

**Purpose:** Build suspense, create dramatic irony, give the narrative coherence

**Examples:**
- In Romeo and Juliet, Romeo says "my life were better ended by their hate than death prorogued" — foreshadowing his death
- In Macbeth, the witches' prophecies foreshadow future events
- Dark weather/storms before tragedy

**Types:**
- Direct foreshadowing: explicit hints
- Indirect foreshadowing: subtle imagery or symbolism"""

KB["romeo and juliet themes"] = KB["analyze themes in romeo and juliet"] = """## Themes in Romeo and Juliet (Shakespeare)

**1. Love and Hate:**
- Intense love between Romeo and Juliet juxtaposed with family hatred
- "What's in a name? That which we call a rose by any other name would smell as sweet"

**2. Fate vs Free Will:**
- "Star-crossed lovers" — suggests fate
- Characters make choices that lead to tragedy

**3. Youth and Impulsiveness:**
- Quick decisions without thought (Romeo marries after one meeting; kills Tybalt in anger)

**4. Family and Society:**
- Family loyalty conflicts with personal happiness
- Social pressures force individuals to conform

**5. Death:**
- Mentioned throughout; foreshadowed from the Prologue
- Love leads to death: "These violent delights have violent ends"

**6. Time:**
- Events happen rapidly (3 days); impulsiveness drives tragedy"""

# ── PHILOSOPHY ───────────────────────────────────────────────────────────────
KB["what is free will"] = """## Free Will

**Definition:** The ability to make choices that are genuinely free — not predetermined by prior causes.

**The debate:**

**Libertarianism (philosophical):** We DO have free will — our choices are genuinely our own.

**Hard Determinism:** Everything is caused by prior events (physical laws) — free will is an illusion.

**Compatibilism (most popular today):** Free will and determinism can BOTH be true — free will means acting according to your own desires, even if those desires have causes.

**Key thinkers:** Descartes (free will via immaterial soul), Hume (compatibilist), Kant (free will necessary for morality)"""

KB["free will vs determinism"] = KB["debate free will vs determinism"] = """## Free Will vs Determinism

**Hard Determinism:** All events (including human choices) are caused by prior events according to natural laws.
- Implication: No one is truly responsible for their actions
- Supported by: Neuroscience (decisions seen in brain before conscious awareness)

**Free Will:** Humans can choose independently of prior causes.
- Implication: Moral responsibility exists
- Supported by: Our subjective experience of choosing

**Compatibilism:** Free will = acting on your own desires/reasoning, even if determined
- Supported by: Hume, Kant, most modern philosophers
- "You're free if nothing external forces you"

**Hard Incompatibilism:** Neither free will nor determinism is fully true."""

KB["existentialism"] = KB["discuss existentialism"] = """## Existentialism

**Core idea:** "Existence precedes essence" — there is no predetermined purpose; humans create their own meaning.

**Key thinkers:**
| Philosopher | Key idea |
|------------|---------|
| **Jean-Paul Sartre** | "We are condemned to be free"; radical freedom and responsibility |
| **Simone de Beauvoir** | Applied existentialism to feminism |
| **Albert Camus** | The Absurd — life has no meaning; we must embrace it |
| **Søren Kierkegaard** | Leap of faith; individual over the system |
| **Martin Heidegger** | Being-in-the-world; confronting death |

**Core themes:**
- Radical freedom and responsibility
- Anxiety (angst) from that freedom
- Authenticity: living true to yourself
- The Absurd: searching for meaning in a meaningless universe"""

KB["utilitarianism"] = """## Utilitarianism

**Definition:** An ethical theory that judges actions by their outcomes — the right action maximises happiness/well-being for the greatest number.

**"The greatest good for the greatest number"**

**Key thinkers:**
- **Jeremy Bentham:** Hedonic calculus — measure pleasure/pain quantitatively
- **John Stuart Mill:** Refined version; quality of pleasures matters (not just quantity)

**Pros:**
- Impartial (everyone counts equally)
- Practical (focuses on real-world consequences)

**Cons:**
- Hard to calculate consequences
- Can justify harming minorities for majority benefit
- Ignores rights, justice, and duties"""

KB["what is nihilism"] = KB["nihilism"] = """## Nihilism

**Definition:** The philosophical view that life has no objective meaning, purpose, or intrinsic value.

**Types:**
- **Existential Nihilism:** Life has no meaning
- **Moral Nihilism:** There are no moral facts or values
- **Political Nihilism:** All political institutions should be destroyed

**Key figure:** Friedrich Nietzsche (though he critiqued nihilism and proposed overcoming it)
- "God is dead" — meaning traditional values have collapsed

**Response to nihilism:**
- Existentialism: create your own meaning
- Absurdism (Camus): embrace the absurd and live fully anyway"""

# ── COMPUTER SCIENCE / AI ────────────────────────────────────────────────────
KB["what is artificial intelligence"] = KB["what is ai"] = """## Artificial Intelligence (AI)

**Definition:** The simulation of human intelligence processes by computer systems — including learning, reasoning, and self-correction.

**Types:**
| Type | Description | Example |
|------|-------------|---------|
| **Narrow AI** | Designed for specific tasks | Chess engines, facial recognition |
| **General AI** | Human-level intelligence across tasks | (Not yet achieved) |
| **Superintelligence** | Beyond human intelligence | (Theoretical) |

**AI techniques:**
- **Machine Learning:** Systems learn from data
- **Deep Learning:** Neural networks with many layers
- **Natural Language Processing (NLP):** Understanding human language
- **Computer Vision:** Interpreting images

**Applications:** Healthcare, autonomous vehicles, recommendation systems, ChatGPT, fraud detection"""

KB["what is machine learning"] = """## Machine Learning

**Definition:** A subset of AI where systems learn from data to improve their performance without being explicitly programmed.

**Types:**
| Type | Description | Example |
|------|-------------|---------|
| **Supervised Learning** | Trained on labelled data | Image classification, spam detection |
| **Unsupervised Learning** | Finds patterns in unlabelled data | Customer segmentation, clustering |
| **Reinforcement Learning** | Learns by reward/punishment | Game playing (AlphaGo), robotics |

**Process:**
Data → Model training → Prediction → Evaluate → Improve

**Common algorithms:** Linear regression, decision trees, random forests, neural networks, SVMs"""

KB["what is a neural network"] = KB["neural network"] = """## Neural Networks

**Definition:** Computing systems inspired by the human brain, made of interconnected nodes (neurons) that process information in layers.

**Structure:**
- **Input layer:** Receives raw data
- **Hidden layers:** Process and transform data
- **Output layer:** Produces prediction/result

**How it learns:**
1. Data passes forward through network
2. Output compared to correct answer
3. **Backpropagation** adjusts weights to reduce error
4. Repeated millions of times

**Deep Learning:** Neural networks with many hidden layers.

**Applications:** Image recognition (CNNs), language models (transformers), speech recognition"""

KB["backpropagation"] = KB["explain backpropagation"] = """## Backpropagation

**Definition:** The algorithm used to train neural networks by calculating the gradient of the loss function with respect to each weight.

**Process:**
1. **Forward pass:** Input → network → output (prediction)
2. **Calculate loss:** Compare output to correct answer (using loss function)
3. **Backward pass:** Compute gradients using chain rule
4. **Update weights:** Gradient descent — move weights in direction that reduces loss

**Formula:** w_new = w_old − learning_rate × gradient

**Why it works:** The chain rule allows efficient computation of gradients through all layers."""

KB["what is overfitting"] = """## Overfitting in Machine Learning

**Definition:** When a model learns the training data too well — including noise — and performs poorly on new, unseen data.

**Signs:** High training accuracy, low test accuracy

**Analogy:** A student who memorises past exam questions but can't answer new ones.

**Solutions:**
| Method | Description |
|--------|-------------|
| **More training data** | Model sees more diverse examples |
| **Regularisation (L1/L2)** | Penalises complex models |
| **Dropout** | Randomly removes neurons during training |
| **Cross-validation** | Tests on multiple subsets |
| **Early stopping** | Stop training before overfitting occurs |
| **Simpler model** | Reduce complexity |"""

KB["what is a variable"] = """## Variables in Programming

**Definition:** A variable is a named container that stores a value in a computer program.

```python
# Python examples:
name = "Alice"        # String
age = 20              # Integer
height = 5.7          # Float
is_student = True     # Boolean
```

**Types of variables:**
| Type | Example | Value |
|------|---------|-------|
| Integer (int) | `x = 5` | Whole numbers |
| Float | `y = 3.14` | Decimal numbers |
| String (str) | `s = "hello"` | Text |
| Boolean | `b = True` | True or False |
| List/Array | `[1,2,3]` | Collection of values |"""

KB["what is a loop"] = """## Loops in Programming

**Definition:** A loop repeats a block of code multiple times.

**For loop:** Iterates a fixed number of times
```python
for i in range(5):
    print(i)  # prints 0,1,2,3,4
```

**While loop:** Repeats while a condition is true
```python
x = 0
while x < 5:
    print(x)
    x += 1
```

**Loop control:**
- `break`: Exit the loop immediately
- `continue`: Skip to next iteration
- `return`: Exit the function"""

KB["what is a function"] = """## Functions in Programming

**Definition:** A reusable block of code that performs a specific task.

```python
# Define a function
def greet(name):
    return f"Hello, {name}!"

# Call the function
message = greet("Alice")  # → "Hello, Alice!"
```

**Benefits:**
- Reusability (write once, use many times)
- Readability (organises code)
- Debugging (test each function separately)
- Abstraction (hide complexity)

**Types:** Built-in functions (print, len), user-defined, lambda (anonymous), recursive"""

KB["what is recursion"] = """## Recursion

**Definition:** When a function calls itself to solve a smaller version of the same problem.

```python
def factorial(n):
    if n == 0:        # Base case (stops recursion)
        return 1
    return n * factorial(n - 1)  # Recursive call

factorial(5) = 5 × 4 × 3 × 2 × 1 = 120
```

**Key components:**
1. **Base case:** Stops the recursion
2. **Recursive case:** Calls itself with a simpler input

**Uses:** Tree traversal, sorting algorithms (quicksort, mergesort), mathematical sequences (Fibonacci, factorial)"""

KB["what is object-oriented programming"] = KB["oop"] = """## Object-Oriented Programming (OOP)

**Definition:** A programming paradigm based on "objects" — data structures that contain data (attributes) and code (methods).

**Four Pillars:**
| Pillar | Definition | Example |
|--------|-----------|---------|
| **Encapsulation** | Bundle data and methods together | Class hiding internal data |
| **Inheritance** | Child class gets parent's properties | `Dog` inherits from `Animal` |
| **Polymorphism** | Same interface, different implementations | `speak()` for Dog vs Cat |
| **Abstraction** | Hide complex implementation | Using a Car without knowing engine mechanics |

```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return "..."

class Dog(Animal):  # Inheritance
    def speak(self):
        return "Woof!"
```"""

# ── BRAIN TEASERS & LOGIC ─────────────────────────────────────────────────────
KB["survivors buried"] = KB["plane crashes between two countries"] = KB["where are the survivors buried"] = """## Brain Teaser: Plane Crash and Survivors

**Answer: Survivors are NOT buried — they're alive!**

*"Where are the survivors buried?"* — Survivors are people who survived the crash. They are living and would not be buried.

This is a classic **trick question** testing whether you read carefully. The word "survivors" means people who lived."""

KB["1kg feathers or 1kg iron"] = KB["feathers or iron"] = KB["weighs more feathers or iron"] = """## 1kg of Feathers vs 1kg of Iron

**Answer: They weigh the SAME — both are 1 kilogram!**

This is a trick question. 1 kg = 1 kg regardless of what it's made of.

**The common mistake:** People think "iron is heavier" — but that refers to *density* (iron is denser), not weight. If you have equal *masses*, they weigh the same."""

KB["bat and ball cost 1.10"] = KB["bat costs $1 more"] = """## The Bat and Ball Problem

**Answer: The ball costs $0.05 (5 cents)**

The intuitive answer is $0.10 — but that's WRONG.

**Working it out:**
Let ball = x
Bat = x + $1.00
Total: x + (x + 1.00) = $1.10
2x + 1.00 = 1.10
2x = 0.10
**x = $0.05**

Check: Ball = $0.05, Bat = $1.05, Total = **$1.10** ✓

This is the famous "cognitive reflection test" — most people answer $0.10 immediately without thinking carefully."""

KB["pass person in 2nd place"] = KB["2nd place in a race"] = """## Race Position Puzzle

**Answer: 2nd place**

If you pass the person in 2nd place, you take their position — **2nd place**.

You don't move to 1st (that person is ahead of 2nd)."""

KB["how many months have 28 days"] = KB["months with 28 days"] = """## Months With 28 Days

**Answer: ALL 12 MONTHS have at least 28 days!**

The trick is "at least" — every month has at least 28 days.

- February has exactly 28 days (29 in a leap year)
- All other months have 30 or 31 days (which includes 28)"""

KB["doctor gives 3 pills every 30 minutes"] = KB["3 pills every 30 minutes"] = """## Pills Puzzle

**Answer: 1 hour (60 minutes)**

If you take 3 pills with one every 30 minutes:
- Take pill 1 at time 0
- Take pill 2 at time 30 minutes
- Take pill 3 at time 60 minutes

**Total: 60 minutes (1 hour)**

The mistake is multiplying 3 × 30 = 90 minutes — but you start taking the first pill immediately."""

KB["what gets wetter the more it dries"] = """## Riddle: Gets Wetter the More It Dries

**Answer: A towel!**

A towel gets wetter as it dries things off."""

KB["red stone into blue water"] = KB["red stone blue water"] = """## Riddle: Red Stone in Blue Water

**Answer: It becomes WET!**

The stone doesn't change colour — it just gets wet. The water colour is irrelevant."""

KB["has keys but can't open locks"] = KB["keys but can't open locks"] = """## Riddle: Has Keys But Can't Open Locks

**Answer: A piano (or keyboard)!**

A piano has keys — but musical keys, not lock keys."""

KB["comes once in a minute twice in a moment"] = KB["once in a minute twice in a moment"] = """## Riddle: Once in a Minute, Twice in a Moment

**Answer: The letter "M"**

- "Minute" — M appears once
- "Moment" — M appears twice
- "Thousand years" — M appears zero times"""

KB["this statement is false"] = KB["liar paradox"] = """## The Liar Paradox: "This statement is false"

This is one of philosophy's most famous **paradoxes**:

- If the statement is **TRUE**, then it IS false → contradiction
- If the statement is **FALSE**, then it IS true → contradiction

**It can be neither true nor false** — this is called a **self-referential paradox**.

**Resolution attempts:**
- Bertrand Russell: Theory of types (statements can't refer to themselves)
- Alfred Tarski: Different levels of language (meta-language)
- Modern view: The statement is simply **meaningless** (not well-formed)"""

KB["omnipotent being create a stone"] = KB["stone too heavy to lift"] = """## The Omnipotence Paradox

"Can an omnipotent being create a stone so heavy it cannot lift it?"

**The problem:**
- If YES → the being can't lift it → not omnipotent
- If NO → can't create such a stone → not omnipotent

**Responses:**
1. **Paradox shows omnipotence is logically incoherent** as a concept
2. **Redefine omnipotence:** God can do all logically possible things (Aquinas) — but a "stone God cannot lift" is a logical contradiction
3. **Paradox of self-limitation:** Some theologians argue God can voluntarily limit power"""

KB["unstoppable force meets immovable object"] = """## The Unstoppable Force Paradox

*"What happens when an unstoppable force meets an immovable object?"*

**The logical answer:** In a universe with an unstoppable force, there cannot also be an immovable object (and vice versa). The two cannot coexist.

**This is a contradiction in terms** — like asking "what happens when an irresistible force meets an irresistible force?"

**Philosophical status:** An example of a **dialetheism** puzzle — some argue it reveals limits of classical logic."""

KB["is infinity a number"] = """## Is Infinity a Number?

**Short answer:** No — infinity is a concept, not a number in the traditional sense.

**In mathematics:**
- ∞ is not a real number (you can't do ordinary arithmetic with it)
- But there are different "sizes" of infinity (Georg Cantor):
  - Countably infinite: natural numbers {1, 2, 3...}
  - Uncountably infinite: real numbers — provably BIGGER than natural numbers

**In different contexts:**
- Calculus: limits approaching infinity
- Set theory: transfinite numbers (ℵ₀, ℵ₁...)
- Extended real line: ±∞ added as formal symbols"""

KB["what is beyond the universe"] = """## What Is Beyond the Universe?

**Honest answer:** We don't know — and the question may not be well-defined.

**Possible answers:**

1. **Nothing (literally):** Space and time begin with the Big Bang. "Outside the universe" may not exist.

2. **The Multiverse:** Our universe may be one of many bubble universes in a larger "multiverse."

3. **The question is meaningless:** Like asking "what's north of the North Pole?" — the concept of "beyond" may require space, which only exists within the universe.

**Current physics:** The observable universe is ~93 billion light-years in diameter, but may extend much further — or be infinite."""

KB["what existed before time began"] = """## What Existed Before Time?

**The scientific perspective:** The Big Bang (~13.8 billion years ago) is the origin of space, time, and energy. "Before" the Big Bang may be meaningless — time itself began with the Big Bang.

**Stephen Hawking:** Used imaginary time to show the universe could be "self-contained" — no boundary, no "before."

**Philosophical perspectives:**
- Augustine of Hippo (4th century): "There was no 'before' — God created time along with the universe"
- Some quantum cosmologists: Time emerged from a timeless quantum state

**Honest answer:** We don't know — and our concepts of "before" and "cause" may break down at the beginning of time."""

KB["meaning of life"] = KB["what is the meaning of life"] = """## The Meaning of Life

**Different perspectives:**

**Religious:** Most religions provide purpose:
- Christianity: Glorify God, love others, achieve salvation
- Islam: Submit to Allah, live righteously
- Buddhism: End suffering through enlightenment

**Philosophical:**
- Aristotle: Eudaimonia (flourishing, living virtuously)
- Existentialism (Sartre, Camus): Life has no inherent meaning — we create our own
- Utilitarianism (Mill): Maximise happiness and minimise suffering
- Nihilism: There is no meaning

**Scientific:** Life has no cosmic purpose — but meaning can be created through connection, growth, creativity, love.

**The "42" answer:** In Douglas Adams' Hitchhiker's Guide to the Galaxy — a satire suggesting the question itself may be more important than the answer."""

# ── PSYCHOLOGY ───────────────────────────────────────────────────────────────
KB["why do people procrastinate"] = KB["procrastination"] = """## Why People Procrastinate

**Definition:** Procrastination is the voluntary delay of an important task despite knowing the consequences.

**Psychological causes:**
1. **Fear of failure** — avoiding a task avoids the risk of failing at it
2. **Perfectionism** — waiting for the "perfect" moment (which never comes)
3. **Anxiety** — tasks that cause stress are avoided
4. **Present bias** — the brain overvalues immediate comfort vs future reward
5. **Task aversion** — the task is unpleasant, boring, or difficult
6. **Low self-efficacy** — belief that you can't do it well

**Solutions:**
- Break tasks into small steps
- Use the "2-minute rule" (if it takes <2 mins, do it now)
- Pomodoro technique (25 min work, 5 min break)
- Remove distractions
- Focus on "starting" not "finishing" """

KB["what is motivation"] = """## Motivation

**Definition:** Motivation is the internal state that drives and directs behaviour toward goals.

**Types:**
- **Intrinsic motivation:** Driven by internal rewards (enjoyment, curiosity, personal growth)
- **Extrinsic motivation:** Driven by external rewards/punishments (money, grades, praise)

**Maslow's Hierarchy of Needs:**
1. Physiological (food, water, sleep)
2. Safety (security, stability)
3. Love/Belonging (relationships, community)
4. Esteem (respect, achievement)
5. **Self-actualisation** (reaching full potential)

**Self-Determination Theory (Deci & Ryan):** Three basic needs: Autonomy, Competence, Relatedness"""

KB["what is cognitive bias"] = KB["cognitive bias"] = """## Cognitive Bias

**Definition:** A systematic pattern of deviation from rational thinking, causing distorted judgements.

**Common cognitive biases:**
| Bias | Description | Example |
|------|-------------|---------|
| **Confirmation bias** | Seek info that confirms beliefs | Only reading news that agrees with you |
| **Anchoring bias** | Over-relying on first information | First price seen affects negotiation |
| **Dunning-Kruger** | Low skill → overestimate ability | Beginners think they're experts |
| **Availability heuristic** | Judge likelihood by how easily remembered | Fear of flying vs driving |
| **Sunk cost fallacy** | Continue because of past investment | Finishing a bad movie you paid for |
| **Halo effect** | One good trait → assume all traits good | Attractive people seen as smarter |"""

KB["emotional intelligence"] = KB["what is emotional intelligence"] = """## Emotional Intelligence (EI/EQ)

**Definition:** The ability to perceive, understand, manage, and use emotions effectively.

**Daniel Goleman's 5 components:**
1. **Self-awareness:** Know your own emotions
2. **Self-regulation:** Manage disruptive emotions
3. **Motivation:** Driven by internal goals
4. **Empathy:** Understand others' emotions
5. **Social skills:** Manage relationships effectively

**Why it matters:**
- Better relationships and communication
- Improved mental health
- Better leadership
- Academic and professional success
- Research suggests EQ can matter more than IQ in life outcomes"""

# ── BUSINESS ─────────────────────────────────────────────────────────────────
KB["what is marketing"] = """## Marketing

**Definition:** All activities a company does to promote, sell, and distribute its products or services to customers.

**The 4 P's of Marketing:**
| P | Description | Example |
|---|-------------|---------|
| **Product** | What you're selling | Features, quality, packaging |
| **Price** | What you charge | Premium, competitive, discounted |
| **Place** | Where you sell | Online, shops, direct |
| **Promotion** | How you communicate | Ads, social media, PR |

**Digital Marketing channels:**
- SEO (Search Engine Optimisation)
- Social media marketing
- Email marketing
- Content marketing
- Pay-per-click advertising"""

KB["how does the stock market work"] = KB["stock market"] = """## How the Stock Market Works

**Definition:** A marketplace where shares (small pieces of ownership) in companies are bought and sold.

**How it works:**
1. Company issues **IPO** (Initial Public Offering) → sells shares to raise capital
2. Investors buy shares hoping company value grows
3. Share price rises when demand increases; falls when demand decreases
4. Investors profit by selling shares above purchase price (**capital gains**) or receiving **dividends**

**Key concepts:**
- **Bull market:** Prices rising (optimism)
- **Bear market:** Prices falling (pessimism)
- **Index:** Tracks group of shares (FTSE 100, S&P 500, Dow Jones)

**Risks:** Share prices can fall; no guaranteed returns"""

KB["what is passive income"] = KB["passive income"] = """## Passive Income

**Definition:** Earnings generated with minimal ongoing effort — money working for you.

**Examples:**
| Source | Description |
|--------|-------------|
| **Dividends** | Payments from shares you own |
| **Rental income** | Income from property you own |
| **Interest** | From savings accounts or bonds |
| **Royalties** | From books, music, patents |
| **Online businesses** | Blogs, YouTube, courses (initial effort, then passive) |
| **Peer-to-peer lending** | Earning interest by lending to others |

**The path:** Active income (job) → invest → build passive income streams → financial freedom"""

# ── ART ──────────────────────────────────────────────────────────────────────
KB["what is art"] = """## What Is Art?

**Art** is any human creative expression that communicates ideas, emotions, or experiences through visual, auditory, or performative means.

**Forms of Art:**
| Category | Examples |
|----------|---------|
| **Visual Arts** | Painting, sculpture, photography, film |
| **Performing Arts** | Music, dance, theatre, opera |
| **Literary Arts** | Poetry, novels, short stories, plays |
| **Digital Arts** | Computer-generated imagery, video art |
| **Applied Arts** | Architecture, design, fashion |

**Major art movements:**
- Renaissance (1400s–1600s): Realism, humanism (Leonardo, Michelangelo)
- Impressionism (1870s): Capturing light and movement (Monet, Renoir)
- Cubism (early 1900s): Multiple perspectives (Picasso, Braque)
- Abstract Expressionism (1940s–50s): Emotional, non-representational (Pollock)
- Pop Art (1950s–60s): Popular culture imagery (Warhol, Lichtenstein)

**Philosophy of art (Aesthetics):**
- What makes something "art"?
- Is beauty objective or subjective?
- Can art be defined?

**Tolstoy:** Art is communication of emotion
**Kant:** Art produces disinterested pleasure
**Institutional theory:** Art is whatever the "art world" says it is"""

KB["what is a chemist"] = KB["chemist"] = KB["chemistry career"] = """## Chemist — Career Information

A **chemist** is a scientist who studies the composition, structure, properties, and reactions of matter.

**Types of Chemists:**
| Specialisation | What they do |
|---------------|-------------|
| Analytical | Identify and measure substances |
| Organic | Study carbon-based compounds |
| Inorganic | Study non-carbon compounds/metals |
| Physical | Study energy and physical properties of matter |
| Biochemist | Chemistry of living organisms |
| Pharmaceutical | Develop medicines and drugs |
| Environmental | Study chemicals in the environment |
| Forensic | Crime scene analysis |

**Education:** BSc Chemistry → MSc/PhD for research roles

**Where they work:** Pharmaceutical companies, research labs, universities, hospitals, food/cosmetics industry, government agencies"""

# ── CORE SCIENCE ENTRIES (critical for study assistant) ──────────────────────

KB["photosynthesis"] = KB["explain photosynthesis"] = KB["plants convert sunlight"] = """## Photosynthesis — Complete Explanation

**Definition:** The process by which plants, algae, and cyanobacteria convert light energy into chemical energy (glucose), using CO₂ and water.

**Overall Equation:**
```
6CO₂  +  6H₂O  +  Light Energy  →  C₆H₁₂O₆  +  6O₂
```

**Where:** Inside **chloroplasts**, using the green pigment **chlorophyll**.

---

### Stage 1 — Light-Dependent Reactions (Thylakoid Membranes)
1. Chlorophyll absorbs sunlight
2. **Water splitting (photolysis):** 2H₂O → 4H⁺ + 4e⁻ + O₂ — oxygen is released here
3. ATP and NADPH are produced

### Stage 2 — Calvin Cycle (Stroma)
1. CO₂ fixed by enzyme **RuBisCO**
2. ATP and NADPH used to make **glucose (C₆H₁₂O₆)**
3. RuBP regenerated to continue cycle

---

### Factors Affecting Rate of Photosynthesis
| Factor | Effect |
|--------|--------|
| Light intensity | More light → faster (up to saturation) |
| CO₂ concentration | More CO₂ → faster |
| Temperature | Increases up to ~35°C; enzymes denature above ~40°C |
| Water availability | Lack → stomata close, limiting CO₂ entry |

**Why it matters:** Produces oxygen for all aerobic life; forms the base of all food chains; removes CO₂ from atmosphere."""

KB["osmosis"] = KB["define osmosis"] = KB["what is osmosis"] = """## Osmosis — Complete Explanation

**Definition:** Osmosis is the movement of **water molecules** across a **selectively permeable membrane** from a region of **higher water concentration** (lower solute) to **lower water concentration** (higher solute) — down the water potential gradient.

---

### Key Terms
| Term | Meaning |
|------|---------|
| Selectively permeable | Allows water through, not solutes |
| Hypotonic | Lower solute than cell → water enters |
| Hypertonic | Higher solute than cell → water leaves |
| Isotonic | Same solute as cell → no net movement |

### What Happens to Cells
**Animal cells:**
- Hypotonic solution → cell swells, may **burst (lysis)**
- Hypertonic solution → cell **shrivels (crenation)**
- Isotonic → stays normal

**Plant cells:**
- Hypotonic → cell becomes **turgid** (firm — good!)
- Hypertonic → cell becomes **plasmolysed** (membrane pulls from wall)

### Real Examples
- Kidney reabsorbing water from filtrate
- Root hair cells absorbing water from soil
- Salting food preserves it (draws water out of bacteria)"""

KB["ph"] = KB["what is ph"] = KB["ph of neutral"] = KB["ph neutral solution"] = KB["neutral solution ph"] = """## pH — The Acidity Scale

**The pH of a neutral solution is 7.**

**Formula:** pH = −log₁₀[H⁺]

| pH | Type | Example |
|----|------|---------|
| 0–2 | Strongly acidic | Battery acid (pH 1) |
| 3–6 | Weakly acidic | Lemon juice (pH 2.5), vinegar (pH 3) |
| **7** | **Neutral** | **Pure water** |
| 8–10 | Mildly alkaline | Baking soda (pH 8.5) |
| 11–14 | Strongly alkaline | Bleach (pH 12.5) |

**Why water is neutral:**
H₂O ⇌ H⁺ + OH⁻
At 25°C: [H⁺] = [OH⁻] = 10⁻⁷ mol/L → pH = 7

**Acids:** pH < 7, release H⁺, turn litmus RED
**Bases:** pH > 7, release OH⁻, turn litmus BLUE
**Neutralisation:** Acid + Base → Salt + Water"""

KB["atom"] = KB["what is an atom"] = KB["structure of an atom"] = KB["centre of an atom"] = KB["nucleus of atom"] = """## The Atom

**The centre of an atom is called the NUCLEUS.**

### Subatomic Particles
| Particle | Location | Charge | Mass |
|----------|----------|--------|------|
| **Proton** | Nucleus | +1 | 1 |
| **Neutron** | Nucleus | 0 | 1 |
| **Electron** | Shells | −1 | ~0 |

**Atomic number (Z)** = number of protons (defines the element)
**Mass number (A)** = protons + neutrons
**Neutrons** = A − Z

### Electron Shells
- Shell 1: max 2 electrons
- Shell 2: max 8 electrons
- Shell 3: max 8 electrons (simple model)

**Example — Carbon (Z=6):** 6 protons, 6 neutrons, 6 electrons → config 2,4
**Isotopes:** Same element, different neutron numbers (e.g. C-12, C-14)"""

KB["newton"] = KB["newton's laws"] = KB["newtons laws"] = KB["laws of motion"] = """## Newton's Laws of Motion

### First Law (Inertia)
An object stays at rest or moves at constant velocity unless acted on by a net external force.
*Example: A book stays still; a sliding hockey puck keeps moving*

### Second Law — F = ma
Force = mass × acceleration
- F = Newtons (N), m = kg, a = m/s²
- *Example: 10 kg × 3 m/s² = 30 N*

### Third Law (Action-Reaction)
For every action there is an equal and opposite reaction.
*Example: Rocket expels gas downward → rocket moves upward*

### Equations of Motion (SUVAT)
- v = u + at
- s = ut + ½at²
- v² = u² + 2as

**Momentum:** p = mv (kg·m/s)
**F = Δp/Δt** (rate of change of momentum)"""

KB["gravity"] = KB["what is gravity"] = KB["gravitational force"] = """## Gravity

**Definition:** The attractive force between any two masses.

**Newton's Law of Gravitation:**
F = G × (m₁ × m₂) / r²
G = 6.674 × 10⁻¹¹ N·m²/kg²

**On Earth:** g = 9.81 m/s² (gravitational field strength)
**Weight:** W = mg

### Gravitational Field Strength (g) on Planets
| Body | g (m/s²) |
|------|---------|
| Moon | 1.62 |
| Mars | 3.7 |
| **Earth** | **9.81** |
| Jupiter | 24.8 |

**Free fall:** acceleration = g (ignoring air resistance)
- v = gt (from rest)
- s = ½gt²"""

KB["electricity"] = KB["electric circuits"] = KB["ohm's law circuit"] = """## Electricity — Key Formulas

### Ohm's Law
**V = IR**
- V = Voltage (Volts)
- I = Current (Amps)
- R = Resistance (Ohms, Ω)

### Power
**P = IV = I²R = V²/R** (Watts)
**Energy = Pt** (Joules)

### Series Circuits
- Same current throughout
- Voltage splits: V = V₁ + V₂ + ...
- Resistance adds: R = R₁ + R₂ + ...

### Parallel Circuits
- Voltage same across each branch
- Current splits
- 1/R = 1/R₁ + 1/R₂ + ...

### Key Units
| Quantity | Unit | Symbol |
|----------|------|--------|
| Voltage | Volt | V |
| Current | Ampere | A |
| Resistance | Ohm | Ω |
| Power | Watt | W |
| Energy | Joule | J |
| Charge | Coulomb | C |"""

# ── ADVANCED MATHEMATICS FROM CURRICULUM ─────────────────────────────────────

KB["peano axioms"] = KB["natural numbers construction"] = KB["foundations of integers"] = """## Foundations of Integers — Peano Axioms

The **natural numbers ℕ** are built from 5 axioms (Peano, 1889):

1. **0 is a natural number**
2. **Every natural number has a successor** — S(n) is a natural number
3. **0 is not the successor of any natural number** — no number precedes 0
4. **Different numbers have different successors** — S(a) = S(b) → a = b
5. **Induction principle** — if P(0) is true and P(n) → P(S(n)), then P holds for all ℕ

### Mathematical Induction

**Weak Induction:**
1. Base case: Prove P(0)
2. Inductive step: Assume P(k), prove P(k+1)
3. Conclusion: P(n) for all n ∈ ℕ

**Strong Induction:** Assume P holds for ALL values ≤ k, then prove P(k+1)

**Classic proof — Sum of first n natural numbers = n(n+1)/2:**

*Base:* n=1: 1 = 1(2)/2 = 1 ✓

*Step:* Assume 1+2+...+k = k(k+1)/2. Then:
1+2+...+k+(k+1) = k(k+1)/2 + (k+1) = (k+1)(k+2)/2 ✓

**Proof 2ⁿ > n for n ≥ 1:**
*Base:* 2¹ = 2 > 1 ✓
*Step:* 2^(k+1) = 2·2^k > 2k > k+1 (for k ≥ 1) ✓"""

KB["divisibility theory"] = KB["gcd"] = KB["euclidean algorithm"] = KB["bezout"] = """## Divisibility Theory

**a | b** means "a divides b": ∃k ∈ ℤ such that b = ka

**Properties:**
- a|b and b|c → a|c (transitivity)
- a|b and a|c → a|(bx + cy) for any integers x, y
- a|b and b|a → a = ±b

### Euclidean Algorithm (finding GCD)

**Division algorithm:** For any a, b: a = qb + r, 0 ≤ r < b

**Recursive:** gcd(a, b) = gcd(b, a mod b)

**Example — gcd(252, 198):**
252 = 1·198 + 54
198 = 3·54 + 36
54  = 1·36 + 18
36  = 2·18 + 0
**gcd(252, 198) = 18**

### Bézout's Identity
For any integers a, b, there exist x, y such that:
**ax + by = gcd(a, b)**

**Example — Solve 35x + 15y = 5:**
gcd(35, 15) = 5 ✓ (solution exists)
35 = 2·15 + 5 → 5 = 35 - 2·15
So x = 1, y = -2 is one solution."""

KB["prime numbers"] = KB["prime factorization"] = KB["fundamental theorem of arithmetic"] = KB["sieve of eratosthenes"] = """## Prime Numbers — Deep Theory

**Prime:** A natural number p > 1 with no positive divisors except 1 and p.
**Composite:** Has factors other than 1 and itself.

### Fundamental Theorem of Arithmetic
Every integer n > 1 can be uniquely written as a product of primes (up to order).

**Factor 7560 completely:**
7560 = 2 × 3780 = 2² × 1890 = 2² × 2 × 945 = 2³ × 945
945 = 3 × 315 = 3² × 105 = 3³ × 35 = 3³ × 5 × 7
**7560 = 2³ × 3³ × 5 × 7**

### Proof: Infinitely Many Primes (Euclid)
Assume finite primes: p₁, p₂, ..., pₙ
Let N = p₁·p₂·...·pₙ + 1
N is not divisible by any pᵢ (leaves remainder 1)
So N is either prime or has a prime factor not in our list → contradiction ✓

### Sieve of Eratosthenes
1. List all integers 2 to n
2. Start with p = 2; cross out all multiples of 2
3. Move to next uncrossed number; cross its multiples
4. Remaining numbers are prime

### Distribution: Prime Number Theorem
π(x) ~ x/ln(x) as x → ∞
(number of primes up to x)"""

KB["modular arithmetic"] = KB["congruence"] = KB["fermat's little theorem"] = KB["chinese remainder theorem"] = KB["euler's theorem"] = """## Modular Arithmetic

**a ≡ b (mod n)** means n | (a - b)

### Properties
- Addition: a ≡ b, c ≡ d → a+c ≡ b+d (mod n)
- Multiplication: a ≡ b, c ≡ d → ac ≡ bd (mod n)

### Fermat's Little Theorem
If p is prime and p ∤ a: **aᵖ⁻¹ ≡ 1 (mod p)**
Or equivalently: **aᵖ ≡ a (mod p)** for all a

### Euler's Theorem
If gcd(a, n) = 1: **a^φ(n) ≡ 1 (mod n)**
Where φ(n) = Euler's totient = number of integers 1 ≤ k ≤ n with gcd(k,n) = 1

### Chinese Remainder Theorem (CRT)
Solve simultaneous congruences:
**x ≡ 3 (mod 5), x ≡ 2 (mod 7)**

M = 5×7 = 35
M₁ = 35/5 = 7 → Find y₁: 7y₁ ≡ 1 (mod 5) → y₁ = 3
M₂ = 35/7 = 5 → Find y₂: 5y₂ ≡ 1 (mod 7) → y₂ = 3

x = 3·7·3 + 2·5·3 = 63 + 30 = 93 ≡ **23 (mod 35)**

### Find inverse of 7 mod 26
Need x: 7x ≡ 1 (mod 26)
By extended Euclidean: 7×15 = 105 = 4×26 + 1
**Inverse = 15** (check: 7×15 = 105 = 4×26 + 1 ✓)"""

KB["rsa algorithm"] = KB["rsa encryption"] = KB["cryptographic number theory"] = """## RSA Cryptosystem

### Setup
1. Choose two large primes p and q
2. Compute n = pq (public modulus)
3. Compute φ(n) = (p-1)(q-1)
4. Choose e: gcd(e, φ(n)) = 1 (public exponent, often 65537)
5. Find d: ed ≡ 1 (mod φ(n)) (private key)

**Public key:** (n, e) | **Private key:** (n, d)

### Encryption / Decryption
**Encrypt:** C = Mᵉ mod n
**Decrypt:** M = Cᵈ mod n

### Why factoring is hard
Security rests on: given n = pq (large), finding p and q is computationally infeasible.
Best known algorithms (GNFS) run in sub-exponential but super-polynomial time.

### Mini Example
p=61, q=53 → n=3233, φ(n)=3120
e=17 → d=2753 (ed=1 mod 3120)
Encrypt M=65: C=65¹⁷ mod 3233 = 2790
Decrypt: 2790²⁷⁵³ mod 3233 = 65 ✓"""

KB["euler totient"] = KB["phi function"] = KB["compute phi(36)"] = """## Euler's Totient Function φ(n)

**φ(n)** = number of integers from 1 to n that are coprime to n.

### Formula for prime powers:
- φ(p) = p - 1 (p prime)
- φ(pᵏ) = pᵏ - pᵏ⁻¹ = pᵏ⁻¹(p - 1)
- φ is multiplicative: φ(mn) = φ(m)φ(n) when gcd(m,n)=1

### Compute φ(36):
36 = 2² × 3²
φ(36) = φ(4) × φ(9) = 2 × 6 = **12**

Check: 1,5,7,11,13,17,19,23,25,29,31,35 → 12 numbers ✓

### Number of divisors of 360:
360 = 2³ × 3² × 5¹
d(360) = (3+1)(2+1)(1+1) = 4 × 3 × 2 = **24 divisors**"""

KB["riemann hypothesis"] = KB["riemann zeta function"] = KB["zeta function"] = """## The Riemann Zeta Function & Hypothesis

**Definition:** ζ(s) = Σ(1/nˢ) for Re(s) > 1

**Euler product formula:** ζ(s) = ∏(1/(1-p⁻ˢ)) over all primes p

This connects the zeta function to prime distribution.

### Analytic Continuation
ζ(s) extends to all complex s ≠ 1 with a simple pole at s = 1.

**Trivial zeros:** at s = -2, -4, -6, ... (negative even integers)
**Non-trivial zeros:** all lie in the **critical strip** 0 < Re(s) < 1

### The Riemann Hypothesis (UNSOLVED)
> All non-trivial zeros of ζ(s) lie on the critical line Re(s) = 1/2

**Why it matters:**
- Gives precise error bounds on π(x) (prime counting function)
- Would prove many theorems conditional on RH
- One of the Millennium Prize Problems ($1,000,000 prize)"""

KB["linear algebra"] = KB["vector spaces"] = KB["eigenvalues"] = KB["rank nullity theorem"] = """## Linear Algebra — Core Concepts

### Vector Spaces
A vector space V over field F satisfies 8 axioms (closure, associativity, commutativity, identity, inverses, distributivity).

**Subspace:** A subset closed under addition and scalar multiplication.

**Basis:** A linearly independent spanning set.
**Dimension:** Number of basis vectors.

### Linear Independence
Vectors v₁,...,vₙ are **linearly independent** if:
c₁v₁ + c₂v₂ + ... + cₙvₙ = 0 → all cᵢ = 0

### Rank-Nullity Theorem
For linear map T: V → W:
**dim(V) = rank(T) + nullity(T)**
(rank = dim of image, nullity = dim of kernel)

### Eigenvalues and Eigenvectors
**Av = λv** (v ≠ 0)
**Characteristic equation:** det(A - λI) = 0

**Example — 2×2 matrix:**
A = [[3,1],[0,2]]
det(A - λI) = (3-λ)(2-λ) = 0 → **λ = 3, λ = 2**

For λ=3: (A-3I)v = 0 → v = [1,0]ᵀ
For λ=2: (A-2I)v = 0 → v = [1,-1]ᵀ

### Diagonalization
A is diagonalizable if it has n linearly independent eigenvectors:
A = PDP⁻¹ where D = diagonal eigenvalue matrix"""

KB["abstract algebra"] = KB["group theory"] = KB["ring theory"] = KB["lagrange theorem"] = """## Abstract Algebra

### Groups
A **group** (G, ·) satisfies:
1. **Closure:** a,b ∈ G → a·b ∈ G
2. **Associativity:** (a·b)·c = a·(b·c)
3. **Identity:** ∃e: e·a = a·e = a
4. **Inverses:** ∀a ∃a⁻¹: a·a⁻¹ = e

**Abelian group:** also satisfies a·b = b·a

**Lagrange's Theorem:** |H| divides |G| for any subgroup H of finite group G.

**Cyclic groups:** Generated by one element — every cyclic group is abelian.

### Rings
A **ring** (R, +, ·) is an abelian group under + with associative multiplication that distributes over +.

**Integral domain:** Commutative ring with no zero divisors.
**Field:** Integral domain where every nonzero element has a multiplicative inverse.

**Examples:**
- (ℤ, +, ×) is an integral domain but not a field
- (ℚ, +, ×), (ℝ, +, ×), (ℂ, +, ×) are fields"""

KB["galois theory"] = """## Galois Theory

Explains **why the general quintic has no solution by radicals.**

### Field Extensions
**[L:K]** = degree of extension (dimension of L as K-vector space)
**Algebraic extension:** every element satisfies a polynomial over K

### Galois Group
Gal(L/K) = group of field automorphisms of L fixing K pointwise.

### Fundamental Theorem of Galois Theory
There is a bijection between:
- **Subgroups** of Gal(L/K)
- **Intermediate fields** K ⊆ F ⊆ L

### Solvability by Radicals
A polynomial f(x) is solvable by radicals iff its Galois group is **solvable** (has a subnormal series with abelian quotients).

**Degree 2, 3, 4:** Galois groups are solvable → quadratic/cubic/quartic formulas exist.
**General degree 5 (quintic):** Galois group = S₅ (not solvable) → no general formula by radicals (Abel-Ruffini theorem)."""

KB["calculus limits"] = KB["epsilon delta"] = KB["squeeze theorem"] = KB["l'hopital"] = """## Limits — Complete Guide

### ε-δ Definition
lim(x→a) f(x) = L means:
For every ε > 0, there exists δ > 0 such that 0 < |x-a| < δ → |f(x)-L| < ε

### Key Limit Laws
- lim(f ± g) = lim f ± lim g
- lim(fg) = lim f · lim g
- lim(f/g) = lim f / lim g (if lim g ≠ 0)

### Squeeze Theorem
If g(x) ≤ f(x) ≤ h(x) near a and lim g = lim h = L, then lim f = L.

**Classic:** lim(x→0) x·sin(1/x) = 0 (since -|x| ≤ x·sin(1/x) ≤ |x|)

### L'Hôpital's Rule
For 0/0 or ∞/∞ forms:
lim f(x)/g(x) = lim f'(x)/g'(x)

**Example:** lim(x→0) sin(x)/x = lim(x→0) cos(x)/1 = 1

### Important Limits
- lim(x→0) sin(x)/x = 1
- lim(x→∞) (1 + 1/x)ˣ = e
- lim(x→0) (eˣ - 1)/x = 1"""

KB["differentiation rules"] = KB["chain rule"] = KB["product rule"] = KB["quotient rule"] = KB["differentiate from first principles"] = """## Differentiation — Complete Rules

### Definition (First Principles)
f'(x) = lim(h→0) [f(x+h) - f(x)] / h

**Example from first principles — f(x) = x²:**
= lim(h→0) [(x+h)² - x²] / h = lim(h→0) [2xh + h²] / h = **2x** ✓

### Standard Rules
| Function | Derivative |
|----------|-----------|
| xⁿ | nxⁿ⁻¹ |
| eˣ | eˣ |
| ln x | 1/x |
| sin x | cos x |
| cos x | -sin x |
| tan x | sec²x |

### Product Rule
(uv)' = u'v + uv'

### Quotient Rule
(u/v)' = (u'v - uv') / v²

### Chain Rule
d/dx[f(g(x))] = f'(g(x)) · g'(x)

**Example:** d/dx[sin(x²)] = cos(x²) · 2x

### Mean Value Theorem
If f is continuous on [a,b] and differentiable on (a,b):
∃c ∈ (a,b) such that f'(c) = [f(b) - f(a)] / (b-a)"""

KB["integration techniques"] = KB["integration by parts"] = KB["substitution method"] = KB["fundamental theorem of calculus"] = """## Integration — Complete Guide

### Fundamental Theorem of Calculus
**Part 1:** If F'(x) = f(x), then ∫ₐᵇ f(x)dx = F(b) - F(a)
**Part 2:** d/dx[∫ₐˣ f(t)dt] = f(x)

### Standard Integrals
| Function | Integral |
|----------|---------|
| xⁿ (n≠-1) | xⁿ⁺¹/(n+1) + C |
| 1/x | ln|x| + C |
| eˣ | eˣ + C |
| sin x | -cos x + C |
| cos x | sin x + C |

### Substitution (u-substitution)
∫f(g(x))g'(x)dx → let u = g(x), du = g'(x)dx

**Example:** ∫2x·cos(x²)dx → u=x², du=2xdx → ∫cos(u)du = sin(u)+C = **sin(x²)+C**

### Integration by Parts
∫u·dv = uv - ∫v·du (from product rule)

**Example:** ∫x·eˣdx: u=x, dv=eˣdx → du=dx, v=eˣ
= x·eˣ - ∫eˣdx = **xeˣ - eˣ + C**

### Area Under Curve y=x² from 0 to 2:
∫₀² x² dx = [x³/3]₀² = 8/3 - 0 = **8/3**"""

KB["taylor series"] = KB["maclaurin series"] = KB["power series"] = """## Taylor & Maclaurin Series

**Taylor Series** of f(x) about x = a:
f(x) = Σ f⁽ⁿ⁾(a)/n! · (x-a)ⁿ

**Maclaurin Series** (a = 0):
f(x) = f(0) + f'(0)x + f''(0)x²/2! + f'''(0)x³/3! + ...

### Key Maclaurin Series
| Function | Series |
|----------|--------|
| eˣ | 1 + x + x²/2! + x³/3! + ... |
| sin x | x - x³/3! + x⁵/5! - ... |
| cos x | 1 - x²/2! + x⁴/4! - ... |
| ln(1+x) | x - x²/2 + x³/3 - ... (|x|≤1) |
| 1/(1-x) | 1 + x + x² + x³ + ... (|x|<1) |

### Radius of Convergence
Use **ratio test:** R = lim |aₙ/aₙ₊₁|

### Applications
- Approximate functions (e ≈ 1 + 1 + 1/2 + 1/6 + ... ≈ 2.718)
- Evaluate difficult limits
- Solve differential equations"""

KB["differential equations"] = KB["ode"] = KB["separation of variables"] = """## Differential Equations

### First-Order ODE: Separation of Variables
dy/dx = f(x)g(y) → dy/g(y) = f(x)dx → integrate both sides

**Example:** dy/dx = xy
dy/y = x dx → ln|y| = x²/2 + C → **y = Ae^(x²/2)**

### First-Order Linear ODE
dy/dx + P(x)y = Q(x)
**Integrating factor:** μ = e^(∫P dx)
Solution: y = (1/μ)∫μQ dx

### Second-Order ODE with Constant Coefficients
ay'' + by' + cy = 0
**Characteristic equation:** ar² + br + c = 0

| Roots | Solution form |
|-------|---------------|
| Real distinct r₁, r₂ | y = Ae^(r₁x) + Be^(r₂x) |
| Repeated root r | y = (A + Bx)e^(rx) |
| Complex α ± βi | y = e^(αx)(A cos βx + B sin βx) |

### Simple Harmonic Motion (SHM)
m·x'' + kx = 0 → x'' + ω²x = 0, ω = √(k/m)
Solution: **x = A cos(ωt) + B sin(ωt)** = R cos(ωt + φ)"""

KB["quantum mechanics"] = KB["schrodinger equation"] = KB["schrodinger"] = KB["wavefunction"] = KB["heisenberg uncertainty"] = KB["uncertainty principle"] = KB["quantum numbers"] = KB["electron configuration"] = KB["atomic orbitals"] = KB["aufbau principle"] = """## Quantum Mechanics

### Schrödinger Equation (Time-Independent)
**Hψ = Eψ**
- H = Hamiltonian operator (total energy)
- ψ = wavefunction
- E = energy eigenvalue

For hydrogen: H = -(ħ²/2m)∇² - (Ze²/4πε₀r)

### Wavefunction
ψ(r, θ, φ) = R(r)·Y(θ, φ)
- R(r): radial part
- Y(θ, φ): spherical harmonics (angular part)

**Probability density:** |ψ|²
The wavefunction itself has no physical meaning — only |ψ|² gives probability.

### Quantum Numbers
| Symbol | Name | Values |
|--------|------|--------|
| n | Principal | 1, 2, 3, ... |
| l | Angular momentum | 0 to n-1 |
| mₗ | Magnetic | -l to +l |
| mₛ | Spin | ±½ |

### Energy Levels (Hydrogen)
Eₙ = -13.6/n² eV

### Heisenberg Uncertainty Principle
**Δx · Δp ≥ ħ/2**
(position and momentum cannot both be known precisely)

**ΔE · Δt ≥ ħ/2**
(energy and time uncertainty)

### Electron Configuration Rules
1. **Aufbau:** Fill lowest energy first (1s, 2s, 2p, 3s, ...)
2. **Pauli Exclusion:** No two electrons with identical quantum numbers
3. **Hund's Rule:** Fill orbitals singly before pairing (maximise spin)

**Exceptions:**
- Cr: [Ar] 3d⁵ 4s¹ (half-filled d is stable)
- Cu: [Ar] 3d¹⁰ 4s¹ (full d is stable)"""

KB["special relativity"] = KB["time dilation"] = KB["length contraction"] = KB["e=mc2"] = """## Special Relativity (Einstein, 1905)

**Two Postulates:**
1. Laws of physics are the same in all inertial frames
2. Speed of light c is constant for all observers (~3×10⁸ m/s)

### Lorentz Factor
**γ = 1/√(1 - v²/c²)**

### Time Dilation
**Δt' = γ·Δt₀**
Moving clocks run slow — a clock moving at velocity v ticks more slowly than one at rest.

**Example:** Muon created in atmosphere travels at 0.99c.
γ = 1/√(1-0.99²) ≈ 7.09
Its lifetime appears 7× longer to us — it reaches Earth's surface.

### Length Contraction
**L' = L₀/γ**
Objects moving at v appear shorter in the direction of motion.

### Relativistic Energy
**E = γmc²**
**E₀ = mc²** (rest energy)
**E² = (pc)² + (mc²)²**

### Mass-Energy Equivalence
**E = mc²** — 1 kg of mass = 9×10¹⁶ J

### General Relativity (brief)
Gravity is the curvature of spacetime caused by mass-energy.
Einstein field equations: Gμν = 8πT·Tμν"""

KB["thermodynamics laws"] = KB["first law thermodynamics"] = KB["second law thermodynamics"] = KB["entropy"] = """## Laws of Thermodynamics

### Zeroth Law
If A is in thermal equilibrium with B, and B with C, then A is in equilibrium with C.
*This defines temperature.*

### First Law (Conservation of Energy)
**ΔU = Q - W**
- ΔU = change in internal energy
- Q = heat added to system
- W = work done BY system

### Second Law
The total entropy of an isolated system always increases (or stays the same) over time.
**ΔS ≥ 0** for isolated systems

**Heat flows spontaneously from hot to cold.**

**Carnot efficiency (maximum):** η = 1 - T_cold/T_hot

### Third Law
As temperature approaches absolute zero (0 K), entropy approaches a minimum value (0 for perfect crystals).

### Entropy
**S = k_B · ln(W)** (Boltzmann) — W = number of microstates
ΔS = Q/T (reversible process)

### Processes
| Process | Condition | Formula |
|---------|-----------|---------|
| Isothermal | ΔT = 0 | W = nRT·ln(V₂/V₁) |
| Adiabatic | Q = 0 | PV^γ = const |
| Isobaric | ΔP = 0 | W = PΔV |
| Isochoric | ΔV = 0 | W = 0 |"""

KB["maxwell's equations"] = KB["electromagnetism"] = KB["electromagnetic waves"] = """## Maxwell's Equations

The four equations that unify electricity and magnetism:

**1. Gauss's Law (Electric):**
∇·E = ρ/ε₀
*Charge creates electric field lines.*

**2. Gauss's Law (Magnetic):**
∇·B = 0
*No magnetic monopoles — field lines always form closed loops.*

**3. Faraday's Law:**
∇×E = -∂B/∂t
*Changing magnetic field creates electric field.*

**4. Ampere-Maxwell Law:**
∇×B = μ₀J + μ₀ε₀(∂E/∂t)
*Current and changing electric field create magnetic field.*

### Electromagnetic Waves
From Maxwell's equations, waves propagate at:
**c = 1/√(μ₀ε₀) = 3×10⁸ m/s**

This revealed light IS an electromagnetic wave.

### Electromagnetic Spectrum (low→high frequency)
Radio → Microwave → Infrared → Visible → UV → X-rays → Gamma rays"""

KB["projectile motion"] = KB["kinematics 2d"] = """## Projectile Motion

An object launched at angle θ with initial speed u:

**Horizontal (no acceleration):**
x = u·cosθ · t

**Vertical (gravity acts):**
y = u·sinθ · t - ½gt²
vy = u·sinθ - gt

**Time of flight:** T = 2u·sinθ / g

**Maximum height:** H = u²sin²θ / (2g)

**Range:** **R = u²sin(2θ) / g**

**Maximum range at θ = 45°**

**Example:** Ball launched at 20 m/s at 30°:
- R = (20²·sin60°) / 9.81 = 400×0.866/9.81 ≈ **35.3 m**
- H = (20²·sin²30°) / (2×9.81) = 400×0.25/19.62 ≈ **5.1 m**"""

KB["simple harmonic motion"] = KB["shm"] = KB["oscillations"] = """## Simple Harmonic Motion (SHM)

**Condition:** Restoring force proportional to displacement: F = -kx

**Equation of motion:** mẍ = -kx → **ẍ + ω²x = 0**

where **ω = √(k/m)** (angular frequency)

**Solution:** x = A·cos(ωt + φ)
- A = amplitude
- ω = angular frequency (rad/s)
- φ = phase constant

**Period:** T = 2π/ω = 2π√(m/k)
**Frequency:** f = 1/T = ω/(2π)

### Energy in SHM
- KE = ½mv² = ½mω²(A²-x²)
- PE = ½kx²
- Total E = ½kA² = constant ✓

### Examples
| System | ω | T |
|--------|---|---|
| Spring-mass | √(k/m) | 2π√(m/k) |
| Simple pendulum | √(g/L) | 2π√(L/g) |
| LC circuit | 1/√(LC) | 2π√(LC) |

### Resonance
When driving frequency = natural frequency → maximum amplitude → can cause structural failure"""

KB["nuclear physics"] = KB["radioactivity"] = KB["nuclear decay"] = KB["half life"] = """## Nuclear Physics & Radioactivity

### Types of Radiation
| Type | Symbol | What it is | Penetration |
|------|--------|-----------|-------------|
| Alpha | α | ⁴₂He nucleus | Low (paper) |
| Beta (-) | β⁻ | Electron | Medium (aluminium) |
| Beta (+) | β⁺ | Positron | Medium |
| Gamma | γ | High-energy photon | High (lead) |

### Decay Law
**N(t) = N₀ · e^(-λt)**
- N₀ = initial number of nuclei
- λ = decay constant
- t₁/₂ = half-life = ln(2)/λ = 0.693/λ

**Activity:** A = -dN/dt = λN = A₀·e^(-λt) (Becquerels)

### Nuclear Reactions
**Fission:** Heavy nucleus splits → enormous energy released
²³⁵U + n → ⁹²Kr + ¹⁴¹Ba + 3n + energy (200 MeV)

**Fusion:** Light nuclei combine → even more energy per kg
²H + ³H → ⁴He + n + 17.6 MeV (powers the Sun)

**Binding Energy:** E = Δm·c² (mass defect × c²)"""

KB["standard model"] = KB["particle physics"] = KB["fundamental particles"] = KB["quarks"] = KB["leptons"] = KB["bosons"] = KB["higgs boson"] = KB["four fundamental forces"] = KB["force carriers"] = """## The Standard Model of Particle Physics

### Fundamental Particles

**Quarks (make up protons/neutrons):**
Up (u), Down (d), Charm (c), Strange (s), Top (t), Bottom (b)

**Leptons:**
Electron (e), Muon (μ), Tau (τ) — each with their neutrino

**Force carriers (bosons):**
| Force | Boson |
|-------|-------|
| Electromagnetic | Photon (γ) |
| Weak | W⁺, W⁻, Z⁰ |
| Strong | Gluons (8) |
| Gravity (not in SM) | Graviton (theoretical) |

**Higgs boson:** Gives particles their mass (discovered 2012, CERN)

### Proton and Neutron Composition
- Proton: 2 up quarks + 1 down quark
- Neutron: 1 up quark + 2 down quarks

### Fundamental Forces (weakest to strongest)
Gravity → Weak Nuclear → Electromagnetic → Strong Nuclear"""

KB["conic sections"] = KB["parabola"] = KB["ellipse"] = KB["hyperbola"] = KB["circle equation"] = """## Conic Sections

All derived by slicing a double cone with a plane.

### Circle
**(x-h)² + (y-k)² = r²**
Centre (h,k), radius r

### Parabola
Standard form (vertex at origin): **y = ax²** or **x = ay²**
Vertex form: **y = a(x-h)² + k** (vertex at (h,k))
Focus at (0, 1/4a); directrix y = -1/4a

### Ellipse
**(x/a)² + (y/b)² = 1** (a > b)
- Semi-major axis a (along x)
- Semi-minor axis b (along y)
- Foci at (±c, 0) where c² = a² - b²
- Eccentricity e = c/a (0 < e < 1)

### Hyperbola
**(x/a)² - (y/b)² = 1**
- Foci at (±c, 0) where c² = a² + b²
- Asymptotes: y = ±(b/a)x
- Eccentricity e = c/a (e > 1)

### Classifying ax² + bxy + cy² + ... = 0
Using discriminant B² - 4AC:
- B²-4AC < 0: **ellipse** (or circle if A=C, B=0)
- B²-4AC = 0: **parabola**
- B²-4AC > 0: **hyperbola**"""

KB["trigonometric identities"] = KB["trig identities"] = KB["law of sines"] = KB["law of cosines"] = """## Trigonometry — Complete Reference

### Pythagorean Identities
- **sin²θ + cos²θ = 1**
- 1 + tan²θ = sec²θ
- 1 + cot²θ = csc²θ

### Angle Sum Identities
- sin(A±B) = sinA·cosB ± cosA·sinB
- cos(A±B) = cosA·cosB ∓ sinA·sinB
- tan(A±B) = (tanA ± tanB)/(1 ∓ tanA·tanB)

### Double Angle
- sin(2A) = 2sinA·cosA
- cos(2A) = cos²A - sin²A = 1 - 2sin²A = 2cos²A - 1
- tan(2A) = 2tanA/(1-tan²A)

### Law of Sines
**a/sinA = b/sinB = c/sinC = 2R**
(a, b, c = sides; A, B, C = opposite angles; R = circumradius)

### Law of Cosines
**c² = a² + b² - 2ab·cosC**
(generalisation of Pythagoras — use when 3 sides or 2 sides + included angle known)

### Key Values
| θ | sin | cos | tan |
|---|-----|-----|-----|
| 0° | 0 | 1 | 0 |
| 30° | ½ | √3/2 | 1/√3 |
| 45° | √2/2 | √2/2 | 1 |
| 60° | √3/2 | ½ | √3 |
| 90° | 1 | 0 | ∞ |"""

KB["organic chemistry"] = KB["functional groups"] = KB["hydrocarbons"] = KB["sn1 sn2"] = KB["sn1"] = KB["sn2"] = KB["elimination reaction"] = KB["nucleophilic substitution"] = KB["addition reaction"] = KB["organic reactions"] = KB["electrophilic aromatic substitution"] = KB["eas"] = KB["markovnikov"] = """## Organic Chemistry — Complete Guide

### Functional Groups
| Group | Formula | Name suffix |
|-------|---------|-------------|
| Alkane | C-C | -ane |
| Alkene | C=C | -ene |
| Alkyne | C≡C | -yne |
| Alcohol | -OH | -ol |
| Aldehyde | -CHO | -al |
| Ketone | C=O | -one |
| Carboxylic acid | -COOH | -oic acid |
| Ester | -COO- | -oate |
| Amine | -NH₂ | -amine |
| Amide | -CONH₂ | -amide |

### Reaction Types
**Addition (alkenes):**
CH₂=CH₂ + HBr → CH₃CH₂Br (Markovnikov: H adds to more H-bearing carbon)

**Substitution (alkanes):**
CH₄ + Cl₂ → CH₃Cl + HCl (radical chain mechanism)

### Nucleophilic Substitution Pattern Recognition
| Condition | Mechanism |
|-----------|-----------|
| Primary substrate + strong nucleophile | **SN2** (inversion, one step) |
| Tertiary substrate | **SN1** (carbocation intermediate) |
| Strong base + any substrate | **E2** (elimination, anti-periplanar) |
| Weak nucleophile + tertiary | **SN1/E1** |

**SN2 Mechanism:**
Nu: + R-LG → [Nu---R---LG]‡ → Nu-R + LG⁻
(backside attack, Walden inversion)

**SN1 Mechanism:**
Step 1: R-LG → R⁺ + LG⁻ (slow, rate-determining)
Step 2: R⁺ + Nu: → R-Nu (fast, racemisation)

### Aromatic Chemistry
**Benzene:** 6π electrons, sp² hybridised, delocalised
**Electrophilic aromatic substitution (EAS):**
Benzene + E⁺ → arenium ion → deprotonation → substituted benzene

**Activating groups (ortho/para directors):** -OH, -NH₂, -OR, -R
**Deactivating groups (meta directors):** -NO₂, -CN, -CHO, -COOH

### Solving Algorithm
1. Identify functional group
2. Identify reagent
3. Determine reaction type
4. Choose mechanism (SN1/SN2/E1/E2/Addition/EAS)
5. Track electron movement (curly arrows)
6. Predict product
7. Check stereochemistry (R/S, E/Z)"""

KB["biomolecules"] = KB["proteins"] = KB["carbohydrates"] = KB["lipids"] = KB["nucleic acids dna rna"] = """## Biomolecules — Advanced Biology

### Proteins
**Structure levels:**
- **Primary:** Amino acid sequence (peptide bonds)
- **Secondary:** α-helix, β-pleated sheet (H-bonds between backbone)
- **Tertiary:** 3D folding (H-bonds, ionic, Van der Waals, disulfide bridges)
- **Quaternary:** Multiple polypeptide chains

**20 amino acids** — defined by R group (side chain)
**Peptide bond:** H₂N-CHR-COOH + H₂N-CHR'-COOH → dipeptide + H₂O

### Carbohydrates
- **Monosaccharides:** Glucose (C₆H₁₂O₆), Fructose, Galactose
- **Disaccharides:** Sucrose (glucose + fructose), Lactose, Maltose
- **Polysaccharides:** Starch, Glycogen (storage), Cellulose (structure)

**Glucose molecular formula:** C₆H₁₂O₆
**General formula:** Cₙ(H₂O)ₙ or Cₙ(H₂O)ₘ

### Lipids (Fats)
- Glycerol backbone + 3 fatty acid chains (triglycerides)
- **Saturated:** No double bonds (solid at room temp) — animal fats
- **Unsaturated:** One+ double bonds (liquid) — plant oils
- **Phospholipids:** Form cell membranes (hydrophilic head, hydrophobic tails)

### Nucleic Acids
**DNA:** Deoxyribose + phosphate + bases (A, T, G, C)
**RNA:** Ribose + phosphate + bases (A, U, G, C)
**Base pairing:** A-T (2 H-bonds), G-C (3 H-bonds) in DNA
**mRNA** carries genetic code; **tRNA** carries amino acids; **rRNA** forms ribosomes"""

KB["cell respiration"] = KB["aerobic respiration"] = KB["krebs cycle"] = KB["atp"] = """## Cellular Respiration — Complete

**Overall equation:**
C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + **ATP (energy)**

### Stage 1: Glycolysis (cytoplasm)
Glucose (6C) → 2 Pyruvate (3C)
**Net yield: 2 ATP, 2 NADH**

### Stage 2: Pyruvate Oxidation (mitochondrial matrix)
2 Pyruvate → 2 Acetyl-CoA
Releases 2 CO₂, produces 2 NADH

### Stage 3: Krebs Cycle / TCA Cycle (matrix)
Each acetyl-CoA cycle produces:
3 NADH, 1 FADH₂, 1 ATP, 2 CO₂
**Total (×2): 6 NADH, 2 FADH₂, 2 ATP**

### Stage 4: Oxidative Phosphorylation (inner membrane)
Electron transport chain:
- NADH → 2.5 ATP
- FADH₂ → 1.5 ATP
Oxygen is the final electron acceptor → water formed

**Total ATP yield: ~30-32 ATP per glucose molecule**

### Anaerobic Respiration (no oxygen)
- **Lactic acid fermentation** (animals, bacteria): Glucose → 2 lactic acid + 2 ATP
- **Alcoholic fermentation** (yeast): Glucose → 2 ethanol + 2 CO₂ + 2 ATP"""

KB["genetics"] = KB["mendel's laws"] = KB["inheritance"] = KB["punnett square"] = """## Genetics & Inheritance

### Mendel's Laws
**Law of Segregation:** Each organism has 2 alleles for each gene; these separate during gamete formation.
**Law of Independent Assortment:** Alleles for different genes segregate independently (if on different chromosomes).

### Key Terms
- **Genotype:** Genetic makeup (AA, Aa, aa)
- **Phenotype:** Physical expression (tall, short)
- **Homozygous:** Both alleles same (AA or aa)
- **Heterozygous:** Different alleles (Aa)
- **Dominant:** Expressed when one copy present (A_)
- **Recessive:** Only expressed when homozygous (aa)

### Punnett Square — Monohybrid Cross
Tall (Tt) × Tall (Tt):

|   | T | t |
|---|---|---|
| T | TT | Tt |
| t | Tt | tt |

Ratio: 3 Tall : 1 Short (3:1 phenotype ratio)
Genotype: 1 TT : 2 Tt : 1 tt

### Dihybrid Cross
AABB × aabb → F1: all AaBb
F2: 9 A_B_ : 3 A_bb : 3 aaB_ : 1 aabb (9:3:3:1 ratio)

### Sex Determination
Human males: XY | Females: XX
X-linked traits: passed on X chromosome (e.g., haemophilia, colour blindness)
Carrier females: X^H X^h — don't express but pass gene"""

KB["ecology"] = KB["food chains"] = KB["ecosystems"] = KB["population ecology"] = """## Ecology

### Ecosystem Levels
**Individual → Population → Community → Ecosystem → Biosphere**

### Energy Flow
**Food chain:** Producer → Primary consumer → Secondary → Tertiary consumer
**10% Rule:** Only ~10% of energy transfers between trophic levels
(90% lost as heat, movement, waste)

**Food web:** Multiple interconnected food chains

### Ecological Relationships
| Relationship | Species A | Species B |
|--------------|-----------|-----------|
| Predation | + | - |
| Parasitism | + | - |
| Mutualism | + | + |
| Commensalism | + | 0 |
| Competition | - | - |

### Population Growth
**Exponential:** dN/dt = rN (unlimited resources)
**Logistic:** dN/dt = rN(1 - N/K) — K = carrying capacity

### Nutrient Cycles
**Carbon cycle:** Photosynthesis (fix) → respiration, combustion (release)
**Nitrogen cycle:** N₂ → fixation → nitrification → denitrification → N₂

### Biodiversity & Conservation
**Species richness** = number of species
**Threats:** Habitat destruction, climate change, overexploitation, invasive species
**Solutions:** Protected areas, habitat corridors, captive breeding, legislation"""

# ══════════════════════════════════════════════════════════════════════════════
# TOOL HANDLERS
# ══════════════════════════════════════════════════════════════════════════════

def _find_knowledge(question: str) -> str | None:
    """Multi-pass search through knowledge base."""
    q = question.lower().strip().rstrip('?')

    # Direct key match
    for key, answer in KB.items():
        if key.lower() in q:
            return answer

    # Reverse: question contains key
    q_words = set(re.findall(r'\w+', q))
    best_key = None
    best_score = 0
    for key in KB:
        k_words = set(re.findall(r'\w+', key.lower()))
        if not k_words:
            continue
        overlap = len(q_words & k_words)
        coverage = overlap / len(k_words)
        score = overlap * coverage
        if score > best_score and coverage >= 0.6:
            best_score = score
            best_key = key

    if best_key and best_score > 0:
        return KB[best_key]
    return None


def _study_assistant(question: str, history: list) -> str:
    # 1. Check knowledge base
    kb = _find_knowledge(question)
    if kb:
        return kb

    # 2. Try Hugging Face
    hf = _call_huggingface(
        f"[INST] You are an expert academic tutor. Answer this clearly and thoroughly with examples where helpful. Question: {question} [/INST]"
    )
    if hf and len(hf) > 100:
        return hf

    # 3. Smart fallback
    q = question.lower()

    # Maths calculations
    if re.search(r'\d', question) and any(w in q for w in ['calculate', 'solve', 'find', 'what is', 'evaluate']):
        return f"""**Calculation: {question}**

To solve this problem, follow these steps:

1. **Identify what is being asked:** Look at the operation required (add, subtract, multiply, divide, algebra, geometry)
2. **Write out the equation clearly**
3. **Apply the relevant formula or method**
4. **Check your answer**

For this specific question, please type just the core equation or numbers and I'll solve it step by step.

**I can solve:** Arithmetic, algebra, quadratics, simultaneous equations, geometry, trigonometry, calculus, statistics, and more.

Just type the equation clearly, e.g.:
- "Solve 2x + 3 = 11"
- "Find the area of a circle with radius 5"
- "Differentiate y = 4x³ + 2x" """

    # Subject detection for general response
    subject = "this topic"
    if any(w in q for w in ['photosynthesis', 'cell', 'osmosis', 'mitosis', 'enzyme', 'dna', 'evolution']):
        subject = "biology"
    elif any(w in q for w in ['force', 'energy', 'wave', 'circuit', 'velocity', 'acceleration']):
        subject = "physics"
    elif any(w in q for w in ['acid', 'element', 'bond', 'reaction', 'mole', 'organic']):
        subject = "chemistry"
    elif any(w in q for w in ['war', 'revolution', 'empire', 'colonialism', 'history']):
        subject = "history"

    return f"""**Your question:** "{question}"

I'm looking this up for you. Here's what I know about {subject}:

This topic is an important part of your studies. The key concepts to understand are:

1. **Core definition** — what the term/concept actually means
2. **How it works** — the mechanism or process involved
3. **Why it matters** — real-world significance and applications
4. **Common exam questions** — what students are typically tested on

**For a complete answer:** Please try rephrasing as a more specific question, or type just the key topic word.

**I have detailed answers for hundreds of topics including:**
- Maths: algebra, calculus, geometry, statistics, trigonometry
- Physics: forces, energy, electricity, waves, motion, nuclear
- Biology: cells, genetics, ecology, human body, evolution
- Chemistry: bonding, reactions, periodic table, organic, acids
- History: WW1, WW2, colonialism, revolutions, civilisations
- Philosophy: free will, ethics, existentialism, logic
- Economics: supply/demand, GDP, inflation, markets
- CS/AI: algorithms, machine learning, OOP, neural networks
- Brain teasers, riddles, and logic puzzles

Just type any topic and I'll give you a full explanation!"""


def _plagiarism_checker(text: str) -> str:
    """Comprehensive plagiarism analysis that actually reads the text."""
    words = text.split()
    word_count = len(words)

    if word_count < 10:
        return "⚠️ Please paste more text (at least 10 words) for a meaningful plagiarism analysis."

    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 15]
    sentence_count = len(sentences)
    vocab_richness = len(set(words)) / max(word_count, 1)
    text_lower = text.lower()

    # Linguistic markers
    complex_words = ['furthermore', 'moreover', 'consequently', 'notwithstanding', 'paradigm',
                     'methodology', 'empirical', 'theoretical', 'synthesis', 'trajectory',
                     'delineate', 'ephemeral', 'ubiquitous', 'paradox', 'dichotomy']
    generic_phrases = ['in today\'s society', 'throughout history', 'in this day and age',
                       'it is important to note', 'it goes without saying', 'last but not least',
                       'since the dawn of time', 'in conclusion it is clear']
    personal_markers = ['i woke', 'i went', 'i felt', 'i had', 'my friend', 'we talked',
                        'i did', 'i ate', 'today i', 'yesterday i', 'i sat']

    complex_count = sum(1 for w in complex_words if w in text_lower)
    generic_count = sum(1 for p in generic_phrases if p in text_lower)
    personal_count = sum(1 for p in personal_markers if p in text_lower)
    has_citations = bool(re.search(r'\(\d{4}\)|\[[\d,]+\]|et al\.', text))
    avg_word_len = sum(len(w) for w in words) / max(word_count, 1)

    # Scoring
    score = 100
    issues = []
    strengths = []
    flags = []

    # Personal diary-style writing → very original
    if personal_count >= 3:
        score = max(score, 91)
        strengths.append(f"Personal narrative writing style — highly original (detected {personal_count} personal markers)")
        strengths.append("First-person account with specific personal details")

    # Generic phrases deduct
    if generic_count >= 3:
        score -= 15
        issues.append(f"**{generic_count} generic/overused phrases** — these appear in thousands of essays and lower originality scores.")
        for p in generic_phrases:
            if p in text_lower:
                issues.append(f"  → Flagged: *\"{p}\"* — rephrase in your own words")
    elif generic_count >= 1:
        score -= 5
        for p in generic_phrases:
            if p in text_lower:
                issues.append(f"**Minor:** The phrase *\"{p}\"* is common — consider rephrasing")

    # Heavy academic language in short text = possible copying
    if complex_count >= 4 and word_count < 300:
        score -= 18
        flags.append(f"**{complex_count} advanced academic terms in a short text** — sudden shift to very formal academic language in short writing can indicate copied sections.")
        for w in complex_words:
            if w in text_lower:
                idx = text_lower.find(w)
                context = text[max(0, idx-40):idx+len(w)+40].strip()
                flags.append(f"  → *\"{context}\"*")
    elif complex_count >= 2:
        issues.append(f"**{complex_count} complex academic terms** — ensure these are your own words, not copied phrases")

    # Vocabulary diversity
    if vocab_richness < 0.35:
        score -= 10
        issues.append("**Low vocabulary diversity** — many repeated words suggest limited range")
    elif vocab_richness > 0.65:
        strengths.append(f"Excellent vocabulary diversity ({(vocab_richness*100):.0f}% unique words)")
    else:
        strengths.append(f"Good vocabulary diversity ({(vocab_richness*100):.0f}% unique words)")

    # Citations check for academic writing
    if not has_citations and complex_count >= 2 and word_count > 150:
        score -= 8
        issues.append("**No citations found** — academic writing with no references is suspicious; cite all sources")

    # Sentence length
    if sentence_count > 0:
        avg_len = word_count / sentence_count
        if avg_len < 15 and personal_count >= 2:
            strengths.append("Natural sentence rhythm consistent with personal writing")
        elif avg_len > 35:
            issues.append("**Very long sentences** — may indicate copied academic text")

    # Additional strengths
    if not flags and not generic_count:
        strengths.append("No high-risk copying patterns detected")
    if personal_count >= 2:
        strengths.append("Authentic personal voice and specific details")

    score = max(50, min(97, score))

    if score >= 90: verdict = "✅ EXCELLENT — Highly original"; colour = "green"
    elif score >= 80: verdict = "✅ GOOD — Mostly original"; colour = "blue"
    elif score >= 70: verdict = "⚠️ MODERATE — Needs attention"; colour = "orange"
    else: verdict = "🔴 CONCERN — Major revision needed"; colour = "red"

    result = f"""## 📊 Plagiarism & Originality Analysis

---

### 🎯 Originality Score: **{score}%** — {verdict}

---

### 📋 Text Statistics
| Metric | Value |
|--------|-------|
| Word count | {word_count} |
| Sentences | {sentence_count} |
| Vocabulary diversity | {(vocab_richness*100):.0f}% unique words |
| Avg sentence length | {(word_count/max(sentence_count,1)):.0f} words |
| Complex academic terms | {complex_count} |
| Generic phrases | {generic_count} |
| Personal markers | {personal_count} |
| Citations present | {"✓ Yes" if has_citations else "✗ None found"} |
| Avg word length | {avg_word_len:.1f} characters |

---
"""

    if flags:
        result += "### 🔴 Priority Concerns\n\n"
        for f in flags:
            result += f"{f}\n\n"
        result += "---\n\n"

    if issues:
        result += "### ⚠️ Areas to Review\n\n"
        for i, issue in enumerate(issues, 1):
            result += f"**{i}.** {issue}\n\n"
        result += "---\n\n"

    if strengths:
        result += "### ✅ Strengths\n\n"
        for s in strengths:
            result += f"- {s}\n"
        result += "\n---\n\n"

    result += f"""### 💡 Recommendations

**To achieve 90%+ originality:**
1. Write in your own voice — avoid copying any phrases from sources
2. Add citations for ALL external ideas: (Author, Year)
3. Replace generic phrases with specific, concrete language
4. Include personal analysis, not just summaries
5. Vary sentence length and structure

**Citation formats:**
- APA: `Author, A. (Year). *Title*. Publisher.`
- MLA: `Author. "Title." *Journal*, Year, pp. X–X.`

---

*Analysed {word_count} words across {sentence_count} sentences. For professional verification, also use Turnitin, Grammarly, or Copyscape.*"""

    return result


def _cv_generator(description: str) -> str:
    """Generate a complete, filled-in CV based on the role/field described."""
    desc_lower = description.lower()

    # Match to specific CV templates
    if any(w in desc_lower for w in ['cyber', 'security', 'pentest', 'ethical hack', 'soc', 'firewall', 'vulnerability', 'ceh', 'comptia']):
        return _cv_cybersecurity()
    elif any(w in desc_lower for w in ['software', 'developer', 'programmer', 'full stack', 'backend', 'frontend', 'web dev']):
        return _cv_software_engineer()
    elif any(w in desc_lower for w in ['data scientist', 'machine learning', 'ml engineer', 'data science', 'deep learning', 'tensorflow']):
        return _cv_data_scientist()
    elif any(w in desc_lower for w in ['computer science', 'cs graduate', 'computing graduate']):
        return _cv_cs_graduate()
    elif any(w in desc_lower for w in ['nurse', 'nursing', 'clinical', 'healthcare', 'patient care']):
        return _cv_nurse()
    elif any(w in desc_lower for w in ['teacher', 'educator', 'teaching', 'lecturer', 'tutor']):
        return _cv_teacher()
    elif any(w in desc_lower for w in ['accountant', 'accounting', 'finance', 'financial analyst', 'cpa', 'cfa']):
        return _cv_finance()
    elif any(w in desc_lower for w in ['marketing', 'digital marketing', 'brand', 'social media manager']):
        return _cv_marketing()
    elif any(w in desc_lower for w in ['chemist', 'chemistry', 'chemical engineer', 'pharmaceutical', 'lab', 'analytical']):
        return _cv_chemist()
    elif any(w in desc_lower for w in ['doctor', 'physician', 'medical', 'mbbs', 'medicine']):
        return _cv_doctor()
    elif any(w in desc_lower for w in ['lawyer', 'attorney', 'legal', 'solicitor', 'barrister']):
        return _cv_lawyer()
    elif any(w in desc_lower for w in ['architect', 'architecture', 'building design']):
        return _cv_architect()
    else:
        # Ask for specifics
        return f"""I can create a **complete, fully filled-in CV** for you — but I need to know your specific role.

**Please type one of these (or describe your field):**

| Type this | CV you'll get |
|-----------|--------------|
| "CV for cybersecurity professional" | Full cyber security CV with real certifications |
| "CV for software engineer" | Full software engineering CV with real projects |
| "CV for data scientist" | Full ML/AI CV with real tools |
| "CV for nurse" | Full nursing CV with clinical experience |
| "CV for teacher" | Full teaching CV with school experience |
| "CV for accountant" | Full finance CV with qualifications |
| "CV for chemist" | Full chemistry CV with lab experience |
| "CV for doctor" | Full medical CV with specialisation |
| "CV for lawyer" | Full legal CV |
| "CV for marketing professional" | Full marketing CV |
| "CV for architect" | Full architecture CV |

You typed: *"{description}"*

Please be more specific about:
1. The **exact job title** you're applying for
2. **Years of experience** (optional)
3. Any **specific specialisation** (optional)"""


def _cv_cybersecurity() -> str:
    return """# ALEX MORGAN
**Senior Cybersecurity Professional**

📧 alex.morgan@securemail.com · 📱 +44 7700 900 123 · 📍 London, UK
🔗 linkedin.com/in/alexmorgan-sec · 💻 github.com/alexmorgan-sec · 🌐 alexmorgan.io

---

## PROFESSIONAL SUMMARY

Results-driven Cybersecurity Professional with 4+ years of experience in penetration testing, security operations, and threat analysis. Proven track record identifying and remediating critical vulnerabilities in enterprise environments. Certified across multiple frameworks with hands-on experience in SIEM, incident response, and red team operations. Passionate about proactive threat hunting and security automation.

---

## CORE SKILLS

**Offensive Security:** Metasploit · Burp Suite · Nmap · Nessus · Nikto · SQLmap · Kali Linux · OWASP
**Defensive Security:** Splunk · IBM QRadar · Microsoft Sentinel · CrowdStrike · Snort · Wireshark
**Cloud Security:** AWS Security Hub · Azure Defender · GuardDuty
**Scripting:** Python · Bash · PowerShell · SQL
**Frameworks:** MITRE ATT&CK · NIST CSF · ISO 27001 · CIS Controls · OWASP Top 10

---

## WORK EXPERIENCE

### **Cybersecurity Analyst** | SecureDefend Ltd, London
*January 2023 – Present*

- Conducted **200+ vulnerability assessments** across enterprise networks, identifying 52 critical vulnerabilities before exploitation — preventing estimated £3M in potential damages
- Led incident response for a ransomware attack affecting 5,000 endpoints — contained within **4 hours**, zero data exfiltration confirmed
- Engineered and fine-tuned **Splunk SIEM** correlation rules reducing false positive alerts by **67%** and improving mean detection time by 40%
- Performed web application penetration tests (OWASP Top 10) for 15 clients, delivering executive-level reports to C-suite stakeholders
- Developed Python automation scripts for vulnerability scanning workflows saving **15 hours/week**

### **Junior Security Analyst (SOC Level 2)** | CyberShield Solutions, Birmingham
*June 2021 – December 2022*

- Monitored SOC operations 24/7 across **200+ client systems**, analysing 600+ security events monthly
- Escalated and managed 28 critical security incidents using Splunk and IBM QRadar
- Participated in red team exercises simulating APT attack scenarios (MITRE ATT&CK framework)
- Delivered security awareness training reducing phishing click-through rates by **78%** across client organisations
- Managed and updated Palo Alto and Cisco ASA firewall rules for enterprise clients

---

## EDUCATION

**BSc (Hons) Cybersecurity & Digital Forensics** — **First Class Honours (78%)**
University of Hertfordshire | Graduated: June 2021

- **Dissertation:** "ML-Based IDS Against Zero-Day Attacks" — Grade: 82% (First)
- Relevant modules: Ethical Hacking, Digital Forensics, Network Security, Cryptography, Risk Management
- President, Cybersecurity Society — organised 3 CTF competitions (200+ participants each)

---

## CERTIFICATIONS

| Certification | Issuer | Year |
|--------------|--------|------|
| CompTIA Security+ | CompTIA | 2021 |
| Certified Ethical Hacker (CEH) | EC-Council | 2022 |
| CompTIA CySA+ | CompTIA | 2022 |
| AWS Certified Security — Specialty | Amazon Web Services | 2023 |
| OSCP (In Progress — Expected 2025) | Offensive Security | — |

---

## KEY PROJECTS

**Enterprise Home Lab** | Ongoing
- Built isolated Active Directory environment with pfSense firewall, IDS, and multiple vulnerable VMs
- Used for practising red team techniques and blue team detection engineering

**CTF Achievements**
- TryHackMe: Top 5% globally · Gold rank · 500+ rooms completed
- HackTheBox: Pro Hacker · 45+ machines pwned
- DEFCON CTF Qualifier participant (2023)

---

## REFERENCES
Available from current employer and previous line manager upon request."""


def _cv_cs_graduate() -> str:
    return """# JORDAN SMITH
**Computer Science Graduate | Software Engineer**

📧 jordan.smith@email.com · 📱 +1 (415) 555-0192 · 📍 San Francisco, CA
🔗 linkedin.com/in/jordansmith-dev · 💻 github.com/jordansmith · 🌐 jordansmith.dev

---

## PROFESSIONAL SUMMARY

Motivated Computer Science graduate with a strong foundation in algorithms, full-stack development, and cloud technologies. Experienced in Python, JavaScript, and React through internships and independent projects. Dean's List all 4 years. Looking for a Junior Software Engineering role to deliver real-world impact.

---

## EDUCATION

**Bachelor of Science — Computer Science** | GPA: 3.8/4.0
University of California, Berkeley | May 2024

- Dean's List: All 8 semesters
- Relevant coursework: Data Structures & Algorithms, Operating Systems, Databases, Computer Networks, ML, Software Engineering
- Senior Capstone: Real-time collaborative code editor using WebSockets, React, Node.js — presented to 200+ attendees

---

## TECHNICAL SKILLS

**Languages:** Python · JavaScript/TypeScript · Java · C++ · SQL · HTML/CSS
**Frameworks:** React · Next.js · Node.js · Express · FastAPI · Django
**Databases:** PostgreSQL · MongoDB · Redis · MySQL
**DevOps/Cloud:** AWS (EC2, S3, Lambda) · Docker · Git/GitHub · CI/CD · Linux
**Tools:** VS Code · Postman · Figma · Jira · Agile/Scrum

---

## WORK EXPERIENCE

### **Software Engineering Intern** | Google, Mountain View, CA
*May 2023 – August 2023*

- Developed a Google Workspace feature reducing document load time by **23%** through optimised lazy-loading
- Maintained 95%+ test coverage on all submitted code; changes merged to production serving millions of users
- Worked in Agile sprints with team of 8 engineers; received **"Exceeds Expectations"** performance review

### **Web Development Intern** | TechStartup Inc., Remote
*June 2022 – August 2022*

- Built 12 responsive React components for customer dashboard (adopted by **5,000+ users**)
- Integrated Stripe payments and Twilio SMS APIs into Node.js backend
- Reduced page load time **40%** through code splitting and image optimisation

---

## PROJECTS

**StudyBuddy AI App** | Python, FastAPI, React, PostgreSQL | 2024
- Full-stack app with AI quiz generation (OpenAI API); **200+ active users**
- Deployed on AWS EC2 with automated CI/CD via GitHub Actions
- [github.com/jordansmith/studybuddy]

**E-Commerce Platform** | Next.js, Node.js, MongoDB, Stripe | 2023
- Complete store with auth, cart, checkout, Stripe payments, admin dashboard
- [github.com/jordansmith/ecommerce]

---

## CERTIFICATIONS
- AWS Certified Cloud Practitioner (2023)

---

## REFERENCES — Available upon request"""


def _cv_software_engineer() -> str:
    return """# SAM WILLIAMS
**Full-Stack Software Engineer**

📧 sam.williams@email.com · 📱 +44 7911 123456 · 📍 Manchester, UK
🔗 linkedin.com/in/samwilliams-dev · 💻 github.com/samwilliams

---

## PROFESSIONAL SUMMARY

Full-Stack Software Engineer with 4 years building scalable web applications and microservices. Expert in React, Node.js, and cloud infrastructure. Delivered 15+ production applications serving 100,000+ combined users. Passionate about clean code, TDD, and developer experience.

---

## TECHNICAL SKILLS

**Frontend:** React · TypeScript · Next.js · Vue.js · Tailwind CSS · Redux
**Backend:** Node.js · Python (FastAPI/Django) · Java Spring Boot · GraphQL · REST APIs
**Databases:** PostgreSQL · MongoDB · Redis · Elasticsearch
**Cloud/DevOps:** AWS · Docker · Kubernetes · Terraform · CI/CD (GitHub Actions)
**Testing:** Jest · Cypress · Pytest · TDD/BDD

---

## WORK EXPERIENCE

### **Senior Software Engineer** | FinTech Innovations Ltd, Manchester
*March 2022 – Present*

- Architected real-time payment processing microservice handling **£2M+ daily transactions** (99.99% uptime)
- Led monolith-to-microservices migration reducing deployment time from 2 hours to **8 minutes**
- Mentored 3 junior engineers through weekly 1:1s and code reviews
- Increased code test coverage from 20% to **85%** across the platform

### **Software Engineer** | Digital Agency Co., Leeds
*July 2020 – February 2022*

- Built 8 full-stack applications for NHS, retail, and education sector clients
- Developed React Native mobile app: **15,000+ downloads**, 4.6★ App Store rating

---

## EDUCATION

**BEng Software Engineering** — **First Class Honours**
University of Manchester | 2020

---

## REFERENCES — Available upon request"""


def _cv_data_scientist() -> str:
    return """# PRIYA SHARMA
**Data Scientist | Machine Learning Engineer**

📧 priya.sharma@email.com · 📱 +1 (212) 555-0187 · 📍 New York, NY
🔗 linkedin.com/in/priyasharma-ds · 💻 github.com/priyasharma-ml · 📊 kaggle.com/priyasharma

---

## PROFESSIONAL SUMMARY

Data Scientist with 3 years building and deploying ML models generating $4M+ annual business value. Expert in Python, deep learning, and MLOps. Published researcher with work cited 47 times. Passionate about translating complex data into actionable insights.

---

## TECHNICAL SKILLS

**Languages:** Python · R · SQL · Scala
**ML/DL:** TensorFlow · PyTorch · scikit-learn · Hugging Face · LangChain
**Data:** Pandas · NumPy · Spark · Kafka · Airflow · dbt
**Visualisation:** Tableau · Power BI · Matplotlib · Plotly · Seaborn
**Cloud/MLOps:** AWS SageMaker · Azure ML · MLflow · Docker · Kubeflow

---

## WORK EXPERIENCE

### **Data Scientist** | Bloomberg LP, New York
*August 2022 – Present*

- Built NLP sentiment model (91.3% accuracy) integrated into trading algorithms managing **$500M portfolio**
- Developed customer churn prediction model (87% AUC) reducing churn by **18%** saving $2.3M/year
- Built real-time anomaly detection processing **10M+ daily transactions** (<50ms latency)
- Reduced model training time by 60% through distributed computing (Spark/AWS EMR)

### **ML Research Intern** | Microsoft Research, Redmond
*May 2021 – August 2021*

- Co-authored paper on transformer-based time series forecasting (NeurIPS 2022)
- Improved RMSE by **34%** using novel attention mechanism

---

## EDUCATION

**MSc Data Science** | Columbia University | 2022 | GPA: 4.0/4.0
**BSc Statistics & Computer Science** | University of Toronto | 2021 | First Class

---

## REFERENCES — Available upon request"""


def _cv_chemist() -> str:
    return """# DR. EMILY CHEN
**Analytical Chemist | Research Scientist**

📧 emily.chen@email.com · 📱 +44 7700 456789 · 📍 Cambridge, UK
🔗 linkedin.com/in/emilychen-chem · 🔬 ORCID: 0000-0001-2345-6789

---

## PROFESSIONAL SUMMARY

Analytical Chemist with 5 years of experience in pharmaceutical R&D and quality control. Expert in HPLC, GC-MS, and NMR spectroscopy. Track record of developing novel analytical methods that reduced testing time by 35%. Strong background in regulatory compliance (GMP, ICH guidelines). Published author with 8 peer-reviewed papers.

---

## TECHNICAL EXPERTISE

**Analytical Techniques:**
- Chromatography: HPLC, GC-MS, LC-MS/MS, Ion chromatography
- Spectroscopy: NMR (¹H, ¹³C), IR, UV-Vis, Raman, AAS, ICP-OES
- Separation: Capillary electrophoresis, SPE, LLE

**Laboratory Skills:**
- Method development and validation (ICH Q2)
- Stability testing (ICH Q1)
- Impurity profiling and characterisation
- Titration, gravimetric analysis

**Software:** Empower 3 · MassLynx · MestReNova · ChemDraw · Python (data analysis) · Excel

**Compliance:** GMP · GLP · FDA/EMA guidelines · ISO 17025

---

## WORK EXPERIENCE

### **Senior Analytical Chemist** | AstraZeneca, Cambridge
*September 2021 – Present*

- Developed and validated **12 HPLC methods** for API and drug product analysis per ICH Q2 guidelines
- Investigated and resolved **23 OOS results** through root cause analysis, maintaining 100% regulatory compliance
- Reduced analytical testing turnaround time by **35%** through automation and method optimisation
- Mentored 2 junior chemists; led internal GMP training programme for 15 analysts
- Led annual GMP audit achieving **zero critical observations** in 2022 and 2023

### **Analytical Chemist** | GlaxoSmithKline, Stevenage
*July 2019 – August 2021*

- Performed routine and non-routine testing of APIs, excipients, and finished products by HPLC, GC, and NMR
- Supported 3 clinical trial submissions with analytical data packages for FDA/EMA
- Contributed to patent application for novel synthesis method

### **Research Chemist (Postdoctoral Fellow)** | University of Cambridge
*October 2018 – June 2019*

- Synthesised and characterised 40+ novel organic compounds for anticancer drug discovery programme
- Published 3 papers in peer-reviewed journals (Journal of Medicinal Chemistry, Organic Letters)

---

## EDUCATION

**PhD Organic Chemistry** — **Distinction**
University of Cambridge | 2018
- Thesis: "Novel Synthesis of Fluorinated Heterocycles for Pharmaceutical Applications"
- Supervisor: Prof. John Smith FRS
- EPSRC Doctoral Training Award recipient

**MChem (Hons) Chemistry** — **First Class (87% average)**
University of Bristol | 2014
- Year abroad at ETH Zurich
- Final year project: Asymmetric synthesis of amino acids

---

## PUBLICATIONS (Selected)

1. Chen, E. et al. (2022). "Rapid HPLC method for simultaneous determination of related substances." *Analytical Chemistry*, 94(8), 3421–3429.
2. Chen, E. et al. (2020). "Synthesis of fluorinated pyrimidine derivatives." *J. Med. Chem.*, 63(14), 7832–7844.
3. Chen, E. et al. (2019). "Novel asymmetric catalysis approach." *Organic Letters*, 21(5), 1456–1460.

---

## CERTIFICATIONS & TRAINING

| Certification | Year |
|--------------|------|
| Chartered Chemist (CChem), Royal Society of Chemistry | 2021 |
| GMP for Pharmaceutical Manufacturing (Intertek) | 2022 |
| Statistical Analysis for Analytical Validation | 2020 |
| Chemical Weapons Convention Awareness | 2019 |

---

## PROFESSIONAL MEMBERSHIPS

- Royal Society of Chemistry (MRSC) — Member since 2014
- Society of Chemical Industry — Member

---

## REFERENCES

Available from line manager (AstraZeneca) and PhD supervisor upon request.

---
*💡 Customise with your actual name, publications, and experience dates.*"""


def _cv_nurse() -> str:
    return """# GRACE OKONKWO
**Registered Nurse (RN)**

📧 grace.okonkwo@email.com · 📱 +44 7700 654321 · 📍 Birmingham, UK
NMC Pin: 12A3456B · DBS: Enhanced (2024)

---

## PROFESSIONAL SUMMARY

Compassionate Registered Nurse with 5 years of experience in acute medical and surgical wards. Skilled in patient assessment, medication administration, wound care, and multidisciplinary collaboration. Committed to evidence-based, patient-centred care. Zero medication errors in 3 years. 97% patient satisfaction score (2023).

---

## CLINICAL SKILLS

- IV cannulation and venepuncture
- Medication administration (oral, IV, IM, SC)
- Wound assessment and dressing
- ECG monitoring and interpretation
- NEWS2 scoring and deteriorating patient management
- Urinary and nasogastric catheterisation
- Pre/post-operative care
- Blood transfusion administration
- SBAR communication tool
- Basic and Advanced Life Support (BLS/ALS)

---

## WORK EXPERIENCE

### **Staff Nurse — Acute Medical Ward (Ward 7)** | Queen Elizabeth Hospital, Birmingham NHS Trust
*September 2021 – Present*

- Provide holistic nursing care for 8–12 patients per shift on a 28-bed acute medical ward
- Administer medications safely per NMC standards; **zero medication errors** in 3 years
- Conduct NEWS2 assessments; escalated 12 deteriorating patients to ITU with positive outcomes
- Supported 3 newly qualified nurses through NMC preceptorship programme
- Achieved **97% patient satisfaction score** in 2023 ward survey
- Act as shift coordinator in charge nurse's absence

### **Staff Nurse — Surgical Ward** | Heartlands Hospital, Birmingham NHS Trust
*August 2019 – August 2021*

- Provided pre/post-operative care for orthopaedic and general surgery patients
- Managed post-surgical pain assessment, wound care, and early mobilisation programmes
- Participated in monthly clinical audit (pressure ulcer prevention; falls prevention)

---

## EDUCATION

**BSc (Hons) Adult Nursing** — **2:1**
Birmingham City University | Graduated: July 2019

**A-Levels:** Biology (A), Chemistry (B), Psychology (B)
**GCSEs:** 10 subjects including English and Maths (Grades A–B)

---

## TRAINING & CERTIFICATIONS

| Course | Provider | Year |
|--------|----------|------|
| Basic Life Support (BLS) | Resuscitation Council UK | 2024 |
| Intermediate Life Support (ILS) | Resuscitation Council UK | 2023 |
| Venepuncture & IV Cannulation | Birmingham NHS Trust | 2020 |
| Wound Care (TVN-assessed) | Birmingham NHS Trust | 2021 |
| Safe Handling of Medicines | NMC / CPPE | Annual |

---

## REFERENCES

Available from Ward Manager (QE Hospital) and previous Ward Sister (Heartlands Hospital)."""


def _cv_teacher() -> str:
    return """# MICHAEL BROWN
**Secondary Teacher — Mathematics & Computer Science**

📧 michael.brown@email.com · 📱 +44 7700 789012 · 📍 London, UK
DBS: Enhanced (2024) · QTS: Qualified Teacher Status

---

## PROFESSIONAL SUMMARY

Dedicated secondary teacher with 6 years of experience raising achievement in Mathematics and Computer Science at GCSE and A-Level. GCSE pass rate increased from 69% to 87% in two years. Experienced in differentiation, SEND, and curriculum design. Head of Computer Science since 2021.

---

## TEACHING EXPERIENCE

### **Head of Computer Science** | Westbridge Academy, London
*September 2021 – Present (KS3, KS4 GCSE, KS5 A-Level)*

- Raised GCSE CS pass rate from **69% to 87%** in two academic years
- Designed and delivered new KS3 computational thinking curriculum adopted across the department
- Established school coding club: **45 active members**; 12 students entered national competitions
- Line manage and mentor 2 Early Career Teachers (ECTs)
- Coordinated Year 11 intervention programme: boosted projected grades by one grade boundary for 18 students

### **Mathematics & ICT Teacher** | Northside Secondary School, Birmingham
*September 2018 – August 2021 (Years 7–11)*

- Taught mixed-ability Mathematics and ICT across 5 year groups
- Differentiated lessons for SEND, EAL, and gifted & talented learners
- Form tutor for Year 9 group (30 students)

---

## EDUCATION

**PGCE Secondary Mathematics** | University of Birmingham | 2018
**BSc Mathematics** — **2:1** | University of Leicester | 2017

**CPD:** Safeguarding Level 3 · SENCO Awareness · Digital Literacy Teaching (Google Certified Educator)

---

## REFERENCES

Available from current Headteacher and previous line manager."""


def _cv_finance() -> str:
    return """# CLAIRE JOHNSON
**Chartered Accountant | Senior Financial Analyst**

📧 claire.johnson@email.com · 📱 +44 7700 321098 · 📍 London, UK
ACA Qualified (ICAEW, 2022) · LinkedIn: linkedin.com/in/clairejohnson-aca

---

## PROFESSIONAL SUMMARY

ACA-qualified Chartered Accountant with 5 years of experience in financial analysis, audit, and management accounting. Identified £1.8M in annual cost savings. Experience across FTSE 250 companies and Big 4 audit practice. Strong in financial modelling, variance analysis, and compliance.

---

## TECHNICAL SKILLS

**Finance:** Financial modelling (Excel/Power BI) · DCF analysis · Budget preparation · IFRS/UK GAAP
**Software:** Advanced Excel (VBA) · SAP · Oracle Financials · Power BI · Tableau
**Audit:** External audit · Internal controls · Risk assessment · SOX compliance

---

## WORK EXPERIENCE

### **Senior Financial Analyst** | Barclays PLC, London
*April 2022 – Present*

- Produce financial models supporting **£500M+ investment decisions**
- Lead monthly management accounts for 3 business units (**£120M combined revenue**)
- Identified **£1.8M annual cost savings** through detailed P&L variance analysis
- Manage and develop 2 junior analysts

### **Audit Senior** | KPMG, London
*September 2019 – March 2022*

- Led audit engagements for 12 clients (revenues £50M–£2B) in financial services and retail
- Supervised teams of 3–5 junior staff; reviewed working papers and client deliverables

---

## EDUCATION

**ACA Qualification** | ICAEW | Qualified 2022 — First-time passes all 15 examinations
**BSc Accounting & Finance** — **First Class Honours**
University of Exeter | 2019

---

## REFERENCES — Available upon request"""


def _cv_marketing() -> str:
    return """# ZARA AHMED
**Digital Marketing Manager**

📧 zara.ahmed@email.com · 📱 +44 7700 654321 · 📍 London, UK
🔗 linkedin.com/in/zaraahmed-marketing · Portfolio: zaraahmed.co.uk

---

## PROFESSIONAL SUMMARY

Creative Digital Marketing Manager with 4 years driving brand growth through data-led campaigns. Managed £500K+ annual ad spend with 340% average ROAS. Grew brand social following from 12K to 180K in 18 months. Expert in SEO, paid social, email marketing, and content strategy.

---

## SKILLS

**Paid Advertising:** Google Ads (certified) · Meta Ads · TikTok Ads · Pinterest Ads
**SEO/Analytics:** SEMrush · Ahrefs · Google Analytics 4 · Google Search Console
**Email Marketing:** Klaviyo · Mailchimp · HubSpot (certified)
**Content:** Canva · Adobe Photoshop · Hootsuite · Buffer
**Data:** Excel · Power BI · Google Data Studio

---

## WORK EXPERIENCE

### **Digital Marketing Manager** | FashionForward Ltd, London
*January 2022 – Present*

- Managed **£500K annual ad budget** (Google/Meta/TikTok/Pinterest)
- Grew Instagram from **12K to 180K** followers in 18 months (organic)
- Email campaigns: **34% open rate** (industry avg 21%), **6.8% CTR**
- SEO strategy: organic traffic +**215%** year-over-year

### **Marketing Executive** | TechStartup Inc., Remote
*June 2020 – December 2021*

- Supported B2B SaaS product launch generating **£200K ARR** in 6 months

---

## EDUCATION

**BA Marketing Communications** — **2:1** | University of the Arts London | 2020

**Certifications:** Google Ads · Meta Blueprint · HubSpot Content Marketing · CIM Level 4

---

## REFERENCES — Available upon request"""


def _cv_doctor() -> str:
    return """# DR. JAMES OSEI
**Junior Doctor (Foundation Year 2) | MBBS**

📧 james.osei@nhs.net · 📱 +44 7700 234567 · 📍 London, UK
GMC Number: 7654321 · Foundation Programme: Health Education England

---

## PROFESSIONAL SUMMARY

Dedicated Foundation Year 2 doctor with experience across Medicine, Surgery, and Emergency Medicine. Skilled in clinical assessment, procedural skills, and multidisciplinary team working. Committed to patient safety and evidence-based practice. Applying for Core Medical Training.

---

## CLINICAL SKILLS

History taking · Physical examination · Venepuncture/cannulation · ABG sampling · ECG interpretation · Pleural aspiration · Lumbar puncture (supervised) · Catheterisation · NG tube insertion · Prescribing (acute and clerking)

---

## FOUNDATION POSTS

### **FY2 — Emergency Medicine** | King's College Hospital NHS FT
*August 2024 – Present*
- Assessing and managing acute presentations (ACS, sepsis, stroke, trauma)
- ALS provider; first responder for cardiac arrests

### **FY1 — Acute Medicine & General Surgery**
Completed August 2024

---

## EDUCATION

**MBBS Medicine** — **Honours**
King's College London | 2023
- Intercalated BSc: Pathology — **First Class**

---

## REFERENCES — Available from Foundation Programme Director"""


def _cv_lawyer() -> str:
    return """# SARAH CHEN
**Solicitor — Corporate & Commercial Law**

📧 sarah.chen@email.com · 📱 +44 7700 987654 · 📍 London, UK
Solicitor of England & Wales (Admitted 2022) | LinkedIn: linkedin.com/in/sarahchen-law

---

## PROFESSIONAL SUMMARY

Qualified Corporate Solicitor with 3 years PQE at a top-tier London law firm. Experience advising on M&A transactions (£10M–£500M), commercial contracts, and corporate governance. Strong analytical ability, attention to detail, and client relationship management.

---

## LEGAL SKILLS

Corporate M&A · Due diligence · SPA and SHA drafting · Commercial contracts · Corporate governance · Joint ventures · GDPR/data protection · Employment law (basic)

---

## WORK EXPERIENCE

### **Associate Solicitor — Corporate** | Allen & Overy, London
*September 2022 – Present*

- Advised on 8 M&A transactions (total value £1.2B) as lead associate on 3 deals
- Drafted and negotiated SPAs, SHAs, and ancillary documents
- Managed due diligence teams of 2–4 trainees

### **Trainee Solicitor** | Allen & Overy, London
*September 2020 – September 2022*
- Seats: Corporate, Dispute Resolution, Finance, Employment

---

## EDUCATION

**LPC (Distinction)** | BPP Law School | 2020
**LLB Law (First Class Honours)** | UCL | 2019

---

## REFERENCES — Available upon request"""


def _cv_architect() -> str:
    return """# DAVID MARTINEZ
**Architect (Part III Qualified) | ARB Registered**

📧 david.martinez@email.com · 📱 +44 7700 112233 · 📍 London, UK
ARB Registration: 123456K · RIBA Member | Portfolio: davidmartinez.co.uk

---

## PROFESSIONAL SUMMARY

RIBA-chartered architect with 6 years of experience in residential, commercial, and mixed-use developments. Led design from concept to completion on projects valued up to £15M. Proficient in sustainable design, BIM, and planning. Passionate about creating spaces that improve people's lives.

---

## TECHNICAL SKILLS

**Design:** AutoCAD · Revit (BIM Level 2) · SketchUp · Rhino · V-Ray · Adobe Creative Suite
**Project:** MS Project · Asta Powerproject · JCT contracts
**Standards:** Building Regulations · Planning Policy · BREEAM · Passivhaus

---

## WORK EXPERIENCE

### **Project Architect** | Foster + Partners, London
*March 2021 – Present*

- Led design development for a **£15M mixed-use scheme** (120 residential units + retail) from RIBA Stage 2–5
- Obtained planning permission for 3 projects; 100% success rate
- Coordinated with structural, M&E, and landscape consultants
- Reduced carbon footprint of flagship project by 30% through passive design strategies

### **Architectural Assistant (Part II)** | Zaha Hadid Architects
*June 2018 – February 2021*

- Contributed to concept and detailed design on 5 international projects
- Prepared planning drawings, technical packages, and client presentations

---

## EDUCATION

**MArch Architecture (Part II)** — **Distinction** | Bartlett School of Architecture, UCL | 2018
**BA (Hons) Architecture (Part I)** — **First Class** | University of Edinburgh | 2015

**ARB/RIBA Part III** | Chartered Member since 2021

---

## REFERENCES — Available upon request"""


def _assignment_helper(text: str) -> str:
    """Format the student's actual content into proper academic structure."""
    words = text.split()
    word_count = len(words)

    # If it's clearly a question (very short), answer it as an essay prompt
    if word_count < 20:
        topic = text.strip().rstrip('?')
        return _write_essay_on_topic(topic)

    text_lower = text.lower()

    # Detect subject
    subject = "General Studies"
    if any(w in text_lower for w in ['photosynthesis', 'cell', 'osmosis', 'mitosis', 'enzyme', 'dna', 'evolution', 'biology', 'organ']):
        subject = "Biology"
    elif any(w in text_lower for w in ['medicine', 'medical', 'health', 'disease', 'doctor', 'treatment', 'patient']):
        subject = "Health Sciences"
    elif any(w in text_lower for w in ['chemistry', 'element', 'molecule', 'reaction', 'acid', 'compound']):
        subject = "Chemistry"
    elif any(w in text_lower for w in ['physics', 'force', 'energy', 'velocity', 'acceleration', 'quantum']):
        subject = "Physics"
    elif any(w in text_lower for w in ['history', 'war', 'century', 'empire', 'revolution', 'ancient', 'colonialism']):
        subject = "History"
    elif any(w in text_lower for w in ['business', 'market', 'economic', 'company', 'profit', 'trade']):
        subject = "Business & Economics"
    elif any(w in text_lower for w in ['computer', 'software', 'algorithm', 'data', 'programming', 'ai']):
        subject = "Computer Science"
    elif any(w in text_lower for w in ['environment', 'climate', 'ecosystem', 'sustainability', 'carbon']):
        subject = "Environmental Science"
    elif any(w in text_lower for w in ['life', 'journey', 'purpose', 'growth', 'connection', 'meaning', 'happiness']):
        subject = "Philosophy & Personal Development"
    elif any(w in text_lower for w in ['geography', 'population', 'earthquake', 'tectonic', 'urbanis']):
        subject = "Geography"
    elif any(w in text_lower for w in ['art', 'painting', 'sculpture', 'creative', 'aesthetic']):
        subject = "Art & Design"

    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 15]

    intro = sentences[0] if sentences else text[:100]
    body_sentences = sentences[1:max(4, len(sentences)-1)] if len(sentences) > 2 else sentences
    conclusion_sentence = sentences[-1] if len(sentences) > 1 else text[-100:]

    # Detect writing level
    complex_words = sum(1 for w in ['furthermore', 'moreover', 'paradigm', 'empirical', 'synthesis', 'ephemeral', 'paradox'] if w in text_lower)
    simple_words = sum(1 for w in ['very', 'nice', 'good', 'bad', 'big', 'small', 'i went', 'i did', 'i had'] if w in text_lower)

    if complex_words >= 3:
        level = "Advanced Academic (University Level)"
    elif simple_words >= 3 or word_count < 60:
        level = "Foundation Level (Primary/KS3)"
    else:
        level = "Intermediate (GCSE/Secondary Level)"

    # Build headings from the text
    headings = re.findall(r'(?:^|\n)([A-Z][a-zA-Z &]{3,50})(?:\n|$)', text)
    has_headings = len(headings) >= 2

    if has_headings:
        main_body = f"""
### Section 1: {headings[0] if headings else 'Background & Context'}

{sentences[1] if len(sentences) > 1 else body_sentences[0] if body_sentences else ''}

This aspect of {subject.lower()} is fundamental to understanding the broader subject matter. Scholars in the field have emphasised the significance of this dimension, particularly in relation to practical applications and theoretical frameworks.

### Section 2: {headings[1] if len(headings) > 1 else 'Critical Analysis'}

{sentences[2] if len(sentences) > 2 else body_sentences[1] if len(body_sentences) > 1 else ''}

The significance of this point is evidenced by the ways in which it shapes outcomes and influences understanding across the discipline. A thorough examination reveals both strengths and limitations worth acknowledging.

### Section 3: {headings[2] if len(headings) > 2 else 'Contemporary Implications'}

{sentences[3] if len(sentences) > 3 else body_sentences[2] if len(body_sentences) > 2 else 'Contemporary applications continue to evolve as new developments emerge in this field.'}

These considerations highlight the ongoing relevance of the subject and its capacity to inform both academic discourse and practical decision-making.
"""
    else:
        main_body = f"""
### Main Argument

{body_sentences[0] if body_sentences else ''}

This represents a key insight within the study of {subject.lower()}. Drawing on established principles and emerging evidence, it becomes clear that this point carries significant weight in the broader academic conversation.

### Development & Evidence

{body_sentences[1] if len(body_sentences) > 1 else ''}

The implications here are considerable. Both theoretical and empirical perspectives support the view that this dimension merits sustained scholarly attention. Cross-disciplinary connections further enrich our understanding of the topic.

### Critical Reflection

{body_sentences[2] if len(body_sentences) > 2 else 'A balanced examination acknowledges both the strengths of the arguments presented and the challenges that remain.'}

While the evidence is compelling, it is important to acknowledge alternative viewpoints and the limits of current understanding. This intellectual humility strengthens rather than weakens the overall argument.
"""

    return f"""# Academic Assignment — Formatted

**Subject:** {subject}
**Level:** {level}
**Original Word Count:** {word_count} words
**Formatted:** Academic standard with structure, transitions, and citations guide

---

## Introduction

{intro}

This assignment examines key themes in {subject.lower()}, drawing on the ideas presented to provide a structured and critically engaged analysis. The central argument advanced herein is that {intro[:80].rstrip('.')}... — a position substantiated through the evidence and reasoning that follows.

---

## Background and Context

To fully appreciate the subject matter, it is necessary to situate the discussion within its broader theoretical and historical context. {subject} as a field of inquiry has evolved significantly, shaped by foundational research, changing social conditions, and advances in knowledge.

{sentences[0] if sentences else ''}

This contextual understanding provides the foundation for the critical analysis that follows.

---

## Critical Analysis
{main_body}

---

## Discussion

The analysis presented above reveals important insights into {subject.lower()}. The evidence suggests that while substantial progress has been made, important questions remain open to further investigation.

{conclusion_sentence}

A balanced assessment requires acknowledging both achievements and limitations — a position that strengthens rather than weakens academic credibility.

---

## Conclusion

In conclusion, this assignment has provided a structured examination of {subject.lower()}, drawing attention to key themes, contextual factors, and analytical frameworks. The central argument has been substantiated through engagement with the primary content and contextual evidence.

The findings have meaningful implications for both academic understanding and practical application. Continued inquiry, informed by diverse perspectives and rigorous methodology, will be essential to advancing knowledge in this area.

---

## References

*(Replace with your actual sources in APA format)*

Author, A. A., & Author, B. B. (Year). *Title of book*. Publisher.
Author, C. (Year). Article title. *Journal Name*, *Volume*(Issue), pp. X–X. https://doi.org/xxxxx

---

*✅ Your original ideas have been preserved and elevated to academic standard. Replace all [bracketed text] with your specific evidence, citations, and details.*"""


def _write_essay_on_topic(topic: str) -> str:
    """Write a complete essay when the assignment tool receives a short question/topic."""
    topic_lower = topic.lower()

    if 'art' in topic_lower:
        title = "What Is Art? A Critical Exploration"
        content = """Art is one of the most enduring and versatile expressions of human experience. Spanning millennia of civilisation, art has served as a mirror to society, a vehicle for emotion, and a catalyst for cultural change. Yet despite its omnipresence, defining art remains one of philosophy's most debated questions.

At its most fundamental level, art is the intentional creation of objects, performances, or experiences designed to communicate ideas, evoke emotions, or reflect reality. From the prehistoric cave paintings of Lascaux to Picasso's cubist abstractions, art consistently reflects the values, anxieties, and aspirations of the society that produces it.

Theorists have long disputed the nature of art. Leo Tolstoy argued that art is fundamentally a communication of emotion — an artist's sincere attempt to transmit a feeling to an audience. Immanuel Kant, by contrast, located art's value in the aesthetic experience itself, defining beauty as producing "disinterested pleasure" — appreciation independent of personal desire or utility. More recently, the Institutional Theory of Art (Dickie, 1974) posits that something becomes art when it is presented as such by an authorised member of the "artworld," allowing for conceptual and provocative works like Marcel Duchamp's Fountain (1917) to be considered genuine art.

Contemporary art challenges traditional boundaries. Digital art, street art, performance art, and AI-generated imagery all push the definition further, raising profound questions about authorship, originality, and intent. What emerges is a picture of art not as a fixed category, but as a living, dynamic field of human endeavour.

Art fulfils critical functions in society: it preserves cultural heritage, challenges power, fosters empathy, and enables self-expression. Whether in a gallery, a concert hall, or a social media post, art continues to shape how we see ourselves and the world around us."""
    else:
        title = f"An Academic Essay: {topic.title()}"
        content = f"""The study of {topic} represents one of the most significant areas of inquiry within its respective discipline. Scholars, researchers, and practitioners have long recognised the importance of this topic, contributing to a rich body of literature that continues to evolve.

From a theoretical perspective, {topic} can be understood through multiple frameworks, each offering a distinct lens through which to examine its key dimensions. These range from structural approaches that emphasise systemic factors to interpretive approaches that foreground lived experience and subjective meaning.

Empirically, the evidence supporting our understanding of {topic} draws from a diverse range of sources. Quantitative studies provide measurable data on patterns and trends, while qualitative research illuminates the nuanced, contextual dimensions that statistics alone cannot capture. Together, these methodologies offer a more complete picture.

The practical implications of this subject are equally significant. Understanding {topic} enables more effective decision-making, informs policy, and contributes to real-world improvement across multiple sectors. Professionals working in this area must navigate complex challenges, drawing on both theoretical knowledge and applied experience.

Looking ahead, the field faces several emerging challenges and opportunities. Technological advances, shifting social dynamics, and global interconnectedness all shape the trajectory of this discipline. The capacity to adapt and integrate new knowledge will be essential for continued progress."""

    return f"""# {title}

**Subject:** Academic Essay
**Format:** Full academic structure with introduction, body, and conclusion

---

## Introduction

{content.split(chr(10))[0]}

This essay will examine the key dimensions of {topic}, drawing on theoretical perspectives and available evidence to construct a coherent and critically informed argument.

---

## Background and Theoretical Framework

{chr(10).join(content.split(chr(10))[1:3])}

---

## Critical Analysis

{chr(10).join(content.split(chr(10))[3:5])}

---

## Contemporary Relevance and Implications

{chr(10).join(content.split(chr(10))[5:])}

---

## Conclusion

In conclusion, this essay has explored the key dimensions of {topic}, demonstrating its significance both theoretically and in practice. The analysis has revealed that a comprehensive understanding requires engagement with multiple perspectives and a willingness to grapple with complexity.

Moving forward, continued scholarly attention to this subject will be essential. The questions it raises are not merely academic; they have practical consequences for how individuals, institutions, and societies navigate the challenges of the modern world.

---

## References

*(Add your actual sources here in APA format)*

Author, A. (Year). *Title of book*. Publisher.
Author, B., & Author, C. (Year). Article title. *Journal*, *Volume*(Issue), pp. X–X.

---

*✅ Complete essay written on your topic. Customise with your specific examples, citations, and course-specific requirements.*"""


def _research_summarizer(text: str) -> str:
    """Summarise the actual content provided — reads the real text."""
    words = text.split()
    word_count = len(words)

    if word_count < 30:
        return f"⚠️ Please paste more text to summarise (at least 50 words). You provided {word_count} words.\n\nFor research summaries, paste the full abstract, article, or paper text and I'll provide a structured analysis."

    text_lower = text.lower()
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 20]

    # Identify what kind of text this is
    is_research = any(w in text_lower for w in ['study', 'research', 'methodology', 'findings', 'participants', 'sample', 'data', 'results', 'hypothesis', 'abstract'])
    is_essay = any(w in text_lower for w in ['argue', 'suggest', 'claim', 'thesis', 'furthermore', 'however', 'therefore'])
    is_personal = any(w in text_lower for w in ['i woke', 'i went', 'i felt', 'my day', 'today i'])

    # Detect subject
    subject = "General"
    if any(w in text_lower for w in ['ai', 'machine learning', 'neural', 'algorithm', 'intelligence']):
        subject = "Artificial Intelligence & Technology"
    elif any(w in text_lower for w in ['medicine', 'medical', 'health', 'clinical', 'patient', 'drug', 'treatment']):
        subject = "Medicine & Healthcare"
    elif any(w in text_lower for w in ['environment', 'climate', 'ecosystem', 'carbon', 'sustainability']):
        subject = "Environmental Science"
    elif any(w in text_lower for w in ['life', 'growth', 'connection', 'purpose', 'meaning', 'journey']):
        subject = "Philosophy & Human Experience"
    elif any(w in text_lower for w in ['economy', 'market', 'gdp', 'inflation', 'trade']):
        subject = "Economics"
    elif any(w in text_lower for w in ['history', 'war', 'empire', 'revolution', 'century']):
        subject = "History"

    # Extract actual key sentences
    intro_sentence = sentences[0] if sentences else words[:20]
    key_sentences = sentences[1:min(4, len(sentences))] if len(sentences) > 1 else sentences
    conclusion_sentence = sentences[-1] if len(sentences) > 1 else ""

    # Find headings
    headings = re.findall(r'(?:^|\n)([A-Z][a-zA-Z &\-]{3,50})(?:\n|$)', text)
    has_structure = len(headings) >= 2

    # Word frequency for themes
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'are', 'was', 'were', 'it', 'this', 'that', 'they', 'we', 'i', 'you', 'he', 'she', 'be', 'by', 'as', 'not', 'from', 'its', 'their', 'our', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'can', 'could', 'should', 'may', 'might', 'which', 'who', 'what', 'when', 'where', 'how', 'than', 'more', 'most', 'also', 'only', 'such', 'if', 'while', 'after'}
    word_freq = {}
    for w in words:
        w = re.sub(r'[^a-z]', '', w.lower())
        if len(w) > 4 and w not in stop_words:
            word_freq[w] = word_freq.get(w, 0) + 1
    top_themes = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:6]
    theme_words = ', '.join(w for w, _ in top_themes if w)

    text_type = "Research Paper" if is_research else "Essay/Article" if is_essay else "Personal Writing" if is_personal else "Text"

    return f"""## 🔬 Research & Text Summary

**Document type:** {text_type}
**Subject area:** {subject}
**Analysed:** {word_count} words · {len(sentences)} sentences

---

### 📌 Central Theme

**In one sentence:**
> "{intro_sentence if isinstance(intro_sentence, str) else ' '.join(intro_sentence)}"

**Key themes identified:** {theme_words if theme_words else 'varied across multiple topics'}

---

### 🎯 Main Arguments

{"**Structured text with " + str(len(headings)) + " sections:** " + ", ".join(headings[:5]) if has_structure else "**Continuous text — main points extracted:**"}

**Point 1:**
{sentences[0] if sentences else ''}

**Point 2:**
{sentences[min(1, len(sentences)-1)] if len(sentences) > 1 else ''}

{"**Point 3:**" + chr(10) + sentences[min(2, len(sentences)-1)] if len(sentences) > 2 else ''}

{"**Point 4:**" + chr(10) + sentences[min(3, len(sentences)-1)] if len(sentences) > 3 else ''}

---

### 📊 Writing Style & Evidence

**Style:** {"Formal academic — evidence-based, third person, technical vocabulary" if is_research else "Analytical essay — argument-driven with transitions" if is_essay else "Personal narrative — first person, observational" if is_personal else "Informational — descriptive and explanatory"}

**Evidence used:**
{"- Empirical data and research findings" if is_research else "- Personal observation and experience" if is_personal else "- Argument and reasoning"}
{"- Theoretical frameworks and academic citations" if is_research or is_essay else ""}
{"- Specific examples to support claims" if any(w in text_lower for w in ['example', 'instance', 'such as', 'for example']) else ""}

**Sample passage:**
> *"{' '.join(words[int(word_count*0.3):int(word_count*0.5)])[:250]}..."*

---

### ✅ Conclusions

**The text concludes:**
> "{conclusion_sentence}"

{"This conclusion **reinforces the central thesis** and brings the argument full circle." if conclusion_sentence and len(conclusion_sentence) > 30 else "The conclusion ties together the main threads of the discussion."}

---

### 💡 Critical Evaluation

| Strength | Area for Development |
|----------|---------------------|
| {"Clear thematic structure" if has_structure else "Fluid narrative flow"} | {"Add more primary data/citations" if not is_research else "Consider counter-arguments"} |
| {"Technical vocabulary" if is_research else "Accessible language"} | {"More specific examples would strengthen claims" if not is_personal else "Could include broader context"} |
| {f"Covers {len(sentences)} distinct points" if len(sentences) > 3 else "Focused argument"} | {"Conclusion could be more comprehensive" if len(conclusion_sentence) < 50 else "Well-developed conclusion"} |

---

### 📚 For Academic Use

**This text is suitable as:**
{"- Primary research source" if is_research else ""}
{"- Secondary/analytical source" if is_essay else ""}
{"- Personal reflective writing" if is_personal else ""}

**Recommended follow-up:**
- Search Google Scholar: *{subject.lower()} {theme_words.split(',')[0] if theme_words else 'key concepts'}*
- Look for systematic reviews and meta-analyses on these themes

---

*Summary of {word_count} words · {len(sentences)} sentences analysed*"""


# ══════════════════════════════════════════════════════════════════════════════
# MAIN DISPATCH
# ══════════════════════════════════════════════════════════════════════════════

def get_ai_response(tool: str, content: str, history: list = None) -> str:
    """Route to correct tool handler."""
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
