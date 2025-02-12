export async function get<T>(path: string): Promise<T[]> {
  const response = await fetch(`/api/proxy/${path}`);

  if (response.ok) {
    const data: { data: { rows: T[] } } = await response.json();
    return data.data.rows;
  } else {
    console.error("Failed to fetch data:", response.statusText);
    return [];
  }
}

export async function post<T, B>(path: string, body: B): Promise<T[]> {
  const response = await fetch(`/api/proxy/${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (response.ok) {
    const data: { data: { rows: T[] } } = await response.json();
    return data.data.rows;
  } else {
    console.error("Failed to fetch data:", response.statusText);
    return [];
  }
}
