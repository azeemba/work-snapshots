import {
  TransformWrapper,
  TransformComponent,
  MiniMap,
} from "react-zoom-pan-pinch";
import { useInView } from "react-intersection-observer";
import { Modal, Button, Tooltip } from "flowbite-react";
import { Fragment, MouseEvent } from "react";
import { TfiUnlink } from "react-icons/tfi";
import { MdClose } from "react-icons/md";
import ProcessesTable from "./processestable";

type SessionSnapshot = {
  display_time: string;
  image: string;
  processes: Array<{ process: string; title: string; active: boolean }>;
};
type SnapshotCardArgs = {
  session: SessionSnapshot;
  snapshotId: number;
  modalPreview: ModalPreviewArgs;
  triggerModalPreview: (data: ModalPreviewArgs) => void;
  splitSessionAtSnapshot: (snapshotId: number) => void;
};
type ModalPreviewArgs = {
  workSessionId?: number;
  targetUrl?: string;
};

export default function SingleSnapshotCard({
  session,
  snapshotId,
  modalPreview,
  triggerModalPreview,
  splitSessionAtSnapshot,
}: SnapshotCardArgs) {
  const { ref, inView } = useInView({
    triggerOnce: true, // image will load once and won't unload
  });

  function launchImage() {
    const data = { snapshotId, targetUrl: session.image };
    triggerModalPreview(data);
  }

  function handleSplitClicked(ev: MouseEvent) {
    ev.preventDefault();
    splitSessionAtSnapshot(snapshotId);
  }

  const activeProcess = session.processes.find((p) => p.active);

  return (
    <div
      className="p-4 bg-gray-900 rounded shadow-md flex flex-col text-white"
      ref={ref}
    >
      <Modal
        size="7xl"
        dismissible
        show={modalPreview != null}
        onClose={() => triggerModalPreview({})}
      >
        <Modal.Header>{session.display_time}</Modal.Header>
        <Modal.Body>
          <div className="h-[75vh]">
            <TransformWrapper initialScale={2} centerOnInit={true}>
              {({ resetTransform }) => (
                <Fragment>
                  <div
                    style={{
                      position: "fixed",
                      zIndex: 5,
                      top: "75px",
                      right: "50px",
                    }}
                  >
                    <MiniMap width={100}>
                      <img
                        src={modalPreview && modalPreview.targetUrl}
                        alt="Minimap"
                      />{" "}
                    </MiniMap>
                  </div>
                  <TransformComponent
                    wrapperStyle={{
                      maxWidth: "100%",
                      maxHeight: "calc(70vh)",
                      width: "100%",
                      height: "100%",
                    }}
                  >
                    <img
                      src={modalPreview && modalPreview.targetUrl}
                      alt="A zoomable version"
                    />
                  </TransformComponent>
                  <div className="flex flex-row-reverse gap-2 py-2">
                    <Button onClick={() => triggerModalPreview({})}>
                      <MdClose />
                      Close
                    </Button>
                    <Button onClick={() => resetTransform()}>Reset</Button>
                    <Button
                      className="bg-pink-950"
                      onClick={handleSplitClicked}
                    >
                      <TfiUnlink />
                      <div>Split</div>
                    </Button>
                  </div>
                </Fragment>
              )}
            </TransformWrapper>
          </div>
          <ProcessesTable session={session}></ProcessesTable>
        </Modal.Body>
      </Modal>
      <Tooltip content={session.display_time} placement="bottom">
        <div
          className="bg-sky-900 flex-1 border-4 border-transparent rounded-md cursor-pointer transition-all duration-300 ease-in-out hover:border-indigo-500"
          ref={ref}
          onClick={launchImage}
        >
          <div className="w-full aspect-video">
            {inView ? <img src={session.image} alt="Session Detail" /> : null}
          </div>
          <div className="flex flex-row justify-between items-center">
            <p className="text-md text-gray-300">{session.display_time}</p>
            {/* <Button className="mx-2 px-5 flex flex-wrap gap-2 items-center bg-pink-950" size="small" onClick={handleSplitClicked}>
                <TfiUnlink className="mr-2 w-5"/>
                Split
            </Button> */}
          </div>
          <p className="h-6 overflow-hidden">{activeProcess?.title}</p>
        </div>
      </Tooltip>
    </div>
  );
}
