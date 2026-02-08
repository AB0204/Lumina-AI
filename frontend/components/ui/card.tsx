import { cn } from '@/lib/utils';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
    children: React.ReactNode;
}

export function Card({ className, children, ...props }: CardProps) {
    return (
        <div
            className={cn(
                'p-6 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl',
                className
            )}
            {...props}
        >
            {children}
        </div>
    );
}

export function CardHeader({ className, children, ...props }: CardProps) {
    return (
        <div className={cn('mb-4', className)} {...props}>
            {children}
        </div>
    );
}

export function CardTitle({ className, children, ...props }: CardProps) {
    return (
        <h3 className={cn('text-xl font-semibold text-white', className)} {...props}>
            {children}
        </h3>
    );
}

export function CardDescription({ className, children, ...props }: CardProps) {
    return (
        <p className={cn('text-gray-400', className)} {...props}>
            {children}
        </p>
    );
}
