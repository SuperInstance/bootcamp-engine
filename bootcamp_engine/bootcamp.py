"""Bootcamp curriculum engine for agent training."""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class Phase(Enum):
    READ = 0        # read codebase, understand context
    ANALYZE = 1     # find patterns, identify gaps
    BUILD = 2       # produce artifacts, write code
    SPECIALIST = 3  # deep expertise in a domain


@dataclass
class Grade:
    """Grade for an assignment."""
    score: float  # 0-1
    passed: bool
    feedback: str = ""
    graded_at: float = field(default_factory=time.time)


@dataclass
class Assignment:
    """A training assignment."""
    id: str
    phase: Phase
    description: str
    difficulty: float = 0.5  # 0-1
    min_score: float = 0.7  # to pass
    max_attempts: int = 3
    attempts: int = 0
    grade: Optional[Grade] = None
    
    def submit(self, score: float, feedback: str = "") -> Grade:
        self.attempts += 1
        grade = Grade(score=score, passed=score >= self.min_score, feedback=feedback)
        self.grade = grade
        return grade
    
    def can_retry(self) -> bool:
        return self.attempts < self.max_attempts and (self.grade is None or not self.grade.passed)


@dataclass
class Greenhorn:
    """A trainee agent in the bootcamp."""
    agent_id: str
    current_phase: Phase = Phase.READ
    assignments_completed: int = 0
    assignments_passed: int = 0
    total_score: float = 0.0
    enrolled_at: float = field(default_factory=time.time)
    specializations: List[str] = field(default_factory=list)
    
    def gpa(self) -> float:
        if self.assignments_completed == 0:
            return 0.0
        return self.total_score / self.assignments_completed
    
    def promotion_ready(self) -> bool:
        """Ready for next phase if GPA > 0.7."""
        return self.gpa() >= 0.7 and self.assignments_completed >= 3


class Bootcamp:
    """4-phase bootcamp curriculum engine.
    
    Usage:
        camp = Bootcamp()
        horn = camp.enroll("agent-x")
        camp.assign(horn, Assignment(id="r1", phase=Phase.READ, description="Read the codebase"))
        camp.grade_assignment(horn, "r1", score=0.85)
        camp.promote(horn)  # READ → ANALYZE
    """
    
    def __init__(self):
        self.greenhorns: Dict[str, Greenhorn] = {}
        self.assignments: Dict[str, Dict[str, Assignment]] = {}  # agent_id → {assign_id → Assignment}
    
    def enroll(self, agent_id: str) -> Greenhorn:
        horn = Greenhorn(agent_id=agent_id)
        self.greenhorns[agent_id] = horn
        self.assignments[agent_id] = {}
        return horn
    
    def assign(self, horn: Greenhorn, assignment: Assignment) -> bool:
        if assignment.phase != horn.current_phase:
            return False
        self.assignments[horn.agent_id][assignment.id] = assignment
        return True
    
    def grade_assignment(self, horn: Greenhorn, assignment_id: str, 
                         score: float, feedback: str = "") -> Optional[Grade]:
        a = self.assignments.get(horn.agent_id, {}).get(assignment_id)
        if not a:
            return None
        grade = a.submit(score, feedback)
        horn.assignments_completed += 1
        horn.total_score += score
        if grade.passed:
            horn.assignments_passed += 1
        return grade
    
    def promote(self, horn: Greenhorn) -> bool:
        if not horn.promotion_ready():
            return False
        next_phase = Phase(horn.current_phase.value + 1)
        if next_phase.value > Phase.SPECIALIST.value:
            return False
        horn.current_phase = next_phase
        return True
    
    def graduate(self, horn: Greenhorn, specialization: str = "") -> bool:
        if horn.current_phase != Phase.SPECIALIST:
            return False
        if specialization:
            horn.specializations.append(specialization)
        return True
    
    def roster(self) -> List[dict]:
        return [
            {"agent_id": h.agent_id, "phase": h.current_phase.name, 
             "gpa": round(h.gpa(), 2), "passed": h.assignments_passed}
            for h in self.greenhorns.values()
        ]
