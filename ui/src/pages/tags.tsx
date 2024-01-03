import { useOutletContext } from "react-router-dom";
import { OutletContextInfo } from "../App";
import { displayMinutes } from "../util/time";
import TagBadge from "../components/tagbadge";

export default function TagsPage() {
  // Figure out how to get the data
  const { allSessions, availableTags } = useOutletContext<OutletContextInfo>();
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

  for (const { key, duration } of durationPairs) {
    durationrows.push(
      <div
        key={key}
        className="flex flex-row flex-wrap gap-2 w-full max-w-lg justify-between pt-4"
      >
        <TagBadge tag={key} availableTags={availableTags} />
        <div>{displayMinutes(duration)}</div>
      </div>,
    );
  }

  // What we want to show?

  // Time spent on each tag in total
  // Time spent on each tag in time period
  // Time spent changing over time

  return (
    <div className="container mx-auto px-2 py-5">
      <div className="flex flex-col content-center gap-3 divide-y">
        {durationrows}
      </div>
    </div>
  );
}
