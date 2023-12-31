import './App.css'
import { Button, Tooltip } from "flowbite-react";
import { Outlet, useLocation, Link } from "react-router-dom";
import "tailwindcss/tailwind.css";

function App() {
  const location = useLocation();
  function refreshClick() {
    fetch("/api/refresh").then(() => {
      window.location.reload();
    });
  }

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
          ) : null}
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
      <Outlet></Outlet>
    </div>
  );
}

export default App;


