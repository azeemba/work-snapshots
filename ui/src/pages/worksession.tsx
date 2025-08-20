import { KeyboardEvent, useState } from "react";
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
    window.location.reload();
  }
  function makeNext(ts: number) {
    const i = timestamps.indexOf(ts);
    if (i + 1 >= timestamps.length) return {};
    const target = timestamps[i + 1];
    const image = details[target].image;
    return { snapshotId: target, targetUrl: image };
  }
  function makePrev(ts: number) {
    const i = timestamps.indexOf(ts);
    if (i <= 0) return {};
    const target = timestamps[i - 1];
    const image = details[target].image;
    return { snapshotId: target, targetUrl: image };
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
      neighbors={{
        prev: makePrev(ts),
        next: makeNext(ts),
      }}
    />
  ));
  function handleKeyPress(ev: KeyboardEvent) {
    if (modalPreviewDetails.snapshotId) {
      // We have a modal view up
      if (ev.key == "ArrowRight") {
        handleTriggerModalPreview(makeNext(modalPreviewDetails.snapshotId));
      } else if (ev.key == "ArrowLeft") {
        handleTriggerModalPreview(makePrev(modalPreviewDetails.snapshotId));
      }
    }
  }
  return (
    <div
      className="bg-gray-900 min-h-screen text-white flex justify-center flex-col"
      onKeyDown={handleKeyPress}
    >
      <h1 className="text-2xl ml-3">{session.title}</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        {cards}
      </div>
    </div>
  );
}

export default WorkSession;
