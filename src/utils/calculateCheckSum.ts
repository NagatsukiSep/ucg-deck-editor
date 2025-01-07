import { BASE64_CHARS } from '@/utils/base64Chars';

export function calculateChecksum(encoded: string): string {
  const checksumValue = [...encoded].reduce((sum, char) => {
    const index = BASE64_CHARS.indexOf(char);
    if (index === -1) {
      throw new Error(`Invalid Base64 character: ${char}`);
    }
    return sum + index;
  }, 0) % 64;
  return BASE64_CHARS[checksumValue];
}