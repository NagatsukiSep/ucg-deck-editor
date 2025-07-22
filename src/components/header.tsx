"use client";
import Link from "next/link";
import Image from "next/image";

export default function Header() {
  return (
    <header className="border-b px-4 py-3">
      <div className="mx-auto flex max-w-7xl items-center justify-start">
        {/* ロゴ部分 */}
        <Link href="/">
          <Image
            src="/logo.png"
            alt="ULTRA DECK BUILDER  Logo"
            width={154}
            height={77}
            priority
            className="cursor-pointer"
          />
        </Link>

        {/* ナビゲーション部分 */}
        <nav>
          <ul className="flex gap-6 ml-12">
            <li>
              <Link href="/" className="text-black hover:underline">
                Top
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}
