export function LoadingSkeleton() {
    return (
        <div className="space-y-6 animate-pulse">
            {/* Image skeleton */}
            <div className="w-full h-96 bg-white/5 rounded-xl"></div>

            {/* Results skeleton */}
            <div className="grid md:grid-cols-2 gap-4">
                {[1, 2, 3, 4].map((i) => (
                    <div key={i} className="p-6 bg-white/5 rounded-xl space-y-3">
                        <div className="h-6 bg-white/10 rounded w-3/4"></div>
                        <div className="h-4 bg-white/10 rounded w-1/2"></div>
                        <div className="h-4 bg-white/10 rounded w-2/3"></div>
                    </div>
                ))}
            </div>
        </div>
    );
}
