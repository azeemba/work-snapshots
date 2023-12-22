import React from 'react';
import 'tailwindcss/tailwind.css'

function SessionCard({ session }) {
  const startDate = session.display_time;
  let duration = `${session.duration_minutes} minutes`
  if (session.duration_minutes > 60) {
    let hours = session.duration_minutes/60;
    duration = `${hours.toFixed(1)} hours`
  }

  // Function to map the duration to a specific background color class
  const getBackgroundColor = (duration) => {
    if (duration <= 60) {
      return "bg-sky-950/70"
    } else if (duration <= 120) {
      return "bg-sky-950";
    } else if (duration <= 240) {
      return "bg-sky-900";
    } else if (duration <= 480) {
      return "bg-sky-800";
    } else {
      return "bg-sky-700";
    }
  };
  const backgroundColor = getBackgroundColor(session.duration_minutes);


  return (
    <div className={backgroundColor + " cursor-pointer border-4 border-transparent shadow-lg rounded-md overflow-hidden transition-all duration-300 ease-in-out hover:border-indigo-500"}>
      <img className="w-full" src={session.image} alt="Session Preview" />
      <div className="p-4">
        <h2 className="font-bold text-xl mb-1 text-white">{session.title}</h2>
        <p className="text-md text-gray-300 mb-1">{startDate}</p>
        <p className="text-sm text-gray-400">Duration: {duration}</p>
      </div>
    </div>
  );

}

export default SessionCard;