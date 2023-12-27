import React, { useEffect, useState } from "react";
import { FaPlus } from "react-icons/fa";
import { Button, TextInput } from "flowbite-react";

import SessionCard from "./sessionCard";

export default function WorkSessionsSummary() {
  const [sessions, setSessions] = useState([]);
  const [availableTags, setAvailableTags] = useState([]);

  const [shouldShowAddTags, setShowAddTags] = useState(false);
  const [newTagValue, setNewTagValue] = useState("");

  useEffect(() => {
    fetch("/api/worksessions")
      .then((response) => response.json())
      .then((data) => setSessions(data));
    fetch("/api/tags")
      .then((response) => response.json())
      .then((data) => setAvailableTags(data.tags));
  }, []);

  const handleEdit = ({ id, title, tag }) => {
    fetch(`/api/worksessions/${id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: title,
        tag: tag,
      }),
    })
      .then((resp) => resp.json())
      .then((resp) => {
        setSessions(resp);
      });
  };

  const addNewTag = (ev) => {
    fetch(`/api/tags/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        tag: newTagValue,
      }),
    })
      .then((resp) => resp.json())
      .then((resp) => setAvailableTags(resp.tags))
      .then(() => {
        setShowAddTags(false);
      });
  };

  return (
    <div className="container mx-auto px-2 md:px-0 py-5">
      <div className="h-10 my-2">
        {shouldShowAddTags ? (
          <div className="flex flex-row">
            <TextInput
              defaultValue={newTagValue}
              onInput={(e) => setNewTagValue(e.target.value)}
            ></TextInput>
            <Button onClick={addNewTag}>Add Tag</Button>
          </div>
        ) : (
          <Button onClick={(e) => setShowAddTags(true)}>
            <FaPlus />
          </Button>
        )}
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {sessions.map((session, i) => (
          <SessionCard
            key={i}
            session={session}
            availableTags={availableTags}
            onEdit={handleEdit}
          />
        ))}
      </div>
    </div>
  );
}
