import sharp from "sharp";
import fs from "fs";
import path from "path";

const OUTPUT_DIR = path.join(process.cwd(), "number_images");
const IMAGE_SIZE = 128;
const VIEW_IMAGE_SIZE = 32
const FONT_SIZE = 18;

const generateSVG = (text: string): string => {
  const verticalAdjust = 0.35 * FONT_SIZE;
  return `
    <svg width="${IMAGE_SIZE}" height="${IMAGE_SIZE}" viewBox="0 0 ${VIEW_IMAGE_SIZE} ${VIEW_IMAGE_SIZE}" xmlns="http://www.w3.org/2000/svg">
      <rect width="${VIEW_IMAGE_SIZE}" height="${VIEW_IMAGE_SIZE}" fill="black" rx="4" ry="4"/>
      <text x="50%" y="${VIEW_IMAGE_SIZE / 2 + verticalAdjust}"
            font-size="${FONT_SIZE}" font-weight="bold"
            text-anchor="middle"
            fill="white" font-family="DejaVu Sans, sans-serif">
        ${text}
      </text>
    </svg>
  `;
};

async function generateImages() {
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR);
  }

  for (let i = 1; i <= 50; i++) {
    const svg = generateSVG(i.toString());
    const buffer = await sharp(Buffer.from(svg))
      .png()
      .toBuffer();

    const filePath = path.join(OUTPUT_DIR, `${i}.png`);
    fs.writeFileSync(filePath, buffer);
    console.log(`Saved: ${filePath}`);
  }
}

generateImages().catch((err) => {
  console.error("Error generating images:", err);
});
