'use client';

import { useState } from 'react';
import Image from 'next/image';
import { ExternalLink, Star } from 'lucide-react';
import type { SearchResult } from '@/types/api';

interface SearchResultsProps {
    results: SearchResult[];
    isLoading?: boolean;
}

export function SearchResults({ results, isLoading }: SearchResultsProps) {
    if (isLoading) {
        return (
            <div className="grid md:grid-cols-3 gap-6 animate-pulse">
                {[1, 2, 3, 4, 5, 6].map((i) => (
                    <div key={i} className="bg-white/5 rounded-xl overflow-hidden">
                        <div className="w-full h-64 bg-white/10"></div>
                        <div className="p-4 space-y-3">
                            <div className="h-4 bg-white/10 rounded w-3/4"></div>
                            <div className="h-3 bg-white/10 rounded w-1/2"></div>
                        </div>
                    </div>
                ))}
            </div>
        );
    }

    if (results.length === 0) {
        return (
            <div className="text-center py-12">
                <p className="text-gray-400 text-lg">No similar products found</p>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-white">
                    Similar Products ({results.length})
                </h2>
                <div className="text-sm text-gray-400">
                    Sorted by similarity score
                </div>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
                {results.map((result, index) => (
                    <div
                        key={index}
                        className="group bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl overflow-hidden hover:border-purple-500/50 transition-all hover:scale-105"
                    >
                        {/* Product Image */}
                        <div className="relative w-full h-64 bg-white/10">
                            {result.image_url ? (
                                <img
                                    src={result.image_url}
                                    alt={result.title || 'Product'}
                                    className="w-full h-full object-cover"
                                />
                            ) : (
                                <div className="w-full h-full flex items-center justify-center text-gray-500">
                                    No Image
                                </div>
                            )}

                            {/* Similarity Badge */}
                            <div className="absolute top-3 right-3 px-3 py-1 bg-purple-500/90 backdrop-blur-sm text-white rounded-full text-sm font-semibold flex items-center gap-1">
                                <Star className="w-4 h-4 fill-current" />
                                {(result.score * 100).toFixed(0)}%
                            </div>
                        </div>

                        {/* Product Info */}
                        <div className="p-4 space-y-3">
                            <h3 className="text-white font-semibold line-clamp-2 group-hover:text-purple-300 transition-colors">
                                {result.title || 'Untitled Product'}
                            </h3>

                            {result.price && (
                                <p className="text-purple-400 font-bold text-lg">
                                    ${result.price}
                                </p>
                            )}

                            {result.category && (
                                <span className="inline-block px-3 py-1 bg-white/10 text-gray-300 rounded-full text-xs">
                                    {result.category}
                                </span>
                            )}

                            {result.product_url && (
                                <a
                                    href={result.product_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="flex items-center gap-2 text-sm text-purple-400 hover:text-purple-300 transition-colors"
                                >
                                    View Product
                                    <ExternalLink className="w-4 h-4" />
                                </a>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
