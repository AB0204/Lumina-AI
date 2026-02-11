export interface DetectionResult {
    label: string;
    score: number;
    box: {
        xmin: number;
        ymin: number;
        xmax: number;
        ymax: number;
    };
}

export interface SearchResult {
    title: string;
    image_url: string;
    product_url?: string;
    price?: number;
    category?: string;
    score: number;
}

export interface ApiResponse<T> {
    data: T;
    message?: string;
    error?: string;
}
