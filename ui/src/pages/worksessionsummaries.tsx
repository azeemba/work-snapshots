import { FormEvent, useEffect, useState } from "react";
import { FaPlus } from "react-icons/fa";
import { Button, TextInput } from "flowbite-react";
import { Session } from "../components/sessionsummarycard";

export async function loader({ params }: { params: { sessionId: string } }) {
  const sessionId = params.sessionId;
  const details = await fetch(`/api/worksessions/${sessionId}`);
  return details;
}

import SessionSummaryCard from "../components/sessionsummarycard";
import TagBadge, { TagObject } from "../components/tagbadge";

export default function WorkSessionsSummaries() {
  const [allSessions, setAllSessions] = useState<Array<Session>>([]);
  const [selectedTag, setSelectedTag] = useState<string | undefined>(undefined);
  const [availableTags, setAvailableTags] = useState<Array<TagObject>>([]);

  const [shouldShowAddTags, setShowAddTags] = useState(false);
  const [newTagValue, setNewTagValue] = useState("");

  useEffect(() => {
    fetch("/api/worksessions")
      .then((response) => response.json())
      .then((data) => {
        setAllSessions(data);
      });
    fetch("/api/tags")
      .then((response) => response.json())
      .then((data) => setAvailableTags(data.tags));
  }, []);

  const handleEdit = ({
    id,
    title,
    tag,
  }: {
    id: number;
    title: string;
    tag: string;
  }) => {
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
        setAllSessions(resp);
      });
  };

  const addNewTag = () => {
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

  const tagClick = ({ tag }: { tag: string }) => {
    setSelectedTag(tag);
  };

  return (
    <div className="container mx-auto px-2 md:px-0 py-5">
      <div className="h-10 my-2">
        <div className="flex flex-row justify-between">
          {shouldShowAddTags ? (
            <div className="flex flex-row gap-1">
              <TextInput
                defaultValue={newTagValue}
                onInput={(e: FormEvent) =>
                  setNewTagValue((e.target as HTMLInputElement).value)
                }
              ></TextInput>
              <Button onClick={addNewTag}>Add Tag</Button>
              <Button color="dark" onClick={() => setShowAddTags(false)}>
                Cancel
              </Button>
            </div>
          ) : (
            <Button onClick={() => setShowAddTags(true)}>
              <FaPlus />
            </Button>
          )}
          {selectedTag !== undefined ? (
            <TagBadge
              availableTags={availableTags}
              tag={selectedTag}
              showClose={true}
              onClick={() => setSelectedTag(undefined)}
            />
          ) : undefined}
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {allSessions
          .filter((s) => !selectedTag || s.tag === selectedTag)
          .map((session, i) => (
            <SessionSummaryCard
              key={i}
              session={session}
              availableTags={availableTags}
              onEdit={handleEdit}
              onTagClick={tagClick}
            />
          ))}
      </div>
    </div>
  );
}
