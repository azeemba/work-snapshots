import React, { useState } from "react";
import { useInView } from "react-intersection-observer";
import "tailwindcss/tailwind.css";
import { FaCheck, FaPencilAlt, FaPlus } from "react-icons/fa";
import { FaXmark } from "react-icons/fa6";
import { Link } from "react-router-dom";
import { Button, Badge } from "flowbite-react";

function SessionCard({ session }) {
  const [inEditMode, setEditMode] = useState(false);
  const { ref, inView } = useInView({
    triggerOnce: true,
  });

  // Get available tags?
  const availableTags = [{ name: "Ump Show" }, { name: "WorkSnapshots" }]
  const tagDropdown = (
    <div className="flex flex-row h-8">
      <select
        id="countries"
        className="bg-gray-50 border border-gray-300 text-gray-900 text-xs rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-2"
        onClick={ev => ev.preventDefault()}
      >
        {availableTags.map((t) => <option key={t.name}>{t.name}</option>)}
      </select>
    </div>
  )


  const startDate = session.display_time;
  let duration = `${session.duration_minutes} minutes`;
  if (session.duration_minutes > 60) {
    let hours = session.duration_minutes / 60;
    duration = `${hours.toFixed(1)} hours`;
  }
  const link = `session/${session.id}`;

  // Function to map the duration to a specific background color class
  const getBackgroundColor = (duration) => {
    if (duration <= 60) {
      return "bg-sky-950/70";
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

  const editButtonClicked = (ev) => {
    ev.preventDefault();
    setEditMode(true);
  };
  const saveButtonClicked = (ev) => {
    ev.preventDefault();
    setEditMode(false);
  }
  const noSaveClicked = (ev) => {
    ev.preventDefault();
    setEditMode(false);
  }

  return (
    <Link to={link}>
      <div
        className={
          backgroundColor +
          " cursor-pointer border-4 border-transparent shadow-lg rounded-md overflow-hidden transition-all duration-300 ease-in-out hover:border-indigo-500"
        }
        ref={ref}
      >
        {inView ? (
          <img className="w-full" src={session.image} alt="Session Preview" />
        ) : null}
        <div className="p-4">
          <h2 className="font-bold text-xl mb-1 text-white">{session.title}</h2>
          <p className="text-md text-gray-300 mb-1">{startDate}</p>
          <p className="text-sm text-gray-400">Duration: {duration}</p>
          <div className="flex flex-row justify-between py-2">
            {inEditMode ? tagDropdown :
              <div className="h-8">
                {session.tag ?
                  <Badge>session.tag.name</Badge> : <Badge color="gray">Untagged</Badge>
                }
              </div>
            }
            {
              inEditMode ?
                <div className="flex flex-row gap-4">
                  <Button
                    size="sm"
                    color="green"
                    onClick={saveButtonClicked} >
                    <FaCheck />
                  </Button>
                  <Button
                    size="sm"
                    color="red"
                    onClick={noSaveClicked} >
                    <FaXmark />
                  </Button>
                </div>
                :

                <Button
                  size="sm"
                  className="bg-indigo-800 text-indigo-50 transition-all enabled:hover:bg-indigo-500"
                  onClick={editButtonClicked}
                >
                  <FaPencilAlt />
                </Button>
            }
          </div>
        </div>
      </div>
    </Link>
  );
}

export default SessionCard;
