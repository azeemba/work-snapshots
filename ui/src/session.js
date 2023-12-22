import React from 'react';
import { useLoaderData } from "react-router-dom";
import { SessionDetailCard } from './sessionDetailCard';
import 'tailwindcss/tailwind.css'

export async function loader({ params }) {
    const sessionId = params.sessionId;
    const details = await fetch(`/api/worksessions/${sessionId}`);
    return details;
}

function Session() {
    const details = useLoaderData();
    const timestamps = Object.keys(details)

    const cards = timestamps.map(ts => (
        <SessionDetailCard key={ts} session={details[ts]} />
    ))
    return (
    <div className="bg-gray-900 min-h-screen text-white flex justify-center">
        <div className="container flex flex-wrap">
        {cards}
        </div>
    </div>
    )
}

export default Session;