import React, { useState } from "react";
import { useLoaderData, useParams } from "react-router-dom";
import SingleSnapshotCard from "../components/singlesnapshotcard"
import ProcessesTable from "../components/processestable";
import { Carousel, Progress, Button } from "flowbite-react";

export async function loader({ params }: {params: {sessionId: string}}) {
    const sessionId = params.sessionId;
    const details = await fetch(`/api/worksessions/${sessionId}`);
    return details;
}


function WorkSession() {
  const [modalPreviewDetails, requestdModalPreview] = useState({});
  const [activeSessionIndex, changeActiveSessionIndex] = useState(0);
  const details = useLoaderData();
  const timestamps = Object.keys(details);
  const {sessionId} = useParams()

  function handleTriggerModalPreview({ key, targetUrl }) {
    requestdModalPreview({
      timestamp: key,
      targetUrl: targetUrl,
    });
  }
  async function handleSplitClick() {
    const res = await fetch(`/api/worksessions/${sessionId}/split`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        customStartTimestamp: timestamps[activeSessionIndex]
      })
    });
    console.log("Split added. Will refresh instead of being clever.")
    window.location.reload(false);
  }
  const cards = timestamps.map((ts) => (
    <SingleSnapshotCard
      key={ts}
      session={details[ts]}
      timestamp={ts}
      modalPreview={
        modalPreviewDetails.timestamp === ts ? modalPreviewDetails : null
      }
      triggerModalPreview={handleTriggerModalPreview}
    />
  ));
  return (
    <div className="bg-gray-900 min-h-screen text-white flex justify-center flex-col">
      <Carousel
        indicators={false}
        pauseOnHover
        slide={!modalPreviewDetails.timestamp}
        onSlideChange={changeActiveSessionIndex}
      >
        {cards}
      </Carousel>
      <Progress
        progress={(activeSessionIndex / timestamps.length) * 100}
        size="sm"
        color="green"
      ></Progress>
      <Button color="failure" className="w-1/3 m-2" onClick={handleSplitClick}>Split!</Button>
      <ProcessesTable
        session={details[timestamps[activeSessionIndex]]}
      ></ProcessesTable>
    </div>
  );
}

export default WorkSession;
