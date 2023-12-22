import React from 'react';
import 'tailwindcss/tailwind.css'

function SessionCard({session}) {
    return (
      <div 
        className="bg-gray-800 border-4 border-transparent shadow-lg rounded-md overflow-hidden transition-all duration-300 ease-in-out hover:border-indigo-500"
      >
        <img className="w-full" src={session.preview} alt="Session Preview" />
        <div className="p-4">
          <h2 className="font-bold text-xl mb-2 text-white">{session.title}</h2>
          <p className="text-sm text-gray-400">{session.dateRange}</p>
        </div>
        <div className="p-4 pt-0 flex justify-end">
          <button className="text-sm font-semibold text-right text-indigo-500 hover:underline">View details</button>
        </div>
      </div>
    );
  }

export default SessionCard;