export async function get<T>(path: string, options?: RequestInit): Promise<T[]> {
  const response = await fetch(`/api/proxy/${path}`, options);

  if (response.ok) {
    const data: { data: { rows: T[] } } = await response.json();
    return data.data.rows;
  } else {
    throw new Error(`Request failed (${response.status})`);
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
    throw new Error(`Request failed (${response.status})`);
  }
}
