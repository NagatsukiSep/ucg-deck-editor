import { NextApiRequest, NextApiResponse } from "next";
import sharp from "sharp";
import axios from "axios";
import path from "path";

interface ImageInput {
  imagePath: string; // URLまたはローカルパス
  count: number; // カードの枚数
  isScene: boolean; // シーンカードかどうか
}

interface GenerateCollageRequest extends NextApiRequest {
  body: {
    images: ImageInput[];
    deckUrl?: string;
  };
}

const BG_WIDTH = 1024;
const BG_HEIGHT = 512;
const PADDING = 24;
const LOGO_WIDTH = 120;
const LOGO_HEIGHT = 60;
const QR_SIZE = 120;

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

  const { images, deckUrl } = req.body;

  if (!images || !Array.isArray(images) || images.length === 0) {
    return res.status(400).json({ error: "Invalid request data" });
  }

  try {
    const CARD_WIDTH = 2 * Math.floor(cardSize(images.length).width / 2);
    const CARD_HEIGHT = 2 * Math.floor(cardSize(images.length).height / 2);
    const row = Math.ceil(images.length / cardsPerColumn(images.length));

    // URLまたはローカルパスから画像を取得してリサイズ
    const fetchImage = async (imagePath: string, isScene: boolean): Promise<Buffer> => {
      if (imagePath.startsWith("http://") || imagePath.startsWith("https://")) {
        const response = await axios.get(imagePath, { responseType: "arraybuffer" });
        return sharp(Buffer.from(response.data))
          .rotate(isScene ? 90 : 0) // シーンカードは90度回転
          .resize(CARD_WIDTH, CARD_HEIGHT)
          .toBuffer();
      } else {
        return sharp(imagePath).resize(CARD_WIDTH, CARD_HEIGHT).toBuffer();
      }
    };

    const COUNT_WIDTH = 32;

    // カード画像と枚数のテキストを重ねて作成
    const cardWithText = await Promise.all(
      images.map(async ({ imagePath, count, isScene }) => {
        const cardImage = await fetchImage(imagePath, isScene);
        const overlayImage = await sharp(path.join(process.cwd(), "public/count_image", `${count}.png`))
          .resize(COUNT_WIDTH, COUNT_WIDTH)
          .toBuffer()

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

    const overlayData = [...compositeData];

    try {
      const logoBuffer = await sharp(path.join(process.cwd(), "public", "logo.png"))
        .resize(LOGO_WIDTH, LOGO_HEIGHT)
        .png()
        .toBuffer();
      overlayData.push({ input: logoBuffer, left: PADDING, top: PADDING });
    } catch (error) {
      console.error("Failed to load logo image:", error);
    }

    if (deckUrl) {
      try {
        const qrResponse = await axios.get(
          `https://api.qrserver.com/v1/create-qr-code/?size=${QR_SIZE}x${QR_SIZE}&data=${encodeURIComponent(deckUrl)}`,
          { responseType: "arraybuffer" }
        );
        const qrBuffer = await sharp(Buffer.from(qrResponse.data))
          .resize(QR_SIZE, QR_SIZE)
          .png()
          .toBuffer();
        overlayData.push({ input: qrBuffer, left: BG_WIDTH - QR_SIZE - PADDING, top: PADDING });
      } catch (error) {
        console.error("Failed to load QR code image:", error);
      }
    }

    // 背景画像を作成し、カードを配置
    const collageBuffer = await sharp({
      create: {
        width: BG_WIDTH,
        height: BG_HEIGHT,
        channels: 3, // RGB
        background: { r: 255, g: 255, b: 255 }, // 白背景
      },
    })
      .composite(overlayData)
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
