import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import React, { useState } from "react";

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
  const [activeInfo, setActiveInfo] = useState<{
    label: string;
    payload: { name: string; value: number; color?: string }[];
  } | null>(null);
  const levelOrder = ["1", "2", "3", "4_hero", "4", "5", "6", "7", "シーン"];
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
    const orderedLevels = [
      ...levelOrder.filter((level) => level in value),
      ...Object.keys(value)
        .filter((level) => !levelOrder.includes(level))
        .sort((a, b) => a.localeCompare(b)),
    ];
    for (const level of orderedLevels) {
      const count = value[level] ?? 0;
      entry[level] = count;
    }
    chartData.push(entry);
  });

  const levelKeys = new Set<string>();
  chartData.forEach((row) => {
    Object.keys(row).forEach((k) => {
      if (k !== "name") levelKeys.add(k);
    });
  });

  const extraLevels = Array.from(levelKeys)
    .filter((level) => !levelOrder.includes(level))
    .sort((a, b) => a.localeCompare(b));
  const sortedLevels = [...levelOrder, ...extraLevels];

  const levelColors: Record<string, string> = {
    "1": "#AEDFF7", // ヒーローLv1: パステルブルー（軽く爽やか）→ #AEDFF7
    "2": "#7FC8F8", // ヒーローLv2: スカイブルー（少し濃く）→ #7FC8F8
    "3": "#3DA9FC", // ヒーローLv3: 鮮やかなブルー（芯のある強さ）→ #3DA9FC

    "4_hero": "#D4AF37", // ヒーローLv4: 金色 → #D4AF37
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

  const getLevelLabel = (level: string) => {
    if (level === "シーン") return "シーン";
    if (level === "4_hero") return "レベル4";
    return `レベル${level}`;
  };

  const formatTooltipPayload = (
    payload: { name: string; value: number; color?: string }[]
  ) =>
    payload
      .filter((entry) => entry.value > 0)
      .map((entry) => ({
        ...entry,
        label: getLevelLabel(entry.name),
      }));

  const handleChartActivate = (event?: {
    activeLabel?: string;
    activePayload?: { name: string; value: number; color?: string }[];
  }) => {
    if (!event?.activeLabel || !event.activePayload?.length) {
      setActiveInfo(null);
      return;
    }
    setActiveInfo({
      label: event.activeLabel,
      payload: event.activePayload,
    });
  };

  const renderTooltipContent = (
    payload: { name: string; value: number; color?: string }[],
    label: string
  ) => {
    const formatted = formatTooltipPayload(payload);
    if (formatted.length === 0) return null;

    return (
      <div className="rounded-md border bg-background p-3 text-sm shadow-md">
        <div className="font-semibold mb-1">{label}</div>
        <ul className="space-y-1">
          {formatted.map((entry) => (
            <li key={entry.name} className="flex items-center gap-2">
              <span
                className="inline-block h-2.5 w-2.5 rounded-full"
                style={{ backgroundColor: entry.color ?? "#999" }}
              />
              <span className="flex-1">{entry.label}</span>
              <span className="tabular-nums">{entry.value}</span>
            </li>
          ))}
        </ul>
      </div>
    );
  };

  return (
    <div className="w-full">
      <div className="mb-2 md:hidden min-h-[64px]">
        {activeInfo &&
          renderTooltipContent(activeInfo.payload, activeInfo.label)}
      </div>
      <div className="w-full" style={{ height: `${chartHeight}px` }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            layout="vertical"
            data={chartData}
            margin={{ top: 16, right: 32, left: 80, bottom: 16 }}
            onClick={handleChartActivate}
            onTouchStart={handleChartActivate}
            onTouchEnd={() => setActiveInfo(null)}
            onMouseLeave={() => setActiveInfo(null)}
          >
            <XAxis type="number" domain={[0, Math.ceil(maxTotal * 1.1)]} />
            <YAxis type="category" dataKey="name" />
            <Tooltip
              wrapperStyle={{ zIndex: 50, pointerEvents: "none" }}
              content={({ active, payload, label }) =>
                active && payload?.length
                  ? renderTooltipContent(
                      payload as {
                        name: string;
                        value: number;
                        color?: string;
                      }[],
                      label ?? ""
                    )
                  : null
              }
            />
            {/* <Legend /> */}
            {sortedLevels.map((level) => (
              <Bar
                key={level}
                dataKey={level}
                stackId="a"
                fill={levelColors[level] ?? "#ccc"}
                name={getLevelLabel(level)}
                hide={!levelKeys.has(level)}
                isAnimationActive={true}
                barSize={20}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
      <p className="mt-2 text-xs text-muted-foreground md:hidden">
        棒グラフをタップしている間、上に詳細が表示されます。
      </p>
    </div>
  );
};

export default HeroLevelBarChartAbsolute;
