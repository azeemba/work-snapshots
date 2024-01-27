import Chart from "react-apexcharts";

export type HeatmapPerDayOfWeek = {
  [weekStart: number | string]: number;
};
export type HeatmapAllData = Array<HeatmapPerDayOfWeek>;

export default function UsageHeatmap({
  title,
  dayWeekMap,
}: {
  title: string;
  dayWeekMap: HeatmapAllData;
}) {
  const dayNames = ["S", "M", "Tu", "W", "Th", "F", "S"];
  const allUniqueDates = new Set(
    dayWeekMap.map((weeks) => Object.keys(weeks)).flat()
  );

  const series = dayWeekMap
    .map((weeks, i) => {
      for (const d of allUniqueDates) {
        if (weeks[d] === undefined) {
          weeks[d] = 0;
        }
      }
      return {
        name: dayNames[i],
        index: i,
        data: Object.keys(weeks)
          .map((weekStart) => {
            const label = new Date(Number(weekStart)).toLocaleDateString();
            return {
              x: label,
              y: Math.round(weeks[weekStart] / 6) / 10,
              o: Number(weekStart),
            };
          })
          .sort((a, b) => a.o - b.o),
      };
    })
    .sort((a, b) => b.index - a.index);

  const options = {
    chart: {
      height: 350,
      toolbar: { show: false },
      foreColor: "#fff",
      background: "#151d2c",
    },
    tooltip: { theme: "dark" },
    plotOptions: {
      heatmap: {
        colorScale: { min: 0, max: 8 },
        shadeIntensity: 0.5,
        radius: 2,
        useFillColorAsStroke: true,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      width: 1,
    },
    title: {
      text: title,
    },
    colors: ["#15909c"],
    xaxis: {
      labels: { rotate: 0 },
    },
  };

  return (
    <div className="h-[220px] md:h-[300px] lg:h-[400px] w-full">
      <Chart type="heatmap" options={options} series={series} height="100%" />
    </div>
  );
}
