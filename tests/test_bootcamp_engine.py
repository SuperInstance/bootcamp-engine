"""Tests for bootcamp-engine."""
import pytest
from bootcamp_engine import Bootcamp, Phase, Assignment


def test_enroll_and_assign():
    camp = Bootcamp()
    horn = camp.enroll("rookie-1")
    assert horn.current_phase == Phase.READ
    a = Assignment(id="r1", phase=Phase.READ, description="Read codebase")
    assert camp.assign(horn, a)


def test_grade_and_gpa():
    camp = Bootcamp()
    horn = camp.enroll("s1")
    camp.assign(horn, Assignment(id="r1", phase=Phase.READ, description="Read"))
    camp.assign(horn, Assignment(id="r2", phase=Phase.READ, description="Read2"))
    camp.grade_assignment(horn, "r1", 0.8)
    camp.grade_assignment(horn, "r2", 0.9)
    assert horn.gpa() == pytest.approx(0.85, abs=0.01)


def test_promotion():
    camp = Bootcamp()
    horn = camp.enroll("p1")
    for i in range(3):
        a = Assignment(id=f"r{i}", phase=Phase.READ, description=f"task {i}")
        camp.assign(horn, a)
        camp.grade_assignment(horn, f"r{i}", 0.8)
    assert horn.promotion_ready()
    assert camp.promote(horn)
    assert horn.current_phase == Phase.ANALYZE


def test_no_promotion_without_gpa():
    camp = Bootcamp()
    horn = camp.enroll("np")
    for i in range(3):
        a = Assignment(id=f"r{i}", phase=Phase.READ, description=f"t{i}")
        camp.assign(horn, a)
        camp.grade_assignment(horn, f"r{i}", 0.5)  # failing
    assert not horn.promotion_ready()


def test_wrong_phase_assignment():
    camp = Bootcamp()
    horn = camp.enroll("w1")
    a = Assignment(id="b1", phase=Phase.BUILD, description="Build")
    assert not camp.assign(horn, a)  # can't assign BUILD in READ phase


def test_retry():
    a = Assignment(id="retry", phase=Phase.READ, description="retry", max_attempts=3)
    a.submit(0.3)
    assert a.can_retry()
    a.submit(0.3)
    a.submit(0.3)
    assert not a.can_retry()  # maxed out


def test_graduate():
    camp = Bootcamp()
    horn = camp.enroll("grad")
    horn.current_phase = Phase.SPECIALIST
    assert camp.graduate(horn, "rust-crates")
    assert "rust-crates" in horn.specializations
