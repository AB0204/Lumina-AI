'use client';

import { useCallback } from 'react';
import { Upload, X, Image as ImageIcon } from 'lucide-react';
import { useImageUpload } from '@/hooks/use-image-upload';
import { cn } from '@/lib/utils';

interface ImageUploadProps {
    onImageSelect?: (file: File) => void;
    className?: string;
}

export function ImageUpload({ onImageSelect, className }: ImageUploadProps) {
    const {
        file,
        preview,
        error,
        handleFileSelect,
        clearImage,
    } = useImageUpload();

    const onDrop = useCallback(
        (e: React.DragEvent<HTMLDivElement>) => {
            e.preventDefault();
            const droppedFile = e.dataTransfer.files[0];
            if (droppedFile) {
                handleFileSelect(droppedFile);
                onImageSelect?.(droppedFile);
            }
        },
        [handleFileSelect, onImageSelect]
    );

    const onFileInputChange = useCallback(
        (e: React.ChangeEvent<HTMLInputElement>) => {
            const selectedFile = e.target.files?.[0];
            if (selectedFile) {
                handleFileSelect(selectedFile);
                onImageSelect?.(selectedFile);
            }
        },
        [handleFileSelect, onImageSelect]
    );

    const handleClear = useCallback(() => {
        clearImage();
    }, [clearImage]);

    return (
        <div className={cn('w-full', className)}>
            {!preview ? (
                <div
                    onDrop={onDrop}
                    onDragOver={(e) => e.preventDefault()}
                    className="relative border-2 border-dashed border-white/20 rounded-xl p-12 text-center hover:border-purple-500/50 transition-all cursor-pointer bg-white/5 backdrop-blur-sm group"
                >
                    <input
                        type="file"
                        accept="image/*"
                        onChange={onFileInputChange}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />

                    <div className="flex flex-col items-center gap-4">
                        <div className="w-16 h-16 bg-purple-500/20 rounded-full flex items-center justify-center group-hover:bg-purple-500/30 transition-colors">
                            <Upload className="w-8 h-8 text-purple-400" />
                        </div>

                        <div>
                            <p className="text-lg font-semibold text-white mb-2">
                                Drop your image here
                            </p>
                            <p className="text-sm text-gray-400">
                                or click to browse • PNG, JPG up to 10MB
                            </p>
                        </div>

                        <div className="flex items-center gap-2 text-xs text-gray-500">
                            <ImageIcon className="w-4 h-4" />
                            <span>Supports fashion images, product photos, and more</span>
                        </div>
                    </div>
                </div>
            ) : (
                <div className="relative rounded-xl overflow-hidden bg-white/5 backdrop-blur-sm border border-white/10">
                    <img
                        src={preview}
                        alt="Preview"
                        className="w-full h-auto max-h-96 object-contain"
                    />

                    <button
                        onClick={handleClear}
                        className="absolute top-4 right-4 w-10 h-10 bg-red-500/80 hover:bg-red-600 text-white rounded-full flex items-center justify-center transition-colors backdrop-blur-sm"
                    >
                        <X className="w-5 h-5" />
                    </button>

                    {file && (
                        <div className="absolute bottom-4 left-4 bg-black/60 backdrop-blur-sm px-4 py-2 rounded-lg">
                            <p className="text-sm text-white font-medium">{file.name}</p>
                            <p className="text-xs text-gray-300">
                                {(file.size / 1024 / 1024).toFixed(2)} MB
                            </p>
                        </div>
                    )}
                </div>
            )}

            {error && (
                <div className="mt-4 p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
                    <p className="text-sm text-red-400">{error}</p>
                </div>
            )}
        </div>
    );
}
