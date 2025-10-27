from sqlalchemy.orm import Session
from models.project import Project
from models.user import User
from utils.calc_utils import calculate_phase_progress

def get_project_kpis(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return {}

    phases_progress = [calculate_phase_progress(phase.deliverables) for phase in project.phases]
    avg_progress = sum(phases_progress) / len(phases_progress) if phases_progress else 0

    total_budget = sum(phase.budget for phase in project.phases)
    total_spent = sum(phase.spent for phase in project.phases)
    current_margin = ((total_budget - total_spent) / total_budget * 100) if total_budget > 0 else 0

    return {
        "project_name": project.name,
        "average_progress": avg_progress,
        "budget_total": total_budget,
        "budget_spent": total_spent,
        "current_margin": round(current_margin, 2),
    }

def get_team_productivity(db: Session):
    users = db.query(User).all()
    productivity = []
    for u in users:
        avg_task_completion = u.performance.avg_task_completion
        on_time_delivery = u.performance.on_time_delivery
        productivity.append({
            "user_name": u.personal.name,
            "avg_task_completion": avg_task_completion,
            "on_time_delivery": on_time_delivery,
            "quality_score": u.performance.quality_score
        })
    return productivity