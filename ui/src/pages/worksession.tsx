import { useState } from "react";
import { useLoaderData, useParams } from "react-router-dom";
import SingleSnapshotCard, {
  ModalPreviewArgs,
  SessionSnapshot,
} from "../components/singlesnapshotcard";
import { Session } from "../components/sessionsummarycard";

export async function loader({ params }: { params: { sessionId: string } }) {
  const sessionId = params.sessionId;
  const resp = await fetch(`/api/worksessions/${sessionId}`);
  const data = await resp.json();
  return data;
}

type SessionDetails = {
  [id: number]: SessionSnapshot;
};
type LoadedData = {
  session: Session;
  details: SessionDetails;
};

function WorkSession() {
  const [modalPreviewDetails, requestdModalPreview] =
    useState<ModalPreviewArgs>({});
  const { session, details } = useLoaderData() as LoadedData;
  const timestamps = Object.keys(details) as unknown as Array<number>;
  const { sessionId } = useParams();

  function handleTriggerModalPreview({
    snapshotId,
    targetUrl,
  }: ModalPreviewArgs) {
    requestdModalPreview({
      snapshotId,
      targetUrl: targetUrl,
    });
  }
  async function handleSplitClick(snapshotId: number) {
    await fetch(`/api/worksessions/${sessionId}/split`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        customStartTimestamp: snapshotId,
      }),
    });
    console.log("Split added. Will refresh instead of being clever.");
    window.location.reload();
  }
  const cards = timestamps.map((ts) => (
    <SingleSnapshotCard
      key={ts}
      session={details[ts]}
      snapshotId={ts}
      modalPreview={
        modalPreviewDetails.snapshotId === ts ? modalPreviewDetails : undefined
      }
      triggerModalPreview={handleTriggerModalPreview}
      splitSessionAtSnapshot={handleSplitClick}
    />
  ));
  return (
    <div className="bg-gray-900 min-h-screen text-white flex justify-center flex-col">
      <h1 className="text-2xl ml-3">{session.title}</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        {cards}
      </div>
    </div>
  );
}

export default WorkSession;
