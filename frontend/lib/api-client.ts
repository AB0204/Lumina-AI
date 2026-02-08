const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = {
    async detectObjects(imageFile: File) {
        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('labels', JSON.stringify(['clothing', 'shoes', 'accessories']));

        const response = await fetch(`${API_URL}/api/detect`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Detection failed');
        }

        return response.json();
    },

    async searchByText(query: string, limit: number = 10) {
        const response = await fetch(`${API_URL}/api/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query, limit }),
        });

        if (!response.ok) {
            throw new Error('Search failed');
        }

        return response.json();
    },
};
