import { NextApiRequest, NextApiResponse } from "next";
import sharp from "sharp";
import axios from "axios";
import path from "path";

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

function cardsPerRow(cardCount: number) {
  if (cardCount <= 21) {
    return 7;
  }
  else if (cardCount <= 24) {
    return 8;
  }
  else if (cardCount <= 27) {
    return 9;
  }
  else if (cardCount <= 40) {
    return 10;
  }
  else if (cardCount <= 44) {
    return 11;
  }
  else if (cardCount <= 48) {
    return 12;
  }
  else {
    return 13;
  }
}

function cardWidth(cardCount: number): { width: number, height: number } {
  if (cardCount <= 21) {
    const height = Math.floor((BG_HEIGHT - PADDING * 2) / 3);
    return { width: Math.floor(height * 143 / 200), height };
  }
  else if (cardCount <= 24) {
    const height = Math.floor((BG_HEIGHT - PADDING * 2) / 3);
    return { width: Math.floor(height * 143 / 200), height };
  }
  else if (cardCount <= 27) {
    const width = Math.floor((BG_WIDTH - PADDING * 2) / 9);
    return { width, height: Math.floor(width * 200 / 143) };
  }
  else if (cardCount <= 40) {
    const height = Math.floor((BG_HEIGHT - PADDING * 2) / 4);
    return { width: Math.floor(height * 143 / 200), height };
  }
  else if (cardCount <= 44) {
    const height = Math.floor((BG_HEIGHT - PADDING * 2) / 4);
    return { width: Math.floor(height * 143 / 200), height };
  }
  else if (cardCount <= 48) {
    const width = Math.floor((BG_WIDTH - PADDING * 2) / 12);
    return { width, height: Math.floor(width * 200 / 143) };
  }
  else {
    const width = Math.floor((BG_WIDTH - PADDING * 2) / 13);
    return { width, height: Math.floor(width * 200 / 143) };
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
    const CARD_WIDTH = 2 * Math.floor(cardWidth(images.length).width / 2);
    const CARD_HEIGHT = 2 * Math.floor(cardWidth(images.length).height / 2);
    const row = cardsPerRow(images.length);

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

    // カード画像と枚数のテキストを重ねて作成
    const cardWithText = await Promise.all(
      images.map(async ({ imagePath }, index) => {
        const cardImage = await fetchImage(imagePath);
        const overlayImage = await sharp(path.join(process.cwd(), "public/count_image", `${count[index]}.png`))
          .resize(20, 20)
          .toBuffer()

        // テキストを重ねたカード画像を作成
        return sharp(cardImage)
          .composite([{ input: overlayImage, top: CARD_HEIGHT - 25, left: CARD_WIDTH / 2 - 10 }])
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

