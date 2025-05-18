
export type TagObject = {
  tag: string;
  parent: string | undefined
};

export function calculateTagParentMap(availableTags: Array<TagObject>)
{
  const tagParentMap: { [key: string]: string } = availableTags.reduce((mapped, curTag) => {
    if (curTag.parent) {
      mapped[curTag.tag] = curTag.parent;
    } else {
      mapped[curTag.tag] = curTag.tag;
    }
    return mapped;
  }, {} as { [key: string]: string });
  tagParentMap[""] = "";

  return tagParentMap;
}