import { Badge } from "flowbite-react";
import { MouseEventHandler } from "react";
import { IoMdCloseCircle } from "react-icons/io";

export type TagObject = {
  tag: string;
};

export default function TagBadge({
  availableTags,
  tag,
  onClick,
  showClose,
}: {
  availableTags: Array<TagObject>;
  tag: string;
  onClick?: MouseEventHandler;
  showClose?: boolean;
}) {
  const tagColors: { [id: string]: string } = {};
  const availableColors = [
    "bg-slate-900 text-slate-100",
    "bg-red-900 text-red-100",
    "bg-green-900 text-green-100",
    "bg-orange-900 text-orange-100",
    "bg-indigo-900 text-indigo-100",
    "bg-yellow-900 text-yellow-100",
    "bg-rose-900 text-rose-100",
    "bg-lime-700 text-lime-100",
    "bg-purple-900 text-purple-100",
  ];
  availableTags.forEach((element, i) => {
    tagColors[element.tag] = availableColors[i % availableColors.length];
  });

  const clickHandler: MouseEventHandler = (e) => {
    if (onClick) onClick(e);
  };

  return tag ? (
    <Badge
      className={
        tagColors[tag] +
        " border-2 border-transparent hover:border-slate-500 cursor-pointer"
      }
      size="sm"
      icon={showClose ? IoMdCloseCircle : undefined}
      onClick={onClick}
    >
      {tag}
    </Badge>
  ) : (
    <Badge color="gray" size="sm" onClick={clickHandler}>
      Untagged
    </Badge>
  );
}
