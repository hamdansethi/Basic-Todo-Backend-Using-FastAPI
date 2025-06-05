from sqlalchemy.orm import Session
from helpers.database import get_db
from models.todo import Todo, TodoCreate, TodoUpdate, TodoResponse
from datetime import datetime

async def create_todo(todo: TodoCreate) -> TodoResponse:
    db: Session = next(get_db())
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return TodoResponse.from_orm(db_todo)

async def get_all_todos() -> list[TodoResponse]:
    db: Session = next(get_db())
    todos = db.query(Todo).all()
    return [TodoResponse.from_orm(todo) for todo in todos]

async def get_todo_by_id(todo_id: int) -> TodoResponse | None:
    db: Session = next(get_db())
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        return TodoResponse.from_orm(todo)
    return None

async def update_todo(todo_id: int, todo: TodoUpdate) -> TodoResponse | None:
    db: Session = next(get_db())
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        return None
    update_data = todo.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return TodoResponse.from_orm(db_todo)

async def delete_todo(todo_id: int) -> bool:
    db: Session = next(get_db())
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        return False
    db.delete(db_todo)
    db.commit()
    return True