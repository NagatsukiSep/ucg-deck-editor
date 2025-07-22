import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import React from "react";

type DeckAnalysis = {
  [name: string]:
    | {
        [level: string]: number;
      }
    | number;
};

type Props = {
  analysis: DeckAnalysis;
};

const HeroLevelBarChartAbsolute: React.FC<Props> = ({ analysis }) => {
  const chartData: { name: string; [level: string]: number | string }[] = [];
  let maxTotal = 0;

  Object.entries(analysis).forEach(([name, value]) => {
    if (typeof value === "number") {
      chartData.push({ name, シーン: value });
      maxTotal = Math.max(maxTotal, value);
      return;
    }

    const total = Object.values(value).reduce((sum, n) => sum + n, 0);
    maxTotal = Math.max(maxTotal, total);

    const entry: { name: string; [level: string]: number | string } = { name };
    for (const [level, count] of Object.entries(value)) {
      entry[level] = count;
    }
    chartData.push(entry);
  });

  chartData.sort((a, b) => {
    const isAScene = a.name === "シーン";
    const isBScene = b.name === "シーン";
    if (isAScene && !isBScene) return 1;
    if (!isAScene && isBScene) return -1;

    const totalA = Object.entries(a)
      .filter(([k]) => k !== "name")
      .reduce((sum, [, v]) => sum + (typeof v === "number" ? v : 0), 0);
    const totalB = Object.entries(b)
      .filter(([k]) => k !== "name")
      .reduce((sum, [, v]) => sum + (typeof v === "number" ? v : 0), 0);
    return totalB - totalA;
  });

  const levelKeys = new Set<string>();
  chartData.forEach((row) => {
    Object.keys(row).forEach((k) => {
      if (k !== "name") levelKeys.add(k);
    });
  });

  const sortedLevels = Array.from(levelKeys).sort();

  const levelColors: Record<string, string> = {
    "1": "#AEDFF7", // ヒーローLv1: パステルブルー（軽く爽やか）→ #AEDFF7
    "2": "#7FC8F8", // ヒーローLv2: スカイブルー（少し濃く）→ #7FC8F8
    "3": "#3DA9FC", // ヒーローLv3: 鮮やかなブルー（芯のある強さ）→ #3DA9FC

    "4": "#F4A261", // 怪獣Lv4: ソフトなオレンジ（軽めの怪獣）→ #F4A261
    "5": "#E76F51", // 怪獣Lv5: 赤みのあるオレンジ（やや強い）→ #E76F51
    "6": "#D62828", // 怪獣Lv6: 深紅（強烈で危険）→ #D62828
    "7": "#6A040F", // 怪獣Lv7: 暗赤（ラスボス感）→ #6A040F

    シーン: "#9E9E9E", // シーン: グレートーン（中立的、補助的）→ #9E9E9E
  };

  const barHeight = 32; // 1バーの高さ
  const barMargin = 8; // バー同士の余白
  const axisHeight = 48; // X軸の目安高さ

  const chartHeight = chartData.length * (barHeight + barMargin) + axisHeight;

  return (
    <div className="w-full" style={{ height: `${chartHeight}px` }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          layout="vertical"
          data={chartData}
          margin={{ top: 16, right: 32, left: 80, bottom: 16 }}
        >
          <XAxis type="number" domain={[0, Math.ceil(maxTotal * 1.1)]} />
          <YAxis type="category" dataKey="name" />
          <Tooltip />
          {/* <Legend /> */}
          {sortedLevels.map((level) => (
            <Bar
              key={level}
              dataKey={level}
              stackId="a"
              fill={levelColors[level] ?? "#ccc"}
              name={level === "シーン" ? "シーン" : `レベル${level}`}
              isAnimationActive={true}
              barSize={20}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default HeroLevelBarChartAbsolute;
