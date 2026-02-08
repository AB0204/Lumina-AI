import { useState, useCallback } from 'react';

export interface ImageUploadState {
    file: File | null;
    preview: string | null;
    isUploading: boolean;
    error: string | null;
}

export function useImageUpload() {
    const [state, setState] = useState<ImageUploadState>({
        file: null,
        preview: null,
        isUploading: false,
        error: null,
    });

    const handleFileSelect = useCallback((file: File) => {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            setState((prev) => ({
                ...prev,
                error: 'Please select an image file',
            }));
            return;
        }

        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            setState((prev) => ({
                ...prev,
                error: 'Image size must be less than 10MB',
            }));
            return;
        }

        // Create preview
        const reader = new FileReader();
        reader.onloadend = () => {
            setState({
                file,
                preview: reader.result as string,
                isUploading: false,
                error: null,
            });
        };
        reader.readAsDataURL(file);
    }, []);

    const clearImage = useCallback(() => {
        setState({
            file: null,
            preview: null,
            isUploading: false,
            error: null,
        });
    }, []);

    const setUploading = useCallback((isUploading: boolean) => {
        setState((prev) => ({ ...prev, isUploading }));
    }, []);

    const setError = useCallback((error: string | null) => {
        setState((prev) => ({ ...prev, error }));
    }, []);

    return {
        ...state,
        handleFileSelect,
        clearImage,
        setUploading,
        setError,
    };
}
