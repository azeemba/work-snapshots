import { useMemo, useState } from "react";
import { useOutletContext } from "react-router-dom";
import { OutletContextInfo } from "../App";
import { displayMinutes } from "../util/time";
import TagBadge from "../components/tagbadge";
import UsageHeatmap, { HeatmapAllData } from "../components/usageheatmap";

export default function TagsPage() {
  // Figure out how to get the data
  const { allSessions, availableTags } = useOutletContext<OutletContextInfo>();
  const [chosenTag, setChosenTag] = useState<string | undefined>(undefined);
  const aggregateDurationByTags = () => {
    const durations: { [key: string]: number } = {};
    for (const session of allSessions) {
      if (session.tag in durations) {
        durations[session.tag] += session.duration_minutes;
      } else {
        durations[session.tag] = session.duration_minutes;
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
    durationrows.push(
      <div key={key} className={classes}>
        <TagBadge
          tag={key}
          availableTags={availableTags}
          onClick={() => toggleTag(key)}
          showClose={chosenTag == key}
        />
        <div>{displayMinutes(duration)}</div>
      </div>
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
      const dontCount = chosenTag !== undefined && session.tag != chosenTag;
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
  }, [allSessions, chosenTag]);

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
