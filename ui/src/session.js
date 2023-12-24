import React, { useState } from 'react';
import { useLoaderData } from "react-router-dom";
import { SessionDetailCard } from './sessionDetailCard';
import { Carousel } from 'flowbite-react';
import 'tailwindcss/tailwind.css'

export async function loader({ params }) {
    const sessionId = params.sessionId;
    const details = await fetch(`/api/worksessions/${sessionId}`);
    return details;
}

function Session() {
    const [modalPreviewDetails, requestdModalPreview] = useState({});
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
        <div className="bg-gray-900 min-h-screen text-white flex justify-center">
            <Carousel pauseOnHover slide={!modalPreviewDetails.timestamp}>
                {cards}
            </Carousel>
        </div>
    )
}

export default Session;