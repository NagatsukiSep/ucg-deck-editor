
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
const API_PUBLIC_KEY = process.env.NEXT_PUBLIC_API_PUBLIC_KEY;
const API_SECRET_KEY = process.env.NEXT_PUBLIC_API_SECRET_KEY;

export async function get(path: string): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/${path}`, {
    method: "GET",
    headers: {
      Authorization: `Basic ${btoa(
        `${API_PUBLIC_KEY}:${API_SECRET_KEY}`
      )}`,
    },
  });
  if (response.ok) {
    const data = await response.json();
    return data.data.rows;
  } else {
    console.error("Failed to fetch data:", response.statusText);
    return [];
  }
}

export async function post(path: string, body: any): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Basic ${btoa(
        `${API_PUBLIC_KEY}:${API_SECRET_KEY}`
      )}`,
    },
    body: JSON.stringify(body),
  });
  if (response.ok) {
    const data = await response.json();
    return data.data.rows;
  } else {
    console.log(response);
    console.error("Failed to fetch data:", response.statusText);
    return [];
  }
}