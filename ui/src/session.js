import React, { useState } from 'react';
import { useLoaderData } from "react-router-dom";
import { SessionDetailCard } from './sessionDetailCard';
import { SessionDetailTable } from './sessionDetailTable';
import { Carousel, Progress } from 'flowbite-react';
import 'tailwindcss/tailwind.css'

export async function loader({ params }) {
    const sessionId = params.sessionId;
    const details = await fetch(`/api/worksessions/${sessionId}`);
    return details;
}

function Session() {
    const [modalPreviewDetails, requestdModalPreview] = useState({});
    const [activeSessionIndex, changeActiveSessionIndex] = useState(0)
    const details = useLoaderData();
    const timestamps = Object.keys(details)

    function handleTriggerModalPreview({ key, targetUrl }) {
        requestdModalPreview({
            timestamp: key,
            targetUrl: targetUrl
        })
    }
    const cards = timestamps.map(ts => (
        <SessionDetailCard key={ts}
            session={details[ts]}
            timestamp={ts}
            modalPreview={modalPreviewDetails.timestamp === ts ? modalPreviewDetails : null}
            triggerModalPreview={handleTriggerModalPreview}
        />
    ))
    return (
        <div className="bg-gray-900 min-h-screen text-white flex justify-center flex-col">
            <Carousel
                indicators={false}
                pauseOnHover
                slide={!modalPreviewDetails.timestamp}
                onSlideChange={changeActiveSessionIndex}>
                {cards}
            </Carousel>
            <Progress progress={activeSessionIndex / timestamps.length * 100} size="sm" color="green"></Progress>
            <SessionDetailTable session={details[timestamps[activeSessionIndex]]}></SessionDetailTable>
        </div>
    )
}

export default Session;