import { useMemo, useState } from "react";
import { useOutletContext } from "react-router-dom";
import { OutletContextInfo } from "../App";
import { displayMinutes } from "../util/time";
import TagBadge from "../components/tagbadge";
import UsageHeatmap, { HeatmapAllData } from "../components/usageheatmap";
import { calculateTagParentMap } from "../util/taghelpers";

export default function TagsPage() {
  // Figure out how to get the data
  const { allSessions, availableTags, setAvailableTags } = useOutletContext<OutletContextInfo>();
  const [chosenTag, setChosenTag] = useState<string | undefined>(undefined);
  const [addParentFor, setAddChildFor] = useState<string | null>(null);
  const [selectedChild, setSelectedChild] = useState<string | null>(null);

  const tagParentMap: { [key: string]: string } = calculateTagParentMap(availableTags);

  const aggregateDurationByTags = () => {
    const durations: { [key: string]: number } = {};
    for (const session of allSessions) {
      const key = tagParentMap[session.tag];
      if (key in durations) {
        durations[key] += session.duration_minutes;
      } else {
        durations[key] = session.duration_minutes;
      }
    }
    // Add tags taht don't have a parent and have 0 data
    // so they can get more children
    for (const tag of availableTags) {
      if (!(tag.parent || tag.tag in durations))
      {
        durations[tag.tag] = 0
      }
    }
    return durations;
  };
  const durations = aggregateDurationByTags();
  const durationrows = [];
  const durationPairs = [];
  for (const [key, duration] of Object.entries(durations)) {
    durationPairs.push({ key, duration });
  }
  durationPairs.sort((a, b) => b.duration - a.duration);

  function toggleTag(clickedTag: string) {
    if (clickedTag == chosenTag) {
      setChosenTag(undefined);
    } else {
      setChosenTag(clickedTag);
    }
  }

  for (const { key, duration } of durationPairs) {
    let classes =
      "flex flex-row flex-wrap gap-2 w-full max-w-lg justify-between pt-4";
    if (chosenTag == key) {
      classes += " bg-slate-700";
    }
    const children = availableTags.filter(x => x.parent == key).map(x => <TagBadge tag={x.tag} availableTags={availableTags}></TagBadge>);

    // "+" button and parent selection UI
    const showAddChild = addParentFor === key;
    const otherTags = availableTags.filter(t => t.tag !== key);

    durationrows.push(
      <div key={key} className={classes}>
        <TagBadge
          tag={key}
          availableTags={availableTags}
          onClick={() => toggleTag(key)}
          showClose={chosenTag == key}
        />
        <button
          className="ml-2 px-2 py-1 rounded bg-blue-600 text-white"
          onClick={() => {
            setAddChildFor(key);
            setSelectedChild(null);
          }}
          title="Add parent tag"
        >+</button>
        {showAddChild && (
          <span className="flex flex-row items-center gap-2 ml-2">
            <select
              value={selectedChild ?? ""}
              onChange={e => setSelectedChild(e.target.value)}
              className="border rounded px-1 py-0.5 text-black"
            >
              {otherTags.filter(t => t.parent != key).filter(t => t.tag).map(t =>
                <option key={t.tag} value={t.tag} selected={selectedChild == t.tag}>{t.tag}</option>
              )}
            </select>
            <button
              className="px-2 py-1 rounded bg-green-600 text-white"
              disabled={!selectedChild}
              onClick={async () => {
                if (!selectedChild) return;
                // Send request to add parent/child relationship
                console.log(JSON.stringify({ parent: key, tag: selectedChild }))
                const response = await fetch("/api/tags", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ parent: key, tag: selectedChild }),
                });
                setAddChildFor(null);
                setSelectedChild(null);
                // Optionally: refresh tags from server here
                const tags = (await response.json()).tags;
                tags.push({"tag": ""})
                setAvailableTags(tags);
              }}
              title="Confirm"
            >✔</button>
            <button
              className="px-2 py-1 rounded bg-gray-400 text-white"
              onClick={() => {
                setAddChildFor(null);
                setSelectedChild(null);
              }}
              title="Cancel"
            >✕</button>
          </span>
        )}
        {children}
        <div>{displayMinutes(duration)}</div>
      </div>,
    );
  }

  function getSundayForThatWeek(orig: Date) {
    const clone = new Date(orig);
    const day = orig.getDay();
    clone.setDate(clone.getDate() - day);
    clone.setHours(0, 0, 0, 0);
    return clone.getTime();
  }

  const heatmapData = useMemo(() => {
    const dayWeekCount: HeatmapAllData = [];
    for (let i = 0; i < 7; ++i) dayWeekCount.push({});

    for (const session of allSessions) {
      const dontCount = chosenTag !== undefined && tagParentMap[session.tag] != chosenTag;
      const start = new Date(session.start * 1000);
      const dayIndex = start.getDay();
      const week = getSundayForThatWeek(start);

      const curDay = dayWeekCount.at(dayIndex);
      if (curDay === undefined) {
        console.log("Magical day? Can't continue.", session);
        continue;
      }

      if (dontCount) {
        // Don't aggregate but add a 0 field so that
        // the calendar doesn't shift when tags are changed
        if (curDay[week] == undefined) curDay[week] = 0;
      } else if (curDay[week]) {
        curDay[week] += session.duration_minutes;
      } else {
        curDay[week] = session.duration_minutes;
      }
    }
    return dayWeekCount;
  }, [allSessions, chosenTag, tagParentMap]);

  // What we want to show?

  // Time spent on each tag in total
  // Time spent on each tag in time period
  // Time spent changing over time

  let chartTitle = "Hours Spent";
  if (chosenTag) {
    chartTitle += " on " + chosenTag;
  }

  return (
    <div className="container mx-auto px-2 py-5">
      <UsageHeatmap dayWeekMap={heatmapData} title={chartTitle} />
      <div className="flex flex-col divide-y content-center gap-3">
        {durationrows}
      </div>
    </div>
  );
}
