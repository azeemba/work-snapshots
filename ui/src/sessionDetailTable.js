import { Table } from "flowbite-react";

export function SessionDetailTable({ session }) {
  let rest = "divide-y-2 text-white text-base hover:bg-cyan-950";
  let processesTable = session.processes.map((proc, index) => (
    <Table.Row
      key={index}
      className={`${proc.active ? "bg-sky-800" : ""} ${rest}`}
    >
      <Table.Cell>{proc.process}</Table.Cell>
      <Table.Cell>{proc.title}</Table.Cell>
    </Table.Row>
  ));

  return (
    <div className="p-4 w-9/12">
      <h2>{session.display_time}</h2>
      <Table hoverable>
        <Table.Head>
          <Table.HeadCell>Process</Table.HeadCell>
          <Table.HeadCell>Title</Table.HeadCell>
        </Table.Head>
        <Table.Body className="overflow-hidden">{processesTable}</Table.Body>
      </Table>
    </div>
  );
}
