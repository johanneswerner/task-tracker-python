"""Test suite for TaskManager."""

from pathlib import Path

import pytest
from pytest import CaptureFixture

from task_cli import TaskManager


@pytest.fixture
def task_manager() -> TaskManager:
    """Fixture for creating a TaskManager instance."""
    manager = TaskManager(tasks_file="test_tasks.json")
    manager.tasks = []
    return manager

def test_add_task(task_manager: TaskManager) -> None:
    """Test adding a task."""
    task_manager.add_task("Test Task 1")
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0]["description"] == "Test Task 1"
    assert task_manager.tasks[0]["status"] == "todo"

def test_add_task_empty_description(task_manager: TaskManager, capsys: CaptureFixture[str]) -> None:
    """Test adding a task with an empty description."""
    task_manager.add_task("")
    captured = capsys.readouterr()
    assert "Task description cannot be empty." in captured.out
    assert len(task_manager.tasks) == 0

def test_update_task(task_manager: TaskManager) -> None:
    """Test updating a task."""
    task_manager.add_task("Test Task 1")
    task_manager.update_task(1, "Updated Task 1")
    assert task_manager.tasks[0]["description"] == "Updated Task 1"

def test_update_task_not_found(task_manager: TaskManager, capsys: CaptureFixture[str]) -> None:
    """Test updating a non-existent task."""
    task_manager.update_task(1, "Updated Task 1")
    captured = capsys.readouterr()
    assert "Task not found." in captured.out

def test_delete_task(task_manager: TaskManager) -> None:
    """Test deleting a task."""
    task_manager.add_task("Test Task 1")
    task_manager.delete_task(1)
    assert len(task_manager.tasks) == 0

def test_delete_task_not_found(task_manager: TaskManager, capsys: CaptureFixture[str]) -> None:
    """Test deleting a non-existent task."""
    task_manager.delete_task(1)
    captured = capsys.readouterr()
    assert "Task not found." in captured.out

def test_mark_task_in_progress(task_manager: TaskManager) -> None:
    """Test marking a task as in-progress."""
    task_manager.add_task("Test Task 1")
    task_manager.mark_task_in_progress(1)
    assert task_manager.tasks[0]["status"] == "in-progress"

def test_mark_task_in_progress_not_found(task_manager: TaskManager, capsys: CaptureFixture[str]) -> None:
    """Test marking a non-existent task as in-progress."""
    task_manager.mark_task_in_progress(1)
    captured = capsys.readouterr()
    assert "Task not found." in captured.out

def test_mark_task_done(task_manager: TaskManager) -> None:
    """Test marking a task as done."""
    task_manager.add_task("Test Task 1")
    task_manager.mark_task_done(1)
    assert task_manager.tasks[0]["status"] == "done"

def test_mark_task_done_not_found(task_manager: TaskManager, capsys: CaptureFixture[str]) -> None:
    """Test marking a non-existent task as done."""
    task_manager.mark_task_done(1)
    captured = capsys.readouterr()
    assert "Task not found." in captured.out

def test_list_tasks(task_manager: TaskManager, capsys: CaptureFixture[str]) -> None:
    """Test listing all tasks."""
    task_manager.add_task("Test Task 1")
    task_manager.add_task("Test Task 2")
    task_manager.list_tasks()
    captured = capsys.readouterr()
    assert "Test Task 1" in captured.out
    assert "Test Task 2" in captured.out

def test_list_tasks_by_status(task_manager: TaskManager, capsys: CaptureFixture[str]) -> None:
    """Test listing tasks by status."""
    task_manager.add_task("Test Task 1")
    task_manager.add_task("Test Task 2")
    task_manager.mark_task_done(2)
    task_manager.list_tasks(status="done")
    captured = capsys.readouterr()
    assert "Task 1 marked as done" not in captured.out
    assert "Task 2 marked as done" in captured.out

def test_load_tasks(task_manager: TaskManager) -> None:
    """Test loading tasks from file."""
    task_manager.add_task("Test Task 1")
    task_manager.save_tasks()
    new_manager = TaskManager(tasks_file="test_tasks.json")
    assert len(new_manager.tasks) == 1
    assert new_manager.tasks[0]["description"] == "Test Task 1"

def test_save_tasks(task_manager: TaskManager) -> None:
    """Test saving tasks to file."""
    task_manager.add_task("Test Task 1")
    task_manager.save_tasks()
    with Path.open("test_tasks.json") as file:
        data = file.read()
    assert "Test Task 1" in data

# Clean up the test file after tests
@pytest.fixture(scope="module", autouse=True)
def cleanup(request: pytest.FixtureRequest) -> None:
    """Fixture to clean up the test file after tests."""
    def remove_test_file() -> None:
        Path("test_tasks.json").unlink(missing_ok=True)
    request.addfinalizer(remove_test_file)
