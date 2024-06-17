import { FormEvent, MouseEvent, useState } from "react";
import { useInView } from "react-intersection-observer";
import "tailwindcss/tailwind.css";
import { FaCheck, FaPencilAlt } from "react-icons/fa";
import { FaXmark } from "react-icons/fa6";
import { Link } from "react-router-dom";
import { Button, TextInput } from "flowbite-react";
import TagBadge, { TagObject } from "./tagbadge";
import { displayMinutes } from "../util/time";

export type Session = {
  id: number;
  start: number;
  end: number;
  display_time: string;
  duration_minutes: number;
  title: string;
  tag: string;
  image: string;
};

type SessionSummaryCardArgs = {
  session: Session;
  availableTags: Array<TagObject>;
  onEdit: (data: { id: number; title: string; tag: string }) => void;
  onTagClick: (data: { tag: string }) => void;
};

function SessionSummaryCard({
  session,
  availableTags,
  onEdit,
  onTagClick,
}: SessionSummaryCardArgs) {
  const [inEditMode, setEditMode] = useState(false);
  const [editedTitle, setEditedTitle] = useState(session.title);
  const [editedTag, setEditedTag] = useState(session.tag);
  const { ref, inView } = useInView({
    triggerOnce: true,
  });

  // Get available tags?
  const tagDropdown = (
    <div className="flex flex-row h-8">
      <select
        id="countries"
        className="bg-gray-50 border border-gray-300 text-gray-900 text-xs rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-2"
        value={editedTag}
        onClick={(e) => e.preventDefault()}
        onChange={(e) => setEditedTag(e.target.value)}
      >
        <option key="empty" value="">
          None
        </option>
        {availableTags.map((t) => (
          <option key={t.tag} value={t.tag}>
            {t.tag}
          </option>
        ))}
      </select>
    </div>
  );

  const startDate = session.display_time;
  const duration = displayMinutes(session.duration_minutes);
  const link = `session/${session.id}`;

  // Function to map the duration to a specific background color class
  const getBackgroundColor = (duration: number) => {
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

  const editButtonClicked = (ev: MouseEvent) => {
    ev.preventDefault();
    setEditMode(true);
  };
  const saveButtonClicked = (ev: MouseEvent) => {
    ev.preventDefault();
    console.log("Will add override", editedTitle, editedTag);
    setEditMode(false);
    onEdit({ id: session.id, title: editedTitle, tag: editedTag });
  };
  const noSaveClicked = (ev: MouseEvent) => {
    ev.preventDefault();
    setEditMode(false);
  };

  return (
    <Link to={link}>
        <div
          className={
            backgroundColor +
            " cursor-pointer border-4 border-transparent shadow-lg rounded-md overflow-hidden transition-all duration-300 ease-in-out hover:border-indigo-500"
          }
          ref={ref}
        >
          <div className="w-full aspect-video">
            {inView ? (
              <img
                className="w-full"
                src={session.image}
                alt="Session Preview"
              />
            ) : null}
          </div>
          <div className="p-4">
            <div className="h-14 overflow-hidden">
              {inEditMode ? (
                <TextInput
                  onClick={(e) => e.preventDefault()}
                  value={editedTitle}
                  onInput={(e: FormEvent<HTMLInputElement>) =>
                    setEditedTitle((e.target as HTMLInputElement).value)
                  }
                ></TextInput>
              ) : (
                <h2 className="font-bold text-xl mb-1 text-white">
                  {session.title}
                </h2>
              )}
            </div>
            <p className="text-md text-gray-300 mb-1">{startDate}</p>
            <p className="text-sm text-gray-400">Active: {duration}</p>
            <div className="flex flex-row justify-between py-2">
              {inEditMode ? (
                tagDropdown
              ) : (
                <div className="h-8">
                  <TagBadge
                    availableTags={availableTags}
                    tag={session.tag}
                    onClick={(ev) => {
                      ev.preventDefault();
                      onTagClick({ tag: session.tag });
                    }}
                  />
                </div>
              )}
              {inEditMode ? (
                <div className="flex flex-row gap-4">
                  <Button size="sm" color="green" onClick={saveButtonClicked}>
                    <FaCheck />
                  </Button>
                  <Button size="sm" color="red" onClick={noSaveClicked}>
                    <FaXmark />
                  </Button>
                </div>
              ) : (
                <Button
                  size="sm"
                  className="bg-indigo-800 text-indigo-50 transition-all enabled:hover:bg-indigo-500"
                  onClick={editButtonClicked}
                >
                  <FaPencilAlt />
                </Button>
              )}
            </div>
          </div>
        </div>
    </Link>
  );
}

export default SessionSummaryCard;
