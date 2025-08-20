import { FormEvent, useState, useMemo } from "react";
import { FaPlus } from "react-icons/fa";
import { Button, TextInput } from "flowbite-react";
import { useOutletContext } from "react-router-dom";

import SessionSummaryCard from "../components/sessionsummarycard";
import TagBadge from "../components/tagbadge";
import { OutletContextInfo } from "../App";
import { calculateTagParentMap } from "../util/taghelpers";

export default function WorkSessionsSummaries() {
  const { allSessions, setAllSessions, availableTags, setAvailableTags } =
    useOutletContext<OutletContextInfo>();
  const [selectedTag, setSelectedTag] = useState<string | undefined>(undefined);

  const [shouldShowAddTags, setShowAddTags] = useState(false);
  const [newTagValue, setNewTagValue] = useState("");

  // Memoize expensive calculations
  const tagParentMap = useMemo(() => calculateTagParentMap(availableTags), [availableTags]);
  
  const filteredTags = useMemo(() => 
    availableTags
      .filter((t) => selectedTag === undefined || tagParentMap[t.tag] === selectedTag)
      .filter(t => !t.parent),
    [availableTags, selectedTag, tagParentMap]
  );

  const filteredSessions = useMemo(() =>
    allSessions.filter((s) => selectedTag === undefined || tagParentMap[s.tag] === selectedTag),
    [allSessions, selectedTag, tagParentMap]
  );

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
      .then((resp) => {
        if (!resp.ok) throw new Error('Failed to update session');
        return resp.json();
      })
      .then((resp) => {
        setAllSessions(resp);
      })
      .catch((err) => {
        console.error('Failed to update session:', err);
        // Optionally show error to user
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
      .then((resp) => {
        if (!resp.ok) throw new Error('Failed to add tag');
        return resp.json();
      })
      .then((resp) => {
        const tags = resp.tags;
        tags.push({ tag: "" });
        setAvailableTags(tags);
        setShowAddTags(false);
        setNewTagValue("");
      })
      .catch((err) => {
        console.error('Failed to add tag:', err);
        // Optionally show error to user
      });
  };

  const tagClick = ({ tag }: { tag: string }) => {
    if (selectedTag === tag) {
      setSelectedTag(undefined);
    } else {
      setSelectedTag(tag);
    }
  };

  return (
    <div className="container mx-auto px-2 md:px-0 py-5">
      <div className="my-2">
        <div className="flex flex-row flex-wrap justify-between">
          {shouldShowAddTags ? (
            <div className="flex flex-row gap-2">
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
          <div className="flex flex-row flex-wrap gap-2">
            {filteredTags.map((t) => {
                return (
                  <TagBadge
                    key={t.tag}
                    availableTags={availableTags}
                    tag={t.tag}
                    showClose={selectedTag === t.tag}
                    onClick={() => tagClick(t)}
                  />
                );
              })}
          </div>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredSessions.map((session) => (
            <SessionSummaryCard
              key={session.id}
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
