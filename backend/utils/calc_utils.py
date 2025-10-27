def calculate_phase_progress(deliverables: list) -> float:
    if not deliverables:
        return 0
    completed = sum(1 for d in deliverables if d["status"] == "completed")
    return round((completed / len(deliverables)) * 100, 2)