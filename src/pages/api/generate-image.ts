import { NextApiRequest, NextApiResponse } from "next";
import sharp from "sharp";
import axios from "axios";

interface ImageInput {
  imagePath: string; // URLまたはローカルパス
}

interface GenerateCollageRequest extends NextApiRequest {
  body: {
    images: ImageInput[];
    count: number[];
  };
}

const BG_WIDTH = 1024;
const BG_HEIGHT = 512;
const PADDING = 24;

function cardsPerColumn(cardCount: number): number {
  if (cardCount <= 4)
    return 1;
  else if (cardCount <= 12)
    return 2;
  else if (cardCount <= 24)
    return 3;
  else if (cardCount <= 48)
    return 4;
  else
    return 5;
}

function cardSize(cardCount: number): { width: number, height: number } {
  const heightTmp = Math.floor((BG_HEIGHT - PADDING * 2) / cardsPerColumn(cardCount));
  const widthTmp = Math.floor(heightTmp * 143 / 200);
  // カードの幅が背景の幅を超える場合、幅を調整
  if (widthTmp * Math.ceil(cardCount / cardsPerColumn(cardCount)) + PADDING * 2 > BG_WIDTH) {
    const width = Math.floor((BG_WIDTH - PADDING * 2) / (Math.ceil(cardCount / cardsPerColumn(cardCount))));
    const height = Math.floor(width * 200 / 143);
    return {
      width: width,
      height: height
    };
  } else {
    return {
      width: widthTmp,
      height: heightTmp
    };
  }
}

export default async function handler(
  req: GenerateCollageRequest,
  res: NextApiResponse
) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { images, count } = req.body;

  if (!images || !Array.isArray(images) || !count || !Array.isArray(count)) {
    return res.status(400).json({ error: "Invalid request data" });
  }

  try {
    const CARD_WIDTH = 2 * Math.floor(cardSize(images.length).width / 2);
    const CARD_HEIGHT = 2 * Math.floor(cardSize(images.length).height / 2);
    const row = Math.ceil(images.length / cardsPerColumn(images.length));

    // URLまたはローカルパスから画像を取得してリサイズ
    const fetchImage = async (imagePath: string): Promise<Buffer> => {
      if (imagePath.startsWith("http://") || imagePath.startsWith("https://")) {
        const response = await axios.get(imagePath, { responseType: "arraybuffer" });
        return sharp(Buffer.from(response.data))
          .resize(CARD_WIDTH, CARD_HEIGHT)
          .toBuffer();
      } else {
        return sharp(imagePath).resize(CARD_WIDTH, CARD_HEIGHT).toBuffer();
      }
    };

    const COUNT_WIDTH = 32;

    const generateCountOverlay = async (text: string): Promise<Buffer> => {
      const fontSize = 18;
      const verticalAdjust = 0.35 * fontSize; // 調整量（フォントサイズの35%分）

      const svgText = `
    <svg width="${COUNT_WIDTH}" height="${COUNT_WIDTH}" xmlns="http://www.w3.org/2000/svg">
    <style>
      @font-face {
        font-family: 'goldman';
        url("data:application/font-woff; charset=utf-8; base64,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") format("woff2");
      }
    </style>
      <rect width="${COUNT_WIDTH}" height="${COUNT_WIDTH}" fill="black" rx="4" ry="4"/>
      <text x="50%" y="${COUNT_WIDTH / 2 + verticalAdjust}" 
            font-size="${fontSize}" font-weight="bold"
            text-anchor="middle"
            fill="white" font-family="goldman, sans-serif"
            >
        ${text}
      </text>
    </svg>
  `;
      return await sharp(Buffer.from(svgText)).toBuffer();
    };


    // カード画像と枚数のテキストを重ねて作成
    const cardWithText = await Promise.all(
      images.map(async ({ imagePath }, index) => {
        const cardImage = await fetchImage(imagePath);
        const overlayImage = await generateCountOverlay(count[index].toString());

        // テキストを重ねたカード画像を作成
        return sharp(cardImage)
          .composite([{ input: overlayImage, top: CARD_HEIGHT - COUNT_WIDTH - 5, left: CARD_WIDTH - COUNT_WIDTH - 5 }])
          .toBuffer();
      })
    );

    // 背景画像サイズを計算
    const rows = Math.ceil(images.length / row);

    // カードを配置する位置を計算
    const compositeData = cardWithText.map((buffer, index) => {
      const x = (index % row) * CARD_WIDTH;
      const y = Math.floor(index / row) * CARD_HEIGHT;
      return { input: buffer, left: x + (BG_WIDTH - CARD_WIDTH * row) / 2, top: y + (BG_HEIGHT - CARD_HEIGHT * rows) / 2 };
    });

    // 背景画像を作成し、カードを配置
    const collageBuffer = await sharp({
      create: {
        width: BG_WIDTH,
        height: BG_HEIGHT,
        channels: 3, // RGB
        background: { r: 255, g: 255, b: 255 }, // 白背景
      },
    })
      .composite(compositeData)
      .png()
      .toBuffer();

    res.setHeader("Content-Type", "image/png");
    res.send(collageBuffer);
  } catch (error) {
    if (error instanceof Error) {
      console.error("Error processing images:", error);
    } else {
      console.error("Error processing images:", error);
    }
    res.status(500).json({ error: "Failed to generate collage" });
  }
}

