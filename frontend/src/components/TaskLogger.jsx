import React, { useState } from "react";
import axios from "axios";

const TaskLogger = ({ onTaskAdded }) => {
  const [task, setTask] = useState({
    name: "",
    duration_minutes: "",
    label: "other",
  });
  const [loading, setLoading] = useState(false);
  const labels = [
    "study",
    "work",
    "meal",
    "health",
    "career",
    "sleep",
    "break",
    "distracted",
    "other",
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const token = localStorage.getItem("token");

    try {
      await axios.post("http://127.0.0.1:8000/tasks", task, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTask({ name: "", duration_minutes: "", label: "other" });
      onTaskAdded();
    } catch (err) {
      alert("Failed to save task:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <article>
      <header>
        <h3>Log Activity</h3>
      </header>
      <form onSubmit={handleSubmit}>
        <fieldset className="grid">
          <input
            placeholder="What did you do?"
            value={task.name}
            onChange={(e) => setTask({ ...task, name: e.target.value })}
            required
          />
          <input
            type="number"
            placeholder="Minutes"
            value={task.duration_minutes}
            onChange={(e) =>
              setTask({ ...task, duration_minutes: e.target.value })
            }
            required
          />
        </fieldset>
        <select
          value={task.label}
          onChange={(e) => setTask({ ...task, label: e.target.value })}
        >
          {labels.map((l) => (
            <option key={l} value={l}>
              {l}
            </option>
          ))}
        </select>
        <button type="submit" aria-busy={loading}>
          Add Task
        </button>
      </form>
    </article>
  );
};

export default TaskLogger;
