import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/learning",
  headers: {
    "Content-Type": "application/json",
  },
});

export const getTopics = () => API.get("/topics");
export const createTopic = (data) => API.post("/topics", data);
export const deleteTopic = (id) => API.delete(`/topics/${id}`);
export const getSubtopics = (topicId) => API.get(`/subtopics/${topicId}`);
export const createSubtopic = (data) => API.post("/subtopics", data);
export const toggleSubtopic = (id) => API.put(`/subtopics/${id}/toggle`);
export const getProjects = () => API.get("/projects");
export const createProject = (data) => API.post("/projects", data);
export const getEntries = () => API.get("/");
export const createEntry = (data) => API.post("/", data);
export const setMonthlyGoal = (hours) =>
  API.post("/goal", null, {
    params: { target_hours: hours },
  });
export const getDashboard = () => API.get("/analytics/dashboard");
export const getStudyTime = (mode = "daily") =>
  API.get(`/analytics/study-time?mode=${mode}`);
export const getBadges = () => API.get("/badges");

export default API;
