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
    id: string;
    score: number;
    metadata: {
        url?: string;
        title?: string;
        [key: string]: any;
    };
}

export interface ApiResponse<T> {
    data: T;
    message?: string;
    error?: string;
}
