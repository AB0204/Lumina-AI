'use client';

import { useState } from 'react';
import { Sparkles, Loader2, Search } from 'lucide-react';
import Link from 'next/link';
import { ImageUpload } from '@/components/search/image-upload';
import { BoundingBoxCanvas } from '@/components/search/bounding-box-canvas';
import { SearchResults } from '@/components/search/search-results';
import { apiClient } from '@/lib/api-client';
import type { DetectionResult, SearchResult } from '@/types/api';

export default function SearchPage() {
    const [isDetecting, setIsDetecting] = useState(false);
    const [isSearching, setIsSearching] = useState(false);
    const [results, setResults] = useState<DetectionResult[]>([]);
    const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [imagePreview, setImagePreview] = useState<string | null>(null);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const handleImageSelect = async (file: File) => {
        setIsDetecting(true);
        setError(null);
        setResults([]);
        setSearchResults([]);
        setSelectedFile(file);

        // Create preview URL for bounding box canvas
        const reader = new FileReader();
        reader.onloadend = () => {
            setImagePreview(reader.result as string);
        };
        reader.readAsDataURL(file);

        try {
            const response = await apiClient.detectObjects(file);
            setResults(response.detections || []);
        } catch (err) {
            setError('Failed to detect objects. Please try again.');
            console.error(err);
        } finally {
            setIsDetecting(false);
        }
    };

    const handleSearchSimilar = async (detection: DetectionResult) => {
        if (!selectedFile) return;

        setIsSearching(true);
        setError(null);

        try {
            const response = await apiClient.searchSimilar(selectedFile, detection.box);
            setSearchResults(response.results || []);
        } catch (err) {
            setError('Failed to search for similar products. Please try again.');
            console.error(err);
        } finally {
            setIsSearching(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
            {/* Navigation */}
            <nav className="border-b border-white/10 backdrop-blur-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <Link href="/" className="flex items-center gap-2">
                            <Sparkles className="w-6 h-6 text-purple-400" />
                            <span className="text-xl font-bold text-white">Lumina AI</span>
                        </Link>
                    </div>
                </div>
            </nav>

            {/* Main Content */}
            <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="text-center mb-12">
                    <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
                        Visual Search
                    </h1>
                    <p className="text-xl text-gray-300">
                        Upload an image to detect fashion items and find similar products
                    </p>
                </div>

                {/* Upload Section */}
                <div className="mb-12">
                    <ImageUpload onImageSelect={handleImageSelect} />
                </div>

                {/* Loading State */}
                {isDetecting && (
                    <div className="flex flex-col items-center justify-center py-12">
                        <Loader2 className="w-12 h-12 text-purple-400 animate-spin mb-4" />
                        <p className="text-gray-300">Analyzing image with Owlv2...</p>
                    </div>
                )}

                {/* Error State */}
                {error && (
                    <div className="p-6 bg-red-500/10 border border-red-500/20 rounded-xl mb-8">
                        <p className="text-red-400 text-center">{error}</p>
                    </div>
                )}

                {/* Results */}
                {results.length > 0 && (
                    <div className="space-y-8 mb-12">
                        {/* Bounding Box Visualization */}
                        <div>
                            <h2 className="text-2xl font-bold text-white mb-4">
                                Visual Detection
                            </h2>
                            <BoundingBoxCanvas
                                imageUrl={imagePreview!}
                                detections={results}
                                className="mb-6"
                            />
                        </div>

                        {/* Detection Results List */}
                        <div>
                            <h2 className="text-2xl font-bold text-white mb-4">
                                Detected Items ({results.length})
                            </h2>

                            <div className="grid md:grid-cols-2 gap-4">
                                {results.map((result, index) => (
                                    <div
                                        key={index}
                                        className="p-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl hover:border-purple-500/50 transition-colors"
                                    >
                                        <div className="flex justify-between items-start mb-3">
                                            <h3 className="text-lg font-semibold text-white capitalize">
                                                {result.label}
                                            </h3>
                                            <span className="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full text-sm font-medium">
                                                {(result.score * 100).toFixed(1)}%
                                            </span>
                                        </div>

                                        <div className="text-sm text-gray-400 space-y-1 mb-4">
                                            <p>Position: ({result.box.xmin.toFixed(2)}, {result.box.ymin.toFixed(2)})</p>
                                            <p>
                                                Size: {(result.box.xmax - result.box.xmin).toFixed(2)} × {' '}
                                                {(result.box.ymax - result.box.ymin).toFixed(2)}
                                            </p>
                                        </div>

                                        <button
                                            onClick={() => handleSearchSimilar(result)}
                                            disabled={isSearching}
                                            className="w-full px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-600/50 text-white rounded-lg font-semibold transition-colors flex items-center justify-center gap-2"
                                        >
                                            <Search className="w-4 h-4" />
                                            Search Similar Products
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {/* Search Results */}
                {searchResults.length > 0 && (
                    <div className="mb-12">
                        <SearchResults results={searchResults} isLoading={isSearching} />
                    </div>
                )}

                {/* Searching State */}
                {isSearching && (
                    <div className="flex flex-col items-center justify-center py-12">
                        <Loader2 className="w-12 h-12 text-purple-400 animate-spin mb-4" />
                        <p className="text-gray-300">Searching for similar products...</p>
                    </div>
                )}
            </main>
        </div>
    );
}
