import { TransformWrapper, TransformComponent, MiniMap } from "react-zoom-pan-pinch";
import { useInView } from 'react-intersection-observer';
import { Modal, Button } from "flowbite-react";
import { Fragment } from "react";

export function SessionDetailCard({ session, timestamp, modalPreview, triggerModalPreview }) {

    const { ref, inView } = useInView({
        triggerOnce: true,  // image will load once and won't unload
    });

    let border = "divide-y-2"
    let processesTable = session.processes.map((proc, index) => (
        <tr key={index} className={`${proc.active ? "bg-sky-800" : ""} ${border}`}>
            <td>{proc.process}</td>
            <td>{proc.title}</td>
        </tr>
    ));

    function launchImage(p) {
        console.log(session)
        let data = { key: timestamp, targetUrl: p.target.src }
        console.log("Image clicked", data)
        triggerModalPreview(data)
    }

    return (
        <div className="p-4 bg-gray-900 rounded shadow-md flex flex-col text-white" ref={ref}>
            <Modal size="7xl" dismissible show={modalPreview != null} onClose={() => triggerModalPreview({})}>
                <Modal.Body >
                    <div className="h-[80vh]">
                        <TransformWrapper initialScale={2} centerOnInit={true}>

                            {({ zoomIn, zoomOut, resetTransform, ...rest }) => (
                                <Fragment>
                                    <div style={{
                                        position: "fixed",
                                        zIndex: 5,
                                        top: "75px",
                                        right: "50px",
                                    }}>
                                        <MiniMap width={100}><img src={modalPreview && modalPreview.targetUrl} alt="Minimap" /> </MiniMap>
                                    </div>
                                    <TransformComponent wrapperStyle={{ maxWidth: "100%", maxHeight: "calc(70vh)", width: "100%", height: "100%" }}>
                                        <img src={modalPreview && modalPreview.targetUrl} alt="A zoomable version" />
                                    </TransformComponent>
                                    <div className="flex flex-row space-x-3">
                                        <Button onClick={() => resetTransform()}>Reset</Button>
                                        <Button onClick={() => triggerModalPreview({})}>Close</Button>
                                    </div>

                                </Fragment>
                            )}
                        </TransformWrapper>
                    </div>
                </Modal.Body>
            </Modal>
            <div className="flex-1">
                {inView ? (<img src={session.image} alt="Session Detail" onClick={launchImage} />) : null}
            </div>
            <div className="flex-1 p-4">
                <h2>{session.display_time}</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Process</th>
                            <th>Title</th>
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