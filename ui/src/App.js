import React, { useEffect, useState } from 'react';
import { Button, Tooltip } from 'flowbite-react';
import 'tailwindcss/tailwind.css'

import SessionCard from './sessionCard';


function App() {
  const [sessions, setSessions] = useState([]);
  useEffect(() => {
    fetch("/api/worksessions").then(response => response.json()).then(data => setSessions(data))
  }, [])

  function refreshClick() {
    fetch("/api/refresh").then(() => { window.location.reload(false); })
  }

  return (
    <div className="bg-gradient-to-r from-gray-800 to-gray-900 min-h-screen text-white">
      <nav className="bg-gradient-to-r from-gray-700 to-gray-800 px-4 py-2 flex justify-between items-center">
        <div className="flex justify-between items-center">
          <div></div>
          <h1 className="text-3xl font-bold ml-3">Work Sessions</h1>
        </div>
        <div>
        <Tooltip content="Reloads data from disk.">
          <Button className="bg-indigo-500 text-indigo-50 hover:bg-indigo-600 transition-colors" onClick={refreshClick}>Refresh</Button>
        </Tooltip>
        </div>
      </nav>
      <div className="container mx-auto px-2 md:px-0 py-5">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {
            sessions.map((session, i) => (
              <SessionCard key={i} session={session} />
            ))
          }
        </div>
      </div>
    </div>
  );
}

export default App;
