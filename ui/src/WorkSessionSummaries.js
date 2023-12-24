import React, { useEffect, useState } from "react";

import SessionCard from "./sessionCard";

export default function WorkSessionsSummary() {
  const [sessions, setSessions] = useState([]);
  useEffect(() => {
    fetch("/api/worksessions")
      .then((response) => response.json())
      .then((data) => setSessions(data));
  }, []);

  return (
    <div className="container mx-auto px-2 md:px-0 py-5">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {sessions.map((session, i) => (
          <SessionCard key={i} session={session} />
        ))}
      </div>
    </div>
  );
}
