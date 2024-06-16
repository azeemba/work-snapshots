import "./App.css";
import { Button, Tooltip } from "flowbite-react";
import { useEffect, useState } from "react";
import { Outlet, useLocation, Link } from "react-router-dom";
import "tailwindcss/tailwind.css";
import { Session } from "./components/sessionsummarycard";
import { TagObject } from "./components/tagbadge";

export type OutletContextInfo = {
  allSessions: Array<Session>;
  setAllSessions: React.Dispatch<React.SetStateAction<Array<Session>>>;
  availableTags: Array<TagObject>;
  setAvailableTags: React.Dispatch<React.SetStateAction<Array<TagObject>>>;
};
function App() {
  const location = useLocation();
  const [allSessions, setAllSessions] = useState<Array<Session>>([]);
  const [availableTags, setAvailableTags] = useState<Array<TagObject>>([]);
  function refreshClick() {
    fetch("/api/refresh").then(() => {
      window.location.reload();
    });
  }
  useEffect(() => {
    fetch("/api/worksessions")
      .then((response) => response.json())
      .then((data) => {
        setAllSessions(data);
      });
    fetch("/api/tags")
      .then((response) => response.json())
      .then((data) => {
        const tags = data.tags;
        tags.push({ tag: "" });
        setAvailableTags(tags);
      });
  }, []);

  return (
    <div className="bg-gradient-to-r from-gray-800 to-gray-900 min-h-screen text-white">
      <nav className="bg-gradient-to-r from-gray-700 to-gray-800 px-4 py-2 flex justify-between items-center">
        <div className="flex justify-between items-center">
          <div></div>
          <h1 className="text-3xl font-bold ml-3">Work Sessions</h1>
        </div>
        <div className="flex flex-row space-x-5">
          {location.pathname !== "/" ? (
            <Link to="/">
              <Button className="bg-indigo-500 text-indigo-50 hover:bg-indigo-600 transition-colors">
                Back
              </Button>
            </Link>
          ) : (
            <Link to="/stats">
              <Button className="bg-indigo-500 text-indigo-50 hover:bg-indigo-600 transition-colors">
                Stats
              </Button>
            </Link>
          )}
          <Tooltip content="Reloads data from disk.">
            <Button
              className="bg-indigo-500 text-indigo-50 hover:bg-indigo-600 transition-colors"
              onClick={refreshClick}
            >
              Refresh
            </Button>
          </Tooltip>
        </div>
      </nav>
      <Outlet
        context={{
          allSessions,
          setAllSessions,
          availableTags,
          setAvailableTags,
        }}
      ></Outlet>
    </div>
  );
}

export default App;
