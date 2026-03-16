import React, { useState, useEffect } from "react";
import axios from "axios";
import TaskLogger from "./TaskLogger";
import Navbar from "./Navbar";

const Home = () => {
  const [tasks, setTasks] = useState([]);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  useEffect(() => {
    const fetchTasks = async () => {
      const token = localStorage.getItem("token");
      if (!token) return;
      try {
        const response = await axios.get("http://127.0.0.1:8000/tasks", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setTasks(response.data);
      } catch (err) {
        console.error("Failed to fetch tasks", err);
      }
    };
    fetchTasks();
  }, [refreshTrigger]);

  return (
    <main className="container">
      <Navbar />
      <div className="grid">
        <div>
          <TaskLogger
            onTaskAdded={() => setRefreshTrigger((prev) => prev + 1)}
          />
        </div>
        <div>
          <article>
            <header>
              <h4>Recent Logs</h4>
            </header>
            {tasks.length === 0 ? (
              <p>No tasks logged yet.</p>
            ) : (
              <table role="grid">
                <thead>
                  <tr>
                    <th scope="col">Task</th>
                    <th scope="col">Category</th>
                    <th scope="col">Time</th>
                  </tr>
                </thead>
                <tbody>
                  {tasks
                    .slice()
                    .reverse()
                    .map((task) => (
                      <tr key={task.id}>
                        <td>{task.name}</td>
                        <td>
                          <kbd>{task.label}</kbd>
                        </td>
                        <td>{task.duration_minutes}m</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            )}
          </article>
        </div>
      </div>
    </main>
  );
};

export default Home;
