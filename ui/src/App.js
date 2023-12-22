import React, { useEffect, useState } from 'react';
import 'tailwindcss/tailwind.css'

import SessionCard from './session';


function App() {
  /*
    const sessions = [
    {
      preview: 'preview1.jpg',
      title: 'Visual Studio Code Session',
      dateRange: 'Dec 09, 2023, 20:07 - 21:07',
    },
    {
      preview: 'preview2.jpg',
      title: 'Firefox Session',
      dateRange: 'Dec 10, 2023, 10:00 - 11:00',
    },
    //...add more sessions as needed
  ];
  */
  const [sessions, setSessions] = useState([]);
  useEffect(() => {
    fetch("/api/worksessions").then(response => response.json()).then(data => setSessions(data))
  }, [])

  return (
    <div className="bg-gradient-to-r from-gray-800 to-gray-900 min-h-screen text-white">
      <nav className="bg-gradient-to-r from-gray-700 to-gray-800 px-4 py-2 flex justify-between items-center">
        <div className="flex justify-between items-center">
          <div></div>
          <h1 className="text-3xl font-bold ml-3">Work Sessions</h1>
        </div>
        <div>
          <button className="px-4 py-2 rounded-md bg-indigo-500 text-indigo-50 hover:bg-indigo-600 transition-colors">Navigation Link</button>
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
