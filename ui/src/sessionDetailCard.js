import { useState } from 'react';
import { useInView } from 'react-intersection-observer';

export function SessionDetailCard({ session }) {

const { ref, inView } = useInView({
    triggerOnce: true,  // image will load once and won't unload
});

let processesTable;
    processesTable = session.processes.map((proc, index) => (
        <tr key={index}>
            <td>{proc.process}</td>
            <td>{proc.title}</td>
            <td>{proc.active.toString()}</td>
        </tr>
    ));

return (
    <div className="p-4 bg-gray-900 rounded shadow-md flex flex-col md:flex-row text-white" ref={ref}>
       <div className="flex-1">
            {inView ? <img  src={session.image} alt="Session Detail"/> : null}
        </div>
        <div className="flex-1 p-4">
            <h2>{session.display_time}</h2>
            <table>
                <thead>
                    <tr>
                        <th>Process</th>
                        <th>Title</th>
                        <th>Active</th>
                    </tr>
                </thead>
                <tbody>
                    {processesTable}
                </tbody>
            </table>
            </div>
    </div>
)
}