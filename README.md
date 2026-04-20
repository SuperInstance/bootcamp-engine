# bootcamp-engine

4-phase greenhorn curriculum: **Read → Analyze → Build → Specialist**. The dojo as code.

Like teaching a greenhorn on a fishing boat: no rulebook, just time on deck. Agents progress through phases by completing assignments and maintaining a passing GPA. Promotions are earned, not given.

## Usage

```python
from bootcamp_engine import Bootcamp, Phase, Assignment

camp = Bootcamp()
horn = camp.enroll("agent-x")

camp.assign(horn, Assignment(id="r1", phase=Phase.READ, description="Read the codebase"))
camp.grade_assignment(horn, "r1", score=0.85, feedback="Good comprehension")

if horn.promotion_ready():
    camp.promote(horn)  # READ → ANALYZE
```

Zero deps. `pip install bootcamp-engine`
