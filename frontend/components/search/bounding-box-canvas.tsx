'use client';

import { useEffect, useRef } from 'react';
import type { DetectionResult } from '@/types/api';

interface BoundingBoxCanvasProps {
    imageUrl: string;
    detections: DetectionResult[];
    className?: string;
}

export function BoundingBoxCanvas({
    imageUrl,
    detections,
    className,
}: BoundingBoxCanvasProps) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const imageRef = useRef<HTMLImageElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const image = imageRef.current;
        if (!canvas || !image) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const drawBoundingBoxes = () => {
            // Set canvas size to match image
            canvas.width = image.naturalWidth;
            canvas.height = image.naturalHeight;

            // Draw image
            ctx.drawImage(image, 0, 0);

            // Draw bounding boxes
            detections.forEach((detection, index) => {
                const { box, label, score } = detection;

                // Calculate box coordinates
                const x = box.xmin * canvas.width;
                const y = box.ymin * canvas.height;
                const width = (box.xmax - box.xmin) * canvas.width;
                const height = (box.ymax - box.ymin) * canvas.height;

                // Generate color based on index
                const colors = [
                    '#667eea', // Purple
                    '#f093fb', // Pink
                    '#4facfe', // Blue
                    '#00f2fe', // Cyan
                    '#43e97b', // Green
                ];
                const color = colors[index % colors.length];

                // Draw box
                ctx.strokeStyle = color;
                ctx.lineWidth = 4;
                ctx.strokeRect(x, y, width, height);

                // Draw label background
                const labelText = `${label} (${(score * 100).toFixed(0)}%)`;
                ctx.font = 'bold 16px Inter, sans-serif';
                const textMetrics = ctx.measureText(labelText);
                const textHeight = 24;
                const padding = 8;

                ctx.fillStyle = color;
                ctx.fillRect(
                    x,
                    y - textHeight - padding,
                    textMetrics.width + padding * 2,
                    textHeight + padding
                );

                // Draw label text
                ctx.fillStyle = '#ffffff';
                ctx.fillText(labelText, x + padding, y - padding);
            });
        };

        image.onload = drawBoundingBoxes;
        if (image.complete) {
            drawBoundingBoxes();
        }
    }, [imageUrl, detections]);

    return (
        <div className={className}>
            <img
                ref={imageRef}
                src={imageUrl}
                alt="Detection source"
                className="hidden"
            />
            <canvas
                ref={canvasRef}
                className="w-full h-auto rounded-xl border border-white/10"
            />
        </div>
    );
}
