from fastapi import APIRouter, HTTPException
from controllers.todo import (
    create_todo,
    get_all_todos,
    get_todo_by_id,
    update_todo,
    delete_todo,
)
from models.todo import TodoCreate, TodoUpdate, TodoResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=TodoResponse)
async def create_todo_route(todo: TodoCreate):
    return await create_todo(todo)

@router.get("/", response_model=List[TodoResponse])
async def get_all_todos_route():
    return await get_all_todos()

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo_route(todo_id: int):
    todo = await get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo_route(todo_id: int, todo: TodoUpdate):
    updated_todo = await update_todo(todo_id, todo)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/{todo_id}", response_model=dict)
async def delete_todo_route(todo_id: int):
    deleted = await delete_todo(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}