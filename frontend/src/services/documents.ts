import api from "./api";

export interface DocumentItem {
  id: number;
  filename: string;
  filepath: string;
  created_at: string;
}

export async function fetchDocuments(): Promise<DocumentItem[]> {
  const response = await api.get<DocumentItem[]>('/documents/');
  return response.data;
}

export async function uploadDocument(file: File): Promise<DocumentItem> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data.document;
}
