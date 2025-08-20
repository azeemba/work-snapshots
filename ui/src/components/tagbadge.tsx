import { Badge } from "flowbite-react";
import { MouseEventHandler, useMemo } from "react";
import { IoMdCloseCircle } from "react-icons/io";
import { calculateTagParentMap, TagObject } from "../util/taghelpers";



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
  const tagColors = useMemo(() => {
    const untaggedColor = "bg-gray-100 text-gray-800";
    const colors: { [id: string]: string } = {
      "": untaggedColor,
    };
    const availableColors = [
      "bg-slate-900 text-slate-100",
      "bg-red-900 text-red-100",
      "bg-green-900 text-green-100",
      "bg-amber-900 text-yellow-100",
      "bg-indigo-900 text-indigo-100",
      "bg-lime-800 text-lime-100",
      "bg-rose-900 text-rose-100",
      "bg-purple-900 text-purple-100",
    ];
    availableTags.filter(x => !x.parent).forEach((element, i) => {
      if (element.tag !== "") {
        colors[element.tag] = availableColors[i % availableColors.length];
      }
    });
    return colors;
  }, [availableTags]);

  const tagParentMap = useMemo(() => calculateTagParentMap(availableTags), [availableTags]);

  const clickHandler: MouseEventHandler = (e) => {
    if (onClick) onClick(e);
  };

  return (
    <Badge
      className={
        tagColors[tagParentMap[tag]] +
        " border-2 border-transparent hover:border-slate-500 cursor-pointer"
      }
      size="sm"
      icon={showClose ? IoMdCloseCircle : undefined}
      onClick={clickHandler}
    >
      {tag ? tag : "Untagged"}
    </Badge>
  );
}
