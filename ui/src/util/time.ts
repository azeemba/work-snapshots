export function displayMinutes(minutes: number) {
  let duration = `${minutes} minutes`;
  if (minutes > 60) {
    const hours = minutes / 60;
    duration = `${hours.toFixed(1)} hours`;
  }
  return duration;
}
